# Custom Multi-Window Settings

Source: `docs/Philips_SICP_Commands.md`, lines 5954-6088.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 10.1.1 Message-Set
- 10.1.2 Message-Get (report) –
- 10.1.3 Message-Set

## DATA[0] Codes

- `0xFB` - Execute Custom                               Command requests the display to set the image of
- `0xFD` - Custom Multi-Win –                                    Command report to the host controller the
- `0xFC` - Custom Multi-Win –                             Command requests the display to set the image

## Source Excerpt
### 10 Custom Multi-Window Settings

```text
 This command is used to set or get screen divisions – called windows on the display screen & configure the
 multi window individually. A window contains the video from a particular input source.

 NOTE: Width, Height parameters can’t be higher than the LCD panel resolution. Aspect ratio 16:9 is only
 supported.

```

##### 10.1.1 Message-Set

```text

  Bytes         Bytes Description                        Bits       Description
  DATA[0]       0xFB = Execute Custom                               Command requests the display to set the image of
                Multi-Win – Set                                     window.
  DATA[1]       Switch Custom Multi-Win                             0x00 = Custom Multi-Win OFF
                                                                    0x01 = Custom Multi-Win ON
  DATA[2]       Windows                                             0x00 = Open one window


                                                                               0x01 = Open two windows
                                                                               0x02 = Open three windows
                                                                               0x03 = Open four windows

Example: Set Display address 01, Custom Multi-Win ON, open 3 windows,
   MsgSize         Control         Group          Data (0)        Data (1)                               Data (2)           Checksum
    0x07             0x01            0x00          0xFB            0x01                                   0x02                0xFE

```

##### 10.1.2 Message-Get (report) –

```text

SPECIAL NOTE: Dragon 1.x & 1.6 platform supports only a maximum of 2 windows. Main window and a sub(x) window.

This message report can be just about which window is currently active or can be very detailed. Both examples are presented after the table.

 Bytes            Bytes Description                                Bits        Description
 DATA[0]          0xFD = Custom Multi-Win –                                    Command report to the host controller the
                  Report                                                       window’s information of the display.
 DATA[1]          Window                                                       0x00 = Main(Display Win1)
                                                                               0x01 = Sub1(Display Win2)
                                                                               0x02 = Sub2(Display Win3)
                                                                               0x03 = Sub3(Display Win4)
 DATA[2]          Image rotation                                               0x00 = ROT_NONE (OFF)
                                                                               0x01 = ROT_90 (ON)
                                                                               0x02 = ROT_270,
                                                                               0x03 = ROT_H_MIRROR
                                                                               0x04 = ROT_V_MIRROR
                                                                               0x05 = ROT_HV_MIRROR
 DATA[3]          X position of image(High byte)                               X position of image(High byte)
 DATA[4]          X position of image(Low byte)                                X position of image(Low byte)
 DATA[5]          Y position of image(High byte)                               Y position of image(High byte)
 DATA[6]          Y position of image(Low byte)                                Y position of image(Low byte)
 DATA[7]          Width of image(High byte)                                    Width of image(High byte)
 DATA[8]          Width of image(Low byte)                                     Width of image(Low byte)
 DATA[9]          Height of image(High byte)                                   Height of image(High byte)
 DATA[10]         Height of image(Low byte)                                    Height of image(Low byte)
 DATA[11]         Picture Format                                               Picture Format.
                                                                               0x00 = Normal (4:3)
                                                                               0x01 = Custom
                                                                               0x02 = Real (1:1)
                                                                               0x03 = Full
                                                                               0x04 = 21:9
                                                                               0x05 = Dynamic
                                                                               0x06 = 16:9
                                                                               0xFF = Current setting(don’t change)

SPECIAL NOTE: Dragon 1.x platform doesn’t support DATA [11] value 0x05.

Example: Display address 01, Main window, ROT_NONE, X:0, Y:0, W:1920, H:1080, Zoom mode: Full
  MsgSize        Control         Group        Data (0)       Data (1)      Data (2)        Data (3)                                         Data (4)
   0x10            0x01           0x01         0xFD           0x00           0x00             0x00                                           0x00
  Data (5)       Data (6)       Data (7)      Data (8)       Data (9)      Data (10)       Data (11)                                       Checksum
   0x00            0x00           0x07         0x80           0x04           0x38             0x03                                           0x55

Example: Get information of Main window (Display address 01)
 MsgSize Control         Group       Data (0)     Data (1)   Checksum
   0x06        0x01        0x00       0xFD         0x00        0xFA

```

##### 10.1.3 Message-Set

```text


  SPECIAL NOTE: 2016 Dragon 1.x platform supports only a maximum of 2 windows. Main window and a sub(x) window.

      Bytes       Bytes Description                          Bits       Description
      DATA[0]     0xFC = Custom Multi-Win –                             Command requests the display to set the image
                  Set                                                   data of window.
      DATA[1]     Window                                                0x00 = Main(Display Win1)
                                                                        0x01 = Sub1(Display Win2)
                                                                        0x02 = Sub2(Display Win3)
                                                                        0x03 = Sub3(Display Win4)
      DATA[2]     Image rotation                                        0x00 = ROT_NONE (OFF)
                                                                        0x01 = ROT_90 (ON)
                                                                        0x02 = ROT_270,
                                                                        0x03 = ROT_H_MIRROR
                                                                        0x04 = ROT_V_MIRROR
                                                                        0x05 = ROT_HV_MIRROR
      DATA[3]     X position of image(High byte)                        X position of image(High byte)
      DATA[4]     X position of image(Low byte)                         X position of image(Low byte)
      DATA[5]     Y position of image(High byte)                        Y position of image(High byte)
      DATA[6]     Y position of image(Low byte)                         Y position of image(Low byte)
      DATA[7]     Width of image(High byte)                             Width of image(High byte)
      DATA[8]     Width of image(Low byte)                              Width of image(Low byte)
      DATA[9]     Height of image(High byte)                            Height of image(High byte)
      DATA[10]    Height of image(Low byte)                             Height of image(Low byte)
      DATA[11]    Picture Format                                        Picture Format.
                                                                        0x00 = Normal
                                                                        0x01 = Custom
                                                                        0x02 = Real
                                                                        0x03 = Full
                                                                        0x04 = 21:9
                                                                        0x05 = Dynamic
                                                                        0x06 = 16:9
                                                                        0xFF = Current setting(don’t change)

  SPECIAL NOTE: Dragon 1.x platform doesn’t support DATA [11] value 0x05.

  Example: Set Display address 01, Main window, ROT_NONE, X:0, Y:0, W:1280, H:2160, Zoom mode: Full
    MsgSize        Control         Group         Data (0)      Data (1)       Data (2)       Data (3)                          Data (4)
     0x10            0x01           0x00          0xFC          0x00            0x00           0x00                             0x00
    Data (5)       Data (6)        Data (7)      Data (8)      Data (9)       Data (10)     Data (11)                         Checksum
     0x00            0x00           0x07           0x80         0x04            0x38           0x03                             0x55


```
