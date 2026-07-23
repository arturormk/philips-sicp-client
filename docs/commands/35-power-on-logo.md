# Power On logo

Source: `docs/Philips_SICP_Commands.md`, lines 4901-4964.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 7.19.1 Message-Get
- 7.19.2 Message-Report
- 7.19.3 Message-Set

## DATA[0] Codes

- `0x3F` - Power On logo status                      Command requests the display to report its
- `0x3F` - Power On logo status –                      Command reports the Power On logo
- `0x3E` - Power On logo status                      Command to set the Power On logo of the

## Source Excerpt
#### 7.19 Power On logo

```text
The command is used to set/get the Power on logo status as it is defined as below.

```

##### 7.19.1 Message-Get

```text


 Bytes       Bytes Description                     Bits       Description
 DATA[0]     0x3F = Power On logo status                      Command requests the display to report its
             – Get                                            current Power On logo status

Example: (Display address 01)
 MsgSize Control Group            Data (0)       Checksum
 0x05      0x01       0x00        0x3F           0x3B


```

##### 7.19.2 Message-Report

```text


 Bytes       Bytes Description                         Bits     Description
 DATA[0]     0x3F = Power On logo status –                      Command reports the Power On logo
             Report                                             enabled or disabled
 DATA[1]     Off / On / User                                    0x00 = Off
                                                                0x01 = On
                                                                0x02 = User

Example: Current Display Power On logo setting: Off (Display address 01)
 MsgSize Control Group          Data (0) Data (1)        Checksum
 0x06      0x01       0x00      0x3F        0x00         0x38


```

##### 7.19.3 Message-Set

```text


 Bytes       Bytes Description                     Bits       Description
 DATA[0]     0x3E = Power On logo status                      Command to set the Power On logo of the
             – Set                                            display enabled or disabled
 DATA[1]     Off / On / User                                  0x00 = Off
                                                              0x01 = On
                                                              0x02 = User

Example: Set the Display to the fallowing: Power on logo Off (Display address 01)
 MsgSize Control Group            Data (0) Data (1)       Checksum
 0x06      0x01       0x00        0x3E        0x00        0x39





```
