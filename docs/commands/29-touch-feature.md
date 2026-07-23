# Touch Feature

Source: `docs/Philips_SICP_Commands.md`, lines 4477-4543.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 7.13.1 Message-Get
- 7.13.2 Message-Report
- 7.13.3 Message-Set

## DATA[0] Codes

- `0x1F` - Touch Feature – Get                         Command requests the display to report its current
- `0x1F` - Touch Feature – Report                         Command reports the Touch Feature enabled or
- `0x1E` - Touch Feature – Set                         Command to set the Touch Feature of the display

## Source Excerpt
#### 7.13 Touch Feature

```text
The command is used to set/get the Touch Feature as it is defined as below.

NOTE: Himalaya 1.0 & 1.2 Dragon 1.x & 2.0 platform does NOT support this commands.



```

##### 7.13.1 Message-Get

```text


 Bytes          Bytes Description                       Bits       Description
 DATA[0]        0x1F = Touch Feature – Get                         Command requests the display to report its current
                                                                   Touch Feature status

Example: (Display address 01)
 MsgSize Control Group                 Data (0)     Checksum
 0x05        0x01        0x00          0x1F         0x1B


```

##### 7.13.2 Message-Report

```text


 Bytes          Bytes Description                           Bits      Description
 DATA[0]        0x1F = Touch Feature – Report                         Command reports the Touch Feature enabled or
                                                                      disabled
 DATA[1]        On / Off                                              0x00 = Off
                                                                      0x01 = On


Example: Current Display Touch Feature settings: Off (Display address 01)
 MsgSize Control Group              Data (0)      Data (1)      Checksum
 0x06       0x01         0x00       0x1F          0x00          0x18


```

##### 7.13.3 Message-Set

```text


 Bytes          Bytes Description                       Bits       Description
 DATA[0]        0x1E = Touch Feature – Set                         Command to set the Touch Feature of the display
                                                                   enabled or disabled
 DATA[1]        On /Off                                            0x00 = Off
                                                                   0x01 = On

Example: Set the Display to the fallowing: Touch Feature off (Display address 01)
 MsgSize Control Group                 Data (0)    Data (1)      Checksum
 0x06        0x01        0x00          0x1E        0x00          0x19





```
