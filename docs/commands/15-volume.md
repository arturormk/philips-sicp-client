# Volume

Source: `docs/Philips_SICP_Commands.md`, lines 3113-3531.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 6.1.1 Message-Get current volume level speakers and audio out
- 6.1.2 Message-Report current volume level speakers and audio out
- 6.1.3 Message-Set current volume level speakers and audio out
- 6.1.4 Message-Set Volume level – step up or step down for Speaker out or Audio Out
- 6.1.5.1 Message-Set Volume Limit
- 6.1.5.2 Message-Get Volume Limit
- 6.1.6.1 Message-Set Volume Limit – Audio out
- 6.1.6.2 Message-Get Volume Limit – Audio out
- 6.1.7.1 Message-Get
- 6.1.7.2 Message-Report
- 6.1.7.3 Message-Set
- 6.1.8.1 Get volume mute
- 6.1.8.2 Message-Report
- 6.1.8.3 Set volume mute

## DATA[0] Codes

- `0x45` - Volume –                      Command requests the display to report its current Volume
- `0x45` - Volume – Report                    Command reports current Volume level
- `0x44` - Volume – Set
- `0x41` - Volume +/- – Set                   Adjust volume up/down
- `0xB8` - Volume Limits– Set      The 3 values must conform to the rule :
- `0xB6` - Volume Limits–                 The 3 values must conform to the rule :
- `0xB9` - Volume Limits– Set      The 3 values must conform to the rule :
- `0xB7` - Volume Limits– Get      The 3 values must conform to the rule :
- `0x43` - Audio Parameters –                           Command requests the display to report its current
- `0x43` - Audio Parameters –                              Command reports Audio Parameters
- `0x42` - Audio Parameters –                           Command to change the Audio Parameters of the
- `0x46` - Volume mute                         Command report current volume mute status
- `0x47` - Volume mute                   Command set current volume mute

## Source Excerpt
#### 6.1 Volume

```text

 This command is used to set/get the volume of speaker out and audio out as it is defined as below.

```

##### 6.1.1 Message-Get current volume level speakers and audio out

```text

  Bytes         Bytes Description          Bits      Description
  DATA[0]       0x45 = Volume –                      Command requests the display to report its current Volume
                Get                                  level

 The interface to set Software must be such that they also modify the variables representing these current
 parameters. To mute the display, set Volume = 0. This command does not overwrite the system mute status of
 the display.

 Example: (Display address 01)
  MsgSize Control Group               Data (0)     Checksum
  0x05        0x01        0x00        0x45         0x41

```

##### 6.1.2 Message-Report current volume level speakers and audio out

```text


 This command can get current volume level for speaker & audio out individually. Valid values range from 0x00
 (lowest 0% volume) through 0x64 (highest – 100% volume).
 Some platforms don’t have variable audio out and the report (Ack) is different, see the special note remark in this
 chapter.



  Bytes         Bytes Description                 Bits    Description
  DATA[0]       0x45 = Volume – Report                    Command reports current Volume level
  DATA[1]       Speaker Out Volume level                  0 to 100 (%) of the user selectable range of the display.
  DATA[2]       Audio Out Volume level                    0 to 100 (%) of the user selectable range of the display.


  DATA[1]       Speaker Out Volume level                  0 to 60 (%) of the user selectable range of the display.
  DATA[2]       Audio Out Volume level                    0 to 60 (%) of the user selectable range of the display.

       Example: Current Display settings: Volume:22% (0x16) for Speak out and 10%(0x0A) for Audio out (Display
       address 01)
       MsgSize Control Group                  Data      Data        Data        Checksum
                                              (0)       (1)         (2)
        0x07       0x01         0x00            0x45    0x16        0x0A          0x5F

SPECIAL NOTE:
       HIMALAYA 1.0 & 1.2 and Eagle (platforms) don’t have variable audio out and data(2) is not received.
       See below example: Data(1) is the speaker out volume level 100% ( 0x64).

       MsgSize     Control     Group       Data          Data                Checksum
                                           (0)           (1)
        0x06       0x01        0x01          0x45        0x64                    0x27


```

##### 6.1.3 Message-Set current volume level speakers and audio out

