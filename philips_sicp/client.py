"""TCP client and command wrappers for Philips SICP."""

from __future__ import annotations

import socket
from dataclasses import dataclass

from .protocol import SicpPacket, build_packet, hex_bytes, parse_packet, validate_byte

DEFAULT_PORT = 5000
DEFAULT_MONITOR_ID = 1
DEFAULT_GROUP_ID = 0
DEFAULT_TIMEOUT = 2.0
DEFAULT_RETRIES = 1

POWER_GET_COMMAND = 0x19
POWER_SET_COMMAND = 0x18
POWER_COLD_START_GET_COMMAND = 0xA4
POWER_COLD_START_SET_COMMAND = 0xA3
POWER_OFF = 0x01
POWER_ON = 0x02
POWER_COLD_START_OFF = 0x00
POWER_COLD_START_ON = 0x01
POWER_COLD_START_LAST = 0x02

OPERATING_HOURS_COMMAND = 0x0F
OPERATING_HOURS_ITEM = 0x02

TILING_GET_COMMAND = 0x23
TILING_SET_COMMAND = 0x22
TILING_STANDARD_MAX_H = 5
TILING_STANDARD_MAX_V = 5
TILING_STANDARD_MAX_POSITION = 25
TILING_ZERO_BEZEL_MAX_H = 15
TILING_ZERO_BEZEL_MAX_V = 10
TILING_ZERO_BEZEL_MAX_POSITION = 150
TILING_KEEP = 0x00
TILING_FRAME_COMP_KEEP = 0x02

SWITCH_ON_DELAY_GET_COMMAND = 0x55
SWITCH_ON_DELAY_SET_COMMAND = 0x54
SWITCH_ON_DELAY_OFF = 0x00
SWITCH_ON_DELAY_AUTO = 0x01
FRAME_COMPENSATION_HORIZONTAL_GET_COMMAND = 0x5E
FRAME_COMPENSATION_HORIZONTAL_SET_COMMAND = 0x5F
FRAME_COMPENSATION_VERTICAL_GET_COMMAND = 0x67
FRAME_COMPENSATION_VERTICAL_SET_COMMAND = 0x68

ANYTILE_ASSIGN_IDS_COMMAND = 0xC0
ANYTILE_DISPLAY_MONITOR_ID_SET_COMMAND = 0x4C
ANYTILE_GET_COMMAND = 0x4A
ANYTILE_SET_COMMAND = 0x4B
ANYTILE_RESOLUTION_GET_COMMAND = 0x4E
ANYTILE_RESOLUTION_SET_COMMAND = 0x4F
ANYTILE_RESOLUTION_NAMES = {
    0x00: "default",
    0x01: "fhd",
    0x02: "uhd4k",
}
ANYTILE_RESOLUTION_ALIASES = {
    **{name: value for value, name in ANYTILE_RESOLUTION_NAMES.items()},
    "uhd": 0x02,
    "4k": 0x02,
    "uhd-4k": 0x02,
}

INPUT_SOURCE_GET_COMMAND = 0xAD
INPUT_SOURCE_SET_COMMAND = 0xAC
INPUT_SOURCE_DISPLAY_STYLE_RESERVED = 0x00
INPUT_SOURCE_DISPLAY_STYLE_SOURCE_LABEL = 0x01

INPUT_SOURCE_NAMES = {
    0x01: "video",
    0x02: "s-video",
    0x03: "component",
    0x04: "cvi2",
    0x05: "vga",
    0x06: "hdmi2",
    0x07: "display-port2",
    0x08: "usb2",
    0x09: "card-dvi-d",
    0x0A: "display-port1",
    0x0B: "card-ops",
    0x0C: "usb1",
    0x0D: "hdmi",
    0x0E: "dvi-d",
    0x0F: "hdmi3",
    0x10: "browser",
    0x11: "smartcms",
    0x12: "dms",
    0x13: "internal-storage",
    0x14: "reserved14",
    0x15: "reserved15",
    0x16: "media-player",
    0x17: "pdf-player",
    0x18: "custom",
    0x19: "hdmi4",
    0x1A: "vga2",
    0x1B: "vga3",
    0x1C: "iwb",
}

INPUT_SOURCE_ALIASES = {
    **{name: value for value, name in INPUT_SOURCE_NAMES.items()},
    "cvi-2": 0x04,
    "dp2": 0x07,
    "displayport2": 0x07,
    "card-dvid": 0x09,
    "dp1": 0x0A,
    "displayport1": 0x0A,
    "ops": 0x0B,
    "dvid": 0x0E,
    "digital-media-server": 0x12,
    "internal": 0x13,
    "storage": 0x13,
    "mediaplayer": 0x16,
    "pdf": 0x17,
    "pdfplayer": 0x17,
}

AUTO_SIGNAL_GET_COMMAND = 0xAF
AUTO_SIGNAL_SET_COMMAND = 0xAE
AUTO_SIGNAL_NAMES = {
    0x00: "off",
    0x01: "all",
    0x02: "reserved",
    0x03: "pc-only",
    0x04: "video-only",
    0x05: "failover",
}
AUTO_SIGNAL_ALIASES = {
    **{name: value for value, name in AUTO_SIGNAL_NAMES.items()},
    "pc": 0x03,
    "pc-sources-only": 0x03,
    "video": 0x04,
    "video-sources-only": 0x04,
}

FAILOVER_GET_COMMAND = 0xA6
FAILOVER_SET_COMMAND = 0xA5
FAILOVER_SOURCE_NAMES = {
    0x00: "hdmi",
    0x01: "component",
    0x02: "composite",
    0x03: "display-port",
    0x04: "dvi-d",
    0x05: "vga",
    0x06: "ops",
    0x07: "usb",
    0x08: "browser",
    0x09: "smartcms",
    0x0A: "internal-storage",
    0x0B: "dms",
    0x0C: "hdmi2",
    0x0D: "hdmi3",
    0x0E: "usb-playlist",
    0x0F: "usb-autoplay",
    0x10: "media-player",
    0x11: "pdf-player",
    0x12: "custom",
    0x13: "hdmi4",
    0x14: "vga2",
    0x15: "vga3",
    0x16: "iwb",
}
FAILOVER_SOURCE_ALIASES = {
    **{name: value for value, name in FAILOVER_SOURCE_NAMES.items()},
    "dp": 0x03,
    "displayport": 0x03,
    "dvi": 0x04,
    "dvid": 0x04,
    "digital-media-server": 0x0B,
    "internal": 0x0A,
    "storage": 0x0A,
    "usbplaylist": 0x0E,
    "autoplay": 0x0F,
    "usbauto": 0x0F,
    "mediaplayer": 0x10,
    "pdf": 0x11,
    "pdfplayer": 0x11,
}

MONITOR_RESTART_COMMAND = 0x57
MONITOR_RESTART_TARGETS = {
    0x00: "android",
    0x01: "scalar",
}
MONITOR_RESTART_ALIASES = {
    **{name: value for value, name in MONITOR_RESTART_TARGETS.items()},
    "scaler": 0x01,
}

TEMPERATURE_GET_COMMAND = 0x2F

FAN_SPEED_GET_COMMAND = 0x62
FAN_SPEED_SET_COMMAND = 0x61
FAN_SPEED_NAMES = {
    0x00: "off",
    0x01: "auto",
    0x02: "low",
    0x03: "middle",
    0x04: "high",
}
FAN_SPEED_ALIASES = {
    **{name: value for value, name in FAN_SPEED_NAMES.items()},
    "medium": 0x03,
}

VIDEO_SIGNAL_PRESENT_COMMAND = 0x59

IR_LOCK_GET_COMMAND = 0x1D
IR_LOCK_SET_COMMAND = 0x1C
KEYPAD_LOCK_GET_COMMAND = 0x1B
KEYPAD_LOCK_SET_COMMAND = 0x1A
LOCK_STATE_NAMES = {
    0x01: "unlock-all",
    0x02: "lock-all",
    0x03: "lock-all-but-power",
    0x04: "lock-all-but-volume",
    0x05: "primary",
    0x06: "secondary",
    0x07: "lock-all-except-power-volume",
}
LOCK_STATE_ALIASES = {
    **{name: value for value, name in LOCK_STATE_NAMES.items()},
    "unlock": 0x01,
    "unlocked": 0x01,
    "lock": 0x02,
    "locked": 0x02,
    "master": 0x05,
    "daisy-chain": 0x06,
    "lock-all-but-power-volume": 0x07,
    "lock-all-except-power-and-volume": 0x07,
}
IR_LOCK_STATE_VALUES = frozenset(LOCK_STATE_NAMES)
KEYPAD_LOCK_STATE_VALUES = frozenset((0x01, 0x02, 0x03, 0x04, 0x07))

VIDEO_PARAMETERS_GET_COMMAND = 0x33
VIDEO_PARAMETERS_SET_COMMAND = 0x32
PICTURE_FORMAT_GET_COMMAND = 0x3B
PICTURE_FORMAT_SET_COMMAND = 0x3A
PICTURE_FORMAT_NAMES = {
    0x00: "normal",
    0x01: "custom",
    0x02: "real",
    0x03: "full",
    0x04: "21:9",
    0x05: "dynamic",
    0x06: "16:9",
}
PICTURE_FORMAT_ALIASES = {
    **{name: value for value, name in PICTURE_FORMAT_NAMES.items()},
    "4:3": 0x00,
    "normal-4:3": 0x00,
    "1:1": 0x02,
    "real-1:1": 0x02,
    "widescreen": 0x03,
    "wide": 0x03,
    "21-9": 0x04,
    "16-9": 0x06,
}
VOLUME_GET_COMMAND = 0x45
VOLUME_SET_COMMAND = 0x44
VOLUME_STEP_COMMAND = 0x41
VOLUME_LIMIT_SPEAKER_GET_COMMAND = 0xB6
VOLUME_LIMIT_SPEAKER_SET_COMMAND = 0xB8
VOLUME_LIMIT_AUDIO_GET_COMMAND = 0xB7
VOLUME_LIMIT_AUDIO_SET_COMMAND = 0xB9
AUDIO_PARAMETERS_GET_COMMAND = 0x43
AUDIO_PARAMETERS_SET_COMMAND = 0x42
VOLUME_MUTE_GET_COMMAND = 0x46
VOLUME_MUTE_SET_COMMAND = 0x47
VOLUME_STEP_NAMES = {
    0x00: "down",
    0x01: "up",
    0x02: "no-change",
}
VOLUME_STEP_ALIASES = {
    **{name: value for value, name in VOLUME_STEP_NAMES.items()},
    "decrease": 0x00,
    "minus": 0x00,
    "-": 0x00,
    "increase": 0x01,
    "plus": 0x01,
    "+": 0x01,
    "none": 0x02,
    "unchanged": 0x02,
}
COLOR_TEMPERATURE_GET_COMMAND = 0x35
COLOR_TEMPERATURE_SET_COMMAND = 0x34
RGB_PARAMETERS_GET_COMMAND = 0x37
RGB_PARAMETERS_SET_COMMAND = 0x36
COLOR_TEMPERATURE_100K_GET_COMMAND = 0x12
COLOR_TEMPERATURE_100K_SET_COMMAND = 0x11
GAMMA_NAMES = {
    0x01: "native",
    0x02: "s-gamma",
    0x03: "2.2",
    0x04: "2.4",
    0x05: "dicom",
}
GAMMA_ALIASES = {
    **{name: value for value, name in GAMMA_NAMES.items()},
    "s": 0x02,
    "sgamma": 0x02,
    "d-image": 0x05,
    "d-image-dicom": 0x05,
}
COLOR_TEMPERATURE_NAMES = {
    0x00: "user1",
    0x01: "native",
    0x02: "11000k",
    0x03: "10000k",
    0x04: "9300k",
    0x05: "7500k",
    0x06: "6500k",
    0x07: "5770k",
    0x08: "5500k",
    0x09: "5000k",
    0x0A: "4000k",
    0x0B: "3400k",
    0x0C: "3350k",
    0x0D: "3000k",
    0x0E: "2800k",
    0x0F: "2600k",
    0x10: "1850k",
    0x12: "user2",
}
COLOR_TEMPERATURE_ALIASES = {
    **{name: value for value, name in COLOR_TEMPERATURE_NAMES.items()},
    "user-1": 0x00,
    "user-2": 0x12,
}

POWER_SAVING_MODE_GET_COMMAND = 0xDE
POWER_SAVING_MODE_SET_COMMAND = 0xDD
POWER_SAVING_MODE_NAMES = {
    0x00: "off",
    0x01: "low",
    0x02: "medium",
    0x03: "high",
}
POWER_SAVING_MODE_ALIASES = {
    **{name: value for value, name in POWER_SAVING_MODE_NAMES.items()},
    "med": 0x02,
}

POWER_SAVING_MODE_STATUS_GET_COMMAND = 0xD3
POWER_SAVING_MODE_STATUS_SET_COMMAND = 0xD2
POWER_SAVING_MODE_STATUS_NAMES = {
    0x00: "rgb-off-video-off",
    0x01: "rgb-off-video-on",
    0x02: "rgb-on-video-off",
    0x03: "rgb-on-video-on",
    0x04: "mode-1",
    0x05: "mode-2",
    0x06: "mode-3",
    0x07: "mode-4",
}
POWER_SAVING_MODE_STATUS_ALIASES = {
    **{name: value for value, name in POWER_SAVING_MODE_STATUS_NAMES.items()},
    "rgb-video-off": 0x00,
    "all-off": 0x00,
    "rgb-off": 0x01,
    "video-on": 0x01,
    "video-off": 0x02,
    "rgb-on": 0x02,
    "rgb-video-on": 0x03,
    "all-on": 0x03,
}

APM_STATUS_GET_COMMAND = 0xD1
APM_STATUS_SET_COMMAND = 0xD0
APM_STATUS_NAMES = {
    0x00: "off",
    0x01: "on",
    0x02: "mode-1",
    0x03: "mode-2",
}
APM_STATUS_ALIASES = {
    **{name: value for value, name in APM_STATUS_NAMES.items()},
    "mode1": 0x02,
    "tcp-off-wol-on": 0x02,
    "mode2": 0x03,
    "tcp-on-wol-off": 0x03,
}

SERIAL_CODE_GET_COMMAND = 0x15

LIGHT_SENSOR_GET_COMMAND = 0x25
LIGHT_SENSOR_SET_COMMAND = 0x24
LIGHT_SENSOR_NAMES = {
    0x00: "off",
    0x01: "on",
    0xFF: "unavailable",
}
LIGHT_SENSOR_SET_NAMES = {
    0x00: "off",
    0x01: "on",
}
LIGHT_SENSOR_ALIASES = {
    **{name: value for value, name in LIGHT_SENSOR_NAMES.items()},
    "hw-unavailable": 0xFF,
    "hardware-unavailable": 0xFF,
}

OSD_ROTATING_GET_COMMAND = 0x27
OSD_ROTATING_SET_COMMAND = 0x26
OSD_ROTATING_NAMES = {
    0x00: "off",
    0x01: "on",
}
OSD_ROTATING_ALIASES = {
    **{name: value for value, name in OSD_ROTATING_NAMES.items()},
}

DISPLAY_ORIENTATION_GET_COMMAND = 0x16
DISPLAY_ORIENTATION_SET_COMMAND = 0x17
DISPLAY_ORIENTATION_AUTO_ROTATE_NAMES = {
    0x00: "off",
    0x01: "on",
}
DISPLAY_ORIENTATION_OSD_ROTATION_NAMES = {
    0x00: "landscape",
    0x01: "portrait",
}
DISPLAY_ORIENTATION_IMAGE_ALL_NAMES = {
    0x00: "off",
    0x01: "on",
    0x02: "clockwise",
    0x03: "counter-clockwise",
}
DISPLAY_ORIENTATION_WINDOW_NAMES = {
    0x00: "off",
    0x01: "on",
}
DISPLAY_ORIENTATION_AUTO_ROTATE_ALIASES = {
    **{name: value for value, name in DISPLAY_ORIENTATION_AUTO_ROTATE_NAMES.items()},
}
DISPLAY_ORIENTATION_OSD_ROTATION_ALIASES = {
    **{name: value for value, name in DISPLAY_ORIENTATION_OSD_ROTATION_NAMES.items()},
}
DISPLAY_ORIENTATION_IMAGE_ALL_ALIASES = {
    **{name: value for value, name in DISPLAY_ORIENTATION_IMAGE_ALL_NAMES.items()},
    "cw": 0x02,
    "on-clockwise": 0x02,
    "counterclockwise": 0x03,
    "ccw": 0x03,
    "on-counter-clockwise": 0x03,
}
DISPLAY_ORIENTATION_WINDOW_ALIASES = {
    **{name: value for value, name in DISPLAY_ORIENTATION_WINDOW_NAMES.items()},
}

TOUCH_FEATURE_GET_COMMAND = 0x1F
TOUCH_FEATURE_SET_COMMAND = 0x1E
TOUCH_FEATURE_NAMES = {
    0x00: "off",
    0x01: "on",
}
TOUCH_FEATURE_ALIASES = {
    **{name: value for value, name in TOUCH_FEATURE_NAMES.items()},
}

NOISE_REDUCTION_GET_COMMAND = 0x2B
NOISE_REDUCTION_SET_COMMAND = 0x2A
NOISE_REDUCTION_NAMES = {
    0x00: "off",
    0x01: "low",
    0x02: "middle",
    0x03: "high",
    0x04: "default",
}
NOISE_REDUCTION_ALIASES = {
    **{name: value for value, name in NOISE_REDUCTION_NAMES.items()},
    "medium": 0x02,
}

SCAN_MODE_GET_COMMAND = 0x51
SCAN_MODE_SET_COMMAND = 0x50
SCAN_MODE_NAMES = {
    0x00: "over-scan",
    0x01: "under-scan",
    0x02: "off",
}
SCAN_MODE_ALIASES = {
    **{name: value for value, name in SCAN_MODE_NAMES.items()},
    "overscan": 0x00,
    "over": 0x00,
    "on": 0x00,
    "underscan": 0x01,
    "under": 0x01,
}
SCAN_MODE_CUSTOM_MIN = 0x03
SCAN_MODE_CUSTOM_MAX = 0x1C

SCAN_CONVERSION_GET_COMMAND = 0x53
SCAN_CONVERSION_SET_COMMAND = 0x52
SCAN_CONVERSION_NAMES = {
    0x00: "progressive",
    0x01: "interlace",
}
SCAN_CONVERSION_ALIASES = {
    **{name: value for value, name in SCAN_CONVERSION_NAMES.items()},
    "interlaced": 0x01,
}

PIXEL_SHIFT_GET_COMMAND = 0xB1
PIXEL_SHIFT_SET_COMMAND = 0xB2
PIXEL_SHIFT_OFF = 0x00
PIXEL_SHIFT_AUTO = 0x5B
PIXEL_SHIFT_SECONDS_MIN = 10
PIXEL_SHIFT_SECONDS_MAX = 900
PIXEL_SHIFT_SECONDS_STEP = 10

MEMC_EFFECT_GET_COMMAND = 0x29
MEMC_EFFECT_SET_COMMAND = 0x28
MEMC_EFFECT_NAMES = {
    0x00: "off",
    0x01: "low",
    0x02: "medium",
    0x03: "high",
}
MEMC_EFFECT_ALIASES = {
    **{name: value for value, name in MEMC_EFFECT_NAMES.items()},
    "med": 0x02,
    "smoothing-off": 0x00,
    "smoothing-low": 0x01,
    "smoothing-medium": 0x02,
    "smoothing-high": 0x03,
}

