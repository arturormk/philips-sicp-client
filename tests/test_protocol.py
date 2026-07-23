import unittest

from philips_sicp.client import (
    SicpAckError,
    SicpClient,
    SicpNackError,
    SicpNavError,
    SicpProtocolError,
    anytile_resolution_name_to_value,
    anytile_resolution_value_to_name,
    apm_status_name_to_value,
    apm_status_value_to_name,
    audio_parameter_value_to_display,
    build_anytile_parameters,
    build_input_source_osd_style,
    build_tiling_set_values,
    color_temperature_name_to_value,
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
    decode_tiling_wall_size,
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
    fan_speed_name_to_value,
    gamma_name_to_value,
    group_id_name_to_value,
    group_id_value_to_name,
    human_sensor_name_to_value,
    information_osd_name_to_value,
    information_osd_value_to_name,
    input_source_name_to_value,
    light_sensor_name_to_value,
    lock_state_name_to_value,
    memc_effect_name_to_value,
    memc_effect_value_to_name,
    monitor_id_name_to_value,
    monitor_restart_target_name_to_value,
    mute_value_to_bool,
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
    power_saving_mode_name_to_value,
    power_saving_mode_status_name_to_value,
    power_saving_mode_status_value_to_name,
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
    validate_audio_parameter,
    validate_color_temperature_100k_steps,
    validate_display_orientation_values,
    validate_failover_priorities,
    validate_percentage,
    validate_scheduling_page,
    validate_volume_level,
    validate_volume_limits,
    volume_step_name_to_value,
    volume_step_value_to_name,
)
from philips_sicp.protocol import build_packet, parse_packet


class FakeSocket:
    def __init__(self, chunks):
        self.chunks = list(chunks)

    def recv(self, _size):
        if self.chunks:
            return self.chunks.pop(0)
        return b""


