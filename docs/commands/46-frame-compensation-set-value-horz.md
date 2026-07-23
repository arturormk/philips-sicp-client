# Frame compensation Set value Horz

Source: `docs/Philips_SICP_Commands.md`, lines 5606-5631.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 7.30 Frame compensation Set value Horz

## DATA[0] Codes

- `0x5F` - Frame compensation –                           Set Horz frame compensation value

## Source Excerpt
#### 7.30 Frame compensation Set value Horz

```text

        Is supported from firmware version : tbc

        Set the Horizontal frame compensation value.


      Bytes        Bytes Description                           Bits      Description
      DATA[0]      0x5F = Frame compensation –                           Set Horz frame compensation value
                   Horz Set
      DATA[1]                                                            0x00 = 00
                                                                         0x01 = 01
                                                                         …
                                                                         0xFF = 255
10


         Example: Current Display settings:
      MsgSize Control Group               Data (0)     Data (1)       Checksum
      0x06     0x01         0x00          0x5F         0x00           0x58
      0x06     0x01         0x00          0x5F         0x03           0x5B

```
