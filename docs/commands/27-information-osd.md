# Information OSD

Source: `docs/Philips_SICP_Commands.md`, lines 4346-4407.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 7.11.1 Message-Get
- 7.11.2 Message-Report
- 7.11.3 Message-Set

## DATA[0] Codes

- `0x2D` - Information OSD                             Command requests the display to report its current
- `0x2D` - Information OSD                                Command reports the Information OSD Feature
- `0x2C` - Information OSD                             Command to set the Information OSD Feature of the

## Source Excerpt
#### 7.11 Information OSD

```text
 The command is used to set/get the Information OSD Feature as it is defined as below.


```

##### 7.11.1 Message-Get

```text


  Bytes         Bytes Description                       Bits       Description
  DATA[0]       0x2D = Information OSD                             Command requests the display to report its current
                Feature – Get                                      Information OSD Feature status

 Example: (Display address 01)
  MsgSize Control Group               Data (0)      Checksum
  0x05        0x01        0x00        0x2D          0x29


```

##### 7.11.2 Message-Report

```text


  Bytes         Bytes Description                           Bits      Description
  DATA[0]       0x2D = Information OSD                                Command reports the Information OSD Feature
                Feature – Report                                      enabled or disabled
  DATA[1]       Off, 1 – 60                                           0x00 = Off
                                                                      0x01 – 0x3C = 1 – 60

 Example: Current Display Information OSD Feature settings: Off (Display address 01)
  MsgSize Control Group               Data (0)    Data (1)      Checksum
  0x06       0x01         0x00        0x2D        0x00          0x2A


```

##### 7.11.3 Message-Set

```text





 Bytes          Bytes Description                       Bits       Description
 DATA[0]        0x2C = Information OSD                             Command to set the Information OSD Feature of the
                Feature – Set                                      display enabled or disabled
 DATA[1]        Off, 1 – 60                                        0x00 = Off
                                                                   0x01 – 0x3C = 1 – 60

Example: Set the Display to the fallowing: Information OSD Feature: Off (Display address 01)
 MsgSize Control Group                 Data (0)     Data (1)    Checksum
 0x06        0x01        0x00          0x2C         0x00        0x2B

```