INFORMATION_OSD_GET_COMMAND = 0x2D
INFORMATION_OSD_SET_COMMAND = 0x2C

HUMAN_SENSOR_GET_COMMAND = 0xB3
HUMAN_SENSOR_SET_COMMAND = 0xB4
HUMAN_SENSOR_NAMES = {
    0x00: "off",
    0x01: "10-mins",
    0x02: "20-mins",
    0x03: "30-mins",
    0x04: "40-mins",
    0x05: "50-mins",
    0x06: "60-mins",
    0xFF: "unavailable",
}
HUMAN_SENSOR_SET_NAMES = {
    value: name for value, name in HUMAN_SENSOR_NAMES.items() if value != 0xFF
}
HUMAN_SENSOR_ALIASES = {
    **{name: value for value, name in HUMAN_SENSOR_NAMES.items()},
    "10-min": 0x01,
    "10": 0x01,
    "20-min": 0x02,
    "20": 0x02,
    "30-min": 0x03,
    "30": 0x03,
    "40-min": 0x04,
    "40": 0x04,
    "50-min": 0x05,
    "50": 0x05,
    "60-min": 0x06,
    "60": 0x06,
    "hw-unavailable": 0xFF,
    "hardware-unavailable": 0xFF,
}

FACTORY_RESET_COMMAND = 0x56

POWER_ON_LOGO_GET_COMMAND = 0x3F
POWER_ON_LOGO_SET_COMMAND = 0x3E
POWER_ON_LOGO_NAMES = {
    0x00: "off",
    0x01: "on",
    0x02: "user",
}
POWER_ON_LOGO_ALIASES = {
    **{name: value for value, name in POWER_ON_LOGO_NAMES.items()},
}

OFF_TIMER_GET_COMMAND = 0x91
OFF_TIMER_SET_COMMAND = 0x92

ECO_MODE_GET_COMMAND = 0x63
ECO_MODE_SET_COMMAND = 0x64
ECO_MODE_NAMES = {
    0x00: "low-power-standby",
    0x01: "normal",
}
ECO_MODE_ALIASES = {
    **{name: value for value, name in ECO_MODE_NAMES.items()},
    "low-power": 0x00,
    "low": 0x00,
    "standby": 0x00,
}

PICTURE_STYLE_GET_COMMAND = 0x65
PICTURE_STYLE_SET_COMMAND = 0x66
PICTURE_STYLE_NAMES = {
    0x00: "highbright",
    0x01: "srgb",
    0x02: "vivid",
    0x03: "natural",
    0x04: "standard",
    0x05: "video",
    0x06: "static-signage",
    0x07: "text",
    0x08: "energy-saving",
    0x09: "soft",
    0x0A: "user",
}
PICTURE_STYLE_ALIASES = {
    **{name: value for value, name in PICTURE_STYLE_NAMES.items()},
    "high-bright": 0x00,
    "s-rgb": 0x01,
    "static": 0x06,
    "signage": 0x06,
    "energysaving": 0x08,
    "energy": 0x08,
}

GROUP_ID_GET_COMMAND = 0x5D
GROUP_ID_SET_COMMAND = 0x5C
GROUP_ID_OFF = 0xFF

MONITOR_ID_SET_COMMAND = 0x69

PORTS_LOCK_GET_COMMAND = 0xF2
PORTS_LOCK_SET_COMMAND = 0xF1
PORTS_LOCK_NAMES = {
    0x00: "unlocked",
    0x01: "locked",
}
PORTS_LOCK_ALIASES = {
    **{name: value for value, name in PORTS_LOCK_NAMES.items()},
    "unlock": 0x00,
    "unlocked": 0x00,
    "enable": 0x00,
    "enabled": 0x00,
    "lock": 0x01,
    "locked": 0x01,
    "disable": 0x01,
    "disabled": 0x01,
}

SCHEDULING_GET_COMMAND = 0x5B
SCHEDULING_SET_COMMAND = 0x5A
SCHEDULING_NULL_HOUR = 24
SCHEDULING_NULL_MINUTE = 60
SCHEDULING_DAY_BITS = {
    "every-week": 0x01,
    "monday": 0x02,
    "tuesday": 0x04,
    "wednesday": 0x08,
    "thursday": 0x10,
    "friday": 0x20,
    "saturday": 0x40,
    "sunday": 0x80,
}
SCHEDULING_DAY_ALIASES = {
    "weekly": 0x01,
    "mon": 0x02,
    "tue": 0x04,
    "tues": 0x04,
    "wed": 0x08,
    "thu": 0x10,
    "thur": 0x10,
    "thurs": 0x10,
    "fri": 0x20,
    "sat": 0x40,
    "sun": 0x80,
    "weekdays": 0x3F,
    "weekends": 0xC1,
    "all": 0xFF,
    "every-day": 0xFF,
    "daily": 0xFF,
}


class SicpError(RuntimeError):
    """Base exception for SICP client failures."""


class SicpProtocolError(SicpError):
    """Raised when a response is valid bytes but unexpected protocol data."""


class SicpAckError(SicpProtocolError):
    """Raised for invalid communication-control responses."""


class SicpNackError(SicpAckError):
    """Raised when the display returns NACK."""


class SicpNavError(SicpAckError):
    """Raised when the display returns NAV."""


def power_value_to_bool(value: int) -> bool:
    if value == POWER_OFF:
        return False
    if value == POWER_ON:
        return True
    raise SicpProtocolError(f"Unknown power-state value: 0x{value:02X}")


def bool_to_power_value(on: bool) -> int:
    return POWER_ON if on else POWER_OFF


def power_cold_start_value_to_name(value: int) -> str:
    if value == POWER_COLD_START_OFF:
        return "off"
    if value == POWER_COLD_START_ON:
        return "on"
    if value == POWER_COLD_START_LAST:
        return "last"
    raise SicpProtocolError(f"Unknown cold-start power-state value: 0x{value:02X}")


def power_cold_start_name_to_value(name: str) -> int:
    if name == "off":
        return POWER_COLD_START_OFF
    if name == "on":
        return POWER_COLD_START_ON
    if name == "last":
        return POWER_COLD_START_LAST
    raise ValueError("cold-start power state must be off, on, or last")


def decode_power_report(packet: SicpPacket) -> bool:
    if packet.command != POWER_GET_COMMAND:
        command = "None" if packet.command is None else f"0x{packet.command:02X}"
        raise SicpProtocolError(f"Expected power report 0x19, got {command}")
    if len(packet.parameters) != 1:
        raise SicpProtocolError("Malformed power-state report")
    return power_value_to_bool(packet.parameters[0])


def decode_power_cold_start_report(packet: SicpPacket) -> str:
    if packet.command != POWER_COLD_START_GET_COMMAND:
        command = "None" if packet.command is None else f"0x{packet.command:02X}"
        raise SicpProtocolError(f"Expected cold-start power report 0xA4, got {command}")
    if len(packet.parameters) != 1:
        raise SicpProtocolError("Malformed cold-start power-state report")
    return power_cold_start_value_to_name(packet.parameters[0])


def decode_operating_hours_report(packet: SicpPacket) -> int:
    if packet.command != OPERATING_HOURS_COMMAND:
        command = "None" if packet.command is None else f"0x{packet.command:02X}"
        raise SicpProtocolError(f"Expected operating-hours report 0x0F, got {command}")
    if len(packet.parameters) != 2:
        raise SicpProtocolError("Malformed operating-hours report")
    return (packet.parameters[0] << 8) | packet.parameters[1]


def decode_input_source_report(packet: SicpPacket) -> InputSourceState:
    if packet.command != INPUT_SOURCE_GET_COMMAND:
        command = "None" if packet.command is None else f"0x{packet.command:02X}"
        raise SicpProtocolError(f"Expected input-source report 0xAD, got {command}")
    if len(packet.parameters) != 4:
        raise SicpProtocolError("Malformed input-source report")
    return InputSourceState(
        source=packet.parameters[0],
        playlist=packet.parameters[1],
        osd_style=packet.parameters[2],
        mute_style=packet.parameters[3],
    )


def decode_scheduling_report(packet: SicpPacket) -> SchedulingState:
    if packet.command != SCHEDULING_GET_COMMAND:
        command = "None" if packet.command is None else f"0x{packet.command:02X}"
        raise SicpProtocolError(f"Expected scheduling report 0x5B, got {command}")
    if len(packet.parameters) not in (7, 8):
        raise SicpProtocolError("Malformed scheduling report")
    enabled, start_hour, start_minute, end_hour, end_minute, source, days = (
        packet.parameters[:7]
    )
    if enabled not in (0x00, 0x01):
        raise SicpProtocolError(f"Unknown scheduling enabled value: 0x{enabled:02X}")
    try:
        validate_scheduling_time(start_hour, start_minute)
        validate_scheduling_time(end_hour, end_minute)
        validate_byte(source, "scheduling source")
        validate_byte(days, "scheduling days")
        tag = (
            validate_scheduling_tag(packet.parameters[7], allow_none_value=True)
            if len(packet.parameters) == 8
            else None
        )
    except (TypeError, ValueError) as exc:
        raise SicpProtocolError(str(exc)) from exc
    return SchedulingState(
        enabled=bool(enabled),
        start_hour=start_hour,
        start_minute=start_minute,
        end_hour=end_hour,
        end_minute=end_minute,
        source=source,
        days=days,
        tag=tag,
    )


def decode_auto_signal_report(packet: SicpPacket) -> str:
    if packet.command != AUTO_SIGNAL_GET_COMMAND:
        command = "None" if packet.command is None else f"0x{packet.command:02X}"
        raise SicpProtocolError(f"Expected auto-signal report 0xAF, got {command}")
    if len(packet.parameters) != 1:
        raise SicpProtocolError("Malformed auto-signal report")
    return auto_signal_value_to_name(packet.parameters[0])


def decode_failover_report(packet: SicpPacket) -> FailoverState:
    if packet.command != FAILOVER_GET_COMMAND:
        command = "None" if packet.command is None else f"0x{packet.command:02X}"
        raise SicpProtocolError(f"Expected failover report 0xA6, got {command}")
    if len(packet.parameters) < 1:
        raise SicpProtocolError("Malformed failover report")
    return FailoverState(priorities=tuple(packet.parameters))


def decode_temperature_report(packet: SicpPacket) -> TemperatureState:
    if packet.command != TEMPERATURE_GET_COMMAND:
        command = "None" if packet.command is None else f"0x{packet.command:02X}"
        raise SicpProtocolError(f"Expected temperature report 0x2F, got {command}")
    if len(packet.parameters) not in (1, 2):
        raise SicpProtocolError("Malformed temperature report")
    for value in packet.parameters:
        if value > 100:
            raise SicpProtocolError(f"Invalid temperature value: {value}")
    return TemperatureState(sensors_celsius=tuple(packet.parameters))


def decode_tiling_report(packet: SicpPacket) -> TilingState:
    if packet.command != TILING_GET_COMMAND:
        command = "None" if packet.command is None else f"0x{packet.command:02X}"
        raise SicpProtocolError(f"Expected tiling report 0x23, got {command}")
    if len(packet.parameters) != 4:
        raise SicpProtocolError("Malformed tiling report")
    try:
        enabled = validate_tiling_enable(packet.parameters[0]) == 0x01
        frame_compensation = (
            validate_tiling_frame_comp(packet.parameters[1], allow_keep=False) == 0x01
        )
        position = validate_tiling_position(
            packet.parameters[2],
            allow_keep=False,
            zero_bezel=True,
        )
        wall_size = validate_tiling_wall_size(
            packet.parameters[3],
            allow_keep=True,
            zero_bezel=True,
        )
    except ValueError as exc:
        raise SicpProtocolError(str(exc)) from exc
    return TilingState(
        enabled=enabled,
        frame_compensation=frame_compensation,
        position=position,
        wall_size=wall_size,
    )


def decode_switch_on_delay_report(packet: SicpPacket) -> int:
    if packet.command != SWITCH_ON_DELAY_GET_COMMAND:
        command = "None" if packet.command is None else f"0x{packet.command:02X}"
        raise SicpProtocolError(f"Expected switch-on-delay report 0x55, got {command}")
    if len(packet.parameters) != 1:
        raise SicpProtocolError("Malformed switch-on-delay report")
    return packet.parameters[0]


def decode_frame_compensation_horizontal_report(packet: SicpPacket) -> int:
    if packet.command != FRAME_COMPENSATION_HORIZONTAL_GET_COMMAND:
        command = "None" if packet.command is None else f"0x{packet.command:02X}"
        raise SicpProtocolError(
            f"Expected horizontal frame-compensation report 0x5E, got {command}"
        )
    if len(packet.parameters) != 1:
        raise SicpProtocolError("Malformed horizontal frame-compensation report")
    return packet.parameters[0]


def decode_frame_compensation_vertical_report(packet: SicpPacket) -> int:
    if packet.command != FRAME_COMPENSATION_VERTICAL_GET_COMMAND:
        command = "None" if packet.command is None else f"0x{packet.command:02X}"
        raise SicpProtocolError(
            f"Expected vertical frame-compensation report 0x67, got {command}"
        )
    if len(packet.parameters) != 1:
        raise SicpProtocolError("Malformed vertical frame-compensation report")
    return packet.parameters[0]


def decode_anytile_report(packet: SicpPacket) -> AnyTileState:
    if packet.command != ANYTILE_GET_COMMAND:
        command = "None" if packet.command is None else f"0x{packet.command:02X}"
        raise SicpProtocolError(f"Expected AnyTile report 0x4A, got {command}")
    if len(packet.parameters) != 11:
        raise SicpProtocolError("Malformed AnyTile report")
    try:
        enabled = validate_tiling_enable(packet.parameters[0]) == 0x01
    except ValueError as exc:
        raise SicpProtocolError(str(exc)) from exc
    return AnyTileState(
        enabled=enabled,
        rotation=uint16_from_lsb_msb(packet.parameters[1], packet.parameters[2]),
        input_h_start=uint16_from_lsb_msb(packet.parameters[3], packet.parameters[4]),
        input_v_start=uint16_from_lsb_msb(packet.parameters[5], packet.parameters[6]),
        input_h_size=uint16_from_lsb_msb(packet.parameters[7], packet.parameters[8]),
        input_v_size=uint16_from_lsb_msb(packet.parameters[9], packet.parameters[10]),
    )


def decode_anytile_resolution_report(packet: SicpPacket) -> str:
    if packet.command != ANYTILE_RESOLUTION_GET_COMMAND:
        command = "None" if packet.command is None else f"0x{packet.command:02X}"
        raise SicpProtocolError(
            f"Expected AnyTile resolution report 0x4E, got {command}"
        )
    if len(packet.parameters) != 1:
        raise SicpProtocolError("Malformed AnyTile resolution report")
    return anytile_resolution_value_to_name(packet.parameters[0])


def decode_fan_speed_report(packet: SicpPacket) -> str:
    if packet.command != FAN_SPEED_GET_COMMAND:
        command = "None" if packet.command is None else f"0x{packet.command:02X}"
        raise SicpProtocolError(f"Expected fan-speed report 0x62, got {command}")
    if len(packet.parameters) != 1:
        raise SicpProtocolError("Malformed fan-speed report")
    return fan_speed_value_to_name(packet.parameters[0])


def decode_video_signal_present_report(packet: SicpPacket) -> bool:
    if packet.command != VIDEO_SIGNAL_PRESENT_COMMAND:
        command = "None" if packet.command is None else f"0x{packet.command:02X}"
        raise SicpProtocolError(f"Expected video-signal report 0x59, got {command}")
    if len(packet.parameters) != 1:
        raise SicpProtocolError("Malformed video-signal report")
    if packet.parameters[0] == 0x00:
        return False
    if packet.parameters[0] == 0x01:
        return True
    raise SicpProtocolError(
        f"Unknown video-signal status value: 0x{packet.parameters[0]:02X}"
    )


def decode_ir_lock_report(packet: SicpPacket) -> str:
    if packet.command != IR_LOCK_GET_COMMAND:
        command = "None" if packet.command is None else f"0x{packet.command:02X}"
        raise SicpProtocolError(f"Expected IR lock report 0x1D, got {command}")
    if len(packet.parameters) != 1:
        raise SicpProtocolError("Malformed IR lock report")
    return lock_state_value_to_name(packet.parameters[0], target="ir")


def decode_keypad_lock_report(packet: SicpPacket) -> str:
    if packet.command != KEYPAD_LOCK_GET_COMMAND:
        command = "None" if packet.command is None else f"0x{packet.command:02X}"
        raise SicpProtocolError(f"Expected keypad lock report 0x1B, got {command}")
    if len(packet.parameters) != 1:
        raise SicpProtocolError("Malformed keypad lock report")
    return lock_state_value_to_name(packet.parameters[0], target="keypad")


def decode_power_saving_mode_report(packet: SicpPacket) -> str:
    if packet.command != POWER_SAVING_MODE_GET_COMMAND:
        command = "None" if packet.command is None else f"0x{packet.command:02X}"
        raise SicpProtocolError(
            f"Expected power-saving mode report 0xDE, got {command}"
        )
    if len(packet.parameters) != 1:
        raise SicpProtocolError("Malformed power-saving mode report")
    return power_saving_mode_value_to_name(packet.parameters[0])


def decode_power_saving_mode_status_report(packet: SicpPacket) -> str:
    if packet.command != POWER_SAVING_MODE_STATUS_GET_COMMAND:
        command = "None" if packet.command is None else f"0x{packet.command:02X}"
        raise SicpProtocolError(
            f"Expected power-saving mode status report 0xD3, got {command}"
        )
    if len(packet.parameters) != 1:
        raise SicpProtocolError("Malformed power-saving mode status report")
    return power_saving_mode_status_value_to_name(packet.parameters[0])


def decode_apm_status_report(packet: SicpPacket) -> str:
    if packet.command != APM_STATUS_GET_COMMAND:
        command = "None" if packet.command is None else f"0x{packet.command:02X}"
        raise SicpProtocolError(f"Expected APM status report 0xD1, got {command}")
    if len(packet.parameters) != 1:
        raise SicpProtocolError("Malformed APM status report")
    return apm_status_value_to_name(packet.parameters[0])


def decode_serial_code_report(packet: SicpPacket) -> str:
    if packet.command != SERIAL_CODE_GET_COMMAND:
        command = "None" if packet.command is None else f"0x{packet.command:02X}"
        raise SicpProtocolError(f"Expected serial-code report 0x15, got {command}")
    if len(packet.parameters) != 14:
        raise SicpProtocolError("Malformed serial-code report")
    try:
        return packet.parameters.decode("ascii")
    except UnicodeDecodeError as exc:
        raise SicpProtocolError("Serial-code report is not ASCII") from exc


def decode_light_sensor_report(packet: SicpPacket) -> str:
    if packet.command != LIGHT_SENSOR_GET_COMMAND:
        command = "None" if packet.command is None else f"0x{packet.command:02X}"
        raise SicpProtocolError(f"Expected light-sensor report 0x25, got {command}")
    if len(packet.parameters) != 1:
        raise SicpProtocolError("Malformed light-sensor report")
    return light_sensor_value_to_name(packet.parameters[0])


