# OSD Rotating

Source: `docs/Philips_SICP_Commands.md`, lines 4193-4251.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 7.10.1 Message-Get
- 7.10.2 Message-Report
- 7.10.3 Message-Set

## DATA[0] Codes

- `0x27` - OSD Rotating – Get                          Command requests the display to report its current
- `0x27` - OSD Rotating – Report                          Command reports OSD Rotating Setting
- `0x26` - OSD Rotating – Set                          Command to change the OSD Rotating setting of the

## Source Excerpt
#### 7.10 OSD Rotating

```text
The command is used to set/get the OSD menu direction as it is defined as below.


```

##### 7.10.1 Message-Get

```text


 Bytes          Bytes Description                       Bits       Description
 DATA[0]        0x27 = OSD Rotating – Get                          Command requests the display to report its current
                                                                   OSD rotating status

Example: (Display address 01)
 MsgSize Control Group                Data (0)      Checksum
 0x05        0x01        0x00         0x27          0x23


```

##### 7.10.2 Message-Report

```text


 Bytes          Bytes Description                           Bits      Description
 DATA[0]        0x27 = OSD Rotating – Report                          Command reports OSD Rotating Setting
 DATA[1]        On / Off                                              0x00 = Off
                                                                      0x01 = On

Example: Current Display settings: Off and On (Display address 01)
 MsgSize Control Group                 Data (0)    Data (1)     Checksum
 0x06       0x01         0x00          0x27        0x00         0x20
 0x06       0x01         0x00          0x27        0x01         0x21


```

##### 7.10.3 Message-Set

```text


 Bytes          Bytes Description                       Bits       Description
 DATA[0]        0x26 = OSD Rotating – Set                          Command to change the OSD Rotating setting of the
                                                                   display
 DATA[1]        On / Off                                           0x00 = Off
                                                                   0x01 = On

Example: Set the Display to the fallowing: OSD rotating Off (Display address 01)
 MsgSize Control Group                 Data (0)    Data (1)      Checksum
 0x06        0x01        0x00          0x26        0x00          0x21

```
