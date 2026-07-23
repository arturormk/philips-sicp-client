# ECO mode

Source: `docs/Philips_SICP_Commands.md`, lines 5352-5412.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 7.25.1 Message-report ECO mode
- 7.25.2 Message- Set ECO mode

## DATA[0] Codes

- `0x63` - Eco mode– Get                               Command requests the display to report its current
- `0x63` - ECO mode                                     Command reports the ECO mode
- `0x64` - ECO mode                                     Command set the ECO mode

## Source Excerpt
#### 7.25 ECO mode

```text
                  The command is used to set/get the ECO mode to normal or low power standby.

                  The command is only available on Phoenix 1 & 2 platform from firmware version: x.xxx (tbc) onwards.


 Bytes       Bytes Description                      Bits       Description
 DATA[0]    0x63 = Eco mode– Get                               Command requests the display to report its current
                                                               ECO mode value

Example: (Display address 01)
 MsgSize Control Group             Data (0)     Checksum
 0x05        0x01        0x00      0x63         0x67

```

##### 7.25.1 Message-report ECO mode

```text

   Bytes      Bytes Description                         Bits      Description
 DATA[0]      0x63 = ECO mode                                     Command reports the ECO mode
              status – Report                                     enabled or disabled
 DATA[1]      Low power standby or normal                         0x00 = low power standby
                                                                  0x01 = normal




Example: Current ECO Mode setting: (Display address 01)

 MsgSize    Control    Group        Data (0)      Data (1)       Checksum
 0x06       0x01       0x00         0x63          0x00           0x65              Low power standby
 0x06       0x01       0x00         0x63          0x01           0x64              normal

```

##### 7.25.2 Message- Set ECO mode

```text

   Bytes      Bytes Description                         Bits      Description
 DATA[0]      0x64 = ECO mode                                     Command set the ECO mode
              status – set                                        enabled or disabled
 DATA[1]      Low power standby or normal                         0x00 = low power standby
                                                                  0x01 = normal




Example: Current Display Power Saving Mode setting: RGB & Video off (Display address 01)
 MsgSize Control Group          Data (0) Data (1) Checksum
 0x06      0x01       0x00      0x64      0x00        0x63           Low power standby
 0x06      0x01       0x00      0x64      0x01        0x62           normal



```
