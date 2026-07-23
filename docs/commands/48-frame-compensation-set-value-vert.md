# Frame compensation Set value Vert

Source: `docs/Philips_SICP_Commands.md`, lines 5673-5703.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 7.32 Frame compensation Set value Vert

## DATA[0] Codes

- `0x68` - Frame compensation Vert                            Set Vert frame compensation value

## Source Excerpt
#### 7.32 Frame compensation Set value Vert

```text
           Set the Vertical frame compensation value.


        Bytes           Bytes Description              Bits                       Description
        DATA[0]         0x68 = Frame compensation Vert                            Set Vert frame compensation value
                        – Set
        DATA[1]                                                                   0x00 = 00
                                                                                  0x01 = 01
                                                                                  …
                                                                                  0xFF = 255
  12


           Example: Current Display settings:
        MsgSize Control Group               Data (0)            Data (1)      Checksum
        0x06     0x01         0x00          0x68                0x00          0x6F
        0x06     0x01         0x00          0x68                0x03          0x6C



```

### 8 Scheduling

```text

```
