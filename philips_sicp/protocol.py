"""Packet construction and parsing for Philips SICP."""

from __future__ import annotations

from dataclasses import dataclass


def validate_byte(value: int, name: str) -> int:
    if not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")
    if value < 0 or value > 0xFF:
        raise ValueError(f"{name} must be in range 0..255")
    return value


def xor_checksum(data: bytes) -> int:
    checksum = 0
    for value in data:
        checksum ^= value
    return checksum


def hex_bytes(data: bytes) -> str:
    return data.hex(" ").upper()


def build_packet(
    command: int,
    *parameters: int,
    monitor_id: int = 1,
    group_id: int = 0,
) -> bytes:
    validate_byte(command, "command")
    validate_byte(monitor_id, "monitor_id")
    validate_byte(group_id, "group_id")
    for index, parameter in enumerate(parameters):
        validate_byte(parameter, f"parameters[{index}]")

    data = bytes([command, *parameters])
    msg_size = 4 + len(data)
    packet_without_checksum = bytes([msg_size, monitor_id, group_id]) + data
    return packet_without_checksum + bytes([xor_checksum(packet_without_checksum)])


@dataclass(frozen=True)
class SicpPacket:
    raw: bytes
    msg_size: int
    monitor_id: int
    group_id: int
    data: bytes
    checksum: int

    @property
    def command(self) -> int | None:
        return self.data[0] if self.data else None

    @property
    def parameters(self) -> bytes:
        return self.data[1:] if len(self.data) > 1 else b""

    @property
    def raw_hex(self) -> str:
        return hex_bytes(self.raw)

    def to_dict(self) -> dict[str, object]:
        return {
            "raw": self.raw_hex,
            "msg_size": self.msg_size,
            "monitor_id": self.monitor_id,
            "group_id": self.group_id,
            "command": self.command,
            "parameters": hex_bytes(self.parameters),
            "checksum": self.checksum,
        }

    def command_matches(self, expected_commands: tuple[int, ...] | None) -> bool:
        return expected_commands is None or self.command in expected_commands


def parse_packet(raw: bytes) -> SicpPacket:
    if len(raw) < 4:
        raise ValueError(f"SICP packet is too short: {hex_bytes(raw)}")

    msg_size = raw[0]
    if len(raw) != msg_size:
        raise ValueError(
            f"Packet length mismatch: header says {msg_size}, "
            f"received {len(raw)}: {hex_bytes(raw)}"
        )

    expected_checksum = xor_checksum(raw[:-1])
    actual_checksum = raw[-1]
    if actual_checksum != expected_checksum:
        raise ValueError(
            f"Checksum mismatch: expected 0x{expected_checksum:02X}, "
            f"received 0x{actual_checksum:02X}: {hex_bytes(raw)}"
        )

    return SicpPacket(
        raw=raw,
        msg_size=msg_size,
        monitor_id=raw[1],
        group_id=raw[2],
        data=raw[3:-1],
        checksum=raw[-1],
    )
