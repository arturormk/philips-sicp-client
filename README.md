# Philips SICP Python Client

[![CI](https://github.com/arturormk/philips-sicp-client/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/arturormk/philips-sicp-client/actions/workflows/ci.yml)

Small, dependency-free Python CLI for the Philips Serial / Ethernet Interface
Communication Protocol (SICP).

The client currently supports TCP communication on port `5000`, packet
construction, checksum handling, response parsing, ACK/NACK/NAV handling, typed
commands for implemented command groups, configuration collect/apply helpers,
and a raw DATA[] command for probing new protocol messages.

The implementation uses only the Python standard library.

## Requirements

- Python `3.10` or newer.
- Optional: [`uv`](https://docs.astral.sh/uv/) for environment and command
  management.

## Installation

Run directly from a checkout with `uv`:

```bash
uv run sicp --host 192.168.1.50 power get
```

Install the package into the current `uv` environment:

```bash
uv sync
uv run sicp --host 192.168.1.50 power get
```

The project has no runtime dependencies.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).

This is an independent project and is not affiliated with, endorsed by, or
sponsored by Philips, TPV, or PPDS. See [NOTICE](NOTICE).

## Usage

Run from the repository root:

```bash
python3 sicp.py --host 192.168.1.50 power get
```

or:

```bash
python3 -m philips_sicp --host 192.168.1.50 power get
```

After installation, the console command is also available:

```bash
sicp --host 192.168.1.50 power get
```

Print the installed client version:

```bash
sicp --version
```

## Global Options

Global options must appear before the command group:

```bash
python3 sicp.py [global-options] <command-group> ...
```

Options:

| Option | Environment variable | Default |
|---|---|---|
| `--host HOST` | `PHILIPS_SICP_HOST` | required |
| `--port PORT` | `PHILIPS_SICP_PORT` | `5000` |
| `--monitor-id ID` | `PHILIPS_SICP_MONITOR_ID` | `1` |
| `--group-id ID` | `PHILIPS_SICP_GROUP_ID` | `0` |
| `--timeout SECONDS` | `PHILIPS_SICP_TIMEOUT` | `2.0` |
| `--retries COUNT` | `PHILIPS_SICP_RETRIES` | `1` |

Other global options:

| Option | Meaning |
|---|---|
| `--verbose` | Print request/response packets and parsed fields. |
| `--json` | Print structured JSON output. |
| `--version` | Print the installed client version. |

Integer options accept decimal or `0xNN` syntax. Raw DATA[] bytes are interpreted
as hex by default.

## Power State

Read current power state:

```bash
python3 sicp.py --host 192.168.1.50 power get
```

Set power state:

```bash
python3 sicp.py --host 192.168.1.50 power set on
python3 sicp.py --host 192.168.1.50 power set off
```

Protocol:

| Operation | DATA[0] | Values |
|---|---:|---|
| GET/report | `0x19` | `0x01` off, `0x02` on |
| SET | `0x18` | `0x01` off, `0x02` on |

## Power State At Cold Start

Read configured cold-start power state:

```bash
python3 sicp.py --host 192.168.1.50 power cold-start get
```

Set cold-start power state:

```bash
python3 sicp.py --host 192.168.1.50 power cold-start set off
python3 sicp.py --host 192.168.1.50 power cold-start set on
python3 sicp.py --host 192.168.1.50 power cold-start set last
```

Protocol:

| Operation | DATA[0] | Values |
|---|---:|---|
| GET/report | `0xA4` | `0x00` off, `0x01` on, `0x02` last |
| SET | `0xA3` | `0x00` off, `0x01` on, `0x02` last |

## Input Source

Read current input source:

```bash
python3 sicp.py --host 192.168.1.50 input-source get
```

Set current input source:

```bash
python3 sicp.py --host 192.168.1.50 input-source set hdmi
python3 sicp.py --host 192.168.1.50 input-source set hdmi2
python3 sicp.py --host 192.168.1.50 input-source set display-port1
python3 sicp.py --host 192.168.1.50 input-source set 0x0D
```

Optional SET fields:

```bash
python3 sicp.py --host 192.168.1.50 input-source set browser --playlist 1
python3 sicp.py --host 192.168.1.50 input-source set hdmi --do-not-switch
python3 sicp.py --host 192.168.1.50 input-source set hdmi --display-style reserved
python3 sicp.py --host 192.168.1.50 input-source set hdmi --mute-style 0
```

Protocol:

| Operation | DATA[0] | DATA fields |
|---|---:|---|
| GET/report | `0xAD` | report returns source, playlist, OSD style, mute style |
| SET | `0xAC` | source, playlist, OSD style, mute style |

Known source names:

`video`, `s-video`, `component`, `cvi2`, `vga`, `hdmi2`,
`display-port2`, `usb2`, `card-dvi-d`, `display-port1`, `card-ops`,
`usb1`, `hdmi`, `dvi-d`, `hdmi3`, `browser`, `smartcms`, `dms`,
`internal-storage`, `media-player`, `pdf-player`, `custom`, `hdmi4`,
`vga2`, `vga3`, `iwb`.

The CLI also accepts numeric byte values such as `0x0D`.

## Auto Signal Detecting

Read auto signal detecting mode:

```bash
python3 sicp.py --host 192.168.1.50 auto-signal get
```

Set auto signal detecting mode:

```bash
python3 sicp.py --host 192.168.1.50 auto-signal set off
python3 sicp.py --host 192.168.1.50 auto-signal set all
python3 sicp.py --host 192.168.1.50 auto-signal set pc-only
python3 sicp.py --host 192.168.1.50 auto-signal set video-only
python3 sicp.py --host 192.168.1.50 auto-signal set failover
```

Protocol:

| Operation | DATA[0] | Values |
|---|---:|---|
| GET/report | `0xAF` | current mode |
| SET | `0xAE` | `0x00` off, `0x01` all, `0x02` reserved, `0x03` PC only, `0x04` video only, `0x05` failover |

## Failover

Read failover priority list:

```bash
python3 sicp.py --host 192.168.1.50 failover get
```

Set failover priority list:

```bash
python3 sicp.py --host 192.168.1.50 failover set hdmi component composite display-port
```

`fallover` is accepted as an alias for `failover`.

Protocol:

| Operation | DATA[0] | DATA fields |
|---|---:|---|
| GET/report | `0xA6` | priority list |
| SET | `0xA5` | 1 to 17 priority source values |

Known failover source names:

`hdmi`, `component`, `composite`, `display-port`, `dvi-d`, `vga`, `ops`,
`usb`, `browser`, `smartcms`, `internal-storage`, `dms`, `hdmi2`, `hdmi3`,
`usb-playlist`, `usb-autoplay`, `media-player`, `pdf-player`, `custom`,
`hdmi4`, `vga2`, `vga3`, `iwb`.

The vendor documentation is inconsistent about the exact number of priorities,
so the CLI accepts between 1 and 17 entries.

## Monitor Restart

Restart the Android system of the monitor:

```bash
python3 sicp.py --host 192.168.1.50 monitor restart
python3 sicp.py --host 192.168.1.50 monitor restart android
```

Restart the scalar/scaler target:

```bash
python3 sicp.py --host 192.168.1.50 monitor restart scalar
python3 sicp.py --host 192.168.1.50 monitor restart scaler
```

Protocol:

| Operation | DATA[0] | Values |
|---|---:|---|
| SET | `0x57` | `0x00` Android, `0x01` Scalar |

The vendor notes say this command is available only on supported Android monitor
platforms.

## Temperature Sensors

Read monitor temperature sensor values:

```bash
python3 sicp.py --host 192.168.1.50 temperature get
```

Protocol:

| Operation | DATA[0] | DATA fields |
|---|---:|---|
| GET/report | `0x2F` | one or two Celsius sensor bytes |

The report normally contains two sensor values in Celsius. Some Dragon platform
models return only one valid sensor byte.

## Fan Speed

Read fan speed mode:

```bash
python3 sicp.py --host 192.168.1.50 fan-speed get
```

Set fan speed mode:

```bash
python3 sicp.py --host 192.168.1.50 fan-speed set off
python3 sicp.py --host 192.168.1.50 fan-speed set auto
python3 sicp.py --host 192.168.1.50 fan-speed set low
python3 sicp.py --host 192.168.1.50 fan-speed set middle
python3 sicp.py --host 192.168.1.50 fan-speed set high
```

`medium` is accepted as an alias for `middle`.

Protocol:

| Operation | DATA[0] | Values |
|---|---:|---|
| GET/report | `0x62` | `0x00` off, `0x01` auto, `0x02` low, `0x03` middle, `0x04` high |
| SET | `0x61` | `0x00` off, `0x01` auto, `0x02` low, `0x03` middle, `0x04` high |

The vendor notes say Dragon 1.x and Dragon 1.6 do not support this command.

## Video Parameters

Read or set the main video parameters:

```bash
python3 sicp.py --host 192.168.1.50 video parameters get
python3 sicp.py --host 192.168.1.50 video parameters set \
  --brightness 55 --color 55 --contrast 55 --sharpness 55 \
  --tint 55 --black-level 55 --gamma 2.2
```

Read or set the color temperature preset:

```bash
python3 sicp.py --host 192.168.1.50 video color-temperature get
python3 sicp.py --host 192.168.1.50 video color-temperature set native
python3 sicp.py --host 192.168.1.50 video color-temperature set 6500k
```

Read or set picture format:

```bash
python3 sicp.py --host 192.168.1.50 video picture-format get
python3 sicp.py --host 192.168.1.50 video picture-format set full
python3 sicp.py --host 192.168.1.50 video picture-format set 16:9
```

Read or set RGB gain and offset parameters:

```bash
python3 sicp.py --host 192.168.1.50 video rgb get
python3 sicp.py --host 192.168.1.50 video rgb set \
  --red-gain 255 --green-gain 255 --blue-gain 255 \
  --red-offset 255 --green-offset 255 --blue-offset 255
```

Read or set color temperature in 100K steps:

```bash
python3 sicp.py --host 192.168.1.50 video color-temperature-100k get
python3 sicp.py --host 192.168.1.50 video color-temperature-100k set 100
```

For `color-temperature-100k`, the value is a step count from `20` to `100`,
representing `2000K` to `10000K`.

Protocol:

| Command | Operation | DATA[0] | Fields |
|---|---|---:|---|
| Video parameters | GET/report | `0x33` | brightness, color, contrast, sharpness, tint, black level, gamma |
| Video parameters | SET | `0x32` | same as GET/report |
| Picture format | GET/report | `0x3B` | format |
| Picture format | SET | `0x3A` | format |
| Color temperature | GET/report | `0x35` | preset |
| Color temperature | SET | `0x34` | preset |
| RGB parameters | GET/report | `0x37` | red/green/blue gain, red/green/blue offset |
| RGB parameters | SET | `0x36` | same as GET/report |
| Color temperature 100K | GET/report | `0x12` | step count |
| Color temperature 100K | SET | `0x11` | step count |

Video parameter fields are validated as `0..100` using the standard table.
RGB fields are byte values from `0..255`. Gamma accepts `native`, `s-gamma`,
`2.2`, `2.4`, and `dicom`.

Picture format accepts `normal`, `custom`, `real`, `full`, `21:9`, `dynamic`,
and `16:9`.

Color temperature presets:

`user1`, `native`, `11000k`, `10000k`, `9300k`, `7500k`, `6500k`, `5770k`,
`5500k`, `5000k`, `4000k`, `3400k`, `3350k`, `3000k`, `2800k`, `2600k`,
`1850k`, `user2`.

The vendor notes say some video and RGB parameter commands are not supported on
QL3 for browser, PDF player, media player, CMND&play, and installed APK inputs.
The Phoenix 2.0 alternate tint and sharpness ranges are not exposed in typed CLI;
use `raw data` for those variant values.

## Volume

Read or set current speaker/audio output volume:

```bash
python3 sicp.py --host 192.168.1.50 volume get
python3 sicp.py --host 192.168.1.50 volume set --speaker 22
python3 sicp.py --host 192.168.1.50 volume set --speaker 22 --audio 50
```

Step volume up or down:

```bash
python3 sicp.py --host 192.168.1.50 volume step --speaker up
python3 sicp.py --host 192.168.1.50 volume step --speaker down --audio no-change
```

Read or set speaker/audio volume limits:

```bash
python3 sicp.py --host 192.168.1.50 volume limit speaker get
python3 sicp.py --host 192.168.1.50 volume limit speaker set --min 10 --max 77 --switch-on 50
python3 sicp.py --host 192.168.1.50 volume limit audio get
python3 sicp.py --host 192.168.1.50 volume limit audio set --min 10 --max 77 --switch-on 50
```

Read or set audio parameters and mute state:

```bash
python3 sicp.py --host 192.168.1.50 volume audio get
python3 sicp.py --host 192.168.1.50 volume audio set --treble 77 --bass 77
python3 sicp.py --host 192.168.1.50 volume mute get
python3 sicp.py --host 192.168.1.50 volume mute set on
python3 sicp.py --host 192.168.1.50 volume mute set off
```

Protocol:

| Command | Operation | DATA[0] | Fields |
|---|---|---:|---|
| Current volume | GET/report | `0x45` | speaker volume, optional audio volume |
| Current volume | SET | `0x44` | speaker volume, optional audio volume |
| Step volume | SET | `0x41` | speaker direction, optional audio direction |
| Speaker volume limits | GET/report | `0xB6` | minimum, maximum, switch-on |
| Speaker volume limits | SET | `0xB8` | minimum, maximum, switch-on |
| Audio volume limits | GET/report | `0xB7` | minimum, maximum, switch-on |
| Audio volume limits | SET | `0xB9` | minimum, maximum, switch-on |
| Audio parameters | GET/report | `0x43` | treble, bass |
| Audio parameters | SET | `0x42` | treble, bass |
| Volume mute | GET/report | `0x46` | `0x00` off, `0x01` on |
| Volume mute | SET | `0x47` | `0x00` off, `0x01` on |

Volume levels are validated as `0..100`. Limit commands require
`min <= switch-on <= max`. Step direction accepts `up`, `down`, `no-change`,
`+`, and `-`. Audio parameters accept normal `0..100` values; signed
`-8..8` values are also accepted for platforms that use the Phoenix 2.0 range.

## Operating Hours

Read the display operating-hours counter:

```bash
python3 sicp.py --host 192.168.1.50 operating-hours get
```

Protocol:

| Operation | DATA[0] | Values |
|---|---:|---|
| GET | `0x0F 0x02` | Misc info item `0x02` requests operating hours |
| Report | `0x0F` | `DATA[1]` and `DATA[2]` form a 16-bit operating-hours value |

## Tiling

Read or set video-wall tiling settings:

```bash
python3 sicp.py --host 192.168.1.50 tiling get
python3 sicp.py --host 192.168.1.50 tiling set --enable yes
python3 sicp.py --host 192.168.1.50 tiling set --enable yes --frame-comp no --position 2 --h-monitors 3 --v-monitors 2
python3 sicp.py --host 192.168.1.50 tiling set --enable yes --frame-comp no --position 2 --h-monitors 3 --v-monitors 2 --zero-bezel
```

Protocol:

| Operation | DATA[0] | Fields |
|---|---:|---|
| GET/report | `0x23` | enable, frame compensation, position, wall-size |
| SET | `0x22` | enable, frame compensation, position, wall-size |

SET supports keep-previous values for optional fields:

```bash
python3 sicp.py --host 192.168.1.50 tiling set --enable yes --frame-comp keep --position keep
```

Wall-size encoding:

| Model class | Limits | Formula |
|---|---|---|
| Standard | H `1..5`, V `1..5`, position `1..25` | `(V - 1) * 5 + H` |
| Zero bezel | H `1..15`, V `1..10`, position `1..150` | `(V - 1) * 15 + H` |

Use `--zero-bezel` to apply the larger wall-size and position limits. `--wall-size`
can be used to pass DATA[4] directly instead of `--h-monitors/--v-monitors`.

## Switch On Delay

Read or set the switch-on delay used with tiling/video-wall installs:

```bash
python3 sicp.py --host 192.168.1.50 switch-on-delay get
python3 sicp.py --host 192.168.1.50 switch-on-delay set off
python3 sicp.py --host 192.168.1.50 switch-on-delay set auto
python3 sicp.py --host 192.168.1.50 switch-on-delay set 20
python3 sicp.py --host 192.168.1.50 switch-on-delay set 20s
```

Protocol:

| Operation | DATA[0] | Values |
|---|---:|---|
| GET/report | `0x55` | `0x00` off, `0x01` auto, `0x02..0xFF` seconds |
| SET | `0x54` | `0x00` off, `0x01` auto, `0x02..0xFF` seconds |

## Frame Compensation

Read or set horizontal and vertical frame-compensation values:

```bash
python3 sicp.py --host 192.168.1.50 frame-compensation horizontal get
python3 sicp.py --host 192.168.1.50 frame-compensation horizontal set 3
python3 sicp.py --host 192.168.1.50 frame-compensation vertical get
python3 sicp.py --host 192.168.1.50 frame-compensation vertical set 3
```

Protocol:

| Axis | Operation | DATA[0] | Values |
|---|---|---:|---|
| Horizontal | GET/report | `0x5E` | `0x00..0xFF` |
| Horizontal | SET | `0x5F` | `0x00..0xFF` |
| Vertical | GET/report | `0x67` | `0x00..0xFF` |
| Vertical | SET | `0x68` | `0x00..0xFF` |

## AnyTile

Read or set AnyTile custom canvas tiling:

```bash
python3 sicp.py --host 192.168.1.50 anytile get
python3 sicp.py --host 192.168.1.50 anytile set \
  --enable yes --rotation 90 \
  --h-start 0 --v-start 0 --h-size 1920 --v-size 1080
```

Read or set the AnyTile resolution mode:

```bash
python3 sicp.py --host 192.168.1.50 anytile resolution get
python3 sicp.py --host 192.168.1.50 anytile resolution set fhd
python3 sicp.py --host 192.168.1.50 anytile resolution set uhd4k
```

Auxiliary AnyTile ID commands:

```bash
python3 sicp.py --host 192.168.1.50 anytile assign-id --monitor-id 3 --group-id 4
python3 sicp.py --host 192.168.1.50 anytile display-id set 3
```

Protocol:

| Command | Operation | DATA[0] | Fields |
|---|---|---:|---|
| AnyTile canvas | GET/report | `0x4A` | enable, rotation, input H/V start, input H/V size |
| AnyTile canvas | SET | `0x4B` | same as GET/report |
| Resolution mode | GET/report | `0x4E` | `0x00` default, `0x01` FHD, `0x02` UHD4K |
| Resolution mode | SET | `0x4F` | `0x00` default, `0x01` FHD, `0x02` UHD4K |
| Assign IDs | SET | `0xC0` | monitor ID, group ID |
| Display monitor ID | SET | `0x4C` | monitor ID |

AnyTile numeric fields are unsigned 16-bit values encoded little-endian in the
protocol. The vendor notes say these commands only work on supported Dragon /
Himalaya platforms when canvas tiling is activated from the admin menu.

## Power Saving Mode

Read or set the Smart Power power-saving level:

```bash
python3 sicp.py --host 192.168.1.50 power-saving get
python3 sicp.py --host 192.168.1.50 power-saving set off
python3 sicp.py --host 192.168.1.50 power-saving set low
python3 sicp.py --host 192.168.1.50 power-saving set medium
python3 sicp.py --host 192.168.1.50 power-saving set high
```

Protocol:

| Operation | DATA[0] | Values |
|---|---:|---|
| GET/report | `0xDE` | `0x00` off, `0x01` low, `0x02` medium, `0x03` high |
| SET | `0xDD` | `0x00` off, `0x01` low, `0x02` medium, `0x03` high |

The vendor notes say `low` is currently defined as the same as `off`. This
command controls active-on power-saving and can affect picture quality depending
on platform support.

## APM Status

Read or set Advanced Power Management status:

```bash
python3 sicp.py --host 192.168.1.50 apm-status get
python3 sicp.py --host 192.168.1.50 apm-status set off
python3 sicp.py --host 192.168.1.50 apm-status set on
python3 sicp.py --host 192.168.1.50 apm-status set mode-1
python3 sicp.py --host 192.168.1.50 apm-status set mode-2
```

Protocol:

| Operation | DATA[0] | Values |
|---|---:|---|
| GET/report | `0xD1` | `0x00` off, `0x01` on, `0x02` mode 1, `0x03` mode 2 |
| SET | `0xD0` | `0x00` off, `0x01` on, `0x02` mode 1, `0x03` mode 2 |

Mode 1 means TCP off / WOL on. Mode 2 means TCP on / WOL off. The vendor notes
say Himalaya supports off/mode 1/mode 2, while Eagle 1.3 supports on/off.

## Power Saving Mode Status

Read or set the power-saving mode status:

```bash
python3 sicp.py --host 192.168.1.50 power-saving-status get
python3 sicp.py --host 192.168.1.50 power-saving-status set rgb-off-video-off
python3 sicp.py --host 192.168.1.50 power-saving-status set rgb-on-video-on
python3 sicp.py --host 192.168.1.50 power-saving-status set mode-1
python3 sicp.py --host 192.168.1.50 power-saving-status set mode-4
```

Protocol:

| Operation | DATA[0] | Values |
|---|---:|---|
| GET/report | `0xD3` | `0x00` RGB off/video off, `0x01` RGB off/video on, `0x02` RGB on/video off, `0x03` RGB on/video on, `0x04..0x07` mode 1..4 |
| SET | `0xD2` | `0x00` RGB off/video off, `0x01` RGB off/video on, `0x02` RGB on/video off, `0x03` RGB on/video on, `0x04..0x07` mode 1..4 |

The typed CLI names are `rgb-off-video-off`, `rgb-off-video-on`,
`rgb-on-video-off`, `rgb-on-video-on`, and `mode-1` through `mode-4`.

## Serial Code

Read the monitor serial code / production code:

```bash
python3 sicp.py --host 192.168.1.50 serial-code get
```

Protocol:

| Operation | DATA[0] | Fields |
|---|---:|---|
| GET/report | `0x15` | 14 ASCII serial-code characters |

## Light Sensor

Read or set the light sensor state:

```bash
python3 sicp.py --host 192.168.1.50 light-sensor get
python3 sicp.py --host 192.168.1.50 light-sensor set off
python3 sicp.py --host 192.168.1.50 light-sensor set on
```

Protocol:

| Operation | DATA[0] | Values |
|---|---:|---|
| GET/report | `0x25` | `0x00` off, `0x01` on, `0xFF` hardware unavailable |
| SET | `0x24` | `0x00` off, `0x01` on |

## OSD Rotating

Read or set the OSD menu rotation state:

```bash
python3 sicp.py --host 192.168.1.50 osd-rotating get
python3 sicp.py --host 192.168.1.50 osd-rotating set off
python3 sicp.py --host 192.168.1.50 osd-rotating set on
```

Protocol:

| Operation | DATA[0] | Values |
|---|---:|---|
| GET/report | `0x27` | `0x00` off, `0x01` on |
| SET | `0x26` | `0x00` off, `0x01` on |

## Display Orientation

Read or set the display orientation fields:

```bash
python3 sicp.py --host 192.168.1.50 display-orientation get
python3 sicp.py --host 192.168.1.50 display-orientation set \
  --auto-rotate off --osd landscape --image-all on \
  --window1 off --window2 off --window3 off --window4 off
```

Protocol:

| Operation | DATA[0] | DATA fields |
|---|---:|---|
| GET/report | `0x16` | auto rotate, OSD rotation, image all, window 1, window 2, window 3, window 4 |
| SET | `0x17` | same as GET/report |

Accepted values:

| Field | Values |
|---|---|
| `--auto-rotate` | `off`, `on` |
| `--osd` | `landscape`, `portrait` |
| `--image-all` | `off`, `on`, `clockwise`, `counter-clockwise` |
| `--window1` through `--window4` | `off`, `on` |

The vendor notes say Himalaya 2.0 only supports OSD rotation and image rotation
on the main window. CRD50 does not support image OSD rotation, and the OSD is
rotated together with the image.

## Information OSD

Read or set the Information OSD feature:

```bash
python3 sicp.py --host 192.168.1.50 information-osd get
python3 sicp.py --host 192.168.1.50 information-osd set off
python3 sicp.py --host 192.168.1.50 information-osd set 30
python3 sicp.py --host 192.168.1.50 information-osd set 60
```

Protocol:

| Operation | DATA[0] | Values |
|---|---:|---|
| GET/report | `0x2D` | `0x00` off, `0x01..0x3C` values 1..60 seconds |
| SET | `0x2C` | `0x00` off, `0x01..0x3C` values 1..60 seconds |

## MEMC Effect

Read or set MEMC motion smoothing level:

```bash
python3 sicp.py --host 192.168.1.50 memc get
python3 sicp.py --host 192.168.1.50 memc set off
python3 sicp.py --host 192.168.1.50 memc set medium
python3 sicp.py --host 192.168.1.50 memc set high
```

Protocol:

| Operation | DATA[0] | Values |
|---|---:|---|
| GET/report | `0x29` | `0x00` off, `0x01` low, `0x02` medium, `0x03` high |
| SET | `0x28` | `0x00` off, `0x01` low, `0x02` medium, `0x03` high |

## Touch Feature

Read or set the touch feature state:

```bash
python3 sicp.py --host 192.168.1.50 touch-feature get
python3 sicp.py --host 192.168.1.50 touch-feature set off
python3 sicp.py --host 192.168.1.50 touch-feature set on
```

Protocol:

| Operation | DATA[0] | Values |
|---|---:|---|
| GET/report | `0x1F` | `0x00` off, `0x01` on |
| SET | `0x1E` | `0x00` off, `0x01` on |

The vendor notes say Himalaya 1.0/1.2 and Dragon 1.x/2.0 platforms do not
support this command.

## Noise Reduction

Read or set the noise reduction level:

```bash
python3 sicp.py --host 192.168.1.50 noise-reduction get
python3 sicp.py --host 192.168.1.50 noise-reduction set off
python3 sicp.py --host 192.168.1.50 noise-reduction set middle
python3 sicp.py --host 192.168.1.50 noise-reduction set high
python3 sicp.py --host 192.168.1.50 noise-reduction set default
```

Protocol:

| Operation | DATA[0] | Values |
|---|---:|---|
| GET/report | `0x2B` | `0x00` off, `0x01` low, `0x02` middle, `0x03` high, `0x04` default |
| SET | `0x2A` | `0x00` off, `0x01` low, `0x02` middle, `0x03` high, `0x04` default |

The `default` value is documented as only valid for Challenger 2.1 platforms.
The CLI also accepts `medium` as an alias for `middle`.

## Scan Mode

Read or set the scan mode:

```bash
python3 sicp.py --host 192.168.1.50 scan-mode get
python3 sicp.py --host 192.168.1.50 scan-mode set over-scan
python3 sicp.py --host 192.168.1.50 scan-mode set under-scan
python3 sicp.py --host 192.168.1.50 scan-mode set off
python3 sicp.py --host 192.168.1.50 scan-mode set custom-25
```

Protocol:

| Operation | DATA[0] | Values |
|---|---:|---|
| GET/report | `0x51` | `0x00` over scan, `0x01` under scan, `0x02` off, `0x03..0x1C` custom 0..25 |
| SET | `0x50` | `0x00` over scan, `0x01` under scan, `0x02` off, `0x03..0x1C` custom 0..25 |

The extended `custom-0` through `custom-25` range is documented as only valid
for Challenger 2.1 platforms. The CLI also accepts `overscan`, `underscan`, and
raw byte values such as `0x1C`.

## Scan Conversion

Read or set the scan conversion mode:

```bash
python3 sicp.py --host 192.168.1.50 scan-conversion get
python3 sicp.py --host 192.168.1.50 scan-conversion set progressive
python3 sicp.py --host 192.168.1.50 scan-conversion set interlace
```

Protocol:

| Operation | DATA[0] | Values |
|---|---:|---|
| GET/report | `0x53` | `0x00` progressive, `0x01` interlace |
| SET | `0x52` | `0x00` progressive, `0x01` interlace |

The CLI also accepts `interlaced` as an alias for `interlace`. The vendor notes
say Himalaya 1.0/1.2 and Dragon 1.x/1.6 platforms do not support this command.

## Pixel Shift

Read or set the pixel shift interval:

```bash
python3 sicp.py --host 192.168.1.50 pixel-shift get
python3 sicp.py --host 192.168.1.50 pixel-shift set off
python3 sicp.py --host 192.168.1.50 pixel-shift set 50
python3 sicp.py --host 192.168.1.50 pixel-shift set 900s
python3 sicp.py --host 192.168.1.50 pixel-shift set auto
```

Protocol:

| Operation | DATA[0] | Values |
|---|---:|---|
| GET/report | `0xB1` | `0x00` off, `0x01..0x5A` 10..900 seconds, `0x5B` auto |
| SET | `0xB2` | `0x00` off, `0x01..0x5A` 10..900 seconds, `0x5B` auto |

Seconds must be a multiple of 10 from `10` to `900`. The CLI accepts forms like
`50`, `50s`, and `50-seconds`. The vendor notes say this command is only
available on Dragon 1.0 and Dragon 1.5 platforms from a later firmware version.

## Human Sensor

Read or set the external human sensor timeout:

```bash
python3 sicp.py --host 192.168.1.50 human-sensor get
python3 sicp.py --host 192.168.1.50 human-sensor set off
python3 sicp.py --host 192.168.1.50 human-sensor set 30-mins
python3 sicp.py --host 192.168.1.50 human-sensor set 60-mins
```

Protocol:

| Operation | DATA[0] | Values |
|---|---:|---|
| GET/report | `0xB3` | `0x00` off, `0x01` 10 mins, `0x02` 20 mins, `0x03` 30 mins, `0x04` 40 mins, `0x05` 50 mins, `0x06` 60 mins, `0xFF` hardware unavailable |
| SET | `0xB4` | `0x00` off, `0x01` 10 mins, `0x02` 20 mins, `0x03` 30 mins, `0x04` 40 mins, `0x05` 50 mins, `0x06` 60 mins |

## Factory Reset

Perform a factory reset:

```bash
python3 sicp.py --host 192.168.1.50 factory-reset set
```

Protocol:

| Operation | DATA[0] |
|---|---:|
| SET | `0x56` |

The vendor section lists this reset as affecting many display settings,
including input controls, power at cold start, auto signal detection, video
parameters, color settings, picture format, volume, smart power, tiling, OSD,
noise reduction, scan mode, and switch-on delay.

## Power On Logo

Read or set the power-on logo state:

```bash
python3 sicp.py --host 192.168.1.50 power-on-logo get
python3 sicp.py --host 192.168.1.50 power-on-logo set off
python3 sicp.py --host 192.168.1.50 power-on-logo set on
python3 sicp.py --host 192.168.1.50 power-on-logo set user
```

Protocol:

| Operation | DATA[0] | Values |
|---|---:|---|
| GET/report | `0x3F` | `0x00` off, `0x01` on, `0x02` user |
| SET | `0x3E` | `0x00` off, `0x01` on, `0x02` user |

## Off Timer

Read or set the off timer:

```bash
python3 sicp.py --host 192.168.1.50 off-timer get
python3 sicp.py --host 192.168.1.50 off-timer set off
python3 sicp.py --host 192.168.1.50 off-timer set 5
python3 sicp.py --host 192.168.1.50 off-timer set 5-hours
```

Protocol:

| Operation | DATA[0] | Values |
|---|---:|---|
| GET/report | `0x91` | `0x00` off, `0x01` 1 hour, ..., `0x18` 24 hours |
| SET | `0x92` | `0x00` off, `0x01` 1 hour, ..., `0x18` 24 hours |

The set command accepts `off`, `0`, and hour values from `1` to `24`, with
optional forms such as `5h` or `5-hours`.

## ECO Mode

Read or set ECO mode:

```bash
python3 sicp.py --host 192.168.1.50 eco-mode get
python3 sicp.py --host 192.168.1.50 eco-mode set low-power-standby
python3 sicp.py --host 192.168.1.50 eco-mode set normal
```

Protocol:

| Operation | DATA[0] | Values |
|---|---:|---|
| GET/report | `0x63` | `0x00` low power standby, `0x01` normal |
| SET | `0x64` | `0x00` low power standby, `0x01` normal |

The typed CLI accepts `low-power-standby`, `low-power`, `low`, `standby`, and
`normal`.

## Picture Style

Read or set picture style:

```bash
python3 sicp.py --host 192.168.1.50 picture-style get
python3 sicp.py --host 192.168.1.50 picture-style set highbright
python3 sicp.py --host 192.168.1.50 picture-style set natural
python3 sicp.py --host 192.168.1.50 picture-style set energy-saving
```

Protocol:

| Operation | DATA[0] | Values |
|---|---:|---|
| GET/report | `0x65` | `0x00` highbright, `0x01` sRGB, `0x02` vivid, `0x03` natural, `0x04` standard, `0x05` video, `0x06` static signage, `0x07` text, `0x08` energy saving, `0x09` soft, `0x0A` user |
| SET | `0x66` | `0x00` highbright, `0x01` sRGB, `0x02` vivid, `0x03` natural, `0x04` standard, `0x05` video, `0x06` static signage, `0x07` text, `0x08` energy saving, `0x09` soft, `0x0A` user |

The typed CLI names are `highbright`, `srgb`, `vivid`, `natural`, `standard`,
`video`, `static-signage`, `text`, `energy-saving`, `soft`, and `user`.

## Group ID

Read or set the display Group ID:

```bash
python3 sicp.py --host 192.168.1.50 group-id get
python3 sicp.py --host 192.168.1.50 group-id set 1
python3 sicp.py --host 192.168.1.50 group-id set 0xFE
python3 sicp.py --host 192.168.1.50 group-id set off
```

Protocol:

| Operation | DATA[0] | Values |
|---|---:|---|
| GET/report | `0x5D` | `0x01..0xFE` group ID 1..254, `0xFF` off |
| SET | `0x5C` | `0x01..0xFE` group ID 1..254, `0xFF` off |

This command changes the monitor's stored Group ID. The global `--group-id`
option still controls which SICP group byte the CLI uses when sending packets.

## Monitor ID

Set the display Monitor ID:

```bash
python3 sicp.py --host 192.168.1.50 --monitor-id 3 monitor-id set 6
python3 sicp.py --host 192.168.1.50 monitor-id set 0xFF
```

Protocol:

| Operation | DATA[0] | Values |
|---|---:|---|
| SET | `0x69` | `0x01..0xFF` monitor ID 1..255 |

This command changes the monitor's stored Monitor ID. The global `--monitor-id`
option still controls which monitor address the CLI sends the command to.

## MicroSD And USB Ports Lock

Read or set whether the MicroSD and USB ports are locked:

```bash
python3 sicp.py --host 192.168.1.50 ports-lock get
python3 sicp.py --host 192.168.1.50 ports-lock set unlocked
python3 sicp.py --host 192.168.1.50 ports-lock set locked
```

Protocol:

| Operation | DATA[0] | Values |
|---|---:|---|
| GET/report | `0xF2` | `0x00` unlocked, `0x01` locked |
| SET | `0xF1` | `0x00` unlocked, `0x01` locked |

The set command also accepts `enable`/`enabled` for unlocked and
`disable`/`disabled` for locked.

## Scheduling Parameters

Read or set scheduling parameters for page `1` through `7`:

```bash
python3 sicp.py --host 192.168.1.50 schedule get 1
python3 sicp.py --host 192.168.1.50 schedule set 1 --enabled --start 06:30 --end 22:00 --source hdmi --days every-day
python3 sicp.py --host 192.168.1.50 schedule set 1 --disabled --start null --end null --source null --days 0x00
python3 sicp.py --host 192.168.1.50 schedule set 2 --enabled --start 08:00 --end 18:00 --source browser --days weekdays --tag 1
```

Protocol:

| Operation | DATA[0] | Values |
|---|---:|---|
| GET/report | `0x5B` | GET sends page `1..7`; report returns enable state, start/end time, source, days, and optional tag |
| SET | `0x5A` | `DATA[1]` is page in high nibble and enable state in low nibble, followed by start/end time, source, days, and optional tag |

Time fields use `HH:MM`, or `null` for the protocol null time (`24:60`).
Source accepts existing input-source names plus `null`. Days accepts names such
as `every-day`, `weekdays`, `weekends`, comma-separated day names, or a raw byte
like `0xFF`. Optional `--tag` accepts `1..7`.

## Video Signal Present

Read whether the monitor currently has a video signal:

```bash
python3 sicp.py --host 192.168.1.50 video-signal get
```

Protocol:

| Operation | DATA[0] | Values |
|---|---:|---|
| GET/report | `0x59` | `0x00` not present, `0x01` present |

## Lock Functions

Read IR remote or keypad lock state:

```bash
python3 sicp.py --host 192.168.1.50 lock ir get
python3 sicp.py --host 192.168.1.50 lock keypad get
```

Set IR remote lock state:

```bash
python3 sicp.py --host 192.168.1.50 lock ir set unlock-all
python3 sicp.py --host 192.168.1.50 lock ir set lock-all
python3 sicp.py --host 192.168.1.50 lock ir set lock-all-but-power
python3 sicp.py --host 192.168.1.50 lock ir set lock-all-but-volume
python3 sicp.py --host 192.168.1.50 lock ir set primary
python3 sicp.py --host 192.168.1.50 lock ir set secondary
python3 sicp.py --host 192.168.1.50 lock ir set lock-all-except-power-volume
```

Set keypad lock state:

```bash
python3 sicp.py --host 192.168.1.50 lock keypad set unlock-all
python3 sicp.py --host 192.168.1.50 lock keypad set lock-all
python3 sicp.py --host 192.168.1.50 lock keypad set lock-all-but-power
python3 sicp.py --host 192.168.1.50 lock keypad set lock-all-but-volume
python3 sicp.py --host 192.168.1.50 lock keypad set lock-all-except-power-volume
```

Protocol:

| Target | Operation | DATA[0] | Values |
|---|---|---:|---|
| IR remote | GET/report | `0x1D` | `0x01` unlock all, `0x02` lock all, `0x03` lock all but power, `0x04` lock all but volume, `0x05` primary, `0x06` secondary, `0x07` lock all except power and volume |
| IR remote | SET | `0x1C` | same as IR remote GET/report |
| Keypad | GET/report | `0x1B` | `0x01` unlock all, `0x02` lock all, `0x03` lock all but power, `0x04` lock all but volume, `0x07` lock all except power and volume |
| Keypad | SET | `0x1A` | same as Keypad GET/report |

The vendor notes say keypad states `lock-all-but-power`,
`lock-all-but-volume`, and `lock-all-except-power-volume` are not valid for
10BDL3151T and 24BDL2451T.

## Configuration Collect/Apply

Collect every safe implemented get/set configuration pair:

```bash
python3 sicp.py --host 192.168.1.50 config collect
python3 sicp.py --host 192.168.1.50 --json config collect > display-config.json
```

Collection tolerates unsupported or missing commands. If a display NACKs or
does not answer a setting query, collection continues; human output prints an
`ERROR` line for that setting, and JSON output records the failure under
`errors`. The command exits successfully as long as at least one setting was
collected.

Apply a JSON configuration previously produced by `config collect --json`:

```bash
python3 sicp.py --host 192.168.1.50 config apply display-config.json
python3 sicp.py --host 192.168.1.50 config apply -
```

By default, apply stops at the first failed setting. Use `--continue-on-error`
to try the remaining settings, and `--ignore-unknown` to skip JSON keys that
this CLI does not know how to apply:

```bash
python3 sicp.py --host 192.168.1.50 config apply display-config.json --continue-on-error
python3 sicp.py --host 192.168.1.50 config apply display-config.json --ignore-unknown
```

Use `--only` to limit collection or apply to specific setting keys:

```bash
python3 sicp.py --host 192.168.1.50 --json config collect --only power,volume_mute
python3 sicp.py --host 192.168.1.50 config apply display-config.json --only power
```

Available setting keys are the keys in the JSON `settings` object:

```text
power, power_cold_start, input_source, auto_signal, failover, fan_speed,
volume, volume_limit_speaker, volume_limit_audio, volume_audio, volume_mute,
lock_ir, lock_keypad, video_parameters, picture_format, color_temperature,
rgb_parameters, color_temperature_100k, power_saving, tiling, switch_on_delay,
frame_compensation_horizontal, frame_compensation_vertical, anytile,
anytile_resolution, power_saving_status, apm_status, light_sensor,
osd_rotating, display_orientation, touch_feature, noise_reduction, scan_mode,
scan_conversion, pixel_shift, memc, information_osd, human_sensor,
power_on_logo, off_timer, eco_mode, picture_style, group_id, ports_lock,
schedule_1, schedule_2, schedule_3, schedule_4, schedule_5, schedule_6,
schedule_7
```

The JSON schema name is `philips-sicp-config-v1`. Operational, destructive, and
read-only commands such as factory reset, restart, raw DATA[], temperature,
operating hours, serial code, and video-signal status are intentionally excluded.

## Raw DATA[] Command

The raw command sends DATA[] bytes while the client automatically adds
`MsgSize`, `Control`, `Group`, and `Checksum`.

Examples:

```bash
python3 sicp.py --host 192.168.1.50 raw data 19
python3 sicp.py --host 192.168.1.50 raw data AD
python3 sicp.py --host 192.168.1.50 raw data "AD 0D 00 01 00"
python3 sicp.py --host 192.168.1.50 raw data AD 0D 00 01 00
```

Raw DATA[] bytes are hex by default, so `19` means `0x19`. Decimal can be passed
with the `d:` prefix:

```bash
python3 sicp.py --host 192.168.1.50 raw data d:25
```

Normal output prints the reply DATA[] bytes:

```text
Reply DATA: 19 02
```

Use `--verbose` to see complete packets:

```bash
python3 sicp.py --host 192.168.1.50 --verbose raw data 19
```

## Development Reference

- [docs/Philips_SICP_Python_Client_Development.md](docs/Philips_SICP_Python_Client_Development.md) contains implementation notes and observed behavior.
- [docs/index.md](docs/index.md) links generated command-group reference files under `docs/commands/`.
- [docs/Philips_SICP_Commands.md](docs/Philips_SICP_Commands.md) is the larger transcribed command reference.

## Tests

Run the standard-library test suite:

```bash
python3 -m unittest discover -v
```

or with `uv`:

```bash
uv run python -m unittest discover -v
```

Run static checks:

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy
```

Compile-check the code:

```bash
python3 -m py_compile sicp.py philips_sicp/*.py tests/*.py
```

GitHub CI runs Ruff linting, Ruff formatting checks, mypy, the test suite on
Python `3.10`, `3.11`, `3.12`, and `3.13`, compile-checks the source,
smoke-tests the `sicp` console command, and builds the package with `uv build`.
