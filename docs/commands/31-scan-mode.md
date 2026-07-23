# Scan Mode

Source: `docs/Philips_SICP_Commands.md`, lines 4617-4687.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 7.15.1 Message-Get
- 7.15.2 Message-Report
- 7.15.3 Message-Set

## DATA[0] Codes

- `0x51` - Scan Mode Feature –                           Command requests the display to report its current
- `0x51` - Scan Mode Feature –                              Command reports the Scan Mode Feature
- `0x50` - Scan Mode Feature –                           Command to set the Scan mode Feature of the

## Source Excerpt
#### 7.15 Scan Mode

```text
The command is used to set/get the Scan Mode Feature as it is defined as below.


```

##### 7.15.1 Message-Get

```text


 Bytes         Bytes Description                       Bits         Description
 DATA[0]       0x51 = Scan Mode Feature –                           Command requests the display to report its current
               Get                                                  Scan Mode Feature status

Example: (Display address 01)
 MsgSize Control Group               Data (0)      Checksum
 0x05        0x01        0x00        0x51          0x55


```

##### 7.15.2 Message-Report

```text


 Bytes         Bytes Description                             Bits      Description
 DATA[0]       0x51 = Scan Mode Feature –                              Command reports the Scan Mode Feature
               Report                                                  enabled or disabled
 DATA[1]       Over scan / Under scan                                  0x00 = Over scan (ON)
                                                                       0x01 = Under scan
                                                                       0x02 = Off
                                                                       0x03 > 0x1C (from 0 > 25)*

    (*) From 0 > 25 only valid for challenger 2.1 platform
Example: Current Display Scan Mode Feature settings: Over scan (Display address 01)
 MsgSize Control Group              Data (0)     Data (1)     Checksum
 0x06       0x01         0x00       0x51         0x00         0x56


```

##### 7.15.3 Message-Set

```text


 Bytes         Bytes Description                       Bits         Description
 DATA[0]       0x50 = Scan Mode Feature –                           Command to set the Scan mode Feature of the
               Set                                                  display enabled or disabled
 DATA[1]       Over scan / Under scan                               0x00 = Over scan
                                                                    0x01 = Under scan
                                                                    0x02 = Off
                                                                    0x03 > 0x1C (from 0 > 25)*

    (*) From 0 > 25 only valid for challenger 2.1 platform


Example: Set the Display to the fallowing: Scan Mode Feature over scan (Display address 01)
 MsgSize Control Group                 Data (0)    Data (1)    Checksum
 0x06        0x01        0x00          0x50        0x00        0x57





```
