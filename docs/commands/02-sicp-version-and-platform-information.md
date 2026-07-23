# SICP version and platform information

Source: `docs/Philips_SICP_Commands.md`, lines 494-528.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 3.1 Message-Get (SICP version, platform information)
- 3.2 Message Report (SICP version, platform information)

## DATA[0] Codes

- `0xA2` - Get Platform                    Request the SICP version
- `0xA2` - Platform and                    Request the internal Hardware (platform ) version.

## Source Excerpt
#### 3.1 Message-Get (SICP version, platform information)

```text

  Bytes         Bytes Description             Bits     Description
  DATA[0]       0xA2 = Get Platform                    Request the SICP version
                and Version Labels
  DATA[1]       Which Label                            0x00 = Get SICP implementation version
                                                       0x01 = Get the platform label
                                                       (Ex: Eagle, Phoenix, Himalaya, Dragon)
                                                       0x02 = Get the platform version
                                                       (Ex: Eagle 1.2, Eagle 1.3, Phoenix 1.0, Himalaya 1.0, Dragon
                                                       1.0, 10BDL3051T 1.0)

 Example: Get SICP version (Display address 01)
  MsgSize      Control Group            Data (0)     Data (1)    Checksum
  0x06         0x01        0x00         0xA2         0x00        0xA5

```

#### 3.2 Message Report (SICP version, platform information)

```text

  Bytes         Bytes Description             Bits     Description
  DATA[0]       0xA2 = Platform and                    Request the internal Hardware (platform ) version.
                Version Label –
                Report
  DATA[1]       Character[0] to                        36 (0x24) characters maximum.
  to            Character[N-1]                         No. of characters, N = 1 to 36 (0x24).
  DATA[N]                                              The actual size determines the value of the message size
                                                       byte.

```
