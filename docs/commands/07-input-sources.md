# Input Sources

Source: `docs/Philips_SICP_Commands.md`, lines 861-1111.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 4.4.1.1 Message-Set
- 4.4.1.2 Message-Get
- 4.4.1.3 Message-Report

## DATA[0] Codes

- `0xAC` - Input Source – Set                              Command requests the display to set the current
- `0xAD` - Current Source – Get                               Command requests the display to report the
- `0xAD` - Current Source –                                   Command reports to the host controller the

## Source Excerpt
#### 4.4 MESSAGES – INPUT SOURCES

```text


```

##### 4.4.1 Input Source

```text

This command is used to change or to get the current input source.


```

###### 4.4.1.1 Message-Set

```text

DATA[1] : set the current source value as below.

DATA[2]: playlist number for PDF player and Media player source input and URL number for source input browser


 Bytes              Bytes Description                           Bits       Description
 DATA[0]            0xAC = Input Source – Set                              Command requests the display to set the current
                                                                           input source
 DATA[1]            Input Source Type/Number                               0x01 = VIDEO
                                                                           0x02 = S-VIDEO
                                                                           0x03 = COMPONENT
                                                                           0x04 = CVI 2 (not applicable)
                                                                           0x05 = VGA
                                                                           0x06 = HDMI 2
                                                                           0x07 = Display Port 2
                                                                           0x08 = USB 2
                                                                           0x09 = Card DVI-D
                                                                           0x0A = Display Port 1
                                                                           0x0B = Card OPS
                                                                           0x0C = USB 1
                                                                           0x0D = HDMI
                                                                           0x0E = DVI-D
                                                                           0x0F = HDMI3
                                                                           0x10 = BROWSER
                                                                           0x11= SMARTCMS
                                                                           0X12= DMS (Digital Media Server)
                                                                           0x13= INTERNAL STORAGE
                                                                           0x14 = Reserved
                                                                           0x15 = Reserved
                                                                           0x16= Media Player
                                                                           0x17= PDF Player
                                                                           0x18= Custom
                                                                           0x19 = HDMI 4
                                                                           0x1A =VGA2
                                                                           0x1B = VGA3
                                                                           0x1C = IWB





  DATA[2]         Start playlist file number on source              0x01 = playlist file 1 or URL 1
                  input media player or PDF player.                 0x02 = playlist file 2 or URL 2
                  Start URL number on browser                       0x03 = playlist file 3 or URL 3
                  input.                                            0x04 = playlist file 4 or URL 4
                  Only working on: Dragon 1, Dragon                 0x05 = playlist file 5 or URL 5
                 1.5, 10BDL3051T, dragon 1.5,                       0x06 = playlist file 6 or URL 6
                 Himalaya 2 & QL3 (see the
                                                                    0x07 = playlist file 7 or URL 7
                 platform list)
                                                                    0x08 = reserved
                 From firmware version : TBC                        0x09 = reserved
                 The monitor will start to display the              0x0A = reserved
                 playlist or URL number.                            0x0B = reserved
                                                                    0x0C = reserved
                                                                    0x0D = reserved
                                                                    0x0E = reserved
                                                                    0x0F = reserved
                                                                    0x10 = reserved
                                                                    0x11 = reserved
                                                                    0X12 = reserved
                                                                    0X13 = reserved
                                                                    0x14 = reserved
                                                                    0x15 = reserved
                                                                    0x16 = reserved
                                                                    0x17 = reserved
                                                                    0x18 = reserved

  DATA[3]         OSD Style                               Bit7      Reserved
                                                          Bit6      Do not switch.
                                                                    Source is made current. Set is updated with the
                                                                    details of this source; however, source change is
                                                                    performed.
                                                                    1 = Do not switch. 0 = Switch
                                                          Bit2.0    Source info. Display Style
                                                                    0 = Reserved
                                                                    1 = Source label
  DATA[4]         Mute Style                              Bit 7     (Reserved, value is 0)
                                                          Bit 6     (Reserved, value is 0)
                                                          Bit 5     (Reserved, value is 0)
                                                          Bit 4     (Reserved, value is 0)
                                                          Bit 3     (Reserved, value is 0)
                                                          Bit 2     (Reserved, value is 0)
                                                          Bit 1     (Reserved, value is 0)
                                                          Bit 0     (Reserved, value is 0)

 Example: Set on DVI-D with Source label displaying on OSD (Display address 01)
  MsgSize Control Group               Data (0)      Data (1)   Data (2)     Data (3)     Data (4)     Checksum
  0x09        0x01       0x00         0xAC          0x09       0x09         0x01         0x00         0xA5

Source command examples:
HDMI 1 :     09 01 00 AC 0D 09 01 00 A1                Ack: 06 01 01 00 06 00
HDMI 2 :     09 01 00 AC 06 09 01 00 AA                Ack: 06 01 01 00 06 00
HDMI 3 :     09 01 00 AC 0F 09 01 00 A3                Ack: 06 01 01 00 06 00
HDMI 4:      09 01 00 AC 19 09 01 00 B5                Ack: 06 01 01 00 06 00
DVI :        09 01 00 AC 0E 09 01 00 A2                Ack: 06 01 01 00 06 00
AV :         09 01 00 AC 01 09 01 00 AD                Ack: 06 01 01 00 06 00
YPBPR :      09 01 00 AC 03 09 01 00 AF                Ack: 06 01 01 00 06 00
VGA :        09 01 00 AC 05 09 01 00 A9                Ack: 06 01 01 00 06 00
DP :         09 01 00 AC 0A 09 01 00 A6                Ack: 06 01 01 00 06 00
USB :        09 01 00 AC 0C 09 01 00 A0                Ack: 06 01 01 00 06 00

OPS :                09 01 00 AC 0B 09 01 00 A7                  Ack: 06 01 01 00 06 00
BROWSER:             09 01 00 AC 10 09 01 00 BC                  Ack: 06 01 01 00 06 00
SMARTCMS:            09 01 00 AC 11 09 01 00 BD                  Ack: 06 01 01 00 06 00
Media player:        09 01 00 AC 16 09 01 00 BA                  Ack: 06 01 01 00 06 00
PDF player:          09 01 00 AC 17 09 01 00 BB                  Ack: 06 01 01 00 06 00
Custom :             09 01 00 AC 18 09 01 00 B4                  Ack: 06 01 01 00 06 00



```

