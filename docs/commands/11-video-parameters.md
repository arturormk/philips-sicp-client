# Video Parameters

Source: `docs/Philips_SICP_Commands.md`, lines 2114-2508.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 5.1.1 Message-Get Video parameters
- 5.1.2 Message-Report Video parameters
- 5.1.3 Message-Set Video parameters
- 5.1.4 Message-Get Color Temperature
- 5.1.5 Message-Report Color Temperature
- 5.1.6 Message-Set Color Temperature
- 5.1.7 Message-Get RGB parameters
- 5.1.8 Message-Report RGB parameters
- 5.1.9 Message-Set RGB parameters
- 5.1.9.1 Message-Get Color Temperature 100K steps
- 5.1.9.2 Message-Report Color Temperature 100K steps
- 5.1.9.3 Message-Set Color Temperature 100K steps

## DATA[0] Codes

- `0x33` - Video Parameters –                         Command requests the display to report its current
- `0x33` - Video Parameters –                      Command reports to the host controller the current
- `0x32` - Video Parameters –                      Command to change the current video parameters
- `0x35` - Color Temperature –                         Command requests the display to report its current
- `0x35` - Color Temperature                       Command reports to the host controller the current
- `0x34` - Color Temperature                        Command to change the current color parameters
- `0x37` - Color Parameters –                          Command requests the display to report its current
- `0x37` - Color Parameters –                      Command reports to the host controller the current
- `0x36` - Color Parameters –                       Command to change the current color parameters
- `0x12` - Color Temperature                          Command requests the display to report its current
- `0x12` - Color Temperature                      Command reports to the host controller the current
- `0x11` - Color Temperature                      Command to change the current color temperature

## Source Excerpt
#### 5.1 Video Parameters

```text

          The following commands are used to get/set video parameters as it is defined below.
          Those commands (0x32 / 0x33) are not working on platform QL3 on source inputs: browser, PDF
          player, media player, CMND&play, installed apk.


```

##### 5.1.1 Message-Get Video parameters

```text

          Bytes         Bytes Description                       Bits      Description
          DATA[0]       0x33 = Video Parameters –                         Command requests the display to report its current
                        Get                                               video parameters.

         Example: (Display address 01)
          MsgSize Control Group            Data (0)      Checksum
          0x05        0x01        0x00     0x33          0x37


```

##### 5.1.2 Message-Report Video parameters

```text

          Bytes       Bytes Description                     Bits     Description
          DATA[0]     0x33 = Video Parameters –                      Command reports to the host controller the current
                      Report                                         video parameters of the display.
          DATA[1]     Brightness.                                    0 to 100 (%) of the user selectable range of the display.
          DATA[2]     Color.                                         0 to 100 (%) of the user selectable range of the display.
          DATA[3]     Contrast.                                      0 to 100 (%) of the user selectable range of the display.
          DATA[4]     Sharpness.                                     0 to 100 (%) of the user selectable range of the display.
          DATA[5]     Tint (Hue)                                     0 to 100 (%) of the user selectable range of the display.
          DATA[6]     Black Level                                    0 to 100 (%) of the user selectable range of the display.
          DATA[7]     Gamma Selection                                0x01= Native, 0x02 = S gamma, 0x03 = 2.2, 0x04 = 2.4,
                                                                     0x05 = D-image(DICOM gamma)

         SPECIAL NOTE: Following table applicable for Phoenix 2.0 platform only (year 2015
          BDLxx70EL/BDLxx90VL/BDLxx30QL/BDLxx35QL)



          Bytes       Bytes Description                     Bits     Description
          DATA[0]     0x33 = Video Parameters –                      Command reports to the host controller the current
                      Report                                         video parameters of the display.
          DATA[1]     Brightness.                                    0 to 100 (%) of the user selectable range of the display.
          DATA[2]     Color.                                         0 to 100 (%) of the user selectable range of the display.
          DATA[3]     Contrast.                                      0 to 100 (%) of the user selectable range of the display.
          DATA[4]     Sharpness.                                     0 to 10 (%) of the user selectable range of the display.
          DATA[5]     Tint (Hue)                                     -50 to +50 (%) of the user selectable range of the
                                                                     display.
          DATA[6]     Black Level                                    0 to 100 (%) of the user selectable range of the display.
          DATA[7]     Gamma Selection                                0x01= Native, 0x02 = S gamma, 0x03 = 2.2, 0x04 = 2.4,
                                                                     0x05 = D-image(DICOM gamma)



        Example: All video parameters are set to 55 % (0x37) (Display address 01)
MsgSize Control Group Data (0)                Data (1)    Data (2)     Data (3)   Data (4)        Data (5)     Data (6)   Data (7)
0x0C     0x01         0x00      0x33          0x37        0x37         0x37       0x37            0x37         0x37       0x03
Checksum
0x3D

```

