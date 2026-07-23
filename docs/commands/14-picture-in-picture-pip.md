# Picture-in-Picture (PIP)

Source: `docs/Philips_SICP_Commands.md`, lines 2661-3112.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 5.4.1 Message-Get
- 5.4.2 Message-Report
- 5.4.3 Message-Set
- 5.4.4.1 Message-Get PIP source
- 5.4.4.2 Message-Report PIP source
- 5.4.4.3 Message-Set

## DATA[0] Codes

- `0x3D` - Picture-in-Picture –                         Command requests the display to get the
- `0x3D` - Picture-in-Picture –                       Command reports to the host controller the
- `0x3C` - Picture-in-Picture –                        Command requests the display to set the
- `0x85` - PIP Source – Get
- `0x84` - PIP Source – Set

## Source Excerpt
#### 5.4 Picture-in-Picture (PIP)

```text

This command is used to control PIP on/off with different Quadrants of the screen.

```

##### 5.4.1 Message-Get

```text

      Bytes        Bytes Description                       Bits        Description
      DATA[0]      0x3D = Picture-in-Picture –                         Command requests the display to get the
                    Get                                                specified PIP settings.

   Example: Get PIP setting (Display address 01)
    MsgSize Control Group               Data (0)       Checksum
    0x05      0x01        0x00          0x3D           0x39

```

##### 5.4.2 Message-Report

```text

      Bytes           Bytes Description                     Bits        Description
      DATA[0]         0x3D = Picture-in-Picture –                       Command reports to the host controller the
                       Report                                           current PIP settings.
      DATA[1]         Picture-in-Picture                    Bit 7..4    ( reserved, default 0 )
                                                            Bit 0..3    0x00 = Off
                                                                        0x01 = On (PIP)
                                                                        0x02 = POP
                                                                        0x03 = Quick swap
                                                                        0x04 = PBP 2win
                                                                        0x05 = PBP 3win
                                                                        0x06 = PBP 4win
                                                                        0x07 = PBP 3win-1
                                                                        0x08 = PBP 3win-2
                                                                        0x09 = PBP 4win-1
                                                                        0x0A = SICP (Custom)

                                                                        Note: platform list
                                                                        1.Eagle 1.3 platform only support (0x00 / 0x01)
                                                                        2.HIMALAYA 1.0 & 1.2 platform only support
                                                                        (0x00 ~0x06)
                                                                        3.DRAGON 1.0, 1.5, 1.6 platform only support
                                                                        (0x00 / 0x01/ 0x03 /0x04 / 0x0A)
                                                                        4.Phoenix platform doesn’t support PIP.
```

### 5 HIMALAYA 2.0 doesn’t support 0X02

```text
      DATA[2]         Additional PIP parameters             Bit 7..3    ( reserved, default 0 )
                                                            Bit 2..0    Position of the PIP window:
                                                                        0x00 = position 0 (typically bottom-left)
                                                                        0x01 = position 1 (typically top-left)
                                                                        0x02 = position 2 (typically top-right)
                                                                        0x03 = position 3 (typically bottom-right)
                                                                        0x04 = position 4 (typically center).
      DATA[3]                                                           ( reserved, default 0 )
      DATA[4]                                                           ( reserved, default 0 )

   Example: Current PIP setting is enabling and located at position 2 (Display address 01)
    MsgSize Control Group                Data (0)     Data (1)      Data (2)     Data (3)     Data (4)   Checksum
    0x09      0x01        0x00           0x3D         0x01          0x02         0x00         0x00       0x36





```

##### 5.4.3 Message-Set

