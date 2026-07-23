# Power state

Source: `docs/Philips_SICP_Commands.md`, lines 586-653.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 4.1.1 Message-Get
- 4.1.2 Message-Report
- 4.1.3 Message-Set

## DATA[0] Codes

- `0x19` - Power state –                      Command requests the display to report its current power
- `0x19` - Power State –                          Command reports Power state
- `0x18` - Power state –                     Command to change the Power state of the display

## Source Excerpt
#### 4.1 Power state

```text

This command is used to set/get the power state as it is defined as below.


```

##### 4.1.1 Message-Get

```text

 Bytes         Bytes Description               Bits      Description
 DATA[0]       0x19 = Power state –                      Command requests the display to report its current power
               Get                                       state

Example: (Display address 01)
 MsgSize Control Group              Data (0)      Checksum
 0x05        0x01        0x00       0x19          0x1D

```

##### 4.1.2 Message-Report

```text

 Bytes         Bytes Description                      Bits   Description
 DATA[0]       0x19 = Power State –                          Command reports Power state
               Report
 DATA[1]       Power State                                   0x01 = Power Off
                                                             0x02 = On

Example: Power State On (Display address 01)
 MsgSize Control Group              Data (0)      Data (1)      Checksum
 0x06       0x01       0x00         0x19          0x02          0x1C

Special Note: 2016 model 10BDL3051T defines DATA[1] meaning as below
0x01 = Power Off (backlight off/CPU clock low)
0x02 = On (means backlight on/CPU clock normal)

```

##### 4.1.3 Message-Set

```text

 Bytes         Bytes Description            Bits        Description
 DATA[0]       0x18 = Power state –                     Command to change the Power state of the display
               Set
 DATA[1]       Power state                              0x01 = Power Off
                                                        0x02 = On

Example: Power State Deep Sleep (Display address 01)
 MsgSize Control Group              Data (0)     Data (1)       Checksum
 0x06       0x01       0x00         0x18         0x01           0x1E


Special Note: 2016 model 10BDL3051T defines DATA[1] meaning as below
0x01 = Power Off (backlight off/CPU clock low)
0x02 = On (means backlight on/CPU clock normal)





```
