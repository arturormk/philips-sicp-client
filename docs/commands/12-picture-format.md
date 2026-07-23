# Picture Format

Source: `docs/Philips_SICP_Commands.md`, lines 2509-2595.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 5.2.1 Message-Get
- 5.2.2 Message-Report
- 5.2.3 Message-Set

## DATA[0] Codes

- `0x3B` - Picture Format –                      Command requests the display to report its current
- `0x3B` - Picture Format –                             Command report to the host controller the
- `0x3A` - Picture Format –                         Command requests the display to set the specified

## Source Excerpt
#### 5.2 Picture Format

```text
This command is used to control the display screen format.

```

##### 5.2.1 Message-Get

```text

 Bytes           Bytes Description                 Bits       Description
 DATA[0]         0x3B = Picture Format –                      Command requests the display to report its current
                 Get                                          picture format

Example: (Display address 01)
 MsgSize Control Group               Data (0)      Checksum
 0x05        0x01        0x00        0x3B          0x3F


```

##### 5.2.2 Message-Report

```text

 Bytes           Bytes Description                        Bits       Description
 DATA[0]         0x3B = Picture Format –                             Command report to the host controller the
                 Report                                              current picture format of the display.
 DATA[1]         Picture Format*                          Bit 7..4   Not used.
                                                          Bit 3..0   Picture Format.
                                                                     0x00 = Normal (4:3)
                                                                     0x01 = Custom
                                                                     0x02 = Real (1:1)
                                                                     0x03 = Full
                                                                     0x04 = 21:9
                                                                     0x05 = Dynamic
                                                                     0x06 = 16:9

Special Note:-

DATA [1] value 0x05 = Dynamic not supported in 2016 Dragon 1.0 (see platform list).

* For further explanations, please see section 6.2.3 – Message-Set.

Example: Current Picture Format is Widescreen on Full Display (Display address 01)
 MsgSize Control Group               Data (0)    Data (0)      Checksum
 0x06       0x01         0x00        0x3B        0x03          0x3F


```

##### 5.2.3 Message-Set

```text

 Bytes           Bytes Description                 Bits          Description
 DATA[0]         0x3A = Picture Format –                         Command requests the display to set the specified
                 Set                                             picture format
 DATA[1]         Picture Format                    Bit 7..4      Not used.
                                                   Bit 3..0      Picture Format.
                                                                 0x00 = Normal
                                                                 0x01 = Custom
                                                                 0x02 = Real
                                                                 0x03 = Full
                                                                 0x04 = 21:9
                                                                 0x05 = Dynamic
                                                                 0x06 = 16:9





Special Note:-

DATA [1] value 0x05 = Dynamic not supported in 2016 Dragon 1.x (see platform list)

The display shall respond with NAV if it receives a Picture Format that is not relevant to its Display Aspect
Ratio.
The display shall ignore the [Picture Format – Set] if it receives a Picture Format that it cannot execute.

Example: Set Picture Format to Widescreen on Full Display (Display address 01)
 MsgSize Control Group               Data (0)     Data (0)     Checksum
 0x06        0x01        0x00        0x3A         0x03         0x3E

```
