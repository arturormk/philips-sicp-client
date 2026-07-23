# Display Orientation

Source: `docs/Philips_SICP_Commands.md`, lines 4252-4345.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 7.11.1 Message-Get
- 7.11.2 Message-Report
- 7.11.3 Message-Set

## DATA[0] Codes

- `0x16` - Display Orientation –                    Command requests the display to report its current
- `0x16` - Display Orientation                          Command reports Display orientation status
- `0x17` - Display Orientation Set                      Command sets Display orientation details

## Source Excerpt
#### 7.11 Display Orientation

```text

The command is used to set/get the Orientation of the display.
The command is only available in dragon 1.0 & 1.5 & 1.6 & Himalaya 2.0 platforms & CRD50 from
firmware version x.xx



```

##### 7.11.1 Message-Get

```text


 Bytes        Bytes Description                    Bits       Description
 DATA[0]      0x16 = Display Orientation –                    Command requests the display to report its current
              Get                                             Display orientation status

Example: (Display address 01)
 MsgSize Control Group            Data (0)     Checksum
 0x05        0x01        0x00     0x16         0x12


```

##### 7.11.2 Message-Report

```text

Himalaya2.0 platform only support OSD Rotation(DATA[2]) and Image rotation on main window(DATA[4]).
CRD50 don’t support image OSD rotation & Data4 > 7, the OSD is rotated together with the image.

 Bytes       Bytes Description                         Bits      Description
 DATA[0]     0x16 = Display Orientation                          Command reports Display orientation status
             Report
 DATA[1]     Auto Rotate                                         0x00 = Off
                                                                 0x01 = On
                                                                 (only available on Dragon 1 & 1.5 platform)
 DATA[2]     OSD Rotation                                        0x00 = Landscape
                                                                 0x01 = Portrait
 DATA[3]     Image All                                           0x00 = Off
                                                                 0x01 = On (not supported on the CRD50)
                                                                 0x02 = On Clock Wise*
                                                                 0x03 = On Counter Clock Wise*
                                                                 (*) only supported on the CRD50
 DATA[4]     Display Window 1(Main)                              0x00 = Off
                                                                 0x01 = On
 DATA[5]     Display Window 2(Sub1)                              0x00 = Off
                                                                 0x01 = On
 DATA[6]     Display Window 3(Sub2)                              0x00 = Off
                                                                 0x01 = On
 DATA[7]     Display Window 4(Sub3)                              0x00 = Off
                                                                 0x01 = On


```

##### 7.11.3 Message-Set

```text

    Himalaya2.0 platform only support OSD Rotation(DATA[2]) and Image rotation on main window(DATA[4]).
    CRD50 don’t support image OSD rotation & Data4 > 7, the OSD is rotated together with the image.


 Bytes       Bytes Description                         Bits      Description
 DATA[0]     0x17 = Display Orientation Set                      Command sets Display orientation details
 DATA[1]     Auto Rotate                                         0x00 = Off
                                                                 0x01 = On

                                                                      (only available on Dragon 1 & 1.5 platform)

  DATA[2]       OSD Rotation                                          0x00 = Landscape
                                                                      0x01 = Portrait
  DATA[3]       Image All                                             0x00 = Off
                                                                      0x01 = On (not supported on the CRD50)
                                                                      0x02 = On Clock Wise*
                                                                      0x03 = On Counter Clock Wise*
                                                                      (*) only supported on the CRD50
  DATA[4]       Display Window 1(Main)                                0x00 = Off
                                                                      0x01 = On
  DATA[5]       Display Window 2(Sub1)                                0x00 = Off
                                                                      0x01 = On
  DATA[6]       Display Window 3(Sub2)                                0x00 = Off
                                                                      0x01 = On
  DATA[7]       Display Window 4(Sub3)                                0x00 = Off
                                                                      0x01 = On
Example: 0C 01 00 17 00 00 01 00 00 00 00 1B portrait image, OSD normal

```
