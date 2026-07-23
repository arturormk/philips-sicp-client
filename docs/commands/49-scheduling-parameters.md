# Scheduling Parameters

Source: `docs/Philips_SICP_Commands.md`, lines 5704-5898.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 8.1.1 Message-Get
- 8.1.2 Message-Report
- 8.1.3 Message-Set

## DATA[0] Codes

- `0x5B` - Scheduling                                      Command requests the display to report its current
- `0x5B` - Scheduling                                Command reports to the host controller the current
- `0x5A` - Scheduling                                 Command to change the current Scheduling parameters

## Source Excerpt
#### 8.1 Scheduling Parameters

```text
       The following commands are used to get/set scheduling parameters as it is defined below.

```

##### 8.1.1 Message-Get

```text

        Bytes              Bytes Description                           Bits       Description
        DATA[0]            0x5B = Scheduling                                      Command requests the display to report its current
                           Parameters – Get                                       Scheduling parameters.
        DATA[1]            Page                                                   1 to 7 of the scheduling pages

       Example: (Display address 01)
        MsgSize Control Group                    Data (0)       Data (1)         Checksum
        0x06        0x01        0x00             0x5B           0x01             0x5D



```

##### 8.1.2 Message-Report

```text

       Only Dragon 1.x & 1.6 & Himalay 2.0 platform supports additional DATA[8] to indicate playlist/bookmark/file number

        Bytes              Bytes Description                       Bits     Description
        DATA[0]            0x5B = Scheduling                                Command reports to the host controller the current
                           Parameters – Report                              Scheduling parameters of the display.
        DATA[1]            Page                                             0: Page disable
                                                                            1: Page enable
        DATA[2]            Start time hour                                  0 to 23 of the start time hour
                                                                            24: NULL
        DATA[3]            Start time minute                                0 to 59 of the start time minute
                                                                            60: NULL
        DATA[4]            End time hour                                    0 to 23 of the end time hour
                                                                            24: NULL


DATA[5]   End time minute                             0 to 59 of the end time minute
                                                      60: NULL
DATA[6]   Video source                                0 to 100 (%) of the user selectable range of the display.
                                                      For video source:
                                                      0x00 = NULL
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
                                                                     0x16=Media Player
                                                                     0x17=PDF Player
                                                                     0x18=Custom
                                                                     0x19 = HDMI 4
                                                                     0x1A = VGA2
                                                                     0x1B = VGA3
                                                                     0x1C = IWB
 DATA[7]            Working day(s)                                   To set the scheduling working days.
                                                                     Bit0 = 1: every week
                                                                     Bit1 = Monday
                                                                     Bit2 = Tuesday
                                                                     Bit3 = Wednesday
                                                                     Bit4 = Thursday
                                                                     Bit5 = Friday
                                                                     Bit6 = Saturday
                                                                     Bit7 = Sunday
 DATA[8]            Bookmark/Playlist/File Tag(s)                    To set the set Tag from 1 through 7
                                                                     0x01 = Tag 1
                                                                     0x02 = Tag 2
                                                                     0x03 = Tag 3
                                                                     0x04 = Tag 4
                                                                     0x05 = Tag 5
                                                                     0x06 = Tag 6
                                                                     0x07 = Tag 7

Example: Report page1 with HDMI starts at 06:30 and ends at 22:00 every day.
 MsgSize Control Group             Data (0) Data (1)         Data (2)      Data (3)                    Data (4)      Data (5)
 0x0C       0x01       0x00        0x5B        0x01          0x06          0x1E                        0x16          0x00
 Data (6) Data (7) Checksum
 0x0A       0xFF       0xAC

```

##### 8.1.3 Message-Set

```text

Only Dragon 1.x & 1.6 & Himalay 2.0 platform supports additional DATA[8] to indicate playlist/bookmark/file number

 Bytes              Bytes Description                      Bits       Description
 DATA[0]            0x5A = Scheduling                                 Command to change the current Scheduling parameters
                    Parameters – Set
 DATA[1]            Page                                              BIT 7-BIT4:
                                                                      1 to 7 of the scheduling pages
                                                                      BIT 3-BIT0:
                                                                      0: Page disable
                                                                      1: Page enable
 DATA[2]            Start time hour                                   0 to 23 of the start time hour
                                                                      24: NULL
 DATA[3]            Start time minute                                 0 to 59 of the start time minute
                                                                      60: NULL
 DATA[4]            End time hour                                     0 to 23 of the end time hour
                                                                      24: NULL
 DATA[5]            End time minute                                   0 to 59 of the end time minute
                                                                      60: NULL





 DATA[6]         Video source                                0 to 100 (%) of the user selectable range of the display.
                                                             For video source:
                                                             0x00 = NULL
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
                                                             0x16=Media Player
                                                             0x17=PDF Player
                                                             0x18=Custom
                                                             0x19= HDMI 4
                                                             0x1A = VGA2
                                                             0x1B = VGA3
                                                             0x1C = IWB
 DATA[7]         Working day(s)                              To set the scheduling working days.
                                                             Bit0 = 1: every week
                                                             Bit1 = Monday
                                                             Bit2 = Tuesday
                                                             Bit3 = Wednesday
                                                             Bit4 = Thursday
                                                             Bit5 = Friday
                                                             Bit6 = Saturday
                                                             Bit7 = Sunday
 DATA[8]         Bookmark/Playlist/File Tag(s)               To set the set Tag from 1 through 7
                                                             0x01 = Tag 1
                                                             0x02 = Tag 2
                                                             0x03 = Tag 3
                                                             0x04 = Tag 4
                                                             0x05 = Tag 5
                                                             0x06 = Tag 6
                                                             0x07 = Tag 7

Example: Set page1 with HDMI starts at 06:30 and ends at 22:00 every day.
 MsgSize Control Group                Data (0)    Data (1)    Data (2)        Data (3)     Data (4)     Data (5)
 0x0C        0x01       0x00          0x5A        0x10        0x06            0x1E         0x16         0x00
 Data (6) Data (7) Checksum
 0x0A        0xFF       0xBC





```