```text

 Bytes        Bytes Description                      Bits        Description
 DATA[0]      0x3C = Picture-in-Picture –                        Command requests the display to set the
              Set                                                specified PIP settings.
 DATA[1]      Picture-in-Picture                     Bit 7..4    ( reserved, default 0 )
                                                     Bit 0..3    0x00 = Off
                                                                 0x01 = On (PIP)
                                                                 0x02 = POP
                                                                 0x03 = Quick swap
                                                                 0x04 = PBP 2win
                                                                 0x05 = PBP 3win
                                                                 0x06 = PBP 4win
                                                                 0x07 = PBP 3win-1
                                                                 0x08 = PBP 3win-2
                                                                 0x09 = PBP 4win-1
                                                                 0x0A = SICP (Custom)

                                                                 Note: platform list
                                                                 1.Eagle 1.3 platform only support (0x00 / 0x01)
                                                                 2.HIMALAYA 1.0 & 1.2 platform only support
                                                                 (0x00 ~0x06)
                                                                 3.DRAGON 1.0, 1.5, 1.6 platform only support
                                                                 (0x00 / 0x01/ 0x03 /0x04 / 0x0A)
                                                                 4.Phoenix platform doesn’t support PIP.
```

### 5 HIMALAYA 2.0 doesn’t support 0X02

```text
 DATA[2]      Additional PIP parameters              Bit 7..2    ( reserved, default 0 )
                                                     Bit 1..0    Position of the PIP window:
                                                                 0x00 = position 0 (typically bottom-left)
                                                                 0x01 = position 1 (typically top-left)
                                                                 0x02 = position 2 (typically top-right)
                                                                 0x03 = position 3 (typically bottom-right)
                                                                 0x04 = position 4 (typically center).
 DATA[3]                                                         ( reserved, default 0 )
 DATA[4]                                                         ( reserved, default 0 )

Example: Set PIP ON, top-right (Display address 01)
 MsgSize       Control Group             Data (0) Data (1)      Data (2)    Data (3)   Data (4)   Checksum
 0x09          0x01         0x00         0x3C       0x01        0x02        0x00       0x00       0x37





```

##### 5.4.4 Picture-In-Picture (PIP) Source

```text

This command is used to control the PIP source settings for each display quadrant on the screen.

Himalaya 1.x & 2.0 platform carries the following PIP Design only
 Example: If display resolution is 4K2K, user can select input source for each Full HD quadrant.


         Q1 (main)                       Q2


           Q3                            Q4




PIP Set/Get can only change input source for Q2, Q3, and Q4 individually by following the commands
below.

Dragon 1.x platform and older platforms (Eagle) carries the following PIP Design only.



     Main Source


                                      PIP source




```

###### 5.4.4.1 Message-Get PIP source

```text


 Bytes          Bytes Description                  Bits    Description
                                                           Command requests the display to report its current
 DATA[0]        0x85 = PIP Source – Get
                                                           PIP source setting.

This command is used to get the source for the PIP window when PIP feature is activated.

Example: Get PIP source setting (Display address 01)
 MsgSize Control Group                Data (0)    Checksum
 0x05      0x01       0x00            0x85        0x81

```

###### 5.4.4.2 Message-Report PIP source