class ProtocolTests(unittest.TestCase):
    def test_get_power_packet(self):
        self.assertEqual(build_packet(0x19), bytes.fromhex("05 01 00 19 1D"))

    def test_set_power_off_packet(self):
        self.assertEqual(build_packet(0x18, 0x01), bytes.fromhex("06 01 00 18 01 1E"))

    def test_set_power_on_packet(self):
        self.assertEqual(build_packet(0x18, 0x02), bytes.fromhex("06 01 00 18 02 1D"))

    def test_get_power_cold_start_packet(self):
        self.assertEqual(build_packet(0xA4), bytes.fromhex("05 01 00 A4 A0"))

    def test_set_power_cold_start_packets(self):
        self.assertEqual(build_packet(0xA3, 0x00), bytes.fromhex("06 01 00 A3 00 A4"))
        self.assertEqual(build_packet(0xA3, 0x01), bytes.fromhex("06 01 00 A3 01 A5"))
        self.assertEqual(build_packet(0xA3, 0x02), bytes.fromhex("06 01 00 A3 02 A6"))

    def test_get_input_source_packet(self):
        self.assertEqual(build_packet(0xAD), bytes.fromhex("05 01 00 AD A9"))

    def test_set_input_source_packet(self):
        self.assertEqual(
            build_packet(0xAC, 0x0D, 0x00, 0x01, 0x00),
            bytes.fromhex("09 01 00 AC 0D 00 01 00 A8"),
        )

    def test_set_input_source_packet_with_do_not_switch(self):
        self.assertEqual(
            build_packet(0xAC, 0x0D, 0x00, 0x41, 0x00),
            bytes.fromhex("09 01 00 AC 0D 00 41 00 E8"),
        )

    def test_auto_signal_packets(self):
        self.assertEqual(build_packet(0xAF), bytes.fromhex("05 01 00 AF AB"))
        self.assertEqual(build_packet(0xAE, 0x00), bytes.fromhex("06 01 00 AE 00 A9"))
        self.assertEqual(build_packet(0xAE, 0x05), bytes.fromhex("06 01 00 AE 05 AC"))

    def test_failover_packets(self):
        self.assertEqual(build_packet(0xA6), bytes.fromhex("05 01 00 A6 A2"))
        self.assertEqual(
            build_packet(0xA5, 0x00, 0x01, 0x02, 0x03),
            bytes.fromhex("09 01 00 A5 00 01 02 03 AD"),
        )

    def test_monitor_restart_packets(self):
        self.assertEqual(build_packet(0x57, 0x00), bytes.fromhex("06 01 00 57 00 50"))
        self.assertEqual(build_packet(0x57, 0x01), bytes.fromhex("06 01 00 57 01 51"))

    def test_temperature_packet(self):
        self.assertEqual(build_packet(0x2F), bytes.fromhex("05 01 00 2F 2B"))

    def test_fan_speed_packets(self):
        self.assertEqual(build_packet(0x62), bytes.fromhex("05 01 00 62 66"))
        self.assertEqual(build_packet(0x61, 0x00), bytes.fromhex("06 01 00 61 00 66"))
        self.assertEqual(build_packet(0x61, 0x04), bytes.fromhex("06 01 00 61 04 62"))

    def test_video_signal_present_packet(self):
        self.assertEqual(build_packet(0x59), bytes.fromhex("05 01 00 59 5D"))

    def test_lock_packets(self):
        self.assertEqual(build_packet(0x1D), bytes.fromhex("05 01 00 1D 19"))
        self.assertEqual(build_packet(0x1C, 0x03), bytes.fromhex("06 01 00 1C 03 18"))
        self.assertEqual(build_packet(0x1B), bytes.fromhex("05 01 00 1B 1F"))
        self.assertEqual(build_packet(0x1A, 0x02), bytes.fromhex("06 01 00 1A 02 1F"))

    def test_video_parameter_packets(self):
        self.assertEqual(build_packet(0x33), bytes.fromhex("05 01 00 33 37"))
        self.assertEqual(
            build_packet(0x32, 0x37, 0x37, 0x37, 0x37, 0x37, 0x37, 0x03),
            bytes.fromhex("0C 01 00 32 37 37 37 37 37 37 03 3C"),
        )
        self.assertEqual(build_packet(0x35), bytes.fromhex("05 01 00 35 31"))
        self.assertEqual(build_packet(0x34, 0x01), bytes.fromhex("06 01 00 34 01 32"))
        self.assertEqual(build_packet(0x37), bytes.fromhex("05 01 00 37 33"))
        self.assertEqual(
            build_packet(0x36, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF),
            bytes.fromhex("0B 01 00 36 FF FF FF FF FF FF 3C"),
        )
        self.assertEqual(build_packet(0x12), bytes.fromhex("05 01 00 12 16"))
        self.assertEqual(build_packet(0x11, 0x64), bytes.fromhex("06 01 00 11 64 72"))

    def test_picture_format_packets(self):
        self.assertEqual(build_packet(0x3B), bytes.fromhex("05 01 00 3B 3F"))
        self.assertEqual(build_packet(0x3A, 0x03), bytes.fromhex("06 01 00 3A 03 3E"))
        self.assertEqual(build_packet(0x3A, 0x06), bytes.fromhex("06 01 00 3A 06 3B"))

    def test_volume_packets(self):
        self.assertEqual(build_packet(0x45), bytes.fromhex("05 01 00 45 41"))
        self.assertEqual(
            build_packet(0x44, 0x16, 0x32), bytes.fromhex("07 01 00 44 16 32 66")
        )
        self.assertEqual(build_packet(0x44, 0x16), bytes.fromhex("06 01 00 44 16 55"))
        self.assertEqual(
            build_packet(0x41, 0x01, 0x00), bytes.fromhex("07 01 00 41 01 00 46")
        )
        self.assertEqual(build_packet(0x41, 0x00), bytes.fromhex("06 01 00 41 00 46"))
        self.assertEqual(build_packet(0x41, 0x01), bytes.fromhex("06 01 00 41 01 47"))
        self.assertEqual(
            build_packet(0xB8, 0x0A, 0x4D, 0x32),
            bytes.fromhex("08 01 00 B8 0A 4D 32 C4"),
        )
        self.assertEqual(
            build_packet(0xB6, 0x0A, 0x4D, 0x32),
            bytes.fromhex("08 01 00 B6 0A 4D 32 CA"),
        )
        self.assertEqual(
            build_packet(0xB9, 0x0A, 0x4D, 0x32),
            bytes.fromhex("08 01 00 B9 0A 4D 32 C5"),
        )
        self.assertEqual(
            build_packet(0xB7, 0x0A, 0x4D, 0x32),
            bytes.fromhex("08 01 00 B7 0A 4D 32 CB"),
        )
        self.assertEqual(build_packet(0x43), bytes.fromhex("05 01 00 43 47"))
        self.assertEqual(
            build_packet(0x42, 0x4D, 0x4D), bytes.fromhex("07 01 00 42 4D 4D 44")
        )
        self.assertEqual(build_packet(0x46), bytes.fromhex("05 01 00 46 42"))
        self.assertEqual(build_packet(0x47, 0x00), bytes.fromhex("06 01 00 47 00 40"))

    def test_operating_hours_packet(self):
        self.assertEqual(build_packet(0x0F, 0x02), bytes.fromhex("06 01 00 0F 02 0A"))

    def test_tiling_packets(self):
        self.assertEqual(build_packet(0x23), bytes.fromhex("05 01 00 23 27"))
        self.assertEqual(
            build_packet(0x23, 0x01, 0x00, 0x02, 0x12),
            bytes.fromhex("09 01 00 23 01 00 02 12 3A"),
        )
        self.assertEqual(
            build_packet(0x23, 0x01, 0x00, 0x02, 0x08),
            bytes.fromhex("09 01 00 23 01 00 02 08 20"),
        )
        self.assertEqual(
            build_packet(0x22, 0x01, 0x00, 0x02, 0x12),
            bytes.fromhex("09 01 00 22 01 00 02 12 3B"),
        )
        self.assertEqual(
            build_packet(0x22, 0x01, 0x02, 0x00, 0x00),
            bytes.fromhex("09 01 00 22 01 02 00 00 29"),
        )
        self.assertEqual(
            build_packet(0x22, 0x01, 0x00, 0x02, 0x08),
            bytes.fromhex("09 01 00 22 01 00 02 08 21"),
        )

    def test_switch_on_delay_packets(self):
        self.assertEqual(build_packet(0x55), bytes.fromhex("05 01 00 55 51"))
        self.assertEqual(build_packet(0x54, 0x00), bytes.fromhex("06 01 00 54 00 53"))
        self.assertEqual(build_packet(0x54, 0x01), bytes.fromhex("06 01 00 54 01 52"))
        self.assertEqual(build_packet(0x54, 0x14), bytes.fromhex("06 01 00 54 14 47"))

    def test_frame_compensation_packets(self):
        self.assertEqual(build_packet(0x5E), bytes.fromhex("05 01 00 5E 5A"))
        self.assertEqual(build_packet(0x5E, 0x03), bytes.fromhex("06 01 00 5E 03 5A"))
        self.assertEqual(build_packet(0x5F, 0x00), bytes.fromhex("06 01 00 5F 00 58"))
        self.assertEqual(build_packet(0x5F, 0x03), bytes.fromhex("06 01 00 5F 03 5B"))
        self.assertEqual(build_packet(0x67), bytes.fromhex("05 01 00 67 63"))
        self.assertEqual(build_packet(0x67, 0x03), bytes.fromhex("06 01 00 67 03 63"))
        self.assertEqual(build_packet(0x68, 0x00), bytes.fromhex("06 01 00 68 00 6F"))
        self.assertEqual(build_packet(0x68, 0x03), bytes.fromhex("06 01 00 68 03 6C"))

    def test_anytile_packets(self):
        parameters = build_anytile_parameters(1, 90, 0, 0, 1920, 1080)
        self.assertEqual(build_packet(0x4A), bytes.fromhex("05 01 00 4A 4E"))
        self.assertEqual(
            build_packet(0x4B, *parameters),
            bytes.fromhex("10 01 00 4B 01 5A 00 00 00 00 00 80 07 38 04 BA"),
        )
        self.assertEqual(build_packet(0x4E), bytes.fromhex("05 01 00 4E 4A"))
        self.assertEqual(build_packet(0x4F, 0x02), bytes.fromhex("06 01 00 4F 02 4A"))
        self.assertEqual(
            build_packet(0xC0, 0x03, 0x04), bytes.fromhex("07 01 00 C0 03 04 C1")
        )
        self.assertEqual(build_packet(0x4C, 0x03), bytes.fromhex("06 01 00 4C 03 48"))

    def test_power_saving_mode_set_packets(self):
        self.assertEqual(build_packet(0xDE), bytes.fromhex("05 01 00 DE DA"))
        self.assertEqual(build_packet(0xDD, 0x00), bytes.fromhex("06 01 00 DD 00 DA"))
        self.assertEqual(build_packet(0xDD, 0x01), bytes.fromhex("06 01 00 DD 01 DB"))
        self.assertEqual(build_packet(0xDD, 0x02), bytes.fromhex("06 01 00 DD 02 D8"))
        self.assertEqual(build_packet(0xDD, 0x03), bytes.fromhex("06 01 00 DD 03 D9"))

    def test_power_saving_mode_status_packets(self):
        self.assertEqual(build_packet(0xD3), bytes.fromhex("05 01 00 D3 D7"))
        self.assertEqual(build_packet(0xD2, 0x00), bytes.fromhex("06 01 00 D2 00 D5"))
        self.assertEqual(build_packet(0xD2, 0x07), bytes.fromhex("06 01 00 D2 07 D2"))

    def test_apm_status_packets(self):
        self.assertEqual(build_packet(0xD1), bytes.fromhex("05 01 00 D1 D5"))
        self.assertEqual(build_packet(0xD0, 0x00), bytes.fromhex("06 01 00 D0 00 D7"))
        self.assertEqual(build_packet(0xD0, 0x03), bytes.fromhex("06 01 00 D0 03 D4"))

    def test_eco_mode_packets(self):
        self.assertEqual(build_packet(0x63), bytes.fromhex("05 01 00 63 67"))
        self.assertEqual(build_packet(0x64, 0x00), bytes.fromhex("06 01 00 64 00 63"))
        self.assertEqual(build_packet(0x64, 0x01), bytes.fromhex("06 01 00 64 01 62"))

    def test_picture_style_packets(self):
        self.assertEqual(build_packet(0x65), bytes.fromhex("05 01 00 65 61"))
        self.assertEqual(build_packet(0x66, 0x00), bytes.fromhex("06 01 00 66 00 61"))
        self.assertEqual(build_packet(0x66, 0x0A), bytes.fromhex("06 01 00 66 0A 6B"))

    def test_group_id_packets(self):
        self.assertEqual(build_packet(0x5D), bytes.fromhex("05 01 00 5D 59"))
        self.assertEqual(build_packet(0x5C, 0x01), bytes.fromhex("06 01 00 5C 01 5A"))
        self.assertEqual(build_packet(0x5C, 0xFF), bytes.fromhex("06 01 00 5C FF A4"))

    def test_monitor_id_packets(self):
        self.assertEqual(
            build_packet(0x69, 0x06, monitor_id=0x03),
            bytes.fromhex("06 03 00 69 06 6A"),
        )
        self.assertEqual(build_packet(0x69, 0xFF), bytes.fromhex("06 01 00 69 FF 91"))

    def test_ports_lock_packets(self):
        self.assertEqual(build_packet(0xF2), bytes.fromhex("05 01 00 F2 F6"))
        self.assertEqual(build_packet(0xF1, 0x00), bytes.fromhex("06 01 00 F1 00 F6"))
        self.assertEqual(build_packet(0xF1, 0x01), bytes.fromhex("06 01 00 F1 01 F7"))

    def test_scheduling_packets(self):
        self.assertEqual(build_packet(0x5B, 0x01), bytes.fromhex("06 01 00 5B 01 5D"))
        self.assertEqual(
            build_packet(0x5A, 0x10, 0x06, 0x1E, 0x16, 0x00, 0x0A, 0xFF),
            bytes.fromhex("0C 01 00 5A 10 06 1E 16 00 0A FF BC"),
        )
        self.assertEqual(
            build_packet(0x5A, 0x11, 0x18, 0x3C, 0x18, 0x3C, 0x00, 0x00, 0x07),
            bytes.fromhex("0D 01 00 5A 11 18 3C 18 3C 00 00 07 40"),
        )

    def test_serial_code_packet(self):
        self.assertEqual(build_packet(0x15), bytes.fromhex("05 01 00 15 11"))

    def test_light_sensor_packets(self):
        self.assertEqual(build_packet(0x25), bytes.fromhex("05 01 00 25 21"))
        self.assertEqual(build_packet(0x24, 0x00), bytes.fromhex("06 01 00 24 00 23"))
        self.assertEqual(build_packet(0x24, 0x01), bytes.fromhex("06 01 00 24 01 22"))

    def test_osd_rotating_packets(self):
        self.assertEqual(build_packet(0x27), bytes.fromhex("05 01 00 27 23"))
        self.assertEqual(build_packet(0x26, 0x00), bytes.fromhex("06 01 00 26 00 21"))
        self.assertEqual(build_packet(0x26, 0x01), bytes.fromhex("06 01 00 26 01 20"))

    def test_display_orientation_packets(self):
        self.assertEqual(build_packet(0x16), bytes.fromhex("05 01 00 16 12"))
        self.assertEqual(
            build_packet(0x17, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00),
            bytes.fromhex("0C 01 00 17 00 00 01 00 00 00 00 1B"),
        )
        self.assertEqual(
            build_packet(0x17, 0x01, 0x01, 0x03, 0x01, 0x01, 0x00, 0x00),
            bytes.fromhex("0C 01 00 17 01 01 03 01 01 00 00 19"),
        )

    def test_touch_feature_packets(self):
        self.assertEqual(build_packet(0x1F), bytes.fromhex("05 01 00 1F 1B"))
        self.assertEqual(build_packet(0x1E, 0x00), bytes.fromhex("06 01 00 1E 00 19"))
        self.assertEqual(build_packet(0x1E, 0x01), bytes.fromhex("06 01 00 1E 01 18"))

    def test_noise_reduction_packets(self):
        self.assertEqual(build_packet(0x2B), bytes.fromhex("05 01 00 2B 2F"))
        self.assertEqual(build_packet(0x2A, 0x00), bytes.fromhex("06 01 00 2A 00 2D"))
        self.assertEqual(build_packet(0x2A, 0x03), bytes.fromhex("06 01 00 2A 03 2E"))
        self.assertEqual(build_packet(0x2A, 0x04), bytes.fromhex("06 01 00 2A 04 29"))

    def test_scan_mode_packets(self):
        self.assertEqual(build_packet(0x51), bytes.fromhex("05 01 00 51 55"))
        self.assertEqual(build_packet(0x50, 0x00), bytes.fromhex("06 01 00 50 00 57"))
        self.assertEqual(build_packet(0x50, 0x01), bytes.fromhex("06 01 00 50 01 56"))
        self.assertEqual(build_packet(0x50, 0x1C), bytes.fromhex("06 01 00 50 1C 4B"))

    def test_scan_conversion_packets(self):
        self.assertEqual(build_packet(0x53), bytes.fromhex("05 01 00 53 57"))
        self.assertEqual(build_packet(0x52, 0x00), bytes.fromhex("06 01 00 52 00 55"))
        self.assertEqual(build_packet(0x52, 0x01), bytes.fromhex("06 01 00 52 01 54"))

    def test_pixel_shift_packets(self):
        self.assertEqual(build_packet(0xB1), bytes.fromhex("05 01 00 B1 B5"))
        self.assertEqual(build_packet(0xB2, 0x00), bytes.fromhex("06 01 00 B2 00 B5"))
        self.assertEqual(build_packet(0xB2, 0x05), bytes.fromhex("06 01 00 B2 05 B0"))
        self.assertEqual(build_packet(0xB2, 0x5B), bytes.fromhex("06 01 00 B2 5B EE"))

    def test_memc_effect_packets(self):
        self.assertEqual(build_packet(0x29), bytes.fromhex("05 01 00 29 2D"))
        self.assertEqual(build_packet(0x28, 0x00), bytes.fromhex("06 01 00 28 00 2F"))
        self.assertEqual(build_packet(0x28, 0x03), bytes.fromhex("06 01 00 28 03 2C"))

    def test_information_osd_packets(self):
        self.assertEqual(build_packet(0x2D), bytes.fromhex("05 01 00 2D 29"))
        self.assertEqual(build_packet(0x2C, 0x00), bytes.fromhex("06 01 00 2C 00 2B"))
        self.assertEqual(build_packet(0x2C, 0x3C), bytes.fromhex("06 01 00 2C 3C 17"))

    def test_human_sensor_packets(self):
        self.assertEqual(build_packet(0xB3), bytes.fromhex("05 01 00 B3 B7"))
        self.assertEqual(build_packet(0xB4, 0x00), bytes.fromhex("06 01 00 B4 00 B3"))
        self.assertEqual(build_packet(0xB4, 0x05), bytes.fromhex("06 01 00 B4 05 B6"))

    def test_factory_reset_packet(self):
        self.assertEqual(build_packet(0x56), bytes.fromhex("05 01 00 56 52"))

    def test_power_on_logo_packets(self):
        self.assertEqual(build_packet(0x3F), bytes.fromhex("05 01 00 3F 3B"))
        self.assertEqual(build_packet(0x3E, 0x00), bytes.fromhex("06 01 00 3E 00 39"))
        self.assertEqual(build_packet(0x3E, 0x02), bytes.fromhex("06 01 00 3E 02 3B"))

    def test_off_timer_packets(self):
        self.assertEqual(build_packet(0x91), bytes.fromhex("05 01 00 91 95"))
        self.assertEqual(build_packet(0x92, 0x00), bytes.fromhex("06 01 00 92 00 95"))
        self.assertEqual(build_packet(0x92, 0x05), bytes.fromhex("06 01 00 92 05 90"))

    def test_parse_power_on_report(self):
        packet = parse_packet(bytes.fromhex("06 01 00 19 02 1C"))
        self.assertEqual(packet.command, 0x19)
        self.assertEqual(packet.parameters, bytes([0x02]))
        self.assertTrue(decode_power_report(packet))

    def test_parse_observed_group_response(self):
        packet = parse_packet(bytes.fromhex("06 01 01 19 02 1D"))
        self.assertEqual(packet.monitor_id, 0x01)
        self.assertEqual(packet.group_id, 0x01)
        self.assertTrue(decode_power_report(packet))

    def test_parse_power_cold_start_report(self):
        packet = parse_packet(bytes.fromhex("06 01 00 A4 02 A1"))
        self.assertEqual(decode_power_cold_start_report(packet), "last")

    def test_parse_input_source_report(self):
        packet = parse_packet(bytes.fromhex("09 01 01 AD 0D 00 01 00 A8"))
        state = decode_input_source_report(packet)
        self.assertEqual(state.source, 0x0D)
        self.assertEqual(state.source_name, "hdmi")
        self.assertEqual(state.playlist, 0)
        self.assertEqual(state.osd_style, 0x01)
        self.assertFalse(state.do_not_switch)
        self.assertEqual(state.display_style, "source-label")
        self.assertEqual(state.mute_style, 0)

    def test_parse_auto_signal_report(self):
        packet = parse_packet(bytes.fromhex("06 01 00 AF 05 AD"))
        self.assertEqual(decode_auto_signal_report(packet), "failover")

    def test_parse_failover_report(self):
        packet = parse_packet(build_packet(0xA6, 0x00, 0x01, 0x02, 0x03))
        state = decode_failover_report(packet)
        self.assertEqual(state.priorities, (0x00, 0x01, 0x02, 0x03))
        self.assertEqual(
            state.priority_names,
            ("hdmi", "component", "composite", "display-port"),
        )

    def test_parse_temperature_report_two_sensors(self):
        packet = parse_packet(build_packet(0x2F, 0x1C, 0x1F))
        state = decode_temperature_report(packet)
        self.assertEqual(state.sensors_celsius, (28, 31))
        self.assertEqual(state.highest_celsius, 31)

    def test_parse_temperature_report_one_sensor(self):
        packet = parse_packet(build_packet(0x2F, 0x1C))
        state = decode_temperature_report(packet)
        self.assertEqual(state.sensors_celsius, (28,))
        self.assertEqual(state.highest_celsius, 28)

    def test_parse_fan_speed_report(self):
        self.assertEqual(
            decode_fan_speed_report(parse_packet(build_packet(0x62, 0x00))), "off"
        )
        self.assertEqual(
            decode_fan_speed_report(parse_packet(build_packet(0x62, 0x01))), "auto"
        )
        self.assertEqual(
            decode_fan_speed_report(parse_packet(build_packet(0x62, 0x02))), "low"
        )
        self.assertEqual(
            decode_fan_speed_report(parse_packet(build_packet(0x62, 0x03))), "middle"
        )
        self.assertEqual(
            decode_fan_speed_report(parse_packet(build_packet(0x62, 0x04))), "high"
        )

    def test_parse_video_signal_present_report(self):
        self.assertFalse(
            decode_video_signal_present_report(
                parse_packet(bytes.fromhex("06 01 00 59 00 5E"))
            )
        )
        self.assertTrue(
            decode_video_signal_present_report(
                parse_packet(bytes.fromhex("06 01 00 59 01 5F"))
            )
        )

    def test_parse_lock_reports(self):
        self.assertEqual(
            decode_ir_lock_report(parse_packet(bytes.fromhex("06 01 00 1D 01 1B"))),
            "unlock-all",
        )
        self.assertEqual(
            decode_ir_lock_report(parse_packet(build_packet(0x1D, 0x05))),
            "primary",
        )
        self.assertEqual(
            decode_keypad_lock_report(parse_packet(bytes.fromhex("06 01 00 1B 02 1E"))),
            "lock-all",
        )
        self.assertEqual(
            decode_keypad_lock_report(parse_packet(build_packet(0x1B, 0x07))),
            "lock-all-except-power-volume",
        )

    def test_parse_power_saving_mode_report(self):
        self.assertEqual(
            decode_power_saving_mode_report(
                parse_packet(bytes.fromhex("06 01 00 DE 01 D8"))
            ),
            "low",
        )
        self.assertEqual(
            decode_power_saving_mode_report(parse_packet(build_packet(0xDE, 0x03))),
            "high",
        )

    def test_parse_operating_hours_report(self):
        self.assertEqual(
            decode_operating_hours_report(
                parse_packet(bytes.fromhex("07 01 00 0F 4D 00 44"))
            ),
            0x4D00,
        )
        self.assertEqual(
            decode_operating_hours_report(parse_packet(build_packet(0x0F, 0x00, 0x2A))),
            42,
        )

    def test_parse_tiling_report(self):
        state = decode_tiling_report(
            parse_packet(bytes.fromhex("09 01 00 23 01 00 02 12 3A"))
        )
        self.assertTrue(state.enabled)
        self.assertFalse(state.frame_compensation)
        self.assertEqual(state.position, 2)
        self.assertEqual(state.wall_size, 0x12)
        self.assertEqual(state.standard_monitors, (3, 4))
        self.assertEqual(state.zero_bezel_monitors, (3, 2))

        standard = decode_tiling_report(parse_packet(build_packet(0x23, 1, 0, 2, 8)))
        self.assertEqual(standard.standard_monitors, (3, 2))

    def test_parse_switch_on_delay_report(self):
        self.assertEqual(
            decode_switch_on_delay_report(parse_packet(build_packet(0x55, 0x00))),
            0x00,
        )
        self.assertEqual(
            decode_switch_on_delay_report(parse_packet(build_packet(0x55, 0x01))),
            0x01,
        )
        self.assertEqual(
            decode_switch_on_delay_report(parse_packet(build_packet(0x55, 0x14))),
            0x14,
        )

    def test_parse_frame_compensation_reports(self):
        self.assertEqual(
            decode_frame_compensation_horizontal_report(
                parse_packet(build_packet(0x5E, 0x03))
            ),
            0x03,
        )
        self.assertEqual(
            decode_frame_compensation_vertical_report(
                parse_packet(build_packet(0x67, 0x04))
            ),
            0x04,
        )

    def test_parse_anytile_report(self):
        packet = parse_packet(
            build_packet(0x4A, *build_anytile_parameters(1, 90, 0, 0, 1920, 1080))
        )
        state = decode_anytile_report(packet)
        self.assertTrue(state.enabled)
        self.assertEqual(state.rotation, 90)
        self.assertEqual(state.input_h_start, 0)
        self.assertEqual(state.input_v_start, 0)
        self.assertEqual(state.input_h_size, 1920)
        self.assertEqual(state.input_v_size, 1080)
        self.assertEqual(
            state.to_dict(),
            {
                "enabled": True,
                "rotation": 90,
                "input_h_start": 0,
                "input_v_start": 0,
                "input_h_size": 1920,
                "input_v_size": 1080,
            },
        )

    def test_parse_anytile_resolution_report(self):
        self.assertEqual(
            decode_anytile_resolution_report(parse_packet(build_packet(0x4E, 0x00))),
            "default",
        )
        self.assertEqual(
            decode_anytile_resolution_report(parse_packet(build_packet(0x4E, 0x02))),
            "uhd4k",
        )

    def test_parse_power_saving_mode_status_report(self):
        self.assertEqual(
            decode_power_saving_mode_status_report(
                parse_packet(bytes.fromhex("06 01 00 D3 00 D4"))
            ),
            "rgb-off-video-off",
        )
        self.assertEqual(
            decode_power_saving_mode_status_report(
                parse_packet(build_packet(0xD3, 0x07))
            ),
            "mode-4",
        )

    def test_parse_apm_status_report(self):
        self.assertEqual(
            decode_apm_status_report(parse_packet(bytes.fromhex("06 01 00 D1 00 D6"))),
            "off",
        )
        self.assertEqual(
            decode_apm_status_report(parse_packet(build_packet(0xD1, 0x03))),
            "mode-2",
        )

    def test_parse_eco_mode_report(self):
        self.assertEqual(
            decode_eco_mode_report(parse_packet(bytes.fromhex("06 01 00 63 00 64"))),
            "low-power-standby",
        )
        self.assertEqual(
            decode_eco_mode_report(parse_packet(bytes.fromhex("06 01 00 63 01 65"))),
            "normal",
        )

    def test_parse_picture_style_report(self):
        self.assertEqual(
            decode_picture_style_report(
                parse_packet(bytes.fromhex("06 01 00 65 00 62"))
            ),
            "highbright",
        )
        self.assertEqual(
            decode_picture_style_report(
                parse_packet(bytes.fromhex("06 01 00 65 03 61"))
            ),
            "natural",
        )
        self.assertEqual(
            decode_picture_style_report(parse_packet(build_packet(0x65, 0x0A))),
            "user",
        )

    def test_parse_group_id_report(self):
        self.assertEqual(
            decode_group_id_report(parse_packet(bytes.fromhex("06 01 01 5D 01 5A"))),
            1,
        )
        self.assertEqual(
            decode_group_id_report(parse_packet(build_packet(0x5D, 0xFE))),
            254,
        )
        self.assertIsNone(
            decode_group_id_report(parse_packet(build_packet(0x5D, 0xFF)))
        )

    def test_parse_ports_lock_report(self):
        self.assertEqual(
            decode_ports_lock_report(parse_packet(bytes.fromhex("06 01 01 F2 00 F4"))),
            "unlocked",
        )
        self.assertEqual(
            decode_ports_lock_report(parse_packet(bytes.fromhex("06 01 01 F2 01 F5"))),
            "locked",
        )

    def test_parse_scheduling_report(self):
        state = decode_scheduling_report(
            parse_packet(bytes.fromhex("0C 01 00 5B 01 06 1E 16 00 0A FF AC"))
        )
        self.assertTrue(state.enabled)
        self.assertEqual(state.start_time, "06:30")
        self.assertEqual(state.end_time, "22:00")
        self.assertEqual(state.source_name, "display-port1")
        self.assertEqual(state.day_names, ("every-day",))
        self.assertIsNone(state.tag)

        tagged = decode_scheduling_report(
            parse_packet(
                build_packet(0x5B, 0x00, 0x18, 0x3C, 0x18, 0x3C, 0x00, 0x00, 0x07)
            )
        )
        self.assertFalse(tagged.enabled)
        self.assertIsNone(tagged.start_time)
        self.assertIsNone(tagged.end_time)
        self.assertEqual(tagged.source_name, "null")
        self.assertEqual(tagged.day_names, ("none",))
        self.assertEqual(tagged.tag_name, "tag-7")

        no_tag = decode_scheduling_report(
            parse_packet(
                build_packet(0x5B, 0x00, 0x18, 0x3C, 0x18, 0x3C, 0x00, 0x00, 0x00)
            )
        )
        self.assertIsNone(no_tag.tag)
        self.assertIsNone(no_tag.tag_name)

    def test_parse_serial_code_report(self):
        packet = parse_packet(
            bytes.fromhex("13 01 00 15 48 41 31 41 30 39 31 37 31 32 33 34 35 36 76")
        )
        self.assertEqual(decode_serial_code_report(packet), "HA1A0917123456")

    def test_parse_light_sensor_report(self):
        self.assertEqual(
            decode_light_sensor_report(
                parse_packet(bytes.fromhex("06 01 00 25 00 22"))
            ),
            "off",
        )
        self.assertEqual(
            decode_light_sensor_report(
                parse_packet(bytes.fromhex("06 01 00 25 01 23"))
            ),
            "on",
        )
        self.assertEqual(
            decode_light_sensor_report(parse_packet(build_packet(0x25, 0xFF))),
            "unavailable",
        )

    def test_parse_osd_rotating_report(self):
        self.assertEqual(
            decode_osd_rotating_report(
                parse_packet(bytes.fromhex("06 01 00 27 00 20"))
            ),
            "off",
        )
        self.assertEqual(
            decode_osd_rotating_report(
                parse_packet(bytes.fromhex("06 01 00 27 01 21"))
            ),
            "on",
        )

    def test_parse_display_orientation_report(self):
        state = decode_display_orientation_report(
            parse_packet(build_packet(0x16, 0x01, 0x01, 0x03, 0x01, 0x01, 0x00, 0x00))
        )
        self.assertEqual(state.auto_rotate, 0x01)
        self.assertEqual(state.auto_rotate_name, "on")
        self.assertEqual(state.osd_rotation, 0x01)
        self.assertEqual(state.osd_rotation_name, "portrait")
        self.assertEqual(state.image_all, 0x03)
        self.assertEqual(state.image_all_name, "counter-clockwise")
        self.assertEqual(state.window1_name, "on")
        self.assertEqual(state.window2_name, "on")
        self.assertEqual(state.window3_name, "off")
        self.assertEqual(state.window4_name, "off")

    def test_parse_touch_feature_report(self):
        self.assertEqual(
            decode_touch_feature_report(
                parse_packet(bytes.fromhex("06 01 00 1F 00 18"))
            ),
            "off",
        )
        self.assertEqual(
            decode_touch_feature_report(parse_packet(build_packet(0x1F, 0x01))),
            "on",
        )

    def test_parse_noise_reduction_report(self):
        self.assertEqual(
            decode_noise_reduction_report(
                parse_packet(bytes.fromhex("06 01 00 2B 00 2C"))
            ),
            "off",
        )
        self.assertEqual(
            decode_noise_reduction_report(parse_packet(build_packet(0x2B, 0x03))),
            "high",
        )
        self.assertEqual(
            decode_noise_reduction_report(parse_packet(build_packet(0x2B, 0x04))),
            "default",
        )

    def test_parse_scan_mode_report(self):
        self.assertEqual(
            decode_scan_mode_report(parse_packet(bytes.fromhex("06 01 00 51 00 56"))),
            "over-scan",
        )
        self.assertEqual(
            decode_scan_mode_report(parse_packet(build_packet(0x51, 0x01))),
            "under-scan",
        )
        self.assertEqual(
            decode_scan_mode_report(parse_packet(build_packet(0x51, 0x1C))),
            "custom-25",
        )

    def test_parse_scan_conversion_report(self):
        self.assertEqual(
            decode_scan_conversion_report(
                parse_packet(bytes.fromhex("06 01 00 53 00 54"))
            ),
            "progressive",
        )
        self.assertEqual(
            decode_scan_conversion_report(parse_packet(build_packet(0x53, 0x01))),
            "interlace",
        )

    def test_parse_pixel_shift_report(self):
        self.assertEqual(
            decode_pixel_shift_report(parse_packet(bytes.fromhex("06 01 00 B1 00 B6"))),
            "off",
        )
        self.assertEqual(
            decode_pixel_shift_report(parse_packet(bytes.fromhex("06 01 00 B1 03 B5"))),
            "30 seconds",
        )
        self.assertEqual(
            decode_pixel_shift_report(parse_packet(build_packet(0xB1, 0x5B))),
            "auto",
        )

    def test_parse_memc_effect_report(self):
        self.assertEqual(
            decode_memc_effect_report(parse_packet(bytes.fromhex("06 01 00 29 00 2E"))),
            "off",
        )
        self.assertEqual(
            decode_memc_effect_report(parse_packet(build_packet(0x29, 0x03))),
            "high",
        )

    def test_parse_information_osd_report(self):
        self.assertEqual(
            decode_information_osd_report(
                parse_packet(bytes.fromhex("06 01 00 2D 00 2A"))
            ),
            0,
        )
        self.assertEqual(
            decode_information_osd_report(parse_packet(build_packet(0x2D, 0x3C))),
            60,
        )

    def test_parse_human_sensor_report(self):
        self.assertEqual(
            decode_human_sensor_report(
                parse_packet(bytes.fromhex("06 01 00 B3 00 B4"))
            ),
            "off",
        )
        self.assertEqual(
            decode_human_sensor_report(
                parse_packet(bytes.fromhex("06 01 00 B3 03 B7"))
            ),
            "30-mins",
        )
        self.assertEqual(
            decode_human_sensor_report(parse_packet(build_packet(0xB3, 0xFF))),
            "unavailable",
        )

    def test_parse_power_on_logo_report(self):
        self.assertEqual(
            decode_power_on_logo_report(
                parse_packet(bytes.fromhex("06 01 00 3F 00 38"))
            ),
            "off",
        )
        self.assertEqual(
            decode_power_on_logo_report(parse_packet(build_packet(0x3F, 0x01))),
            "on",
        )
        self.assertEqual(
            decode_power_on_logo_report(parse_packet(build_packet(0x3F, 0x02))),
            "user",
        )

    def test_parse_off_timer_report(self):
        self.assertEqual(
            decode_off_timer_report(parse_packet(bytes.fromhex("06 01 00 91 00 96"))),
            0,
        )
        self.assertEqual(
            decode_off_timer_report(parse_packet(bytes.fromhex("06 01 00 91 03 95"))),
            3,
        )

    def test_parse_video_parameters_report(self):
        state = decode_video_parameters_report(
            parse_packet(bytes.fromhex("0C 01 00 33 37 37 37 37 37 37 03 3D"))
        )
        self.assertEqual(state.brightness, 55)
        self.assertEqual(state.color, 55)
        self.assertEqual(state.contrast, 55)
        self.assertEqual(state.sharpness, 55)
        self.assertEqual(state.tint, 55)
        self.assertEqual(state.black_level, 55)
        self.assertEqual(state.gamma, 0x03)
        self.assertEqual(state.gamma_name, "2.2")

    def test_parse_picture_format_report(self):
        self.assertEqual(
            decode_picture_format_report(
                parse_packet(bytes.fromhex("06 01 00 3B 03 3F"))
            ),
            "full",
        )
        self.assertEqual(
            decode_picture_format_report(parse_packet(build_packet(0x3B, 0x86))),
            "16:9",
        )

    def test_parse_volume_report(self):
        state = decode_volume_report(
            parse_packet(bytes.fromhex("07 01 00 45 16 0A 5F"))
        )
        self.assertEqual(state.speaker, 22)
        self.assertEqual(state.audio, 10)
        self.assertEqual(state.to_dict(), {"speaker": 22, "audio": 10})

        speaker_only = decode_volume_report(
            parse_packet(bytes.fromhex("06 01 01 45 64 27"))
        )
        self.assertEqual(speaker_only.speaker, 100)
        self.assertIsNone(speaker_only.audio)

    def test_parse_volume_limit_reports(self):
        speaker = decode_volume_limit_report(
            parse_packet(bytes.fromhex("08 01 00 B6 0A 4D 32 CA")),
            target="speaker",
        )
        self.assertEqual(speaker.minimum, 10)
        self.assertEqual(speaker.maximum, 77)
        self.assertEqual(speaker.switch_on, 50)

        audio = decode_volume_limit_report(
            parse_packet(bytes.fromhex("08 01 00 B7 0A 4D 32 CB")),
            target="audio",
        )
        self.assertEqual(
            audio.to_dict(), {"minimum": 10, "maximum": 77, "switch_on": 50}
        )

    def test_parse_audio_parameters_report(self):
        state = decode_audio_parameters_report(
            parse_packet(bytes.fromhex("07 01 00 43 50 5D 48"))
        )
        self.assertEqual(state.treble, 80)
        self.assertEqual(state.treble_display, 80)
        self.assertEqual(state.bass, 93)
        self.assertEqual(state.bass_display, 93)

        signed = decode_audio_parameters_report(
            parse_packet(build_packet(0x43, 0xF8, 0xFF))
        )
        self.assertEqual(signed.treble_display, -8)
        self.assertEqual(signed.bass_display, -1)

    def test_parse_volume_mute_report(self):
        self.assertTrue(
            decode_volume_mute_report(parse_packet(bytes.fromhex("06 01 00 46 01 40")))
        )
        self.assertFalse(
            decode_volume_mute_report(parse_packet(build_packet(0x46, 0x00)))
        )

    def test_parse_color_temperature_report(self):
        self.assertEqual(
            decode_color_temperature_report(
                parse_packet(bytes.fromhex("06 01 00 35 01 33"))
            ),
            "native",
        )

    def test_parse_rgb_parameters_report(self):
        state = decode_rgb_parameters_report(
            parse_packet(bytes.fromhex("0B 01 00 37 FF FF FF FF FF FF 3D"))
        )
        self.assertEqual(state.red_gain, 0xFF)
        self.assertEqual(state.green_gain, 0xFF)
        self.assertEqual(state.blue_gain, 0xFF)
        self.assertEqual(state.red_offset, 0xFF)
        self.assertEqual(state.green_offset, 0xFF)
        self.assertEqual(state.blue_offset, 0xFF)

    def test_parse_color_temperature_100k_report(self):
        state = decode_color_temperature_100k_report(
            parse_packet(bytes.fromhex("06 01 00 12 64 71"))
        )
        self.assertEqual(state.steps, 100)
        self.assertEqual(state.kelvin, 10000)

    def test_power_cold_start_name_to_value(self):
        self.assertEqual(power_cold_start_name_to_value("off"), 0x00)
        self.assertEqual(power_cold_start_name_to_value("on"), 0x01)
        self.assertEqual(power_cold_start_name_to_value("last"), 0x02)

    def test_input_source_name_to_value(self):
        self.assertEqual(input_source_name_to_value("hdmi"), 0x0D)
        self.assertEqual(input_source_name_to_value("display-port1"), 0x0A)
        self.assertEqual(input_source_name_to_value("dp1"), 0x0A)
        self.assertEqual(input_source_name_to_value("0x1C"), 0x1C)

    def test_failover_source_name_to_value(self):
        self.assertEqual(failover_source_name_to_value("hdmi"), 0x00)
        self.assertEqual(failover_source_name_to_value("display-port"), 0x03)
        self.assertEqual(failover_source_name_to_value("dp"), 0x03)
        self.assertEqual(failover_source_name_to_value("hdmi4"), 0x13)

    def test_monitor_restart_target_name_to_value(self):
        self.assertEqual(monitor_restart_target_name_to_value("android"), 0x00)
        self.assertEqual(monitor_restart_target_name_to_value("scalar"), 0x01)
        self.assertEqual(monitor_restart_target_name_to_value("scaler"), 0x01)

    def test_fan_speed_name_to_value(self):
        self.assertEqual(fan_speed_name_to_value("off"), 0x00)
        self.assertEqual(fan_speed_name_to_value("auto"), 0x01)
        self.assertEqual(fan_speed_name_to_value("low"), 0x02)
        self.assertEqual(fan_speed_name_to_value("middle"), 0x03)
        self.assertEqual(fan_speed_name_to_value("medium"), 0x03)
        self.assertEqual(fan_speed_name_to_value("high"), 0x04)
        with self.assertRaises(ValueError):
            fan_speed_name_to_value("0x05")

    def test_lock_state_name_to_value(self):
        self.assertEqual(lock_state_name_to_value("unlock-all", target="ir"), 0x01)
        self.assertEqual(lock_state_name_to_value("lock-all", target="ir"), 0x02)
        self.assertEqual(
            lock_state_name_to_value("lock-all-but-power", target="ir"),
            0x03,
        )
        self.assertEqual(
            lock_state_name_to_value("lock-all-but-volume", target="ir"),
            0x04,
        )
        self.assertEqual(lock_state_name_to_value("primary", target="ir"), 0x05)
        self.assertEqual(lock_state_name_to_value("secondary", target="ir"), 0x06)
        self.assertEqual(
            lock_state_name_to_value("lock-all-except-power-volume", target="ir"),
            0x07,
        )
        self.assertEqual(
            lock_state_name_to_value("lock-all-except-power-volume", target="keypad"),
            0x07,
        )
        with self.assertRaises(ValueError):
            lock_state_name_to_value("primary", target="keypad")

    def test_video_parameter_value_helpers(self):
        self.assertEqual(validate_percentage(100, "brightness"), 100)
        with self.assertRaises(ValueError):
            validate_percentage(101, "brightness")
        self.assertEqual(picture_format_name_to_value("normal"), 0x00)
        self.assertEqual(picture_format_name_to_value("4:3"), 0x00)
        self.assertEqual(picture_format_name_to_value("real-1:1"), 0x02)
        self.assertEqual(picture_format_name_to_value("wide"), 0x03)
        self.assertEqual(picture_format_name_to_value("21-9"), 0x04)
        self.assertEqual(picture_format_name_to_value("16:9"), 0x06)
        self.assertEqual(picture_format_value_to_name(0x06), "16:9")
        self.assertEqual(picture_format_value_to_name(0x86), "16:9")
        with self.assertRaises(ValueError):
            picture_format_name_to_value("0x07")
        self.assertEqual(gamma_name_to_value("native"), 0x01)
        self.assertEqual(gamma_name_to_value("2.2"), 0x03)
        with self.assertRaises(ValueError):
            gamma_name_to_value("0x06")
        self.assertEqual(color_temperature_name_to_value("native"), 0x01)
        self.assertEqual(color_temperature_name_to_value("10000k"), 0x03)
        self.assertEqual(color_temperature_name_to_value("user2"), 0x12)
        with self.assertRaises(ValueError):
            color_temperature_name_to_value("0x11")
        self.assertEqual(validate_color_temperature_100k_steps(20), 20)
        self.assertEqual(validate_color_temperature_100k_steps(100), 100)
        with self.assertRaises(ValueError):
            validate_color_temperature_100k_steps(19)
        with self.assertRaises(ValueError):
            validate_color_temperature_100k_steps(101)

    def test_volume_helpers(self):
        self.assertEqual(validate_volume_level(100, "speaker volume"), 100)
        with self.assertRaises(ValueError):
            validate_volume_level(101, "speaker volume")
        self.assertEqual(validate_volume_limits(10, 77, 50), (10, 77, 50))
        with self.assertRaises(ValueError):
            validate_volume_limits(50, 10, 20)
        self.assertEqual(volume_step_name_to_value("up"), 0x01)
        self.assertEqual(volume_step_name_to_value("+"), 0x01)
        self.assertEqual(volume_step_name_to_value("down"), 0x00)
        self.assertEqual(volume_step_name_to_value("no-change"), 0x02)
        self.assertEqual(volume_step_value_to_name(0x00), "down")
        with self.assertRaises(ValueError):
            volume_step_name_to_value("0x03")
        self.assertEqual(validate_audio_parameter(-8, "treble"), 0xF8)
        self.assertEqual(parse_audio_parameter_value("-1", "treble"), 0xFF)
        self.assertEqual(audio_parameter_value_to_display(0xF8), -8)
        with self.assertRaises(ValueError):
            parse_audio_parameter_value("-9", "treble")
        with self.assertRaises(SicpProtocolError):
            audio_parameter_value_to_display(0x65)
        self.assertTrue(mute_value_to_bool(0x01))
        self.assertFalse(mute_value_to_bool(0x00))
        with self.assertRaises(SicpProtocolError):
            mute_value_to_bool(0x02)

    def test_power_saving_mode_name_to_value(self):
        self.assertEqual(power_saving_mode_name_to_value("off"), 0x00)
        self.assertEqual(power_saving_mode_name_to_value("low"), 0x01)
        self.assertEqual(power_saving_mode_name_to_value("medium"), 0x02)
        self.assertEqual(power_saving_mode_name_to_value("high"), 0x03)
        with self.assertRaises(ValueError):
            power_saving_mode_name_to_value("0x04")

    def test_power_saving_mode_status_helpers(self):
        self.assertEqual(
            power_saving_mode_status_name_to_value("rgb-off-video-off"), 0x00
        )
        self.assertEqual(power_saving_mode_status_name_to_value("all-on"), 0x03)
        self.assertEqual(power_saving_mode_status_name_to_value("mode-1"), 0x04)
        self.assertEqual(power_saving_mode_status_name_to_value("0x07"), 0x07)
        self.assertEqual(
            power_saving_mode_status_value_to_name(0x02), "rgb-on-video-off"
        )
        with self.assertRaises(ValueError):
            power_saving_mode_status_name_to_value("0x08")

    def test_apm_status_helpers(self):
        self.assertEqual(apm_status_name_to_value("off"), 0x00)
        self.assertEqual(apm_status_name_to_value("on"), 0x01)
        self.assertEqual(apm_status_name_to_value("mode-1"), 0x02)
        self.assertEqual(apm_status_name_to_value("tcp-on-wol-off"), 0x03)
        self.assertEqual(apm_status_value_to_name(0x03), "mode-2")
        with self.assertRaises(ValueError):
            apm_status_name_to_value("0x04")

    def test_eco_mode_helpers(self):
        self.assertEqual(eco_mode_name_to_value("low-power-standby"), 0x00)
        self.assertEqual(eco_mode_name_to_value("standby"), 0x00)
        self.assertEqual(eco_mode_name_to_value("normal"), 0x01)
        self.assertEqual(eco_mode_name_to_value("0x01"), 0x01)
        self.assertEqual(eco_mode_value_to_name(0x00), "low-power-standby")
        with self.assertRaises(ValueError):
            eco_mode_name_to_value("0x02")

    def test_picture_style_helpers(self):
        self.assertEqual(picture_style_name_to_value("highbright"), 0x00)
        self.assertEqual(picture_style_name_to_value("s-rgb"), 0x01)
        self.assertEqual(picture_style_name_to_value("static-signage"), 0x06)
        self.assertEqual(picture_style_name_to_value("energy"), 0x08)
        self.assertEqual(picture_style_name_to_value("0x0A"), 0x0A)
        self.assertEqual(picture_style_value_to_name(0x09), "soft")
        with self.assertRaises(ValueError):
            picture_style_name_to_value("0x0B")

    def test_group_id_helpers(self):
        self.assertEqual(group_id_name_to_value("1"), 0x01)
        self.assertEqual(group_id_name_to_value("0xFE"), 0xFE)
        self.assertEqual(group_id_name_to_value("off"), 0xFF)
        self.assertEqual(group_id_value_to_name(0x01), "1")
        self.assertEqual(group_id_value_to_name(0xFF), "off")
        with self.assertRaises(ValueError):
            group_id_name_to_value("0")
        with self.assertRaises(ValueError):
            group_id_name_to_value("255")

    def test_monitor_id_helpers(self):
        self.assertEqual(monitor_id_name_to_value("1"), 0x01)
        self.assertEqual(monitor_id_name_to_value("0xFF"), 0xFF)
        with self.assertRaises(ValueError):
            monitor_id_name_to_value("0")
        with self.assertRaises(ValueError):
            monitor_id_name_to_value("256")

    def test_ports_lock_helpers(self):
        self.assertEqual(ports_lock_name_to_value("unlocked"), 0x00)
        self.assertEqual(ports_lock_name_to_value("enable"), 0x00)
        self.assertEqual(ports_lock_name_to_value("locked"), 0x01)
        self.assertEqual(ports_lock_name_to_value("disable"), 0x01)
        self.assertEqual(ports_lock_value_to_name(0x00), "unlocked")
        self.assertEqual(ports_lock_value_to_name(0x01), "locked")
        with self.assertRaises(ValueError):
            ports_lock_name_to_value("0x02")

    def test_scheduling_helpers(self):
        self.assertEqual(validate_scheduling_page(1), 1)
        self.assertEqual(validate_scheduling_page(7), 7)
        with self.assertRaises(ValueError):
            validate_scheduling_page(0)
        self.assertEqual(parse_scheduling_time("06:30"), (6, 30))
        self.assertEqual(parse_scheduling_time("null"), (24, 60))
        with self.assertRaises(ValueError):
            parse_scheduling_time("24:00")
        self.assertEqual(scheduling_source_name_to_value("null"), 0x00)
        self.assertEqual(scheduling_source_name_to_value("hdmi"), 0x0D)
        self.assertEqual(scheduling_source_value_to_name(0x00), "null")
        self.assertEqual(scheduling_days_name_to_value("every-day"), 0xFF)
        self.assertEqual(scheduling_days_name_to_value("monday,friday"), 0x22)
        self.assertEqual(scheduling_days_value_to_names(0x22), ("monday", "friday"))
        with self.assertRaises(ValueError):
            scheduling_days_name_to_value("funday")

    def test_tiling_helpers(self):
        self.assertEqual(tiling_enable_name_to_value("yes"), 0x01)
        self.assertEqual(tiling_enable_name_to_value("off"), 0x00)
        self.assertEqual(tiling_frame_comp_name_to_value("keep"), 0x02)
        self.assertEqual(tiling_position_name_to_value("2"), 0x02)
        self.assertEqual(tiling_position_name_to_value("keep"), 0x00)
        self.assertEqual(encode_tiling_wall_size(3, 2), 0x08)
        self.assertEqual(encode_tiling_wall_size(3, 2, zero_bezel=True), 0x12)
        self.assertEqual(decode_tiling_wall_size(0x08, max_h=5), (3, 2))
        self.assertEqual(decode_tiling_wall_size(0x12, max_h=15), (3, 2))
        self.assertEqual(
            build_tiling_set_values(1, 0, 2, 0x08),
            (1, 0, 2, 0x08),
        )
        self.assertEqual(
            build_tiling_set_values(1, 2, 0, 0),
            (1, 2, 0, 0),
        )
        with self.assertRaises(ValueError):
            encode_tiling_wall_size(6, 1)
        with self.assertRaises(ValueError):
            encode_tiling_wall_size(16, 1, zero_bezel=True)
        with self.assertRaises(ValueError):
            tiling_position_name_to_value("26")
        self.assertEqual(tiling_position_name_to_value("150", zero_bezel=True), 150)

    def test_switch_on_delay_helpers(self):
        self.assertEqual(switch_on_delay_value_to_name(0x00), "off")
        self.assertEqual(switch_on_delay_value_to_name(0x01), "auto")
        self.assertEqual(switch_on_delay_value_to_name(0x14), "20 seconds")
        self.assertEqual(switch_on_delay_name_to_value("off"), 0x00)
        self.assertEqual(switch_on_delay_name_to_value("auto"), 0x01)
        self.assertEqual(switch_on_delay_name_to_value("20"), 0x14)
        self.assertEqual(switch_on_delay_name_to_value("20s"), 0x14)
        self.assertEqual(switch_on_delay_name_to_value("0xFF"), 0xFF)
        with self.assertRaises(ValueError):
            switch_on_delay_name_to_value("256")
        with self.assertRaises(ValueError):
            switch_on_delay_name_to_value("later")

    def test_anytile_helpers(self):
        self.assertEqual(
            build_anytile_parameters(1, 90, 0, 0, 1920, 1080),
            (1, 0x5A, 0x00, 0, 0, 0, 0, 0x80, 0x07, 0x38, 0x04),
        )
        self.assertEqual(anytile_resolution_name_to_value("default"), 0x00)
        self.assertEqual(anytile_resolution_name_to_value("fhd"), 0x01)
        self.assertEqual(anytile_resolution_name_to_value("uhd4k"), 0x02)
        self.assertEqual(anytile_resolution_name_to_value("4k"), 0x02)
        self.assertEqual(anytile_resolution_value_to_name(0x02), "uhd4k")
        with self.assertRaises(ValueError):
            build_anytile_parameters(2, 0, 0, 0, 1920, 1080)
        with self.assertRaises(ValueError):
            build_anytile_parameters(1, 0x10000, 0, 0, 1920, 1080)
        with self.assertRaises(ValueError):
            anytile_resolution_name_to_value("0x03")
        with self.assertRaises(SicpProtocolError):
            anytile_resolution_value_to_name(0x03)

    def test_light_sensor_name_to_value(self):
        self.assertEqual(light_sensor_name_to_value("off"), 0x00)
        self.assertEqual(light_sensor_name_to_value("on"), 0x01)
        with self.assertRaises(ValueError):
            light_sensor_name_to_value("unavailable")
        self.assertEqual(
            light_sensor_name_to_value("unavailable", allow_unavailable=True),
            0xFF,
        )

    def test_osd_rotating_helpers(self):
        self.assertEqual(osd_rotating_name_to_value("off"), 0x00)
        self.assertEqual(osd_rotating_name_to_value("on"), 0x01)
        self.assertEqual(osd_rotating_name_to_value("0x01"), 0x01)
        self.assertEqual(osd_rotating_value_to_name(0x00), "off")
        with self.assertRaises(ValueError):
            osd_rotating_name_to_value("0x02")

    def test_display_orientation_helpers(self):
        self.assertEqual(display_orientation_auto_rotate_name_to_value("off"), 0x00)
        self.assertEqual(display_orientation_auto_rotate_name_to_value("on"), 0x01)
        self.assertEqual(display_orientation_auto_rotate_value_to_name(0x01), "on")
        self.assertEqual(
            display_orientation_osd_rotation_name_to_value("landscape"), 0x00
        )
        self.assertEqual(
            display_orientation_osd_rotation_name_to_value("portrait"), 0x01
        )
        self.assertEqual(
            display_orientation_osd_rotation_value_to_name(0x01), "portrait"
        )
        self.assertEqual(display_orientation_image_all_name_to_value("off"), 0x00)
        self.assertEqual(display_orientation_image_all_name_to_value("clockwise"), 0x02)
        self.assertEqual(display_orientation_image_all_name_to_value("ccw"), 0x03)
        self.assertEqual(
            display_orientation_image_all_value_to_name(0x03),
            "counter-clockwise",
        )
        self.assertEqual(display_orientation_window_name_to_value("on"), 0x01)
        self.assertEqual(display_orientation_window_value_to_name(0x00), "off")
        self.assertEqual(
            validate_display_orientation_values(0x01, 0x01, 0x03, 0x01, 0, 0, 0),
            (0x01, 0x01, 0x03, 0x01, 0, 0, 0),
        )
        with self.assertRaises(ValueError):
            display_orientation_image_all_name_to_value("0x04")
        with self.assertRaises(SicpProtocolError):
            display_orientation_window_value_to_name(0x02)

    def test_touch_feature_helpers(self):
        self.assertEqual(touch_feature_name_to_value("off"), 0x00)
        self.assertEqual(touch_feature_name_to_value("on"), 0x01)
        self.assertEqual(touch_feature_name_to_value("0x01"), 0x01)
        self.assertEqual(touch_feature_value_to_name(0x00), "off")
        with self.assertRaises(ValueError):
            touch_feature_name_to_value("0x02")
        with self.assertRaises(SicpProtocolError):
            touch_feature_value_to_name(0x02)

    def test_noise_reduction_helpers(self):
        self.assertEqual(noise_reduction_name_to_value("off"), 0x00)
        self.assertEqual(noise_reduction_name_to_value("low"), 0x01)
        self.assertEqual(noise_reduction_name_to_value("middle"), 0x02)
        self.assertEqual(noise_reduction_name_to_value("medium"), 0x02)
        self.assertEqual(noise_reduction_name_to_value("high"), 0x03)
        self.assertEqual(noise_reduction_name_to_value("default"), 0x04)
        self.assertEqual(noise_reduction_name_to_value("0x04"), 0x04)
        self.assertEqual(noise_reduction_value_to_name(0x02), "middle")
        with self.assertRaises(ValueError):
            noise_reduction_name_to_value("0x05")
        with self.assertRaises(SicpProtocolError):
            noise_reduction_value_to_name(0x05)

    def test_scan_mode_helpers(self):
        self.assertEqual(scan_mode_name_to_value("over-scan"), 0x00)
        self.assertEqual(scan_mode_name_to_value("overscan"), 0x00)
        self.assertEqual(scan_mode_name_to_value("under-scan"), 0x01)
        self.assertEqual(scan_mode_name_to_value("underscan"), 0x01)
        self.assertEqual(scan_mode_name_to_value("off"), 0x02)
        self.assertEqual(scan_mode_name_to_value("custom-0"), 0x03)
        self.assertEqual(scan_mode_name_to_value("level-25"), 0x1C)
        self.assertEqual(scan_mode_name_to_value("0x1C"), 0x1C)
        self.assertEqual(scan_mode_value_to_name(0x00), "over-scan")
        self.assertEqual(scan_mode_value_to_name(0x1C), "custom-25")
        with self.assertRaises(ValueError):
            scan_mode_name_to_value("custom-26")
        with self.assertRaises(ValueError):
            scan_mode_name_to_value("0x1D")
        with self.assertRaises(SicpProtocolError):
            scan_mode_value_to_name(0x1D)

    def test_scan_conversion_helpers(self):
        self.assertEqual(scan_conversion_name_to_value("progressive"), 0x00)
        self.assertEqual(scan_conversion_name_to_value("interlace"), 0x01)
        self.assertEqual(scan_conversion_name_to_value("interlaced"), 0x01)
        self.assertEqual(scan_conversion_name_to_value("0x01"), 0x01)
        self.assertEqual(scan_conversion_value_to_name(0x00), "progressive")
        self.assertEqual(scan_conversion_value_to_name(0x01), "interlace")
        with self.assertRaises(ValueError):
            scan_conversion_name_to_value("0x02")
        with self.assertRaises(SicpProtocolError):
            scan_conversion_value_to_name(0x02)

    def test_pixel_shift_helpers(self):
        self.assertEqual(pixel_shift_name_to_value("off"), 0x00)
        self.assertEqual(pixel_shift_name_to_value("auto"), 0x5B)
        self.assertEqual(pixel_shift_name_to_value("50"), 0x05)
        self.assertEqual(pixel_shift_name_to_value("50s"), 0x05)
        self.assertEqual(pixel_shift_name_to_value("50-seconds"), 0x05)
        self.assertEqual(pixel_shift_name_to_value("0x5B"), 0x5B)
        self.assertEqual(pixel_shift_value_to_name(0x00), "off")
        self.assertEqual(pixel_shift_value_to_name(0x05), "50 seconds")
        self.assertEqual(pixel_shift_value_to_name(0x5B), "auto")
        with self.assertRaises(ValueError):
            pixel_shift_name_to_value("55")
        with self.assertRaises(ValueError):
            pixel_shift_name_to_value("0x5C")
        with self.assertRaises(SicpProtocolError):
            pixel_shift_value_to_name(0x5C)

    def test_memc_effect_helpers(self):
        self.assertEqual(memc_effect_name_to_value("off"), 0x00)
        self.assertEqual(memc_effect_name_to_value("low"), 0x01)
        self.assertEqual(memc_effect_name_to_value("medium"), 0x02)
        self.assertEqual(memc_effect_name_to_value("med"), 0x02)
        self.assertEqual(memc_effect_name_to_value("smoothing-high"), 0x03)
        self.assertEqual(memc_effect_name_to_value("0x03"), 0x03)
        self.assertEqual(memc_effect_value_to_name(0x03), "high")
        with self.assertRaises(ValueError):
            memc_effect_name_to_value("0x04")

    def test_information_osd_helpers(self):
        self.assertEqual(information_osd_name_to_value("off"), 0x00)
        self.assertEqual(information_osd_name_to_value("1"), 0x01)
        self.assertEqual(information_osd_name_to_value("0x3C"), 0x3C)
        self.assertEqual(information_osd_value_to_name(0), "off")
        self.assertEqual(information_osd_value_to_name(60), "60 seconds")
        with self.assertRaises(ValueError):
            information_osd_name_to_value("61")

    def test_human_sensor_name_to_value(self):
        self.assertEqual(human_sensor_name_to_value("off"), 0x00)
        self.assertEqual(human_sensor_name_to_value("10-mins"), 0x01)
        self.assertEqual(human_sensor_name_to_value("30"), 0x03)
        self.assertEqual(human_sensor_name_to_value("60-min"), 0x06)
        with self.assertRaises(ValueError):
            human_sensor_name_to_value("unavailable")
        self.assertEqual(
            human_sensor_name_to_value("unavailable", allow_unavailable=True),
            0xFF,
        )

    def test_power_on_logo_name_to_value(self):
        self.assertEqual(power_on_logo_name_to_value("off"), 0x00)
        self.assertEqual(power_on_logo_name_to_value("on"), 0x01)
        self.assertEqual(power_on_logo_name_to_value("user"), 0x02)
        with self.assertRaises(ValueError):
            power_on_logo_name_to_value("0x03")

    def test_off_timer_helpers(self):
        self.assertEqual(off_timer_name_to_value("off"), 0)
        self.assertEqual(off_timer_name_to_value("0"), 0)
        self.assertEqual(off_timer_name_to_value("1-hour"), 1)
        self.assertEqual(off_timer_name_to_value("5h"), 5)
        self.assertEqual(off_timer_name_to_value("24-hours"), 24)
        self.assertEqual(off_timer_value_to_name(0), "off")
        self.assertEqual(off_timer_value_to_name(1), "1-hour")
        self.assertEqual(off_timer_value_to_name(24), "24-hours")
        with self.assertRaises(ValueError):
            off_timer_name_to_value("25")

    def test_build_input_source_osd_style(self):
        self.assertEqual(build_input_source_osd_style(), 0x01)
        self.assertEqual(
            build_input_source_osd_style(do_not_switch=True),
            0x41,
        )
        self.assertEqual(
            build_input_source_osd_style(display_style="reserved"),
            0x00,
        )

    def test_reject_invalid_length(self):
        with self.assertRaises(ValueError):
            parse_packet(bytes.fromhex("06 01 00 19 02"))

    def test_reject_invalid_checksum(self):
        with self.assertRaises(ValueError):
            parse_packet(bytes.fromhex("06 01 00 19 02 00"))

    def test_decode_power_off(self):
        self.assertFalse(
            decode_power_report(parse_packet(bytes.fromhex("06 01 00 19 01 1F")))
        )

    def test_reject_unknown_power_value(self):
        packet = build_packet(0x19, 0x03)
        with self.assertRaises(SicpProtocolError):
            decode_power_report(parse_packet(packet))

    def test_reject_unknown_power_cold_start_value(self):
        packet = build_packet(0xA4, 0x03)
        with self.assertRaises(SicpProtocolError):
            decode_power_cold_start_report(parse_packet(packet))

    def test_reject_malformed_input_source_report(self):
        packet = build_packet(0xAD, 0x0D)
        with self.assertRaises(SicpProtocolError):
            decode_input_source_report(parse_packet(packet))

    def test_reject_malformed_failover_report(self):
        with self.assertRaises(SicpProtocolError):
            decode_failover_report(parse_packet(build_packet(0xA6)))

    def test_reject_malformed_temperature_report(self):
        with self.assertRaises(SicpProtocolError):
            decode_temperature_report(parse_packet(build_packet(0x2F)))
        with self.assertRaises(SicpProtocolError):
            decode_temperature_report(parse_packet(build_packet(0x2F, 0x65)))

    def test_reject_malformed_fan_speed_report(self):
        with self.assertRaises(SicpProtocolError):
            decode_fan_speed_report(parse_packet(build_packet(0x62)))
        with self.assertRaises(SicpProtocolError):
            decode_fan_speed_report(parse_packet(build_packet(0x62, 0x05)))

    def test_reject_malformed_video_signal_present_report(self):
        with self.assertRaises(SicpProtocolError):
            decode_video_signal_present_report(parse_packet(build_packet(0x59)))
        with self.assertRaises(SicpProtocolError):
            decode_video_signal_present_report(parse_packet(build_packet(0x59, 0x02)))

    def test_reject_malformed_lock_reports(self):
        with self.assertRaises(SicpProtocolError):
            decode_ir_lock_report(parse_packet(build_packet(0x1D)))
        with self.assertRaises(SicpProtocolError):
            decode_ir_lock_report(parse_packet(build_packet(0x1D, 0x08)))
        with self.assertRaises(SicpProtocolError):
            decode_keypad_lock_report(parse_packet(build_packet(0x1B)))
        with self.assertRaises(SicpProtocolError):
            decode_keypad_lock_report(parse_packet(build_packet(0x1B, 0x05)))

    def test_reject_malformed_power_saving_mode_report(self):
        with self.assertRaises(SicpProtocolError):
            decode_power_saving_mode_report(parse_packet(build_packet(0xDE)))
        with self.assertRaises(SicpProtocolError):
            decode_power_saving_mode_report(parse_packet(build_packet(0xDE, 0x04)))

    def test_reject_malformed_operating_hours_report(self):
        with self.assertRaises(SicpProtocolError):
            decode_operating_hours_report(parse_packet(build_packet(0x0F)))
        with self.assertRaises(SicpProtocolError):
            decode_operating_hours_report(parse_packet(build_packet(0x0F, 0x00)))

    def test_reject_malformed_power_saving_mode_status_report(self):
        with self.assertRaises(SicpProtocolError):
            decode_power_saving_mode_status_report(parse_packet(build_packet(0xD3)))
        with self.assertRaises(SicpProtocolError):
            decode_power_saving_mode_status_report(
                parse_packet(build_packet(0xD3, 0x08))
            )

    def test_reject_malformed_apm_status_report(self):
        with self.assertRaises(SicpProtocolError):
            decode_apm_status_report(parse_packet(build_packet(0xD1)))
        with self.assertRaises(SicpProtocolError):
            decode_apm_status_report(parse_packet(build_packet(0xD1, 0x04)))

    def test_reject_malformed_eco_mode_report(self):
        with self.assertRaises(SicpProtocolError):
            decode_eco_mode_report(parse_packet(build_packet(0x63)))
        with self.assertRaises(SicpProtocolError):
            decode_eco_mode_report(parse_packet(build_packet(0x63, 0x02)))

    def test_reject_malformed_picture_style_report(self):
        with self.assertRaises(SicpProtocolError):
            decode_picture_style_report(parse_packet(build_packet(0x65)))
        with self.assertRaises(SicpProtocolError):
            decode_picture_style_report(parse_packet(build_packet(0x65, 0x0B)))

    def test_reject_malformed_group_id_report(self):
        with self.assertRaises(SicpProtocolError):
            decode_group_id_report(parse_packet(build_packet(0x5D)))
        with self.assertRaises(SicpProtocolError):
            decode_group_id_report(parse_packet(build_packet(0x5D, 0x00)))

    def test_reject_malformed_ports_lock_report(self):
        with self.assertRaises(SicpProtocolError):
            decode_ports_lock_report(parse_packet(build_packet(0xF2)))
        with self.assertRaises(SicpProtocolError):
            decode_ports_lock_report(parse_packet(build_packet(0xF2, 0x02)))

    def test_reject_malformed_scheduling_report(self):
        with self.assertRaises(SicpProtocolError):
            decode_scheduling_report(parse_packet(build_packet(0x5B)))
        with self.assertRaises(SicpProtocolError):
            decode_scheduling_report(
                parse_packet(build_packet(0x5B, 0x02, 6, 30, 22, 0, 0x0A, 0xFF))
            )
        with self.assertRaises(SicpProtocolError):
            decode_scheduling_report(
                parse_packet(build_packet(0x5B, 0x01, 24, 0, 22, 0, 0x0A, 0xFF))
            )
        with self.assertRaises(SicpProtocolError):
            decode_scheduling_report(
                parse_packet(build_packet(0x5B, 0x01, 6, 30, 22, 0, 0x0A, 0xFF, 8))
            )

    def test_reject_malformed_serial_code_report(self):
        with self.assertRaises(SicpProtocolError):
            decode_serial_code_report(parse_packet(build_packet(0x15)))
        with self.assertRaises(SicpProtocolError):
            decode_serial_code_report(parse_packet(build_packet(0x15, *([0x41] * 13))))
        with self.assertRaises(SicpProtocolError):
            decode_serial_code_report(parse_packet(build_packet(0x15, *([0xFF] * 14))))

    def test_reject_malformed_tiling_report(self):
        with self.assertRaises(SicpProtocolError):
            decode_tiling_report(parse_packet(build_packet(0x23)))
        with self.assertRaises(SicpProtocolError):
            decode_tiling_report(parse_packet(build_packet(0x23, 0x02, 0, 1, 1)))
        with self.assertRaises(SicpProtocolError):
            decode_tiling_report(parse_packet(build_packet(0x23, 1, 0x02, 1, 1)))
        with self.assertRaises(SicpProtocolError):
            decode_tiling_report(parse_packet(build_packet(0x23, 1, 0, 0, 1)))

    def test_reject_malformed_switch_on_delay_report(self):
        with self.assertRaises(SicpProtocolError):
            decode_switch_on_delay_report(parse_packet(build_packet(0x55)))
        with self.assertRaises(SicpProtocolError):
            decode_switch_on_delay_report(parse_packet(build_packet(0x55, 0x00, 0x01)))
        with self.assertRaises(SicpProtocolError):
            decode_switch_on_delay_report(parse_packet(build_packet(0x54, 0x00)))

    def test_reject_malformed_frame_compensation_reports(self):
        with self.assertRaises(SicpProtocolError):
            decode_frame_compensation_horizontal_report(
                parse_packet(build_packet(0x5E))
            )
        with self.assertRaises(SicpProtocolError):
            decode_frame_compensation_horizontal_report(
                parse_packet(build_packet(0x5E, 0x00, 0x01))
            )
        with self.assertRaises(SicpProtocolError):
            decode_frame_compensation_horizontal_report(
                parse_packet(build_packet(0x5F, 0x00))
            )
        with self.assertRaises(SicpProtocolError):
            decode_frame_compensation_vertical_report(parse_packet(build_packet(0x67)))
        with self.assertRaises(SicpProtocolError):
            decode_frame_compensation_vertical_report(
                parse_packet(build_packet(0x67, 0x00, 0x01))
            )
        with self.assertRaises(SicpProtocolError):
            decode_frame_compensation_vertical_report(
                parse_packet(build_packet(0x68, 0x00))
            )

    def test_reject_malformed_anytile_report(self):
        with self.assertRaises(SicpProtocolError):
            decode_anytile_report(parse_packet(build_packet(0x4A)))
        with self.assertRaises(SicpProtocolError):
            decode_anytile_report(parse_packet(build_packet(0x4A, *([0x00] * 10))))
        with self.assertRaises(SicpProtocolError):
            decode_anytile_report(parse_packet(build_packet(0x4A, 2, *([0x00] * 10))))
        with self.assertRaises(SicpProtocolError):
            decode_anytile_resolution_report(parse_packet(build_packet(0x4E)))
        with self.assertRaises(SicpProtocolError):
            decode_anytile_resolution_report(parse_packet(build_packet(0x4E, 0x03)))

    def test_reject_malformed_light_sensor_report(self):
        with self.assertRaises(SicpProtocolError):
            decode_light_sensor_report(parse_packet(build_packet(0x25)))
        with self.assertRaises(SicpProtocolError):
            decode_light_sensor_report(parse_packet(build_packet(0x25, 0x02)))

    def test_reject_malformed_osd_rotating_report(self):
        with self.assertRaises(SicpProtocolError):
            decode_osd_rotating_report(parse_packet(build_packet(0x27)))
        with self.assertRaises(SicpProtocolError):
            decode_osd_rotating_report(parse_packet(build_packet(0x27, 0x02)))

    def test_reject_malformed_display_orientation_report(self):
        with self.assertRaises(SicpProtocolError):
            decode_display_orientation_report(parse_packet(build_packet(0x16)))
        with self.assertRaises(SicpProtocolError):
            decode_display_orientation_report(
                parse_packet(build_packet(0x16, 0, 0, 0, 0, 0, 0))
            )
        with self.assertRaises(SicpProtocolError):
            decode_display_orientation_report(
                parse_packet(build_packet(0x16, 0, 0, 4, 0, 0, 0, 0))
            )

    def test_reject_malformed_touch_feature_report(self):
        with self.assertRaises(SicpProtocolError):
            decode_touch_feature_report(parse_packet(build_packet(0x1F)))
        with self.assertRaises(SicpProtocolError):
            decode_touch_feature_report(parse_packet(build_packet(0x1F, 0x02)))

    def test_reject_malformed_noise_reduction_report(self):
        with self.assertRaises(SicpProtocolError):
            decode_noise_reduction_report(parse_packet(build_packet(0x2B)))
        with self.assertRaises(SicpProtocolError):
            decode_noise_reduction_report(parse_packet(build_packet(0x2B, 0x05)))

    def test_reject_malformed_scan_mode_report(self):
        with self.assertRaises(SicpProtocolError):
            decode_scan_mode_report(parse_packet(build_packet(0x51)))
        with self.assertRaises(SicpProtocolError):
            decode_scan_mode_report(parse_packet(build_packet(0x51, 0x1D)))

    def test_reject_malformed_scan_conversion_report(self):
        with self.assertRaises(SicpProtocolError):
            decode_scan_conversion_report(parse_packet(build_packet(0x53)))
        with self.assertRaises(SicpProtocolError):
            decode_scan_conversion_report(parse_packet(build_packet(0x53, 0x02)))

    def test_reject_malformed_pixel_shift_report(self):
        with self.assertRaises(SicpProtocolError):
            decode_pixel_shift_report(parse_packet(build_packet(0xB1)))
        with self.assertRaises(SicpProtocolError):
            decode_pixel_shift_report(parse_packet(build_packet(0xB1, 0x5C)))

    def test_reject_malformed_memc_effect_report(self):
        with self.assertRaises(SicpProtocolError):
            decode_memc_effect_report(parse_packet(build_packet(0x29)))
        with self.assertRaises(SicpProtocolError):
            decode_memc_effect_report(parse_packet(build_packet(0x29, 0x04)))

    def test_reject_malformed_information_osd_report(self):
        with self.assertRaises(SicpProtocolError):
            decode_information_osd_report(parse_packet(build_packet(0x2D)))
        with self.assertRaises(SicpProtocolError):
            decode_information_osd_report(parse_packet(build_packet(0x2D, 0x3D)))

    def test_reject_malformed_human_sensor_report(self):
        with self.assertRaises(SicpProtocolError):
            decode_human_sensor_report(parse_packet(build_packet(0xB3)))
        with self.assertRaises(SicpProtocolError):
            decode_human_sensor_report(parse_packet(build_packet(0xB3, 0x07)))

    def test_reject_malformed_power_on_logo_report(self):
        with self.assertRaises(SicpProtocolError):
            decode_power_on_logo_report(parse_packet(build_packet(0x3F)))
        with self.assertRaises(SicpProtocolError):
            decode_power_on_logo_report(parse_packet(build_packet(0x3F, 0x03)))

    def test_reject_malformed_off_timer_report(self):
        with self.assertRaises(SicpProtocolError):
            decode_off_timer_report(parse_packet(build_packet(0x91)))
        with self.assertRaises(ValueError):
            decode_off_timer_report(parse_packet(build_packet(0x91, 0x19)))

    def test_reject_malformed_video_parameter_reports(self):
        with self.assertRaises(SicpProtocolError):
            decode_video_parameters_report(parse_packet(build_packet(0x33)))
        with self.assertRaises(SicpProtocolError):
            decode_video_parameters_report(
                parse_packet(build_packet(0x33, 50, 50, 50, 50, 50, 50, 0x06))
            )
        with self.assertRaises(SicpProtocolError):
            decode_video_parameters_report(
                parse_packet(build_packet(0x33, 101, 50, 50, 50, 50, 50, 0x03))
            )
        with self.assertRaises(SicpProtocolError):
            decode_picture_format_report(parse_packet(build_packet(0x3B)))
        with self.assertRaises(SicpProtocolError):
            decode_picture_format_report(parse_packet(build_packet(0x3B, 0x07)))
        with self.assertRaises(SicpProtocolError):
            decode_color_temperature_report(parse_packet(build_packet(0x35)))
        with self.assertRaises(SicpProtocolError):
            decode_color_temperature_report(parse_packet(build_packet(0x35, 0x11)))
        with self.assertRaises(SicpProtocolError):
            decode_rgb_parameters_report(parse_packet(build_packet(0x37)))
        with self.assertRaises(SicpProtocolError):
            decode_color_temperature_100k_report(parse_packet(build_packet(0x12)))
        with self.assertRaises(SicpProtocolError):
            decode_color_temperature_100k_report(parse_packet(build_packet(0x12, 19)))

    def test_validate_failover_priorities(self):
        self.assertEqual(validate_failover_priorities((0x00,)), (0x00,))
        with self.assertRaises(ValueError):
            validate_failover_priorities(())
        with self.assertRaises(ValueError):
            validate_failover_priorities(tuple(range(18)))

    def test_require_ack_accepts_ack(self):
        require_ack(parse_packet(bytes.fromhex("06 01 00 00 06 01")))

    def test_require_ack_rejects_nack_and_nav(self):
        with self.assertRaises(SicpNackError):
            require_ack(parse_packet(build_packet(0x00, 0x15)))
        with self.assertRaises(SicpNavError):
            require_ack(parse_packet(build_packet(0x00, 0x18)))

    def test_require_ack_rejects_non_control_response(self):
        with self.assertRaises(SicpAckError):
            require_ack(parse_packet(bytes.fromhex("06 01 00 19 02 1C")))

    def test_recv_packet_handles_split_packet(self):
        client = SicpClient("127.0.0.1")
        sock = FakeSocket([bytes.fromhex("06 01"), bytes.fromhex("00 19 02 1C")])
        result = client._recv_packet(sock)
        self.assertEqual(result.packet.raw, bytes.fromhex("06 01 00 19 02 1C"))

    def test_recv_packet_skips_stray_prefix_bytes(self):
        client = SicpClient("127.0.0.1")
        sock = FakeSocket([bytes.fromhex("00 FF"), bytes.fromhex("06 01 00 19 02 1C")])
        result = client._recv_packet(sock)
        self.assertEqual(result.packet.raw, bytes.fromhex("06 01 00 19 02 1C"))

    def test_recv_packet_recovers_after_invalid_candidate(self):
        client = SicpClient("127.0.0.1")
        sock = FakeSocket(
            [
                bytes.fromhex("06 01 00 19 02 01"),
                bytes.fromhex("06 01 00 19 02 1C"),
            ]
        )
        result = client._recv_packet(sock)
        self.assertEqual(result.packet.raw, bytes.fromhex("06 01 00 19 02 1C"))

    def test_recv_packet_waits_for_expected_command(self):
        client = SicpClient("127.0.0.1")
        sock = FakeSocket(
            [
                build_packet(0x01, 0x02),
                bytes.fromhex("06 01 00 19 02 1C"),
            ]
        )
        result = client._recv_packet(sock, expected_response_commands=(0x19,))
        self.assertEqual(result.packet.raw, bytes.fromhex("06 01 00 19 02 1C"))
        self.assertEqual(len(result.skipped), 1)
        self.assertEqual(result.skipped[0].command, 0x01)

    def test_recv_packet_uses_expected_size_to_avoid_overlapping_false_frame(self):
        client = SicpClient("127.0.0.1")
        sock = FakeSocket(
            [
                bytes.fromhex(
                    "1E 06 01 01 19 01 "
                    "1E 06 01 01 19 01 "
                    "1E 06 01 01 19 01 "
                    "1E 06 01 01 19 01 "
                    "1E 06 01 01 19 01"
                )
            ]
        )
        result = client._recv_packet(
            sock,
            expected_response_commands=(0x19,),
            expected_response_sizes=(6,),
        )
        self.assertEqual(result.packet.raw, bytes.fromhex("06 01 01 19 01 1E"))
        self.assertEqual(result.packet.command, 0x19)
        self.assertEqual(result.skipped, ())

    def test_recv_packet_finds_expected_packet_inside_false_frame(self):
        client = SicpClient("127.0.0.1")
        sock = FakeSocket([bytes.fromhex("06 00 06 01 01 00 06 00")])
        result = client._recv_packet(
            sock,
            expected_response_commands=(0x00,),
            expected_response_sizes=(6,),
        )
        self.assertEqual(result.packet.raw, bytes.fromhex("06 01 01 00 06 00"))
        self.assertEqual(result.packet.command, 0x00)

    def test_recv_packet_errors_when_only_unexpected_command_arrives(self):
        client = SicpClient("127.0.0.1")
        sock = FakeSocket([build_packet(0x01, 0x02)])
        with self.assertRaisesRegex(SicpProtocolError, "saw"):
            client._recv_packet(sock, expected_response_commands=(0x19,))


if __name__ == "__main__":
    unittest.main()
