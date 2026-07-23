# Power Saving Mode

Source: `docs/Philips_SICP_Commands.md`, lines 3574-3641.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 7.2.1 Message-Get
- 7.2.2 Message-Report
- 7.2.3 Message-Set

## DATA[0] Codes

- `0xDE` - Smart Power –                     Command requests the display to get the specified Power
- `0xDE` - Smart Power –                     Command reports Power Saving Mode Setting
- `0xDD` - Smart Power –                      Command requests the display to set the specified Power

## Source Excerpt
#### 7.2 Power Saving Mode

```text

This command is used for dimming back light power consumption control. Different levels of power
consumptions can be achieved by using this command.

```

##### 7.2.1 Message-Get

```text

 Bytes        Bytes Description                 Bits   Description
 DATA[0]      0xDE = Smart Power –                     Command requests the display to get the specified Power
              Get                                      Saving Mode.

Example: Get the Smart Power Level (Display address 01)
 MsgSize Control Group              Data (0)     Checksum
 0x05       0x01       0x00         0xDE         0xDA





```

##### 7.2.2 Message-Report

```text

 Bytes          Bytes Description                Bits    Description
 DATA[0]        0xDE = Smart Power –                     Command reports Power Saving Mode Setting
                Report
 DATA[1]        Level of Smart Power                     0x00 = OFF
                control                                  0x01 = Low (defined to be same as OFF)
                                                         0x02 = Medium
                                                         0x03 = High

Example: Current Display settings: Power Saving Mode setting is Low (Display address 01)
 MsgSize Control Group                Data (0)    Data (1)      Checksum
 0x06       0x01       0x00           0xDE        0x01          0xD8

```

##### 7.2.3 Message-Set

```text

 Bytes         Bytes Description                 Bits    Description
 DATA[0]       0xDD = Smart Power –                      Command requests the display to set the specified Power
               Set                                       Saving Mode.
 DATA[1]       Level of Smart Power                      For the currently-defined Type = 0:
               control                                    0x00 = OFF         (no special action, default mode)
                                                          0x01 = Low         (defined to be same as OFF)
                                                          0x02 = Medium
                                                          0x03 = High        (highest power-saving mode)

Example: Set the Display to Medium Smart Power Level (Display address 01)
 MsgSize Control Group              Data (0)    Data (1)     Checksum
 0x06        0x01        0x00       0xDD        0x02         0xD8

Note1: This command controls the level of power-saving when the display is active-on.
Note2: Exactly how this feature is implemented, or whether it can be done at all, depends on the platform. It
      is possible that the picture quality might be compromised as a trade-off.

```
