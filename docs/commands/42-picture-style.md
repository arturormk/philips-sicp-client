# Picture Style

Source: `docs/Philips_SICP_Commands.md`, lines 5413-5490.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 7.26.1 Message-report get Picture Style
- 7.26.2 Message-set Picture Style

## DATA[0] Codes

- `0x65` - Picture Style – Get                           Command requests the display to report its current
- `0x65` - Picture Style                                  Command reports the Picture Style
- `0x66` - Set Picture Style                        Command set the Picture Style

## Source Excerpt
#### 7.26 Picture Style

```text

            The command is used to set/get the picture style :

            Highbright, sRGB, Vivid, Natural, Standard, Video, Static Signage, Text, Energy saving

            The command is only available on Phoenix 1 & 2 platform from firmware version: x.xx (tbc) onwards.


 Bytes       Bytes Description                      Bits       Description


  DATA[0]      0x65 = Picture Style – Get                           Command requests the display to report its current
                                                                    Picture Style value

 Example: (Display address 01)
  MsgSize Control Group        Data (0)  Checksum
  0x05        0x01        0x00 0x65      0x61
```

##### 7.26.1 Message-report get Picture Style

```text

    Bytes        Bytes Description                           Bits      Description
  DATA[0]        0x65 = Picture Style                                  Command reports the Picture Style
                 status – Report
  DATA[1]        Picture style*                                        0x00 = Highbright
                                                                       0x01 = sRGB
                                                                       0x02 = Vivid
                                                                       0x03 = Natural
                                                                       0x04 = Standard
                                                                       0x05 = Video
                                                                       0x06 = Static Signage
                                                                       0x07 = Text
                                                                       0x08 = Energy saving
                                                                       0x09 = Soft
                                                                       0x0A = User

                *: could be that not all the picture styles are available, check the OSD menu of your monitor
     Example: Current picture style setting: (Display address 01)

  MsgSize  Control Group        Data (0)               Data (1)       Checksum
  0x06     0x01      0x00       0x65                   0x00           0x62              Highbright
  0x06     0x01      0x00       0x65                   0x03           0x61              Natural
```

##### 7.26.2 Message-set Picture Style

```text

   The command is only available on Phoenix 1 & 2 platform from firmware version: x.xx (tbc) onwards.
    Bytes   Bytes Description                       Bits    Description
  DATA[0]   0x66 = Set Picture Style                        Command set the Picture Style

  DATA[1]        Picture style*                                        0x00 = Highbright
                                                                       0x01 = sRGB
                                                                       0x02 = Vivid
                                                                       0x03 = Natural
                                                                       0x04 = Standard
                                                                       0x05 = Video
                                                                       0x06 = Static Signage
                                                                       0x07 = Text
                                                                       0x08 = Energy saving
                                                                       0x09 = Soft
                                                                       0x0A = User


                *: could be that not all the picture styles are available, check the OSD menu of your monitor

Example : set picture style to highbright
  MsgSize Control Group                Data (0)      DATA[1]          Checksum
  0x06        0x01        0x00         0x66          0x00             0x61

```
