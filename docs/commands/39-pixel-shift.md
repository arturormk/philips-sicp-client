# Pixel Shift

Source: `docs/Philips_SICP_Commands.md`, lines 5200-5274.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 7.23.1 Message-Get Pixel Shift
- 7.23.2 Message-Report Pixel Shift
- 7.23.3 Message-Set Pixel Shift

## DATA[0] Codes

- `0xB1` - Pixel Shift – Get                           Command requests the display to report its current
- `0xB1` - Pixel Shift – Report                           Command reports Pixel Shift Setting
- `0xB2` - Pixel Sensor – Set                          Command to change the Pixel shift setting of the

## Source Excerpt
#### 7.23 Pixel Shift

```text
                  The command is used to set/get the pixel shift value.

                  The command is only available on Dragon 1.0 and Dragon 1.5 platform from firmware version: x.xxx
                  (tbc) onwards.

```

##### 7.23.1 Message-Get Pixel Shift

```text

     Bytes          Bytes Description                       Bits       Description
     DATA[0]        0xB1 = Pixel Shift – Get                           Command requests the display to report its current
                                                                       Pixel shift value

    Example: (Display address 01)
     MsgSize Control Group                Data (0)      Checksum
     0x05        0x01        0x00         0xB1          0xB5


```

##### 7.23.2 Message-Report Pixel Shift

```text

     Bytes          Bytes Description                           Bits      Description
     DATA[0]        0xB1 = Pixel Shift – Report                           Command reports Pixel Shift Setting
     DATA[1]         Off /secs                                            0x00 = Off
                                                                          0x01 = 10 secs
                                                                          0x02 = 20 secs
                                                                          0x03 = 30 secs
                                                                          0x04 = 40 secs
                                                                          …
                                                                          0x5A = 900 secs
                                                                          0x5B = AUTO
8


        Example: Current Display settings: Off and xx secs (Display address 01)
     MsgSize Control Group               Data (0)     Data (1)     Checksum
     0x06     0x01         0x00          0xB1         0x00         0xB6
     0x06     0x01         0x00          0xB1         0x03         0xB5



```

##### 7.23.3 Message-Set Pixel Shift

```text

     Bytes          Bytes Description                       Bits       Description
     DATA[0]        0xB2 = Pixel Sensor – Set                          Command to change the Pixel shift setting of the
                                                                       display
     DATA[1]        Off /mins                                          0x00 = Off
                                                                       0x01 = 10 secs
                                                                       0x02 = 20 secs
                                                                       0x03 = 30 secs
                                                                       0x04 = 40 secs
                                                                       …
                                                                       0x5A = 900 secs
                                                                       0x5B = AUTO

    Example: Set the Display to the fallowing: Pixel Sensor off and 50 secs (Display address 01)
     MsgSize Control Group                 Data (0)      Data (1)    Checksum
     0x06        0x01        0x00          0xB2          0x00        0xB5
     0x06        0x01        0x00          0xB2          0x05        0xB0


```
