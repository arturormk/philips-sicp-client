# Lock Functions for IR-Remote Control & Keypad

Source: `docs/Philips_SICP_Commands.md`, lines 654-787.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 4.2.1 Message-Get (IR-Remote Control)
- 4.2.2 Message-Report (IR-Remote Control)
- 4.2.3 Message-Set (IR –Remote Control)
- 4.2.3 Message-Get (Keypad)
- 4.2.4 Message-Report (Keypad)
- 4.2.5 Message-Set (Keypad)

## DATA[0] Codes

- `0x1D` - Get – Lock Status – IR –                          Get unlock all /lock all /lock all but
- `0x1D` - Report – Lock Status – IR                        Report unlock all /lock all /lock all but
- `0x1C` - Set – Lock State – IR –                        Set unlock all/lock all /lock all but
- `0x1B` - Get – Keypad Lock                                   Get unlock all /lock all/lock all but
- `0x1B` - Report – Keypad Status                              Report unlock all /lock all/lock all but
- `0x1A` - Set – Keypad Lock Status                            Set unlock all/lock all /lock all but

## Source Excerpt
#### 4.2 Lock Functions for IR-Remote Control & Keypad

```text

The following commands separately are used to lock/unlock the Remote Control and Keypad.


```

##### 4.2.1 Message-Get (IR-Remote Control)

```text

 Bytes             Bytes Description                         Bits           Description
 DATA[0]           0x1D = Get – Lock Status – IR –                          Get unlock all /lock all /lock all but
                   Remote Control                                           power/lock all but volume/
                                                                            Primary/Secondary status

Example: (Display address 01)
 MsgSize Control Group              Data (0)     Checksum
 0x05        0x01        0x00       0x1D         0x19


```

##### 4.2.2 Message-Report (IR-Remote Control)

```text

 Bytes             Bytes Description                           Bits        Description
 DATA[0]           0x1D = Report – Lock Status – IR                        Report unlock all /lock all /lock all but
                   – Remote Control                                        power/lock all but volume/
                                                                           Primary/Secondary status
 DATA[1]           Status indicator byte for Remote                         0x01 = Unlock all
                   Control                                                  0x02 = Lock all
                                                                            0x03 = Lock all but Power
                                                                            0x04 = Lock all but Volume
                                                                            0x05 = Primary (Master)
                                                                            0x06 = Secondary (Daisy chain PD)
                                                                            0x07 = Lock all except Power & Volume

Example: Unlock all on IR Remote Control on (Display address 01)
 MsgSize Control Group              Data (0)      Data (1)    Checksum
 0x06       0x01         0x00       0x1D          0x01        0x1B


```

##### 4.2.3 Message-Set (IR –Remote Control)

```text

 Bytes             Bytes Description                       Bits          Description
 DATA[0]           0x1C = Set – Lock State – IR –                        Set unlock all/lock all /lock all but
                   Remote Control                                        power/lock all but volume/
                                                                         Primary/Secondary status
 DATA[1]           Status indicator byte for Remote                      0x01 = Unlock all
                   Control                                               0x02 = Lock all
                                                                         0x03 = Lock all but Power
                                                                         0x04 = Lock all but Volume
                                                                         0x05 = Primary (Master)
                                                                         0x06 = Secondary (Daisy chain PD)
                                                                         0x07 = Lock all except Power & Volume

Example: IR Remote Control – lock all but power (Display address 01)
 MsgSize Control Group                Data (0)    Data (1)     Checksum
 0x06        0x01      0x00           0x1C        0x03         0x18





```

##### 4.2.3 Message-Get (Keypad)

```text

 Bytes              Bytes Description                           Bits           Description
 DATA[0]            0x1B = Get – Keypad Lock                                   Get unlock all /lock all/lock all but
                    Status                                                     power/ lock all but Volume

Example: (Display address 01)
 MsgSize Control Group                Data (0)      Checksum
 0x05        0x01        0x00         0x1B          0x1F


```

##### 4.2.4 Message-Report (Keypad)

```text

 Bytes              Bytes Description                             Bits         Description
 DATA[0]            0x1B = Report – Keypad Status                              Report unlock all /lock all/lock all but
                                                                               power/ lock all but Volume
 DATA[1]            Status indicator byte for Keypad                           0x01 = Unlock all
                                                                               0x02 = Lock all
                                                                               0x03 = Lock all but Power*
                                                                               0x04 = Lock all but Volume*
                                                                               0x07 = Lock all except Power & Volume*
(*) not valid for 10BDL3151T & 24BDL2451T

Example: Reporting status of Keypad indicating Lock all for (Display address 01)
 MsgSize Control Group                Data (0)     Data (1)      Checksum
 0x06       0x01         0x00         0x1B         0x02          0x1E


```

##### 4.2.5 Message-Set (Keypad)

```text

 Bytes              Bytes Description                             Bits         Description
 DATA[0]            0x1A = Set – Keypad Lock Status                            Set unlock all/lock all /lock all but
                                                                               power/ lock all but Volume
 DATA[1]            Status indicator byte for Keypad                           0x01 = Unlock all
                                                                               0x02 = Lock all
                                                                               0x03 = Lock all but Power*
                                                                               0x04 = Lock all but Volume*
                                                                               0x07 = Lock all except Power & Volume*
(*) not valid for 10BDL3151T & 24BDL2451T

Example: Set Lock all on Keypad for (Display address 01)
 MsgSize Control Group                Data (0)    Data (1)       Checksum
 0x06        0x01        0x00         0x1A        0x02           0x1F





```
