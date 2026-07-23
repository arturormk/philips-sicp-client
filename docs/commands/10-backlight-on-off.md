# Backlight On-Off

Source: `docs/Philips_SICP_Commands.md`, lines 2062-2113.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 4.7.1 Get backlight status
- 4.7.2 Set backlight on-off

## DATA[0] Codes

- `0x71` - Backlight – Get                                Command to restart monitor
- `0x72` - Backlight – Set                                Command to switch on-off the backlights

## Source Excerpt
#### 4.7 Backlight On-Off

##### 4.7.1 Get backlight status

```text

  Check if the backlight is off or on
  Supported on models : TBC

  Bytes   Bytes Description                            Bits     Description
  DATA[0] 0x71 = Backlight – Get                                Command to restart monitor


 Example: get the picture mute status
  MsgSize Control Group           Data (0)           Checksum
  0x05      0x01        0x00      0x71               0x50


  Report from monitor
  06 01 00 71 00 76 > get status : backlight is on
  06 01 00 71 01 77 > get status : backlight is off

```

##### 4.7.2 Set backlight on-off

```text

    Set the backlight on or off. (the audio will not be muted/unmuted)

    Message-Set

  Bytes   Bytes Description                            Bits     Description
  DATA[0] 0x72 = Backlight – Set                                Command to switch on-off the backlights

  DATA[1]                                                       0x00 = backlight on
                                                                0x01 = backlight off


 Example: mute the picture (Display address 01)
  MsgSize Control Group           Data (0) Data (1)                  Checksum
  0x06     0x01        0x00       0x72        0x01                   0x74

06 01 00 72 00 75 > set backlight on
06 01 00 72 01 74 > set backlight off


MESSAGES – VIDEO


```
