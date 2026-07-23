# Philips SICP Command Reference Index

This index is for quick reference when implementing a new command group in the Python client. Each linked file contains the relevant GET, REPORT, SET, or action notes extracted from `Philips_SICP_Commands.md`.

| Command group | File | Operations |
|---|---|---|
| Communication Control | [`01-communication-control.md`](commands/01-communication-control.md) | 2.4.1 Message-Report |
| SICP version and platform information | [`02-sicp-version-and-platform-information.md`](commands/02-sicp-version-and-platform-information.md) | 3.1 Message-Get (SICP version, platform information), 3.2 Message Report (SICP version, platform information) |
| Model Number, Firmware Version, Build Date | [`03-model-number-firmware-version-build-date.md`](commands/03-model-number-firmware-version-build-date.md) | 3.3 Message-Get (Model Number, FW Version, Build date), 3.4 Message-Report (Model Number, FW Version, Build date) |
| Power state | [`04-power-state.md`](commands/04-power-state.md) | 4.1.1 Message-Get, 4.1.2 Message-Report, 4.1.3 Message-Set |
| Lock Functions for IR-Remote Control & Keypad | [`05-lock-functions-for-ir-remote-control-and-keypad.md`](commands/05-lock-functions-for-ir-remote-control-and-keypad.md) | 4.2.1 Message-Get (IR-Remote Control), 4.2.2 Message-Report (IR-Remote Control), 4.2.3 Message-Set (IR –Remote Control), 4.2.3 Message-Get (Keypad), 4.2.4 Message-Report (Keypad), 4.2.5 Message-Set (Keypad) |
| Power state at Cold Start | [`06-power-state-at-cold-start.md`](commands/06-power-state-at-cold-start.md) | 4.3.1 Message-Get, 4.3.2 Message-Report, 4.3.3 Message-Set |
| Input Sources | [`07-input-sources.md`](commands/07-input-sources.md) | 4.4.1.1 Message-Set, 4.4.1.2 Message-Get, 4.4.1.3 Message-Report |
| Auto Signal Detecting / Failover | [`08-auto-signal-detecting-failover.md`](commands/08-auto-signal-detecting-failover.md) | 4.5.1 Message-Get, 4.5.2 Message-Report, 4.5.3 Message-Set, 4.5.4 Message-Get, 4.5.5 Message-Report, 4.5.6 Message-Set |
| Monitor restart | [`09-monitor-restart.md`](commands/09-monitor-restart.md) | 4.6.1 Message-Set |
| Backlight On-Off | [`10-backlight-on-off.md`](commands/10-backlight-on-off.md) | 4.7.1 Get backlight status, 4.7.2 Set backlight on-off |
| Video Parameters | [`11-video-parameters.md`](commands/11-video-parameters.md) | 5.1.1 Message-Get Video parameters, 5.1.2 Message-Report Video parameters, 5.1.3 Message-Set Video parameters, 5.1.4 Message-Get Color Temperature, 5.1.5 Message-Report Color Temperature, 5.1.6 Message-Set Color Temperature, 5.1.7 Message-Get RGB parameters, 5.1.8 Message-Report RGB parameters, 5.1.9 Message-Set RGB parameters, 5.1.9.1 Message-Get Color Temperature 100K steps, 5.1.9.2 Message-Report Color Temperature 100K steps, 5.1.9.3 Message-Set Color Temperature 100K steps |
| Picture Format | [`12-picture-format.md`](commands/12-picture-format.md) | 5.2.1 Message-Get, 5.2.2 Message-Report, 5.2.3 Message-Set |
| VGA video Parameters | [`13-vga-video-parameters.md`](commands/13-vga-video-parameters.md) | 5.3.1 Message-Get, 5.3.2 Message-Report, 5.3.4 Message-Set |
| Picture-in-Picture (PIP) | [`14-picture-in-picture-pip.md`](commands/14-picture-in-picture-pip.md) | 5.4.1 Message-Get, 5.4.2 Message-Report, 5.4.3 Message-Set, 5.4.4.1 Message-Get PIP source, 5.4.4.2 Message-Report PIP source, 5.4.4.3 Message-Set |
| Volume | [`15-volume.md`](commands/15-volume.md) | 6.1.1 Message-Get current volume level speakers and audio out, 6.1.2 Message-Report current volume level speakers and audio out, 6.1.3 Message-Set current volume level speakers and audio out, 6.1.4 Message-Set Volume level – step up or step down for Speaker out or Audio Out, 6.1.5.1 Message-Set Volume Limit, 6.1.5.2 Message-Get Volume Limit, 6.1.6.1 Message-Set Volume Limit – Audio out, 6.1.6.2 Message-Get Volume Limit – Audio out, 6.1.7.1 Message-Get, 6.1.7.2 Message-Report, 6.1.7.3 Message-Set, 6.1.8.1 Get volume mute, 6.1.8.2 Message-Report, 6.1.8.3 Set volume mute |
| Operating Hours | [`16-operating-hours.md`](commands/16-operating-hours.md) | 7.1.1 Message-Get, 7.1.2 Message-Report |
| Power Saving Mode | [`17-power-saving-mode.md`](commands/17-power-saving-mode.md) | 7.2.1 Message-Get, 7.2.2 Message-Report, 7.2.3 Message-Set |
| Auto Adjust | [`18-auto-adjust.md`](commands/18-auto-adjust.md) | 7.3.1 Message-Set |
| Temperature Sensors | [`19-temperature-sensors.md`](commands/19-temperature-sensors.md) | 7.4.1 Message-Get, 7.4.2 Message-Report |
| Serial Code | [`20-serial-code.md`](commands/20-serial-code.md) | 7.5.1 Message-Get, 7.5.2 Message-Report |
| Tiling | [`21-tiling.md`](commands/21-tiling.md) | 7.6.1 Message-Get, 7.6.2 Message-Report, 7.6.3 Message-Set |
| AnyTile (Canvas) | [`22-anytile-canvas.md`](commands/22-anytile-canvas.md) | 7.7.3 AnyTile –Report, 7.7.4 AnyTile Set, 7.7.4 AnyTile Set/Get Resolution Mode |
| Light Sensor | [`23-light-sensor.md`](commands/23-light-sensor.md) | 7.8.1 Message-Get, 7.8.2 Message-Report, 7.8.3 Message-Set |
| Human Sensor | [`24-human-sensor.md`](commands/24-human-sensor.md) | 7.9.1 Human Sensor Message-Get, 7.9.2 Human Sensor Message-Report, 7.9.3 Human Sensor Message-Set |
| OSD Rotating | [`25-osd-rotating.md`](commands/25-osd-rotating.md) | 7.10.1 Message-Get, 7.10.2 Message-Report, 7.10.3 Message-Set |
| Display Orientation | [`26-display-orientation.md`](commands/26-display-orientation.md) | 7.11.1 Message-Get, 7.11.2 Message-Report, 7.11.3 Message-Set |
| Information OSD | [`27-information-osd.md`](commands/27-information-osd.md) | 7.11.1 Message-Get, 7.11.2 Message-Report, 7.11.3 Message-Set |
| MEMC Effect | [`28-memc-effect.md`](commands/28-memc-effect.md) | 7.12.1 Message-Get, 7.12.2 Message-Report, 7.12.3 Message-Set |
| Touch Feature | [`29-touch-feature.md`](commands/29-touch-feature.md) | 7.13.1 Message-Get, 7.13.2 Message-Report, 7.13.3 Message-Set |
| Noise Reduction | [`30-noise-reduction.md`](commands/30-noise-reduction.md) | 7.14.1 Message-Get, 7.14.2 Message-Report, 7.14.3 Message-Set |
| Scan Mode | [`31-scan-mode.md`](commands/31-scan-mode.md) | 7.15.1 Message-Get, 7.15.2 Message-Report, 7.15.3 Message-Set |
| Scan Conversion | [`32-scan-conversion.md`](commands/32-scan-conversion.md) | 7.16.1 Message-Get, 7.16.2 Message-Report, 7.16.3 Message-Set |
| Switch On Delay (Tiling) | [`33-switch-on-delay-tiling.md`](commands/33-switch-on-delay-tiling.md) | 7.17.1 Message-Get, 7.17.2 Message-Report, 7.17.3 Message-Set |
| Factory Reset | [`34-factory-reset.md`](commands/34-factory-reset.md) | 7.18.1 Message-Set |
| Power On logo | [`35-power-on-logo.md`](commands/35-power-on-logo.md) | 7.19.1 Message-Get, 7.19.2 Message-Report, 7.19.3 Message-Set |
| Fan Speed | [`36-fan-speed.md`](commands/36-fan-speed.md) | 7.20.1 Message-Get, 7.20.2 Message-Report, 7.20.3 Message-Set |
| APM status (advanced power management) | [`37-apm-status-advanced-power-management.md`](commands/37-apm-status-advanced-power-management.md) | 7.21.1 Message-Get, 7.21.2 Message-Report, 7.21.3 Message-Set |
| Power saving mode status | [`38-power-saving-mode-status.md`](commands/38-power-saving-mode-status.md) | 7.22.1 Message-Get, 7.22.2 Message-Report, 7.22.3 Message-Set |
| Pixel Shift | [`39-pixel-shift.md`](commands/39-pixel-shift.md) | 7.23.1 Message-Get Pixel Shift, 7.23.2 Message-Report Pixel Shift, 7.23.3 Message-Set Pixel Shift |
| Off Timer | [`40-off-timer.md`](commands/40-off-timer.md) | 7.24.1 Message-Get Off Timer, 7.24.2 Message-Report Off Timer, 7.24.3 Message-Set Off Timer |
| ECO mode | [`41-eco-mode.md`](commands/41-eco-mode.md) | 7.25.1 Message-report ECO mode, 7.25.2 Message- Set ECO mode |
| Picture Style | [`42-picture-style.md`](commands/42-picture-style.md) | 7.26.1 Message-report get Picture Style, 7.26.2 Message-set Picture Style |
| Send screenshot | [`43-send-screenshot.md`](commands/43-send-screenshot.md) | See source excerpt |
| Video signal present | [`44-video-signal-present.md`](commands/44-video-signal-present.md) | 7.28.1 Message-report |
| Frame compensation Get value Horz value | [`45-frame-compensation-get-value-horz-value.md`](commands/45-frame-compensation-get-value-horz-value.md) | 7.29 Frame compensation Get value Horz value |
| Frame compensation Set value Horz | [`46-frame-compensation-set-value-horz.md`](commands/46-frame-compensation-set-value-horz.md) | 7.30 Frame compensation Set value Horz |
| Frame compensation Get value Vert value | [`47-frame-compensation-get-value-vert-value.md`](commands/47-frame-compensation-get-value-vert-value.md) | 7.31 Frame compensation Get value Vert value |
| Frame compensation Set value Vert | [`48-frame-compensation-set-value-vert.md`](commands/48-frame-compensation-set-value-vert.md) | 7.32 Frame compensation Set value Vert |
| Scheduling Parameters | [`49-scheduling-parameters.md`](commands/49-scheduling-parameters.md) | 8.1.1 Message-Get, 8.1.2 Message-Report, 8.1.3 Message-Set |
| Group ID | [`50-group-id.md`](commands/50-group-id.md) | 9.1.1 Message-Get, 9.1.2 Message-Report, 9.1.3 Message-Set |
| Custom Multi-Window Settings | [`51-custom-multi-window-settings.md`](commands/51-custom-multi-window-settings.md) | 10.1.1 Message-Set, 10.1.2 Message-Get (report) –, 10.1.3 Message-Set |
| Color Calibration MIC | [`52-color-calibration-mic.md`](commands/52-color-calibration-mic.md) | 11.1 Message-Set |
| LED Strip Control | [`53-led-strip-control.md`](commands/53-led-strip-control.md) | 12.1 Message-Get (Report), 12.2 Message-Set |
| MicroSD and USB Ports Unlock Lock | [`54-microsd-and-usb-ports-unlock-lock.md`](commands/54-microsd-and-usb-ports-unlock-lock.md) | 13.1 Message-Get (Report), 13.2 Message-Set |
| Monitor ID | [`55-monitor-id.md`](commands/55-monitor-id.md) | See source excerpt |
