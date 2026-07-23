# Light Sensor

Source: `docs/Philips_SICP_Commands.md`, lines 4049-4109.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 7.8.1 Message-Get
- 7.8.2 Message-Report
- 7.8.3 Message-Set

## DATA[0] Codes

- `0x25` - Light Sensor – Get                              Command requests the display to report its current
- `0x25` - Light Sensor – Report                              Command reports Light Sensor Setting
- `0x24` - Light Sensor – Set                          Command to change the Light Sensor setting of the

## Source Excerpt
#### 7.8 Light Sensor

```text
The command is used to set/get the light sensor status as it is defined as below.


```

##### 7.8.1 Message-Get

```text


 Bytes         Bytes Description                           Bits       Description
 DATA[0]       0x25 = Light Sensor – Get                              Command requests the display to report its current
                                                                      light sensor status

Example: (Display address 01)
 MsgSize Control Group                   Data (0)      Checksum
 0x05        0x01        0x00            0x25          0x21


```

##### 7.8.2 Message-Report

```text


 Bytes         Bytes Description                               Bits      Description
 DATA[0]       0x25 = Light Sensor – Report                              Command reports Light Sensor Setting
 DATA[1]       On / Off                                                  0x00 = Off
                                                                         0x01 = On
                                                                         0xFF = HW unavailable in this model

Example: Current Display settings: Off and On (Display address 01)
 MsgSize Control Group                 Data (0)    Data (1)     Checksum
 0x06       0x01         0x00          0x25        0x00         0x22
 0x06       0x01         0x00          0x25        0x01         0x23


```

##### 7.8.3 Message-Set

```text


 Bytes         Bytes Description                           Bits       Description

 DATA[0]        0x24 = Light Sensor – Set                          Command to change the Light Sensor setting of the
                                                                   display
 DATA[1]        On / Off                                           0x00 = Off
                                                                   0x01 = On

Example: Set the Display to the fallowing: Light Sensor off (Display address 01)
 MsgSize Control Group                 Data (0)      Data (1)      Checksum
 0x06        0x01        0x00          0x24          0x00          0x23

```