##### 5.1.3 Message-Set Video parameters

```text
 This command is not working on platform QL3 on source inputs: browser, PDF player, media player,
         CMND&play,
         installed apk.


 Bytes         Bytes Description                    Bits      Description
 DATA[0]       0x32 = Video Parameters –                      Command to change the current video parameters
               Set
 DATA[1]       Brightness.                                    0 to 100 (%) of the user selectable range of the display.
 DATA[2]       Color.                                         0 to 100 (%) of the user selectable range of the display.
 DATA[3]       Contrast.                                      0 to 100 (%) of the user selectable range of the display.
 DATA[4]       Sharpness.                                     0 to 100 (%) of the user selectable range of the display.
 DATA[5]       Tint (Hue)                                     0 to 100 (%) of the user selectable range of the display.
 DATA[6]       Black Level                                    0 to 100 (%) of the user selectable range of the display.
 DATA[7]       Gamma Selection                                0x01= Native, 0x02 = S gamma, 0x03 = 2.2, 0x04 = 2.4,
                                                              0x05 = D-image(DICOM gamma)

         NOTE: Following table applicable for Phoenix 2.0 platform only (year 2015
         BDLxx70EL/BDLxx90VL/BDLxx30QL/BDLxx35QL)

 Bytes         Bytes Description                    Bits      Description
 DATA[0]       0x32 = Video Parameters –                      Command to change the current video parameters
               Set
 DATA[1]       Brightness.                                    0 to 100 (%) of the user selectable range of the display.
 DATA[2]       Color.                                         0 to 100 (%) of the user selectable range of the display.
 DATA[3]       Contrast.                                      0 to 100 (%) of the user selectable range of the display.
 DATA[4]       Sharpness.                                     0 to 10 (%) of the user selectable range of the display.
 DATA[5]       Tint (Hue)                                     -50 to +50 (%) of the user selectable range of the
                                                              display.
 DATA[6]       Black Level                                    0 to 100 (%) of the user selectable range of the display.
 DATA[7]       Gamma Selection                                0x01= Native, 0x02 = S gamma, 0x03 = 2.2, 0x04 = 2.4,
                                                              0x05 = D-image(DICOM gamma)

         NOTE: Following table applicable for Phoenix 2.0 platform only (year 2015
         BDLxx70EL/BDLxx90VL/BDLxx30QL/BDLxx35QL)

      NOTE: Tint(Hue) value (-50) ～ (-1)

       -50         -49        -48         -47         -46        -45          -44      -43        -42         -41
        0xCE      0xCF       0xD0        0xD1        0xD2       0xD3         0xD4     0xD5       0xD6        0xD7
         -40       -39        -38         -37         -36        -35          -34      -33        -32         -31
        0xD8      0xD9       0xDA        0xDB        0xDC       0xDD         0xDE     0xDF       0xE0        0xE1
         -30       -29        -28         -27         -26        -25          -24      -23        -22         -21
        0xE2      0xE3       0xE4        0xE5        0xE6       0xE7         0xE8     0xE9       0xEA        0xEB
         -20       -19        -18         -17         -16        -15          -14      -13        -12         -11
        0xEC      0xED       0xEE        0xEF        0xF0       0xF1         0xF2     0xF3       0xF4        0xF5
         -10        -9         -8          -7          -6         -5           -4       -3         -2          -1
        0xF6      0xF7       0xF8        0xF9        0xFA       0xFB         0xFC     0xFD       0xFE        0xFF


Example: Set all video parameters to 0x37 (55 %) (Display address 01)
MsgSize Control Group                Data (0)   Data (1)     Data (2)      Data (3)   Data (4)    Data (5)     Data (6)   Data (7)
0x0C       0x01         0x00         0x32       0x37         0x37          0x37       0x37        0x37         0x37       0x03

 Checksum
 0x3C

  The following commands are used to get/set the color temperature.


```

##### 5.1.4 Message-Get Color Temperature

```text

  Bytes           Bytes Description                         Bits     Description
 DATA[0]         0x35 = Color Temperature –                         Command requests the display to report its current
                 Get                                                color temperature.

Example: (Display address 01)
 MsgSize Control Group                Data (0)     Checksum
 0x05        0x01        0x00         0x35         0x31



```

