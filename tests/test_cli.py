import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout

from philips_sicp import __version__
from philips_sicp.cli import (
    CONFIG_SCHEMA,
    CliConfig,
    build_parser,
    config_from_args,
    load_config_document,
    parse_data_bytes,
    run_config_apply,
    run_config_collect,
)
from philips_sicp.client import (
    POWER_GET_COMMAND,
    POWER_SET_COMMAND,
    VOLUME_MUTE_GET_COMMAND,
    VOLUME_MUTE_SET_COMMAND,
    SicpError,
    SicpTransaction,
)
from philips_sicp.protocol import build_packet, parse_packet


class FakeConfigClient:
    def __init__(self, responses=None):
        self.responses = responses or {}
        self.calls = []

    def transact_with_request(
        self,
        command,
        *parameters,
        expected_response_commands=None,
        expected_response_sizes=None,
    ):
        self.calls.append((command, parameters))
        if expected_response_commands == (0x00,):
            response = parse_packet(build_packet(0x00, 0x06))
        else:
            if command not in self.responses:
                raise SicpError("missing command")
            response_command, response_parameters = self.responses[command]
            response = parse_packet(
                build_packet(response_command, *response_parameters)
            )
        return SicpTransaction(
            request=build_packet(command, *parameters),
            response=response,
            skipped=(),
        )


