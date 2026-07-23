# Auto Signal Detecting / Failover

Source: `docs/Philips_SICP_Commands.md`, lines 1112-2032.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 4.5.1 Message-Get
- 4.5.2 Message-Report
- 4.5.3 Message-Set
- 4.5.4 Message-Get
- 4.5.5 Message-Report
- 4.5.6 Message-Set

## DATA[0] Codes

- `0xAF` - Auto Signal                                       Command requests the display to report its current
- `0xAF` - Auto Signal Detecting –                              Command reports Auto Signal Detecting Setting
- `0xAE` - Auto Signal                                       Command to change the Auto Signal Detecting
- `0xA6` - Failover – Get                           Command requests the display to report its
- `0xA6` - Failover – Report                           Command reports Failover Setting
- `0xA5` - Failover – Set                          Command to change the Failover setting of the

## Source Excerpt
#### 4.5 Auto Signal Detecting / Failover

```text



Failover means, if current input source has no signal system will switch to another based on settings as defined by commands below.
The specification file explains the usage/behaviour.

```

##### 4.5.1 Message-Get

```text

 Bytes            Bytes Description                             Bits       Description
 DATA[0]          0xAF = Auto Signal                                       Command requests the display to report its current
                  Detecting – Get                                          Auto Signal Detecting status

Example: (Display address 01)
 MsgSize Control Group                      Data (0)       Checksum
 0x05        0x01        0x00               0xAF           0xAB

```

##### 4.5.2 Message-Report

```text

 Bytes            Bytes Description                                 Bits      Description
 DATA[0]          0xAF = Auto Signal Detecting –                              Command reports Auto Signal Detecting Setting
                  Report
 DATA[1]          On / All / PC sources only /                                0x00 = Off
                  Video sources only / Failover                               0x01 = All
                                                                              0x02 = Reserved
                                                                              0x03 = PC sources only
                                                                              0x04 = Video sources only
                                                                              0x05 = Failover

Special Note:

Dragon 1.0 (see platform ) excludes DATA [1] values below
0x03 = PC sources only 0x04 = Video sources only

Example: Current Display settings: Off and All (Display address 01)
 MsgSize Control Group                 Data (0)     Data (1)     Checksum
 0x06       0x01         0x00          0xAF         0x00         0xA8
 0x06       0x01         0x00          0xAF         0x01         0xA9

```

##### 4.5.3 Message-Set

```text

 Bytes            Bytes Description                             Bits       Description
 DATA[0]          0xAE = Auto Signal                                       Command to change the Auto Signal Detecting
                  Detecting – Set                                          setting of the display
 DATA[1]          On / All /PC sources only /                              0x00 = Off
                  Video sources only / Failover                            0x01 = All
                                                                           0x02 = Reserved
                                                                           0x03 = PC sources only
                                                                           0x04 = Video sources only
                                                                           0x05 = Failover





Special Note:

2016 Dragon 1.0 (see platform ) excludes DATA [1] values below
0x03 = PC sources only 0x04 = Video sources only

Example: Set the Display to the fallowing: Auto Signal Detecting Off (Display address 01)
 MsgSize Control Group                 Data (0)     Data (1)     Checksum
 0x06        0x01        0x00          0xAE         0x00         0xA9

```

##### 4.5.4 Message-Get

```text

 Bytes           Bytes Description                      Bits     Description
 DATA[0]         0xA6 = Failover – Get                           Command requests the display to report its
                                                                 current Failover status

Example: (Display address 01)
 MsgSize Control Group                Data (0)      Checksum
 0x05        0x01        0x00         0xA6


```

##### 4.5.5 Message-Report

