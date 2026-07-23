# Power state at Cold Start

Source: `docs/Philips_SICP_Commands.md`, lines 788-860.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 4.3.1 Message-Get
- 4.3.2 Message-Report
- 4.3.3 Message-Set

## DATA[0] Codes

- `0xA4` - Power at Cold Start –                               Get Power state at Cold Start state
- `0xA4` - Power at Cold Start –                              Report from Power state at Cold Start
- `0xA3` - Power at Cold Start – Set                           Set Power state at Cold Start

## Source Excerpt
#### 4.3 Power state at Cold Start

```text

Command is used to set the cold start power state, the cold start power state are updated and stored by this
command. In the OSD setting of the monitor it is called “switch on state”.

```

##### 4.3.1 Message-Get

```text

 Bytes              Bytes Description                           Bits           Description
 DATA[0]            0xA4 = Power at Cold Start –                               Get Power state at Cold Start state
                    Get

Example: (Display address 01)
 MsgSize Control Group                Data (0)      Checksum
 0x05        0x01        0x00         0xA4          0xA0


```

##### 4.3.2 Message-Report

```text

 Bytes              Bytes Description                             Bits        Description
 DATA[0]            0xA4 = Power at Cold Start –                              Report from Power state at Cold Start
                    Report                                                    state
 DATA[1]            Power at Cold Start                                       0x00 = Power Off
                                                                              0x01 = Forced On
                                                                              0x02 = Last Status

Example: Current Power state at Cold Start state: Last Status (Display address 01)
 MsgSize Control Group               Data (0)       Data (1)     Checksum
 0x06       0x01        0x00         0xA4           0x02         0xA1

```

##### 4.3.3 Message-Set

```text


 Bytes              Bytes Description                            Bits          Description
 DATA[0]            0xA3 = Power at Cold Start – Set                           Set Power state at Cold Start
 DATA[1]            Power at Cold Start                                        0x00 = Power Off
                                                                               0x01 = Forced On
                                                                               0x02 = Last Status

The value is stored and it is applied only when the display starts up from cold start power state the next time:
Power Off:
The monitor will automatically switched Off (even if the last status was on) whenever the mains power is
turned on or resumed after the power interruption.
Forced On:
The monitor will be automatically switched to ON mode whenever the mains power is turned on or resumed
after the power interruption.
Last Status:
The monitor will be automatically switched to the last status (either Power Off or On) whenever the mains
power is turned on or resumed after the power interruption.

Example: Set Power state at cold start to last status (Display address 01)
 MsgSize      Control Group              Data (0)      Data (1)     Checksum
 0x06         0x01        0x00           0xA3          0x02         0xA6





```