##### 5.1.5 Message-Report Color Temperature

```text

 Bytes         Bytes Description                     Bits     Description
 DATA[0]       0x35 = Color Temperature                       Command reports to the host controller the current
               – Report                                       color temperature of the display.
 DATA[1]       Color temperature                              0x00 = User 1
                                                              0x01 = Native
                                                              0x02 = 11000K(Not applicable)
                                                              0x03 = 10000K
                                                              0x04 = 9300K
                                                              0x05 = 7500K
                                                              0x06 = 6500K
                                                              0x07 = 5770K (Not pplicable)
                                                              0x08 = 5500K(Not applicable)
                                                              0x09 = 5000K
                                                              0x0A = 4000K
                                                              0x0B = 3400K (Not applicable)
                                                              0x0C = 3350K (Not applicable)
                                                              0x0D = 3000K
                                                              0x0E = 2800K (Not pplicable)
                                                              0x0F = 2600K (Not applicable)
                                                              0x10 = 1850K (Notapplicable)
                                                              0x12 = User 2

Example: The current color temperature is set to Native (Display address 01)
 MsgSize Control Group               Data (0)      Data (1)     Checksum
 0x06       0x01         0x00        0x35          0x01         0x33



```

##### 5.1.6 Message-Set Color Temperature

```text

 Bytes         Bytes Description                     Bits      Description
 DATA[0]       0x34 = Color Temperature                        Command to change the current color parameters
               – Set





DATA[1]   Color temperature                             0x00 = User 1
                                                        0x01 = Native
                                                        0x02 = 11000K(Not applicable)
                                                        0x03 = 10000K
                                                        0x04 = 9300K
                                                        0x05 = 7500K
                                                        0x06 = 6500K
                                                        0x07 = 5770K (Not pplicable)
                                                        0x08 = 5500K(Not applicable)
                                                        0x09 = 5000K
                                                        0x0A = 4000K
                                                        0x0B = 3400K (Not applicable)
                                                        0x0C = 3350K (Not applicable)
                                                        0x0D = 3000K





           The following commands are used to get/set the color parameters for specific color temperature.
                                                                   0x0E = 2800K (Not applicable)
                                                                   0x0F = 2600K (Not applicable)
                                                                   0x10 = 1850K (Not applicable)
                                                                   0x12 = User 2

           Example: The current color temperature is set to Native (Display address 01)
            MsgSize Control Group               Data (0)      Data (1)     Checksum
            0x06       0x01         0x00        0x34          0x01         0x32


```

##### 5.1.7 Message-Get RGB parameters

```text
                       This command is not working on platform QL3 on source inputs: browser, PDF player, media player, CMND&play,
                       installed apk.

            Bytes           Bytes Description                        Bits      Description
            DATA[0]         0x37 = Color Parameters –                          Command requests the display to report its current
                            Get                                                color parameters.

           Example: (Display address 01)
            MsgSize Control Group                Data (0)     Checksum
            0x05        0x01        0x00         0x37         0x33



```

##### 5.1.8 Message-Report RGB parameters

```text

            Bytes         Bytes Description                     Bits     Description
            DATA[0]       0x37 = Color Parameters –                      Command reports to the host controller the current
                          Report                                         color parameters of the display.
            DATA[1]       Red color gain value                           0 to 255 of the user selectable range of the display.
            DATA[2]       Green color gain value                         0 to 255 of the user selectable range of the display.
            DATA[3]       Blue color gain value                          0 to 255 of the user selectable range of the display.
            DATA[4]       Red color offset value                         0 to 255 of the user selectable range of the display.
            DATA[5]       Green color offset value                       0 to 255 of the user selectable range of the display.
            DATA[6]       Blue color offset value                        0 to 255 of the user selectable range of the display.

           Example: All color parameters are set to 255 (0xFF) (Display address 01)
 MsgSize      Control Group           Data (0)      Data (1)     Data (2)    Data (3)      Data (4)    Data (5)    Data (6)       Check
 0x0B         0x01         0x00       0x37          0xFF         0xFF        0xFF          0xFF        0xFF        0xFF           0x3D



```

##### 5.1.9 Message-Set RGB parameters