def decode_osd_rotating_report(packet: SicpPacket) -> str:
    if packet.command != OSD_ROTATING_GET_COMMAND:
        command = "None" if packet.command is None else f"0x{packet.command:02X}"
        raise SicpProtocolError(f"Expected OSD rotating report 0x27, got {command}")
    if len(packet.parameters) != 1:
        raise SicpProtocolError("Malformed OSD rotating report")
    return osd_rotating_value_to_name(packet.parameters[0])


def decode_display_orientation_report(packet: SicpPacket) -> DisplayOrientationState:
    if packet.command != DISPLAY_ORIENTATION_GET_COMMAND:
        command = "None" if packet.command is None else f"0x{packet.command:02X}"
        raise SicpProtocolError(
            f"Expected display-orientation report 0x16, got {command}"
        )
    if len(packet.parameters) != 7:
        raise SicpProtocolError("Malformed display-orientation report")
    try:
        display_orientation_auto_rotate_value_to_name(packet.parameters[0])
        display_orientation_osd_rotation_value_to_name(packet.parameters[1])
        display_orientation_image_all_value_to_name(packet.parameters[2])
        for index, value in enumerate(packet.parameters[3:], start=1):
            display_orientation_window_value_to_name(value, label=f"window{index}")
    except SicpProtocolError:
        raise
    return DisplayOrientationState(
        auto_rotate=packet.parameters[0],
        osd_rotation=packet.parameters[1],
        image_all=packet.parameters[2],
        window1=packet.parameters[3],
        window2=packet.parameters[4],
        window3=packet.parameters[5],
        window4=packet.parameters[6],
    )


def decode_touch_feature_report(packet: SicpPacket) -> str:
    if packet.command != TOUCH_FEATURE_GET_COMMAND:
        command = "None" if packet.command is None else f"0x{packet.command:02X}"
        raise SicpProtocolError(f"Expected touch-feature report 0x1F, got {command}")
    if len(packet.parameters) != 1:
        raise SicpProtocolError("Malformed touch-feature report")
    return touch_feature_value_to_name(packet.parameters[0])


def decode_noise_reduction_report(packet: SicpPacket) -> str:
    if packet.command != NOISE_REDUCTION_GET_COMMAND:
        command = "None" if packet.command is None else f"0x{packet.command:02X}"
        raise SicpProtocolError(f"Expected noise-reduction report 0x2B, got {command}")
    if len(packet.parameters) != 1:
        raise SicpProtocolError("Malformed noise-reduction report")
    return noise_reduction_value_to_name(packet.parameters[0])


def decode_scan_mode_report(packet: SicpPacket) -> str:
    if packet.command != SCAN_MODE_GET_COMMAND:
        command = "None" if packet.command is None else f"0x{packet.command:02X}"
        raise SicpProtocolError(f"Expected scan-mode report 0x51, got {command}")
    if len(packet.parameters) != 1:
        raise SicpProtocolError("Malformed scan-mode report")
    return scan_mode_value_to_name(packet.parameters[0])


def decode_scan_conversion_report(packet: SicpPacket) -> str:
    if packet.command != SCAN_CONVERSION_GET_COMMAND:
        command = "None" if packet.command is None else f"0x{packet.command:02X}"
        raise SicpProtocolError(f"Expected scan-conversion report 0x53, got {command}")
    if len(packet.parameters) != 1:
        raise SicpProtocolError("Malformed scan-conversion report")
    return scan_conversion_value_to_name(packet.parameters[0])


def decode_pixel_shift_report(packet: SicpPacket) -> str:
    if packet.command != PIXEL_SHIFT_GET_COMMAND:
        command = "None" if packet.command is None else f"0x{packet.command:02X}"
        raise SicpProtocolError(f"Expected pixel-shift report 0xB1, got {command}")
    if len(packet.parameters) != 1:
        raise SicpProtocolError("Malformed pixel-shift report")
    return pixel_shift_value_to_name(packet.parameters[0])


def decode_memc_effect_report(packet: SicpPacket) -> str:
    if packet.command != MEMC_EFFECT_GET_COMMAND:
        command = "None" if packet.command is None else f"0x{packet.command:02X}"
        raise SicpProtocolError(f"Expected MEMC effect report 0x29, got {command}")
    if len(packet.parameters) != 1:
        raise SicpProtocolError("Malformed MEMC effect report")
    return memc_effect_value_to_name(packet.parameters[0])


def decode_information_osd_report(packet: SicpPacket) -> int:
    if packet.command != INFORMATION_OSD_GET_COMMAND:
        command = "None" if packet.command is None else f"0x{packet.command:02X}"
        raise SicpProtocolError(f"Expected information OSD report 0x2D, got {command}")
    if len(packet.parameters) != 1:
        raise SicpProtocolError("Malformed information OSD report")
    try:
        return validate_information_osd_value(packet.parameters[0])
    except ValueError as exc:
        raise SicpProtocolError(str(exc)) from exc


def decode_human_sensor_report(packet: SicpPacket) -> str:
    if packet.command != HUMAN_SENSOR_GET_COMMAND:
        command = "None" if packet.command is None else f"0x{packet.command:02X}"
        raise SicpProtocolError(f"Expected human-sensor report 0xB3, got {command}")
    if len(packet.parameters) != 1:
        raise SicpProtocolError("Malformed human-sensor report")
    return human_sensor_value_to_name(packet.parameters[0])


def decode_power_on_logo_report(packet: SicpPacket) -> str:
    if packet.command != POWER_ON_LOGO_GET_COMMAND:
        command = "None" if packet.command is None else f"0x{packet.command:02X}"
        raise SicpProtocolError(f"Expected power-on-logo report 0x3F, got {command}")
    if len(packet.parameters) != 1:
        raise SicpProtocolError("Malformed power-on-logo report")
    return power_on_logo_value_to_name(packet.parameters[0])


def decode_off_timer_report(packet: SicpPacket) -> int:
    if packet.command != OFF_TIMER_GET_COMMAND:
        command = "None" if packet.command is None else f"0x{packet.command:02X}"
        raise SicpProtocolError(f"Expected off-timer report 0x91, got {command}")
    if len(packet.parameters) != 1:
        raise SicpProtocolError("Malformed off-timer report")
    return validate_off_timer_hours(packet.parameters[0])


def decode_eco_mode_report(packet: SicpPacket) -> str:
    if packet.command != ECO_MODE_GET_COMMAND:
        command = "None" if packet.command is None else f"0x{packet.command:02X}"
        raise SicpProtocolError(f"Expected ECO mode report 0x63, got {command}")
    if len(packet.parameters) != 1:
        raise SicpProtocolError("Malformed ECO mode report")
    return eco_mode_value_to_name(packet.parameters[0])


def decode_picture_style_report(packet: SicpPacket) -> str:
    if packet.command != PICTURE_STYLE_GET_COMMAND:
        command = "None" if packet.command is None else f"0x{packet.command:02X}"
        raise SicpProtocolError(f"Expected picture-style report 0x65, got {command}")
    if len(packet.parameters) != 1:
        raise SicpProtocolError("Malformed picture-style report")
    return picture_style_value_to_name(packet.parameters[0])


def decode_group_id_report(packet: SicpPacket) -> int | None:
    if packet.command != GROUP_ID_GET_COMMAND:
        command = "None" if packet.command is None else f"0x{packet.command:02X}"
        raise SicpProtocolError(f"Expected group-id report 0x5D, got {command}")
    if len(packet.parameters) != 1:
        raise SicpProtocolError("Malformed group-id report")
    return group_id_value_to_id(packet.parameters[0])


def decode_ports_lock_report(packet: SicpPacket) -> str:
    if packet.command != PORTS_LOCK_GET_COMMAND:
        command = "None" if packet.command is None else f"0x{packet.command:02X}"
        raise SicpProtocolError(f"Expected ports-lock report 0xF2, got {command}")
    if len(packet.parameters) != 1:
        raise SicpProtocolError("Malformed ports-lock report")
    return ports_lock_value_to_name(packet.parameters[0])


def decode_video_parameters_report(packet: SicpPacket) -> VideoParametersState:
    if packet.command != VIDEO_PARAMETERS_GET_COMMAND:
        command = "None" if packet.command is None else f"0x{packet.command:02X}"
        raise SicpProtocolError(f"Expected video parameters report 0x33, got {command}")
    if len(packet.parameters) != 7:
        raise SicpProtocolError("Malformed video parameters report")
    brightness, color, contrast, sharpness, tint, black_level, gamma = packet.parameters
    for name, value in (
        ("brightness", brightness),
        ("color", color),
        ("contrast", contrast),
        ("sharpness", sharpness),
        ("tint", tint),
        ("black level", black_level),
    ):
        if value > 100:
            raise SicpProtocolError(f"Invalid {name} value: {value}")
    gamma_value_to_name(gamma)
    return VideoParametersState(
        brightness=brightness,
        color=color,
        contrast=contrast,
        sharpness=sharpness,
        tint=tint,
        black_level=black_level,
        gamma=gamma,
    )


def decode_picture_format_report(packet: SicpPacket) -> str:
    if packet.command != PICTURE_FORMAT_GET_COMMAND:
        command = "None" if packet.command is None else f"0x{packet.command:02X}"
        raise SicpProtocolError(f"Expected picture-format report 0x3B, got {command}")
    if len(packet.parameters) != 1:
        raise SicpProtocolError("Malformed picture-format report")
    return picture_format_value_to_name(packet.parameters[0] & 0x0F)


def decode_volume_report(packet: SicpPacket) -> VolumeState:
    if packet.command != VOLUME_GET_COMMAND:
        command = "None" if packet.command is None else f"0x{packet.command:02X}"
        raise SicpProtocolError(f"Expected volume report 0x45, got {command}")
    if len(packet.parameters) not in (1, 2):
        raise SicpProtocolError("Malformed volume report")
    try:
        speaker = validate_volume_level(packet.parameters[0], "speaker volume")
        audio = (
            validate_volume_level(packet.parameters[1], "audio volume")
            if len(packet.parameters) == 2
            else None
        )
    except ValueError as exc:
        raise SicpProtocolError(str(exc)) from exc
    return VolumeState(speaker=speaker, audio=audio)


def decode_volume_limit_report(packet: SicpPacket, *, target: str) -> VolumeLimitState:
    expected = (
        VOLUME_LIMIT_SPEAKER_GET_COMMAND
        if target == "speaker"
        else VOLUME_LIMIT_AUDIO_GET_COMMAND
    )
    if packet.command != expected:
        command = "None" if packet.command is None else f"0x{packet.command:02X}"
        raise SicpProtocolError(
            f"Expected {target} volume-limit report 0x{expected:02X}, got {command}"
        )
    if len(packet.parameters) != 3:
        raise SicpProtocolError("Malformed volume-limit report")
    try:
        minimum, maximum, switch_on = validate_volume_limits(*packet.parameters)
    except ValueError as exc:
        raise SicpProtocolError(str(exc)) from exc
    return VolumeLimitState(minimum=minimum, maximum=maximum, switch_on=switch_on)


def decode_audio_parameters_report(packet: SicpPacket) -> AudioParametersState:
    if packet.command != AUDIO_PARAMETERS_GET_COMMAND:
        command = "None" if packet.command is None else f"0x{packet.command:02X}"
        raise SicpProtocolError(f"Expected audio-parameters report 0x43, got {command}")
    if len(packet.parameters) != 2:
        raise SicpProtocolError("Malformed audio-parameters report")
    try:
        audio_parameter_value_to_display(packet.parameters[0])
        audio_parameter_value_to_display(packet.parameters[1])
    except SicpProtocolError:
        raise
    return AudioParametersState(treble=packet.parameters[0], bass=packet.parameters[1])


def decode_volume_mute_report(packet: SicpPacket) -> bool:
    if packet.command != VOLUME_MUTE_GET_COMMAND:
        command = "None" if packet.command is None else f"0x{packet.command:02X}"
        raise SicpProtocolError(f"Expected volume-mute report 0x46, got {command}")
    if len(packet.parameters) != 1:
        raise SicpProtocolError("Malformed volume-mute report")
    return mute_value_to_bool(packet.parameters[0])


def decode_color_temperature_report(packet: SicpPacket) -> str:
    if packet.command != COLOR_TEMPERATURE_GET_COMMAND:
        command = "None" if packet.command is None else f"0x{packet.command:02X}"
        raise SicpProtocolError(
            f"Expected color-temperature report 0x35, got {command}"
        )
    if len(packet.parameters) != 1:
        raise SicpProtocolError("Malformed color-temperature report")
    return color_temperature_value_to_name(packet.parameters[0])


def decode_rgb_parameters_report(packet: SicpPacket) -> RgbParametersState:
    if packet.command != RGB_PARAMETERS_GET_COMMAND:
        command = "None" if packet.command is None else f"0x{packet.command:02X}"
        raise SicpProtocolError(f"Expected RGB parameters report 0x37, got {command}")
    if len(packet.parameters) != 6:
        raise SicpProtocolError("Malformed RGB parameters report")
    return RgbParametersState(
        red_gain=packet.parameters[0],
        green_gain=packet.parameters[1],
        blue_gain=packet.parameters[2],
        red_offset=packet.parameters[3],
        green_offset=packet.parameters[4],
        blue_offset=packet.parameters[5],
    )


def decode_color_temperature_100k_report(
    packet: SicpPacket,
) -> ColorTemperature100KState:
    if packet.command != COLOR_TEMPERATURE_100K_GET_COMMAND:
        command = "None" if packet.command is None else f"0x{packet.command:02X}"
        raise SicpProtocolError(
            f"Expected color-temperature-100k report 0x12, got {command}"
        )
    if len(packet.parameters) != 1:
        raise SicpProtocolError("Malformed color-temperature-100k report")
    try:
        steps = validate_color_temperature_100k_steps(packet.parameters[0])
    except ValueError as exc:
        raise SicpProtocolError(str(exc)) from exc
    return ColorTemperature100KState(steps=steps)


def require_ack(packet: SicpPacket) -> None:
    if packet.command != 0x00:
        command = "None" if packet.command is None else f"0x{packet.command:02X}"
        raise SicpAckError(
            f"Expected communication-control response, got command {command}"
        )
    if len(packet.parameters) != 1:
        raise SicpAckError("Malformed communication-control response")

    status = packet.parameters[0]
    if status == 0x06:
        return
    if status == 0x15:
        raise SicpNackError("Display returned NACK")
    if status == 0x18:
        raise SicpNavError("Display returned NAV")
    raise SicpAckError(f"Unknown communication-control status: 0x{status:02X}")


@dataclass(frozen=True)
class SicpTransaction:
    request: bytes
    response: SicpPacket | None
    skipped: tuple[SicpPacket, ...] = ()


@dataclass(frozen=True)
class _ReceiveResult:
    packet: SicpPacket
    skipped: tuple[SicpPacket, ...]


@dataclass(frozen=True)
class InputSourceState:
    source: int
    playlist: int
    osd_style: int
    mute_style: int

    @property
    def source_name(self) -> str:
        return input_source_value_to_name(self.source)

    @property
    def do_not_switch(self) -> bool:
        return bool(self.osd_style & 0x40)

    @property
    def display_style(self) -> str:
        value = self.osd_style & 0x07
        if value == INPUT_SOURCE_DISPLAY_STYLE_SOURCE_LABEL:
            return "source-label"
        if value == INPUT_SOURCE_DISPLAY_STYLE_RESERVED:
            return "reserved"
        return f"unknown-0x{value:02X}"

    def to_dict(self) -> dict[str, object]:
        return {
            "source": self.source,
            "source_name": self.source_name,
            "playlist": self.playlist,
            "osd_style": self.osd_style,
            "do_not_switch": self.do_not_switch,
            "display_style": self.display_style,
            "mute_style": self.mute_style,
        }


@dataclass(frozen=True)
class FailoverState:
    priorities: tuple[int, ...]

    @property
    def priority_names(self) -> tuple[str, ...]:
        return tuple(failover_source_value_to_name(value) for value in self.priorities)

    def to_dict(self) -> dict[str, object]:
        return {
            "priorities": list(self.priorities),
            "priority_names": list(self.priority_names),
        }


@dataclass(frozen=True)
class TemperatureState:
    sensors_celsius: tuple[int, ...]

    @property
    def highest_celsius(self) -> int:
        return max(self.sensors_celsius)

    def to_dict(self) -> dict[str, object]:
        return {
            "sensors_celsius": list(self.sensors_celsius),
            "highest_celsius": self.highest_celsius,
        }


@dataclass(frozen=True)
class TilingState:
    enabled: bool
    frame_compensation: bool
    position: int
    wall_size: int

    @property
    def standard_monitors(self) -> tuple[int, int] | None:
        return decode_tiling_wall_size(self.wall_size, max_h=TILING_STANDARD_MAX_H)

    @property
    def zero_bezel_monitors(self) -> tuple[int, int] | None:
        return decode_tiling_wall_size(self.wall_size, max_h=TILING_ZERO_BEZEL_MAX_H)

    def to_dict(self) -> dict[str, object]:
        standard = self.standard_monitors
        zero_bezel = self.zero_bezel_monitors
        return {
            "enabled": self.enabled,
            "frame_compensation": self.frame_compensation,
            "position": self.position,
            "wall_size": self.wall_size,
            "standard_h_monitors": None if standard is None else standard[0],
            "standard_v_monitors": None if standard is None else standard[1],
            "zero_bezel_h_monitors": None if zero_bezel is None else zero_bezel[0],
            "zero_bezel_v_monitors": None if zero_bezel is None else zero_bezel[1],
        }


@dataclass(frozen=True)
class AnyTileState:
    enabled: bool
    rotation: int
    input_h_start: int
    input_v_start: int
    input_h_size: int
    input_v_size: int

    def to_dict(self) -> dict[str, object]:
        return {
            "enabled": self.enabled,
            "rotation": self.rotation,
            "input_h_start": self.input_h_start,
            "input_v_start": self.input_v_start,
            "input_h_size": self.input_h_size,
            "input_v_size": self.input_v_size,
        }


@dataclass(frozen=True)
class VideoParametersState:
    brightness: int
    color: int
    contrast: int
    sharpness: int
    tint: int
    black_level: int
    gamma: int

    @property
    def gamma_name(self) -> str:
        return gamma_value_to_name(self.gamma)

    def to_dict(self) -> dict[str, object]:
        return {
            "brightness": self.brightness,
            "color": self.color,
            "contrast": self.contrast,
            "sharpness": self.sharpness,
            "tint": self.tint,
            "black_level": self.black_level,
            "gamma": self.gamma,
            "gamma_name": self.gamma_name,
        }


@dataclass(frozen=True)
class VolumeState:
    speaker: int
    audio: int | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "speaker": self.speaker,
            "audio": self.audio,
        }


@dataclass(frozen=True)
class VolumeLimitState:
    minimum: int
    maximum: int
    switch_on: int

    def to_dict(self) -> dict[str, object]:
        return {
            "minimum": self.minimum,
            "maximum": self.maximum,
            "switch_on": self.switch_on,
        }


