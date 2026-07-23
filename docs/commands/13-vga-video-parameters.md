# VGA video Parameters

Source: `docs/Philips_SICP_Commands.md`, lines 2596-2660.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 5.3.1 Message-Get
- 5.3.2 Message-Report
- 5.3.4 Message-Set

## DATA[0] Codes

- `0x39` - VGA Video                                  Command requests the display to report its VGA
- `0x39` - VGA Video                             Command reports to the host controller the VGA
- `0x38` - VGA Video                              Command to change the VGA current video parameters

## Source Excerpt
#### 5.3 VGA video Parameters

```text
This command is used to control the VGA video parameters.
      Value in(0,10,20,30,40,50,60,70,80,90,100)
```

##### 5.3.1 Message-Get

```text

 Bytes            Bytes Description                       Bits      Description
 DATA[0]          0x39 = VGA Video                                  Command requests the display to report its VGA
                  Parameters – Get                                  current video parameters.

Example: (Display address 01)
 MsgSize Control Group               Data (0)      Checksum
 0x05        0x01        0x00        0x39          0x3D



```

##### 5.3.2 Message-Report

```text

 Bytes           Bytes Description                   Bits     Description
 DATA[0]         0x39 = VGA Video                             Command reports to the host controller the VGA
                 Parameters – Report                          current video parameters of the display.
 DATA[1]         Clock                                        0 to 100 (%) of the user selectable range of the display.
 DATA[2]         Clock Phase                                  0 to 100 (%) of the user selectable range of the display.
 DATA[3]         H. position                                  0 to 100 (%) of the user selectable range of the display.
 DATA[4]         V. Position                                  0 to 100 (%) of the user selectable range of the display.

Example: All VGA video parameters are set to 55 % (0x37) (Display address 01)
 MsgSize Control Group               Data (0)    Data (1)     Data (2)    Data (3)       Data (4)    Checksum
 0x09        0x01       0x00         0x39        0x37         0x37        0x37           0x37        0x31



```

##### 5.3.4 Message-Set

```text

 Bytes           Bytes Description                   Bits      Description
 DATA[0]         0x38 = VGA Video                              Command to change the VGA current video parameters
                 Parameters – Set
 DATA[1]         Clock(Invalid)                                0 to 100 (%) of the user selectable range of the display.
 DATA[2]         Clock Phase(Invalid)                          0 to 100 (%) of the user selectable range of the display.
 DATA[3]         H. position                                   0 to 100 (%) of the user selectable range of the display.
 DATA[4]         V. Position                                   0 to 100 (%) of the user selectable range of the display.

Example: Set all VGA video parameters to 0x37 (55 %) (Display address 01)
 MsgSize Control Group               Data (0)    Data (1)     Data (2)    Data (3)       Data (4)    Checksum
 0x09        0x01        0x00        0x38        0x37         0x37        0x37           0x37        0x30





```
