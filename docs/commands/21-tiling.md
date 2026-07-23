# Tiling

Source: `docs/Philips_SICP_Commands.md`, lines 3762-3936.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 7.6.1 Message-Get
- 7.6.2 Message-Report
- 7.6.3 Message-Set

## DATA[0] Codes

- `0x23` - Tiling – Get                                 Command requests the display to report Tiling
- `0x23` - Tiling – Report                                 Command reports Tiling Setting
- `0x22` - Tiling – Set                                   Command reports Tiling Setting

## Source Excerpt
#### 7.6 Tiling

```text

The command is used to set/get the tiling status as it is defined as below. Tiling is basically splitting video
content to appear in more than one display. Video wall, is an example.


```

##### 7.6.1 Message-Get

```text

 Bytes          Bytes Description                      Bits         Description
 DATA[0]        0x23 = Tiling – Get                                 Command requests the display to report Tiling
                                                                    status.

Example: (Display address 01)
 MsgSize Control Group                Data (0)     Checksum
 0x05        0x01        0x00         0x23         0x27


```

##### 7.6.2 Message-Report

```text

 Bytes          Bytes Description                            Bits      Description
 DATA[0]        0x23 = Tiling – Report                                 Command reports Tiling Setting
 DATA[1]        Enable                                                 0x00 = No
                                                                       0x01 = Yes
 DATA[2]        Frame comp.                                            0x00 = No
                                                                       0x01 = Yes
 DATA[3]        Position                                               0x01 = position 1
                                                                       0x02 = position 2
                                                                       …
                                                                       See Note 1
 DATA[4]        V Monitors, H Monitors                                 0x00 = don’t care
                                                                       0x01 = V Monitors =1, H Monitors =1
                                                                       0x02 = V Monitors =1, H Monitors =2
                                                                       …
                                                                       See Note 2

Note 1:
(1) For Zero Bezel models, the maximum Position value is 150 (hexadecimal value is 0x96).
(2) For other models, the maximum Position value is 25 (hexadecimal value is 0x19).
(3) The Position is counted from left to right, then up to down in the Tiling Wall.
Example: See Figure 3 for the hexadecimal Position value in a 4x3 (H Monitors x V Monitors) Tiling Wall.
Example: See Figure 4 for the hexadecimal Position value in a 5x5 (H Monitors x V Monitors) Tiling Wall.
Example: See Figure 5 for the hexadecimal Position value in a 15x10 (H Monitors x V Monitors) Tiling Wall.

Note 2:
     (20) For Zero Bezel models, the maximum H Monitors are 15 and the maximum V Monitors are 10. The
          formulas for DATA [4], V Monitors, and H Monitors are as follows:
      H Monitors = MOD (Data [4], 15)         (Data [4] ÷ 15, take the remainder)
      V Monitors = INT (Data [4], 15) + 1      (Data [4] ÷ 15, take the quotient and plus one)
      Data [4] = (V Monitors – 1) x 15 + H Monitors
Example: If H Monitors = 12 and V Monitors = 6, the Data [4] value will be (6–1) x 15 + 12 = 87
(2) For other models, the maximum H Monitors and V Monitors are 5, and the formulas for DATA [4], V
Monitors, and H Monitors are as follows:
      H Monitors = MOD (Data [4], 5)        (Data [4] ÷ 5, take the remainder)
     V Monitors = INT (Data [4], 5) + 1      (Data [4] ÷ 5, take the quotient and plus one)





    Data [4] = (V Monitors – 1) x 5 + H Monitors
Example: If H Monitors = 4 and V Monitors = 3, the Data [4] value will be (3–1) x 5 + 4 = 14.



Example for BDL4675XU, Display address 01,
Set the display as follows:
Tiling enabled: Yes
Frame comp.: No
Position: 2
H Monitors: 3
V monitors: 2
Data [4] value will be: (2–1) x 15 + 3 = 18 (hex value: 0x12)
 MsgSize Control Group               Data[0]    Data (1) Data (2)            Data (3)   Data (4)   Checksum
 0x09         0x01          0x00     0x23       0x01        0x00             0x02       0x12       0x3A

Example for BDL4230E, Display address 01
Set the display as follows:
Tiling enabled: Yes
Frame comp.: No
Position: 2
H Monitors: 3
V monitors: 2
Data [4] value will be: (2–1) x 5 + 3 = 8
 MsgSize       Control Group          Data[0]    Data (1)     Data (2)       Data (3)   Data (4)   Checksum
 0x09          0x01         0x00      0x23       0x01         0x00           0x02       0x08       0x20

Figure 3. The hexadecimal Position value in a 4x3 (H Monitors x V Monitors) Tiling Wall.




Figure 4. The hexadecimal Position value in a 5x5 (H Monitors x V Monitors) Tiling Wall.




Figure 5. The hexadecimal Position value in a 15x10 (H Monitors x V Monitors) Tiling Wall.





```

##### 7.6.3 Message-Set

```text

 Bytes        Bytes Description                          Bits       Description
 DATA[0]      0x22 = Tiling – Set                                   Command reports Tiling Setting
 DATA[1]      Enable                                                0x00 = No
                                                                    0x01 = Yes
 DATA[2]      Frame comp.                                           0x00 = No
                                                                    0x01 = Yes
                                                                    0x02 = don’t overwrite (keep previous value)
 DATA[3]      Position                                              0x00 = don’t overwrite (keep previous value)
                                                                    0x01 = position 1
                                                                    0x02 = position 2
                                                                    …
                                                                    See Note 1 at 8.6.2
 DATA[4]      V Monitors, H Monitors                                0x00 = don’t overwrite (keep previous value)
                                                                    0x01 = V Monitors =1, H Monitors =1
                                                                    0x02 = V Monitors =1, H Monitors =2
                                                                    …
                                                                    See Note 2 at 8.6.2

Example for BDL4675XU, Display address: 01
Set the display as follows:
Tiling enabled: Yes
Frame comp.: No
Position: 2
H Monitors: 3
V monitors: 2

Data [4] value will be (2–1) x 15 + 3 = 18 (hex value: 0x12)
 MsgSize     Control Group           Data[0]    Data (1) Data (2)           Data (3)     Data (4)     Checksum
 0x09        0x01        0x00        0x22       0x01        0x00            0x02         0x12         0x3B

Example for BDL4675XU, Display address 01
Set the display as follows:
Tiling enabled: Yes
Frame comp., Position, H Monitors, V Monitors: Keep as before
 MsgSize Control Group               Data[0]      Data (1) Data (2)         Data (3)     Data (4)      Checksum
 0x09         0x01          0x00     0x22         0x01        0x02          0x00         0x00          0x29

Example for BDL4230E, Display address 01
Set the display as follows:
Tiling enabled: Yes
Frame comp.: No
Position: 2
H Monitors: 3
V monitors: 2
 MsgSize       Control Group       Data[0]      Data (1)        Data (2)    Data (3)     Data (4)     Checksum
 0x09          0x01         0x00   0x22         0x01            0x00        0x02         0x08         0x21

 Example for BDL4230E, Display address 01
 Set the display as follows:
 Tiling enabled: Yes
 Frame comp., Position, H Monitors, V Monitors: Keep as before
  MsgSize Control Group               Data[0]      Data (1) Data (2)                Data (3)         Data (4)         Checksum
  0x09         0x01          0x00     0x22         0x01        0x02                 0x00             0x00             0x29


```
