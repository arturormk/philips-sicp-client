# Noise Reduction

Source: `docs/Philips_SICP_Commands.md`, lines 4544-4616.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 7.14.1 Message-Get
- 7.14.2 Message-Report
- 7.14.3 Message-Set

## DATA[0] Codes

- `0x2B` - Noise Reduction                              Command requests the display to report its current
- `0x2B` - Noise reduction Feature                         Command reports the Noise Reduction Feature
- `0x2A` - Noise reduction                              Command to set the Noise Reduction Feature of the

## Source Excerpt
#### 7.14 Noise Reduction

```text
The command is used to set/get the Noise reduction Feature as it is defined as below.


```

##### 7.14.1 Message-Get

```text


 Bytes          Bytes Description                        Bits       Description
 DATA[0]        0x2B = Noise Reduction                              Command requests the display to report its current
                Feature – Get                                       Noise Reduction status

Example: (Display address 01)
 MsgSize Control Group                 Data (0)      Checksum
 0x05        0x01        0x00          0x2B          0x2F


```

##### 7.14.2 Message-Report

```text


 Bytes          Bytes Description                            Bits      Description
 DATA[0]        0x2B = Noise reduction Feature                         Command reports the Noise Reduction Feature
                – Report                                               enabled or disabled
 DATA[1]        Off / Low / Middle / High                              0x00 = Off
                                                                       0x01 = Low
                                                                       0x02 = Middle
                                                                       0x03 = High
                                                                       0x04 = default*

(*) only valid for challenger2.1 platform
Example: Current Display Noise Reduction Feature settings: Off (Display address 01)
 MsgSize Control Group              Data (0)      Data (1)      Checksum
 0x06       0x01         0x00       0x2B          0x00          0x2C


```

##### 7.14.3 Message-Set

```text


 Bytes          Bytes Description                        Bits       Description
 DATA[0]        0x2A = Noise reduction                              Command to set the Noise Reduction Feature of the
                Feature – Set                                       display enabled or disabled
 DATA[1]        Off / Low / Middle / High                           0x00 = Off
                                                                    0x01 = Low
                                                                    0x02 = Middle
                                                                    0x03 = High
                                                                    0x04 = default*

(*) only valid for challenger2.1 platform


Example: Set the Display to the fallowing: Noise Reduction Feature off (Display address 01)
 MsgSize Control Group                 Data (0)     Data (1)    Checksum
 0x06        0x01        0x00          0x2A         0x00        0x2D





```
