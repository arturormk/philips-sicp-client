# Human Sensor

Source: `docs/Philips_SICP_Commands.md`, lines 4110-4192.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 7.9.1 Human Sensor Message-Get
- 7.9.2 Human Sensor Message-Report
- 7.9.3 Human Sensor Message-Set

## DATA[0] Codes

- `0xB3` - Human Sensor – Get                          Command requests the display to report its current
- `0xB3` - Human Sensor – Report                          Command reports Human Sensor Setting
- `0xB4` - Human Sensor – Set                          Command to change the Human Sensor setting of the

## Source Excerpt
#### 7.9 Human Sensor

```text
              The command is used to set/get the external human sensor (CRD41) status as it is defined as below.

              The command is available on Dragon 1.x platform from firmware version: x.xxx (tbc) onwards

              Himalaya 2.0 and Dragon 1.6 platform from production start.




```

##### 7.9.1 Human Sensor Message-Get

```text


 Bytes          Bytes Description                       Bits       Description
 DATA[0]        0xB3 = Human Sensor – Get                          Command requests the display to report its current
                                                                   Human sensor time status

Example: (Display address 01)
 MsgSize Control Group                 Data (0)     Checksum
 0x05        0x01        0x00          0xB3         0xB7




```

##### 7.9.2 Human Sensor Message-Report

```text


 Bytes          Bytes Description                           Bits      Description
 DATA[0]        0xB3 = Human Sensor – Report                          Command reports Human Sensor Setting
 DATA[1]         Off /mins                                            0x00 = Off
                                                                      0x01 = 10 mins
                                                                      0x02 = 20 mins
                                                                      0x03 = 30 mins
                                                                      0x04 = 40 mins
                                                                      0x05 = 50 mins
                                                                      0x06 = 60 mins
                                                                      0xFF = HW unavailable in this model

Example: Current Display settings: Off and 30 mins (Display address 01)
 MsgSize Control Group                 Data (0)    Data (1)    Checksum
 0x06       0x01         0x00          0xB3        0x00        0xB4
 0x06       0x01         0x00          0xB3        0x03        0xB7


```

##### 7.9.3 Human Sensor Message-Set

```text


 Bytes          Bytes Description                       Bits       Description


 DATA[0]        0xB4 = Human Sensor – Set                          Command to change the Human Sensor setting of the
                                                                   display
 DATA[1]        Off /mins                                          0x00 = Off
                                                                   0x01 = 10 mins
                                                                   0x02 = 20 mins
                                                                   0x03 = 30 mins
                                                                   0x04 = 40 mins
                                                                   0x05 = 50 mins
                                                                   0x06 = 60 mins


Example: Set the Display to the fallowing: Human Sensor off and 50 mins (Display address 01)
 MsgSize Control Group                 Data (0)   Data (1)    Checksum
 0x06        0x01        0x00          0xB4       0x00        0xB3
 0x06        0x01        0x00          0xB4       0x05        0xB6


```