```text

This command can set volume level for speaker & audio out individually. Valid values range from 0x00 (lowest 0%
volume) through 0x64 (highest – 100% volume). If DATA [1] or [2] are higher than 0x64 no action will be taken in the
display and current volume level will be maintained without any effect.
Some platforms don’t have variable audio out and the command is different, see the special note remark in this chapter.



  Bytes         Bytes Description                 Bits    Description

  DATA[0]         0x44 = Volume – Set
  DATA[1]         Speaker Out Volume level                   0 to 100 (%) of the user selectable range of the display.
  DATA[2]         Audio Out Volume level                     0 to 100 (%) of the user selectable range of the display.



    DATA[1]          Speaker Out Volume level                  0 to 60 (%) of the user selectable range of the display.
    DATA[2]          Audio Out Volume level                    0 to 60 (%) of the user selectable range of the display.

         Example: Set the Display Volume to 22% (0x16) for Speaker out and 50 %(0x32) for Audio out (Display
   address 01)
          MsgSize Control Group               Data       Data        Data        Checksum
                                              (0)        (1)         (2)
            0x07        0x01         0x00       0x44        0x16        0x32       0x66

SPECIAL NOTE:
       Himalaya 1 & 1.2 and Eagle (platforms) don’t have variable audio out and data(2) may not be sent.
       See below example: Data(1) is the speaker out volume level 22% ( 0x16).


            MsgSize Control         Group        Data(0) Data(1) Checksum

              0x06        0x01         0x00        0x44        0x16          0x55



```

##### 6.1.4 Message-Set Volume level – step up or step down for Speaker out or Audio Out

```text

   This command can set volume level in step up or step down a count for speaker & audio out individually.
   DATA [1] or [2] must supply “0x00” to count down a step and supply “0x01” to count up a step of volume.
   All other values supplied to DATA [1] or [2] will get no “response” from the display.
   Some platforms don’t have variable audio out and the command is different, see the special note remark in this
   chapter.


    Bytes            Bytes Description               Bits      Description
    DATA[0]          0x41 = Volume +/- – Set                   Adjust volume up/down
    DATA[1]          Speaker Out.                              0 : down, 1: up, 2: no change*
    DATA[2]          Audio Out.                                0 : down, 1: up, 2: no change*

               * “2 no change” will only work in below platforms:
                    Dragon 1.0 : from firmware phase 3 (after V1.3XX ).
                    Dragon 1.5 : from firmware phase 2 (after V1.2XX).
                    Dragon 1.6: from start production
                    Himalay 2.0 : from start production
                    and new platforms

   Example: Set the Display Volume up (0x01) (Display address 01)
    MsgSize Control Group               Data (0)    Data (1)    Data(2)              Checksum
    0x07        0x01        0x00        0x41        0x01        0x00                 0x46


           SPECIAL NOTE:
           Himalaya 1 & 1.2 and Eagle (platforms)don’t have variable audio out and data(2) may not be sent.
           See below example: Data(1) is the speaker out volume.


            MsgSize Control         Group        Data(0) Data(1) Checksum Volume

              0x06        0x01         0x00        0x41        0x00          0x46          Step -
              0x06        0x01         0x00        0x41        0x01          0x47          Step +

```

##### 6.1.5 Volume Limit – Speaker out

```text

 This command is used to set or get the volume limit (minimum, maximum and switch on volume) for speaker
 out
```

###### 6.1.5.1 Message-Set Volume Limit

```text

  Bytes        Bytes Description          Bits Description
   DATA[0]      0xB8 = Volume Limits– Set      The 3 values must conform to the rule :
                for Speaker out                Min <= Switch On <= Max
    DATA[1]     Minimum Volume                 0 to 100 (%) of the user selectable range of the display.
    DATA[2]     Maximum Volume                 0 to 100 (%) of the user selectable range of the display.
    DATA[3]     Switch On Volume               0 to 100 (%) of the user selectable range of the display.

 Example: Set the Display Speaker out to the following: 10% (0x0A), 77% (0x4D), 50% (0x32) (Display address 01)
   MsgSize       Control Group             Data (0)      Data (1)    Data (2)     Data (3)   Checksum
   0x08          0x01       0x00           0xB8          0x0A        0x4D         0x32       0xC4

```

###### 6.1.5.2 Message-Get Volume Limit

```text

```

**2.** Bytes        Bytes Description                 Bits Description