```text

Dragon 1.x & 1.6 platform DATA[3] & DATA[4] are not
available.

 Return bytes are DATA[0]~DATA[2]+Checksum byte.

 Bytes          Bytes Description                  Bits    Description
                                                           Command requests the display to report its current
 DATA[0]        0x85 = PIP Source – Get
                                                           PIP source setting.
                                                           0xFD = Input Source (normal state)
 DATA[1]        Source Type
                                                           0xFE = Reserved for smartcard
                                                           If Source types == 0xFD then…

 DATA[2]        Q2 Source Number                           0x01 = VIDEO
                                                           0x02 = S-VIDEO
                                                           0x03 = COMPONENT
                                                           0x04 = CVI 2 (not applicable)



                                                 0x05 = VGA
                                                 0x06 = HDMI 2
                                                 0x07 = Display Port 2
                                                 0x08 = USB 2
                                                 0x09 = Card DVI-D
                                                 0x0A = Display Port
                                                 0x0B= Card OPS
                                                 0x0C = USB
                                                 0x0D= HDMI
                                                 0x0E= DVI-D
                                                 0x0F = HDMI3
                                                 0x10= BROWSER
                                                 0x11= SMARTCMS
                                                 0X12= DMS (Digital Media Server)
                                                 0x13= INTERNAL STORAGE
                                                 0x14= Reserved
                                                 0x15= Reserved
                                                 0x16= Media Player
                                                 0x17= PDF Player
                                                 0x18= Custom
                                                 0x19 = reserved
                                                 0x1A = VGA2
                                                 0x1B = VGA3
                                                 0x1C = IWB
                                                 If Source type == 0xFD then…

                                                 0x01 = VIDEO
                                                 0x02 = S-VIDEO
                                                 0x03 = COMPONENT
                                                 0x04 = CVI 2 (not applicable)
                                                 0x05 = VGA
                                                 0x06 = HDMI 2
                                                 0x07 = Display Port 2
                                                 0x08 = USB 2
                                                 0x09 = Card DVI-D
                                                 0x0A = Display Port
                                                 0x0B= Card OPS
DATA[3]   Q3 Source Number
                                                 0x0C = USB
                                                 0x0D= HDMI
                                                 0x0E= DVI-D
                                                 0x0F = HDMI3
                                                 0x10= BROWSER
                                                 0x11= SMARTCMS
                                                 0X12= DMS (Digital Media Server)
                                                 0x13= INTERNAL STORAGE
                                                 0x14= Reserved
                                                 0x15= Reserved
                                                 0x16= Media Player
                                                 0x17= PDF Player
                                                 0x18= Custom
                                                 0x19 = reserved
                                                 0x1A = VGA2
                                                 0x1B = VGA3
                                                 0x1C = IWB





                                                 If Source type == 0xFD then…

                                                 0x01 = VIDEO
                                                 0x02 = S-VIDEO
                                                 0x03 = COMPONENT
                                                 0x04 = CVI 2 (not applicable)
DATA[4]   Q4 Source Number
                                                 0x05 = VGA
                                                 0x06 = HDMI 2
                                                 0x07 = Display Port 2
                                                 0x08 = USB 2
                                                 0x09 = Card DVI-D
                                                 0x0A = Display Port





                                                           0x0B= Card OPS
                                                           0x0C = USB
                                                           0x0D= HDMI
                                                           0x0E= DVI-D
                                                           0x0F = HDMI3
                                                           0x10= BROWSER
                                                           0x11= SMARTCMS
                                                           0X12= DMS (Digital Media Server)
                                                           0x13= INTERNAL STORAGE
                                                           0x14= Reserved
                                                           0x15= Reserved
                                                           0x16= Media Player
                                                           0x17= PDF Player
                                                           0x18= Custom
                                                           0x19 = reserved
                                                           0x1A = VGA2
                                                           0x1B = VGA3
                                                           0x1C = IWB


Example: Get PIP source report (Display address 01, Q2 Video, Q3 VGA, Q4 DVI-D)

 MsgSize   Control Group            Data (0)      Data (1)     Data (2)      Data(3)    Data(4)       Checksum
 0x09      0x01    0x00             0x85          0xFD         0x01          0x05       0x0E          0x7A

```

###### 5.4.4.3 Message-Set

