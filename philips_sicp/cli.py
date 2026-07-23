"""Command-line interface for Philips SICP."""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any, TypeVar, cast

from . import __version__
from .client import (
    ANYTILE_ASSIGN_IDS_COMMAND,
    ANYTILE_DISPLAY_MONITOR_ID_SET_COMMAND,
    ANYTILE_GET_COMMAND,
    ANYTILE_RESOLUTION_GET_COMMAND,
    ANYTILE_RESOLUTION_SET_COMMAND,
    ANYTILE_SET_COMMAND,
    APM_STATUS_GET_COMMAND,
    APM_STATUS_SET_COMMAND,
    AUDIO_PARAMETERS_GET_COMMAND,
    AUDIO_PARAMETERS_SET_COMMAND,
    AUTO_SIGNAL_GET_COMMAND,
    AUTO_SIGNAL_SET_COMMAND,
    COLOR_TEMPERATURE_100K_GET_COMMAND,
    COLOR_TEMPERATURE_100K_SET_COMMAND,
    COLOR_TEMPERATURE_GET_COMMAND,
    COLOR_TEMPERATURE_SET_COMMAND,
    DEFAULT_GROUP_ID,
    DEFAULT_MONITOR_ID,
    DEFAULT_PORT,
    DEFAULT_RETRIES,
    DEFAULT_TIMEOUT,
    DISPLAY_ORIENTATION_GET_COMMAND,
    DISPLAY_ORIENTATION_SET_COMMAND,
    ECO_MODE_GET_COMMAND,
    ECO_MODE_SET_COMMAND,
    FACTORY_RESET_COMMAND,
    FAILOVER_GET_COMMAND,
    FAILOVER_SET_COMMAND,
    FAN_SPEED_GET_COMMAND,
    FAN_SPEED_SET_COMMAND,
    FRAME_COMPENSATION_HORIZONTAL_GET_COMMAND,
    FRAME_COMPENSATION_HORIZONTAL_SET_COMMAND,
    FRAME_COMPENSATION_VERTICAL_GET_COMMAND,
    FRAME_COMPENSATION_VERTICAL_SET_COMMAND,
    GROUP_ID_GET_COMMAND,
    GROUP_ID_SET_COMMAND,
    HUMAN_SENSOR_GET_COMMAND,
    HUMAN_SENSOR_SET_COMMAND,
    INFORMATION_OSD_GET_COMMAND,
    INFORMATION_OSD_SET_COMMAND,
    INPUT_SOURCE_GET_COMMAND,
    INPUT_SOURCE_SET_COMMAND,
    IR_LOCK_GET_COMMAND,
    IR_LOCK_SET_COMMAND,
    KEYPAD_LOCK_GET_COMMAND,
    KEYPAD_LOCK_SET_COMMAND,
    LIGHT_SENSOR_GET_COMMAND,
    LIGHT_SENSOR_SET_COMMAND,
    MEMC_EFFECT_GET_COMMAND,
    MEMC_EFFECT_SET_COMMAND,
    MONITOR_ID_SET_COMMAND,
    MONITOR_RESTART_COMMAND,
    NOISE_REDUCTION_GET_COMMAND,
    NOISE_REDUCTION_SET_COMMAND,
    OFF_TIMER_GET_COMMAND,
    OFF_TIMER_SET_COMMAND,
    OPERATING_HOURS_COMMAND,
    OPERATING_HOURS_ITEM,
    OSD_ROTATING_GET_COMMAND,
    OSD_ROTATING_SET_COMMAND,
    PICTURE_FORMAT_GET_COMMAND,
    PICTURE_FORMAT_SET_COMMAND,
    PICTURE_STYLE_GET_COMMAND,
    PICTURE_STYLE_SET_COMMAND,
    PIXEL_SHIFT_GET_COMMAND,
    PIXEL_SHIFT_SET_COMMAND,
    PORTS_LOCK_GET_COMMAND,
    PORTS_LOCK_SET_COMMAND,
    POWER_COLD_START_GET_COMMAND,
    POWER_COLD_START_SET_COMMAND,
    POWER_GET_COMMAND,
    POWER_ON_LOGO_GET_COMMAND,
    POWER_ON_LOGO_SET_COMMAND,
    POWER_SAVING_MODE_GET_COMMAND,
    POWER_SAVING_MODE_SET_COMMAND,
    POWER_SAVING_MODE_STATUS_GET_COMMAND,
    POWER_SAVING_MODE_STATUS_SET_COMMAND,
    POWER_SET_COMMAND,
    RGB_PARAMETERS_GET_COMMAND,
    RGB_PARAMETERS_SET_COMMAND,
    SCAN_CONVERSION_GET_COMMAND,
    SCAN_CONVERSION_SET_COMMAND,
    SCAN_MODE_GET_COMMAND,
    SCAN_MODE_SET_COMMAND,
    SCHEDULING_GET_COMMAND,
    SCHEDULING_SET_COMMAND,
    SERIAL_CODE_GET_COMMAND,
    SWITCH_ON_DELAY_GET_COMMAND,
    SWITCH_ON_DELAY_SET_COMMAND,
    TEMPERATURE_GET_COMMAND,
    TILING_GET_COMMAND,
    TILING_SET_COMMAND,
    TOUCH_FEATURE_GET_COMMAND,
    TOUCH_FEATURE_SET_COMMAND,
    VIDEO_PARAMETERS_GET_COMMAND,
    VIDEO_PARAMETERS_SET_COMMAND,
    VIDEO_SIGNAL_PRESENT_COMMAND,
    VOLUME_GET_COMMAND,
    VOLUME_LIMIT_AUDIO_GET_COMMAND,
    VOLUME_LIMIT_AUDIO_SET_COMMAND,
    VOLUME_LIMIT_SPEAKER_GET_COMMAND,
    VOLUME_LIMIT_SPEAKER_SET_COMMAND,
    VOLUME_MUTE_GET_COMMAND,
    VOLUME_MUTE_SET_COMMAND,
    VOLUME_SET_COMMAND,
    VOLUME_STEP_COMMAND,
    SicpClient,
    SicpError,
    TilingState,
    anytile_resolution_name_to_value,
    anytile_resolution_value_to_name,
    apm_status_name_to_value,
    apm_status_value_to_name,
    audio_parameter_value_to_display,
    auto_signal_name_to_value,
    bool_to_mute_value,
    bool_to_power_value,
    build_anytile_parameters,
    build_input_source_osd_style,
    build_tiling_set_values,
    color_temperature_name_to_value,
    color_temperature_value_to_name,
    decode_anytile_report,
    decode_anytile_resolution_report,
    decode_apm_status_report,
    decode_audio_parameters_report,
    decode_auto_signal_report,
    decode_color_temperature_100k_report,
    decode_color_temperature_report,
    decode_display_orientation_report,
    decode_eco_mode_report,
    decode_failover_report,
    decode_fan_speed_report,
    decode_frame_compensation_horizontal_report,
    decode_frame_compensation_vertical_report,
    decode_group_id_report,
    decode_human_sensor_report,
    decode_information_osd_report,
    decode_input_source_report,
    decode_ir_lock_report,
    decode_keypad_lock_report,
    decode_light_sensor_report,
    decode_memc_effect_report,
    decode_noise_reduction_report,
    decode_off_timer_report,
    decode_operating_hours_report,
    decode_osd_rotating_report,
    decode_picture_format_report,
    decode_picture_style_report,
    decode_pixel_shift_report,
    decode_ports_lock_report,
    decode_power_cold_start_report,
    decode_power_on_logo_report,
    decode_power_report,
    decode_power_saving_mode_report,
    decode_power_saving_mode_status_report,
    decode_rgb_parameters_report,
    decode_scan_conversion_report,
    decode_scan_mode_report,
    decode_scheduling_report,
    decode_serial_code_report,
    decode_switch_on_delay_report,
    decode_temperature_report,
    decode_tiling_report,
    decode_touch_feature_report,
    decode_video_parameters_report,
    decode_video_signal_present_report,
    decode_volume_limit_report,
    decode_volume_mute_report,
    decode_volume_report,
    display_orientation_auto_rotate_name_to_value,
    display_orientation_auto_rotate_value_to_name,
    display_orientation_image_all_name_to_value,
    display_orientation_image_all_value_to_name,
    display_orientation_osd_rotation_name_to_value,
    display_orientation_osd_rotation_value_to_name,
    display_orientation_window_name_to_value,
    display_orientation_window_value_to_name,
    eco_mode_name_to_value,
    eco_mode_value_to_name,
    encode_tiling_wall_size,
    failover_source_name_to_value,
    failover_source_value_to_name,
    fan_speed_name_to_value,
    fan_speed_value_to_name,
    gamma_name_to_value,
    gamma_value_to_name,
    group_id_name_to_value,
    group_id_value_to_name,
    human_sensor_name_to_value,
    human_sensor_value_to_name,
    information_osd_name_to_value,
    information_osd_value_to_name,
    input_source_name_to_value,
    input_source_value_to_name,
    light_sensor_name_to_value,
    light_sensor_value_to_name,
    lock_state_name_to_value,
    lock_state_value_to_name,
    memc_effect_name_to_value,
    memc_effect_value_to_name,
    monitor_id_name_to_value,
    monitor_restart_target_name_to_value,
    monitor_restart_target_value_to_name,
    noise_reduction_name_to_value,
    noise_reduction_value_to_name,
    off_timer_name_to_value,
    off_timer_value_to_name,
    osd_rotating_name_to_value,
    osd_rotating_value_to_name,
    parse_audio_parameter_value,
    parse_scheduling_time,
    picture_format_name_to_value,
    picture_format_value_to_name,
    picture_style_name_to_value,
    picture_style_value_to_name,
    pixel_shift_name_to_value,
    pixel_shift_value_to_name,
    ports_lock_name_to_value,
    ports_lock_value_to_name,
    power_cold_start_name_to_value,
    power_on_logo_name_to_value,
    power_on_logo_value_to_name,
    power_saving_mode_name_to_value,
    power_saving_mode_status_name_to_value,
    power_saving_mode_status_value_to_name,
    power_saving_mode_value_to_name,
    require_ack,
    scan_conversion_name_to_value,
    scan_conversion_value_to_name,
    scan_mode_name_to_value,
    scan_mode_value_to_name,
    scheduling_days_name_to_value,
    scheduling_days_value_to_names,
    scheduling_source_name_to_value,
    scheduling_source_value_to_name,
    switch_on_delay_name_to_value,
    switch_on_delay_value_to_name,
    tiling_enable_name_to_value,
    tiling_frame_comp_name_to_value,
    tiling_position_name_to_value,
    touch_feature_name_to_value,
    touch_feature_value_to_name,
    validate_color_temperature_100k_steps,
    validate_display_orientation_values,
    validate_failover_priorities,
    validate_percentage,
    validate_scheduling_page,
    validate_scheduling_tag,
    validate_volume_level,
    validate_volume_limits,
    volume_step_name_to_value,
    volume_step_value_to_name,
)
from .protocol import SicpPacket, build_packet, hex_bytes

ENV_HOST = "PHILIPS_SICP_HOST"
ENV_PORT = "PHILIPS_SICP_PORT"
ENV_MONITOR_ID = "PHILIPS_SICP_MONITOR_ID"
ENV_GROUP_ID = "PHILIPS_SICP_GROUP_ID"
ENV_TIMEOUT = "PHILIPS_SICP_TIMEOUT"
ENV_RETRIES = "PHILIPS_SICP_RETRIES"


@dataclass(frozen=True)
class CliConfig:
    host: str
    port: int
    monitor_id: int
    group_id: int
    timeout: float
    retries: int
    json_output: bool
    verbose: bool


CONFIG_SCHEMA = "philips-sicp-config-v1"
T = TypeVar("T")


@dataclass(frozen=True)
class ConfigEntry:
    key: str
    label: str
    getter: Callable[[SicpClient], Any]
    setter: Callable[[SicpClient, Any], None]
    formatter: Callable[[Any], str] = str


def parse_int(value: str) -> int:
    try:
        return int(value, 0)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"invalid integer: {value}") from exc


def parse_byte(value: str) -> int:
    parsed = parse_int(value)
    if parsed < 0 or parsed > 0xFF:
        raise argparse.ArgumentTypeError("value must be in range 0..255")
    return parsed


def parse_uint16(value: str) -> int:
    parsed = parse_int(value)
    if parsed < 0 or parsed > 0xFFFF:
        raise argparse.ArgumentTypeError("value must be in range 0..65535")
    return parsed


