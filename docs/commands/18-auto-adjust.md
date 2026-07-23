# Auto Adjust

Source: `docs/Philips_SICP_Commands.md`, lines 3642-3671.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 7.3.1 Message-Set

## DATA[0] Codes

- `0x70` - Video Alignment –                       Command requests the display to        make       auto

## Source Excerpt
#### 7.3 Auto Adjust

```text

This command works for VGA (host controller) video auto adjust.


```

##### 7.3.1 Message-Set

```text

 Bytes         Bytes Description                     Bits     Description
 DATA[0]       0x70 = Video Alignment –                       Command requests the display to        make       auto
               Set                                            adjustment on VGA Input source.
 DATA[1]       Item                                           0x40 = Auto Adjust
                                                              (* All other values are reserved *)
 DATA[2]                                                      ( reserved, default 0 )

Example: (Display address 01)
 MsgSize Control Group                Data (0)     Data (1)     Data (2)     Checksum
 0x07        0x01        0x00         0x70         0x40         0x00         0x36





```
