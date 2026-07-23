# Operating Hours

Source: `docs/Philips_SICP_Commands.md`, lines 3532-3573.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 7.1.1 Message-Get
- 7.1.2 Message-Report

## DATA[0] Codes

- `0x0F` - Misc. Info –                  Command requests the display to report from miscellaneous
- `0x0F` - Misc. Info –                       Command reports current Operating Hours

## Source Excerpt
#### 7.1 Operating Hours

```text

The command is used to record the working hours of the display.

```

##### 7.1.1 Message-Get

```text

 Bytes        Bytes Description          Bits      Description
 DATA[0]      0x0F = Misc. Info –                  Command requests the display to report from miscellaneous
              Get                                  information parameters
 DATA[1]      Item                                 0x02 = Operating Hours
                                                   (All other values are reserved)

Example: (Display address 01)
 MsgSize Control Group             Data (0)      Data (1)     Checksum
 0x06        0x01        0x00      0x0F          0x02         0x0A

```

##### 7.1.2 Message-Report

```text

 Bytes        Bytes Description                 Bits    Description
 DATA[0]      0x0F = Misc. Info –                       Command reports current Operating Hours
              Report
 DATA[1]      Operating Hours
 to                                                     DATA [1] and DATA [2] form the MS Byte and LSByte,
 DATA[2]                                                respectively, of the 16-bit-wide Operational Hours value.


Example: Current Display Operation Hours counter value (Display address 01)
 MsgSize Control Group              Data (0)     Data (1)     Data (2)    Checksum
 0x07       0x01         0x00       0x0F         0x4D         0x00        0x44

```