def parse_percentage(value: str) -> int:
    try:
        return validate_percentage(parse_int(value), "value")
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def parse_tiling_enable(value: str) -> int:
    try:
        return tiling_enable_name_to_value(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def parse_anytile_resolution(value: str) -> int:
    try:
        return anytile_resolution_name_to_value(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def parse_switch_on_delay(value: str) -> int:
    try:
        return switch_on_delay_name_to_value(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def parse_tiling_frame_comp(value: str) -> int:
    try:
        return tiling_frame_comp_name_to_value(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def parse_tiling_position(value: str) -> str:
    normalized = value.strip().lower()
    if normalized in ("keep", "keep-previous", "previous", "unchanged"):
        return normalized
    try:
        parsed = parse_int(value)
    except argparse.ArgumentTypeError as exc:
        raise argparse.ArgumentTypeError(
            "tiling position must be an integer or keep"
        ) from exc
    if parsed < 0 or parsed > 0xFF:
        raise argparse.ArgumentTypeError("tiling position must be in range 0..255")
    return value


def parse_volume_level(value: str) -> int:
    try:
        return validate_volume_level(parse_int(value))
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def parse_volume_step(value: str) -> int:
    try:
        return volume_step_name_to_value(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def parse_audio_parameter(value: str) -> int:
    try:
        return parse_audio_parameter_value(value, "audio parameter")
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def parse_display_orientation_auto_rotate(value: str) -> int:
    try:
        return display_orientation_auto_rotate_name_to_value(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def parse_display_orientation_osd_rotation(value: str) -> int:
    try:
        return display_orientation_osd_rotation_name_to_value(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def parse_display_orientation_image_all(value: str) -> int:
    try:
        return display_orientation_image_all_name_to_value(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def parse_display_orientation_window(value: str) -> int:
    try:
        return display_orientation_window_name_to_value(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def parse_scan_mode(value: str) -> int:
    try:
        return scan_mode_name_to_value(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def parse_pixel_shift(value: str) -> int:
    try:
        return pixel_shift_name_to_value(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def parse_color_temperature_100k_steps(value: str) -> int:
    try:
        return validate_color_temperature_100k_steps(parse_int(value))
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def parse_off_timer_hours(value: str) -> int:
    try:
        return off_timer_name_to_value(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def parse_power_saving_mode_status(value: str) -> int:
    try:
        return power_saving_mode_status_name_to_value(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def parse_apm_status(value: str) -> int:
    try:
        return apm_status_name_to_value(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def parse_eco_mode(value: str) -> int:
    try:
        return eco_mode_name_to_value(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def parse_picture_style(value: str) -> int:
    try:
        return picture_style_name_to_value(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def parse_picture_format(value: str) -> int:
    try:
        return picture_format_name_to_value(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def parse_group_id_value(value: str) -> int:
    try:
        return group_id_name_to_value(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def parse_monitor_id_value(value: str) -> int:
    try:
        return monitor_id_name_to_value(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def parse_ports_lock_state(value: str) -> int:
    try:
        return ports_lock_name_to_value(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def parse_information_osd_value(value: str) -> int:
    try:
        return information_osd_name_to_value(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def parse_scheduling_page_arg(value: str) -> int:
    try:
        return validate_scheduling_page(parse_int(value))
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def parse_scheduling_time_arg(value: str) -> tuple[int, int]:
    try:
        return parse_scheduling_time(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def parse_scheduling_source_arg(value: str) -> int:
    try:
        return scheduling_source_name_to_value(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def parse_scheduling_days_arg(value: str) -> int:
    try:
        return scheduling_days_name_to_value(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def parse_scheduling_tag_arg(value: str) -> int:
    try:
        tag = validate_scheduling_tag(parse_int(value))
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc
    if tag is None:
        raise argparse.ArgumentTypeError("scheduling tag must be in range 1..7")
    return tag


def parse_data_bytes(values: list[str]) -> list[int]:
    parsed: list[int] = []
    for value in values:
        parts = value.replace(",", " ").split()
        for part in parts:
            parsed.append(parse_data_byte(part))
    if not parsed:
        raise ValueError("at least one DATA byte is required")
    return parsed


def parse_data_byte(value: str) -> int:
    normalized = value.strip().lower()
    if normalized.startswith("d:"):
        return parse_byte(normalized[2:])
    if normalized.startswith("0x"):
        return parse_byte(normalized)
    try:
        parsed = int(normalized, 16)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"invalid DATA byte: {value}") from exc
    if parsed < 0 or parsed > 0xFF:
        raise argparse.ArgumentTypeError("DATA byte must be in range 00..FF")
    return parsed


def parse_port(value: str) -> int:
    parsed = parse_int(value)
    if parsed <= 0 or parsed > 65535:
        raise argparse.ArgumentTypeError("port must be in range 1..65535")
    return parsed


def parse_positive_float(value: str) -> float:
    try:
        parsed = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"invalid number: {value}") from exc
    if parsed <= 0:
        raise argparse.ArgumentTypeError("value must be positive")
    return parsed


def parse_nonnegative_int(value: str) -> int:
    parsed = parse_int(value)
    if parsed < 0:
        raise argparse.ArgumentTypeError("value must be >= 0")
    return parsed


def env_or_default(
    args: argparse.Namespace,
    attr: str,
    env: Mapping[str, str],
    env_name: str,
    default: T,
    parser: Callable[[str], T],
) -> T:
    value = getattr(args, attr)
    if value is not None:
        return cast(T, value)
    if env_name in env:
        try:
            return parser(env[env_name])
        except argparse.ArgumentTypeError as exc:
            raise ValueError(f"{env_name}: {exc}") from exc
    return default


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sicp",
        description="Philips SICP command-line client",
    )
    parser.add_argument("--host", help=f"monitor IP/host, or {ENV_HOST}")
    parser.add_argument("--port", type=parse_port, help=f"default: {DEFAULT_PORT}")
    parser.add_argument(
        "--monitor-id",
        type=parse_byte,
        help=f"monitor ID byte, or {ENV_MONITOR_ID}",
    )
    parser.add_argument(
        "--group-id",
        type=parse_byte,
        help=f"group ID byte, or {ENV_GROUP_ID}",
    )
    parser.add_argument(
        "--timeout",
        type=parse_positive_float,
        help=f"socket timeout seconds, default: {DEFAULT_TIMEOUT}",
    )
    parser.add_argument(
        "--retries",
        type=parse_nonnegative_int,
        help=f"retry count after timeout/failure, default: {DEFAULT_RETRIES}",
    )
    parser.add_argument("--json", action="store_true", help="print JSON output")
    parser.add_argument("--verbose", action="store_true", help="print packet details")
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    subcommands = parser.add_subparsers(dest="group", required=True)
    power = subcommands.add_parser("power", help="power-state commands")
    power_subcommands = power.add_subparsers(dest="action", required=True)
    power_subcommands.add_parser("get", help="read power state")
    power_set = power_subcommands.add_parser("set", help="set power state")
    power_set.add_argument("state", choices=("on", "off"))
    cold_start = power_subcommands.add_parser(
        "cold-start",
        help="power state after cold start",
    )
    cold_start_subcommands = cold_start.add_subparsers(
        dest="cold_start_action",
        required=True,
    )
    cold_start_subcommands.add_parser("get", help="read cold-start power state")
    cold_start_set = cold_start_subcommands.add_parser(
        "set",
        help="set cold-start power state",
    )
    cold_start_set.add_argument("state", choices=("off", "on", "last"))

    input_source = subcommands.add_parser(
        "input-source",
        help="input-source commands",
    )
    input_source_subcommands = input_source.add_subparsers(
        dest="action",
        required=True,
    )
    input_source_subcommands.add_parser("get", help="read input source")
    input_source_set = input_source_subcommands.add_parser(
        "set",
        help="set input source",
    )
    input_source_set.add_argument(
        "source",
        help="source name or byte, for example hdmi, hdmi2, display-port1, 0x0D",
    )
    input_source_set.add_argument(
        "--playlist",
        type=parse_byte,
        default=0,
        help="playlist or URL slot byte, default: 0",
    )
    input_source_set.add_argument(
        "--display-style",
        choices=("source-label", "reserved"),
        default="source-label",
        help="OSD source-info display style, default: source-label",
    )
    input_source_set.add_argument(
        "--do-not-switch",
        action="store_true",
        help="set OSD style bit 6",
    )
    input_source_set.add_argument(
        "--mute-style",
        type=parse_byte,
        default=0,
        help="mute style byte, default: 0",
    )

    auto_signal = subcommands.add_parser(
        "auto-signal",
        help="auto signal detecting commands",
    )
    auto_signal_subcommands = auto_signal.add_subparsers(
        dest="action",
        required=True,
    )
    auto_signal_subcommands.add_parser("get", help="read auto signal detecting mode")
    auto_signal_set = auto_signal_subcommands.add_parser(
        "set",
        help="set auto signal detecting mode",
    )
    auto_signal_set.add_argument(
        "mode",
        choices=("off", "all", "reserved", "pc-only", "video-only", "failover"),
    )

    failover = subcommands.add_parser(
        "failover",
        aliases=("fallover",),
        help="failover priority commands",
    )
    failover_subcommands = failover.add_subparsers(dest="action", required=True)
    failover_subcommands.add_parser("get", help="read failover priority list")
    failover_set = failover_subcommands.add_parser(
        "set",
        help="set failover priority list",
    )
    failover_set.add_argument(
        "sources",
        nargs="+",
        help="priority sources, for example: hdmi component display-port dvi-d",
    )

    monitor = subcommands.add_parser(
        "monitor",
        help="monitor-level commands",
    )
    monitor_subcommands = monitor.add_subparsers(dest="action", required=True)
    monitor_restart = monitor_subcommands.add_parser(
        "restart",
        help="restart/reboot the monitor",
    )
    monitor_restart.add_argument(
        "target",
        nargs="?",
        default="android",
        choices=("android", "scalar", "scaler"),
        help="target system to restart, default: android",
    )

    temperature = subcommands.add_parser(
        "temperature",
        help="temperature sensor commands",
    )
    temperature_subcommands = temperature.add_subparsers(
        dest="action",
        required=True,
    )
    temperature_subcommands.add_parser("get", help="read temperature sensors")

    fan_speed = subcommands.add_parser(
        "fan-speed",
        help="fan speed commands",
    )
    fan_speed_subcommands = fan_speed.add_subparsers(
        dest="action",
        required=True,
    )
    fan_speed_subcommands.add_parser("get", help="read fan speed")
    fan_speed_set = fan_speed_subcommands.add_parser("set", help="set fan speed")
    fan_speed_set.add_argument(
        "speed",
        choices=("off", "auto", "low", "middle", "medium", "high"),
    )

    volume = subcommands.add_parser("volume", help="volume and audio commands")
    volume_subcommands = volume.add_subparsers(dest="action", required=True)
    volume_subcommands.add_parser("get", help="read speaker/audio volume")
    volume_set = volume_subcommands.add_parser("set", help="set speaker/audio volume")
    volume_set.add_argument("--speaker", type=parse_volume_level, required=True)
    volume_set.add_argument("--audio", type=parse_volume_level)
    volume_step = volume_subcommands.add_parser("step", help="step volume up/down")
    volume_step.add_argument("--speaker", type=parse_volume_step, required=True)
    volume_step.add_argument("--audio", type=parse_volume_step)

    volume_limit = volume_subcommands.add_parser(
        "limit",
        help="speaker/audio volume limit commands",
    )
    volume_limit_targets = volume_limit.add_subparsers(dest="target", required=True)
    for target in ("speaker", "audio"):
        limit_target = volume_limit_targets.add_parser(
            target,
            help=f"{target} volume limit commands",
        )
        limit_subcommands = limit_target.add_subparsers(
            dest="limit_action", required=True
        )
        limit_subcommands.add_parser("get", help=f"read {target} volume limits")
        limit_set = limit_subcommands.add_parser(
            "set", help=f"set {target} volume limits"
        )
        limit_set.add_argument(
            "--min", dest="minimum", type=parse_volume_level, required=True
        )
        limit_set.add_argument(
            "--max", dest="maximum", type=parse_volume_level, required=True
        )
        limit_set.add_argument(
            "--switch-on",
            type=parse_volume_level,
            required=True,
        )

    volume_audio = volume_subcommands.add_parser(
        "audio",
        help="treble/bass audio parameter commands",
    )
    volume_audio_subcommands = volume_audio.add_subparsers(
        dest="audio_action",
        required=True,
    )
    volume_audio_subcommands.add_parser("get", help="read treble and bass")
    volume_audio_set = volume_audio_subcommands.add_parser(
        "set",
        help="set treble and bass",
    )
    volume_audio_set.add_argument("--treble", type=parse_audio_parameter, required=True)
    volume_audio_set.add_argument("--bass", type=parse_audio_parameter, required=True)

    volume_mute = volume_subcommands.add_parser("mute", help="volume mute commands")
    volume_mute_subcommands = volume_mute.add_subparsers(
        dest="mute_action",
        required=True,
    )
    volume_mute_subcommands.add_parser("get", help="read volume mute")
    volume_mute_set = volume_mute_subcommands.add_parser("set", help="set volume mute")
    volume_mute_set.add_argument("state", choices=("off", "on"))

    video_signal = subcommands.add_parser(
        "video-signal",
        help="video signal present commands",
    )
    video_signal_subcommands = video_signal.add_subparsers(
        dest="action",
        required=True,
    )
    video_signal_subcommands.add_parser("get", help="read video signal status")

    lock = subcommands.add_parser(
        "lock",
        help="IR remote and keypad lock commands",
    )
    lock_targets = lock.add_subparsers(dest="target", required=True)
    lock_state_choices = (
        "unlock-all",
        "lock-all",
        "lock-all-but-power",
        "lock-all-but-volume",
        "lock-all-except-power-volume",
    )

    ir_lock = lock_targets.add_parser("ir", help="IR remote lock commands")
    ir_lock_subcommands = ir_lock.add_subparsers(dest="action", required=True)
    ir_lock_subcommands.add_parser("get", help="read IR remote lock state")
    ir_lock_set = ir_lock_subcommands.add_parser("set", help="set IR remote lock state")
    ir_lock_set.add_argument(
        "state",
        choices=(*lock_state_choices, "primary", "secondary"),
    )

    keypad_lock = lock_targets.add_parser("keypad", help="keypad lock commands")
    keypad_lock_subcommands = keypad_lock.add_subparsers(dest="action", required=True)
    keypad_lock_subcommands.add_parser("get", help="read keypad lock state")
    keypad_lock_set = keypad_lock_subcommands.add_parser(
        "set",
        help="set keypad lock state",
    )
    keypad_lock_set.add_argument("state", choices=lock_state_choices)

    video = subcommands.add_parser(
        "video",
        help="video parameter commands",
    )
    video_subcommands = video.add_subparsers(dest="target", required=True)

    video_parameters = video_subcommands.add_parser(
        "parameters",
        help="brightness, color, contrast, sharpness, tint, black level, gamma",
    )
    video_parameters_subcommands = video_parameters.add_subparsers(
        dest="action",
        required=True,
    )
    video_parameters_subcommands.add_parser("get", help="read video parameters")
    video_parameters_set = video_parameters_subcommands.add_parser(
        "set",
        help="set video parameters",
    )
    video_parameters_set.add_argument(
        "--brightness",
        type=parse_percentage,
        required=True,
    )
    video_parameters_set.add_argument("--color", type=parse_percentage, required=True)
    video_parameters_set.add_argument(
        "--contrast", type=parse_percentage, required=True
    )
    video_parameters_set.add_argument(
        "--sharpness",
        type=parse_percentage,
        required=True,
    )
    video_parameters_set.add_argument("--tint", type=parse_percentage, required=True)
    video_parameters_set.add_argument(
        "--black-level",
        type=parse_percentage,
        required=True,
    )
    video_parameters_set.add_argument(
        "--gamma",
        choices=("native", "s-gamma", "2.2", "2.4", "dicom"),
        required=True,
    )

    picture_format = video_subcommands.add_parser(
        "picture-format",
        help="picture format commands",
    )
    picture_format_subcommands = picture_format.add_subparsers(
        dest="action",
        required=True,
    )
    picture_format_subcommands.add_parser("get", help="read picture format")
    picture_format_set = picture_format_subcommands.add_parser(
        "set",
        help="set picture format",
    )
    picture_format_set.add_argument(
        "format",
        type=parse_picture_format,
        help="normal, custom, real, full, 21:9, dynamic, or 16:9",
    )

    color_temperature = video_subcommands.add_parser(
        "color-temperature",
        help="color temperature preset commands",
    )
    color_temperature_subcommands = color_temperature.add_subparsers(
        dest="action",
        required=True,
    )
    color_temperature_subcommands.add_parser(
        "get",
        help="read color temperature preset",
    )
    color_temperature_set = color_temperature_subcommands.add_parser(
        "set",
        help="set color temperature preset",
    )
    color_temperature_set.add_argument(
        "temperature",
        choices=(
            "user1",
            "native",
            "11000k",
            "10000k",
            "9300k",
            "7500k",
            "6500k",
            "5770k",
            "5500k",
            "5000k",
            "4000k",
            "3400k",
            "3350k",
            "3000k",
            "2800k",
            "2600k",
            "1850k",
            "user2",
        ),
    )

    rgb = video_subcommands.add_parser(
        "rgb",
        help="RGB gain and offset commands",
    )
    rgb_subcommands = rgb.add_subparsers(dest="action", required=True)
    rgb_subcommands.add_parser("get", help="read RGB parameters")
    rgb_set = rgb_subcommands.add_parser("set", help="set RGB parameters")
    rgb_set.add_argument("--red-gain", type=parse_byte, required=True)
    rgb_set.add_argument("--green-gain", type=parse_byte, required=True)
    rgb_set.add_argument("--blue-gain", type=parse_byte, required=True)
    rgb_set.add_argument("--red-offset", type=parse_byte, required=True)
    rgb_set.add_argument("--green-offset", type=parse_byte, required=True)
    rgb_set.add_argument("--blue-offset", type=parse_byte, required=True)

    color_temperature_100k = video_subcommands.add_parser(
        "color-temperature-100k",
        help="color temperature 100K step commands",
    )
    color_temperature_100k_subcommands = color_temperature_100k.add_subparsers(
        dest="action",
        required=True,
    )
    color_temperature_100k_subcommands.add_parser(
        "get",
        help="read color temperature 100K step value",
    )
    color_temperature_100k_set = color_temperature_100k_subcommands.add_parser(
        "set",
        help="set color temperature 100K step value",
    )
    color_temperature_100k_set.add_argument(
        "steps",
        type=parse_color_temperature_100k_steps,
    )

    power_saving = subcommands.add_parser(
        "power-saving",
        help="power saving mode commands",
    )
    power_saving_subcommands = power_saving.add_subparsers(
        dest="action",
        required=True,
    )
    power_saving_subcommands.add_parser(
        "get",
        help="read smart power saving mode",
    )
    power_saving_set = power_saving_subcommands.add_parser(
        "set",
        help="set smart power saving mode",
    )
    power_saving_set.add_argument(
        "mode",
        choices=("off", "low", "medium", "high"),
    )

    operating_hours = subcommands.add_parser(
        "operating-hours",
        help="operating hours commands",
    )
    operating_hours_subcommands = operating_hours.add_subparsers(
        dest="action",
        required=True,
    )
    operating_hours_subcommands.add_parser("get", help="read operating hours")

    tiling = subcommands.add_parser(
        "tiling",
        help="tiling/video wall commands",
    )
    tiling_subcommands = tiling.add_subparsers(dest="action", required=True)
    tiling_subcommands.add_parser("get", help="read tiling settings")
    tiling_set = tiling_subcommands.add_parser("set", help="set tiling settings")
    tiling_set.add_argument("--enable", type=parse_tiling_enable, required=True)
    tiling_set.add_argument(
        "--frame-comp",
        type=parse_tiling_frame_comp,
        default="keep",
        help="yes, no, or keep; default: keep",
    )
    tiling_set.add_argument(
        "--position",
        type=parse_tiling_position,
        default="keep",
        help="position number or keep; default: keep",
    )
    tiling_set.add_argument("--h-monitors", type=parse_int)
    tiling_set.add_argument("--v-monitors", type=parse_int)
    tiling_set.add_argument(
        "--wall-size",
        type=parse_byte,
        help="raw DATA[4] wall-size value; default: keep",
    )
    tiling_set.add_argument(
        "--zero-bezel",
        action="store_true",
        help="use 15x10 zero-bezel wall limits/formula instead of 5x5",
    )

    switch_on_delay = subcommands.add_parser(
        "switch-on-delay",
        help="switch-on delay for tiling commands",
    )
    switch_on_delay_subcommands = switch_on_delay.add_subparsers(
        dest="action",
        required=True,
    )
    switch_on_delay_subcommands.add_parser(
        "get",
        help="read switch-on delay",
    )
    switch_on_delay_set = switch_on_delay_subcommands.add_parser(
        "set",
        help="set switch-on delay",
    )
    switch_on_delay_set.add_argument(
        "delay",
        type=parse_switch_on_delay,
        help="off, auto, seconds, or raw byte",
    )

    frame_compensation = subcommands.add_parser(
        "frame-compensation",
        help="frame compensation value commands",
    )
    frame_compensation.add_argument(
        "axis",
        choices=("horizontal", "vertical"),
        help="frame compensation axis",
    )
    frame_compensation_subcommands = frame_compensation.add_subparsers(
        dest="action",
        required=True,
    )
    frame_compensation_subcommands.add_parser(
        "get",
        help="read frame compensation value",
    )
    frame_compensation_set = frame_compensation_subcommands.add_parser(
        "set",
        help="set frame compensation value",
    )
    frame_compensation_set.add_argument(
        "value",
        type=parse_byte,
        help="frame compensation value in range 0..255",
    )

    anytile = subcommands.add_parser(
        "anytile",
        help="AnyTile/custom canvas tiling commands",
    )
    anytile_subcommands = anytile.add_subparsers(dest="action", required=True)
    anytile_subcommands.add_parser("get", help="read AnyTile canvas settings")
    anytile_set = anytile_subcommands.add_parser("set", help="set AnyTile canvas")
    anytile_set.add_argument("--enable", type=parse_tiling_enable, required=True)
    anytile_set.add_argument("--rotation", type=parse_uint16, required=True)
    anytile_set.add_argument("--h-start", type=parse_uint16, required=True)
    anytile_set.add_argument("--v-start", type=parse_uint16, required=True)
    anytile_set.add_argument("--h-size", type=parse_uint16, required=True)
    anytile_set.add_argument("--v-size", type=parse_uint16, required=True)

    anytile_resolution = anytile_subcommands.add_parser(
        "resolution",
        help="AnyTile resolution mode commands",
    )
    anytile_resolution_subcommands = anytile_resolution.add_subparsers(
        dest="resolution_action",
        required=True,
    )
    anytile_resolution_subcommands.add_parser("get", help="read resolution mode")
    anytile_resolution_set = anytile_resolution_subcommands.add_parser(
        "set",
        help="set resolution mode",
    )
    anytile_resolution_set.add_argument(
        "mode",
        type=parse_anytile_resolution,
        help="default, fhd, uhd4k, or raw byte",
    )

    anytile_assign = anytile_subcommands.add_parser(
        "assign-id",
        help="assign monitor and group IDs over IP",
    )
    anytile_assign.add_argument("--monitor-id", type=parse_byte, required=True)
    anytile_assign.add_argument("--group-id", type=parse_byte, required=True)

    anytile_display_id = anytile_subcommands.add_parser(
        "display-id",
        help="display monitor ID command",
    )
    anytile_display_id_subcommands = anytile_display_id.add_subparsers(
        dest="display_id_action",
        required=True,
    )
    anytile_display_id_set = anytile_display_id_subcommands.add_parser(
        "set",
        help="set displayed monitor ID",
    )
    anytile_display_id_set.add_argument("monitor_id", type=parse_byte)

    power_saving_status = subcommands.add_parser(
        "power-saving-status",
        help="power saving mode status commands",
    )
    power_saving_status_subcommands = power_saving_status.add_subparsers(
        dest="action",
        required=True,
    )
    power_saving_status_subcommands.add_parser(
        "get",
        help="read power saving mode status",
    )
    power_saving_status_set = power_saving_status_subcommands.add_parser(
        "set",
        help="set power saving mode status",
    )
    power_saving_status_set.add_argument(
        "status",
        type=parse_power_saving_mode_status,
        help=(
            "rgb-off-video-off, rgb-off-video-on, rgb-on-video-off, "
            "rgb-on-video-on, mode-1, mode-2, mode-3, or mode-4"
        ),
    )

    apm_status = subcommands.add_parser(
        "apm-status",
        help="advanced power management status commands",
    )
    apm_status_subcommands = apm_status.add_subparsers(
        dest="action",
        required=True,
    )
    apm_status_subcommands.add_parser(
        "get",
        help="read APM status",
    )
    apm_status_set = apm_status_subcommands.add_parser(
        "set",
        help="set APM status",
    )
    apm_status_set.add_argument(
        "status",
        type=parse_apm_status,
        help="off, on, mode-1, or mode-2",
    )

    serial_code = subcommands.add_parser(
        "serial-code",
        help="serial code commands",
    )
    serial_code_subcommands = serial_code.add_subparsers(
        dest="action",
        required=True,
    )
    serial_code_subcommands.add_parser("get", help="read serial code")

    light_sensor = subcommands.add_parser(
        "light-sensor",
        help="light sensor commands",
    )
    light_sensor_subcommands = light_sensor.add_subparsers(
        dest="action",
        required=True,
    )
    light_sensor_subcommands.add_parser("get", help="read light sensor state")
    light_sensor_set = light_sensor_subcommands.add_parser(
        "set",
        help="set light sensor state",
    )
    light_sensor_set.add_argument("state", choices=("off", "on"))

    osd_rotating = subcommands.add_parser(
        "osd-rotating",
        help="OSD rotating commands",
    )
    osd_rotating_subcommands = osd_rotating.add_subparsers(
        dest="action",
        required=True,
    )
    osd_rotating_subcommands.add_parser("get", help="read OSD rotating state")
    osd_rotating_set = osd_rotating_subcommands.add_parser(
        "set",
        help="set OSD rotating state",
    )
    osd_rotating_set.add_argument("state", choices=("off", "on"))

    display_orientation = subcommands.add_parser(
        "display-orientation",
        help="display orientation commands",
    )
    display_orientation_subcommands = display_orientation.add_subparsers(
        dest="action",
        required=True,
    )
    display_orientation_subcommands.add_parser(
        "get",
        help="read display orientation",
    )
    display_orientation_set = display_orientation_subcommands.add_parser(
        "set",
        help="set display orientation",
    )
    display_orientation_set.add_argument(
        "--auto-rotate",
        type=parse_display_orientation_auto_rotate,
        required=True,
    )
    display_orientation_set.add_argument(
        "--osd",
        type=parse_display_orientation_osd_rotation,
        required=True,
        help="OSD rotation: landscape or portrait",
    )
    display_orientation_set.add_argument(
        "--image-all",
        type=parse_display_orientation_image_all,
        required=True,
        help="image-all rotation: off, on, clockwise, or counter-clockwise",
    )
    for window in ("window1", "window2", "window3", "window4"):
        display_orientation_set.add_argument(
            f"--{window}",
            type=parse_display_orientation_window,
            required=True,
            help=f"{window} image rotation: off or on",
        )

    touch_feature = subcommands.add_parser(
        "touch-feature",
        help="touch feature commands",
    )
    touch_feature_subcommands = touch_feature.add_subparsers(
        dest="action",
        required=True,
    )
    touch_feature_subcommands.add_parser("get", help="read touch feature state")
    touch_feature_set = touch_feature_subcommands.add_parser(
        "set",
        help="set touch feature state",
    )
    touch_feature_set.add_argument("state", choices=("off", "on"))

    noise_reduction = subcommands.add_parser(
        "noise-reduction",
        help="noise reduction commands",
    )
    noise_reduction_subcommands = noise_reduction.add_subparsers(
        dest="action",
        required=True,
    )
    noise_reduction_subcommands.add_parser("get", help="read noise reduction level")
    noise_reduction_set = noise_reduction_subcommands.add_parser(
        "set",
        help="set noise reduction level",
    )
    noise_reduction_set.add_argument(
        "level",
        choices=("off", "low", "middle", "medium", "high", "default"),
    )

    scan_mode = subcommands.add_parser(
        "scan-mode",
        help="scan mode commands",
    )
    scan_mode_subcommands = scan_mode.add_subparsers(
        dest="action",
        required=True,
    )
    scan_mode_subcommands.add_parser("get", help="read scan mode")
    scan_mode_set = scan_mode_subcommands.add_parser("set", help="set scan mode")
    scan_mode_set.add_argument(
        "mode",
        type=parse_scan_mode,
        help="over-scan, under-scan, off, custom-0..custom-25, or raw byte",
    )

    scan_conversion = subcommands.add_parser(
        "scan-conversion",
        help="scan conversion commands",
    )
    scan_conversion_subcommands = scan_conversion.add_subparsers(
        dest="action",
        required=True,
    )
    scan_conversion_subcommands.add_parser("get", help="read scan conversion")
    scan_conversion_set = scan_conversion_subcommands.add_parser(
        "set",
        help="set scan conversion",
    )
    scan_conversion_set.add_argument(
        "mode",
        choices=("progressive", "interlace", "interlaced"),
    )

    pixel_shift = subcommands.add_parser(
        "pixel-shift",
        help="pixel shift commands",
    )
    pixel_shift_subcommands = pixel_shift.add_subparsers(
        dest="action",
        required=True,
    )
    pixel_shift_subcommands.add_parser("get", help="read pixel shift")
    pixel_shift_set = pixel_shift_subcommands.add_parser("set", help="set pixel shift")
    pixel_shift_set.add_argument(
        "value",
        type=parse_pixel_shift,
        help="off, auto, seconds 10..900 by 10, or raw byte",
    )

    memc = subcommands.add_parser(
        "memc",
        help="MEMC effect / smoothing commands",
    )
    memc_subcommands = memc.add_subparsers(
        dest="action",
        required=True,
    )
    memc_subcommands.add_parser("get", help="read MEMC effect level")
    memc_set = memc_subcommands.add_parser(
        "set",
        help="set MEMC effect level",
    )
    memc_set.add_argument(
        "level",
        choices=("off", "low", "medium", "high"),
    )

    information_osd = subcommands.add_parser(
        "information-osd",
        help="information OSD commands",
    )
    information_osd_subcommands = information_osd.add_subparsers(
        dest="action",
        required=True,
    )
    information_osd_subcommands.add_parser("get", help="read information OSD value")
    information_osd_set = information_osd_subcommands.add_parser(
        "set",
        help="set information OSD value",
    )
    information_osd_set.add_argument(
        "value",
        type=parse_information_osd_value,
        help="off or 1..60",
    )

    human_sensor = subcommands.add_parser(
        "human-sensor",
        help="human sensor commands",
    )
    human_sensor_subcommands = human_sensor.add_subparsers(
        dest="action",
        required=True,
    )
    human_sensor_subcommands.add_parser("get", help="read human sensor state")
    human_sensor_set = human_sensor_subcommands.add_parser(
        "set",
        help="set human sensor state",
    )
    human_sensor_set.add_argument(
        "state",
        choices=(
            "off",
            "10-mins",
            "20-mins",
            "30-mins",
            "40-mins",
            "50-mins",
            "60-mins",
        ),
    )

    factory_reset = subcommands.add_parser(
        "factory-reset",
        help="factory reset commands",
    )
    factory_reset_subcommands = factory_reset.add_subparsers(
        dest="action",
        required=True,
    )
    factory_reset_subcommands.add_parser("set", help="perform factory reset")

    power_on_logo = subcommands.add_parser(
        "power-on-logo",
        help="power on logo commands",
    )
    power_on_logo_subcommands = power_on_logo.add_subparsers(
        dest="action",
        required=True,
    )
    power_on_logo_subcommands.add_parser("get", help="read power on logo state")
    power_on_logo_set = power_on_logo_subcommands.add_parser(
        "set",
        help="set power on logo state",
    )
    power_on_logo_set.add_argument("state", choices=("off", "on", "user"))

    off_timer = subcommands.add_parser(
        "off-timer",
        help="off timer commands",
    )
    off_timer_subcommands = off_timer.add_subparsers(
        dest="action",
        required=True,
    )
    off_timer_subcommands.add_parser("get", help="read off timer value")
    off_timer_set = off_timer_subcommands.add_parser("set", help="set off timer")
    off_timer_set.add_argument(
        "hours",
        type=parse_off_timer_hours,
        help="off, 0, or 1..24 hours; also accepts forms like 5h or 5-hours",
    )

    eco_mode = subcommands.add_parser(
        "eco-mode",
        help="ECO mode commands",
    )
    eco_mode_subcommands = eco_mode.add_subparsers(
        dest="action",
        required=True,
    )
    eco_mode_subcommands.add_parser("get", help="read ECO mode")
    eco_mode_set = eco_mode_subcommands.add_parser("set", help="set ECO mode")
    eco_mode_set.add_argument(
        "mode",
        type=parse_eco_mode,
        help="low-power-standby or normal",
    )

    picture_style = subcommands.add_parser(
        "picture-style",
        help="picture style commands",
    )
    picture_style_subcommands = picture_style.add_subparsers(
        dest="action",
        required=True,
    )
    picture_style_subcommands.add_parser("get", help="read picture style")
    picture_style_set = picture_style_subcommands.add_parser(
        "set",
        help="set picture style",
    )
    picture_style_set.add_argument(
        "style",
        type=parse_picture_style,
        help=(
            "highbright, srgb, vivid, natural, standard, video, "
            "static-signage, text, energy-saving, soft, or user"
        ),
    )

    group_id = subcommands.add_parser(
        "group-id",
        help="display group ID commands",
    )
    group_id_subcommands = group_id.add_subparsers(
        dest="action",
        required=True,
    )
    group_id_subcommands.add_parser("get", help="read display group ID")
    group_id_set = group_id_subcommands.add_parser("set", help="set display group ID")
    group_id_set.add_argument(
        "group_id",
        type=parse_group_id_value,
        help="1..254, 0x01..0xFE, or off",
    )

    monitor_id = subcommands.add_parser(
        "monitor-id",
        help="display monitor ID commands",
    )
    monitor_id_subcommands = monitor_id.add_subparsers(
        dest="action",
        required=True,
    )
    monitor_id_set = monitor_id_subcommands.add_parser(
        "set",
        help="set display monitor ID",
    )
    monitor_id_set.add_argument(
        "monitor_id",
        type=parse_monitor_id_value,
        help="1..255 or 0x01..0xFF",
    )

    ports_lock = subcommands.add_parser(
        "ports-lock",
        help="MicroSD and USB ports lock commands",
    )
    ports_lock_subcommands = ports_lock.add_subparsers(
        dest="action",
        required=True,
    )
    ports_lock_subcommands.add_parser(
        "get",
        help="read MicroSD and USB ports lock state",
    )
    ports_lock_set = ports_lock_subcommands.add_parser(
        "set",
        help="set MicroSD and USB ports lock state",
    )
    ports_lock_set.add_argument(
        "state",
        type=parse_ports_lock_state,
        help="unlocked or locked",
    )

    schedule = subcommands.add_parser(
        "schedule",
        help="scheduling parameter commands",
    )
    schedule_subcommands = schedule.add_subparsers(
        dest="action",
        required=True,
    )
    schedule_get = schedule_subcommands.add_parser(
        "get",
        help="read scheduling parameters for a page",
    )
    schedule_get.add_argument("page", type=parse_scheduling_page_arg)
    schedule_set = schedule_subcommands.add_parser(
        "set",
        help="set scheduling parameters for a page",
    )
    schedule_set.add_argument("page", type=parse_scheduling_page_arg)
    schedule_state = schedule_set.add_mutually_exclusive_group(required=True)
    schedule_state.add_argument(
        "--enabled",
        action="store_true",
        help="enable the scheduling page",
    )
    schedule_state.add_argument(
        "--disabled",
        action="store_true",
        help="disable the scheduling page",
    )
    schedule_set.add_argument(
        "--start",
        type=parse_scheduling_time_arg,
        required=True,
        help="start time as HH:MM, or null",
    )
    schedule_set.add_argument(
        "--end",
        type=parse_scheduling_time_arg,
        required=True,
        help="end time as HH:MM, or null",
    )
    schedule_set.add_argument(
        "--source",
        type=parse_scheduling_source_arg,
        required=True,
        help="input source name, 0xNN, or null",
    )
    schedule_set.add_argument(
        "--days",
        type=parse_scheduling_days_arg,
        required=True,
        help="days such as every-day, weekdays, monday,friday, or 0xNN",
    )
    schedule_set.add_argument(
        "--tag",
        type=parse_scheduling_tag_arg,
        help="optional playlist/bookmark/file tag 1..7",
    )

    config_cmd = subcommands.add_parser(
        "config",
        help="collect and apply display configuration",
    )
    config_subcommands = config_cmd.add_subparsers(dest="action", required=True)
    config_collect = config_subcommands.add_parser(
        "collect",
        help="collect safe get/set configuration settings",
    )
    config_collect.add_argument(
        "--continue-on-error",
        action="store_true",
        help=(
            "accepted for compatibility; collect already continues after "
            "per-setting failures"
        ),
    )
    config_collect.add_argument(
        "--only",
        help="comma-separated config setting keys to collect",
    )
    config_apply = config_subcommands.add_parser(
        "apply",
        help="apply a JSON configuration from a file or stdin",
    )
    config_apply.add_argument("path", help="JSON configuration path, or - for stdin")
    config_apply.add_argument(
        "--continue-on-error",
        action="store_true",
        help="continue applying after per-setting failures",
    )
    config_apply.add_argument(
        "--ignore-unknown",
        action="store_true",
        help="ignore JSON settings that this CLI does not know how to apply",
    )
    config_apply.add_argument(
        "--only",
        help="comma-separated config setting keys to apply",
    )

    raw = subcommands.add_parser(
        "raw",
        help="generic raw DATA[] commands",
    )
    raw_subcommands = raw.add_subparsers(dest="action", required=True)
    raw_data = raw_subcommands.add_parser(
        "data",
        help="send DATA[] bytes; packet framing is generated automatically",
    )
    raw_data.add_argument(
        "data",
        nargs="+",
        help='DATA[] hex bytes, for example: 19, AD, or "AD 0D 00 01 00"',
    )
    return parser


def config_from_args(args: argparse.Namespace, env: Mapping[str, str]) -> CliConfig:
    host = args.host or env.get(ENV_HOST)
    if not host:
        raise ValueError(f"host is required; pass --host or set {ENV_HOST}")

    return CliConfig(
        host=host,
        port=env_or_default(args, "port", env, ENV_PORT, DEFAULT_PORT, parse_port),
        monitor_id=env_or_default(
            args,
            "monitor_id",
            env,
            ENV_MONITOR_ID,
            DEFAULT_MONITOR_ID,
            parse_byte,
        ),
        group_id=env_or_default(
            args,
            "group_id",
            env,
            ENV_GROUP_ID,
            DEFAULT_GROUP_ID,
            parse_byte,
        ),
        timeout=env_or_default(
            args,
            "timeout",
            env,
            ENV_TIMEOUT,
            DEFAULT_TIMEOUT,
            parse_positive_float,
        ),
        retries=env_or_default(
            args,
            "retries",
            env,
            ENV_RETRIES,
            DEFAULT_RETRIES,
            parse_nonnegative_int,
        ),
        json_output=args.json,
        verbose=args.verbose,
    )


def packet_dict(packet: SicpPacket | None) -> dict[str, object] | None:
    return None if packet is None else packet.to_dict()


def print_result(payload: dict[str, object], config: CliConfig) -> None:
    if config.json_output:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return

    print(payload["message"])
    if config.verbose:
        print(f"Request: {payload['request_raw']}")
        response = payload.get("response")
        if isinstance(response, dict):
            print(f"Response: {response['raw']}")
            print(
                "Parsed: "
                f"msg_size={response['msg_size']} "
                f"monitor_id=0x{response['monitor_id']:02X} "
                f"group_id=0x{response['group_id']:02X} "
                f"command={format_command(response['command'])} "
                f"parameters={response['parameters']} "
                f"checksum=0x{response['checksum']:02X}"
            )
        skipped = payload.get("skipped")
        if isinstance(skipped, list) and skipped:
            print("Skipped:")
            for packet in skipped:
                print(
                    f"  {packet['raw']} (command={format_command(packet['command'])})"
                )


def format_command(command: object) -> str:
    if command is None:
        return "None"
    if isinstance(command, int):
        return f"0x{command:02X}"
    return str(command)


def run_power_get(client: SicpClient, config: CliConfig) -> int:
    transaction = client.transact_with_request(
        POWER_GET_COMMAND,
        expected_response_commands=(POWER_GET_COMMAND,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Power get did not return a response")
    is_on = decode_power_report(transaction.response)
    state = "on" if is_on else "off"
    print_result(
        {
            "command": "power get",
            "power": state,
            "message": f"Power: {state}",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_power_set(client: SicpClient, state: str, config: CliConfig) -> int:
    on = state == "on"
    transaction = client.transact_with_request(
        POWER_SET_COMMAND,
        bool_to_power_value(on),
        expected_response_commands=(0x00,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Power set did not return a response")
    require_ack(transaction.response)
    print_result(
        {
            "command": "power set",
            "requested_power": state,
            "status": "ACK",
            "message": f"Power set: {state} (ACK)",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_power_cold_start_get(client: SicpClient, config: CliConfig) -> int:
    transaction = client.transact_with_request(
        POWER_COLD_START_GET_COMMAND,
        expected_response_commands=(POWER_COLD_START_GET_COMMAND,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Cold-start power get did not return a response")
    state = decode_power_cold_start_report(transaction.response)
    print_result(
        {
            "command": "power cold-start get",
            "cold_start_power": state,
            "message": f"Cold-start power: {state}",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_power_cold_start_set(
    client: SicpClient,
    state: str,
    config: CliConfig,
) -> int:
    transaction = client.transact_with_request(
        POWER_COLD_START_SET_COMMAND,
        power_cold_start_name_to_value(state),
        expected_response_commands=(0x00,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Cold-start power set did not return a response")
    require_ack(transaction.response)
    print_result(
        {
            "command": "power cold-start set",
            "requested_cold_start_power": state,
            "status": "ACK",
            "message": f"Cold-start power set: {state} (ACK)",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_input_source_get(client: SicpClient, config: CliConfig) -> int:
    transaction = client.transact_with_request(
        INPUT_SOURCE_GET_COMMAND,
        expected_response_commands=(INPUT_SOURCE_GET_COMMAND,),
        expected_response_sizes=(9,),
    )
    if transaction.response is None:
        raise SicpError("Input-source get did not return a response")
    state = decode_input_source_report(transaction.response)
    print_result(
        {
            "command": "input-source get",
            "input_source": state.to_dict(),
            "message": (
                f"Input source: {state.source_name} "
                f"(playlist={state.playlist}, "
                f"display-style={state.display_style}, "
                f"do-not-switch={str(state.do_not_switch).lower()}, "
                f"mute-style=0x{state.mute_style:02X})"
            ),
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_input_source_set(
    client: SicpClient,
    source: str,
    playlist: int,
    display_style: str,
    do_not_switch: bool,
    mute_style: int,
    config: CliConfig,
) -> int:
    source_value = input_source_name_to_value(source)
    source_name = input_source_value_to_name(source_value)
    osd_style = build_input_source_osd_style(
        do_not_switch=do_not_switch,
        display_style=display_style,
    )
    transaction = client.transact_with_request(
        INPUT_SOURCE_SET_COMMAND,
        source_value,
        playlist,
        osd_style,
        mute_style,
        expected_response_commands=(0x00,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Input-source set did not return a response")
    require_ack(transaction.response)
    print_result(
        {
            "command": "input-source set",
            "requested_input_source": {
                "source": source_value,
                "source_name": source_name,
                "playlist": playlist,
                "osd_style": osd_style,
                "display_style": display_style,
                "do_not_switch": do_not_switch,
                "mute_style": mute_style,
            },
            "status": "ACK",
            "message": (
                f"Input source set: {source_name} "
                f"(playlist={playlist}, display-style={display_style}, ACK)"
            ),
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_auto_signal_get(client: SicpClient, config: CliConfig) -> int:
    transaction = client.transact_with_request(
        AUTO_SIGNAL_GET_COMMAND,
        expected_response_commands=(AUTO_SIGNAL_GET_COMMAND,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Auto-signal get did not return a response")
    mode = decode_auto_signal_report(transaction.response)
    print_result(
        {
            "command": "auto-signal get",
            "auto_signal": mode,
            "message": f"Auto signal: {mode}",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_auto_signal_set(client: SicpClient, mode: str, config: CliConfig) -> int:
    value = auto_signal_name_to_value(mode)
    transaction = client.transact_with_request(
        AUTO_SIGNAL_SET_COMMAND,
        value,
        expected_response_commands=(0x00,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Auto-signal set did not return a response")
    require_ack(transaction.response)
    print_result(
        {
            "command": "auto-signal set",
            "requested_auto_signal": mode,
            "status": "ACK",
            "message": f"Auto signal set: {mode} (ACK)",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_failover_get(client: SicpClient, config: CliConfig) -> int:
    transaction = client.transact_with_request(
        FAILOVER_GET_COMMAND,
        expected_response_commands=(FAILOVER_GET_COMMAND,),
    )
    if transaction.response is None:
        raise SicpError("Failover get did not return a response")
    state = decode_failover_report(transaction.response)
    print_result(
        {
            "command": "failover get",
            "failover": state.to_dict(),
            "message": "Failover: " + ", ".join(state.priority_names),
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_failover_set(
    client: SicpClient,
    sources: list[str],
    config: CliConfig,
) -> int:
    values = tuple(failover_source_name_to_value(source) for source in sources)
    validate_failover_priorities(values)
    transaction = client.transact_with_request(
        FAILOVER_SET_COMMAND,
        *values,
        expected_response_commands=(0x00,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Failover set did not return a response")
    require_ack(transaction.response)
    names = [failover_source_value_to_name(value) for value in values]
    print_result(
        {
            "command": "failover set",
            "requested_failover": {
                "priorities": list(values),
                "priority_names": names,
            },
            "status": "ACK",
            "message": "Failover set: " + ", ".join(names) + " (ACK)",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_monitor_restart(
    client: SicpClient,
    target: str,
    config: CliConfig,
) -> int:
    target_value = monitor_restart_target_name_to_value(target)
    target_name = monitor_restart_target_value_to_name(target_value)
    transaction = client.transact_with_request(
        MONITOR_RESTART_COMMAND,
        target_value,
        expected_response_commands=(0x00,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Monitor restart did not return a response")
    require_ack(transaction.response)
    print_result(
        {
            "command": "monitor restart",
            "target": target_name,
            "status": "ACK",
            "message": f"Monitor restart: {target_name} (ACK)",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_temperature_get(client: SicpClient, config: CliConfig) -> int:
    transaction = client.transact_with_request(
        TEMPERATURE_GET_COMMAND,
        expected_response_commands=(TEMPERATURE_GET_COMMAND,),
        expected_response_sizes=(6, 7),
    )
    if transaction.response is None:
        raise SicpError("Temperature get did not return a response")
    state = decode_temperature_report(transaction.response)
    print_result(
        {
            "command": "temperature get",
            "temperature": state.to_dict(),
            "message": (
                "Temperature: "
                + ", ".join(f"{value} C" for value in state.sensors_celsius)
                + f" (highest={state.highest_celsius} C)"
            ),
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_fan_speed_get(client: SicpClient, config: CliConfig) -> int:
    transaction = client.transact_with_request(
        FAN_SPEED_GET_COMMAND,
        expected_response_commands=(FAN_SPEED_GET_COMMAND,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Fan-speed get did not return a response")
    speed = decode_fan_speed_report(transaction.response)
    print_result(
        {
            "command": "fan-speed get",
            "fan_speed": speed,
            "message": f"Fan speed: {speed}",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_fan_speed_set(client: SicpClient, speed: str, config: CliConfig) -> int:
    value = fan_speed_name_to_value(speed)
    transaction = client.transact_with_request(
        FAN_SPEED_SET_COMMAND,
        value,
        expected_response_commands=(0x00,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Fan-speed set did not return a response")
    require_ack(transaction.response)
    canonical = fan_speed_value_to_name(value)
    print_result(
        {
            "command": "fan-speed set",
            "requested_fan_speed": canonical,
            "status": "ACK",
            "message": f"Fan speed set: {canonical} (ACK)",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_volume_get(client: SicpClient, config: CliConfig) -> int:
    transaction = client.transact_with_request(
        VOLUME_GET_COMMAND,
        expected_response_commands=(VOLUME_GET_COMMAND,),
        expected_response_sizes=(6, 7),
    )
    if transaction.response is None:
        raise SicpError("Volume get did not return a response")
    state = decode_volume_report(transaction.response)
    audio = "not reported" if state.audio is None else f"{state.audio}%"
    print_result(
        {
            "command": "volume get",
            "volume": state.to_dict(),
            "message": f"Volume: speaker={state.speaker}%, audio={audio}",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_volume_set(
    args: argparse.Namespace, client: SicpClient, config: CliConfig
) -> int:
    parameters = [args.speaker]
    if args.audio is not None:
        parameters.append(args.audio)
    transaction = client.transact_with_request(
        VOLUME_SET_COMMAND,
        *parameters,
        expected_response_commands=(0x00,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Volume set did not return a response")
    require_ack(transaction.response)
    audio = "not sent" if args.audio is None else f"{args.audio}%"
    print_result(
        {
            "command": "volume set",
            "requested_volume": {
                "speaker": args.speaker,
                "audio": args.audio,
            },
            "status": "ACK",
            "message": f"Volume set: speaker={args.speaker}%, audio={audio} (ACK)",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_volume_step(
    args: argparse.Namespace, client: SicpClient, config: CliConfig
) -> int:
    parameters = [args.speaker]
    if args.audio is not None:
        parameters.append(args.audio)
    transaction = client.transact_with_request(
        VOLUME_STEP_COMMAND,
        *parameters,
        expected_response_commands=(0x00,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Volume step did not return a response")
    require_ack(transaction.response)
    speaker = volume_step_value_to_name(args.speaker)
    audio = None if args.audio is None else volume_step_value_to_name(args.audio)
    print_result(
        {
            "command": "volume step",
            "requested_volume_step": {
                "speaker": speaker,
                "audio": audio,
            },
            "status": "ACK",
            "message": (
                f"Volume step: speaker={speaker}, "
                f"audio={audio if audio is not None else 'not sent'} (ACK)"
            ),
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def volume_limit_command_pair(target: str) -> tuple[int, int]:
    if target == "speaker":
        return VOLUME_LIMIT_SPEAKER_GET_COMMAND, VOLUME_LIMIT_SPEAKER_SET_COMMAND
    if target == "audio":
        return VOLUME_LIMIT_AUDIO_GET_COMMAND, VOLUME_LIMIT_AUDIO_SET_COMMAND
    raise ValueError("volume limit target must be speaker or audio")


def run_volume_limit_get(
    client: SicpClient,
    target: str,
    config: CliConfig,
) -> int:
    get_command, _ = volume_limit_command_pair(target)
    transaction = client.transact_with_request(
        get_command,
        expected_response_commands=(get_command,),
        expected_response_sizes=(8,),
    )
    if transaction.response is None:
        raise SicpError("Volume limit get did not return a response")
    state = decode_volume_limit_report(transaction.response, target=target)
    print_result(
        {
            "command": f"volume limit {target} get",
            "target": target,
            "volume_limit": state.to_dict(),
            "message": (
                f"Volume limit {target}: min={state.minimum}%, "
                f"max={state.maximum}%, switch-on={state.switch_on}%"
            ),
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_volume_limit_set(
    args: argparse.Namespace,
    client: SicpClient,
    config: CliConfig,
) -> int:
    validate_volume_limits(args.minimum, args.maximum, args.switch_on)
    _, set_command = volume_limit_command_pair(args.target)
    transaction = client.transact_with_request(
        set_command,
        args.minimum,
        args.maximum,
        args.switch_on,
        expected_response_commands=(0x00,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Volume limit set did not return a response")
    require_ack(transaction.response)
    print_result(
        {
            "command": f"volume limit {args.target} set",
            "target": args.target,
            "requested_volume_limit": {
                "minimum": args.minimum,
                "maximum": args.maximum,
                "switch_on": args.switch_on,
            },
            "status": "ACK",
            "message": (
                f"Volume limit {args.target} set: min={args.minimum}%, "
                f"max={args.maximum}%, switch-on={args.switch_on}% (ACK)"
            ),
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_volume_audio_get(client: SicpClient, config: CliConfig) -> int:
    transaction = client.transact_with_request(
        AUDIO_PARAMETERS_GET_COMMAND,
        expected_response_commands=(AUDIO_PARAMETERS_GET_COMMAND,),
        expected_response_sizes=(7,),
    )
    if transaction.response is None:
        raise SicpError("Audio parameters get did not return a response")
    state = decode_audio_parameters_report(transaction.response)
    print_result(
        {
            "command": "volume audio get",
            "audio_parameters": state.to_dict(),
            "message": (
                f"Audio parameters: treble={state.treble_display}, "
                f"bass={state.bass_display}"
            ),
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_volume_audio_set(
    args: argparse.Namespace, client: SicpClient, config: CliConfig
) -> int:
    transaction = client.transact_with_request(
        AUDIO_PARAMETERS_SET_COMMAND,
        args.treble,
        args.bass,
        expected_response_commands=(0x00,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Audio parameters set did not return a response")
    require_ack(transaction.response)
    treble = audio_parameter_value_to_display(args.treble)
    bass = audio_parameter_value_to_display(args.bass)
    print_result(
        {
            "command": "volume audio set",
            "requested_audio_parameters": {
                "treble": args.treble,
                "treble_display": treble,
                "bass": args.bass,
                "bass_display": bass,
            },
            "status": "ACK",
            "message": f"Audio parameters set: treble={treble}, bass={bass} (ACK)",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_volume_mute_get(client: SicpClient, config: CliConfig) -> int:
    transaction = client.transact_with_request(
        VOLUME_MUTE_GET_COMMAND,
        expected_response_commands=(VOLUME_MUTE_GET_COMMAND,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Volume mute get did not return a response")
    muted = decode_volume_mute_report(transaction.response)
    state = "on" if muted else "off"
    print_result(
        {
            "command": "volume mute get",
            "volume_muted": muted,
            "volume_mute": state,
            "message": f"Volume mute: {state}",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_volume_mute_set(client: SicpClient, state: str, config: CliConfig) -> int:
    muted = state == "on"
    transaction = client.transact_with_request(
        VOLUME_MUTE_SET_COMMAND,
        bool_to_mute_value(muted),
        expected_response_commands=(0x00,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Volume mute set did not return a response")
    require_ack(transaction.response)
    print_result(
        {
            "command": "volume mute set",
            "requested_volume_muted": muted,
            "requested_volume_mute": state,
            "status": "ACK",
            "message": f"Volume mute set: {state} (ACK)",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_video_signal_get(client: SicpClient, config: CliConfig) -> int:
    transaction = client.transact_with_request(
        VIDEO_SIGNAL_PRESENT_COMMAND,
        expected_response_commands=(VIDEO_SIGNAL_PRESENT_COMMAND,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Video-signal get did not return a response")
    present = decode_video_signal_present_report(transaction.response)
    status = "present" if present else "not present"
    print_result(
        {
            "command": "video-signal get",
            "video_signal_present": present,
            "video_signal": status,
            "message": f"Video signal: {status}",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_lock_get(client: SicpClient, target: str, config: CliConfig) -> int:
    if target == "ir":
        command = IR_LOCK_GET_COMMAND
        decoder = decode_ir_lock_report
        label = "IR remote lock"
    elif target == "keypad":
        command = KEYPAD_LOCK_GET_COMMAND
        decoder = decode_keypad_lock_report
        label = "Keypad lock"
    else:
        raise ValueError("lock target must be ir or keypad")

    transaction = client.transact_with_request(
        command,
        expected_response_commands=(command,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError(f"{label} get did not return a response")
    state = decoder(transaction.response)
    print_result(
        {
            "command": f"lock {target} get",
            "target": target,
            "lock_state": state,
            "message": f"{label}: {state}",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_lock_set(
    client: SicpClient,
    target: str,
    state: str,
    config: CliConfig,
) -> int:
    if target == "ir":
        command = IR_LOCK_SET_COMMAND
        label = "IR remote lock"
    elif target == "keypad":
        command = KEYPAD_LOCK_SET_COMMAND
        label = "Keypad lock"
    else:
        raise ValueError("lock target must be ir or keypad")

    value = lock_state_name_to_value(state, target=target)
    canonical = lock_state_value_to_name(value, target=target)
    transaction = client.transact_with_request(
        command,
        value,
        expected_response_commands=(0x00,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError(f"{label} set did not return a response")
    require_ack(transaction.response)
    print_result(
        {
            "command": f"lock {target} set",
            "target": target,
            "requested_lock_state": canonical,
            "status": "ACK",
            "message": f"{label} set: {canonical} (ACK)",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_video_parameters_get(client: SicpClient, config: CliConfig) -> int:
    transaction = client.transact_with_request(
        VIDEO_PARAMETERS_GET_COMMAND,
        expected_response_commands=(VIDEO_PARAMETERS_GET_COMMAND,),
        expected_response_sizes=(12,),
    )
    if transaction.response is None:
        raise SicpError("Video parameters get did not return a response")
    state = decode_video_parameters_report(transaction.response)
    print_result(
        {
            "command": "video parameters get",
            "video_parameters": state.to_dict(),
            "message": (
                "Video parameters: "
                f"brightness={state.brightness}, color={state.color}, "
                f"contrast={state.contrast}, sharpness={state.sharpness}, "
                f"tint={state.tint}, black-level={state.black_level}, "
                f"gamma={state.gamma_name}"
            ),
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_video_parameters_set(
    args: argparse.Namespace,
    client: SicpClient,
    config: CliConfig,
) -> int:
    gamma_value = gamma_name_to_value(args.gamma)
    transaction = client.transact_with_request(
        VIDEO_PARAMETERS_SET_COMMAND,
        args.brightness,
        args.color,
        args.contrast,
        args.sharpness,
        args.tint,
        args.black_level,
        gamma_value,
        expected_response_commands=(0x00,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Video parameters set did not return a response")
    require_ack(transaction.response)
    print_result(
        {
            "command": "video parameters set",
            "requested_video_parameters": {
                "brightness": args.brightness,
                "color": args.color,
                "contrast": args.contrast,
                "sharpness": args.sharpness,
                "tint": args.tint,
                "black_level": args.black_level,
                "gamma": gamma_value,
                "gamma_name": gamma_value_to_name(gamma_value),
            },
            "status": "ACK",
            "message": (
                "Video parameters set: "
                f"brightness={args.brightness}, color={args.color}, "
                f"contrast={args.contrast}, sharpness={args.sharpness}, "
                f"tint={args.tint}, black-level={args.black_level}, "
                f"gamma={args.gamma} (ACK)"
            ),
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_picture_format_get(client: SicpClient, config: CliConfig) -> int:
    transaction = client.transact_with_request(
        PICTURE_FORMAT_GET_COMMAND,
        expected_response_commands=(PICTURE_FORMAT_GET_COMMAND,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Picture-format get did not return a response")
    picture_format = decode_picture_format_report(transaction.response)
    print_result(
        {
            "command": "video picture-format get",
            "picture_format": picture_format,
            "message": f"Picture format: {picture_format}",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_picture_format_set(
    client: SicpClient,
    picture_format: int,
    config: CliConfig,
) -> int:
    canonical = picture_format_value_to_name(picture_format)
    transaction = client.transact_with_request(
        PICTURE_FORMAT_SET_COMMAND,
        picture_format,
        expected_response_commands=(0x00,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Picture-format set did not return a response")
    require_ack(transaction.response)
    print_result(
        {
            "command": "video picture-format set",
            "requested_picture_format": canonical,
            "requested_picture_format_value": picture_format,
            "status": "ACK",
            "message": f"Picture format set: {canonical} (ACK)",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_color_temperature_get(client: SicpClient, config: CliConfig) -> int:
    transaction = client.transact_with_request(
        COLOR_TEMPERATURE_GET_COMMAND,
        expected_response_commands=(COLOR_TEMPERATURE_GET_COMMAND,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Color-temperature get did not return a response")
    temperature = decode_color_temperature_report(transaction.response)
    print_result(
        {
            "command": "video color-temperature get",
            "color_temperature": temperature,
            "message": f"Color temperature: {temperature}",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_color_temperature_set(
    client: SicpClient,
    temperature: str,
    config: CliConfig,
) -> int:
    value = color_temperature_name_to_value(temperature)
    canonical = color_temperature_value_to_name(value)
    transaction = client.transact_with_request(
        COLOR_TEMPERATURE_SET_COMMAND,
        value,
        expected_response_commands=(0x00,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Color-temperature set did not return a response")
    require_ack(transaction.response)
    print_result(
        {
            "command": "video color-temperature set",
            "requested_color_temperature": canonical,
            "status": "ACK",
            "message": f"Color temperature set: {canonical} (ACK)",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_rgb_parameters_get(client: SicpClient, config: CliConfig) -> int:
    transaction = client.transact_with_request(
        RGB_PARAMETERS_GET_COMMAND,
        expected_response_commands=(RGB_PARAMETERS_GET_COMMAND,),
        expected_response_sizes=(11,),
    )
    if transaction.response is None:
        raise SicpError("RGB parameters get did not return a response")
    state = decode_rgb_parameters_report(transaction.response)
    print_result(
        {
            "command": "video rgb get",
            "rgb_parameters": state.to_dict(),
            "message": (
                "RGB parameters: "
                f"red-gain={state.red_gain}, green-gain={state.green_gain}, "
                f"blue-gain={state.blue_gain}, red-offset={state.red_offset}, "
                f"green-offset={state.green_offset}, blue-offset={state.blue_offset}"
            ),
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_rgb_parameters_set(
    args: argparse.Namespace,
    client: SicpClient,
    config: CliConfig,
) -> int:
    transaction = client.transact_with_request(
        RGB_PARAMETERS_SET_COMMAND,
        args.red_gain,
        args.green_gain,
        args.blue_gain,
        args.red_offset,
        args.green_offset,
        args.blue_offset,
        expected_response_commands=(0x00,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("RGB parameters set did not return a response")
    require_ack(transaction.response)
    print_result(
        {
            "command": "video rgb set",
            "requested_rgb_parameters": {
                "red_gain": args.red_gain,
                "green_gain": args.green_gain,
                "blue_gain": args.blue_gain,
                "red_offset": args.red_offset,
                "green_offset": args.green_offset,
                "blue_offset": args.blue_offset,
            },
            "status": "ACK",
            "message": (
                "RGB parameters set: "
                f"red-gain={args.red_gain}, green-gain={args.green_gain}, "
                f"blue-gain={args.blue_gain}, red-offset={args.red_offset}, "
                f"green-offset={args.green_offset}, "
                f"blue-offset={args.blue_offset} (ACK)"
            ),
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_color_temperature_100k_get(client: SicpClient, config: CliConfig) -> int:
    transaction = client.transact_with_request(
        COLOR_TEMPERATURE_100K_GET_COMMAND,
        expected_response_commands=(COLOR_TEMPERATURE_100K_GET_COMMAND,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Color-temperature-100k get did not return a response")
    state = decode_color_temperature_100k_report(transaction.response)
    print_result(
        {
            "command": "video color-temperature-100k get",
            "color_temperature_100k": state.to_dict(),
            "message": (f"Color temperature 100K: {state.steps} ({state.kelvin}K)"),
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_color_temperature_100k_set(
    client: SicpClient,
    steps: int,
    config: CliConfig,
) -> int:
    value = validate_color_temperature_100k_steps(steps)
    transaction = client.transact_with_request(
        COLOR_TEMPERATURE_100K_SET_COMMAND,
        value,
        expected_response_commands=(0x00,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Color-temperature-100k set did not return a response")
    require_ack(transaction.response)
    print_result(
        {
            "command": "video color-temperature-100k set",
            "requested_color_temperature_100k": {
                "steps": value,
                "kelvin": value * 100,
            },
            "status": "ACK",
            "message": f"Color temperature 100K set: {value} ({value * 100}K) (ACK)",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_power_saving_set(client: SicpClient, mode: str, config: CliConfig) -> int:
    value = power_saving_mode_name_to_value(mode)
    canonical = power_saving_mode_value_to_name(value)
    transaction = client.transact_with_request(
        POWER_SAVING_MODE_SET_COMMAND,
        value,
        expected_response_commands=(0x00,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Power-saving mode set did not return a response")
    require_ack(transaction.response)
    print_result(
        {
            "command": "power-saving set",
            "requested_power_saving_mode": canonical,
            "status": "ACK",
            "message": f"Power-saving mode set: {canonical} (ACK)",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_power_saving_get(client: SicpClient, config: CliConfig) -> int:
    transaction = client.transact_with_request(
        POWER_SAVING_MODE_GET_COMMAND,
        expected_response_commands=(POWER_SAVING_MODE_GET_COMMAND,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Power-saving mode get did not return a response")
    mode = decode_power_saving_mode_report(transaction.response)
    print_result(
        {
            "command": "power-saving get",
            "power_saving_mode": mode,
            "message": f"Power-saving mode: {mode}",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_operating_hours_get(client: SicpClient, config: CliConfig) -> int:
    transaction = client.transact_with_request(
        OPERATING_HOURS_COMMAND,
        OPERATING_HOURS_ITEM,
        expected_response_commands=(OPERATING_HOURS_COMMAND,),
        expected_response_sizes=(7,),
    )
    if transaction.response is None:
        raise SicpError("Operating-hours get did not return a response")
    hours = decode_operating_hours_report(transaction.response)
    print_result(
        {
            "command": "operating-hours get",
            "operating_hours": hours,
            "message": f"Operating hours: {hours}",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def tiling_wall_summary(state: TilingState) -> str:
    standard = state.standard_monitors
    zero_bezel = state.zero_bezel_monitors
    standard_text = (
        "unknown"
        if standard is None
        else f"H={standard[0]}, V={standard[1]} (5-wide formula)"
    )
    zero_bezel_text = (
        "unknown"
        if zero_bezel is None
        else f"H={zero_bezel[0]}, V={zero_bezel[1]} (15-wide formula)"
    )
    return f"{standard_text}; {zero_bezel_text}"


def run_tiling_get(client: SicpClient, config: CliConfig) -> int:
    transaction = client.transact_with_request(
        TILING_GET_COMMAND,
        expected_response_commands=(TILING_GET_COMMAND,),
        expected_response_sizes=(9,),
    )
    if transaction.response is None:
        raise SicpError("Tiling get did not return a response")
    state = decode_tiling_report(transaction.response)
    print_result(
        {
            "command": "tiling get",
            "tiling": state.to_dict(),
            "message": (
                "Tiling: "
                f"enabled={'yes' if state.enabled else 'no'}, "
                f"frame-comp={'yes' if state.frame_compensation else 'no'}, "
                f"position={state.position}, wall-size=0x{state.wall_size:02X} "
                f"({tiling_wall_summary(state)})"
            ),
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_tiling_set(
    args: argparse.Namespace, client: SicpClient, config: CliConfig
) -> int:
    if args.wall_size is not None and (
        args.h_monitors is not None or args.v_monitors is not None
    ):
        raise ValueError(
            "use either --wall-size or --h-monitors/--v-monitors, not both"
        )
    if (args.h_monitors is None) != (args.v_monitors is None):
        raise ValueError("--h-monitors and --v-monitors must be passed together")

    if args.wall_size is not None:
        wall_size = args.wall_size
    elif args.h_monitors is not None and args.v_monitors is not None:
        wall_size = encode_tiling_wall_size(
            args.h_monitors,
            args.v_monitors,
            zero_bezel=args.zero_bezel,
        )
    else:
        wall_size = 0x00

    frame_comp = (
        args.frame_comp
        if isinstance(args.frame_comp, int)
        else tiling_frame_comp_name_to_value(args.frame_comp)
    )
    position = tiling_position_name_to_value(args.position, zero_bezel=args.zero_bezel)
    values = build_tiling_set_values(
        args.enable,
        frame_comp,
        position,
        wall_size,
        zero_bezel=args.zero_bezel,
    )
    transaction = client.transact_with_request(
        TILING_SET_COMMAND,
        *values,
        expected_response_commands=(0x00,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Tiling set did not return a response")
    require_ack(transaction.response)
    requested = {
        "enabled": bool(values[0]),
        "frame_compensation": (
            "keep" if values[1] == 0x02 else ("yes" if values[1] else "no")
        ),
        "position": "keep" if values[2] == 0x00 else values[2],
        "wall_size": values[3],
        "wall_size_mode": "zero-bezel" if args.zero_bezel else "standard",
    }
    print_result(
        {
            "command": "tiling set",
            "requested_tiling": requested,
            "status": "ACK",
            "message": (
                "Tiling set: "
                f"enabled={'yes' if values[0] else 'no'}, "
                f"frame-comp={requested['frame_compensation']}, "
                f"position={requested['position']}, "
                f"wall-size=0x{values[3]:02X} (ACK)"
            ),
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_switch_on_delay_get(client: SicpClient, config: CliConfig) -> int:
    transaction = client.transact_with_request(
        SWITCH_ON_DELAY_GET_COMMAND,
        expected_response_commands=(SWITCH_ON_DELAY_GET_COMMAND,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Switch-on-delay get did not return a response")
    delay = decode_switch_on_delay_report(transaction.response)
    formatted = switch_on_delay_value_to_name(delay)
    print_result(
        {
            "command": "switch-on-delay get",
            "switch_on_delay": {
                "value": delay,
                "display": formatted,
            },
            "message": f"Switch-on delay: {formatted}",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_switch_on_delay_set(
    client: SicpClient,
    delay: int,
    config: CliConfig,
) -> int:
    formatted = switch_on_delay_value_to_name(delay)
    transaction = client.transact_with_request(
        SWITCH_ON_DELAY_SET_COMMAND,
        delay,
        expected_response_commands=(0x00,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Switch-on-delay set did not return a response")
    require_ack(transaction.response)
    print_result(
        {
            "command": "switch-on-delay set",
            "requested_switch_on_delay": {
                "value": delay,
                "display": formatted,
            },
            "status": "ACK",
            "message": f"Switch-on delay set: {formatted} (ACK)",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def frame_compensation_commands(axis: str) -> tuple[int, int]:
    if axis == "horizontal":
        return (
            FRAME_COMPENSATION_HORIZONTAL_GET_COMMAND,
            FRAME_COMPENSATION_HORIZONTAL_SET_COMMAND,
        )
    if axis == "vertical":
        return (
            FRAME_COMPENSATION_VERTICAL_GET_COMMAND,
            FRAME_COMPENSATION_VERTICAL_SET_COMMAND,
        )
    raise ValueError(f"unknown frame compensation axis: {axis}")


def decode_frame_compensation_report(axis: str, packet: SicpPacket) -> int:
    if axis == "horizontal":
        return decode_frame_compensation_horizontal_report(packet)
    if axis == "vertical":
        return decode_frame_compensation_vertical_report(packet)
    raise ValueError(f"unknown frame compensation axis: {axis}")


def run_frame_compensation_get(
    client: SicpClient,
    axis: str,
    config: CliConfig,
) -> int:
    get_command, _set_command = frame_compensation_commands(axis)
    transaction = client.transact_with_request(
        get_command,
        expected_response_commands=(get_command,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError(
            f"{axis.title()} frame-compensation get did not return a response"
        )
    value = decode_frame_compensation_report(axis, transaction.response)
    print_result(
        {
            "command": f"frame-compensation {axis} get",
            "frame_compensation": {
                "axis": axis,
                "value": value,
            },
            "message": f"Frame compensation {axis}: {value}",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_frame_compensation_set(
    client: SicpClient,
    axis: str,
    value: int,
    config: CliConfig,
) -> int:
    _get_command, set_command = frame_compensation_commands(axis)
    transaction = client.transact_with_request(
        set_command,
        value,
        expected_response_commands=(0x00,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError(
            f"{axis.title()} frame-compensation set did not return a response"
        )
    require_ack(transaction.response)
    print_result(
        {
            "command": f"frame-compensation {axis} set",
            "requested_frame_compensation": {
                "axis": axis,
                "value": value,
            },
            "status": "ACK",
            "message": f"Frame compensation {axis} set: {value} (ACK)",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_anytile_get(client: SicpClient, config: CliConfig) -> int:
    transaction = client.transact_with_request(
        ANYTILE_GET_COMMAND,
        expected_response_commands=(ANYTILE_GET_COMMAND,),
        expected_response_sizes=(16,),
    )
    if transaction.response is None:
        raise SicpError("AnyTile get did not return a response")
    state = decode_anytile_report(transaction.response)
    print_result(
        {
            "command": "anytile get",
            "anytile": state.to_dict(),
            "message": (
                "AnyTile: "
                f"enabled={'yes' if state.enabled else 'no'}, "
                f"rotation={state.rotation}, "
                f"h-start={state.input_h_start}, v-start={state.input_v_start}, "
                f"h-size={state.input_h_size}, v-size={state.input_v_size}"
            ),
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_anytile_set(
    args: argparse.Namespace, client: SicpClient, config: CliConfig
) -> int:
    parameters = build_anytile_parameters(
        args.enable,
        args.rotation,
        args.h_start,
        args.v_start,
        args.h_size,
        args.v_size,
    )
    transaction = client.transact_with_request(
        ANYTILE_SET_COMMAND,
        *parameters,
        expected_response_commands=(0x00,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("AnyTile set did not return a response")
    require_ack(transaction.response)
    print_result(
        {
            "command": "anytile set",
            "requested_anytile": {
                "enabled": bool(args.enable),
                "rotation": args.rotation,
                "input_h_start": args.h_start,
                "input_v_start": args.v_start,
                "input_h_size": args.h_size,
                "input_v_size": args.v_size,
            },
            "status": "ACK",
            "message": (
                "AnyTile set: "
                f"enabled={'yes' if args.enable else 'no'}, "
                f"rotation={args.rotation}, h-start={args.h_start}, "
                f"v-start={args.v_start}, h-size={args.h_size}, "
                f"v-size={args.v_size} (ACK)"
            ),
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_anytile_resolution_get(client: SicpClient, config: CliConfig) -> int:
    transaction = client.transact_with_request(
        ANYTILE_RESOLUTION_GET_COMMAND,
        expected_response_commands=(ANYTILE_RESOLUTION_GET_COMMAND,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("AnyTile resolution get did not return a response")
    mode = decode_anytile_resolution_report(transaction.response)
    print_result(
        {
            "command": "anytile resolution get",
            "anytile_resolution": mode,
            "message": f"AnyTile resolution: {mode}",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_anytile_resolution_set(
    client: SicpClient,
    mode: int,
    config: CliConfig,
) -> int:
    canonical = anytile_resolution_value_to_name(mode)
    transaction = client.transact_with_request(
        ANYTILE_RESOLUTION_SET_COMMAND,
        mode,
        expected_response_commands=(0x00,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("AnyTile resolution set did not return a response")
    require_ack(transaction.response)
    print_result(
        {
            "command": "anytile resolution set",
            "requested_anytile_resolution": canonical,
            "status": "ACK",
            "message": f"AnyTile resolution set: {canonical} (ACK)",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_anytile_assign_id(
    args: argparse.Namespace, client: SicpClient, config: CliConfig
) -> int:
    transaction = client.transact_with_request(
        ANYTILE_ASSIGN_IDS_COMMAND,
        args.monitor_id,
        args.group_id,
        expected_response_commands=(0x00,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("AnyTile assign-id did not return a response")
    require_ack(transaction.response)
    print_result(
        {
            "command": "anytile assign-id",
            "requested_monitor_id": args.monitor_id,
            "requested_group_id": args.group_id,
            "status": "ACK",
            "message": (
                f"AnyTile IDs assigned: monitor={args.monitor_id}, "
                f"group={args.group_id} (ACK)"
            ),
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_anytile_display_id_set(
    client: SicpClient,
    monitor_id: int,
    config: CliConfig,
) -> int:
    transaction = client.transact_with_request(
        ANYTILE_DISPLAY_MONITOR_ID_SET_COMMAND,
        monitor_id,
        expected_response_commands=(0x00,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("AnyTile display-id set did not return a response")
    require_ack(transaction.response)
    print_result(
        {
            "command": "anytile display-id set",
            "requested_monitor_id": monitor_id,
            "status": "ACK",
            "message": f"AnyTile display monitor ID set: {monitor_id} (ACK)",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_power_saving_status_set(
    client: SicpClient,
    status: int,
    config: CliConfig,
) -> int:
    canonical = power_saving_mode_status_value_to_name(status)
    transaction = client.transact_with_request(
        POWER_SAVING_MODE_STATUS_SET_COMMAND,
        status,
        expected_response_commands=(0x00,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Power-saving mode status set did not return a response")
    require_ack(transaction.response)
    print_result(
        {
            "command": "power-saving-status set",
            "requested_power_saving_mode_status": canonical,
            "requested_power_saving_mode_status_value": status,
            "status": "ACK",
            "message": f"Power-saving mode status set: {canonical} (ACK)",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_power_saving_status_get(client: SicpClient, config: CliConfig) -> int:
    transaction = client.transact_with_request(
        POWER_SAVING_MODE_STATUS_GET_COMMAND,
        expected_response_commands=(POWER_SAVING_MODE_STATUS_GET_COMMAND,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Power-saving mode status get did not return a response")
    status = decode_power_saving_mode_status_report(transaction.response)
    print_result(
        {
            "command": "power-saving-status get",
            "power_saving_mode_status": status,
            "message": f"Power-saving mode status: {status}",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_apm_status_set(
    client: SicpClient,
    status: int,
    config: CliConfig,
) -> int:
    canonical = apm_status_value_to_name(status)
    transaction = client.transact_with_request(
        APM_STATUS_SET_COMMAND,
        status,
        expected_response_commands=(0x00,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("APM status set did not return a response")
    require_ack(transaction.response)
    print_result(
        {
            "command": "apm-status set",
            "requested_apm_status": canonical,
            "requested_apm_status_value": status,
            "status": "ACK",
            "message": f"APM status set: {canonical} (ACK)",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_apm_status_get(client: SicpClient, config: CliConfig) -> int:
    transaction = client.transact_with_request(
        APM_STATUS_GET_COMMAND,
        expected_response_commands=(APM_STATUS_GET_COMMAND,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("APM status get did not return a response")
    status = decode_apm_status_report(transaction.response)
    print_result(
        {
            "command": "apm-status get",
            "apm_status": status,
            "message": f"APM status: {status}",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_serial_code_get(client: SicpClient, config: CliConfig) -> int:
    transaction = client.transact_with_request(
        SERIAL_CODE_GET_COMMAND,
        expected_response_commands=(SERIAL_CODE_GET_COMMAND,),
        expected_response_sizes=(19,),
    )
    if transaction.response is None:
        raise SicpError("Serial-code get did not return a response")
    serial_code = decode_serial_code_report(transaction.response)
    print_result(
        {
            "command": "serial-code get",
            "serial_code": serial_code,
            "message": f"Serial code: {serial_code}",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_light_sensor_get(client: SicpClient, config: CliConfig) -> int:
    transaction = client.transact_with_request(
        LIGHT_SENSOR_GET_COMMAND,
        expected_response_commands=(LIGHT_SENSOR_GET_COMMAND,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Light-sensor get did not return a response")
    state = decode_light_sensor_report(transaction.response)
    print_result(
        {
            "command": "light-sensor get",
            "light_sensor": state,
            "message": f"Light sensor: {state}",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_light_sensor_set(client: SicpClient, state: str, config: CliConfig) -> int:
    value = light_sensor_name_to_value(state)
    canonical = light_sensor_value_to_name(value)
    transaction = client.transact_with_request(
        LIGHT_SENSOR_SET_COMMAND,
        value,
        expected_response_commands=(0x00,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Light-sensor set did not return a response")
    require_ack(transaction.response)
    print_result(
        {
            "command": "light-sensor set",
            "requested_light_sensor": canonical,
            "status": "ACK",
            "message": f"Light sensor set: {canonical} (ACK)",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_osd_rotating_get(client: SicpClient, config: CliConfig) -> int:
    transaction = client.transact_with_request(
        OSD_ROTATING_GET_COMMAND,
        expected_response_commands=(OSD_ROTATING_GET_COMMAND,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("OSD rotating get did not return a response")
    state = decode_osd_rotating_report(transaction.response)
    print_result(
        {
            "command": "osd-rotating get",
            "osd_rotating": state,
            "message": f"OSD rotating: {state}",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_osd_rotating_set(client: SicpClient, state: str, config: CliConfig) -> int:
    value = osd_rotating_name_to_value(state)
    canonical = osd_rotating_value_to_name(value)
    transaction = client.transact_with_request(
        OSD_ROTATING_SET_COMMAND,
        value,
        expected_response_commands=(0x00,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("OSD rotating set did not return a response")
    require_ack(transaction.response)
    print_result(
        {
            "command": "osd-rotating set",
            "requested_osd_rotating": canonical,
            "status": "ACK",
            "message": f"OSD rotating set: {canonical} (ACK)",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_display_orientation_get(client: SicpClient, config: CliConfig) -> int:
    transaction = client.transact_with_request(
        DISPLAY_ORIENTATION_GET_COMMAND,
        expected_response_commands=(DISPLAY_ORIENTATION_GET_COMMAND,),
        expected_response_sizes=(12,),
    )
    if transaction.response is None:
        raise SicpError("Display-orientation get did not return a response")
    state = decode_display_orientation_report(transaction.response)
    print_result(
        {
            "command": "display-orientation get",
            "display_orientation": state.to_dict(),
            "message": (
                "Display orientation: "
                f"auto-rotate={state.auto_rotate_name}, "
                f"osd={state.osd_rotation_name}, "
                f"image-all={state.image_all_name}, "
                f"window1={state.window1_name}, "
                f"window2={state.window2_name}, "
                f"window3={state.window3_name}, "
                f"window4={state.window4_name}"
            ),
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_display_orientation_set(
    args: argparse.Namespace,
    client: SicpClient,
    config: CliConfig,
) -> int:
    values = validate_display_orientation_values(
        args.auto_rotate,
        args.osd,
        args.image_all,
        args.window1,
        args.window2,
        args.window3,
        args.window4,
    )
    transaction = client.transact_with_request(
        DISPLAY_ORIENTATION_SET_COMMAND,
        *values,
        expected_response_commands=(0x00,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Display-orientation set did not return a response")
    require_ack(transaction.response)
    requested = {
        "auto_rotate": args.auto_rotate,
        "auto_rotate_name": display_orientation_auto_rotate_value_to_name(
            args.auto_rotate
        ),
        "osd_rotation": args.osd,
        "osd_rotation_name": display_orientation_osd_rotation_value_to_name(args.osd),
        "image_all": args.image_all,
        "image_all_name": display_orientation_image_all_value_to_name(args.image_all),
        "window1": args.window1,
        "window1_name": display_orientation_window_value_to_name(args.window1),
        "window2": args.window2,
        "window2_name": display_orientation_window_value_to_name(args.window2),
        "window3": args.window3,
        "window3_name": display_orientation_window_value_to_name(args.window3),
        "window4": args.window4,
        "window4_name": display_orientation_window_value_to_name(args.window4),
    }
    print_result(
        {
            "command": "display-orientation set",
            "requested_display_orientation": requested,
            "status": "ACK",
            "message": (
                "Display orientation set: "
                f"auto-rotate={requested['auto_rotate_name']}, "
                f"osd={requested['osd_rotation_name']}, "
                f"image-all={requested['image_all_name']}, "
                f"window1={requested['window1_name']}, "
                f"window2={requested['window2_name']}, "
                f"window3={requested['window3_name']}, "
                f"window4={requested['window4_name']} (ACK)"
            ),
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_touch_feature_get(client: SicpClient, config: CliConfig) -> int:
    transaction = client.transact_with_request(
        TOUCH_FEATURE_GET_COMMAND,
        expected_response_commands=(TOUCH_FEATURE_GET_COMMAND,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Touch-feature get did not return a response")
    state = decode_touch_feature_report(transaction.response)
    print_result(
        {
            "command": "touch-feature get",
            "touch_feature": state,
            "message": f"Touch feature: {state}",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_touch_feature_set(client: SicpClient, state: str, config: CliConfig) -> int:
    value = touch_feature_name_to_value(state)
    canonical = touch_feature_value_to_name(value)
    transaction = client.transact_with_request(
        TOUCH_FEATURE_SET_COMMAND,
        value,
        expected_response_commands=(0x00,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Touch-feature set did not return a response")
    require_ack(transaction.response)
    print_result(
        {
            "command": "touch-feature set",
            "requested_touch_feature": canonical,
            "status": "ACK",
            "message": f"Touch feature set: {canonical} (ACK)",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_noise_reduction_get(client: SicpClient, config: CliConfig) -> int:
    transaction = client.transact_with_request(
        NOISE_REDUCTION_GET_COMMAND,
        expected_response_commands=(NOISE_REDUCTION_GET_COMMAND,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Noise-reduction get did not return a response")
    level = decode_noise_reduction_report(transaction.response)
    print_result(
        {
            "command": "noise-reduction get",
            "noise_reduction": level,
            "message": f"Noise reduction: {level}",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_noise_reduction_set(client: SicpClient, level: str, config: CliConfig) -> int:
    value = noise_reduction_name_to_value(level)
    canonical = noise_reduction_value_to_name(value)
    transaction = client.transact_with_request(
        NOISE_REDUCTION_SET_COMMAND,
        value,
        expected_response_commands=(0x00,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Noise-reduction set did not return a response")
    require_ack(transaction.response)
    print_result(
        {
            "command": "noise-reduction set",
            "requested_noise_reduction": canonical,
            "status": "ACK",
            "message": f"Noise reduction set: {canonical} (ACK)",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_scan_mode_get(client: SicpClient, config: CliConfig) -> int:
    transaction = client.transact_with_request(
        SCAN_MODE_GET_COMMAND,
        expected_response_commands=(SCAN_MODE_GET_COMMAND,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Scan-mode get did not return a response")
    mode = decode_scan_mode_report(transaction.response)
    print_result(
        {
            "command": "scan-mode get",
            "scan_mode": mode,
            "message": f"Scan mode: {mode}",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_scan_mode_set(client: SicpClient, mode: int, config: CliConfig) -> int:
    canonical = scan_mode_value_to_name(mode)
    transaction = client.transact_with_request(
        SCAN_MODE_SET_COMMAND,
        mode,
        expected_response_commands=(0x00,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Scan-mode set did not return a response")
    require_ack(transaction.response)
    print_result(
        {
            "command": "scan-mode set",
            "requested_scan_mode": canonical,
            "requested_scan_mode_value": mode,
            "status": "ACK",
            "message": f"Scan mode set: {canonical} (ACK)",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_scan_conversion_get(client: SicpClient, config: CliConfig) -> int:
    transaction = client.transact_with_request(
        SCAN_CONVERSION_GET_COMMAND,
        expected_response_commands=(SCAN_CONVERSION_GET_COMMAND,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Scan-conversion get did not return a response")
    mode = decode_scan_conversion_report(transaction.response)
    print_result(
        {
            "command": "scan-conversion get",
            "scan_conversion": mode,
            "message": f"Scan conversion: {mode}",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_scan_conversion_set(client: SicpClient, mode: str, config: CliConfig) -> int:
    value = scan_conversion_name_to_value(mode)
    canonical = scan_conversion_value_to_name(value)
    transaction = client.transact_with_request(
        SCAN_CONVERSION_SET_COMMAND,
        value,
        expected_response_commands=(0x00,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Scan-conversion set did not return a response")
    require_ack(transaction.response)
    print_result(
        {
            "command": "scan-conversion set",
            "requested_scan_conversion": canonical,
            "status": "ACK",
            "message": f"Scan conversion set: {canonical} (ACK)",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_pixel_shift_get(client: SicpClient, config: CliConfig) -> int:
    transaction = client.transact_with_request(
        PIXEL_SHIFT_GET_COMMAND,
        expected_response_commands=(PIXEL_SHIFT_GET_COMMAND,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Pixel-shift get did not return a response")
    value = decode_pixel_shift_report(transaction.response)
    print_result(
        {
            "command": "pixel-shift get",
            "pixel_shift": value,
            "message": f"Pixel shift: {value}",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_pixel_shift_set(client: SicpClient, value: int, config: CliConfig) -> int:
    canonical = pixel_shift_value_to_name(value)
    transaction = client.transact_with_request(
        PIXEL_SHIFT_SET_COMMAND,
        value,
        expected_response_commands=(0x00,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Pixel-shift set did not return a response")
    require_ack(transaction.response)
    print_result(
        {
            "command": "pixel-shift set",
            "requested_pixel_shift": canonical,
            "requested_pixel_shift_value": value,
            "status": "ACK",
            "message": f"Pixel shift set: {canonical} (ACK)",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_memc_get(client: SicpClient, config: CliConfig) -> int:
    transaction = client.transact_with_request(
        MEMC_EFFECT_GET_COMMAND,
        expected_response_commands=(MEMC_EFFECT_GET_COMMAND,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("MEMC effect get did not return a response")
    level = decode_memc_effect_report(transaction.response)
    print_result(
        {
            "command": "memc get",
            "memc_effect": level,
            "message": f"MEMC effect: {level}",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_memc_set(client: SicpClient, level: str, config: CliConfig) -> int:
    value = memc_effect_name_to_value(level)
    canonical = memc_effect_value_to_name(value)
    transaction = client.transact_with_request(
        MEMC_EFFECT_SET_COMMAND,
        value,
        expected_response_commands=(0x00,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("MEMC effect set did not return a response")
    require_ack(transaction.response)
    print_result(
        {
            "command": "memc set",
            "requested_memc_effect": canonical,
            "status": "ACK",
            "message": f"MEMC effect set: {canonical} (ACK)",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_information_osd_get(client: SicpClient, config: CliConfig) -> int:
    transaction = client.transact_with_request(
        INFORMATION_OSD_GET_COMMAND,
        expected_response_commands=(INFORMATION_OSD_GET_COMMAND,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Information OSD get did not return a response")
    value = decode_information_osd_report(transaction.response)
    label = information_osd_value_to_name(value)
    print_result(
        {
            "command": "information-osd get",
            "information_osd": label,
            "information_osd_value": value,
            "message": f"Information OSD: {label}",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_information_osd_set(client: SicpClient, value: int, config: CliConfig) -> int:
    label = information_osd_value_to_name(value)
    transaction = client.transact_with_request(
        INFORMATION_OSD_SET_COMMAND,
        value,
        expected_response_commands=(0x00,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Information OSD set did not return a response")
    require_ack(transaction.response)
    print_result(
        {
            "command": "information-osd set",
            "requested_information_osd": label,
            "requested_information_osd_value": value,
            "status": "ACK",
            "message": f"Information OSD set: {label} (ACK)",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_human_sensor_get(client: SicpClient, config: CliConfig) -> int:
    transaction = client.transact_with_request(
        HUMAN_SENSOR_GET_COMMAND,
        expected_response_commands=(HUMAN_SENSOR_GET_COMMAND,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Human-sensor get did not return a response")
    state = decode_human_sensor_report(transaction.response)
    print_result(
        {
            "command": "human-sensor get",
            "human_sensor": state,
            "message": f"Human sensor: {state}",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_human_sensor_set(client: SicpClient, state: str, config: CliConfig) -> int:
    value = human_sensor_name_to_value(state)
    canonical = human_sensor_value_to_name(value)
    transaction = client.transact_with_request(
        HUMAN_SENSOR_SET_COMMAND,
        value,
        expected_response_commands=(0x00,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Human-sensor set did not return a response")
    require_ack(transaction.response)
    print_result(
        {
            "command": "human-sensor set",
            "requested_human_sensor": canonical,
            "status": "ACK",
            "message": f"Human sensor set: {canonical} (ACK)",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_factory_reset_set(client: SicpClient, config: CliConfig) -> int:
    transaction = client.transact_with_request(
        FACTORY_RESET_COMMAND,
        expected_response_commands=(0x00,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Factory reset did not return a response")
    require_ack(transaction.response)
    print_result(
        {
            "command": "factory-reset set",
            "status": "ACK",
            "message": "Factory reset: ACK",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_power_on_logo_get(client: SicpClient, config: CliConfig) -> int:
    transaction = client.transact_with_request(
        POWER_ON_LOGO_GET_COMMAND,
        expected_response_commands=(POWER_ON_LOGO_GET_COMMAND,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Power-on-logo get did not return a response")
    state = decode_power_on_logo_report(transaction.response)
    print_result(
        {
            "command": "power-on-logo get",
            "power_on_logo": state,
            "message": f"Power on logo: {state}",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_power_on_logo_set(client: SicpClient, state: str, config: CliConfig) -> int:
    value = power_on_logo_name_to_value(state)
    canonical = power_on_logo_value_to_name(value)
    transaction = client.transact_with_request(
        POWER_ON_LOGO_SET_COMMAND,
        value,
        expected_response_commands=(0x00,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Power-on-logo set did not return a response")
    require_ack(transaction.response)
    print_result(
        {
            "command": "power-on-logo set",
            "requested_power_on_logo": canonical,
            "status": "ACK",
            "message": f"Power on logo set: {canonical} (ACK)",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_off_timer_get(client: SicpClient, config: CliConfig) -> int:
    transaction = client.transact_with_request(
        OFF_TIMER_GET_COMMAND,
        expected_response_commands=(OFF_TIMER_GET_COMMAND,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Off-timer get did not return a response")
    hours = decode_off_timer_report(transaction.response)
    name = off_timer_value_to_name(hours)
    print_result(
        {
            "command": "off-timer get",
            "off_timer_hours": hours,
            "off_timer": name,
            "message": f"Off timer: {name}",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_off_timer_set(client: SicpClient, hours: int, config: CliConfig) -> int:
    name = off_timer_value_to_name(hours)
    transaction = client.transact_with_request(
        OFF_TIMER_SET_COMMAND,
        hours,
        expected_response_commands=(0x00,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Off-timer set did not return a response")
    require_ack(transaction.response)
    print_result(
        {
            "command": "off-timer set",
            "requested_off_timer_hours": hours,
            "requested_off_timer": name,
            "status": "ACK",
            "message": f"Off timer set: {name} (ACK)",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_eco_mode_get(client: SicpClient, config: CliConfig) -> int:
    transaction = client.transact_with_request(
        ECO_MODE_GET_COMMAND,
        expected_response_commands=(ECO_MODE_GET_COMMAND,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("ECO mode get did not return a response")
    mode = decode_eco_mode_report(transaction.response)
    print_result(
        {
            "command": "eco-mode get",
            "eco_mode": mode,
            "message": f"ECO mode: {mode}",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_eco_mode_set(client: SicpClient, mode: int, config: CliConfig) -> int:
    canonical = eco_mode_value_to_name(mode)
    transaction = client.transact_with_request(
        ECO_MODE_SET_COMMAND,
        mode,
        expected_response_commands=(0x00,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("ECO mode set did not return a response")
    require_ack(transaction.response)
    print_result(
        {
            "command": "eco-mode set",
            "requested_eco_mode": canonical,
            "requested_eco_mode_value": mode,
            "status": "ACK",
            "message": f"ECO mode set: {canonical} (ACK)",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_picture_style_get(client: SicpClient, config: CliConfig) -> int:
    transaction = client.transact_with_request(
        PICTURE_STYLE_GET_COMMAND,
        expected_response_commands=(PICTURE_STYLE_GET_COMMAND,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Picture-style get did not return a response")
    style = decode_picture_style_report(transaction.response)
    print_result(
        {
            "command": "picture-style get",
            "picture_style": style,
            "message": f"Picture style: {style}",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_picture_style_set(client: SicpClient, style: int, config: CliConfig) -> int:
    canonical = picture_style_value_to_name(style)
    transaction = client.transact_with_request(
        PICTURE_STYLE_SET_COMMAND,
        style,
        expected_response_commands=(0x00,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Picture-style set did not return a response")
    require_ack(transaction.response)
    print_result(
        {
            "command": "picture-style set",
            "requested_picture_style": canonical,
            "requested_picture_style_value": style,
            "status": "ACK",
            "message": f"Picture style set: {canonical} (ACK)",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_group_id_get(client: SicpClient, config: CliConfig) -> int:
    transaction = client.transact_with_request(
        GROUP_ID_GET_COMMAND,
        expected_response_commands=(GROUP_ID_GET_COMMAND,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Group ID get did not return a response")
    group_id = decode_group_id_report(transaction.response)
    label = "off" if group_id is None else str(group_id)
    print_result(
        {
            "command": "group-id get",
            "group_id": group_id,
            "group_id_name": label,
            "message": f"Group ID: {label}",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_group_id_set(client: SicpClient, group_id: int, config: CliConfig) -> int:
    label = group_id_value_to_name(group_id)
    transaction = client.transact_with_request(
        GROUP_ID_SET_COMMAND,
        group_id,
        expected_response_commands=(0x00,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Group ID set did not return a response")
    require_ack(transaction.response)
    print_result(
        {
            "command": "group-id set",
            "requested_group_id": None if label == "off" else group_id,
            "requested_group_id_name": label,
            "status": "ACK",
            "message": f"Group ID set: {label} (ACK)",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_monitor_id_set(client: SicpClient, monitor_id: int, config: CliConfig) -> int:
    transaction = client.transact_with_request(
        MONITOR_ID_SET_COMMAND,
        monitor_id,
        expected_response_commands=(0x00,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Monitor ID set did not return a response")
    require_ack(transaction.response)
    print_result(
        {
            "command": "monitor-id set",
            "requested_monitor_id": monitor_id,
            "status": "ACK",
            "message": f"Monitor ID set: {monitor_id} (ACK)",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_ports_lock_get(client: SicpClient, config: CliConfig) -> int:
    transaction = client.transact_with_request(
        PORTS_LOCK_GET_COMMAND,
        expected_response_commands=(PORTS_LOCK_GET_COMMAND,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Ports-lock get did not return a response")
    state = decode_ports_lock_report(transaction.response)
    print_result(
        {
            "command": "ports-lock get",
            "ports_lock": state,
            "message": f"MicroSD/USB ports: {state}",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_ports_lock_set(client: SicpClient, state: int, config: CliConfig) -> int:
    canonical = ports_lock_value_to_name(state)
    transaction = client.transact_with_request(
        PORTS_LOCK_SET_COMMAND,
        state,
        expected_response_commands=(0x00,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Ports-lock set did not return a response")
    require_ack(transaction.response)
    print_result(
        {
            "command": "ports-lock set",
            "requested_ports_lock": canonical,
            "requested_ports_lock_value": state,
            "status": "ACK",
            "message": f"MicroSD/USB ports set: {canonical} (ACK)",
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_schedule_get(client: SicpClient, page: int, config: CliConfig) -> int:
    transaction = client.transact_with_request(
        SCHEDULING_GET_COMMAND,
        page,
        expected_response_commands=(SCHEDULING_GET_COMMAND,),
        expected_response_sizes=(12, 13),
    )
    if transaction.response is None:
        raise SicpError("Scheduling get did not return a response")
    state = decode_scheduling_report(transaction.response)
    enabled = "enabled" if state.enabled else "disabled"
    start = state.start_time or "null"
    end = state.end_time or "null"
    days = ",".join(state.day_names)
    tag = f", tag={state.tag_name}" if state.tag_name is not None else ""
    print_result(
        {
            "command": "schedule get",
            "page": page,
            "schedule": state.to_dict(),
            "message": (
                f"Schedule page {page}: {enabled}, {start}-{end}, "
                f"source={state.source_name}, days={days}{tag}"
            ),
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def run_schedule_set(
    args: argparse.Namespace, client: SicpClient, config: CliConfig
) -> int:
    enabled = bool(args.enabled)
    start_hour, start_minute = args.start
    end_hour, end_minute = args.end
    page_state = (args.page << 4) | (0x01 if enabled else 0x00)
    parameters = [
        page_state,
        start_hour,
        start_minute,
        end_hour,
        end_minute,
        args.source,
        args.days,
    ]
    if args.tag is not None:
        parameters.append(args.tag)
    transaction = client.transact_with_request(
        SCHEDULING_SET_COMMAND,
        *parameters,
        expected_response_commands=(0x00,),
        expected_response_sizes=(6,),
    )
    if transaction.response is None:
        raise SicpError("Scheduling set did not return a response")
    require_ack(transaction.response)
    start = f"{start_hour:02d}:{start_minute:02d}" if args.start != (24, 60) else "null"
    end = f"{end_hour:02d}:{end_minute:02d}" if args.end != (24, 60) else "null"
    source = scheduling_source_value_to_name(args.source)
    days = ",".join(scheduling_days_value_to_names(args.days))
    tag = f", tag=tag-{args.tag}" if args.tag is not None else ""
    status = "enabled" if enabled else "disabled"
    print_result(
        {
            "command": "schedule set",
            "page": args.page,
            "requested_schedule": {
                "enabled": enabled,
                "start_time": None if args.start == (24, 60) else start,
                "end_time": None if args.end == (24, 60) else end,
                "source": args.source,
                "source_name": source,
                "days": args.days,
                "day_names": list(scheduling_days_value_to_names(args.days)),
                "tag": args.tag,
                "tag_name": f"tag-{args.tag}" if args.tag is not None else None,
            },
            "status": "ACK",
            "message": (
                f"Schedule page {args.page} set: {status}, {start}-{end}, "
                f"source={source}, days={days}{tag} (ACK)"
            ),
            "request_raw": hex_bytes(transaction.request),
            "response": packet_dict(transaction.response),
            "skipped": [packet_dict(packet) for packet in transaction.skipped],
        },
        config,
    )
    return 0


def config_transact_get(
    client: SicpClient,
    command: int,
    decoder: Callable[[SicpPacket], Any],
    *,
    parameters: tuple[int, ...] = (),
    expected_response_sizes: tuple[int, ...] | None = None,
) -> Any:
    transaction = client.transact_with_request(
        command,
        *parameters,
        expected_response_commands=(command,),
        expected_response_sizes=expected_response_sizes,
    )
    if transaction.response is None:
        raise SicpError(f"Config get 0x{command:02X} did not return a response")
    value = decoder(transaction.response)
    return value.to_dict() if hasattr(value, "to_dict") else value


def config_transact_set(
    client: SicpClient,
    command: int,
    *parameters: int,
    expected_response_sizes: tuple[int, ...] = (6,),
) -> None:
    transaction = client.transact_with_request(
        command,
        *parameters,
        expected_response_commands=(0x00,),
        expected_response_sizes=expected_response_sizes,
    )
    if transaction.response is None:
        raise SicpError(f"Config set 0x{command:02X} did not return a response")
    require_ack(transaction.response)


def require_dict(value: Any, key: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{key} must be an object")
    return value


def require_bool(value: Any, name: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{name} must be true or false")
    return value


def require_int(value: Any, name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(f"{name} must be an integer")
    return value


def require_optional_int(value: Any, name: str) -> int | None:
    if value is None:
        return None
    return require_int(value, name)


def require_str(value: Any, name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{name} must be a string")
    return value


def require_named_or_int(
    data: dict[str, Any],
    int_key: str,
    name_key: str,
    converter: Callable[[str], int],
) -> int:
    raw_int = data.get(int_key)
    if isinstance(raw_int, int) and not isinstance(raw_int, bool):
        return raw_int
    return converter(require_str(data.get(name_key), name_key))


def config_format_value(value: Any) -> str:
    if isinstance(value, dict):
        parts = []
        for key, item in value.items():
            if isinstance(item, list):
                item = ",".join(str(part) for part in item)
            parts.append(f"{key}={item}")
        return ", ".join(parts)
    return str(value)


def config_get_power(client: SicpClient) -> str:
    return (
        "on"
        if config_transact_get(
            client,
            POWER_GET_COMMAND,
            decode_power_report,
            expected_response_sizes=(6,),
        )
        else "off"
    )


def config_set_power(client: SicpClient, value: Any) -> None:
    state = require_str(value, "power")
    if state not in ("on", "off"):
        raise ValueError("power must be on or off")
    config_transact_set(client, POWER_SET_COMMAND, bool_to_power_value(state == "on"))


def config_set_power_cold_start(client: SicpClient, value: Any) -> None:
    config_transact_set(
        client,
        POWER_COLD_START_SET_COMMAND,
        power_cold_start_name_to_value(require_str(value, "power_cold_start")),
    )


def config_set_input_source(client: SicpClient, value: Any) -> None:
    data = require_dict(value, "input_source")
    source = data.get("source_name", data.get("source"))
    source_value = (
        input_source_name_to_value(source)
        if isinstance(source, str)
        else require_int(source, "input_source.source")
    )
    playlist = require_int(data.get("playlist", 0), "input_source.playlist")
    display_style = require_str(
        data.get("display_style", "source-label"),
        "input_source.display_style",
    )
    do_not_switch = require_bool(
        data.get("do_not_switch", False),
        "input_source.do_not_switch",
    )
    mute_style = require_int(data.get("mute_style", 0), "input_source.mute_style")
    config_transact_set(
        client,
        INPUT_SOURCE_SET_COMMAND,
        source_value,
        playlist,
        build_input_source_osd_style(
            do_not_switch=do_not_switch,
            display_style=display_style,
        ),
        mute_style,
    )


def config_set_auto_signal(client: SicpClient, value: Any) -> None:
    config_transact_set(
        client,
        AUTO_SIGNAL_SET_COMMAND,
        auto_signal_name_to_value(require_str(value, "auto_signal")),
    )


def config_set_failover(client: SicpClient, value: Any) -> None:
    data = require_dict(value, "failover")
    raw_sources = data.get("priority_names", data.get("priorities"))
    if not isinstance(raw_sources, list):
        raise ValueError("failover.priority_names must be a list")
    values = tuple(
        failover_source_name_to_value(item)
        if isinstance(item, str)
        else require_int(item, "failover.priorities[]")
        for item in raw_sources
    )
    validate_failover_priorities(values)
    config_transact_set(client, FAILOVER_SET_COMMAND, *values)


def config_set_fan_speed(client: SicpClient, value: Any) -> None:
    config_transact_set(
        client,
        FAN_SPEED_SET_COMMAND,
        fan_speed_name_to_value(require_str(value, "fan_speed")),
    )


def config_set_volume(client: SicpClient, value: Any) -> None:
    data = require_dict(value, "volume")
    speaker = validate_volume_level(require_int(data.get("speaker"), "volume.speaker"))
    audio = require_optional_int(data.get("audio"), "volume.audio")
    parameters = [speaker]
    if audio is not None:
        parameters.append(validate_volume_level(audio))
    config_transact_set(client, VOLUME_SET_COMMAND, *parameters)


def config_get_volume_limit(client: SicpClient, target: str) -> dict[str, Any]:
    get_command, _set_command = volume_limit_command_pair(target)
    return cast(
        dict[str, Any],
        config_transact_get(
            client,
            get_command,
            lambda packet: decode_volume_limit_report(packet, target=target),
            expected_response_sizes=(8,),
        ),
    )


def config_set_volume_limit(client: SicpClient, target: str, value: Any) -> None:
    data = require_dict(value, f"volume_limit_{target}")
    minimum = require_int(data.get("minimum"), "volume_limit.minimum")
    maximum = require_int(data.get("maximum"), "volume_limit.maximum")
    switch_on = require_int(data.get("switch_on"), "volume_limit.switch_on")
    validate_volume_limits(minimum, maximum, switch_on)
    _get_command, set_command = volume_limit_command_pair(target)
    config_transact_set(client, set_command, minimum, maximum, switch_on)


def config_set_volume_audio(client: SicpClient, value: Any) -> None:
    data = require_dict(value, "volume_audio")
    config_transact_set(
        client,
        AUDIO_PARAMETERS_SET_COMMAND,
        parse_audio_parameter_value(str(data.get("treble")), "treble"),
        parse_audio_parameter_value(str(data.get("bass")), "bass"),
    )


def config_set_volume_mute(client: SicpClient, value: Any) -> None:
    state = require_str(value, "volume_mute")
    if state not in ("on", "off"):
        raise ValueError("volume_mute must be on or off")
    config_transact_set(
        client, VOLUME_MUTE_SET_COMMAND, bool_to_mute_value(state == "on")
    )


def config_get_lock(client: SicpClient, target: str) -> str:
    command = IR_LOCK_GET_COMMAND if target == "ir" else KEYPAD_LOCK_GET_COMMAND
    decoder = decode_ir_lock_report if target == "ir" else decode_keypad_lock_report
    return cast(
        str,
        config_transact_get(client, command, decoder, expected_response_sizes=(6,)),
    )


def config_set_lock(client: SicpClient, target: str, value: Any) -> None:
    command = IR_LOCK_SET_COMMAND if target == "ir" else KEYPAD_LOCK_SET_COMMAND
    config_transact_set(
        client,
        command,
        lock_state_name_to_value(require_str(value, f"lock_{target}"), target=target),
    )


def config_set_video_parameters(client: SicpClient, value: Any) -> None:
    data = require_dict(value, "video_parameters")
    gamma = data.get("gamma_name", data.get("gamma"))
    gamma_value = (
        gamma_name_to_value(gamma)
        if isinstance(gamma, str)
        else require_int(gamma, "video_parameters.gamma")
    )
    values = [
        validate_percentage(
            require_int(data.get(name), f"video_parameters.{name}"), name
        )
        for name in (
            "brightness",
            "color",
            "contrast",
            "sharpness",
            "tint",
            "black_level",
        )
    ]
    config_transact_set(client, VIDEO_PARAMETERS_SET_COMMAND, *values, gamma_value)


def config_set_picture_format(client: SicpClient, value: Any) -> None:
    raw = require_str(value, "picture_format") if isinstance(value, str) else value
    config_transact_set(
        client,
        PICTURE_FORMAT_SET_COMMAND,
        picture_format_name_to_value(raw)
        if isinstance(raw, str)
        else require_int(raw, "picture_format"),
    )


def config_set_color_temperature(client: SicpClient, value: Any) -> None:
    config_transact_set(
        client,
        COLOR_TEMPERATURE_SET_COMMAND,
        color_temperature_name_to_value(require_str(value, "color_temperature")),
    )


def config_set_rgb_parameters(client: SicpClient, value: Any) -> None:
    data = require_dict(value, "rgb_parameters")
    config_transact_set(
        client,
        RGB_PARAMETERS_SET_COMMAND,
        *(
            parse_byte(str(data.get(name)))
            for name in (
                "red_gain",
                "green_gain",
                "blue_gain",
                "red_offset",
                "green_offset",
                "blue_offset",
            )
        ),
    )


def config_set_color_temperature_100k(client: SicpClient, value: Any) -> None:
    config_transact_set(
        client,
        COLOR_TEMPERATURE_100K_SET_COMMAND,
        validate_color_temperature_100k_steps(
            require_int(value, "color_temperature_100k")
        ),
    )


def config_set_power_saving(client: SicpClient, value: Any) -> None:
    config_transact_set(
        client,
        POWER_SAVING_MODE_SET_COMMAND,
        power_saving_mode_name_to_value(require_str(value, "power_saving")),
    )


def config_set_tiling(client: SicpClient, value: Any) -> None:
    data = require_dict(value, "tiling")
    enabled = 1 if require_bool(data.get("enabled"), "tiling.enabled") else 0
    frame_comp = (
        1
        if require_bool(
            data.get("frame_compensation"),
            "tiling.frame_compensation",
        )
        else 0
    )
    position = parse_byte(str(data.get("position")))
    wall_size = parse_byte(str(data.get("wall_size")))
    config_transact_set(
        client, TILING_SET_COMMAND, enabled, frame_comp, position, wall_size
    )


def config_set_switch_on_delay(client: SicpClient, value: Any) -> None:
    raw = value.get("value") if isinstance(value, dict) else value
    delay = (
        switch_on_delay_name_to_value(raw)
        if isinstance(raw, str)
        else require_int(raw, "switch_on_delay")
    )
    config_transact_set(client, SWITCH_ON_DELAY_SET_COMMAND, delay)


def config_get_frame_compensation(client: SicpClient, axis: str) -> int:
    get_command, _set_command = frame_compensation_commands(axis)
    return cast(
        int,
        config_transact_get(
            client,
            get_command,
            lambda packet: decode_frame_compensation_report(axis, packet),
            expected_response_sizes=(6,),
        ),
    )


def config_set_frame_compensation(client: SicpClient, axis: str, value: Any) -> None:
    _get_command, set_command = frame_compensation_commands(axis)
    config_transact_set(client, set_command, parse_byte(str(value)))


def config_set_anytile(client: SicpClient, value: Any) -> None:
    data = require_dict(value, "anytile")
    parameters = build_anytile_parameters(
        1 if require_bool(data.get("enabled"), "anytile.enabled") else 0,
        require_int(data.get("rotation"), "anytile.rotation"),
        require_int(data.get("input_h_start"), "anytile.input_h_start"),
        require_int(data.get("input_v_start"), "anytile.input_v_start"),
        require_int(data.get("input_h_size"), "anytile.input_h_size"),
        require_int(data.get("input_v_size"), "anytile.input_v_size"),
    )
    config_transact_set(client, ANYTILE_SET_COMMAND, *parameters)


def config_set_anytile_resolution(client: SicpClient, value: Any) -> None:
    mode = (
        anytile_resolution_name_to_value(value)
        if isinstance(value, str)
        else require_int(value, "anytile_resolution")
    )
    config_transact_set(client, ANYTILE_RESOLUTION_SET_COMMAND, mode)


def config_set_power_saving_status(client: SicpClient, value: Any) -> None:
    status = (
        power_saving_mode_status_name_to_value(value)
        if isinstance(value, str)
        else require_int(value, "power_saving_status")
    )
    config_transact_set(client, POWER_SAVING_MODE_STATUS_SET_COMMAND, status)


def config_set_apm_status(client: SicpClient, value: Any) -> None:
    status = (
        apm_status_name_to_value(value)
        if isinstance(value, str)
        else require_int(value, "apm_status")
    )
    config_transact_set(client, APM_STATUS_SET_COMMAND, status)


def config_set_named_byte(
    client: SicpClient,
    command: int,
    converter: Callable[[str], int],
    key: str,
    value: Any,
) -> None:
    config_transact_set(client, command, converter(require_str(value, key)))


def config_set_display_orientation(client: SicpClient, value: Any) -> None:
    data = require_dict(value, "display_orientation")
    values = validate_display_orientation_values(
        require_named_or_int(
            data,
            "auto_rotate",
            "auto_rotate_name",
            display_orientation_auto_rotate_name_to_value,
        ),
        require_named_or_int(
            data,
            "osd_rotation",
            "osd_rotation_name",
            display_orientation_osd_rotation_name_to_value,
        ),
        require_named_or_int(
            data,
            "image_all",
            "image_all_name",
            display_orientation_image_all_name_to_value,
        ),
        require_named_or_int(
            data,
            "window1",
            "window1_name",
            display_orientation_window_name_to_value,
        ),
        require_named_or_int(
            data,
            "window2",
            "window2_name",
            display_orientation_window_name_to_value,
        ),
        require_named_or_int(
            data,
            "window3",
            "window3_name",
            display_orientation_window_name_to_value,
        ),
        require_named_or_int(
            data,
            "window4",
            "window4_name",
            display_orientation_window_name_to_value,
        ),
    )
    config_transact_set(client, DISPLAY_ORIENTATION_SET_COMMAND, *values)


def config_set_scan_mode(client: SicpClient, value: Any) -> None:
    mode = (
        scan_mode_name_to_value(value)
        if isinstance(value, str)
        else require_int(value, "scan_mode")
    )
    config_transact_set(client, SCAN_MODE_SET_COMMAND, mode)


def config_set_scan_conversion(client: SicpClient, value: Any) -> None:
    config_transact_set(
        client,
        SCAN_CONVERSION_SET_COMMAND,
        scan_conversion_name_to_value(require_str(value, "scan_conversion")),
    )


def config_set_pixel_shift(client: SicpClient, value: Any) -> None:
    raw = (
        pixel_shift_name_to_value(value)
        if isinstance(value, str)
        else require_int(value, "pixel_shift")
    )
    config_transact_set(client, PIXEL_SHIFT_SET_COMMAND, raw)


def config_set_information_osd(client: SicpClient, value: Any) -> None:
    raw = value.get("value") if isinstance(value, dict) else value
    info = (
        information_osd_name_to_value(raw)
        if isinstance(raw, str)
        else require_int(raw, "information_osd")
    )
    config_transact_set(client, INFORMATION_OSD_SET_COMMAND, info)


def config_set_off_timer(client: SicpClient, value: Any) -> None:
    hours = (
        off_timer_name_to_value(value)
        if isinstance(value, str)
        else require_int(value, "off_timer")
    )
    config_transact_set(client, OFF_TIMER_SET_COMMAND, hours)


def config_set_eco_mode(client: SicpClient, value: Any) -> None:
    mode = (
        eco_mode_name_to_value(value)
        if isinstance(value, str)
        else require_int(value, "eco_mode")
    )
    config_transact_set(client, ECO_MODE_SET_COMMAND, mode)


def config_set_picture_style(client: SicpClient, value: Any) -> None:
    style = (
        picture_style_name_to_value(value)
        if isinstance(value, str)
        else require_int(value, "picture_style")
    )
    config_transact_set(client, PICTURE_STYLE_SET_COMMAND, style)


def config_get_group_id(client: SicpClient) -> str:
    group_id = config_transact_get(
        client,
        GROUP_ID_GET_COMMAND,
        decode_group_id_report,
        expected_response_sizes=(6,),
    )
    return "off" if group_id is None else str(group_id)


def config_set_group_id(client: SicpClient, value: Any) -> None:
    group_id = group_id_name_to_value(str(value))
    config_transact_set(client, GROUP_ID_SET_COMMAND, group_id)


def config_set_ports_lock(client: SicpClient, value: Any) -> None:
    state = (
        ports_lock_name_to_value(value)
        if isinstance(value, str)
        else require_int(value, "ports_lock")
    )
    config_transact_set(client, PORTS_LOCK_SET_COMMAND, state)


def config_get_schedule(client: SicpClient, page: int) -> dict[str, Any]:
    return cast(
        dict[str, Any],
        config_transact_get(
            client,
            SCHEDULING_GET_COMMAND,
            decode_scheduling_report,
            parameters=(page,),
            expected_response_sizes=(12, 13),
        ),
    )


def config_set_schedule(client: SicpClient, page: int, value: Any) -> None:
    data = require_dict(value, f"schedule_{page}")
    enabled = require_bool(data.get("enabled"), "schedule.enabled")
    start = parse_scheduling_time(data.get("start_time") or "null")
    end = parse_scheduling_time(data.get("end_time") or "null")
    raw_source = data.get("source_name", data.get("source"))
    source = (
        scheduling_source_name_to_value(raw_source)
        if isinstance(raw_source, str)
        else require_int(raw_source, "schedule.source")
    )
    raw_days = data.get("day_names", data.get("days"))
    if isinstance(raw_days, list):
        days = scheduling_days_name_to_value(",".join(str(day) for day in raw_days))
    elif isinstance(raw_days, str):
        days = scheduling_days_name_to_value(raw_days)
    else:
        days = require_int(raw_days, "schedule.days")
    tag = require_optional_int(data.get("tag"), "schedule.tag")
    parameters = [
        (page << 4) | (0x01 if enabled else 0x00),
        start[0],
        start[1],
        end[0],
        end[1],
        source,
        days,
    ]
    if tag is not None:
        validated_tag = validate_scheduling_tag(tag)
        if validated_tag is None:
            raise ValueError("schedule.tag must be in range 1..7")
        parameters.append(validated_tag)
    config_transact_set(client, SCHEDULING_SET_COMMAND, *parameters)


def build_config_registry() -> list[ConfigEntry]:
    def switch_on_delay_config(client: SicpClient) -> dict[str, Any]:
        value = config_transact_get(
            client,
            SWITCH_ON_DELAY_GET_COMMAND,
            decode_switch_on_delay_report,
            expected_response_sizes=(6,),
        )
        return {"value": value, "display": switch_on_delay_value_to_name(value)}

    def information_osd_config(client: SicpClient) -> dict[str, Any]:
        value = config_transact_get(
            client,
            INFORMATION_OSD_GET_COMMAND,
            decode_information_osd_report,
            expected_response_sizes=(6,),
        )
        return {"value": value, "display": information_osd_value_to_name(value)}

    entries = [
        ConfigEntry("power", "Power", config_get_power, config_set_power),
        ConfigEntry(
            "power_cold_start",
            "Cold-start power",
            lambda client: config_transact_get(
                client,
                POWER_COLD_START_GET_COMMAND,
                decode_power_cold_start_report,
                expected_response_sizes=(6,),
            ),
            config_set_power_cold_start,
        ),
        ConfigEntry(
            "input_source",
            "Input source",
            lambda client: config_transact_get(
                client,
                INPUT_SOURCE_GET_COMMAND,
                decode_input_source_report,
                expected_response_sizes=(9,),
            ),
            config_set_input_source,
            config_format_value,
        ),
        ConfigEntry(
            "auto_signal",
            "Auto signal",
            lambda client: config_transact_get(
                client,
                AUTO_SIGNAL_GET_COMMAND,
                decode_auto_signal_report,
                expected_response_sizes=(6,),
            ),
            config_set_auto_signal,
        ),
        ConfigEntry(
            "failover",
            "Failover",
            lambda client: config_transact_get(
                client, FAILOVER_GET_COMMAND, decode_failover_report
            ),
            config_set_failover,
            config_format_value,
        ),
        ConfigEntry(
            "fan_speed",
            "Fan speed",
            lambda client: config_transact_get(
                client,
                FAN_SPEED_GET_COMMAND,
                decode_fan_speed_report,
                expected_response_sizes=(6,),
            ),
            config_set_fan_speed,
        ),
        ConfigEntry(
            "volume",
            "Volume",
            lambda client: config_transact_get(
                client,
                VOLUME_GET_COMMAND,
                decode_volume_report,
                expected_response_sizes=(6, 7),
            ),
            config_set_volume,
            config_format_value,
        ),
        ConfigEntry(
            "volume_limit_speaker",
            "Speaker volume limit",
            lambda client: config_get_volume_limit(client, "speaker"),
            lambda client, value: config_set_volume_limit(client, "speaker", value),
            config_format_value,
        ),
        ConfigEntry(
            "volume_limit_audio",
            "Audio volume limit",
            lambda client: config_get_volume_limit(client, "audio"),
            lambda client, value: config_set_volume_limit(client, "audio", value),
            config_format_value,
        ),
        ConfigEntry(
            "volume_audio",
            "Audio parameters",
            lambda client: config_transact_get(
                client,
                AUDIO_PARAMETERS_GET_COMMAND,
                decode_audio_parameters_report,
                expected_response_sizes=(7,),
            ),
            config_set_volume_audio,
            config_format_value,
        ),
        ConfigEntry(
            "volume_mute",
            "Volume mute",
            lambda client: (
                "on"
                if config_transact_get(
                    client,
                    VOLUME_MUTE_GET_COMMAND,
                    decode_volume_mute_report,
                    expected_response_sizes=(6,),
                )
                else "off"
            ),
            config_set_volume_mute,
        ),
        ConfigEntry(
            "lock_ir",
            "IR remote lock",
            lambda client: config_get_lock(client, "ir"),
            lambda client, value: config_set_lock(client, "ir", value),
        ),
        ConfigEntry(
            "lock_keypad",
            "Keypad lock",
            lambda client: config_get_lock(client, "keypad"),
            lambda client, value: config_set_lock(client, "keypad", value),
        ),
        ConfigEntry(
            "video_parameters",
            "Video parameters",
            lambda client: config_transact_get(
                client,
                VIDEO_PARAMETERS_GET_COMMAND,
                decode_video_parameters_report,
                expected_response_sizes=(12,),
            ),
            config_set_video_parameters,
            config_format_value,
        ),
        ConfigEntry(
            "picture_format",
            "Picture format",
            lambda client: config_transact_get(
                client,
                PICTURE_FORMAT_GET_COMMAND,
                decode_picture_format_report,
                expected_response_sizes=(6,),
            ),
            config_set_picture_format,
        ),
        ConfigEntry(
            "color_temperature",
            "Color temperature",
            lambda client: config_transact_get(
                client,
                COLOR_TEMPERATURE_GET_COMMAND,
                decode_color_temperature_report,
                expected_response_sizes=(6,),
            ),
            config_set_color_temperature,
        ),
        ConfigEntry(
            "rgb_parameters",
            "RGB parameters",
            lambda client: config_transact_get(
                client,
                RGB_PARAMETERS_GET_COMMAND,
                decode_rgb_parameters_report,
                expected_response_sizes=(11,),
            ),
            config_set_rgb_parameters,
            config_format_value,
        ),
        ConfigEntry(
            "color_temperature_100k",
            "Color temperature 100K",
            lambda client: config_transact_get(
                client,
                COLOR_TEMPERATURE_100K_GET_COMMAND,
                decode_color_temperature_100k_report,
                expected_response_sizes=(6,),
            ),
            config_set_color_temperature_100k,
        ),
        ConfigEntry(
            "power_saving",
            "Power-saving mode",
            lambda client: config_transact_get(
                client,
                POWER_SAVING_MODE_GET_COMMAND,
                decode_power_saving_mode_report,
                expected_response_sizes=(6,),
            ),
            config_set_power_saving,
        ),
        ConfigEntry(
            "tiling",
            "Tiling",
            lambda client: config_transact_get(
                client,
                TILING_GET_COMMAND,
                decode_tiling_report,
                expected_response_sizes=(9,),
            ),
            config_set_tiling,
            config_format_value,
        ),
        ConfigEntry(
            "switch_on_delay",
            "Switch-on delay",
            switch_on_delay_config,
            config_set_switch_on_delay,
            config_format_value,
        ),
        ConfigEntry(
            "frame_compensation_horizontal",
            "Horizontal frame compensation",
            lambda client: config_get_frame_compensation(client, "horizontal"),
            lambda client, value: config_set_frame_compensation(
                client, "horizontal", value
            ),
        ),
        ConfigEntry(
            "frame_compensation_vertical",
            "Vertical frame compensation",
            lambda client: config_get_frame_compensation(client, "vertical"),
            lambda client, value: config_set_frame_compensation(
                client, "vertical", value
            ),
        ),
        ConfigEntry(
            "anytile",
            "AnyTile",
            lambda client: config_transact_get(
                client,
                ANYTILE_GET_COMMAND,
                decode_anytile_report,
                expected_response_sizes=(16,),
            ),
            config_set_anytile,
            config_format_value,
        ),
        ConfigEntry(
            "anytile_resolution",
            "AnyTile resolution",
            lambda client: config_transact_get(
                client,
                ANYTILE_RESOLUTION_GET_COMMAND,
                decode_anytile_resolution_report,
                expected_response_sizes=(6,),
            ),
            config_set_anytile_resolution,
        ),
        ConfigEntry(
            "power_saving_status",
            "Power-saving status",
            lambda client: config_transact_get(
                client,
                POWER_SAVING_MODE_STATUS_GET_COMMAND,
                decode_power_saving_mode_status_report,
                expected_response_sizes=(6,),
            ),
            config_set_power_saving_status,
        ),
        ConfigEntry(
            "apm_status",
            "APM status",
            lambda client: config_transact_get(
                client,
                APM_STATUS_GET_COMMAND,
                decode_apm_status_report,
                expected_response_sizes=(6,),
            ),
            config_set_apm_status,
        ),
        ConfigEntry(
            "light_sensor",
            "Light sensor",
            lambda client: config_transact_get(
                client,
                LIGHT_SENSOR_GET_COMMAND,
                decode_light_sensor_report,
                expected_response_sizes=(6,),
            ),
            lambda client, value: config_set_named_byte(
                client,
                LIGHT_SENSOR_SET_COMMAND,
                light_sensor_name_to_value,
                "light_sensor",
                value,
            ),
        ),
        ConfigEntry(
            "osd_rotating",
            "OSD rotating",
            lambda client: config_transact_get(
                client,
                OSD_ROTATING_GET_COMMAND,
                decode_osd_rotating_report,
                expected_response_sizes=(6,),
            ),
            lambda client, value: config_set_named_byte(
                client,
                OSD_ROTATING_SET_COMMAND,
                osd_rotating_name_to_value,
                "osd_rotating",
                value,
            ),
        ),
        ConfigEntry(
            "display_orientation",
            "Display orientation",
            lambda client: config_transact_get(
                client,
                DISPLAY_ORIENTATION_GET_COMMAND,
                decode_display_orientation_report,
                expected_response_sizes=(12,),
            ),
            config_set_display_orientation,
            config_format_value,
        ),
        ConfigEntry(
            "touch_feature",
            "Touch feature",
            lambda client: config_transact_get(
                client,
                TOUCH_FEATURE_GET_COMMAND,
                decode_touch_feature_report,
                expected_response_sizes=(6,),
            ),
            lambda client, value: config_set_named_byte(
                client,
                TOUCH_FEATURE_SET_COMMAND,
                touch_feature_name_to_value,
                "touch_feature",
                value,
            ),
        ),
        ConfigEntry(
            "noise_reduction",
            "Noise reduction",
            lambda client: config_transact_get(
                client,
                NOISE_REDUCTION_GET_COMMAND,
                decode_noise_reduction_report,
                expected_response_sizes=(6,),
            ),
            lambda client, value: config_set_named_byte(
                client,
                NOISE_REDUCTION_SET_COMMAND,
                noise_reduction_name_to_value,
                "noise_reduction",
                value,
            ),
        ),
        ConfigEntry(
            "scan_mode",
            "Scan mode",
            lambda client: config_transact_get(
                client,
                SCAN_MODE_GET_COMMAND,
                decode_scan_mode_report,
                expected_response_sizes=(6,),
            ),
            config_set_scan_mode,
        ),
        ConfigEntry(
            "scan_conversion",
            "Scan conversion",
            lambda client: config_transact_get(
                client,
                SCAN_CONVERSION_GET_COMMAND,
                decode_scan_conversion_report,
                expected_response_sizes=(6,),
            ),
            config_set_scan_conversion,
        ),
        ConfigEntry(
            "pixel_shift",
            "Pixel shift",
            lambda client: config_transact_get(
                client,
                PIXEL_SHIFT_GET_COMMAND,
                decode_pixel_shift_report,
                expected_response_sizes=(6,),
            ),
            config_set_pixel_shift,
        ),
        ConfigEntry(
            "memc",
            "MEMC",
            lambda client: config_transact_get(
                client,
                MEMC_EFFECT_GET_COMMAND,
                decode_memc_effect_report,
                expected_response_sizes=(6,),
            ),
            lambda client, value: config_set_named_byte(
                client,
                MEMC_EFFECT_SET_COMMAND,
                memc_effect_name_to_value,
                "memc",
                value,
            ),
        ),
        ConfigEntry(
            "information_osd",
            "Information OSD",
            information_osd_config,
            config_set_information_osd,
            config_format_value,
        ),
        ConfigEntry(
            "human_sensor",
            "Human sensor",
            lambda client: config_transact_get(
                client,
                HUMAN_SENSOR_GET_COMMAND,
                decode_human_sensor_report,
                expected_response_sizes=(6,),
            ),
            lambda client, value: config_set_named_byte(
                client,
                HUMAN_SENSOR_SET_COMMAND,
                human_sensor_name_to_value,
                "human_sensor",
                value,
            ),
        ),
        ConfigEntry(
            "power_on_logo",
            "Power on logo",
            lambda client: config_transact_get(
                client,
                POWER_ON_LOGO_GET_COMMAND,
                decode_power_on_logo_report,
                expected_response_sizes=(6,),
            ),
            lambda client, value: config_set_named_byte(
                client,
                POWER_ON_LOGO_SET_COMMAND,
                power_on_logo_name_to_value,
                "power_on_logo",
                value,
            ),
        ),
        ConfigEntry(
            "off_timer",
            "Off timer",
            lambda client: config_transact_get(
                client,
                OFF_TIMER_GET_COMMAND,
                decode_off_timer_report,
                expected_response_sizes=(6,),
            ),
            config_set_off_timer,
        ),
        ConfigEntry(
            "eco_mode",
            "ECO mode",
            lambda client: config_transact_get(
                client,
                ECO_MODE_GET_COMMAND,
                decode_eco_mode_report,
                expected_response_sizes=(6,),
            ),
            config_set_eco_mode,
        ),
        ConfigEntry(
            "picture_style",
            "Picture style",
            lambda client: config_transact_get(
                client,
                PICTURE_STYLE_GET_COMMAND,
                decode_picture_style_report,
                expected_response_sizes=(6,),
            ),
            config_set_picture_style,
        ),
        ConfigEntry("group_id", "Group ID", config_get_group_id, config_set_group_id),
        ConfigEntry(
            "ports_lock",
            "MicroSD/USB ports",
            lambda client: config_transact_get(
                client,
                PORTS_LOCK_GET_COMMAND,
                decode_ports_lock_report,
                expected_response_sizes=(6,),
            ),
            config_set_ports_lock,
        ),
    ]
    for page in range(1, 8):

        def get_schedule_page(client: SicpClient, page: int = page) -> dict[str, Any]:
            return config_get_schedule(client, page)

        def set_schedule_page(
            client: SicpClient,
            value: Any,
            page: int = page,
        ) -> None:
            config_set_schedule(client, page, value)

        entries.append(
            ConfigEntry(
                f"schedule_{page}",
                f"Schedule page {page}",
                get_schedule_page,
                set_schedule_page,
                config_format_value,
            )
        )
    return entries


def selected_config_entries(only: str | None) -> list[ConfigEntry]:
    entries = build_config_registry()
    if only is None:
        return entries
    requested = [key.strip() for key in only.split(",") if key.strip()]
    if not requested:
        raise ValueError("--only must include at least one setting key")
    by_key = {entry.key: entry for entry in entries}
    unknown = [key for key in requested if key not in by_key]
    if unknown:
        raise ValueError("unknown config setting(s): " + ", ".join(unknown))
    return [by_key[key] for key in requested]


def run_config_collect(
    args: argparse.Namespace, client: SicpClient, config: CliConfig
) -> int:
    settings: dict[str, Any] = {}
    errors: dict[str, str] = {}
    entries = selected_config_entries(args.only)
    for entry in entries:
        try:
            settings[entry.key] = entry.getter(client)
        except (ValueError, SicpError) as exc:
            errors[entry.key] = str(exc)

    if config.json_output:
        payload: dict[str, Any] = {
            "schema": CONFIG_SCHEMA,
            "settings": settings,
            "errors": errors,
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        by_key = {entry.key: entry for entry in entries}
        for key, value in settings.items():
            entry = by_key[key]
            print(f"{entry.label}: {entry.formatter(value)}")
        for key, error in errors.items():
            print(f"{key}: ERROR: {error}")
    return 0 if settings else 1


def load_config_document(path: str) -> dict[str, Any]:
    try:
        if path == "-":
            text = sys.stdin.read()
        else:
            with open(path, encoding="utf-8") as config_file:
                text = config_file.read()
    except OSError as exc:
        raise ValueError(f"could not read config JSON: {exc}") from exc
    try:
        document = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid config JSON: {exc}") from exc
    if not isinstance(document, dict):
        raise ValueError("config JSON must be an object")
    if document.get("schema") != CONFIG_SCHEMA:
        raise ValueError(f"config schema must be {CONFIG_SCHEMA}")
    settings = document.get("settings")
    if not isinstance(settings, dict):
        raise ValueError("config JSON must contain an object settings field")
    return document


def run_config_apply(
    args: argparse.Namespace, client: SicpClient, config: CliConfig
) -> int:
    document = load_config_document(args.path)
    settings = document["settings"]
    entries = selected_config_entries(args.only)
    by_key = {entry.key: entry for entry in entries}
    all_known_keys = {entry.key for entry in build_config_registry()}
    errors: dict[str, str] = {}
    applied: list[str] = []

    for key, value in settings.items():
        if args.only is not None and key not in by_key:
            continue
        entry = by_key.get(key)
        if entry is None:
            if args.ignore_unknown and key not in all_known_keys:
                continue
            errors[key] = "unknown config setting"
            if not args.continue_on_error:
                raise ValueError(f"{key}: unknown config setting")
            continue
        try:
            entry.setter(client, value)
            applied.append(key)
        except (ValueError, SicpError, argparse.ArgumentTypeError) as exc:
            errors[key] = str(exc)
            if not args.continue_on_error:
                raise SicpError(f"{key}: {exc}") from exc

    if config.json_output:
        print(
            json.dumps({"applied": applied, "errors": errors}, indent=2, sort_keys=True)
        )
    else:
        for key in applied:
            print(f"{key}: applied")
        for key, error in errors.items():
            print(f"{key}: ERROR: {error}")
    return 1 if errors else 0


def run_raw_data(client: SicpClient, data_args: list[str], config: CliConfig) -> int:
    data = parse_data_bytes(data_args)
    request = build_packet(
        data[0],
        *data[1:],
        monitor_id=client.monitor_id,
        group_id=client.group_id,
    )
    response = client.send_raw(request)
    if response is None:
        print_result(
            {
                "command": "raw data",
                "data": hex_bytes(bytes(data)),
                "reply_data": None,
                "message": "Reply DATA: <none>",
                "request_raw": hex_bytes(request),
                "response": None,
                "skipped": [],
            },
            config,
        )
        return 0

    reply_data = response.packet.data
    print_result(
        {
            "command": "raw data",
            "data": hex_bytes(bytes(data)),
            "reply_data": hex_bytes(reply_data),
            "reply_data_bytes": list(reply_data),
            "message": f"Reply DATA: {hex_bytes(reply_data)}",
            "request_raw": hex_bytes(request),
            "response": packet_dict(response.packet),
            "skipped": [packet_dict(packet) for packet in response.skipped],
        },
        config,
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        config = config_from_args(args, os.environ)
        client = SicpClient(
            host=config.host,
            port=config.port,
            monitor_id=config.monitor_id,
            group_id=config.group_id,
            timeout=config.timeout,
            retries=config.retries,
        )
        if args.group == "power" and args.action == "get":
            return run_power_get(client, config)
        if args.group == "power" and args.action == "set":
            return run_power_set(client, args.state, config)
        if args.group == "power" and args.action == "cold-start":
            if args.cold_start_action == "get":
                return run_power_cold_start_get(client, config)
            if args.cold_start_action == "set":
                return run_power_cold_start_set(client, args.state, config)
        if args.group == "input-source" and args.action == "get":
            return run_input_source_get(client, config)
        if args.group == "input-source" and args.action == "set":
            return run_input_source_set(
                client,
                args.source,
                args.playlist,
                args.display_style,
                args.do_not_switch,
                args.mute_style,
                config,
            )
        if args.group == "auto-signal" and args.action == "get":
            return run_auto_signal_get(client, config)
        if args.group == "auto-signal" and args.action == "set":
            return run_auto_signal_set(client, args.mode, config)
        if args.group in ("failover", "fallover") and args.action == "get":
            return run_failover_get(client, config)
        if args.group in ("failover", "fallover") and args.action == "set":
            return run_failover_set(client, args.sources, config)
        if args.group == "monitor" and args.action == "restart":
            return run_monitor_restart(client, args.target, config)
        if args.group == "temperature" and args.action == "get":
            return run_temperature_get(client, config)
        if args.group == "fan-speed" and args.action == "get":
            return run_fan_speed_get(client, config)
        if args.group == "fan-speed" and args.action == "set":
            return run_fan_speed_set(client, args.speed, config)
        if args.group == "volume" and args.action == "get":
            return run_volume_get(client, config)
        if args.group == "volume" and args.action == "set":
            return run_volume_set(args, client, config)
        if args.group == "volume" and args.action == "step":
            return run_volume_step(args, client, config)
        if args.group == "volume" and args.action == "limit":
            if args.limit_action == "get":
                return run_volume_limit_get(client, args.target, config)
            if args.limit_action == "set":
                return run_volume_limit_set(args, client, config)
        if args.group == "volume" and args.action == "audio":
            if args.audio_action == "get":
                return run_volume_audio_get(client, config)
            if args.audio_action == "set":
                return run_volume_audio_set(args, client, config)
        if args.group == "volume" and args.action == "mute":
            if args.mute_action == "get":
                return run_volume_mute_get(client, config)
            if args.mute_action == "set":
                return run_volume_mute_set(client, args.state, config)
        if args.group == "video-signal" and args.action == "get":
            return run_video_signal_get(client, config)
        if args.group == "lock" and args.action == "get":
            return run_lock_get(client, args.target, config)
        if args.group == "lock" and args.action == "set":
            return run_lock_set(client, args.target, args.state, config)
        if args.group == "video" and args.target == "parameters":
            if args.action == "get":
                return run_video_parameters_get(client, config)
            if args.action == "set":
                return run_video_parameters_set(args, client, config)
        if args.group == "video" and args.target == "picture-format":
            if args.action == "get":
                return run_picture_format_get(client, config)
            if args.action == "set":
                return run_picture_format_set(client, args.format, config)
        if args.group == "video" and args.target == "color-temperature":
            if args.action == "get":
                return run_color_temperature_get(client, config)
            if args.action == "set":
                return run_color_temperature_set(client, args.temperature, config)
        if args.group == "video" and args.target == "rgb":
            if args.action == "get":
                return run_rgb_parameters_get(client, config)
            if args.action == "set":
                return run_rgb_parameters_set(args, client, config)
        if args.group == "video" and args.target == "color-temperature-100k":
            if args.action == "get":
                return run_color_temperature_100k_get(client, config)
            if args.action == "set":
                return run_color_temperature_100k_set(client, args.steps, config)
        if args.group == "power-saving" and args.action == "set":
            return run_power_saving_set(client, args.mode, config)
        if args.group == "power-saving" and args.action == "get":
            return run_power_saving_get(client, config)
        if args.group == "operating-hours" and args.action == "get":
            return run_operating_hours_get(client, config)
        if args.group == "tiling" and args.action == "get":
            return run_tiling_get(client, config)
        if args.group == "tiling" and args.action == "set":
            return run_tiling_set(args, client, config)
        if args.group == "switch-on-delay" and args.action == "get":
            return run_switch_on_delay_get(client, config)
        if args.group == "switch-on-delay" and args.action == "set":
            return run_switch_on_delay_set(client, args.delay, config)
        if args.group == "frame-compensation" and args.action == "get":
            return run_frame_compensation_get(client, args.axis, config)
        if args.group == "frame-compensation" and args.action == "set":
            return run_frame_compensation_set(client, args.axis, args.value, config)
        if args.group == "anytile" and args.action == "get":
            return run_anytile_get(client, config)
        if args.group == "anytile" and args.action == "set":
            return run_anytile_set(args, client, config)
        if args.group == "anytile" and args.action == "resolution":
            if args.resolution_action == "get":
                return run_anytile_resolution_get(client, config)
            if args.resolution_action == "set":
                return run_anytile_resolution_set(client, args.mode, config)
        if args.group == "anytile" and args.action == "assign-id":
            return run_anytile_assign_id(args, client, config)
        if args.group == "anytile" and args.action == "display-id":
            if args.display_id_action == "set":
                return run_anytile_display_id_set(client, args.monitor_id, config)
        if args.group == "power-saving-status" and args.action == "set":
            return run_power_saving_status_set(client, args.status, config)
        if args.group == "power-saving-status" and args.action == "get":
            return run_power_saving_status_get(client, config)
        if args.group == "apm-status" and args.action == "set":
            return run_apm_status_set(client, args.status, config)
        if args.group == "apm-status" and args.action == "get":
            return run_apm_status_get(client, config)
        if args.group == "serial-code" and args.action == "get":
            return run_serial_code_get(client, config)
        if args.group == "light-sensor" and args.action == "get":
            return run_light_sensor_get(client, config)
        if args.group == "light-sensor" and args.action == "set":
            return run_light_sensor_set(client, args.state, config)
        if args.group == "osd-rotating" and args.action == "get":
            return run_osd_rotating_get(client, config)
        if args.group == "osd-rotating" and args.action == "set":
            return run_osd_rotating_set(client, args.state, config)
        if args.group == "display-orientation" and args.action == "get":
            return run_display_orientation_get(client, config)
        if args.group == "display-orientation" and args.action == "set":
            return run_display_orientation_set(args, client, config)
        if args.group == "touch-feature" and args.action == "get":
            return run_touch_feature_get(client, config)
        if args.group == "touch-feature" and args.action == "set":
            return run_touch_feature_set(client, args.state, config)
        if args.group == "noise-reduction" and args.action == "get":
            return run_noise_reduction_get(client, config)
        if args.group == "noise-reduction" and args.action == "set":
            return run_noise_reduction_set(client, args.level, config)
        if args.group == "scan-mode" and args.action == "get":
            return run_scan_mode_get(client, config)
        if args.group == "scan-mode" and args.action == "set":
            return run_scan_mode_set(client, args.mode, config)
        if args.group == "scan-conversion" and args.action == "get":
            return run_scan_conversion_get(client, config)
        if args.group == "scan-conversion" and args.action == "set":
            return run_scan_conversion_set(client, args.mode, config)
        if args.group == "pixel-shift" and args.action == "get":
            return run_pixel_shift_get(client, config)
        if args.group == "pixel-shift" and args.action == "set":
            return run_pixel_shift_set(client, args.value, config)
        if args.group == "memc" and args.action == "get":
            return run_memc_get(client, config)
        if args.group == "memc" and args.action == "set":
            return run_memc_set(client, args.level, config)
        if args.group == "information-osd" and args.action == "get":
            return run_information_osd_get(client, config)
        if args.group == "information-osd" and args.action == "set":
            return run_information_osd_set(client, args.value, config)
        if args.group == "human-sensor" and args.action == "get":
            return run_human_sensor_get(client, config)
        if args.group == "human-sensor" and args.action == "set":
            return run_human_sensor_set(client, args.state, config)
        if args.group == "factory-reset" and args.action == "set":
            return run_factory_reset_set(client, config)
        if args.group == "power-on-logo" and args.action == "get":
            return run_power_on_logo_get(client, config)
        if args.group == "power-on-logo" and args.action == "set":
            return run_power_on_logo_set(client, args.state, config)
        if args.group == "off-timer" and args.action == "get":
            return run_off_timer_get(client, config)
        if args.group == "off-timer" and args.action == "set":
            return run_off_timer_set(client, args.hours, config)
        if args.group == "eco-mode" and args.action == "get":
            return run_eco_mode_get(client, config)
        if args.group == "eco-mode" and args.action == "set":
            return run_eco_mode_set(client, args.mode, config)
        if args.group == "picture-style" and args.action == "get":
            return run_picture_style_get(client, config)
        if args.group == "picture-style" and args.action == "set":
            return run_picture_style_set(client, args.style, config)
        if args.group == "group-id" and args.action == "get":
            return run_group_id_get(client, config)
        if args.group == "group-id" and args.action == "set":
            return run_group_id_set(client, args.group_id, config)
        if args.group == "monitor-id" and args.action == "set":
            return run_monitor_id_set(client, args.monitor_id, config)
        if args.group == "ports-lock" and args.action == "get":
            return run_ports_lock_get(client, config)
        if args.group == "ports-lock" and args.action == "set":
            return run_ports_lock_set(client, args.state, config)
        if args.group == "schedule" and args.action == "get":
            return run_schedule_get(client, args.page, config)
        if args.group == "schedule" and args.action == "set":
            return run_schedule_set(args, client, config)
        if args.group == "config" and args.action == "collect":
            return run_config_collect(args, client, config)
        if args.group == "config" and args.action == "apply":
            return run_config_apply(args, client, config)
        if args.group == "raw" and args.action == "data":
            return run_raw_data(client, args.data, config)
    except (ValueError, SicpError) as exc:
        parser.exit(2, f"sicp: error: {exc}\n")

    parser.error("unsupported command")
    return 2


if __name__ == "__main__":
    sys.exit(main())