```text
    DATA[0]            0xB6 = Volume Limits–                 The 3 values must conform to the rule :
                       Get for Speaker out                   Min <= Switch On <= Max
    DATA[1]            Minimum Volume                        0 to 100 (%) of the user selectable range of the
                                                             display.
    DATA[2]            Maximum Volume                        0 to 100 (%) of the user selectable range of the
                                                             display.
    DATA[3]            Switch On Volume                      0 to 100 (%) of the user selectable range of the
                                                             display.





Example: Get the Speaker out values as follows: 10% (0x0A), 77% (0x4D), 50% (0x32) (Display address 01)
  MsgSize      Control Group              Data (0)    Data (1)    Data (2)     Data (3)     Checksum
  0x08         0x01       0x00            0xB6        0x0A        0x4D         0x32         0xB0

```

##### 6.1.6 Volume Limit – Audio out

```text

This command is used to set or get the volume limit (minimum, maximum and switch on volume) for Audio
out

```

###### 6.1.6.1 Message-Set Volume Limit – Audio out

```text

 Bytes          Bytes Description          Bits Description
  DATA[0]        0xB9 = Volume Limits– Set      The 3 values must conform to the rule :
                 for Audio out.                 Min <= Switch On <= Max
  DATA[1]        Minimum Volume                 0 to 100 (%) of the user selectable range of the display.
  DATA[2]        Maximum Volume                 0 to 100 (%) of the user selectable range of the display.
  DATA[3]        Switch On Volume               0 to 100 (%) of the user selectable range of the display.

SPECIAL NOTE:
      Following DATA [1], DATA [2], DATA [3], applicable for Phoenix 2.0 platform only (year 2015
      BDLxx70EL/BDLxx90VL/BDLxx30QL/BDLxx35QL)

 DATA[1]        Minimum Volume                          0 to 60 (%) of the user selectable range of the display.
 DATA[2]        Maximum Volume                          0 to 60 (%) of the user selectable range of the display.
 DATA[3]        Switch On Volume                        0 to 60 (%) of the user selectable range of the display.

Example: Set the Display Audio out to the following: 10% (0x0A), 77% (0x4D), 50% (0x32) (Display address 01)
  MsgSize       Control Group              Data (0)     Data (1)   Data (2)     Data (3)     Checksum
  0x08          0x01       0x00            0xB9         0x0A       0x4D         0x32         0xC5

```

###### 6.1.6.2 Message-Get Volume Limit – Audio out

```text

 Bytes          Bytes Description          Bits Description
  DATA[0]        0xB7 = Volume Limits– Get      The 3 values must conform to the rule :
                 values for Audio out.          Min <= Switch On <= Max
  DATA[1]        Minimum Volume                 0 to 100 (%) of the user selectable range of the display.
  DATA[2]        Maximum Volume                 0 to 100 (%) of the user selectable range of the display.
  DATA[3]        Switch On Volume               0 to 100 (%) of the user selectable range of the display.

SPECIAL NOTE:
      Following DATA [1], DATA [2], DATA [3], applicable for Phoenix 2.0 platform only (year 2015
      BDLxx70EL/BDLxx90VL/BDLxx30QL/BDLxx35QL)

 DATA[1]        Minimum Volume                          0 to 60 (%) of the user selectable range of the display.
 DATA[2]        Maximum Volume                          0 to 60 (%) of the user selectable range of the display.
 DATA[3]        Switch On Volume                        0 to 60 (%) of the user selectable range of the display.

Example: Get the Display Audio out values as follows: 10% (0x0A), 77% (0x4D), 50% (0x32) (Display address 01)
  MsgSize      Control Group              Data (0)      Data (1)   Data (2)     Data (3)    Checksum
  0x08         0x01        0x00           0xB7          0x0A       0x4D         0x32        0xCB

```

##### 6.1.7 Audio Parameters

```text

This command is used to set/get the audio parameters as it is defined as below.

```

###### 6.1.7.1 Message-Get

```text



 Bytes         Bytes Description                       Bits        Description
 DATA[0]       0x43 = Audio Parameters –                           Command requests the display to report its current
               Get                                                 audio parameters

Example: (Display address 01)
 MsgSize      Control Group            Data (0)     Checksum
 0x05         0x01        0x00         0x43         0x47

```

