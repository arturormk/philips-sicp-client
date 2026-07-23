# Serial Code

Source: `docs/Philips_SICP_Commands.md`, lines 3716-3761.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 7.5.1 Message-Get
- 7.5.2 Message-Report

## DATA[0] Codes

- `0x15` - Serial Code Get                            Command requests the display to report its Serial Code
- `0x15` - Serial Code – Report                            Command reports Serial Code

## Source Excerpt
#### 7.5 Serial Code

```text

```

##### 7.5.1 Message-Get

```text

Bytes        Bytes Description                      Bits       Description
DATA[0]      0x15 = Serial Code Get                            Command requests the display to report its Serial Code
                                                               Number (Production code) 14 digits

Example: (Display address 01)
MsgSize      Control Group          Data (0)     Checksum
0x05         0x01        0x00       0x15         0x11

```

##### 7.5.2 Message-Report

```text

Bytes        Bytes Description                          Bits        Description
DATA[0]      0x15 = Serial Code – Report                            Command reports Serial Code
DATA[1]      1st Character                                          Character acc. ASCII character map (HEX)
DATA[2]      2nd Character
DATA[3]      3rd Character

DATA[14]     14th Character                                         Character acc. ASCII character map (HEX)

Example: Current Display settings: Serial Code = HA1A0917123456 (Display address 01)
MsgSize    Control Group Data (0) Data (1) Data (2) Data (3) Data (4)                       Data (5)   Data (6)     Data (7)
0x13       0x01        0x00         0x15       0x48     0x41     0x31       0x41            0x30       0x39         0x31





Data (8)   Data (9)    Data (10)   Data (11)     Data (12)     Data (13)     Data (14)   Checksum
0x37       0x31        0x32        0x33          0x34          0x35          0x36        0x76


```