class CliConfigTests(unittest.TestCase):
    def parse(self, argv):
        return build_parser().parse_args(argv)

    def test_cli_flags_override_env(self):
        args = self.parse(
            [
                "--host",
                "192.0.2.20",
                "--port",
                "5001",
                "--monitor-id",
                "0x02",
                "--group-id",
                "3",
                "--timeout",
                "1.5",
                "--retries",
                "2",
                "--json",
                "--verbose",
                "power",
                "get",
            ]
        )
        config = config_from_args(
            args,
            {
                "PHILIPS_SICP_HOST": "192.0.2.10",
                "PHILIPS_SICP_PORT": "5000",
                "PHILIPS_SICP_MONITOR_ID": "1",
                "PHILIPS_SICP_GROUP_ID": "1",
                "PHILIPS_SICP_TIMEOUT": "2.0",
                "PHILIPS_SICP_RETRIES": "1",
            },
        )
        self.assertEqual(config.host, "192.0.2.20")
        self.assertEqual(config.port, 5001)
        self.assertEqual(config.monitor_id, 2)
        self.assertEqual(config.group_id, 3)
        self.assertEqual(config.timeout, 1.5)
        self.assertEqual(config.retries, 2)
        self.assertTrue(config.json_output)
        self.assertTrue(config.verbose)

    def test_env_vars_apply_when_flags_absent(self):
        args = self.parse(["power", "set", "on"])
        config = config_from_args(
            args,
            {
                "PHILIPS_SICP_HOST": "192.0.2.10",
                "PHILIPS_SICP_PORT": "0x1388",
                "PHILIPS_SICP_MONITOR_ID": "0x01",
                "PHILIPS_SICP_GROUP_ID": "0x00",
                "PHILIPS_SICP_TIMEOUT": "2.5",
                "PHILIPS_SICP_RETRIES": "3",
            },
        )
        self.assertEqual(config.host, "192.0.2.10")
        self.assertEqual(config.port, 5000)
        self.assertEqual(config.monitor_id, 1)
        self.assertEqual(config.group_id, 0)
        self.assertEqual(config.timeout, 2.5)
        self.assertEqual(config.retries, 3)

    def test_missing_host_is_clear_error(self):
        args = self.parse(["power", "get"])
        with self.assertRaisesRegex(ValueError, "host is required"):
            config_from_args(args, {})

    def test_invalid_byte_arg_is_argparse_error(self):
        with self.assertRaises(SystemExit):
            self.parse(["--monitor-id", "256", "--host", "192.0.2.10", "power", "get"])

    def test_version_flag_prints_package_version(self):
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            with self.assertRaises(SystemExit) as context:
                self.parse(["--version"])
        self.assertEqual(context.exception.code, 0)
        self.assertEqual(stdout.getvalue().strip(), f"sicp {__version__}")

    def test_invalid_env_var_is_value_error(self):
        args = self.parse(["power", "get"])
        with self.assertRaisesRegex(ValueError, "PHILIPS_SICP_GROUP_ID"):
            config_from_args(
                args,
                {
                    "PHILIPS_SICP_HOST": "192.0.2.10",
                    "PHILIPS_SICP_GROUP_ID": "256",
                },
            )

    def test_parse_data_bytes_accepts_multiple_formats(self):
        self.assertEqual(parse_data_bytes(["19"]), [0x19])
        self.assertEqual(
            parse_data_bytes(["0xAD", "0x0D", "0", "1", "0"]), [0xAD, 0x0D, 0, 1, 0]
        )
        self.assertEqual(parse_data_bytes(["AD 0D 00 01 00"]), [0xAD, 0x0D, 0, 1, 0])
        self.assertEqual(parse_data_bytes(["AD,0D,00,01,00"]), [0xAD, 0x0D, 0, 1, 0])
        self.assertEqual(parse_data_bytes(["d:25"]), [25])

    def test_parse_data_bytes_rejects_empty_list(self):
        with self.assertRaisesRegex(ValueError, "at least one DATA byte"):
            parse_data_bytes([])

    def test_config_collect_parser(self):
        args = self.parse(
            ["config", "collect", "--continue-on-error", "--only", "power"]
        )
        self.assertEqual(args.group, "config")
        self.assertEqual(args.action, "collect")
        self.assertTrue(args.continue_on_error)
        self.assertEqual(args.only, "power")

    def test_config_apply_parser(self):
        args = self.parse(
            [
                "config",
                "apply",
                "-",
                "--continue-on-error",
                "--ignore-unknown",
                "--only",
                "power",
            ]
        )
        self.assertEqual(args.group, "config")
        self.assertEqual(args.action, "apply")
        self.assertEqual(args.path, "-")
        self.assertTrue(args.continue_on_error)
        self.assertTrue(args.ignore_unknown)
        self.assertEqual(args.only, "power")

    def test_config_collect_json_uses_applyable_schema(self):
        args = self.parse(
            ["--json", "config", "collect", "--only", "power,volume_mute"]
        )
        config = CliConfig(
            host="192.0.2.10",
            port=5000,
            monitor_id=1,
            group_id=0,
            timeout=1.0,
            retries=0,
            json_output=True,
            verbose=False,
        )
        client = FakeConfigClient(
            {
                POWER_GET_COMMAND: (POWER_GET_COMMAND, (0x02,)),
                VOLUME_MUTE_GET_COMMAND: (VOLUME_MUTE_GET_COMMAND, (0x01,)),
            }
        )
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            exit_code = run_config_collect(args, client, config)
        payload = json.loads(stdout.getvalue())
        self.assertEqual(exit_code, 0)
        self.assertEqual(payload["schema"], CONFIG_SCHEMA)
        self.assertEqual(payload["settings"], {"power": "on", "volume_mute": "on"})
        self.assertEqual(payload["errors"], {})

    def test_config_collect_tolerates_missing_commands(self):
        args = self.parse(
            ["--json", "config", "collect", "--only", "power,volume_mute"]
        )
        config = CliConfig(
            host="192.0.2.10",
            port=5000,
            monitor_id=1,
            group_id=0,
            timeout=1.0,
            retries=0,
            json_output=True,
            verbose=False,
        )
        client = FakeConfigClient({POWER_GET_COMMAND: (POWER_GET_COMMAND, (0x02,))})
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            exit_code = run_config_collect(args, client, config)
        payload = json.loads(stdout.getvalue())
        self.assertEqual(exit_code, 0)
        self.assertEqual(payload["settings"], {"power": "on"})
        self.assertEqual(payload["errors"], {"volume_mute": "missing command"})

    def test_config_apply_sends_expected_set_commands(self):
        document = {
            "schema": CONFIG_SCHEMA,
            "settings": {
                "power": "off",
                "volume_mute": "off",
            },
        }
        with tempfile.NamedTemporaryFile("w", encoding="utf-8") as tmp:
            json.dump(document, tmp)
            tmp.flush()
            args = self.parse(["config", "apply", tmp.name])
            config = CliConfig(
                host="192.0.2.10",
                port=5000,
                monitor_id=1,
                group_id=0,
                timeout=1.0,
                retries=0,
                json_output=False,
                verbose=False,
            )
            client = FakeConfigClient()
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = run_config_apply(args, client, config)
        self.assertEqual(exit_code, 0)
        self.assertEqual(
            client.calls,
            [
                (POWER_SET_COMMAND, (0x01,)),
                (VOLUME_MUTE_SET_COMMAND, (0x00,)),
            ],
        )

    def test_config_document_rejects_wrong_schema(self):
        with tempfile.NamedTemporaryFile("w", encoding="utf-8") as tmp:
            json.dump({"schema": "wrong", "settings": {}}, tmp)
            tmp.flush()
            with self.assertRaisesRegex(ValueError, "config schema"):
                load_config_document(tmp.name)


if __name__ == "__main__":
    unittest.main()