```text

This is the PIP source selection command

Dragon 1.x & 2.0 platform – DATA[3] & DATA[4] may not
be send.
Return bytes are DATA[0]~DATA[2]+Checksum byte.

 Bytes         Bytes Description                 Bits      Description
                                                           Command requests the display to set the specified PIP
 DATA[0]       0x84 = PIP Source – Set
                                                           source.
                                                           0xFD = Input Source (normal state)
 DATA[1]       Source Type
                                                           0xFE = Reserved for smartcard





                                                 If Source type == 0xFD then…

                                                 0x01 = VIDEO
                                                 0x02 = S-VIDEO
                                                 0x03 = COMPONENT
                                                 0x04 = CVI 2 (not applicable)
                                                 0x05 = VGA
                                                 0x06 = HDMI 2
                                                 0x07 = Display Port 2
                                                 0x08 = USB 2
                                                 0x09 = Card DVI-D
                                                 0x0A = Display Port
DATA[2]   Q2 Source Number
                                                 0x0B= Card OPS
                                                 0x0C = USB
                                                 0x0D= HDMI
                                                 0x0E= DVI-D
                                                 0x0F = HDMI3
                                                 0x10= BROWSER
                                                 0x11= SMARTCMS
                                                 0X12= DMS (Digital Media Server)
                                                 0x13= INTERNAL STORAGE
                                                 0x14= Reserved
                                                 0x15= Reserved
                                                 0x16= Media Player





                                                  0x17= PDF Player
                                                  0x18= Custom
                                                  0x19 = reserved
                                                  0x1A = VGA2
                                                  0x1B = VGA3
                                                  0x1C = IWB
                                                  If Source type == 0xFD then…

                                                  0x01 = VIDEO
                                                  0x02 = S-VIDEO
                                                  0x03 = COMPONENT
                                                  0x04 = CVI 2 (not applicable)
                                                  0x05 = VGA
                                                  0x06 = HDMI 2
                                                  0x07 = Display Port 2
                                                  0x08 = USB 2
                                                  0x09 = Card DVI-D
                                                  0x0A = Display Port
                                                  0x0B= Card OPS
DATA[3]   Q3 Source Number
                                                  0x0C = USB
                                                  0x0D= HDMI
                                                  0x0E= DVI-D
                                                  0x0F = HDMI3
                                                  0x10= BROWSER
                                                  0x11= SMARTCMS
                                                  0X12= DMS (Digital Media Server)
                                                  0x13= INTERNAL STORAGE
                                                  0x14= Reserved
                                                  0x15= Reserved
                                                  0x16= Media Player
                                                  0x17= PDF Player
                                                  0x18= Custom
                                                  0x19 = reserved
                                                  0x1A = VGA2
                                                  0x1B = VGA3
                                                  0x1C = IWB
                                                  If Source type == 0xFD then…

                                                  0x01 = VIDEO
                                                  0x02 = S-VIDEO
                                                  0x03 = COMPONENT
                                                  0x04 = CVI 2 (not applicable)
                                                  0x05 = VGA
                                                  0x06 = HDMI 2
                                                  0x07 = Display Port 2
                                                  0x08 = USB 2
                                                  0x09 = Card DVI-D
                                                  0x0A = Display Port
                                                  0x0B= Card OPS
DATA[4]   Q4 Source Number
                                                  0x0C = USB
                                                  0x0D= HDMI
                                                  0x0E= DVI-D
                                                  0x0F = HDMI3
                                                  0x10= BROWSER
                                                  0x11= SMARTCMS
                                                  0X12= DMS (Digital Media Server)
                                                  0x13= INTERNAL STORAGE
                                                  0x14= Reserved
                                                  0x15= Reserved
                                                  0x16= Media Player
                                                  0x17= PDF Player
                                                  0x18= Custom
                                                  0x19 = reserved

                                                          0x1A = VGA2
                                                          0x1B = VGA3
                                                          0x1C = IWB




 This command is used to select the source for the PIP window before the PIP feature is activated.

 Example: Set source PIP (Display address 01, Q2 Video, Q3 VGA, Q4 DVI-D)

     MsgSize    Control    Group        Data (0)    Data (1)      Data (2)       Data(3)   Data(4)   Checksum
     0x09       0x01       0x00         0x84        0xFD          0x01           0x05      0x0E      0x7B
Example :
        set PIP source to DP:      07 01 00 84 FD 0A 75
        set PIP source to VGA:     07 01 00 84 FD 05 7A





```

### 6 MESSAGES – AUDIO