@dataclass(frozen=True)
class DisplayOrientationState:
    auto_rotate: int
    osd_rotation: int
    image_all: int
    window1: int
    window2: int
    window3: int
    window4: int

    @property
    def auto_rotate_name(self) -> str:
        return display_orientation_auto_rotate_value_to_name(self.auto_rotate)

    @property
    def osd_rotation_name(self) -> str:
        return display_orientation_osd_rotation_value_to_name(self.osd_rotation)

    @property
    def image_all_name(self) -> str:
        return display_orientation_image_all_value_to_name(self.image_all)

    @property
    def window1_name(self) -> str:
        return display_orientation_window_value_to_name(self.window1)

    @property
    def window2_name(self) -> str:
        return display_orientation_window_value_to_name(self.window2)

    @property
    def window3_name(self) -> str:
        return display_orientation_window_value_to_name(self.window3)

    @property
    def window4_name(self) -> str:
        return display_orientation_window_value_to_name(self.window4)

    def to_dict(self) -> dict[str, object]:
        return {
            "auto_rotate": self.auto_rotate,
            "auto_rotate_name": self.auto_rotate_name,
            "osd_rotation": self.osd_rotation,
            "osd_rotation_name": self.osd_rotation_name,
            "image_all": self.image_all,
            "image_all_name": self.image_all_name,
            "window1": self.window1,
            "window1_name": self.window1_name,
            "window2": self.window2,
            "window2_name": self.window2_name,
            "window3": self.window3,
            "window3_name": self.window3_name,
            "window4": self.window4,
            "window4_name": self.window4_name,
        }


@dataclass(frozen=True)
class AudioParametersState:
    treble: int
    bass: int

    @property
    def treble_display(self) -> int:
        return audio_parameter_value_to_display(self.treble)

    @property
    def bass_display(self) -> int:
        return audio_parameter_value_to_display(self.bass)

    def to_dict(self) -> dict[str, object]:
        return {
            "treble": self.treble,
            "treble_display": self.treble_display,
            "bass": self.bass,
            "bass_display": self.bass_display,
        }


@dataclass(frozen=True)
class RgbParametersState:
    red_gain: int
    green_gain: int
    blue_gain: int
    red_offset: int
    green_offset: int
    blue_offset: int

    def to_dict(self) -> dict[str, object]:
        return {
            "red_gain": self.red_gain,
            "green_gain": self.green_gain,
            "blue_gain": self.blue_gain,
            "red_offset": self.red_offset,
            "green_offset": self.green_offset,
            "blue_offset": self.blue_offset,
        }


@dataclass(frozen=True)
class ColorTemperature100KState:
    steps: int

    @property
    def kelvin(self) -> int:
        return self.steps * 100

    def to_dict(self) -> dict[str, object]:
        return {
            "steps": self.steps,
            "kelvin": self.kelvin,
        }


@dataclass(frozen=True)
class SchedulingState:
    enabled: bool
    start_hour: int
    start_minute: int
    end_hour: int
    end_minute: int
    source: int
    days: int
    tag: int | None = None

    @property
    def start_time(self) -> str | None:
        return scheduling_time_value_to_string(self.start_hour, self.start_minute)

    @property
    def end_time(self) -> str | None:
        return scheduling_time_value_to_string(self.end_hour, self.end_minute)

    @property
    def source_name(self) -> str:
        return scheduling_source_value_to_name(self.source)

    @property
    def day_names(self) -> tuple[str, ...]:
        return scheduling_days_value_to_names(self.days)

    @property
    def tag_name(self) -> str | None:
        if self.tag is None:
            return None
        return f"tag-{self.tag}"

    def to_dict(self) -> dict[str, object]:
        return {
            "enabled": self.enabled,
            "start_hour": self.start_hour,
            "start_minute": self.start_minute,
            "start_time": self.start_time,
            "end_hour": self.end_hour,
            "end_minute": self.end_minute,
            "end_time": self.end_time,
            "source": self.source,
            "source_name": self.source_name,
            "days": self.days,
            "day_names": list(self.day_names),
            "tag": self.tag,
            "tag_name": self.tag_name,
        }


def input_source_value_to_name(value: int) -> str:
    return INPUT_SOURCE_NAMES.get(value, f"unknown-0x{value:02X}")


def input_source_name_to_value(name: str) -> int:
    normalized = name.strip().lower().replace("_", "-").replace(" ", "-")
    if normalized.startswith("0x"):
        value = int(normalized, 16)
    elif normalized.isdigit():
        value = int(normalized, 10)
    elif normalized in INPUT_SOURCE_ALIASES:
        value = INPUT_SOURCE_ALIASES[normalized]
    else:
        raise ValueError(f"unknown input source: {name}")
    validate_byte(value, "input source")
    return value


def validate_scheduling_page(value: int) -> int:
    validate_byte(value, "scheduling page")
    if value < 1 or value > 7:
        raise ValueError("scheduling page must be in range 1..7")
    return value


def validate_scheduling_hour(value: int) -> int:
    validate_byte(value, "scheduling hour")
    if value > 24:
        raise ValueError("scheduling hour must be in range 0..24")
    return value


def validate_scheduling_minute(value: int) -> int:
    validate_byte(value, "scheduling minute")
    if value > 60:
        raise ValueError("scheduling minute must be in range 0..60")
    return value


def validate_scheduling_time(hour: int, minute: int) -> tuple[int, int]:
    hour = validate_scheduling_hour(hour)
    minute = validate_scheduling_minute(minute)
    if (hour, minute) == (SCHEDULING_NULL_HOUR, SCHEDULING_NULL_MINUTE):
        return hour, minute
    if hour == SCHEDULING_NULL_HOUR or minute == SCHEDULING_NULL_MINUTE:
        raise ValueError("scheduling time must be HH:MM or null")
    if hour > 23:
        raise ValueError("scheduling hour must be in range 0..23 or null")
    if minute > 59:
        raise ValueError("scheduling minute must be in range 0..59 or null")
    return hour, minute


def scheduling_time_value_to_string(hour: int, minute: int) -> str | None:
    validate_scheduling_time(hour, minute)
    if (hour, minute) == (SCHEDULING_NULL_HOUR, SCHEDULING_NULL_MINUTE):
        return None
    return f"{hour:02d}:{minute:02d}"


def parse_scheduling_time(value: str) -> tuple[int, int]:
    normalized = value.strip().lower()
    if normalized in ("null", "none", "disabled", "-"):
        return SCHEDULING_NULL_HOUR, SCHEDULING_NULL_MINUTE
    parts = normalized.split(":", 1)
    if len(parts) != 2:
        raise ValueError("scheduling time must be HH:MM or null")
    try:
        hour = int(parts[0], 10)
        minute = int(parts[1], 10)
    except ValueError as exc:
        raise ValueError("scheduling time must be HH:MM or null") from exc
    return validate_scheduling_time(hour, minute)


def scheduling_source_value_to_name(value: int) -> str:
    validate_byte(value, "scheduling source")
    if value == 0x00:
        return "null"
    return input_source_value_to_name(value)


def scheduling_source_name_to_value(name: str) -> int:
    normalized = name.strip().lower().replace("_", "-").replace(" ", "-")
    if normalized in ("null", "none", "off", "disabled"):
        return 0x00
    return input_source_name_to_value(name)


def scheduling_days_value_to_names(value: int) -> tuple[str, ...]:
    validate_byte(value, "scheduling days")
    if value == 0xFF:
        return ("every-day",)
    names = [name for name, bit in SCHEDULING_DAY_BITS.items() if value & bit]
    return tuple(names) if names else ("none",)


def scheduling_days_name_to_value(name: str) -> int:
    normalized = name.strip().lower().replace("_", "-").replace(" ", "-")
    if normalized.startswith("0x"):
        return validate_byte(int(normalized, 16), "scheduling days")
    if normalized.isdigit():
        return validate_byte(int(normalized, 10), "scheduling days")

    value = 0
    for part in normalized.replace(",", "+").split("+"):
        item = part.strip()
        if not item:
            continue
        if item in SCHEDULING_DAY_BITS:
            value |= SCHEDULING_DAY_BITS[item]
        elif item in SCHEDULING_DAY_ALIASES:
            value |= SCHEDULING_DAY_ALIASES[item]
        else:
            raise ValueError(f"unknown scheduling day: {part}")
    return validate_byte(value, "scheduling days")


def validate_scheduling_tag(
    value: int | None,
    *,
    allow_none_value: bool = False,
) -> int | None:
    if value is None:
        return None
    validate_byte(value, "scheduling tag")
    if allow_none_value and value == 0:
        return None
    if value < 1 or value > 7:
        raise ValueError("scheduling tag must be in range 1..7")
    return value


def bool_name_to_value(name: str, label: str) -> int:
    normalized = name.strip().lower().replace("_", "-").replace(" ", "-")
    if normalized in ("yes", "on", "true", "1", "enable", "enabled"):
        return 0x01
    if normalized in ("no", "off", "false", "0", "disable", "disabled"):
        return 0x00
    raise ValueError(f"unknown {label}: {name}")


def bool_value_to_name(value: int, label: str) -> str:
    if value == 0x00:
        return "no"
    if value == 0x01:
        return "yes"
    raise SicpProtocolError(f"Unknown {label} value: 0x{value:02X}")


def tiling_enable_name_to_value(name: str) -> int:
    return bool_name_to_value(name, "tiling enable")


def tiling_frame_comp_name_to_value(name: str) -> int:
    normalized = name.strip().lower().replace("_", "-").replace(" ", "-")
    if normalized in ("keep", "keep-previous", "previous", "unchanged"):
        return TILING_FRAME_COMP_KEEP
    return bool_name_to_value(name, "tiling frame compensation")


def tiling_position_name_to_value(name: str, *, zero_bezel: bool = False) -> int:
    normalized = name.strip().lower().replace("_", "-").replace(" ", "-")
    if normalized in ("keep", "keep-previous", "previous", "unchanged"):
        return TILING_KEEP
    value = int(normalized, 0)
    return validate_tiling_position(value, allow_keep=True, zero_bezel=zero_bezel)


def validate_tiling_enable(value: int) -> int:
    validate_byte(value, "tiling enable")
    if value not in (0x00, 0x01):
        raise ValueError("tiling enable must be yes or no")
    return value


def validate_tiling_frame_comp(value: int, *, allow_keep: bool) -> int:
    validate_byte(value, "tiling frame compensation")
    valid = (0x00, 0x01, TILING_FRAME_COMP_KEEP) if allow_keep else (0x00, 0x01)
    if value not in valid:
        raise ValueError("tiling frame compensation must be yes, no, or keep")
    return value


def validate_tiling_position(
    value: int,
    *,
    allow_keep: bool,
    zero_bezel: bool,
) -> int:
    validate_byte(value, "tiling position")
    if allow_keep and value == TILING_KEEP:
        return value
    maximum = (
        TILING_ZERO_BEZEL_MAX_POSITION if zero_bezel else TILING_STANDARD_MAX_POSITION
    )
    if value < 1 or value > maximum:
        raise ValueError(f"tiling position must be in range 1..{maximum}")
    return value


def encode_tiling_wall_size(
    h_monitors: int,
    v_monitors: int,
    *,
    zero_bezel: bool = False,
) -> int:
    max_h = TILING_ZERO_BEZEL_MAX_H if zero_bezel else TILING_STANDARD_MAX_H
    max_v = TILING_ZERO_BEZEL_MAX_V if zero_bezel else TILING_STANDARD_MAX_V
    if h_monitors < 1 or h_monitors > max_h:
        raise ValueError(f"tiling H monitors must be in range 1..{max_h}")
    if v_monitors < 1 or v_monitors > max_v:
        raise ValueError(f"tiling V monitors must be in range 1..{max_v}")
    return (v_monitors - 1) * max_h + h_monitors


def decode_tiling_wall_size(value: int, *, max_h: int) -> tuple[int, int] | None:
    validate_byte(value, "tiling wall size")
    if value == TILING_KEEP:
        return None
    h_monitors = value % max_h
    v_monitors = value // max_h + 1
    if h_monitors == 0:
        h_monitors = max_h
        v_monitors -= 1
    if v_monitors < 1:
        return None
    return h_monitors, v_monitors


def validate_tiling_wall_size(
    value: int,
    *,
    allow_keep: bool,
    zero_bezel: bool,
) -> int:
    validate_byte(value, "tiling wall size")
    if allow_keep and value == TILING_KEEP:
        return value
    max_h = TILING_ZERO_BEZEL_MAX_H if zero_bezel else TILING_STANDARD_MAX_H
    max_v = TILING_ZERO_BEZEL_MAX_V if zero_bezel else TILING_STANDARD_MAX_V
    decoded = decode_tiling_wall_size(value, max_h=max_h)
    if decoded is None:
        raise ValueError("tiling wall size must not be keep")
    h_monitors, v_monitors = decoded
    if h_monitors > max_h or v_monitors > max_v:
        raise ValueError(f"tiling wall size must encode H 1..{max_h} and V 1..{max_v}")
    return value


def build_tiling_set_values(
    enabled: int,
    frame_compensation: int = TILING_FRAME_COMP_KEEP,
    position: int = TILING_KEEP,
    wall_size: int = TILING_KEEP,
    *,
    zero_bezel: bool = False,
) -> tuple[int, int, int, int]:
    return (
        validate_tiling_enable(enabled),
        validate_tiling_frame_comp(frame_compensation, allow_keep=True),
        validate_tiling_position(position, allow_keep=True, zero_bezel=zero_bezel),
        validate_tiling_wall_size(wall_size, allow_keep=True, zero_bezel=zero_bezel),
    )


def switch_on_delay_value_to_name(value: int) -> str:
    validate_byte(value, "switch-on delay")
    if value == SWITCH_ON_DELAY_OFF:
        return "off"
    if value == SWITCH_ON_DELAY_AUTO:
        return "auto"
    return f"{value} seconds"


def switch_on_delay_name_to_value(name: str) -> int:
    normalized = name.strip().lower().replace("_", "-").replace(" ", "-")
    if normalized in ("off", "disabled", "disable"):
        return SWITCH_ON_DELAY_OFF
    if normalized in ("auto", "automatic"):
        return SWITCH_ON_DELAY_AUTO
    if normalized.startswith("0x"):
        value = int(normalized, 16)
    else:
        suffixes = (
            "-seconds",
            "-second",
            "-secs",
            "-sec",
            "seconds",
            "second",
            "secs",
            "sec",
            "s",
        )
        number = normalized
        for suffix in suffixes:
            if number.endswith(suffix):
                number = number[: -len(suffix)]
                break
        if not number.isdigit():
            raise ValueError(f"unknown switch-on-delay value: {name}")
        value = int(number, 10)
    return validate_byte(value, "switch-on delay")


def validate_uint16(value: int, name: str) -> int:
    if not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")
    if value < 0 or value > 0xFFFF:
        raise ValueError(f"{name} must be in range 0..65535")
    return value


def uint16_to_lsb_msb(value: int, name: str) -> tuple[int, int]:
    value = validate_uint16(value, name)
    return value & 0xFF, (value >> 8) & 0xFF


def uint16_from_lsb_msb(lsb: int, msb: int) -> int:
    validate_byte(lsb, "uint16 lsb")
    validate_byte(msb, "uint16 msb")
    return lsb | (msb << 8)


def build_anytile_parameters(
    enabled: int,
    rotation: int,
    input_h_start: int,
    input_v_start: int,
    input_h_size: int,
    input_v_size: int,
) -> tuple[int, ...]:
    enabled = validate_tiling_enable(enabled)
    rotation_lsb, rotation_msb = uint16_to_lsb_msb(rotation, "AnyTile rotation")
    h_start_lsb, h_start_msb = uint16_to_lsb_msb(input_h_start, "AnyTile H start")
    v_start_lsb, v_start_msb = uint16_to_lsb_msb(input_v_start, "AnyTile V start")
    h_size_lsb, h_size_msb = uint16_to_lsb_msb(input_h_size, "AnyTile H size")
    v_size_lsb, v_size_msb = uint16_to_lsb_msb(input_v_size, "AnyTile V size")
    return (
        enabled,
        rotation_lsb,
        rotation_msb,
        h_start_lsb,
        h_start_msb,
        v_start_lsb,
        v_start_msb,
        h_size_lsb,
        h_size_msb,
        v_size_lsb,
        v_size_msb,
    )


def anytile_resolution_value_to_name(value: int) -> str:
    if value not in ANYTILE_RESOLUTION_NAMES:
        raise SicpProtocolError(f"Unknown AnyTile resolution mode: 0x{value:02X}")
    return ANYTILE_RESOLUTION_NAMES[value]


def anytile_resolution_name_to_value(name: str) -> int:
    normalized = name.strip().lower().replace("_", "-").replace(" ", "-")
    if normalized.startswith("0x"):
        value = int(normalized, 16)
    elif normalized.isdigit():
        value = int(normalized, 10)
    elif normalized in ANYTILE_RESOLUTION_ALIASES:
        value = ANYTILE_RESOLUTION_ALIASES[normalized]
    else:
        raise ValueError(f"unknown AnyTile resolution mode: {name}")
    validate_byte(value, "AnyTile resolution mode")
    if value not in ANYTILE_RESOLUTION_NAMES:
        raise ValueError(f"unknown AnyTile resolution mode: 0x{value:02X}")
    return value


def auto_signal_value_to_name(value: int) -> str:
    return AUTO_SIGNAL_NAMES.get(value, f"unknown-0x{value:02X}")


def auto_signal_name_to_value(name: str) -> int:
    normalized = name.strip().lower().replace("_", "-").replace(" ", "-")
    if normalized.startswith("0x"):
        value = int(normalized, 16)
    elif normalized.isdigit():
        value = int(normalized, 10)
    elif normalized in AUTO_SIGNAL_ALIASES:
        value = AUTO_SIGNAL_ALIASES[normalized]
    else:
        raise ValueError(f"unknown auto-signal mode: {name}")
    validate_byte(value, "auto-signal mode")
    return value


def failover_source_value_to_name(value: int) -> str:
    return FAILOVER_SOURCE_NAMES.get(value, f"unknown-0x{value:02X}")


def failover_source_name_to_value(name: str) -> int:
    normalized = name.strip().lower().replace("_", "-").replace(" ", "-")
    if normalized.startswith("0x"):
        value = int(normalized, 16)
    elif normalized.isdigit():
        value = int(normalized, 10)
    elif normalized in FAILOVER_SOURCE_ALIASES:
        value = FAILOVER_SOURCE_ALIASES[normalized]
    else:
        raise ValueError(f"unknown failover source: {name}")
    validate_byte(value, "failover source")
    return value


def validate_failover_priorities(values: tuple[int, ...]) -> tuple[int, ...]:
    if not values:
        raise ValueError("at least one failover priority is required")
    if len(values) > 17:
        raise ValueError("failover priority list can contain at most 17 sources")
    for index, value in enumerate(values):
        validate_byte(value, f"failover priority {index + 1}")
    return values


def monitor_restart_target_name_to_value(name: str) -> int:
    normalized = name.strip().lower().replace("_", "-").replace(" ", "-")
    if normalized.startswith("0x"):
        value = int(normalized, 16)
    elif normalized.isdigit():
        value = int(normalized, 10)
    elif normalized in MONITOR_RESTART_ALIASES:
        value = MONITOR_RESTART_ALIASES[normalized]
    else:
        raise ValueError(f"unknown monitor restart target: {name}")
    validate_byte(value, "monitor restart target")
    return value


