# Frame compensation Get value Horz value

Source: `docs/Philips_SICP_Commands.md`, lines 5566-5605.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 7.29 Frame compensation Get value Horz value

## DATA[0] Codes

- `0x5E` - Frame compensation                        Command requests the display to report its current
- `0x5E` - Frame compensation –                           Horz frame compensation value

## Source Excerpt
#### 7.29 Frame compensation Get value Horz value

```text
   Is supported from firmware version : tbc

   Get the Horizontal frame compensation value.


 Bytes        Bytes Description                     Bits       Description
 DATA[0]      0x5E = Frame compensation                        Command requests the display to report its current
              Horz value – Get                                 Frame compensation Horz value

Example: (Display address 01)
 MsgSize Control Group             Data (0)     Checksum
 0x05        0x01        0x00      0x5E         0x5A


   Message-Report

 Bytes        Bytes Description                         Bits      Description

      DATA[0]      0x5E = Frame compensation –                           Horz frame compensation value
                   Horz Report
      DATA[1]                                                            0x00 = 00
                                                                         0x01 = 01
                                                                         …
                                                                         0xFF = 255
9


         Example: Current Display settings:
      MsgSize Control Group               Data (0)     Data (1)       Checksum
      0x06     0x01         0x00          0x5E         0x00           0x59
      0x06     0x01         0x00          0x5E         0x03           0x5A




```
