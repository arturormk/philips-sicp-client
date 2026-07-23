# Off Timer

Source: `docs/Philips_SICP_Commands.md`, lines 5275-5351.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 7.24.1 Message-Get Off Timer
- 7.24.2 Message-Report Off Timer
- 7.24.3 Message-Set Off Timer

## DATA[0] Codes

- `0x91` - Off Timer– Get                                Command requests the display to report its current
- `0x91` - Off Timer – Report                             Command reports Off Timer Setting
- `0x92` - Off Timer – Set                             Command to change the Off Timer setting of the

## Source Excerpt
#### 7.24 Off Timer

```text


                  The command is used to set/get the Off Timer value.

                  The command is only available on Dragon 1.0 and Dragon 1.5 platform from firmware version: x.xxx
                  (tbc) onwards.

```

##### 7.24.1 Message-Get Off Timer

```text


     Bytes         Bytes Description                        Bits       Description
     DATA[0]      0x91 = Off Timer– Get                                Command requests the display to report its current
                                                                       Off timer value

    Example: (Display address 01)
     MsgSize Control Group                Data (0)      Checksum
     0x05        0x01        0x00         0x91          0x95


```

##### 7.24.2 Message-Report Off Timer

```text

     Bytes          Bytes Description                           Bits      Description
     DATA[0]        0x91 = Off Timer – Report                             Command reports Off Timer Setting
     DATA[1]         Off /Hours                                           0x00 = Off
                                                                          0x01 = 1 Hour
                                                                          0x02 = 2 Hours
                                                                          0x03 = 3 Hours
                                                                          0x04 = 4 Hours
                                                                          …
                                                                          0x18 = 24 Hours
8


        Example: Current Display settings: Off and 3 hours (Display address 01)
     MsgSize Control Group               Data (0)     Data (1)     Checksum
     0x06     0x01         0x00          0x91         0x00         0x96
     0x06     0x01         0x00          0x91         0x03         0x95



```

##### 7.24.3 Message-Set Off Timer

```text

     Bytes          Bytes Description                       Bits       Description
     DATA[0]        0x92 = Off Timer – Set                             Command to change the Off Timer setting of the
                                                                       display
     DATA[1]        Off /Hours                                         0x00 = Off
                                                                       0x01 = 1 Hour
                                                                       0x02 = 2 Hours
                                                                       0x03 = 3 Hours
                                                                       0x04 = 4 Hours
                                                                       …
                                                                       0x18 = 24 Hours


    Example: Set the Display to the fallowing: Pixel Sensor off and 5 hours (Display address 01)
     MsgSize Control Group                 Data (0)      Data (1)    Checksum
     0x06        0x01        0x00          0x92          0x00        0x95
     0x06        0x01        0x00          0x92          0x05        0x90


```
