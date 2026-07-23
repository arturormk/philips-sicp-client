# AnyTile (Canvas)

Source: `docs/Philips_SICP_Commands.md`, lines 3937-4048.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 7.7.3 AnyTile –Report
- 7.7.4 AnyTile Set
- 7.7.4 AnyTile Set/Get Resolution Mode

## DATA[0] Codes

- `0xC0` - Set Group ID & Monitor ID                       Change Group ID and monitor ID of the monitor
- `0x4C` - Display monitor ID – Set                        Enable or Disable displaying monitor ID on the monitor
- `0x4A` - Custom Tiling – Report                          Command reports Custom Tiling Setting
- `0x4B` - Custom Tiling – Report                           Command reports Custom Tiling Setting
- `0x4E` - Display monitor ID – Get                         Set/get the resolution input mode

## Source Excerpt
#### 7.7 AnyTile (Canvas)

```text

Tiling can be set beyond the OSD menu options and therefore can be flexible to a certain extent allowable by
command thresholds.
 SPECIAL NOTE: only 2016 Dragon 1.x, Dragon 1.6 & Himalaya2.0 platform supports these commands
 Those commands only work if the the canvas tiling is activated from the admin menu.



```

##### 7.7.1 AnyTile Assign Group ID and monitor ID

```text

Change the monitor ID & Group ID of the monitor, this command is only working via IP connection and not via
RS232.

  Bytes              Bytes Description                             Bits     Description
  DATA[0]            0xC0 = Set Group ID & Monitor ID                       Change Group ID and monitor ID of the monitor
                     (this command only works via IP)
  DATA[1]            Monitor ID                                             Monitor ID

  DATA[2]            Group ID                                               Group ID


```

##### 7.7.2 Display monitor ID

```text

  Bytes              Bytes Description                             Bits     Description
  DATA[0]            0x4C = Display monitor ID – Set                        Enable or Disable displaying monitor ID on the monitor

  DATA[1]            Monitor ID




```

##### 7.7.3 AnyTile –Report

```text


  Bytes              Bytes Description                             Bits     Description
  DATA[0]            0x4A = Custom Tiling – Report                          Command reports Custom Tiling Setting
  DATA[1]            Enable                                                 0x00 = No
                                                                            0x01 = Yes
  DATA[2]            Rotation (lsb)                                         0 degree > lsb= 0x00 & msb= 0x00
                                                                            90 degree > lsb= 0x5A & msb= 0x00
  DATA[3]            Rotation (msb)                                         270 degree > lsb= 0x0E & msb= 0x10

  DATA[4]            Input H Start(lsb)                                     H Start of captured input picture(lsb).
  DATA[5]            Input H Start(msb)                                     H Start of captured input picture(msb).
  DATA[6]            Input V Start(lsb)                                     V Start of captured input picture(lsb).
  DATA[7]            Input V Start(msb)                                     V Start of captured input picture(msb).
  DATA[8]            Input H Size(lsb)                                      H Size of captured input picture(lsb).
  DATA[9]            Input H Size(msb)                                      H Size of captured input picture(msb).
  DATA[10]           Input V Size(lsb)                                      V Size of captured input picture(lsb).
  DATA[11]           Input V Size(msb                                       V Size of captured input picture(msb).


Data[4] to Data[11] is the pixel value in hex, max value depends of the panel.
If FHD : max = 1920/1080

```

##### 7.7.4 AnyTile Set

```text


 Bytes             Bytes Description                              Bits     Description
 DATA[0]           0x4B = Custom Tiling – Report                           Command reports Custom Tiling Setting
 DATA[1]           Enable                                                  0x00 = No
                                                                           0x01 = Yes
 DATA[2]           Rotation (lsb)                                          0 degree
                                                                           90 degree
 DATA[3]           Rotation (msb)                                          270 degree

 DATA[4]           Input H Start(lsb)                                      H Start of captured input picture(lsb).
 DATA[5]           Input H Start(msb)                                      H Start of captured input picture(msb).
 DATA[6]           Input V Start(lsb)                                      V Start of captured input picture(lsb).
 DATA[7]           Input V Start(msb)                                      V Start of captured input picture(msb).
 DATA[8]           Input H Size(lsb)                                       H Size of captured input picture(lsb).
 DATA[9]           Input H Size(msb)                                       H Size of captured input picture(msb).
 DATA[10]          Input V Size(lsb)                                       V Size of captured input picture(lsb).
 DATA[11]          Input V Size(msb                                        V Size of captured input picture(msb).

```

##### 7.7.4 AnyTile Set/Get Resolution Mode

```text

 Bytes             Bytes Description                              Bits     Description
 DATA[0]           0x4E = Display monitor ID – Get                         Set/get the resolution input mode
                   0x4F = Display monitor ID – Set
 DATA[1]           Mode                                                    0x00 : default
                                                                           0x01 : FHD
                                                                           0x02 : UHD4K




```