```text

 Bytes            Bytes Description                         Bits     Description
 DATA[0]          0xA6 = Failover – Report                           Command reports Failover Setting
 DATA[1]          HDMI / Component /                                 1st priority:
                  Composite / Display Port /                         0x00 = HDMI
                  DVI-D / VGA / OPS / USB /                          0x01 = Component
                  Browser / SmartCMS /                               0x02 = Composite
                  Internal Storage / DMS / HDMI                      0x03 = Display Port
                  2/ HDMI 3 / USB Playlist / USB                     0x04 = DVI-D
                  AutoPlay / Media Player / PDF                      0x05 = VGA
                  player / Custom/HMDI 4/                            0x06 = OPS
                  VGA2 / VGA3 / IWB                                  0x07 = USB
                                                                     0x08 = Browser
                                                                     0x09 = SmartCMS
                                                                     0x0A= Internal Storage
                                                                     0x0B = DMS (Digital Media Server)
                                                                     0x0C = HDMI2
                                                                     0x0D = HDMI3
                                                                     0x0E = USB Playlist
                                                                     0x0F = USB AutoPlay
                                                                     0x10= Media Player
                                                                     0x11= PDF Player
                                                                     0x12= Custom
                                                                     0x13= HDMI 4
                                                                     0x14 =VGA2
                                                                     0x15 = VGA3
                                                                     0x16 = IWB





DATA[2]   HDMI / Component /                            2nd priority:
          Composite / Display Port /                    0x00 = HDMI
          DVI-D / VGA / OPS / USB /                     0x01 = Component
          Browser / SmartCMS /                          0x02 = Composite
          Internal Storage / DMS / HDMI                 0x03 = Display Port
          2/ HDMI 3 / USB Playlist / USB                0x04 = DVI-D
          AutoPlay / Media Player / PDF                 0x05 = VGA
          player / Custom/HMDI 4/                       0x06 = OPS
          VGA2 / VGA3 / IWB                             0x07 = USB
                                                        0x08 = Browser
                                                        0x09 = SmartCMS
                                                        0x0A= Internal Storage
                                                        0x0B = DMS (Digital Media Server)
                                                        0x0C = HDMI2
                                                        0x0D = HDMI3
                                                        0x0E = USB Playlist
                                                        0x0F = USB AutoPlay
                                                        0x10= Media Player
                                                        0x11= PDF Player
                                                        0x12= Custom
                                                        0x13 = HDMI 4
                                                        0x14 =VGA2
                                                        0x15 = VGA3
                                                        0x16 = IWB
DATA[3]   HDMI / Component /                            3rd priority:
          Composite / Display Port /                    0x00 = HDMI
          DVI-D / VGA / OPS / USB /                     0x01 = Component
          Browser / SmartCMS /                          0x02 = Composite
          Internal Storage / DMS / HDMI                 0x03 = Display Port
          2/ HDMI 3 / USB Playlist / USB                0x04 = DVI-D
          AutoPlay / Media Player / PDF                 0x05 = VGA
          player / Custom/HMDI 4/                       0x06 = OPS
          VGA2 / VGA3 / IWB                             0x07 = USB
                                                        0x08 = Browser
                                                        0x09 = SmartCMS
                                                        0x0A= Internal Storage
                                                        0x0B = DMS (Digital Media Server)
                                                        0x0C = HDMI2
                                                        0x0D = HDMI3
                                                        0x0E = USB Playlist
                                                        0x0F = USB AutoPlay
                                                        0x10= Media Player
                                                        0x11= PDF Player
                                                        0x12= Custom
                                                        0x13 = HDMI 4
                                                        0x14 =VGA2
                                                        0x15 = VGA3
                                                        0x16 = IWB





DATA[4]   HDMI / Component /                            4th priority:
          Composite / Display Port /                    0x00 = HDMI
          DVI-D / VGA / OPS / USB /                     0x01 = Component
          Browser / SmartCMS /                          0x02 = Composite
          Internal Storage / DMS / HDMI                 0x03 = Display Port
          2/ HDMI 3 / USB Playlist / USB                0x04 = DVI-D
          AutoPlay / Media Player / PDF                 0x05 = VGA
          player / Custom/HMDI 4/                       0x06 = OPS
          VGA2 / VGA3 / IWB                             0x07 = USB
                                                        0x08 = Browser
                                                        0x09 = SmartCMS
                                                        0x0A= Internal Storage
                                                        0x0B = DMS (Digital Media Server)
                                                        0x0C = HDMI2
                                                        0x0D = HDMI3
                                                        0x0E = USB Playlist
                                                        0x0F = USB AutoPlay
                                                        0x10= Media Player
                                                        0x11= PDF Player
                                                        0x12= Custom
                                                        0x13 = HDMI 4
                                                        0x14 =VGA2
                                                        0x15 = VGA3
                                                        0x16 = IWB
DATA[5]   HDMI / Component /                            5th priority:
          Composite / Display Port /                    0x00 = HDMI
          DVI-D / VGA / OPS / USB /                     0x01 = Component
          Browser / SmartCMS /                          0x02 = Composite
          Internal Storage / DMS / HDMI                 0x03 = Display Port
          2/ HDMI 3 / USB Playlist / USB                0x04 = DVI-D
          AutoPlay / Media Player / PDF                 0x05 = VGA
          player / Custom/HMDI 4/                       0x06 = OPS
          VGA2 / VGA3 / IWB                             0x07 = USB
                                                        0x08 = Browser
                                                        0x09 = SmartCMS
                                                        0x0A= Internal Storage
                                                        0x0B = DMS (Digital Media Server)
                                                        0x0C = HDMI2
                                                        0x0D = HDMI3
                                                        0x0E = USB Playlist
                                                        0x0F = USB AutoPlay
                                                        0x10= Media Player
                                                        0x11= PDF Player
                                                        0x12= Custom
                                                        0x13 = HDMI 4
                                                        0x14 =VGA2
                                                        0x15 = VGA3
                                                        0x16 = IWB





DATA[6]   HDMI / Component /                            6th priority:
          Composite / Display Port /                    0x00 = HDMI
          DVI-D / VGA / OPS / USB /                     0x01 = Component
          Browser / SmartCMS /                          0x02 = Composite
          Internal Storage / DMS / HDMI                 0x03 = Display Port
          2/ HDMI 3 / USB Playlist / USB                0x04 = DVI-D
          AutoPlay / Media Player / PDF                 0x05 = VGA
          player / Custom/HMDI 4/                       0x06 = OPS
          VGA2 / VGA3 / IWB                             0x07 = USB
                                                        0x08 = Browser
                                                        0x09 = SmartCMS
                                                        0x0A= Internal Storage
                                                        0x0B = DMS (Digital Media Server)
                                                        0x0C = HDMI2
                                                        0x0D = HDMI3
                                                        0x0E = USB Playlist
                                                        0x0F = USB AutoPlay
                                                        0x10= Media Player
                                                        0x11= PDF Player
                                                        0x12= Custom
                                                        0x13 = HDMI 4
                                                        0x14 =VGA2
                                                        0x15 = VGA3
                                                        0x16 = IWB
DATA[7]   HDMI / Component /                            7th priority:
          Composite / Display Port /                    0x00 = HDMI
          DVI-D / VGA / OPS / USB /                     0x01 = Component
          Browser / SmartCMS /                          0x02 = Composite
          Internal Storage / DMS / HDMI                 0x03 = Display Port
          2/ HDMI 3 / USB Playlist / USB                0x04 = DVI-D
          AutoPlay / Media Player / PDF                 0x05 = VGA
          player / Custom/HMDI 4/                       0x06 = OPS
          VGA2 / VGA3 / IWB                             0x07 = USB
                                                        0x08 = Browser
                                                        0x09 = SmartCMS
                                                        0x0A= Internal Storage
                                                        0x0B = DMS (Digital Media Server)
                                                        0x0C = HDMI2
                                                        0x0D = HDMI3
                                                        0x0E = USB Playlist
                                                        0x0F = USB AutoPlay
                                                        0x10= Media Player
                                                        0x11= PDF Player
                                                        0x12= Custom
                                                        0x13 = HDMI 4
                                                        0x14 =VGA2
                                                        0x15 = VGA3
                                                        0x16 = IWB





DATA[8]   HDMI / Component /                            8th priority:
          Composite / Display Port /                    0x00 = HDMI
          DVI-D / VGA / OPS / USB /                     0x01 = Component
          Browser / SmartCMS /                          0x02 = Composite
          Internal Storage / DMS / HDMI                 0x03 = Display Port
          2/ HDMI 3 / USB Playlist / USB                0x04 = DVI-D
          AutoPlay / Media Player / PDF                 0x05 = VGA
          player / Custom/HMDI 4/                       0x06 = OPS
          VGA2 / VGA3 / IWB                             0x07 = USB
                                                        0x08 = Browser
                                                        0x09 = SmartCMS
                                                        0x0A= Internal Storage
                                                        0x0B = DMS (Digital Media Server)
                                                        0x0C = HDMI2
                                                        0x0D = HDMI3
                                                        0x0E = USB Playlist
                                                        0x0F = USB AutoPlay
                                                        0x10= Media Player
                                                        0x11= PDF Player
                                                        0x12= Custom
                                                        0x13 = HDMI 4
                                                        0x14 =VGA2
                                                        0x15 = VGA3
                                                        0x16 = IWB
DATA[9]   HDMI / Component /                            9th priority:
          Composite / Display Port /                    0x00 = HDMI
          DVI-D / VGA / OPS / USB /                     0x01 = Component
          Browser / SmartCMS /                          0x02 = Composite
          Internal Storage / DMS / HDMI                 0x03 = Display Port
          2/ HDMI 3 / USB Playlist / USB                0x04 = DVI-D
          AutoPlay / Media Player / PDF                 0x05 = VGA
          player / Custom/HMDI 4/                       0x06 = OPS
          VGA2 / VGA3 / IWB                             0x07 = USB
                                                        0x08 = Browser
                                                        0x09 = SmartCMS
                                                        0x0A= Internal Storage
                                                        0x0B = DMS (Digital Media Server)
                                                        0x0C = HDMI2
                                                        0x0D = HDMI3
                                                        0x0E = USB Playlist
                                                        0x0F = USB AutoPlay
                                                        0x10= Media Player
                                                        0x11= PDF Player
                                                        0x12= Custom
                                                        0x13 = HDMI 4
                                                        0x14 =VGA2
                                                        0x15 = VGA3
                                                        0x16 = IWB





DATA[10]   HDMI / Component /                            10th priority:
           Composite / Display Port /                    0x00 = HDMI
           DVI-D / VGA / OPS / USB /                     0x01 = Component
           Browser / SmartCMS /                          0x02 = Composite
           Internal Storage / DMS / HDMI                 0x03 = Display Port
           2/ HDMI 3 / USB Playlist / USB                0x04 = DVI-D
           AutoPlay / Media Player / PDF                 0x05 = VGA
           player / Custom/HMDI 4/                       0x06 = OPS
           VGA2 / VGA3 / IWB                             0x07 = USB
                                                         0x08 = Browser
                                                         0x09 = SmartCMS
                                                         0x0A= Internal Storage
                                                         0x0B = DMS (Digital Media Server)
                                                         0x0C = HDMI2
                                                         0x0D = HDMI3
                                                         0x0E = USB Playlist
                                                         0x0F = USB AutoPlay
                                                         0x10= Media Player
                                                         0x11= PDF Player
                                                         0x12= Custom
                                                         0x13 = HDMI 4
                                                         0x14 =VGA2
                                                         0x15 = VGA3
                                                         0x16 = IWB
DATA[11]   HDMI / Component /                            11th priority:
           Composite / Display Port /                    0x00 = HDMI
           DVI-D / VGA / OPS / USB /                     0x01 = Component
           Browser / SmartCMS /                          0x02 = Composite
           Internal Storage / DMS / HDMI                 0x03 = Display Port
           2/ HDMI 3 / USB Playlist / USB                0x04 = DVI-D
           AutoPlay / Media Player / PDF                 0x05 = VGA
           player / Custom/HMDI 4/                       0x06 = OPS
           VGA2 / VGA3 / IWB                             0x07 = USB
                                                         0x08 = Browser
                                                         0x09 = SmartCMS
                                                         0x0A= Internal Storage
                                                         0x0B = DMS (Digital Media Server)
                                                         0x0C = HDMI2
                                                         0x0D = HDMI3
                                                         0x0E = USB Playlist
                                                         0x0F = USB AutoPlay
                                                         0x10= Media Player
                                                         0x11= PDF Player
                                                         0x12= Custom
                                                         0x13 = HDMI 4
                                                         0x14 =VGA2
                                                         0x15 = VGA3
                                                         0x16 = IWB





DATA[12]   HDMI / Component /                            12th priority:
           Composite / Display Port /                    0x00 = HDMI
           DVI-D / VGA / OPS / USB /                     0x01 = Component
           Browser / SmartCMS /                          0x02 = Composite
           Internal Storage / DMS / HDMI                 0x03 = Display Port
           2/ HDMI 3 / USB Playlist / USB                0x04 = DVI-D
           AutoPlay / Media Player / PDF                 0x05 = VGA
           player / Custom/HMDI 4/                       0x06 = OPS
           VGA2 / VGA3 / IWB                             0x07 = USB
                                                         0x08 = Browser
                                                         0x09 = SmartCMS
                                                         0x0A= Internal Storage
                                                         0x0B = DMS (Digital Media Server)
                                                         0x0C = HDMI2
                                                         0x0D = HDMI3
                                                         0x0E = USB Playlist
                                                         0x0F = USB AutoPlay
                                                         0x10= Media Player
                                                         0x11= PDF Player
                                                         0x12= Custom
                                                         0x13 = HDMI 4
                                                         0x14 =VGA2
                                                         0x15 = VGA3
                                                         0x16 = IWB
DATA[13]   HDMI / Component /                            13th priority:
           Composite / Display Port /                    0x00 = HDMI
           DVI-D / VGA / OPS / USB /                     0x01 = Component
           Browser / SmartCMS /                          0x02 = Composite
           Internal Storage / DMS / HDMI                 0x03 = Display Port
           2/ HDMI 3 / USB Playlist / USB                0x04 = DVI-D
           AutoPlay / Media Player / PDF                 0x05 = VGA
           player / Custom/HMDI 4/                       0x06 = OPS
           VGA2 / VGA3 / IWB                             0x07 = USB
                                                         0x08 = Browser
                                                         0x09 = SmartCMS
                                                         0x0A= Internal Storage
                                                         0x0B = DMS (Digital Media Server)
                                                         0x0C = HDMI2
                                                         0x0D = HDMI3
                                                         0x0E = USB Playlist
                                                         0x0F = USB AutoPlay
                                                         0x10= Media Player
                                                         0x11= PDF Player
                                                         0x12= Custom
                                                         0x13 = HDMI 4
                                                         0x14 =VGA2
                                                         0x15 = VGA3
                                                         0x16 = IWB





DATA[14]   HDMI / Component /                            14th priority:
           Composite / Display Port /                    0x00 = HDMI
           DVI-D / VGA / OPS / USB /                     0x01 = Component
           Browser / SmartCMS /                          0x02 = Composite
           Internal Storage / DMS / HDMI                 0x03 = Display Port
           2/ HDMI 3 / USB Playlist / USB                0x04 = DVI-D
           AutoPlay / Media Player / PDF                 0x05 = VGA
           player / Custom/HMDI 4/                       0x06 = OPS
           VGA2 / VGA3 / IWB                             0x07 = USB
                                                         0x08 = Browser
                                                         0x09 = SmartCMS
                                                         0x0A= Internal Storage
                                                         0x0B = DMS (Digital Media Server)
                                                         0x0C = HDMI2
                                                         0x0D = HDMI3
                                                         0x0E = USB Playlist
                                                         0x0F = USB AutoPlay
                                                         0x10= Media Player
                                                         0x11= PDF Player
                                                         0x12= Custom
                                                         0x13 = HDMI 4
                                                         0x14 =VGA2
                                                         0x15 = VGA3
                                                         0x16 = IWB
DATA[15]   HDMI / Component /                            14th priority:
           Composite / Display Port /                    0x00 = HDMI
           DVI-D / VGA / OPS / USB /                     0x01 = Component
           Browser / SmartCMS /                          0x02 = Composite
           Internal Storage / DMS / HDMI                 0x03 = Display Port
           2/ HDMI 3 / USB Playlist / USB                0x04 = DVI-D
           AutoPlay / Media Player / PDF                 0x05 = VGA
           player / Custom/HMDI 4/                       0x06 = OPS
           VGA2 / VGA3 / IWB                             0x07 = USB
                                                         0x08 = Browser
                                                         0x09 = SmartCMS
                                                         0x0A= Internal Storage
                                                         0x0B = DMS (Digital Media Server)
                                                         0x0C = HDMI2
                                                         0x0D = HDMI3
                                                         0x0E = USB Playlist
                                                         0x0F = USB AutoPlay
                                                         0x10= Media Player
                                                         0x11= PDF Player
                                                         0x12= Custom
                                                         0x13 = HDMI 4
                                                         0x14 =VGA2
                                                         0x15 = VGA3
                                                         0x16 = IWB





 DATA[16]        HDMI / Component /                                14th priority:
                 Composite / Display Port /                        0x00 = HDMI
                 DVI-D / VGA / OPS / USB /                         0x01 = Component
                 Browser / SmartCMS /                              0x02 = Composite
                 Internal Storage / DMS / HDMI                     0x03 = Display Port
                 2/ HDMI 3 / USB Playlist / USB                    0x04 = DVI-D
                 AutoPlay / Media Player / PDF                     0x05 = VGA
                 player / Custom/HMDI 4/                           0x06 = OPS
                 VGA2 / VGA3 / IWB                                 0x07 = USB
                                                                   0x08 = Browser
                                                                   0x09 = SmartCMS
                                                                   0x0A= Internal Storage
                                                                   0x0B = DMS (Digital Media Server)
                                                                   0x0C = HDMI2
                                                                   0x0D = HDMI3
                                                                   0x0E = USB Playlist
                                                                   0x0F = USB AutoPlay
                                                                   0x10= Media Player
                                                                   0x11= PDF Player
                                                                   0x12= Custom
                                                                   0x13 = HDMI 4
                                                                   0x14 =VGA2
                                                                   0x15 = VGA3
                                                                   0x16 = IWB
 DATA[17]        HDMI / Component /                                14th priority:
                 Composite / Display Port /                        0x00 = HDMI
                 DVI-D / VGA / OPS / USB /                         0x01 = Component
                 Browser / SmartCMS /                              0x02 = Composite
                 Internal Storage / DMS / HDMI                     0x03 = Display Port
                 2/ HDMI 3 / USB Playlist / USB                    0x04 = DVI-D
                 AutoPlay / Media Player / PDF                     0x05 = VGA
                 player / Custom/HMDI 4/                           0x06 = OPS
                 VGA2 / VGA3 / IWB                                 0x07 = USB
                                                                   0x08 = Browser
                                                                   0x09 = SmartCMS
                                                                   0x0A= Internal Storage
                                                                   0x0B = DMS (Digital Media Server)
                                                                   0x0C = HDMI2
                                                                   0x0D = HDMI3
                                                                   0x0E = USB Playlist
                                                                   0x0F = USB AutoPlay
                                                                   0x10= Media Player
                                                                   0x11= PDF Player
                                                                   0x12= Custom
                                                                   0x13 = HDMI 4
                                                                   0x14 =VGA2
                                                                   0x15 = VGA3
                                                                   0x16 = IWB




Example: Current Display settings: Sources priority = HDMI – Component – Composite – Display Port – DVI-D –
VGA – OPS – USB – Browser – SmartCMS – Internal Storage – DMS – HDMI 2 – HDMI3 (Display address 01)

 MsgSize       Contro     Group       Data (0)        Data (1)      Data (2)     Data (3)   Data (4)   Data (5)
               l
 0x0D          0x01       0x00        0xA6            0x00          0x01         0x02       0x03       0x04

Data (6)    Data   Data (8)      Data (9)        Data (10)       Data (11)      Data (12)   Data (13)
            (7)
0x05        0x06   0x07          0x08            0x09            0x0A           0x0B          0x0C
Data (14)   Data   Data          Data (17)       Checksum
            (15)   (16)
  0x0D





```