def monitor_restart_target_value_to_name(value: int) -> str:
    return MONITOR_RESTART_TARGETS.get(value, f"unknown-0x{value:02X}")


def fan_speed_value_to_name(value: int) -> str:
    if value not in FAN_SPEED_NAMES:
        raise SicpProtocolError(f"Unknown fan-speed value: 0x{value:02X}")
    return FAN_SPEED_NAMES[value]


def fan_speed_name_to_value(name: str) -> int:
    normalized = name.strip().lower().replace("_", "-").replace(" ", "-")
    if normalized.startswith("0x"):
        value = int(normalized, 16)
    elif normalized.isdigit():
        value = int(normalized, 10)
    elif normalized in FAN_SPEED_ALIASES:
        value = FAN_SPEED_ALIASES[normalized]
    else:
        raise ValueError(f"unknown fan speed: {name}")
    validate_byte(value, "fan speed")
    if value not in FAN_SPEED_NAMES:
        raise ValueError(f"unknown fan speed value: 0x{value:02X}")
    return value


def lock_state_value_to_name(value: int, *, target: str) -> str:
    valid_values = lock_state_values_for_target(target)
    if value not in valid_values:
        raise SicpProtocolError(f"Unknown {target} lock-state value: 0x{value:02X}")
    return LOCK_STATE_NAMES[value]


def lock_state_name_to_value(name: str, *, target: str) -> int:
    normalized = name.strip().lower().replace("_", "-").replace(" ", "-")
    if normalized.startswith("0x"):
        value = int(normalized, 16)
    elif normalized.isdigit():
        value = int(normalized, 10)
    elif normalized in LOCK_STATE_ALIASES:
        value = LOCK_STATE_ALIASES[normalized]
    else:
        raise ValueError(f"unknown {target} lock state: {name}")
    validate_byte(value, f"{target} lock state")
    if value not in lock_state_values_for_target(target):
        raise ValueError(f"unknown {target} lock-state value: 0x{value:02X}")
    return value


def lock_state_values_for_target(target: str) -> frozenset[int]:
    if target == "ir":
        return IR_LOCK_STATE_VALUES
    if target == "keypad":
        return KEYPAD_LOCK_STATE_VALUES
    raise ValueError("lock target must be ir or keypad")


def validate_percentage(value: int, name: str) -> int:
    validate_byte(value, name)
    if value > 100:
        raise ValueError(f"{name} must be in range 0..100")
    return value


def picture_format_value_to_name(value: int) -> str:
    low_nibble = value & 0x0F
    if low_nibble not in PICTURE_FORMAT_NAMES:
        raise SicpProtocolError(f"Unknown picture-format value: 0x{value:02X}")
    return PICTURE_FORMAT_NAMES[low_nibble]


def picture_format_name_to_value(name: str) -> int:
    normalized = name.strip().lower().replace("_", "-").replace(" ", "-")
    if normalized.startswith("0x"):
        value = int(normalized, 16)
    elif normalized.isdigit():
        value = int(normalized, 10)
    elif normalized in PICTURE_FORMAT_ALIASES:
        value = PICTURE_FORMAT_ALIASES[normalized]
    else:
        raise ValueError(f"unknown picture format: {name}")
    validate_byte(value, "picture format")
    if value > 0x0F or value not in PICTURE_FORMAT_NAMES:
        raise ValueError(f"unknown picture-format value: 0x{value:02X}")
    return value


def validate_volume_level(value: int, name: str = "volume") -> int:
    validate_byte(value, name)
    if value > 100:
        raise ValueError(f"{name} must be in range 0..100")
    return value


def validate_volume_limits(
    minimum: int,
    maximum: int,
    switch_on: int,
) -> tuple[int, int, int]:
    minimum = validate_volume_level(minimum, "minimum volume")
    maximum = validate_volume_level(maximum, "maximum volume")
    switch_on = validate_volume_level(switch_on, "switch-on volume")
    if not minimum <= switch_on <= maximum:
        raise ValueError("volume limits must satisfy minimum <= switch-on <= maximum")
    return minimum, maximum, switch_on


def volume_limit_get_command(target: str) -> int:
    if target == "speaker":
        return VOLUME_LIMIT_SPEAKER_GET_COMMAND
    if target == "audio":
        return VOLUME_LIMIT_AUDIO_GET_COMMAND
    raise ValueError("volume-limit target must be speaker or audio")


def volume_limit_set_command(target: str) -> int:
    if target == "speaker":
        return VOLUME_LIMIT_SPEAKER_SET_COMMAND
    if target == "audio":
        return VOLUME_LIMIT_AUDIO_SET_COMMAND
    raise ValueError("volume-limit target must be speaker or audio")


def volume_step_name_to_value(name: str) -> int:
    normalized = name.strip().lower().replace("_", "-").replace(" ", "-")
    if normalized.startswith("0x"):
        value = int(normalized, 16)
    elif normalized.isdigit():
        value = int(normalized, 10)
    elif normalized in VOLUME_STEP_ALIASES:
        value = VOLUME_STEP_ALIASES[normalized]
    else:
        raise ValueError(f"unknown volume step direction: {name}")
    validate_byte(value, "volume step")
    if value not in VOLUME_STEP_NAMES:
        raise ValueError(f"unknown volume step value: 0x{value:02X}")
    return value


def volume_step_value_to_name(value: int) -> str:
    if value not in VOLUME_STEP_NAMES:
        raise SicpProtocolError(f"Unknown volume step value: 0x{value:02X}")
    return VOLUME_STEP_NAMES[value]


def validate_audio_parameter(value: int, name: str) -> int:
    if not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")
    if -8 <= value <= -1:
        return value + 0x100
    validate_byte(value, name)
    if value > 100 and value < 0xF8:
        raise ValueError(f"{name} must be in range 0..100 or -8..-1")
    return value


def audio_parameter_value_to_display(value: int) -> int:
    validate_byte(value, "audio parameter")
    if value <= 100:
        return value
    if 0xF8 <= value <= 0xFF:
        return value - 0x100
    raise SicpProtocolError(f"Unknown audio parameter value: 0x{value:02X}")


def parse_audio_parameter_value(name: str, label: str) -> int:
    normalized = name.strip().lower()
    try:
        value = (
            int(normalized, 16) if normalized.startswith("0x") else int(normalized, 10)
        )
    except ValueError as exc:
        raise ValueError(f"{label} must be in range 0..100 or -8..8") from exc
    if -8 <= value <= 8:
        return validate_audio_parameter(value, label)
    if 9 <= value <= 100:
        return validate_audio_parameter(value, label)
    raise ValueError(f"{label} must be in range 0..100 or -8..8")


def bool_to_mute_value(muted: bool) -> int:
    return 0x01 if muted else 0x00


def mute_value_to_bool(value: int) -> bool:
    if value == 0x00:
        return False
    if value == 0x01:
        return True
    raise SicpProtocolError(f"Unknown mute value: 0x{value:02X}")


def gamma_value_to_name(value: int) -> str:
    if value not in GAMMA_NAMES:
        raise SicpProtocolError(f"Unknown gamma value: 0x{value:02X}")
    return GAMMA_NAMES[value]


def gamma_name_to_value(name: str) -> int:
    normalized = name.strip().lower().replace("_", "-").replace(" ", "-")
    if normalized.startswith("0x"):
        value = int(normalized, 16)
    elif normalized.isdigit() and "." not in normalized:
        value = int(normalized, 10)
    elif normalized in GAMMA_ALIASES:
        value = GAMMA_ALIASES[normalized]
    else:
        raise ValueError(f"unknown gamma: {name}")
    validate_byte(value, "gamma")
    if value not in GAMMA_NAMES:
        raise ValueError(f"unknown gamma value: 0x{value:02X}")
    return value


def color_temperature_value_to_name(value: int) -> str:
    if value not in COLOR_TEMPERATURE_NAMES:
        raise SicpProtocolError(f"Unknown color-temperature value: 0x{value:02X}")
    return COLOR_TEMPERATURE_NAMES[value]


def color_temperature_name_to_value(name: str) -> int:
    normalized = name.strip().lower().replace("_", "-").replace(" ", "-")
    if normalized.startswith("0x"):
        value = int(normalized, 16)
    elif normalized.isdigit():
        value = int(normalized, 10)
    elif normalized in COLOR_TEMPERATURE_ALIASES:
        value = COLOR_TEMPERATURE_ALIASES[normalized]
    else:
        raise ValueError(f"unknown color temperature: {name}")
    validate_byte(value, "color temperature")
    if value not in COLOR_TEMPERATURE_NAMES:
        raise ValueError(f"unknown color-temperature value: 0x{value:02X}")
    return value


def power_saving_mode_value_to_name(value: int) -> str:
    if value not in POWER_SAVING_MODE_NAMES:
        raise SicpProtocolError(f"Unknown power-saving mode value: 0x{value:02X}")
    return POWER_SAVING_MODE_NAMES[value]


def power_saving_mode_name_to_value(name: str) -> int:
    normalized = name.strip().lower().replace("_", "-").replace(" ", "-")
    if normalized.startswith("0x"):
        value = int(normalized, 16)
    elif normalized.isdigit():
        value = int(normalized, 10)
    elif normalized in POWER_SAVING_MODE_ALIASES:
        value = POWER_SAVING_MODE_ALIASES[normalized]
    else:
        raise ValueError(f"unknown power-saving mode: {name}")
    validate_byte(value, "power-saving mode")
    if value not in POWER_SAVING_MODE_NAMES:
        raise ValueError(f"unknown power-saving mode value: 0x{value:02X}")
    return value


def power_saving_mode_status_value_to_name(value: int) -> str:
    if value not in POWER_SAVING_MODE_STATUS_NAMES:
        raise SicpProtocolError(
            f"Unknown power-saving mode status value: 0x{value:02X}"
        )
    return POWER_SAVING_MODE_STATUS_NAMES[value]


def power_saving_mode_status_name_to_value(name: str) -> int:
    normalized = name.strip().lower().replace("_", "-").replace(" ", "-")
    if normalized.startswith("0x"):
        value = int(normalized, 16)
    elif normalized.isdigit():
        value = int(normalized, 10)
    elif normalized in POWER_SAVING_MODE_STATUS_ALIASES:
        value = POWER_SAVING_MODE_STATUS_ALIASES[normalized]
    else:
        raise ValueError(f"unknown power-saving mode status: {name}")
    validate_byte(value, "power-saving mode status")
    if value not in POWER_SAVING_MODE_STATUS_NAMES:
        raise ValueError(f"unknown power-saving mode status value: 0x{value:02X}")
    return value


def apm_status_value_to_name(value: int) -> str:
    if value not in APM_STATUS_NAMES:
        raise SicpProtocolError(f"Unknown APM status value: 0x{value:02X}")
    return APM_STATUS_NAMES[value]


def apm_status_name_to_value(name: str) -> int:
    normalized = name.strip().lower().replace("_", "-").replace(" ", "-")
    if normalized.startswith("0x"):
        value = int(normalized, 16)
    elif normalized.isdigit():
        value = int(normalized, 10)
    elif normalized in APM_STATUS_ALIASES:
        value = APM_STATUS_ALIASES[normalized]
    else:
        raise ValueError(f"unknown APM status: {name}")
    validate_byte(value, "APM status")
    if value not in APM_STATUS_NAMES:
        raise ValueError(f"unknown APM status value: 0x{value:02X}")
    return value


def light_sensor_value_to_name(value: int) -> str:
    if value not in LIGHT_SENSOR_NAMES:
        raise SicpProtocolError(f"Unknown light-sensor value: 0x{value:02X}")
    return LIGHT_SENSOR_NAMES[value]


def light_sensor_name_to_value(name: str, *, allow_unavailable: bool = False) -> int:
    normalized = name.strip().lower().replace("_", "-").replace(" ", "-")
    if normalized.startswith("0x"):
        value = int(normalized, 16)
    elif normalized.isdigit():
        value = int(normalized, 10)
    elif normalized in LIGHT_SENSOR_ALIASES:
        value = LIGHT_SENSOR_ALIASES[normalized]
    else:
        raise ValueError(f"unknown light-sensor state: {name}")
    validate_byte(value, "light sensor")
    valid_values = LIGHT_SENSOR_NAMES if allow_unavailable else LIGHT_SENSOR_SET_NAMES
    if value not in valid_values:
        raise ValueError(f"unknown light-sensor state value: 0x{value:02X}")
    return value


def osd_rotating_value_to_name(value: int) -> str:
    if value not in OSD_ROTATING_NAMES:
        raise SicpProtocolError(f"Unknown OSD rotating value: 0x{value:02X}")
    return OSD_ROTATING_NAMES[value]


def osd_rotating_name_to_value(name: str) -> int:
    normalized = name.strip().lower().replace("_", "-").replace(" ", "-")
    if normalized.startswith("0x"):
        value = int(normalized, 16)
    elif normalized.isdigit():
        value = int(normalized, 10)
    elif normalized in OSD_ROTATING_ALIASES:
        value = OSD_ROTATING_ALIASES[normalized]
    else:
        raise ValueError(f"unknown OSD rotating state: {name}")
    validate_byte(value, "OSD rotating")
    if value not in OSD_ROTATING_NAMES:
        raise ValueError(f"unknown OSD rotating value: 0x{value:02X}")
    return value


def _named_byte_value_to_name(
    value: int,
    names: dict[int, str],
    label: str,
) -> str:
    if value not in names:
        raise SicpProtocolError(f"Unknown {label} value: 0x{value:02X}")
    return names[value]


def _named_byte_name_to_value(
    name: str,
    aliases: dict[str, int],
    names: dict[int, str],
    label: str,
) -> int:
    normalized = name.strip().lower().replace("_", "-").replace(" ", "-")
    if normalized.startswith("0x"):
        value = int(normalized, 16)
    elif normalized.isdigit():
        value = int(normalized, 10)
    elif normalized in aliases:
        value = aliases[normalized]
    else:
        raise ValueError(f"unknown {label}: {name}")
    validate_byte(value, label)
    if value not in names:
        raise ValueError(f"unknown {label} value: 0x{value:02X}")
    return value


def display_orientation_auto_rotate_value_to_name(value: int) -> str:
    return _named_byte_value_to_name(
        value,
        DISPLAY_ORIENTATION_AUTO_ROTATE_NAMES,
        "display-orientation auto-rotate",
    )


def display_orientation_auto_rotate_name_to_value(name: str) -> int:
    return _named_byte_name_to_value(
        name,
        DISPLAY_ORIENTATION_AUTO_ROTATE_ALIASES,
        DISPLAY_ORIENTATION_AUTO_ROTATE_NAMES,
        "display-orientation auto-rotate",
    )


def display_orientation_osd_rotation_value_to_name(value: int) -> str:
    return _named_byte_value_to_name(
        value,
        DISPLAY_ORIENTATION_OSD_ROTATION_NAMES,
        "display-orientation OSD rotation",
    )


def display_orientation_osd_rotation_name_to_value(name: str) -> int:
    return _named_byte_name_to_value(
        name,
        DISPLAY_ORIENTATION_OSD_ROTATION_ALIASES,
        DISPLAY_ORIENTATION_OSD_ROTATION_NAMES,
        "display-orientation OSD rotation",
    )


def display_orientation_image_all_value_to_name(value: int) -> str:
    return _named_byte_value_to_name(
        value,
        DISPLAY_ORIENTATION_IMAGE_ALL_NAMES,
        "display-orientation image-all",
    )


def display_orientation_image_all_name_to_value(name: str) -> int:
    return _named_byte_name_to_value(
        name,
        DISPLAY_ORIENTATION_IMAGE_ALL_ALIASES,
        DISPLAY_ORIENTATION_IMAGE_ALL_NAMES,
        "display-orientation image-all",
    )


def display_orientation_window_value_to_name(
    value: int,
    *,
    label: str = "display-orientation window",
) -> str:
    return _named_byte_value_to_name(value, DISPLAY_ORIENTATION_WINDOW_NAMES, label)


def display_orientation_window_name_to_value(
    name: str,
    *,
    label: str = "display-orientation window",
) -> int:
    return _named_byte_name_to_value(
        name,
        DISPLAY_ORIENTATION_WINDOW_ALIASES,
        DISPLAY_ORIENTATION_WINDOW_NAMES,
        label,
    )


def validate_display_orientation_values(
    auto_rotate: int,
    osd_rotation: int,
    image_all: int,
    window1: int,
    window2: int,
    window3: int,
    window4: int,
) -> tuple[int, int, int, int, int, int, int]:
    display_orientation_auto_rotate_value_to_name(auto_rotate)
    display_orientation_osd_rotation_value_to_name(osd_rotation)
    display_orientation_image_all_value_to_name(image_all)
    windows = (window1, window2, window3, window4)
    for index, value in enumerate(windows, start=1):
        display_orientation_window_value_to_name(value, label=f"window{index}")
    return (auto_rotate, osd_rotation, image_all, window1, window2, window3, window4)


def touch_feature_value_to_name(value: int) -> str:
    if value not in TOUCH_FEATURE_NAMES:
        raise SicpProtocolError(f"Unknown touch-feature value: 0x{value:02X}")
    return TOUCH_FEATURE_NAMES[value]


def touch_feature_name_to_value(name: str) -> int:
    normalized = name.strip().lower().replace("_", "-").replace(" ", "-")
    if normalized.startswith("0x"):
        value = int(normalized, 16)
    elif normalized.isdigit():
        value = int(normalized, 10)
    elif normalized in TOUCH_FEATURE_ALIASES:
        value = TOUCH_FEATURE_ALIASES[normalized]
    else:
        raise ValueError(f"unknown touch-feature state: {name}")
    validate_byte(value, "touch feature")
    if value not in TOUCH_FEATURE_NAMES:
        raise ValueError(f"unknown touch-feature value: 0x{value:02X}")
    return value


def noise_reduction_value_to_name(value: int) -> str:
    if value not in NOISE_REDUCTION_NAMES:
        raise SicpProtocolError(f"Unknown noise-reduction value: 0x{value:02X}")
    return NOISE_REDUCTION_NAMES[value]


def noise_reduction_name_to_value(name: str) -> int:
    normalized = name.strip().lower().replace("_", "-").replace(" ", "-")
    if normalized.startswith("0x"):
        value = int(normalized, 16)
    elif normalized.isdigit():
        value = int(normalized, 10)
    elif normalized in NOISE_REDUCTION_ALIASES:
        value = NOISE_REDUCTION_ALIASES[normalized]
    else:
        raise ValueError(f"unknown noise-reduction level: {name}")
    validate_byte(value, "noise reduction")
    if value not in NOISE_REDUCTION_NAMES:
        raise ValueError(f"unknown noise-reduction value: 0x{value:02X}")
    return value


def scan_mode_value_to_name(value: int) -> str:
    if value in SCAN_MODE_NAMES:
        return SCAN_MODE_NAMES[value]
    if SCAN_MODE_CUSTOM_MIN <= value <= SCAN_MODE_CUSTOM_MAX:
        return f"custom-{value - SCAN_MODE_CUSTOM_MIN}"
    raise SicpProtocolError(f"Unknown scan-mode value: 0x{value:02X}")