###### 4.4.1.2 Message-Get

```text

  Bytes              Bytes Description                              Bits       Description
  DATA[0]            0xAD = Current Source – Get                               Command requests the display to report the
                                                                               current input source in use.

 Example: (Display address 01)
  MsgSize Control Group                      Data (0)       Checksum
  0x05        0x01        0x00               0xAD           0xA9

```

###### 4.4.1.3 Message-Report

```text

 DATA[1] will get the current source value as below.
 DATA[2] will get the current selected playlist or URL number if current source is PDF player, Browser, Media player.
 DATA[3], DATA[4] can be ignored by requestor or may not be returned by device depending on model .

  Bytes              Bytes Description                              Bits       Description
  DATA[0]            0xAD = Current Source –                                   Command reports to the host controller the
                     Report                                                    current input source in use by the display.
  DATA[1]            Input Source Type/Number                                  0x01 = VIDEO
                                                                               0x02 = S-VIDEO
                                                                               0x03 = COMPONENT
                                                                               0x04 = CVI 2 (not applicable)
                                                                               0x05 = VGA
                                                                               0x06 = HDMI 2
                                                                               0x07 = Display Port 2
                                                                               0x08 = USB 2
                                                                               0x09 = Card DVI-D
                                                                               0x0A = Display Port 1
                                                                               0x0B= Card OPS
                                                                               0x0C = USB 1
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
                                                                               0x19 = HDMI 4
                                                                               0x1A =VGA2
                                                                               0x1B = VGA3
                                                                               0x1C = IWB





DATA[2]    Get the selected playlist file number             0x00 = no playlist or URL
           on source input media player or                   0x01 = playlist file 1 or URL 1
           PDF player.                                       0x02 = playlist file 2 or URL 2
           Get the selected URL number on                    0x03 = playlist file 3 or URL 3
           browser input.                                    0x04 = playlist file 4 or URL 4
                                                             0x05 = playlist file 5 or URL 5
           Only working on: Dragon 1, Dragon                 0x06 = playlist file 6 or URL 6
          1.5, 10BDL3051T, dragon 1.5,
                                                             0x07 = playlist file 7 or URL 7
          Himalaya 2 & QL3 (see the
          platform list)                                     0x08 = reserved
                                                             0x09 = reserved
           From firmware version : TBC                       0x0A = reserved
                                                             0x0B = reserved
                                                             0x0C = reserved
                                                             0x0D = reserved
                                                             0x0E = reserved
                                                             0x0F = reserved
                                                             0x10 = reserved
                                                             0x11 = reserved
                                                             0X12 = reserved
                                                             0X13 = reserved
                                                             0x14 = reserved
                                                             0x15 = reserved
                                                             0x16 = reserved
                                                             0x17 = reserved
                                                             0x18 = reserved





                                                                   0x17= PDF Player
                                                                   0x18= Custom
 DATA[3]        OSD Style                               Bit7       Reserved
                                                        Bit6       Reserved
                                                        Bit2.0     Source info. Display Style
                                                                   0 = Reserved
                                                                   1 = Source label
 DATA[4]        Mute Style                              Bit 7      (Reserved, value is 0)
                                                        Bit 6      (Reserved, value is 0)
                                                        Bit 5      (Reserved, value is 0)
                                                        Bit 4      (Reserved, value is 0)
                                                        Bit 3      (Reserved, value is 0)
                                                        Bit 2      (Reserved, value is 0)
                                                        Bit 1      (Reserved, value is 0)
                                                        Bit 0      (Reserved, value is 0)

Example: Current Input Source: VIDEO (Display address 01)

 MsgSize    Control    Group       Data (0)   Data          Data       Data         Data        Checksum
                                              (1)           (2)        (3)          (4)
 0x09       0x01       0x00        0xAD       0xFD          0x01       0x00         0x00        0x59





```