```text
                       This command is not working on platform QL3 on source inputs: browser, PDF player, media player, CMND&play,
                       installed apk.

            Bytes         Bytes Description                     Bits      Description
            DATA[0]       0x36 = Color Parameters –                       Command to change the current color parameters
                          Set
            DATA[1]       Red color gain value                            0 to 255 of the user selectable range of the display.
            DATA[2]       Green color gain value                          0 to 255 of the user selectable range of the display.
            DATA[3]       Blue color gain value                           0 to 255 of the user selectable range of the display.
            DATA[4]       Red color offset value                          0 to 255 of the user selectable range of the display.
            DATA[5]       Green color offset value                        0 to 255 of the user selectable range of the display.
            DATA[6]       Blue color offset value                         0 to 255 of the user selectable range of the display.

           Example: All color parameters are set to 255 (0xFF) (Display address 01)
MsgSize     Control Group            Data (0)      Data (1)    Data (2)     Data (3)      Data (4)    Data (5)    Data (6)      Check
0x0B        0x01         0x00        0x36          0xFF        0xFF         0xFF          0xFF        0xFF        0xFFPage | 44 0x3C

The following commands are used to get/set the color temperature 100K/step adjustment.


```

###### 5.1.9.1 Message-Get Color Temperature 100K steps

```text

 Bytes           Bytes Description                       Bits      Description
 DATA[0]         0x12 = Color Temperature                          Command requests the display to report its current
                 100K steps – Get                                  color temperature 100K steps.

Example: (Display address 01)
 MsgSize Control Group               Data (0)     Checksum
 0x05        0x01        0x00        0x12         0x16


```

###### 5.1.9.2 Message-Report Color Temperature 100K steps

```text

 Bytes         Bytes Description                    Bits     Description
 DATA[0]       0x12 = Color Temperature                      Command reports to the host controller the current
               100K – Report                                 color temperature 100K steps of the display.
 DATA[1]       Color temperature steps                       20 to 100 of the user selectable range of the display.
                                                             0x14(20) = 2000K
                                                             0x15(21)= 2100K
                                                             0x16(22) = 2200K
                                                             ………………
                                                             0x61(97) = 9700K
                                                             0x62(98) = 9800K
                                                             0x63(99) = 9900K
                                                             0x64(100) = 10000K

NOTE: Following table applicable for Phoenix 2.0 platform only (year 2015
BDLxx70EL/BDLxx90VL/BDLxx30QL/BDLxx35QL)

 Bytes         Bytes Description                    Bits     Description
 DATA[0]       0x12 = Color Temperature                      Command reports to the host controller the current
               100K – Report                                 color temperature 100K steps of the display.
 DATA[1]       Color temperature steps                       20 to 100 of the user selectable range of the display.
                                                             0x1A(26) = 2600K
                                                             0x1B(27) = 2700K
                                                             0x1C(28) = 2800K
                                                             ………………
                                                             0x61(97) = 9700K
                                                             0x62(98) = 9800K
                                                             0x63(99) = 9900K
                                                             0x64(100) = 10000K

Example: The current color temperature is set to 10000K (Display address 01)
 MsgSize Control Group               Data (0)      Data (1)   Checksum
 0x06       0x01         0x00        0x12          0x64       0x71



```

###### 5.1.9.3 Message-Set Color Temperature 100K steps

```text

 Bytes         Bytes Description                    Bits     Description
 DATA[0]       0x11 = Color Temperature                      Command to change the current color temperature
               100K steps – Set                              100K steps
 DATA[1]       Color temperature                             20 to 100 of the user selectable range of the display.
                                                             0x14(20) = 2000K


                                                             0x15(21)= 2100K
                                                             0x16(22) = 2200K
                                                             ………………
                                                             0x61(97) = 9700K
                                                             0x62(98) = 9800K
                                                             0x63(99) = 9900K
                                                             0x64(100) = 10000K

NOTE: Following table applicable for Phoenix 2.0 platform only (year 2015
BDLxx70EL/BDLxx90VL/BDLxx30QL/BDLxx35QL)

 Bytes         Bytes Description                    Bits     Description
 DATA[0]       0x11 = Color Temperature                      Command to change the current color temperature
               100K steps – Set                              100K steps
 DATA[1]       Color temperature                             20 to 100 of the user selectable range of the display.
                                                             0x1A(26) = 2600K
                                                             0x1B(27) = 2700K
                                                             0x1C(28) = 2800K
                                                             ………………
                                                             0x61(97) = 9700K
                                                             0x62(98) = 9800K
                                                             0x63(99) = 9900K
                                                             0x64(100) = 10000K

Example: The current color temperature is set to 10000K (Display address 01)
 MsgSize Control Group               Data (0)      Data (1)   Checksum
 0x06       0x01         0x00        0x11          0x64       0x72





```
