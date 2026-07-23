# Model Number, Firmware Version, Build Date

Source: `docs/Philips_SICP_Commands.md`, lines 529-585.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 3.3 Message-Get (Model Number, FW Version, Build date)
- 3.4 Message-Report (Model Number, FW Version, Build date)

## DATA[0] Codes

- `0xA1` - Get Model                       Request the Model Number and FW version of the device
- `0xA1` - Report –                        Request the Model number, FW version, FW build date

## Source Excerpt
#### 3.3 Message-Get (Model Number, FW Version, Build date)

```text

  Bytes         Bytes Description             Bits     Description
  DATA[0]       0xA1 = Get Model                       Request the Model Number and FW version of the device
                Number & FW
                version of device with
                Date
  DATA[1]       Codes to request                     0x00 = Model Number
                                                     0x01 = FW version
                                                     0x02 = Build Date
                                                     0x03 = Android FW version (build number)*
(*) 0x03 android FW version is supported on below platform:
         QL3.0 > (android: FB03.01)
         Dragon 1.0 > (android: FB10.07 Scalar not implement yet)
         Dragon 1.5 > (android: FB06.03 Scalar not implement yet)
         Himalaya 2 > (android: FB03.10 Scalar: V1.105)
         10BDL3051T > (android: FB03.07)
         24BDL4151T > (android from FB03.04)
         CRD50/51 > (CRD50/CRD51 not implement yet)


```

#### 3.4 Message-Report (Model Number, FW Version, Build date)

```text

  Bytes         Bytes Description             Bits     Description
  DATA[0]       0xA1 = Report –                        Request the Model number, FW version, FW build date
                Model Number & FW
                version of device with
                Date

DATA[1]   Character[0] to                      36 (0x24) characters maximum.
to        Character[N-1]                       No. of characters, N = 1 to 36 (0x24).
DATA[N]                                        The actual size determines the value of the message size





                                                        byte.




```

**4.** MESSAGES – GENERAL

```text


```
