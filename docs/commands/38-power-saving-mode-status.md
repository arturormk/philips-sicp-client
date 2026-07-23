# Power saving mode status

Source: `docs/Philips_SICP_Commands.md`, lines 5121-5199.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 7.22.1 Message-Get
- 7.22.2 Message-Report
- 7.22.3 Message-Set

## DATA[0] Codes

- `0xD3` - Power Saving mode                         Command requests the display to report its
- `0xD3` - Power Saving Mode                          Command reports the Power Saving Mode
- `0xD2` - Power Saving Mode                        Command to set the Power Saving Mode

## Source Excerpt
#### 7.22 Power saving mode status

```text
The command is used to set/get the Power Saving Mode status as it is defined as below.


```

##### 7.22.1 Message-Get

```text


 Bytes         Bytes Description                    Bits       Description
 DATA[0       0xD3 = Power Saving mode                         Command requests the display to report its
 ]            status – Get                                     current Power Saving Mode status

Example: (Display address 01)
 MsgSize Control Group             Data (0)       Checksum
 0x05      0x01       0x00         0xD3           0xD7


```

##### 7.22.2 Message-Report

```text

Dragon 1.x , 1.6 & Challenger 2.1 platform supports 4 power modes only (0x04 ~ 0x07) are valid

 Bytes         Bytes Description                        Bits     Description
 DATA[0]       0xD3 = Power Saving Mode                          Command reports the Power Saving Mode
               status – Report                                   enabled or disabled
 DATA[1]       Off / On                                          0x00 = RGB Off & Video Off
                                                                 0x01 = RGB Off, Video On
                                                                 0x02 = RGB On, Video Off
                                                                 0x03 = RGB On & Video On
                                                                 0x04 = mode 1
                                                                 0x05 = mode 2
                                                                 0x06 = mode 3
                                                                 0x07 = mode 4


Example: Current Display Power Saving Mode setting: RGB & Video off (Display address 01)
 MsgSize Control Group          Data (0) Data (1) Checksum
 0x06      0x01       0x00      0xD3      0x00        0xD4


```

##### 7.22.3 Message-Set

```text

Dragon 1.x , 1.6 & Challenger 2.1 platform supports 4 power modes only (0x04 ~ 0x07) are valid



 Bytes         Bytes Description                    Bits       Description
 DATA[0]       0xD2 = Power Saving Mode                        Command to set the Power Saving Mode
               status – Set                                    enabled or disabled
 DATA[1]       Off / On                                        0x00 = RGB Off & Video Off
                                                               0x01 = RGB Off, Video On
                                                               0x02 = RGB On, Video Off
                                                               0x03 = RGB On & Video On
                                                               0x04 = mode 1
                                                               0x05 = mode 2
                                                               0x06 = mode 3
                                                               0x07 = mode 4


Example: Set the Display to the fallowing: Power Saving Mode RGB & Video Off (Display address 01)
 MsgSize Control Group            Data (0) Data (1) Checksum

     0x06         0x01          0x00       0xD2           0x00           0xD5


```
