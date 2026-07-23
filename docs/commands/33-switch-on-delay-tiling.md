# Switch On Delay (Tiling)

Source: `docs/Philips_SICP_Commands.md`, lines 4754-4828.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 7.17.1 Message-Get
- 7.17.2 Message-Report
- 7.17.3 Message-Set

## DATA[0] Codes

- `0x55` - Switch On Delay                                    Command requests the display to report its current
- `0x55` - Switch On Delay (Tiling)                              Command reports the Switch On Delay (Tiling)
- `0x54` - Switch On Delay                                    Command to set the Switch On Delay (Tiling)

## Source Excerpt
#### 7.17 Switch On Delay (Tiling)

```text
The command is used to set/get the Switch on Delay (Tiling) Feature as it is defined as below.
Value in (OFF (0), 2, 4, 6, 8, 10, 20, 30, 40, 50, Auto (60))

```

##### 7.17.1 Message-Get

```text

 Bytes             Bytes Description                              Bits       Description
 DATA[0]           0x55 = Switch On Delay                                    Command requests the display to report its current
                   (Tiling) Feature – Get                                    Switch On Delay (Tiling) Feature status

Example: (Display address 01)
 MsgSize Control Group                         Data (0)         Checksum
 0x05        0x01        0x00                  0x55             0x51


```

##### 7.17.2 Message-Report

```text

 Bytes             Bytes Description                                  Bits      Description
 DATA[0]           0x55 = Switch On Delay (Tiling)                              Command reports the Switch On Delay (Tiling)
                   Feature – Report                                             Feature enabled or disabled
 DATA[1]           Switch on delay time                                         0x00 = Off
                                                                                0x01 = Auto
                                                                                0x02 = 2 seconds
                                                                                0x03 = 3 seconds
                                                                                0x04 = 4 seconds
                                                                                ………………….
                                                                                0xFD = 253 seconds
                                                                                0xFE = 254 seconds
                                                                                0xFF = 255 seconds

Example: Current Display Switch On Delay (Tiling) Feature settings: Off (Display address 01)
 MsgSize Control Group              Data (0)       Data (1)     Checksum
 0x06       0x01         0x00       0x55           0x01         0x53


```

##### 7.17.3 Message-Set

```text


 Bytes             Bytes Description                               Bits      Description
 DATA[0]           0x54 = Switch On Delay                                    Command to set the Switch On Delay (Tiling)
                   (Tiling) Feature – Set                                    Feature of the display enabled or disabled
 DATA[1]           Switch on delay time                                      0x00 = Off
                                                                             0x01 = Auto
                                                                             0x02 = 2 seconds
                                                                             0x03 = 3 seconds
                                                                             0x04 = 4 seconds
                                                                             ………………….
                                                                             0xFD = 253 seconds
                                                                             0xFE = 254 seconds
                                                                             0xFF = 255 seconds

Example: Set the Display to the fallowing: Switch On Delay (Tiling) Feature: Off (Display address 01)
 MsgSize Control Group                 Data (0)     Data (1)     Checksum
 0x06        0x01        0x00          0x54         0x00         0x53





```
