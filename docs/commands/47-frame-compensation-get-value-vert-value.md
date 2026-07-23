# Frame compensation Get value Vert value

Source: `docs/Philips_SICP_Commands.md`, lines 5632-5672.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 7.31 Frame compensation Get value Vert value

## DATA[0] Codes

- `0x67` - Frame compensation                          Command requests the display to report its current
- `0x67` - Frame compensation                             Vert frame compensation value

## Source Excerpt
#### 7.31 Frame compensation Get value Vert value

```text

        Is supported from firmware version : tbc

        Get the Horizontal frame compensation value.


      Bytes        Bytes Description                       Bits       Description
      DATA[0]      0x67 = Frame compensation                          Command requests the display to report its current
                   Vert value – Get                                   Frame compensation Vert value

     Example: (Display address 01)
      MsgSize Control Group               Data (0)     Checksum
      0x05        0x01        0x00        0x67         0x63


        Message-Report

      Bytes        Bytes Description                           Bits      Description
      DATA[0]      0x67 = Frame compensation                             Vert frame compensation value
                   Vert– Report
      DATA[1]                                                            0x00 = 00
                                                                         0x01 = 01
                                                                         …
                                                                         0xFF = 255
11


         Example: Current Display settings:

        MsgSize      Control       Group         Data (0)       Data (1)      Checksum
        0x06         0x01          0x00          0x67           0x00          0x60
        0x06         0x01          0x00          0x67           0x03          0x63




```