def scan_mode_name_to_value(name: str) -> int:
    normalized = name.strip().lower().replace("_", "-").replace(" ", "-")
    if normalized.startswith("custom-"):
        try:
            custom_value = int(normalized.removeprefix("custom-"), 10)
        except ValueError as exc:
            raise ValueError(f"unknown scan-mode value: {name}") from exc
        if custom_value < 0 or custom_value > 25:
            raise ValueError("scan-mode custom value must be in range 0..25")
        return SCAN_MODE_CUSTOM_MIN + custom_value
    if normalized.startswith("level-"):
        try:
            custom_value = int(normalized.removeprefix("level-"), 10)
        except ValueError as exc:
            raise ValueError(f"unknown scan-mode value: {name}") from exc
        if custom_value < 0 or custom_value > 25:
            raise ValueError("scan-mode custom value must be in range 0..25")
        return SCAN_MODE_CUSTOM_MIN + custom_value
    if normalized.startswith("0x"):
        value = int(normalized, 16)
    elif normalized.isdigit():
        value = int(normalized, 10)
    elif normalized in SCAN_MODE_ALIASES:
        value = SCAN_MODE_ALIASES[normalized]
    else:
        raise ValueError(f"unknown scan-mode value: {name}")
    validate_byte(value, "scan mode")
    if value not in SCAN_MODE_NAMES and not (
        SCAN_MODE_CUSTOM_MIN <= value <= SCAN_MODE_CUSTOM_MAX
    ):
        raise ValueError(f"unknown scan-mode value: 0x{value:02X}")
    return value


def scan_conversion_value_to_name(value: int) -> str:
    if value not in SCAN_CONVERSION_NAMES:
        raise SicpProtocolError(f"Unknown scan-conversion value: 0x{value:02X}")
    return SCAN_CONVERSION_NAMES[value]


def scan_conversion_name_to_value(name: str) -> int:
    normalized = name.strip().lower().replace("_", "-").replace(" ", "-")
    if normalized.startswith("0x"):
        value = int(normalized, 16)
    elif normalized.isdigit():
        value = int(normalized, 10)
    elif normalized in SCAN_CONVERSION_ALIASES:
        value = SCAN_CONVERSION_ALIASES[normalized]
    else:
        raise ValueError(f"unknown scan-conversion value: {name}")
    validate_byte(value, "scan conversion")
    if value not in SCAN_CONVERSION_NAMES:
        raise ValueError(f"unknown scan-conversion value: 0x{value:02X}")
    return value


def pixel_shift_value_to_name(value: int) -> str:
    if value == PIXEL_SHIFT_OFF:
        return "off"
    if value == PIXEL_SHIFT_AUTO:
        return "auto"
    if 0x01 <= value <= 0x5A:
        return f"{value * PIXEL_SHIFT_SECONDS_STEP} seconds"
    raise SicpProtocolError(f"Unknown pixel-shift value: 0x{value:02X}")


def pixel_shift_name_to_value(name: str) -> int:
    normalized = name.strip().lower().replace("_", "-").replace(" ", "-")
    if normalized in ("off", "disabled", "disable"):
        return PIXEL_SHIFT_OFF
    if normalized in ("auto", "automatic"):
        return PIXEL_SHIFT_AUTO
    if normalized.startswith("0x"):
        value = int(normalized, 16)
    else:
        suffixes = (
            "-seconds",
            "-second",
            "-secs",
            "-sec",
            "seconds",
            "second",
            "secs",
            "sec",
            "s",
        )
        number = normalized
        for suffix in suffixes:
            if number.endswith(suffix):
                number = number[: -len(suffix)]
                break
        if not number.isdigit():
            raise ValueError(f"unknown pixel-shift value: {name}")
        seconds = int(number, 10)
        if seconds == 0:
            return PIXEL_SHIFT_OFF
        if (
            seconds < PIXEL_SHIFT_SECONDS_MIN
            or seconds > PIXEL_SHIFT_SECONDS_MAX
            or seconds % PIXEL_SHIFT_SECONDS_STEP != 0
        ):
            raise ValueError(
                "pixel-shift seconds must be off or in range 10..900 by 10"
            )
        value = seconds // PIXEL_SHIFT_SECONDS_STEP
    validate_byte(value, "pixel shift")
    if value != PIXEL_SHIFT_AUTO and not (PIXEL_SHIFT_OFF <= value <= 0x5A):
        raise ValueError(f"unknown pixel-shift value: 0x{value:02X}")
    return value


def memc_effect_value_to_name(value: int) -> str:
    if value not in MEMC_EFFECT_NAMES:
        raise SicpProtocolError(f"Unknown MEMC effect value: 0x{value:02X}")
    return MEMC_EFFECT_NAMES[value]


def memc_effect_name_to_value(name: str) -> int:
    normalized = name.strip().lower().replace("_", "-").replace(" ", "-")
    if normalized.startswith("0x"):
        value = int(normalized, 16)
    elif normalized.isdigit():
        value = int(normalized, 10)
    elif normalized in MEMC_EFFECT_ALIASES:
        value = MEMC_EFFECT_ALIASES[normalized]
    else:
        raise ValueError(f"unknown MEMC effect: {name}")
    validate_byte(value, "MEMC effect")
    if value not in MEMC_EFFECT_NAMES:
        raise ValueError(f"unknown MEMC effect value: 0x{value:02X}")
    return value


def validate_information_osd_value(value: int) -> int:
    validate_byte(value, "information OSD")
    if value > 60:
        raise ValueError("information OSD must be off or in range 1..60")
    return value


def information_osd_value_to_name(value: int) -> str:
    value = validate_information_osd_value(value)
    return "off" if value == 0 else f"{value} seconds"


def information_osd_name_to_value(name: str) -> int:
    normalized = name.strip().lower().replace("_", "-").replace(" ", "-")
    if normalized in ("off", "none", "disabled"):
        return 0
    if normalized.startswith("0x"):
        value = int(normalized, 16)
    else:
        value = int(normalized, 10)
    return validate_information_osd_value(value)


def human_sensor_value_to_name(value: int) -> str:
    if value not in HUMAN_SENSOR_NAMES:
        raise SicpProtocolError(f"Unknown human-sensor value: 0x{value:02X}")
    return HUMAN_SENSOR_NAMES[value]


def human_sensor_name_to_value(name: str, *, allow_unavailable: bool = False) -> int:
    normalized = name.strip().lower().replace("_", "-").replace(" ", "-")
    if normalized.startswith("0x"):
        value = int(normalized, 16)
    elif normalized in HUMAN_SENSOR_ALIASES:
        value = HUMAN_SENSOR_ALIASES[normalized]
    elif normalized.isdigit():
        value = int(normalized, 10)
    else:
        raise ValueError(f"unknown human-sensor state: {name}")
    validate_byte(value, "human sensor")
    valid_values = HUMAN_SENSOR_NAMES if allow_unavailable else HUMAN_SENSOR_SET_NAMES
    if value not in valid_values:
        raise ValueError(f"unknown human-sensor state value: 0x{value:02X}")
    return value


def power_on_logo_value_to_name(value: int) -> str:
    if value not in POWER_ON_LOGO_NAMES:
        raise SicpProtocolError(f"Unknown power-on-logo value: 0x{value:02X}")
    return POWER_ON_LOGO_NAMES[value]


def power_on_logo_name_to_value(name: str) -> int:
    normalized = name.strip().lower().replace("_", "-").replace(" ", "-")
    if normalized.startswith("0x"):
        value = int(normalized, 16)
    elif normalized.isdigit():
        value = int(normalized, 10)
    elif normalized in POWER_ON_LOGO_ALIASES:
        value = POWER_ON_LOGO_ALIASES[normalized]
    else:
        raise ValueError(f"unknown power-on-logo state: {name}")
    validate_byte(value, "power-on logo")
    if value not in POWER_ON_LOGO_NAMES:
        raise ValueError(f"unknown power-on-logo state value: 0x{value:02X}")
    return value


def validate_off_timer_hours(value: int) -> int:
    validate_byte(value, "off timer")
    if value > 24:
        raise ValueError("off timer must be in range 0..24 hours")
    return value


def off_timer_name_to_value(name: str) -> int:
    normalized = name.strip().lower().replace("_", "-").replace(" ", "-")
    if normalized == "off":
        return 0
    if normalized.endswith("-hours"):
        normalized = normalized[:-6]
    elif normalized.endswith("-hour"):
        normalized = normalized[:-5]
    elif normalized.endswith("h"):
        normalized = normalized[:-1]
    if normalized.startswith("0x"):
        value = int(normalized, 16)
    else:
        value = int(normalized, 10)
    return validate_off_timer_hours(value)


def off_timer_value_to_name(value: int) -> str:
    hours = validate_off_timer_hours(value)
    if hours == 0:
        return "off"
    if hours == 1:
        return "1-hour"
    return f"{hours}-hours"


def eco_mode_value_to_name(value: int) -> str:
    if value not in ECO_MODE_NAMES:
        raise SicpProtocolError(f"Unknown ECO mode value: 0x{value:02X}")
    return ECO_MODE_NAMES[value]


def eco_mode_name_to_value(name: str) -> int:
    normalized = name.strip().lower().replace("_", "-").replace(" ", "-")
    if normalized.startswith("0x"):
        value = int(normalized, 16)
    elif normalized.isdigit():
        value = int(normalized, 10)
    elif normalized in ECO_MODE_ALIASES:
        value = ECO_MODE_ALIASES[normalized]
    else:
        raise ValueError(f"unknown ECO mode: {name}")
    validate_byte(value, "ECO mode")
    if value not in ECO_MODE_NAMES:
        raise ValueError(f"unknown ECO mode value: 0x{value:02X}")
    return value


def picture_style_value_to_name(value: int) -> str:
    if value not in PICTURE_STYLE_NAMES:
        raise SicpProtocolError(f"Unknown picture-style value: 0x{value:02X}")
    return PICTURE_STYLE_NAMES[value]


def picture_style_name_to_value(name: str) -> int:
    normalized = name.strip().lower().replace("_", "-").replace(" ", "-")
    if normalized.startswith("0x"):
        value = int(normalized, 16)
    elif normalized.isdigit():
        value = int(normalized, 10)
    elif normalized in PICTURE_STYLE_ALIASES:
        value = PICTURE_STYLE_ALIASES[normalized]
    else:
        raise ValueError(f"unknown picture style: {name}")
    validate_byte(value, "picture style")
    if value not in PICTURE_STYLE_NAMES:
        raise ValueError(f"unknown picture-style value: 0x{value:02X}")
    return value


def group_id_value_to_id(value: int) -> int | None:
    validate_byte(value, "group ID")
    if value == GROUP_ID_OFF:
        return None
    if value < 1 or value > 254:
        raise SicpProtocolError(f"Unknown group ID value: 0x{value:02X}")
    return value


def group_id_value_to_name(value: int) -> str:
    group_id = group_id_value_to_id(value)
    return "off" if group_id is None else str(group_id)


def group_id_name_to_value(name: str) -> int:
    normalized = name.strip().lower().replace("_", "-").replace(" ", "-")
    if normalized in ("off", "none", "disabled"):
        return GROUP_ID_OFF
    if normalized.startswith("0x"):
        value = int(normalized, 16)
    else:
        value = int(normalized, 10)
    validate_byte(value, "group ID")
    if value < 1 or value > 254:
        raise ValueError("group ID must be in range 1..254 or off")
    return value


def validate_monitor_id_value(value: int) -> int:
    validate_byte(value, "monitor ID")
    if value < 1:
        raise ValueError("monitor ID must be in range 1..255")
    return value


def monitor_id_name_to_value(name: str) -> int:
    normalized = name.strip().lower().replace("_", "-").replace(" ", "-")
    if normalized.startswith("0x"):
        value = int(normalized, 16)
    else:
        value = int(normalized, 10)
    return validate_monitor_id_value(value)


def ports_lock_value_to_name(value: int) -> str:
    if value not in PORTS_LOCK_NAMES:
        raise SicpProtocolError(f"Unknown ports-lock value: 0x{value:02X}")
    return PORTS_LOCK_NAMES[value]


def ports_lock_name_to_value(name: str) -> int:
    normalized = name.strip().lower().replace("_", "-").replace(" ", "-")
    if normalized.startswith("0x"):
        value = int(normalized, 16)
    elif normalized.isdigit():
        value = int(normalized, 10)
    elif normalized in PORTS_LOCK_ALIASES:
        value = PORTS_LOCK_ALIASES[normalized]
    else:
        raise ValueError(f"unknown ports-lock state: {name}")
    validate_byte(value, "ports-lock state")
    if value not in PORTS_LOCK_NAMES:
        raise ValueError(f"unknown ports-lock state value: 0x{value:02X}")
    return value


def validate_color_temperature_100k_steps(value: int) -> int:
    validate_byte(value, "color temperature 100K steps")
    if value < 20 or value > 100:
        raise ValueError("color temperature 100K steps must be in range 20..100")
    return value


def build_input_source_osd_style(
    *,
    do_not_switch: bool = False,
    display_style: str = "source-label",
) -> int:
    if display_style == "source-label":
        value = INPUT_SOURCE_DISPLAY_STYLE_SOURCE_LABEL
    elif display_style == "reserved":
        value = INPUT_SOURCE_DISPLAY_STYLE_RESERVED
    else:
        raise ValueError("display style must be source-label or reserved")
    if do_not_switch:
        value |= 0x40
    return value