###### 6.1.7.2 Message-Report

```text

 Bytes         Bytes Description                            Bits      Description
 DATA[0]       0x43 = Audio Parameters –                              Command reports Audio Parameters
               Report
 DATA[1]       Treble.                                                0 to 100 (%) of the user selectable range of the
                                                                      display.
 DATA[2]       Bass.                                                  0 to 100 (%) of the user selectable range of the
                                                                      display.


SPECIAL NOTE:
      Following DATA [1], DATA [2] applicable for Phoenix 2.0 platform only (year 2015
      BDLxx70EL/BDLxx90VL/BDLxx30QL/BDLxx35QL)

 DATA[1]       Treble.                                                -8 to 8 are the boundaries of the user selectable
                                                                      range of the display.
 DATA[2]       Bass.                                                  -8 to 8 are the boundaries of the user selectable
                                                                      range of the display.


Example: Current Display settings: Treble: 80% (0x50), Bass: 93% (0x5D) (Display address 01)
 MsgSize      Control Group             Data (0)    Data (1)    Data (2)    Checksum
 0x07         0x01        0x00          0x43        0x50        0x5D        0x48

```

###### 6.1.7.3 Message-Set

```text

 Bytes         Bytes Description                       Bits        Description
 DATA[0]       0x42 = Audio Parameters –                           Command to change the Audio Parameters of the
               Set                                                 display
 DATA[1]       Treble.                                             0 to 100 (%) of the user selectable range of the display.
 DATA[2]       Bass.                                               0 to 100 (%) of the user selectable range of the display.

         SPECIAL NOTE:
         Following DATA [1], DATA [2] applicable for Phoenix 2.0 platform only (year 2015
         BDLxx70EL/BDLxx90VL/BDLxx30QL/BDLxx35QL)

 DATA[1]       Treble.                                                -8 to 8 are the boundaries of the user selectable
                                                                      range of the display.
 DATA[2]       Bass.                                                  -8 to 8 are the boundaries of the user selectable
                                                                      range of the display.

         SPECIAL NOTE: Following table applicable for Phoenix 2.0 platform only (year 2015
         BDLxx70EL/BDLxx90VL/BDLxx30QL/BDLxx35QL)

      The value (-8) ～ (-1)
         -8         -7         -6          -5          -4            -3         -2         -1



             0xF8        0xF9      0xFA        0xFB         0xFC       0xFD        0xFE     0xFF

 The interface to set Software must be such that they modify the variables representing these current
 parameters

 Example: Set the Display to the fallowing: Treble: 77% (0x4D), Bass: 77% (0x4D) (Display address 01)
  MsgSize      Control Group             Data (0)     Data (1)    Data (2)    Checksum
  0x07         0x01         0x00         0x42         0x4D        0x4D        0x44

```

##### 6.1.8 Volume mute

```text

               This command mute the volume of the internal speakers and audio out.
               The command is available from firmware version : TBC x.xx on platforms TBC


```

###### 6.1.8.1 Get volume mute

```text
     Bytes      Bytes Description                  Bits    Description
     DATA[0]    0x46 = Volume mute                         Command report current volume mute status
                – Get

                    Example : get volume mute status
     MsgSize        Control Group         Data (0)   checksum
     0x05           0x01       0x00       0x46       0x42


```

###### 6.1.8.2 Message-Report

```text
     Bytes      Bytes Description                  Bits    Description
     DATA[0]    0x46 = Volume mute                         Command report current volume mute status
                – Get
     DATA[1]                                               0x01 = mute on
                                                           0x00= mute off


                    Example: current volume mute is on
     MsgSize        Control Group          Data (0)    Data (1)       checksum
     0x06           0x01      0x00         0x46        0x01           0x40


```

###### 6.1.8.3 Set volume mute

```text

               The command is available from firmware version : TBC x.xx on platforms TBC


     Bytes            Bytes Description            Bits    Description
     DATA[0]          0x47 = Volume mute                   Command set current volume mute
                      – Set
     DATA[1]                                               0x01 = mute on
                                                           0x00= mute off



                    Example: set volume mute off

     MsgSize        Control     Group      Data (0)       Data (1)    checksum
     0x06           0x01        0x00       0x47           0x00        0x40


```

### 7 MISCELLANEOUS

```text


```
