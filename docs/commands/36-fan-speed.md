# Fan Speed

Source: `docs/Philips_SICP_Commands.md`, lines 4965-5034.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 7.20.1 Message-Get
- 7.20.2 Message-Report
- 7.20.3 Message-Set

## DATA[0] Codes

- `0x62` - Fan Speed status –                           Command requests the display to report its
- `0x62` - Fan Speed status –                              Command reports the Fan Speed status
- `0x61` - Fan Speed status – Set                       Command to set the Fan Speed status of the

## Source Excerpt
#### 7.20 Fan Speed

```text
 The command is used to set/get the Fan Speed status as it is defined as below.

 NOTE: Dragon 1.x & 1.6 platform does not support Fan Speed commands.


```

##### 7.20.1 Message-Get

```text


  Bytes          Bytes Description                        Bits       Description
  DATA[0         0x62 = Fan Speed status –                           Command requests the display to report its
  ]              Get                                                 current Fan Speed status
Example: (Display address 01)
  MsgSize Control Group                  Data (0)       Checksum
  0x05        0x01        0x00           0x62           0x66


```

##### 7.20.2 Message-Report

```text


  Bytes          Bytes Description                            Bits      Description
  DATA[0         0x62 = Fan Speed status –                              Command reports the Fan Speed status
  ]              Report                                                 enabled or disabled
  DATA[1         Off / Auto / Low / Middle / High                       0x00 = Off
  ]                                                                     0x01 = Auto
                                                                        0x02 = Low
                                                                        0x03 = Middle
                                                                        0x04 = High

 Example: Current Display Fan Speed settings: Off (Display address 01)
  MsgSize Control Group          Data (0) Data (1)         Checksum
  0x06      0x01       0x00      0x62         0x00         0x65


```

##### 7.20.3 Message-Set

```text


  Bytes          Bytes Description                        Bits       Description
  DATA[0         0x61 = Fan Speed status – Set                       Command to set the Fan Speed status of the
  ]                                                                  display enabled or disabled
  DATA[1         Off / Auto / Low / Middle /                         0x00 = Off
  ]              High                                                0x01 = Auto
                                                                     0x02 = Low
                                                                     0x03 = Middle
                                                                     0x04 = High

 Example: Set the Display to the fallowing: Fan Speed off (Display address 01)
  MsgSize Control Group            Data (0) Data (1)        Checksum
  0x06      0x01       0x00        0x61        0x00         0x66





```