##### 4.5.6 Message-Set

```text

Bytes       Bytes Description                    Bits      Description
DATA[0]     0xA5 = Failover – Set                          Command to change the Failover setting of the
                                                           display
DATA[1]     HDMI / Component /                             1st priority:
            Composite / Display Port /                     0x00 = HDMI
            DVI-D / VGA / OPS / USB /                      0x01 = Component
            Browser / SmartCMS /                           0x02 = Composite
            Internal Storage / DMS / HDMI                  0x03 = Display Port
            2/ HDMI 3 / USB Playlist / USB                 0x04 = DVI-D
            AutoPlay / Media Player / PDF                  0x05 = VGA
            player / Custom/ HDMI 4 /                      0x06 = OPS
            VGA2 / VGA3 / IWB /                            0x07 = USB
                                                           0x08 = Browser
                                                           0x09 = SmartCMS
                                                           0x0A= Internal Storage
                                                           0x0B = DMS (Digital Media Server)
                                                           0x0C = HDMI2
                                                           0x0D = HDMI3
                                                           0x0E = USB Playlist
                                                           0x0F = USB AutoPlay
                                                           0x10= Media Player
                                                           0x11= PDF Player
                                                           0x12= Custom
                                                           0x13 = HDMI 4
                                                           0x14 =VGA2
                                                           0x15 = VGA3
                                                           0x16 = IWB
DATA[2]     HDMI / Component /                             2nd priority:
            Composite / Display Port /                     0x00 = HDMI
            DVI-D / VGA / OPS / USB /                      0x01 = Component
            Browser / SmartCMS /                           0x02 = Composite
            Internal Storage / DMS / HDMI                  0x03 = Display Port
            2/ HDMI 3 / USB Playlist / USB                 0x04 = DVI-D
            AutoPlay / Media Player / PDF                  0x05 = VGA
            player / Custom/ HDMI 4 /                      0x06 = OPS
            VGA2 / VGA3 / IWB /                            0x07 = USB
                                                           0x08 = Browser
                                                           0x09 = SmartCMS
                                                           0x0A= Internal Storage
                                                           0x0B = DMS (Digital Media Server)
                                                           0x0C = HDMI2
                                                           0x0D = HDMI3
                                                           0x0E = USB Playlist
                                                           0x0F = USB AutoPlay
                                                           0x13 = HDMI 4
                                                           0x14 =VGA2
                                                           0x15 = VGA3
                                                           0x16 = IWB





DATA[3]   HDMI / Component /                             3rd priority:
          Composite / Display Port /                     0x00 = HDMI
          DVI-D / VGA / OPS / USB /                      0x01 = Component
          Browser / SmartCMS /                           0x02 = Composite
          Internal Storage / DMS / HDMI                  0x03 = Display Port
          2/ HDMI 3 / USB Playlist / USB                 0x04 = DVI-D
          AutoPlay / Media Player / PDF                  0x05 = VGA
          player / Custom/ HDMI 4 /                      0x06 = OPS
          VGA2 / VGA3 / IWB /                            0x07 = USB
                                                         0x08 = Browser
                                                         0x09 = SmartCMS
                                                         0x0A= Internal Storage
                                                         0x0B = DMS (Digital Media Server)
                                                         0x0C = HDMI2
                                                         0x0D = HDMI3
                                                         0x0E = USB Playlist
                                                         0x0F = USB AutoPlay
                                                         0x13 = HDMI 4
                                                         0x14 =VGA2
                                                         0x15 = VGA3
                                                         0x16 = IWB
DATA[4]   HDMI / Component /                             4th priority:
          Composite / Display Port /                     0x00 = HDMI
          DVI-D / VGA / OPS / USB /                      0x01 = Component
          Browser / SmartCMS /                           0x02 = Composite
          Internal Storage / DMS / HDMI                  0x03 = Display Port
          2/ HDMI 3 / USB Playlist / USB                 0x04 = DVI-D
          AutoPlay / Media Player / PDF                  0x05 = VGA
          player / Custom/ HDMI 4 /                      0x06 = OPS
          VGA2 / VGA3 / IWB /                            0x07 = USB
                                                         0x08 = Browser
                                                         0x09 = SmartCMS
                                                         0x0A= Internal Storage
                                                         0x0B = DMS (Digital Media Server)
                                                         0x0C = HDMI2
                                                         0x0D = HDMI3
                                                         0x0E = USB Playlist
                                                         0x0F = USB AutoPlay
                                                         0x13 = HDMI 4
                                                         0x14 =VGA2
                                                         0x15 = VGA3
                                                         0x16 = IWB
DATA[5]   HDMI / Component /                             5th priority:
          Composite / Display Port /                     0x00 = HDMI
          DVI-D / VGA / OPS / USB /                      0x01 = Component
          Browser / SmartCMS /                           0x02 = Composite
          Internal Storage / DMS / HDMI                  0x03 = Display Port
          2/ HDMI 3 / USB Playlist / USB                 0x04 = DVI-D
          AutoPlay / Media Player / PDF                  0x05 = VGA
          player / Custom/ HDMI 4 /                      0x06 = OPS
          VGA2 / VGA3 / IWB /                            0x07 = USB
                                                         0x08 = Browser
                                                         0x09 = SmartCMS
                                                         0x0A= Internal Storage
                                                         0x0B = DMS (Digital Media Server)
                                                         0x0C = HDMI2
                                                         0x0D = HDMI3
                                                         0x0E = USB Playlist
                                                         0x0F = USB AutoPlay

                                                         0x13 = HDMI 4
                                                         0x14 =VGA2
                                                         0x15 = VGA3
                                                         0x16 = IWB




DATA[6]   HDMI / Component /                             6th priority:
          Composite / Display Port /                     0x00 = HDMI
          DVI-D / VGA / OPS / USB /                      0x01 = Component
          Browser / SmartCMS /                           0x02 = Composite
          Internal Storage / DMS / HDMI                  0x03 = Display Port
          2/ HDMI 3 / USB Playlist / USB                 0x04 = DVI-D
          AutoPlay / Media Player / PDF                  0x05 = VGA
          player / Custom/ HDMI 4 /                      0x06 = OPS
          VGA2 / VGA3 / IWB /                            0x07 = USB
                                                         0x08 = Browser
                                                         0x09 = SmartCMS
                                                         0x0A= Internal Storage
                                                         0x0B = DMS (Digital Media Server)
                                                         0x0C = HDMI2
                                                         0x0D = HDMI3
                                                         0x0E = USB Playlist
                                                         0x0F = USB AutoPlay
                                                         0x13 = HDMI 4
                                                         0x14 =VGA2
                                                         0x15 = VGA3
                                                         0x16 = IWB
DATA[7]   HDMI / Component /                             7th priority:
          Composite / Display Port /                     0x00 = HDMI
          DVI-D / VGA / OPS / USB /                      0x01 = Component
          Browser / SmartCMS /                           0x02 = Composite
          Internal Storage / DMS / HDMI                  0x03 = Display Port
          2/ HDMI 3 / USB Playlist / USB                 0x04 = DVI-D
          AutoPlay / Media Player / PDF                  0x05 = VGA
          player / Custom/ HDMI 4 /                      0x06 = OPS
          VGA2 / VGA3 / IWB /                            0x07 = USB
                                                         0x08 = Browser
                                                         0x09 = SmartCMS
                                                         0x0A= Internal Storage
                                                         0x0B = DMS (Digital Media Server)
                                                         0x0C = HDMI2
                                                         0x0D = HDMI3
                                                         0x0E = USB Playlist
                                                         0x0F = USB AutoPlay
                                                         0x13 = HDMI 4
                                                         0x14 =VGA2

                                                         0x15 = VGA3
                                                         0x16 = IWB




DATA[8]   HDMI / Component /                             8th priority:
          Composite / Display Port /                     0x00 = HDMI
          DVI-D / VGA / OPS / USB /                      0x01 = Component
          Browser / SmartCMS /                           0x02 = Composite
          Internal Storage / DMS / HDMI                  0x03 = Display Port
          2/ HDMI 3 / USB Playlist / USB                 0x04 = DVI-D
          AutoPlay / Media Player / PDF                  0x05 = VGA
          player / Custom/ HDMI 4 /                      0x06 = OPS
          VGA2 / VGA3 / IWB /                            0x07 = USB
                                                         0x08 = Browser
                                                         0x09 = SmartCMS
                                                         0x0A= Internal Storage
                                                         0x0B = DMS (Digital Media Server)
                                                         0x0C = HDMI2
                                                         0x0D = HDMI3
                                                         0x0E = USB Playlist
                                                         0x0F = USB AutoPlay
                                                         0x13 = HDMI 4
                                                         0x14 =VGA2
                                                         0x15 = VGA3
                                                         0x16 = IWB





DATA[9]    HDMI / Component /                             8th priority:
           Composite / Display Port /                     0x00 = HDMI
           DVI-D / VGA / OPS / USB /                      0x01 = Component
           Browser / SmartCMS /                           0x02 = Composite
           Internal Storage / DMS / HDMI                  0x03 = Display Port
           2/ HDMI 3 / USB Playlist / USB                 0x04 = DVI-D
           AutoPlay / Media Player / PDF                  0x05 = VGA
           player / Custom/ HDMI 4 /                      0x06 = OPS
           VGA2 / VGA3 / IWB /                            0x07 = USB
                                                          0x08 = Browser
                                                          0x09 = SmartCMS
                                                          0x0A= Internal Storage
                                                          0x0B = DMS (Digital Media Server)
                                                          0x0C = HDMI2
                                                          0x0D = HDMI3
                                                          0x0E = USB Playlist
                                                          0x0F = USB AutoPlay
                                                          0x13 = HDMI 4
                                                          0x14 =VGA2
                                                          0x15 = VGA3
                                                          0x16 = IWB
DATA[10]   HDMI / Component /                             8th priority:
           Composite / Display Port /                     0x00 = HDMI
           DVI-D / VGA / OPS / USB /                      0x01 = Component
           Browser / SmartCMS /                           0x02 = Composite
           Internal Storage / DMS / HDMI                  0x03 = Display Port
           2/ HDMI 3 / USB Playlist / USB                 0x04 = DVI-D
           AutoPlay / Media Player / PDF                  0x05 = VGA
           player / Custom/ HDMI 4 /                      0x06 = OPS
           VGA2 / VGA3 / IWB /                            0x07 = USB
                                                          0x08 = Browser
                                                          0x09 = SmartCMS
                                                          0x0A= Internal Storage
                                                          0x0B = DMS (Digital Media Server)
                                                          0x0C = HDMI2
                                                          0x0D = HDMI3
                                                          0x0E = USB Playlist
                                                          0x0F = USB AutoPlay
                                                          0x13 = HDMI 4
                                                          0x14 =VGA2
                                                          0x15 = VGA3
                                                          0x16 = IWB
DATA[11]   HDMI / Component /                             8th priority:
           Composite / Display Port /                     0x00 = HDMI
           DVI-D / VGA / OPS / USB /                      0x01 = Component
           Browser / SmartCMS /                           0x02 = Composite
           Internal Storage / DMS / HDMI                  0x03 = Display Port
           2/ HDMI 3 / USB Playlist / USB                 0x04 = DVI-D
           AutoPlay / Media Player / PDF                  0x05 = VGA
           player / Custom/ HDMI 4 /                      0x06 = OPS
           VGA2 / VGA3 / IWB /                            0x07 = USB
                                                          0x08 = Browser
                                                          0x09 = SmartCMS
                                                          0x0A= Internal Storage
                                                          0x0B = DMS (Digital Media Server)
                                                          0x0C = HDMI2
                                                          0x0D = HDMI3
                                                          0x0E = USB Playlist
                                                          0x0F = USB AutoPlay
                                                          0x13 = HDMI 4
                                                          0x14 =VGA2
                                                          0x15 = VGA3
                                                          0x16 = IWB

DATA[12]   HDMI / Component /                             8th priority:
           Composite / Display Port /                     0x00 = HDMI
           DVI-D / VGA / OPS / USB /                      0x01 = Component
           Browser / SmartCMS /                           0x02 = Composite
           Internal Storage / DMS / HDMI                  0x03 = Display Port
           2/ HDMI 3 / USB Playlist / USB                 0x04 = DVI-D
           AutoPlay / Media Player / PDF                  0x05 = VGA
           player / Custom/ HDMI 4 /                      0x06 = OPS
           VGA2 / VGA3 / IWB /                            0x07 = USB
                                                          0x08 = Browser
                                                          0x09 = SmartCMS
                                                          0x0A= Internal Storage
                                                          0x0B = DMS (Digital Media Server)
                                                          0x0C = HDMI2
                                                          0x0D = HDMI3
                                                          0x0E = USB Playlist
                                                          0x0F = USB AutoPlay
                                                          0x13 = HDMI 4
                                                          0x14 =VGA2
                                                          0x15 = VGA3
                                                          0x16 = IWB
DATA[13]   HDMI / Component /                             13th priority:
           Composite / Display Port /                     0x00 = HDMI
           DVI-D / VGA / OPS / USB /                      0x01 = Component
           Browser / SmartCMS /                           0x02 = Composite
           Internal Storage / DMS / HDMI                  0x03 = Display Port
           2/ HDMI 3 / USB Playlist / USB                 0x04 = DVI-D
           AutoPlay / Media Player / PDF                  0x05 = VGA
           player / Custom/ HDMI 4 /                      0x06 = OPS
           VGA2 / VGA3 / IWB /                            0x07 = USB
                                                          0x08 = Browser
                                                          0x09 = SmartCMS
                                                          0x0A= Internal Storage
                                                          0x0B = DMS (Digital Media Server)
                                                          0x0C = HDMI2
                                                          0x0D = HDMI3
                                                          0x0E = USB Playlist
                                                          0x0F = USB AutoPlay
                                                          0x13 = HDMI 4
                                                          0x14 =VGA2
                                                          0x15 = VGA3
                                                          0x16 = IWB
DATA[14]   HDMI / Component /                             14th priority:
           Composite / Display Port /                     0x00 = HDMI
           DVI-D / VGA / OPS / USB /                      0x01 = Component
           Browser / SmartCMS /                           0x02 = Composite
           Internal Storage / DMS / HDMI                  0x03 = Display Port
           2/ HDMI 3 / USB Playlist / USB                 0x04 = DVI-D
           AutoPlay / Media Player / PDF                  0x05 = VGA
           player / Custom/ HDMI 4 /                      0x06 = OPS
           VGA2 / VGA3 / IWB /                            0x07 = USB
                                                          0x08 = Browser
                                                          0x09 = SmartCMS
                                                          0x0A= Internal Storage
                                                          0x0B = DMS (Digital Media Server)
                                                          0x0C = HDMI2
                                                          0x0D = HDMI3
                                                          0x0E = USB Playlist
                                                          0x0F = USB AutoPlay
                                                          0x13 = HDMI 4
                                                          0x14 =VGA2

                                                                     0x15 = VGA3
                                                                     0x16 = IWB




Example: Set the Display to the fallowing: Sources priority = HDMI – Component – Composite – Display Port – DVI-
D – VGA – OPS – USB – Browser – SmartCMS – Internal Storage – DMS – HDMI2 – HDMI3 (Display address 01)

 MsgSize      Control       Group      Data (0)        Data (1)      Data (2)   Data (3)   Data (4)   Data (5)
 0x0D         0x01          0x00       0xA5            0x00          0x01       0x02       0x03       0x04
 Data (6)     Data (7)      Data       Data (9)        Data (10)      Data (11)    Data (12)    Data (13)
                            (8)
 0x05         0x06          0x07       0x08            0x09            0x0A           0x0B          0x0C
 Data         Checksum
 (14)
 0x0D             A8





```