class SicpClient:
    def __init__(
        self,
        host: str,
        port: int = DEFAULT_PORT,
        monitor_id: int = DEFAULT_MONITOR_ID,
        group_id: int = DEFAULT_GROUP_ID,
        timeout: float = DEFAULT_TIMEOUT,
        retries: int = DEFAULT_RETRIES,
    ):
        if not host:
            raise ValueError("host is required")
        validate_byte(monitor_id, "monitor_id")
        validate_byte(group_id, "group_id")
        if port <= 0 or port > 65535:
            raise ValueError("port must be in range 1..65535")
        if timeout <= 0:
            raise ValueError("timeout must be positive")
        if retries < 0:
            raise ValueError("retries must be >= 0")

        self.host = host
        self.port = port
        self.monitor_id = monitor_id
        self.group_id = group_id
        self.timeout = timeout
        self.retries = retries

    def build_request(self, command: int, *parameters: int) -> bytes:
        return build_packet(
            command,
            *parameters,
            monitor_id=self.monitor_id,
            group_id=self.group_id,
        )

    def transact(
        self,
        command: int,
        *parameters: int,
        expected_response_commands: tuple[int, ...] | None = None,
        expected_response_sizes: tuple[int, ...] | None = None,
    ) -> SicpPacket:
        transaction = self.transact_with_request(
            command,
            *parameters,
            expected_response_commands=expected_response_commands,
            expected_response_sizes=expected_response_sizes,
        )
        if transaction.response is None:
            raise SicpError("Command did not return a response")
        return transaction.response

    def transact_with_request(
        self,
        command: int,
        *parameters: int,
        expected_response_commands: tuple[int, ...] | None = None,
        expected_response_sizes: tuple[int, ...] | None = None,
    ) -> SicpTransaction:
        request = self.build_request(command, *parameters)
        response = self.send_raw(
            request,
            expected_response_commands=expected_response_commands,
            expected_response_sizes=expected_response_sizes,
        )
        return SicpTransaction(
            request=request,
            response=response.packet if response is not None else None,
            skipped=response.skipped if response is not None else (),
        )

    def send_raw(
        self,
        packet: bytes,
        expected_response_commands: tuple[int, ...] | None = None,
        expected_response_sizes: tuple[int, ...] | None = None,
    ) -> _ReceiveResult | None:
        if len(packet) < 2:
            raise ValueError("raw packet is too short")

        attempts = self.retries + 1
        last_error: Exception | None = None
        for _ in range(attempts):
            try:
                with socket.create_connection(
                    (self.host, self.port), timeout=self.timeout
                ) as sock:
                    sock.settimeout(self.timeout)
                    sock.sendall(packet)
                    if packet[1] == 0x00:
                        return None
                    return self._recv_packet(
                        sock,
                        expected_response_commands=expected_response_commands,
                        expected_response_sizes=expected_response_sizes,
                    )
            except (TimeoutError, ConnectionError, OSError, SicpProtocolError) as exc:
                last_error = exc

        if last_error is None:
            raise SicpError("SICP transaction failed")
        raise SicpError(f"SICP transaction failed: {last_error}") from last_error

    def get_power_state(self) -> bool:
        return decode_power_report(
            self.transact(
                POWER_GET_COMMAND,
                expected_response_commands=(POWER_GET_COMMAND,),
                expected_response_sizes=(6,),
            )
        )

    def set_power_state(self, on: bool) -> None:
        value = bool_to_power_value(on)
        response = self.transact(
            POWER_SET_COMMAND,
            value,
            expected_response_commands=(0x00,),
            expected_response_sizes=(6,),
        )
        require_ack(response)

    def get_power_cold_start_state(self) -> str:
        return decode_power_cold_start_report(
            self.transact(
                POWER_COLD_START_GET_COMMAND,
                expected_response_commands=(POWER_COLD_START_GET_COMMAND,),
                expected_response_sizes=(6,),
            )
        )

    def set_power_cold_start_state(self, state: str) -> None:
        value = power_cold_start_name_to_value(state)
        response = self.transact(
            POWER_COLD_START_SET_COMMAND,
            value,
            expected_response_commands=(0x00,),
            expected_response_sizes=(6,),
        )
        require_ack(response)

    def get_operating_hours(self) -> int:
        return decode_operating_hours_report(
            self.transact(
                OPERATING_HOURS_COMMAND,
                OPERATING_HOURS_ITEM,
                expected_response_commands=(OPERATING_HOURS_COMMAND,),
                expected_response_sizes=(7,),
            )
        )

    def get_tiling(self) -> TilingState:
        return decode_tiling_report(
            self.transact(
                TILING_GET_COMMAND,
                expected_response_commands=(TILING_GET_COMMAND,),
                expected_response_sizes=(9,),
            )
        )

    def set_tiling(
        self,
        enabled: str | int,
        frame_compensation: str | int = TILING_FRAME_COMP_KEEP,
        position: str | int = TILING_KEEP,
        wall_size: int = TILING_KEEP,
        *,
        zero_bezel: bool = False,
    ) -> None:
        enabled_value = (
            tiling_enable_name_to_value(enabled)
            if isinstance(enabled, str)
            else validate_byte(enabled, "tiling enable")
        )
        frame_comp_value = (
            tiling_frame_comp_name_to_value(frame_compensation)
            if isinstance(frame_compensation, str)
            else validate_byte(frame_compensation, "tiling frame compensation")
        )
        position_value = (
            tiling_position_name_to_value(position, zero_bezel=zero_bezel)
            if isinstance(position, str)
            else validate_byte(position, "tiling position")
        )
        values = build_tiling_set_values(
            enabled_value,
            frame_comp_value,
            position_value,
            wall_size,
            zero_bezel=zero_bezel,
        )
        response = self.transact(
            TILING_SET_COMMAND,
            *values,
            expected_response_commands=(0x00,),
            expected_response_sizes=(6,),
        )
        require_ack(response)

    def get_switch_on_delay(self) -> int:
        return decode_switch_on_delay_report(
            self.transact(
                SWITCH_ON_DELAY_GET_COMMAND,
                expected_response_commands=(SWITCH_ON_DELAY_GET_COMMAND,),
                expected_response_sizes=(6,),
            )
        )

    def set_switch_on_delay(self, delay: str | int) -> None:
        value = (
            switch_on_delay_name_to_value(delay)
            if isinstance(delay, str)
            else validate_byte(delay, "switch-on delay")
        )
        response = self.transact(
            SWITCH_ON_DELAY_SET_COMMAND,
            value,
            expected_response_commands=(0x00,),
            expected_response_sizes=(6,),
        )
        require_ack(response)

    def get_frame_compensation_horizontal(self) -> int:
        return decode_frame_compensation_horizontal_report(
            self.transact(
                FRAME_COMPENSATION_HORIZONTAL_GET_COMMAND,
                expected_response_commands=(FRAME_COMPENSATION_HORIZONTAL_GET_COMMAND,),
                expected_response_sizes=(6,),
            )
        )

    def set_frame_compensation_horizontal(self, value: int) -> None:
        value = validate_byte(value, "horizontal frame compensation")
        response = self.transact(
            FRAME_COMPENSATION_HORIZONTAL_SET_COMMAND,
            value,
            expected_response_commands=(0x00,),
            expected_response_sizes=(6,),
        )
        require_ack(response)

    def get_frame_compensation_vertical(self) -> int:
        return decode_frame_compensation_vertical_report(
            self.transact(
                FRAME_COMPENSATION_VERTICAL_GET_COMMAND,
                expected_response_commands=(FRAME_COMPENSATION_VERTICAL_GET_COMMAND,),
                expected_response_sizes=(6,),
            )
        )

    def set_frame_compensation_vertical(self, value: int) -> None:
        value = validate_byte(value, "vertical frame compensation")
        response = self.transact(
            FRAME_COMPENSATION_VERTICAL_SET_COMMAND,
            value,
            expected_response_commands=(0x00,),
            expected_response_sizes=(6,),
        )
        require_ack(response)

    def get_anytile(self) -> AnyTileState:
        return decode_anytile_report(
            self.transact(
                ANYTILE_GET_COMMAND,
                expected_response_commands=(ANYTILE_GET_COMMAND,),
                expected_response_sizes=(16,),
            )
        )

    def set_anytile(
        self,
        enabled: str | int,
        rotation: int,
        input_h_start: int,
        input_v_start: int,
        input_h_size: int,
        input_v_size: int,
    ) -> None:
        enabled_value = (
            tiling_enable_name_to_value(enabled)
            if isinstance(enabled, str)
            else validate_byte(enabled, "AnyTile enable")
        )
        parameters = build_anytile_parameters(
            enabled_value,
            rotation,
            input_h_start,
            input_v_start,
            input_h_size,
            input_v_size,
        )
        response = self.transact(
            ANYTILE_SET_COMMAND,
            *parameters,
            expected_response_commands=(0x00,),
            expected_response_sizes=(6,),
        )
        require_ack(response)

    def get_anytile_resolution(self) -> str:
        return decode_anytile_resolution_report(
            self.transact(
                ANYTILE_RESOLUTION_GET_COMMAND,
                expected_response_commands=(ANYTILE_RESOLUTION_GET_COMMAND,),
                expected_response_sizes=(6,),
            )
        )

    def set_anytile_resolution(self, mode: str | int) -> None:
        value = (
            anytile_resolution_name_to_value(mode)
            if isinstance(mode, str)
            else validate_byte(mode, "AnyTile resolution mode")
        )
        anytile_resolution_value_to_name(value)
        response = self.transact(
            ANYTILE_RESOLUTION_SET_COMMAND,
            value,
            expected_response_commands=(0x00,),
            expected_response_sizes=(6,),
        )
        require_ack(response)

    def assign_anytile_ids(self, monitor_id: int, group_id: int) -> None:
        response = self.transact(
            ANYTILE_ASSIGN_IDS_COMMAND,
            validate_byte(monitor_id, "monitor ID"),
            validate_byte(group_id, "group ID"),
            expected_response_commands=(0x00,),
            expected_response_sizes=(6,),
        )
        require_ack(response)

    def set_anytile_display_monitor_id(self, monitor_id: int) -> None:
        response = self.transact(
            ANYTILE_DISPLAY_MONITOR_ID_SET_COMMAND,
            validate_byte(monitor_id, "monitor ID"),
            expected_response_commands=(0x00,),
            expected_response_sizes=(6,),
        )
        require_ack(response)

    def get_input_source(self) -> InputSourceState:
        return decode_input_source_report(
            self.transact(
                INPUT_SOURCE_GET_COMMAND,
                expected_response_commands=(INPUT_SOURCE_GET_COMMAND,),
                expected_response_sizes=(9,),
            )
        )

    def set_input_source(
        self,
        source: str | int,
        playlist: int = 0,
        osd_style: int = INPUT_SOURCE_DISPLAY_STYLE_SOURCE_LABEL,
        mute_style: int = 0,
    ) -> None:
        source_value = (
            input_source_name_to_value(source)
            if isinstance(source, str)
            else validate_byte(source, "input source")
        )
        validate_byte(playlist, "playlist")
        validate_byte(osd_style, "osd_style")
        validate_byte(mute_style, "mute_style")
        response = self.transact(
            INPUT_SOURCE_SET_COMMAND,
            source_value,
            playlist,
            osd_style,
            mute_style,
            expected_response_commands=(0x00,),
            expected_response_sizes=(6,),
        )
        require_ack(response)

    def get_scheduling(self, page: int) -> SchedulingState:
        page = validate_scheduling_page(page)
        return decode_scheduling_report(
            self.transact(
                SCHEDULING_GET_COMMAND,
                page,
                expected_response_commands=(SCHEDULING_GET_COMMAND,),
                expected_response_sizes=(12, 13),
            )
        )

    def set_scheduling(
        self,
        page: int,
        enabled: bool,
        start_time: tuple[int, int],
        end_time: tuple[int, int],
        source: str | int,
        days: str | int,
        tag: int | None = None,
    ) -> None:
        page = validate_scheduling_page(page)
        start_hour, start_minute = validate_scheduling_time(*start_time)
        end_hour, end_minute = validate_scheduling_time(*end_time)
        source_value = (
            scheduling_source_name_to_value(source)
            if isinstance(source, str)
            else validate_byte(source, "scheduling source")
        )
        days_value = (
            scheduling_days_name_to_value(days)
            if isinstance(days, str)
            else validate_byte(days, "scheduling days")
        )
        tag = validate_scheduling_tag(tag)
        page_state = (page << 4) | (0x01 if enabled else 0x00)
        parameters = [
            page_state,
            start_hour,
            start_minute,
            end_hour,
            end_minute,
            source_value,
            days_value,
        ]
        if tag is not None:
            parameters.append(tag)
        response = self.transact(
            SCHEDULING_SET_COMMAND,
            *parameters,
            expected_response_commands=(0x00,),
            expected_response_sizes=(6,),
        )
        require_ack(response)

    def get_auto_signal_mode(self) -> str:
        return decode_auto_signal_report(
            self.transact(
                AUTO_SIGNAL_GET_COMMAND,
                expected_response_commands=(AUTO_SIGNAL_GET_COMMAND,),
                expected_response_sizes=(6,),
            )
        )

    def set_auto_signal_mode(self, mode: str) -> None:
        value = auto_signal_name_to_value(mode)
        response = self.transact(
            AUTO_SIGNAL_SET_COMMAND,
            value,
            expected_response_commands=(0x00,),
            expected_response_sizes=(6,),
        )
        require_ack(response)

    def get_failover_priorities(self) -> FailoverState:
        return decode_failover_report(
            self.transact(
                FAILOVER_GET_COMMAND,
                expected_response_commands=(FAILOVER_GET_COMMAND,),
            )
        )

    def set_failover_priorities(self, priorities: tuple[str | int, ...]) -> None:
        values = tuple(
            failover_source_name_to_value(priority)
            if isinstance(priority, str)
            else validate_byte(priority, "failover source")
            for priority in priorities
        )
        validate_failover_priorities(values)
        response = self.transact(
            FAILOVER_SET_COMMAND,
            *values,
            expected_response_commands=(0x00,),
            expected_response_sizes=(6,),
        )
        require_ack(response)

    def restart_monitor(self, target: str | int = "android") -> None:
        value = (
            monitor_restart_target_name_to_value(target)
            if isinstance(target, str)
            else validate_byte(target, "monitor restart target")
        )
        response = self.transact(
            MONITOR_RESTART_COMMAND,
            value,
            expected_response_commands=(0x00,),
            expected_response_sizes=(6,),
        )
        require_ack(response)

    def get_temperature(self) -> TemperatureState:
        return decode_temperature_report(
            self.transact(
                TEMPERATURE_GET_COMMAND,
                expected_response_commands=(TEMPERATURE_GET_COMMAND,),
                expected_response_sizes=(6, 7),
            )
        )

    def get_fan_speed(self) -> str:
        return decode_fan_speed_report(
            self.transact(
                FAN_SPEED_GET_COMMAND,
                expected_response_commands=(FAN_SPEED_GET_COMMAND,),
                expected_response_sizes=(6,),
            )
        )

    def set_fan_speed(self, speed: str | int) -> None:
        value = (
            fan_speed_name_to_value(speed)
            if isinstance(speed, str)
            else validate_byte(speed, "fan speed")
        )
        fan_speed_value_to_name(value)
        response = self.transact(
            FAN_SPEED_SET_COMMAND,
            value,
            expected_response_commands=(0x00,),
            expected_response_sizes=(6,),
        )
        require_ack(response)

    def get_video_signal_present(self) -> bool:
        return decode_video_signal_present_report(
            self.transact(
                VIDEO_SIGNAL_PRESENT_COMMAND,
                expected_response_commands=(VIDEO_SIGNAL_PRESENT_COMMAND,),
                expected_response_sizes=(6,),
            )
        )

    def get_ir_lock(self) -> str:
        return decode_ir_lock_report(
            self.transact(
                IR_LOCK_GET_COMMAND,
                expected_response_commands=(IR_LOCK_GET_COMMAND,),
                expected_response_sizes=(6,),
            )
        )

    def set_ir_lock(self, state: str | int) -> None:
        value = (
            lock_state_name_to_value(state, target="ir")
            if isinstance(state, str)
            else validate_byte(state, "IR lock state")
        )
        lock_state_value_to_name(value, target="ir")
        response = self.transact(
            IR_LOCK_SET_COMMAND,
            value,
            expected_response_commands=(0x00,),
            expected_response_sizes=(6,),
        )
        require_ack(response)

    def get_keypad_lock(self) -> str:
        return decode_keypad_lock_report(
            self.transact(
                KEYPAD_LOCK_GET_COMMAND,
                expected_response_commands=(KEYPAD_LOCK_GET_COMMAND,),
                expected_response_sizes=(6,),
            )
        )

    def set_keypad_lock(self, state: str | int) -> None:
        value = (
            lock_state_name_to_value(state, target="keypad")
            if isinstance(state, str)
            else validate_byte(state, "keypad lock state")
        )
        lock_state_value_to_name(value, target="keypad")
        response = self.transact(
            KEYPAD_LOCK_SET_COMMAND,
            value,
            expected_response_commands=(0x00,),
            expected_response_sizes=(6,),
        )
        require_ack(response)

    def get_video_parameters(self) -> VideoParametersState:
        return decode_video_parameters_report(
            self.transact(
                VIDEO_PARAMETERS_GET_COMMAND,
                expected_response_commands=(VIDEO_PARAMETERS_GET_COMMAND,),
                expected_response_sizes=(12,),
            )
        )

    def set_video_parameters(
        self,
        *,
        brightness: int,
        color: int,
        contrast: int,
        sharpness: int,
        tint: int,
        black_level: int,
        gamma: str | int,
    ) -> None:
        gamma_value = gamma_name_to_value(gamma) if isinstance(gamma, str) else gamma
        gamma_value_to_name(gamma_value)
        values = (
            validate_percentage(brightness, "brightness"),
            validate_percentage(color, "color"),
            validate_percentage(contrast, "contrast"),
            validate_percentage(sharpness, "sharpness"),
            validate_percentage(tint, "tint"),
            validate_percentage(black_level, "black level"),
            gamma_value,
        )
        response = self.transact(
            VIDEO_PARAMETERS_SET_COMMAND,
            *values,
            expected_response_commands=(0x00,),
            expected_response_sizes=(6,),
        )
        require_ack(response)

    def get_picture_format(self) -> str:
        return decode_picture_format_report(
            self.transact(
                PICTURE_FORMAT_GET_COMMAND,
                expected_response_commands=(PICTURE_FORMAT_GET_COMMAND,),
                expected_response_sizes=(6,),
            )
        )

    def set_picture_format(self, picture_format: str | int) -> None:
        value = (
            picture_format_name_to_value(picture_format)
            if isinstance(picture_format, str)
            else validate_byte(picture_format, "picture format")
        )
        picture_format_value_to_name(value)
        response = self.transact(
            PICTURE_FORMAT_SET_COMMAND,
            value,
            expected_response_commands=(0x00,),
            expected_response_sizes=(6,),
        )
        require_ack(response)

    def get_volume(self) -> VolumeState:
        return decode_volume_report(
            self.transact(
                VOLUME_GET_COMMAND,
                expected_response_commands=(VOLUME_GET_COMMAND,),
                expected_response_sizes=(6, 7),
            )
        )

    def set_volume(self, speaker: int, audio: int | None = None) -> None:
        parameters = [validate_volume_level(speaker, "speaker volume")]
        if audio is not None:
            parameters.append(validate_volume_level(audio, "audio volume"))
        response = self.transact(
            VOLUME_SET_COMMAND,
            *parameters,
            expected_response_commands=(0x00,),
            expected_response_sizes=(6,),
        )
        require_ack(response)

    def step_volume(self, speaker: str | int, audio: str | int | None = None) -> None:
        speaker_value = (
            volume_step_name_to_value(speaker)
            if isinstance(speaker, str)
            else validate_byte(speaker, "speaker volume step")
        )
        volume_step_value_to_name(speaker_value)
        parameters = [speaker_value]
        if audio is not None:
            audio_value = (
                volume_step_name_to_value(audio)
                if isinstance(audio, str)
                else validate_byte(audio, "audio volume step")
            )
            volume_step_value_to_name(audio_value)
            parameters.append(audio_value)
        response = self.transact(
            VOLUME_STEP_COMMAND,
            *parameters,
            expected_response_commands=(0x00,),
            expected_response_sizes=(6,),
        )
        require_ack(response)

    def get_volume_limit(self, target: str) -> VolumeLimitState:
        command = volume_limit_get_command(target)
        return decode_volume_limit_report(
            self.transact(
                command,
                expected_response_commands=(command,),
                expected_response_sizes=(8,),
            ),
            target=target,
        )

    def set_volume_limit(
        self,
        target: str,
        minimum: int,
        maximum: int,
        switch_on: int,
    ) -> None:
        command = volume_limit_set_command(target)
        values = validate_volume_limits(minimum, maximum, switch_on)
        response = self.transact(
            command,
            *values,
            expected_response_commands=(0x00,),
            expected_response_sizes=(6,),
        )
        require_ack(response)

    def get_audio_parameters(self) -> AudioParametersState:
        return decode_audio_parameters_report(
            self.transact(
                AUDIO_PARAMETERS_GET_COMMAND,
                expected_response_commands=(AUDIO_PARAMETERS_GET_COMMAND,),
                expected_response_sizes=(7,),
            )
        )

    def set_audio_parameters(self, treble: int, bass: int) -> None:
        response = self.transact(
            AUDIO_PARAMETERS_SET_COMMAND,
            validate_audio_parameter(treble, "treble"),
            validate_audio_parameter(bass, "bass"),
            expected_response_commands=(0x00,),
            expected_response_sizes=(6,),
        )
        require_ack(response)

    def get_volume_mute(self) -> bool:
        return decode_volume_mute_report(
            self.transact(
                VOLUME_MUTE_GET_COMMAND,
                expected_response_commands=(VOLUME_MUTE_GET_COMMAND,),
                expected_response_sizes=(6,),
            )
        )

    def set_volume_mute(self, muted: bool) -> None:
        response = self.transact(
            VOLUME_MUTE_SET_COMMAND,
            bool_to_mute_value(muted),
            expected_response_commands=(0x00,),
            expected_response_sizes=(6,),
        )
        require_ack(response)

    def get_color_temperature(self) -> str:
        return decode_color_temperature_report(
            self.transact(
                COLOR_TEMPERATURE_GET_COMMAND,
                expected_response_commands=(COLOR_TEMPERATURE_GET_COMMAND,),
                expected_response_sizes=(6,),
            )
        )

    def set_color_temperature(self, temperature: str | int) -> None:
        value = (
            color_temperature_name_to_value(temperature)
            if isinstance(temperature, str)
            else validate_byte(temperature, "color temperature")
        )
        color_temperature_value_to_name(value)
        response = self.transact(
            COLOR_TEMPERATURE_SET_COMMAND,
            value,
            expected_response_commands=(0x00,),
            expected_response_sizes=(6,),
        )
        require_ack(response)

    def get_rgb_parameters(self) -> RgbParametersState:
        return decode_rgb_parameters_report(
            self.transact(
                RGB_PARAMETERS_GET_COMMAND,
                expected_response_commands=(RGB_PARAMETERS_GET_COMMAND,),
                expected_response_sizes=(11,),
            )
        )

    def set_rgb_parameters(
        self,
        *,
        red_gain: int,
        green_gain: int,
        blue_gain: int,
        red_offset: int,
        green_offset: int,
        blue_offset: int,
    ) -> None:
        values = (
            validate_byte(red_gain, "red gain"),
            validate_byte(green_gain, "green gain"),
            validate_byte(blue_gain, "blue gain"),
            validate_byte(red_offset, "red offset"),
            validate_byte(green_offset, "green offset"),
            validate_byte(blue_offset, "blue offset"),
        )
        response = self.transact(
            RGB_PARAMETERS_SET_COMMAND,
            *values,
            expected_response_commands=(0x00,),
            expected_response_sizes=(6,),
        )
        require_ack(response)

    def get_color_temperature_100k(self) -> ColorTemperature100KState:
        return decode_color_temperature_100k_report(
            self.transact(
                COLOR_TEMPERATURE_100K_GET_COMMAND,
                expected_response_commands=(COLOR_TEMPERATURE_100K_GET_COMMAND,),
                expected_response_sizes=(6,),
            )
        )

    def set_color_temperature_100k(self, steps: int) -> None:
        value = validate_color_temperature_100k_steps(steps)
        response = self.transact(
            COLOR_TEMPERATURE_100K_SET_COMMAND,
            value,
            expected_response_commands=(0x00,),
            expected_response_sizes=(6,),
        )
        require_ack(response)

    def get_power_saving_mode(self) -> str:
        return decode_power_saving_mode_report(
            self.transact(
                POWER_SAVING_MODE_GET_COMMAND,
                expected_response_commands=(POWER_SAVING_MODE_GET_COMMAND,),
                expected_response_sizes=(6,),
            )
        )

    def set_power_saving_mode(self, mode: str | int) -> None:
        value = (
            power_saving_mode_name_to_value(mode)
            if isinstance(mode, str)
            else validate_byte(mode, "power-saving mode")
        )
        power_saving_mode_value_to_name(value)
        response = self.transact(
            POWER_SAVING_MODE_SET_COMMAND,
            value,
            expected_response_commands=(0x00,),
            expected_response_sizes=(6,),
        )
        require_ack(response)

    def get_power_saving_mode_status(self) -> str:
        return decode_power_saving_mode_status_report(
            self.transact(
                POWER_SAVING_MODE_STATUS_GET_COMMAND,
                expected_response_commands=(POWER_SAVING_MODE_STATUS_GET_COMMAND,),
                expected_response_sizes=(6,),
            )
        )

    def set_power_saving_mode_status(self, status: str | int) -> None:
        value = (
            power_saving_mode_status_name_to_value(status)
            if isinstance(status, str)
            else validate_byte(status, "power-saving mode status")
        )
        power_saving_mode_status_value_to_name(value)
        response = self.transact(
            POWER_SAVING_MODE_STATUS_SET_COMMAND,
            value,
            expected_response_commands=(0x00,),
            expected_response_sizes=(6,),
        )
        require_ack(response)

    def get_apm_status(self) -> str:
        return decode_apm_status_report(
            self.transact(
                APM_STATUS_GET_COMMAND,
                expected_response_commands=(APM_STATUS_GET_COMMAND,),
                expected_response_sizes=(6,),
            )
        )

    def set_apm_status(self, status: str | int) -> None:
        value = (
            apm_status_name_to_value(status)
            if isinstance(status, str)
            else validate_byte(status, "APM status")
        )
        apm_status_value_to_name(value)
        response = self.transact(
            APM_STATUS_SET_COMMAND,
            value,
            expected_response_commands=(0x00,),
            expected_response_sizes=(6,),
        )
        require_ack(response)

    def get_serial_code(self) -> str:
        return decode_serial_code_report(
            self.transact(
                SERIAL_CODE_GET_COMMAND,
                expected_response_commands=(SERIAL_CODE_GET_COMMAND,),
                expected_response_sizes=(19,),
            )
        )

    def get_light_sensor(self) -> str:
        return decode_light_sensor_report(
            self.transact(
                LIGHT_SENSOR_GET_COMMAND,
                expected_response_commands=(LIGHT_SENSOR_GET_COMMAND,),
                expected_response_sizes=(6,),
            )
        )

    def set_light_sensor(self, state: str | int) -> None:
        value = (
            light_sensor_name_to_value(state)
            if isinstance(state, str)
            else validate_byte(state, "light sensor")
        )
        if value not in LIGHT_SENSOR_SET_NAMES:
            raise ValueError(f"unknown light-sensor state value: 0x{value:02X}")
        response = self.transact(
            LIGHT_SENSOR_SET_COMMAND,
            value,
            expected_response_commands=(0x00,),
            expected_response_sizes=(6,),
        )
        require_ack(response)

    def get_osd_rotating(self) -> str:
        return decode_osd_rotating_report(
            self.transact(
                OSD_ROTATING_GET_COMMAND,
                expected_response_commands=(OSD_ROTATING_GET_COMMAND,),
                expected_response_sizes=(6,),
            )
        )

    def set_osd_rotating(self, state: str | int) -> None:
        value = (
            osd_rotating_name_to_value(state)
            if isinstance(state, str)
            else validate_byte(state, "OSD rotating")
        )
        osd_rotating_value_to_name(value)
        response = self.transact(
            OSD_ROTATING_SET_COMMAND,
            value,
            expected_response_commands=(0x00,),
            expected_response_sizes=(6,),
        )
        require_ack(response)

    def get_display_orientation(self) -> DisplayOrientationState:
        return decode_display_orientation_report(
            self.transact(
                DISPLAY_ORIENTATION_GET_COMMAND,
                expected_response_commands=(DISPLAY_ORIENTATION_GET_COMMAND,),
                expected_response_sizes=(12,),
            )
        )

    def set_display_orientation(
        self,
        auto_rotate: str | int,
        osd_rotation: str | int,
        image_all: str | int,
        window1: str | int,
        window2: str | int,
        window3: str | int,
        window4: str | int,
    ) -> None:
        values = (
            display_orientation_auto_rotate_name_to_value(auto_rotate)
            if isinstance(auto_rotate, str)
            else auto_rotate,
            display_orientation_osd_rotation_name_to_value(osd_rotation)
            if isinstance(osd_rotation, str)
            else osd_rotation,
            display_orientation_image_all_name_to_value(image_all)
            if isinstance(image_all, str)
            else image_all,
            display_orientation_window_name_to_value(window1, label="window1")
            if isinstance(window1, str)
            else window1,
            display_orientation_window_name_to_value(window2, label="window2")
            if isinstance(window2, str)
            else window2,
            display_orientation_window_name_to_value(window3, label="window3")
            if isinstance(window3, str)
            else window3,
            display_orientation_window_name_to_value(window4, label="window4")
            if isinstance(window4, str)
            else window4,
        )
        values = validate_display_orientation_values(*values)
        response = self.transact(
            DISPLAY_ORIENTATION_SET_COMMAND,
            *values,
            expected_response_commands=(0x00,),
            expected_response_sizes=(6,),
        )
        require_ack(response)

    def get_touch_feature(self) -> str:
        return decode_touch_feature_report(
            self.transact(
                TOUCH_FEATURE_GET_COMMAND,
                expected_response_commands=(TOUCH_FEATURE_GET_COMMAND,),
                expected_response_sizes=(6,),
            )
        )

    def set_touch_feature(self, state: str | int) -> None:
        value = (
            touch_feature_name_to_value(state)
            if isinstance(state, str)
            else validate_byte(state, "touch feature")
        )
        touch_feature_value_to_name(value)
        response = self.transact(
            TOUCH_FEATURE_SET_COMMAND,
            value,
            expected_response_commands=(0x00,),
            expected_response_sizes=(6,),
        )
        require_ack(response)

    def get_noise_reduction(self) -> str:
        return decode_noise_reduction_report(
            self.transact(
                NOISE_REDUCTION_GET_COMMAND,
                expected_response_commands=(NOISE_REDUCTION_GET_COMMAND,),
                expected_response_sizes=(6,),
            )
        )

    def set_noise_reduction(self, level: str | int) -> None:
        value = (
            noise_reduction_name_to_value(level)
            if isinstance(level, str)
            else validate_byte(level, "noise reduction")
        )
        noise_reduction_value_to_name(value)
        response = self.transact(
            NOISE_REDUCTION_SET_COMMAND,
            value,
            expected_response_commands=(0x00,),
            expected_response_sizes=(6,),
        )
        require_ack(response)

    def get_scan_mode(self) -> str:
        return decode_scan_mode_report(
            self.transact(
                SCAN_MODE_GET_COMMAND,
                expected_response_commands=(SCAN_MODE_GET_COMMAND,),
                expected_response_sizes=(6,),
            )
        )

    def set_scan_mode(self, mode: str | int) -> None:
        value = (
            scan_mode_name_to_value(mode)
            if isinstance(mode, str)
            else validate_byte(mode, "scan mode")
        )
        scan_mode_value_to_name(value)
        response = self.transact(
            SCAN_MODE_SET_COMMAND,
            value,
            expected_response_commands=(0x00,),
            expected_response_sizes=(6,),
        )
        require_ack(response)

    def get_scan_conversion(self) -> str:
        return decode_scan_conversion_report(
            self.transact(
                SCAN_CONVERSION_GET_COMMAND,
                expected_response_commands=(SCAN_CONVERSION_GET_COMMAND,),
                expected_response_sizes=(6,),
            )
        )

    def set_scan_conversion(self, mode: str | int) -> None:
        value = (
            scan_conversion_name_to_value(mode)
            if isinstance(mode, str)
            else validate_byte(mode, "scan conversion")
        )
        scan_conversion_value_to_name(value)
        response = self.transact(
            SCAN_CONVERSION_SET_COMMAND,
            value,
            expected_response_commands=(0x00,),
            expected_response_sizes=(6,),
        )
        require_ack(response)

    def get_pixel_shift(self) -> str:
        return decode_pixel_shift_report(
            self.transact(
                PIXEL_SHIFT_GET_COMMAND,
                expected_response_commands=(PIXEL_SHIFT_GET_COMMAND,),
                expected_response_sizes=(6,),
            )
        )

    def set_pixel_shift(self, value: str | int) -> None:
        shift_value = (
            pixel_shift_name_to_value(value)
            if isinstance(value, str)
            else validate_byte(value, "pixel shift")
        )
        pixel_shift_value_to_name(shift_value)
        response = self.transact(
            PIXEL_SHIFT_SET_COMMAND,
            shift_value,
            expected_response_commands=(0x00,),
            expected_response_sizes=(6,),
        )
        require_ack(response)

    def get_memc_effect(self) -> str:
        return decode_memc_effect_report(
            self.transact(
                MEMC_EFFECT_GET_COMMAND,
                expected_response_commands=(MEMC_EFFECT_GET_COMMAND,),
                expected_response_sizes=(6,),
            )
        )

    def set_memc_effect(self, level: str | int) -> None:
        value = (
            memc_effect_name_to_value(level)
            if isinstance(level, str)
            else validate_byte(level, "MEMC effect")
        )
        memc_effect_value_to_name(value)
        response = self.transact(
            MEMC_EFFECT_SET_COMMAND,
            value,
            expected_response_commands=(0x00,),
            expected_response_sizes=(6,),
        )
        require_ack(response)

    def get_information_osd(self) -> int:
        return decode_information_osd_report(
            self.transact(
                INFORMATION_OSD_GET_COMMAND,
                expected_response_commands=(INFORMATION_OSD_GET_COMMAND,),
                expected_response_sizes=(6,),
            )
        )

    def set_information_osd(self, value: str | int) -> None:
        osd_value = (
            information_osd_name_to_value(value)
            if isinstance(value, str)
            else validate_information_osd_value(value)
        )
        response = self.transact(
            INFORMATION_OSD_SET_COMMAND,
            osd_value,
            expected_response_commands=(0x00,),
            expected_response_sizes=(6,),
        )
        require_ack(response)

    def get_human_sensor(self) -> str:
        return decode_human_sensor_report(
            self.transact(
                HUMAN_SENSOR_GET_COMMAND,
                expected_response_commands=(HUMAN_SENSOR_GET_COMMAND,),
                expected_response_sizes=(6,),
            )
        )

    def set_human_sensor(self, state: str | int) -> None:
        value = (
            human_sensor_name_to_value(state)
            if isinstance(state, str)
            else validate_byte(state, "human sensor")
        )
        if value not in HUMAN_SENSOR_SET_NAMES:
            raise ValueError(f"unknown human-sensor state value: 0x{value:02X}")
        response = self.transact(
            HUMAN_SENSOR_SET_COMMAND,
            value,
            expected_response_commands=(0x00,),
            expected_response_sizes=(6,),
        )
        require_ack(response)

    def factory_reset(self) -> None:
        response = self.transact(
            FACTORY_RESET_COMMAND,
            expected_response_commands=(0x00,),
            expected_response_sizes=(6,),
        )
        require_ack(response)

    def get_power_on_logo(self) -> str:
        return decode_power_on_logo_report(
            self.transact(
                POWER_ON_LOGO_GET_COMMAND,
                expected_response_commands=(POWER_ON_LOGO_GET_COMMAND,),
                expected_response_sizes=(6,),
            )
        )

    def set_power_on_logo(self, state: str | int) -> None:
        value = (
            power_on_logo_name_to_value(state)
            if isinstance(state, str)
            else validate_byte(state, "power-on logo")
        )
        power_on_logo_value_to_name(value)
        response = self.transact(
            POWER_ON_LOGO_SET_COMMAND,
            value,
            expected_response_commands=(0x00,),
            expected_response_sizes=(6,),
        )
        require_ack(response)

    def get_off_timer(self) -> int:
        return decode_off_timer_report(
            self.transact(
                OFF_TIMER_GET_COMMAND,
                expected_response_commands=(OFF_TIMER_GET_COMMAND,),
                expected_response_sizes=(6,),
            )
        )

    def set_off_timer(self, hours: str | int) -> None:
        value = off_timer_name_to_value(hours) if isinstance(hours, str) else hours
        value = validate_off_timer_hours(value)
        response = self.transact(
            OFF_TIMER_SET_COMMAND,
            value,
            expected_response_commands=(0x00,),
            expected_response_sizes=(6,),
        )
        require_ack(response)

    def get_eco_mode(self) -> str:
        return decode_eco_mode_report(
            self.transact(
                ECO_MODE_GET_COMMAND,
                expected_response_commands=(ECO_MODE_GET_COMMAND,),
                expected_response_sizes=(6,),
            )
        )

    def set_eco_mode(self, mode: str | int) -> None:
        value = (
            eco_mode_name_to_value(mode)
            if isinstance(mode, str)
            else validate_byte(mode, "ECO mode")
        )
        eco_mode_value_to_name(value)
        response = self.transact(
            ECO_MODE_SET_COMMAND,
            value,
            expected_response_commands=(0x00,),
            expected_response_sizes=(6,),
        )
        require_ack(response)

    def get_picture_style(self) -> str:
        return decode_picture_style_report(
            self.transact(
                PICTURE_STYLE_GET_COMMAND,
                expected_response_commands=(PICTURE_STYLE_GET_COMMAND,),
                expected_response_sizes=(6,),
            )
        )

    def set_picture_style(self, style: str | int) -> None:
        value = (
            picture_style_name_to_value(style)
            if isinstance(style, str)
            else validate_byte(style, "picture style")
        )
        picture_style_value_to_name(value)
        response = self.transact(
            PICTURE_STYLE_SET_COMMAND,
            value,
            expected_response_commands=(0x00,),
            expected_response_sizes=(6,),
        )
        require_ack(response)

    def get_group_id(self) -> int | None:
        return decode_group_id_report(
            self.transact(
                GROUP_ID_GET_COMMAND,
                expected_response_commands=(GROUP_ID_GET_COMMAND,),
                expected_response_sizes=(6,),
            )
        )

    def set_group_id(self, group_id: str | int) -> None:
        value = (
            group_id_name_to_value(group_id)
            if isinstance(group_id, str)
            else validate_byte(group_id, "group ID")
        )
        group_id_value_to_id(value)
        response = self.transact(
            GROUP_ID_SET_COMMAND,
            value,
            expected_response_commands=(0x00,),
            expected_response_sizes=(6,),
        )
        require_ack(response)

    def set_monitor_id(self, monitor_id: str | int) -> None:
        value = (
            monitor_id_name_to_value(monitor_id)
            if isinstance(monitor_id, str)
            else validate_monitor_id_value(monitor_id)
        )
        response = self.transact(
            MONITOR_ID_SET_COMMAND,
            value,
            expected_response_commands=(0x00,),
            expected_response_sizes=(6,),
        )
        require_ack(response)

    def get_ports_lock(self) -> str:
        return decode_ports_lock_report(
            self.transact(
                PORTS_LOCK_GET_COMMAND,
                expected_response_commands=(PORTS_LOCK_GET_COMMAND,),
                expected_response_sizes=(6,),
            )
        )

    def set_ports_lock(self, state: str | int) -> None:
        value = (
            ports_lock_name_to_value(state)
            if isinstance(state, str)
            else validate_byte(state, "ports-lock state")
        )
        ports_lock_value_to_name(value)
        response = self.transact(
            PORTS_LOCK_SET_COMMAND,
            value,
            expected_response_commands=(0x00,),
            expected_response_sizes=(6,),
        )
        require_ack(response)

    def _recv_packet(
        self,
        sock: socket.socket,
        expected_response_commands: tuple[int, ...] | None = None,
        expected_response_sizes: tuple[int, ...] | None = None,
    ) -> _ReceiveResult:
        buffer = bytearray()
        last_parse_error: ValueError | None = None
        skipped: list[SicpPacket] = []
        pending_unmatched: list[SicpPacket] = []

        while True:
            try:
                chunk = sock.recv(1024)
            except TimeoutError as exc:
                if pending_unmatched:
                    raise SicpProtocolError(
                        "Timed out waiting for expected response; saw "
                        f"{format_packet_list(pending_unmatched)}"
                    ) from exc
                if last_parse_error is not None or buffer:
                    raise ConnectionError(
                        f"Timed out before a valid packet was received; "
                        f"buffer={hex_bytes(bytes(buffer))}; last error: "
                        f"{last_parse_error}"
                    ) from exc
                if skipped:
                    raise SicpProtocolError(
                        "Timed out waiting for expected response; skipped "
                        f"{format_packet_list(skipped)}"
                    ) from exc
                raise
            if not chunk:
                if pending_unmatched:
                    raise SicpProtocolError(
                        "Connection closed before expected response; saw "
                        f"{format_packet_list(pending_unmatched)}"
                    )
                if skipped:
                    raise SicpProtocolError(
                        "Connection closed before expected response; skipped "
                        f"{format_packet_list(skipped)}"
                    )
                if last_parse_error is not None:
                    raise ConnectionError(
                        f"Connection closed before a valid packet was received; "
                        f"buffer={hex_bytes(bytes(buffer))}; last error: "
                        f"{last_parse_error}"
                    )
                raise ConnectionError("Connection closed before packet header")
            buffer.extend(chunk)

            packet, newly_skipped, last_parse_error = self._extract_matching_packet(
                buffer,
                expected_response_commands=expected_response_commands,
                expected_response_sizes=expected_response_sizes,
            )
            if packet is not None:
                skipped.extend(newly_skipped)
                return _ReceiveResult(packet=packet, skipped=tuple(skipped))
            pending_unmatched = newly_skipped

    def _extract_matching_packet(
        self,
        buffer: bytearray,
        expected_response_commands: tuple[int, ...] | None = None,
        expected_response_sizes: tuple[int, ...] | None = None,
    ) -> tuple[SicpPacket | None, list[SicpPacket], ValueError | None]:
        last_parse_error = None
        candidates: list[tuple[int, int, SicpPacket]] = []
        for offset in range(len(buffer)):
            msg_size = buffer[offset]
            if msg_size < 4:
                continue
            if (
                expected_response_sizes is not None
                and msg_size not in expected_response_sizes
            ):
                continue
            packet_end = offset + msg_size
            if len(buffer) < packet_end:
                continue

            candidate = bytes(buffer[offset:packet_end])
            try:
                packet = parse_packet(candidate)
            except ValueError as exc:
                last_parse_error = exc
                continue

            candidates.append((offset, packet_end, packet))

        if not candidates:
            return None, [], last_parse_error

        if expected_response_commands is None:
            offset, packet_end, packet = candidates[0]
            del buffer[:packet_end]
            return packet, [], None

        for offset, packet_end, packet in candidates:
            if not packet.command_matches(expected_response_commands):
                continue

            skipped = [
                candidate
                for candidate_offset, candidate_end, candidate in candidates
                if candidate_end <= offset
                and not candidate.command_matches(expected_response_commands)
            ]
            del buffer[:packet_end]
            return packet, skipped, None

        # Keep the bytes. A later recv may complete an overlapping expected
        # packet that starts inside a currently valid but unrelated frame.
        return None, [candidate for _, _, candidate in candidates], last_parse_error


def format_packet_list(packets: list[SicpPacket]) -> str:
    return ", ".join(
        f"{packet.raw_hex} (command={format_command(packet.command)})"
        for packet in packets
    )


def format_command(command: int | None) -> str:
    return "None" if command is None else f"0x{command:02X}"
