# Scan Conversion

Source: `docs/Philips_SICP_Commands.md`, lines 4688-4753.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 7.16.1 Message-Get
- 7.16.2 Message-Report
- 7.16.3 Message-Set

## DATA[0] Codes

- `0x53` - Scan Conversion                             Command requests the display to report its current
- `0x53` - Scan Conversion Feature                        Command reports the Scan Conversion Feature
- `0x52` - Scan Conversion                             Command to set the Scan Conversion Feature of the

## Source Excerpt
#### 7.16 Scan Conversion

```text
The command is used to set/get the Scan Conversion Feature as it is defined as below.

NOTE: Himalaya 1.0 &1.2 & Dragon 1.x & 1.6 platform does NOT support Scan Conversion.



```

##### 7.16.1 Message-Get

```text


 Bytes          Bytes Description                       Bits       Description
 DATA[0]        0x53 = Scan Conversion                             Command requests the display to report its current
                Feature – Get                                      Scan Conversion Feature status

Example: (Display address 01)
 MsgSize Control Group                 Data (0)     Checksum
 0x05        0x01        0x00          0x53         0x57


```

##### 7.16.2 Message-Report

```text


 Bytes          Bytes Description                           Bits      Description
 DATA[0]        0x53 = Scan Conversion Feature                        Command reports the Scan Conversion Feature
                – Report                                              enabled or disabled
 DATA[1]        Progressive / Interlace                               0x00 = Progressive
                                                                      0x01 = Interlace

Example: Current Display Scan Conversion Feature settings: Progressive (Display address 01)
 MsgSize Control Group              Data (0)     Data (1)      Checksum
 0x06       0x01         0x00       0x53         0x00          0x54


```

##### 7.16.3 Message-Set

```text


 Bytes          Bytes Description                       Bits       Description
 DATA[0]        0x52 = Scan Conversion                             Command to set the Scan Conversion Feature of the
                Feature – Set                                      display enabled or disabled
 DATA[1]        Progressive / Interlace                            0x00 = Progressive
                                                                   0x01 = Interlace

Example: Set the Display to the fallowing: Scan Conversion Feature Progressive (Display address 01)
 MsgSize Control Group                 Data (0)    Data (1)     Checksum
 0x06        0x01        0x00          0x52        0x00         0x55





```
