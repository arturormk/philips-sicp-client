# APM status (advanced power management)

Source: `docs/Philips_SICP_Commands.md`, lines 5035-5120.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 7.21.1 Message-Get
- 7.21.2 Message-Report
- 7.21.3 Message-Set

## DATA[0] Codes

- `0xD1` - APM status – Get                           Command requests the display to report its
- `0xD1` - APM status – Report                           Command reports the APM enabled or
- `0xD0` - APM status – Set                          Command to set the APM enabled or disabled

## Source Excerpt
#### 7.21 APM status (advanced power management)

```text
 The command is used to set/get the APM status as it is defined as below.

 Supported on Himalaya & eagle 1.3 platform .


```

##### 7.21.1 Message-Get

```text


  Bytes        Bytes Description                      Bits       Description
  DATA[0       0xD1 = APM status – Get                           Command requests the display to report its
  ]                                                              current APM status

 Example: (Display address 01)
  MsgSize Control Group              Data          Checksum
                                     (0)
  0x05        0x01       0x00        0xD1          0xD5


```

##### 7.21.2 Message-Report

```text


  Bytes        Bytes Description                          Bits      Description
  DATA[0]      0xD1 = APM status – Report                           Command reports the APM enabled or
                                                                    disabled
  DATA[1]                                                           0x00 = Off
                                                                    0x01 = On
                                                                    0x02 = Mode 1 (TCP off / WOL on)
                                                                    0x03 = Mode 2 (TCP on / WOL off)



Note: Himalaya platform only support off/Mode1/Mode2.
Eagle 1.3 platform only support on/off.



 Example: Current Display APM setting: Off (Display address 01)
  MsgSize Control Group         Data        Data       Checksum
                                (0)         (1)
  0x06      0x01       0x00     0xD1        0x00       0xD6


```

##### 7.21.3 Message-Set

```text


  Bytes         Bytes Description                     Bits       Description
  DATA[0]       0xD0 = APM status – Set                          Command to set the APM enabled or disabled

  DATA[1]                                                        0x00 = Off
                                                                 0x01 = On
                                                                 0x02 = Mode 1 (TCP off / WOL on)
                                                                 0x03 = Mode 2 (TCP on / WOL off)

Note: Note: Himalaya platform only support off/Mode1/Mode2.
Eagle 1.3 platform only support on/off.





Example: Set the Display to the fallowing: APM off (Display address 01)
 MsgSize Control Group            Data       Data       Checksum
                                  (0)        (1)
 0x06      0x01       0x00        0xD0       0x00       0xD7





```
