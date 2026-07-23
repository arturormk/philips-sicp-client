# Philips SICP Commands

**Protocol:** Serial / Ethernet Interface Communication Protocol  
**Specification:** SICP V2.03  
**Vendor document date:** 14 June 2019  
**Purpose:** implementation reference for a Python command-line client

> This is a development-oriented transcription of the supplied Philips/TPV
> protocol specification. The vendor PDF contains inconsistencies, duplicated
> sections, platform-specific exceptions, and occasional typographical errors.
> Preserve raw packet logging and verify every command against the target model
> before treating it as production-safe.

## 1. Recommended CLI architecture

Keep the transport, packet codec, command definitions, and CLI presentation
separate:

```text
philips_sicp/
    __init__.py
    packet.py        # encode, decode, checksum, stream framing
    transport.py     # TCP and RS-232
    response.py      # ACK/NACK/NAV and typed reports
    commands.py      # command metadata and value mappings
    client.py        # high-level operations
    cli.py           # argparse or Typer interface
tests/
    test_packet.py
    test_commands.py
    test_hardware.py
```

The first implementation should expose both:

```text
sicp raw 05 01 00 19 1D
sicp power get
sicp power set on
```

The raw interface is essential for adding and testing commands one at a time.

## 2. Physical transport

### 2.1 RS-232

| Property | Value |
|---|---|
| Baud rates | 1200, 2400, 4800, **9600 default**, 19200, 38400, 57600 |
| Data bits | 8 |
| Parity | None |
| Stop bits | 1 |
| Flow control | None |
| Display DB9 pin 2 | RXD, input to display |
| Display DB9 pin 3 | TXD, output from display |
| Display DB9 pin 5 | GND |

A null-modem/crossover connection is required.

### 2.2 Ethernet

| Property | Value |
|---|---|
| Protocol | TCP |
| Default port | `5000` |
| Suggested initial timeout | `2.0 s` |
| Specification retry threshold | approximately `500 ms` |

TCP is a byte stream. A single `recv()` is not guaranteed to return exactly one
packet. Buffer bytes and use the first byte, `MsgSize`, as the frame length.

## 3. Packet format

With the Group byte present:

```text
MsgSize Control Group Data[0] Data[1] ... Data[N] Checksum
```

| Offset | Name | Meaning |
|---:|---|---|
| 0 | `MsgSize` | Total number of bytes, including checksum |
| 1 | `Control` | Monitor ID |
| 2 | `Group` | Group ID |
| 3 | `Data[0]` | Command code |
| 4... | `Data[1..N]` | Parameters or report data |
| last | `Checksum` | XOR of all preceding bytes |

The specification permits packet sizes from `0x03` through `0x28`.

### 3.1 Addressing

| Monitor ID | Group ID | Meaning |
|---:|---:|---|
| `0x00` | `0x00` | Broadcast; no response expected |
| `0x01..0xFF` | `0x00` | Address one monitor |
| any | `0x01..0xFE` | Address a group |

Some older implementations may omit the Group byte when grouping is disabled.
For a new client, support both layouts in the decoder, but use the modern
Group-byte layout by default.

### 3.2 Checksum

```python
def xor_checksum(values: bytes) -> int:
    result = 0
    for value in values:
        result ^= value
    return result
```

```python
def build_packet(
    command: int,
    *parameters: int,
    monitor_id: int = 1,
    group_id: int = 0,
) -> bytes:
    data = bytes((command, *parameters))
    msg_size = 4 + len(data)
    partial = bytes((msg_size, monitor_id, group_id)) + data
    return partial + bytes((xor_checksum(partial),))
```

### 3.3 Generic responses

A SET command normally receives:

```text
Data[0] = 0x00
Data[1] = status
```

| Status | Meaning |
|---:|---|
| `0x06` | ACK - command executed |
| `0x15` | NACK - malformed, corrupt, or invalid command |
| `0x18` | NAV - unavailable, irrelevant, unsupported, or cannot execute |

A valid GET normally receives the corresponding command-specific report rather
than a generic ACK.

No reply is expected for broadcast addressing, an inactive Monitor ID, or some
group-addressed operations.

## 4. Minimal Python packet model

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class SicpPacket:
    raw: bytes
    size: int
    monitor_id: int
    group_id: int | None
    data: bytes
    checksum: int

    @property
    def command(self) -> int | None:
        return self.data[0] if self.data else None

    @property
    def parameters(self) -> bytes:
        return self.data[1:]


def parse_group_packet(raw: bytes) -> SicpPacket:
    if not raw:
        raise ValueError("empty packet")
    if raw[0] != len(raw):
        raise ValueError(
            f"length byte says {raw[0]}, received {len(raw)} bytes"
        )
    if xor_checksum(raw[:-1]) != raw[-1]:
        raise ValueError("checksum mismatch")
    if len(raw) < 4:
        raise ValueError("packet too short")

    return SicpPacket(
        raw=raw,
        size=raw[0],
        monitor_id=raw[1],
        group_id=raw[2],
        data=raw[3:-1],
        checksum=raw[-1],
    )
```

Do not require the response Group byte to equal the request Group byte. At least
one real display has been observed returning Group `0x01` in a report after a
request using Group `0x00`.

## 5. Command-definition model

A registry keeps the CLI generic while typed wrappers are added gradually:

```python
from dataclasses import dataclass
from enum import Enum


class Operation(str, Enum):
    GET = "get"
    SET = "set"
    ACTION = "action"
    REPORT = "report"


@dataclass(frozen=True)
class CommandDefinition:
    name: str
    code: int
    operation: Operation
    parameter_names: tuple[str, ...] = ()
    notes: str = ""
```

Suggested CLI behavior:

```text
sicp commands
sicp describe power-state
sicp get power-state
sicp set power-state on
sicp raw --hex "05 01 00 19 1D"
sicp listen
```

Always print or optionally log:

- transmitted bytes
- received bytes
- parsed Monitor ID and Group ID
- command code and parameters
- checksum result
- elapsed time
- ACK/NACK/NAV interpretation

## 6. Command index

The following index is derived from the specification's command-summary pages. Some codes are duplicated or used for reports; consult the detailed section.

| Code | Command name from summary | Remarks |
|---:|---|---|
| `0x00` | Communication Control | Generic ACK/NACK/NAV report |
| `0xA2` | Platform and version labels |  |
| `0x19` | Power state Get |  |
| `0x18` | Power state Set |  |
| `0x1B` | Keypad Lock status Get | Changed Functionality |
| `0x1A` | Keypad Lock status Set | Changed Functionality |
| `0x1D` | IR Lock status Get | Changed Functionality |
| `0x1C` | IR Lock status Set | Changed Functionality |
| `0xA4` | Power state at cold start Get |  |
| `0xA3` | Power state at cold start Set |  |
| `0xAC` | Input Source | Change/Add input |
| `0xAD` | Current Source | Change/Add input |
| `0xAF` | Auto Signal Detecting Get | Change/Add input |
| `0xAE` | Auto Signal Detecting Set | Change/Add input |
| `0xA6` | Failover Get | Change/Add input |
| `0xA5` | Failover Set | Change/Add input |
| `0x33` | Video parameters Get | Brightness, etc. |
| `0x32` | Video parameters Set | Add DICOM gamma |
| `0x35` | Color Temperature Get |  |
| `0x34` | Color Temperature Set |  |
| `0x37` | Color Parameters Get |  |
| `0x36` | Color Parameters Set |  |
| `0x39` | VGA Video Parameters Get |  |
| `0x38` | VGA Video Parameters Set |  |
| `0x3B` | Picture Format Get |  |
| `0x3A` | Picture Format Set |  |
| `0x3D` | Picture-in-picture Get |  |
| `0x3C` | Picture-in-picture Set |  |
| `0x85` | PIP source Get | Change/Add input |
| `0x84` | PIP source Set | Change/Add input |
| `0x45` | Volume Get |  |
| `0x44` | Volume Set |  |
| `0x41` | Volume up/down Set |  |
| `0xB8` | Volume limits Speaker out |  |
| `0xB9` | Volume limit Audio out |  |
| `0x43` | Audio parameters Get |  |
| `0x42` | Audio parameters Set |  |
| `0x0F` | Miscellaneous info | Operating hours |
| `0xDE` | Smart power Get | Dimming backlight |
| `0xDD` | Smart power Set | Dimming backlight |
| `0x70` | Auto Adjust | VGA only |
| `0x2F` | Temperature Get |  |
| `0x15` | Serial Code Get |  |
| `0x23` | Tiling Get |  |
| `0x22` | Tiling Set |  |
| `0x25` | Light Sensor Get |  |
| `0x24` | Light Sensor Set |  |
| `0x27` | OSD Rotating Get |  |
| `0x26` | OSD Rotating Set |  |
| `0x29` | MEMC Effect Get | Himalaya 1.0 – no |
| `0x28` | MEMC Effect Set | Himalaya 1.0 – no |
| `0x2D` | Information OSD Features Get |  |
| `0x2C` | Information OSD Features Set |  |
| `0x2B` | Noise Reduction Get |  |
| `0x2A` | Noise Reduction Set |  |
| `0x1F` | Touch Feature Get | Himalaya 1.0 – no |
| `0x1E` | Touch Feature Set | Himalaya 1.0 – no |
| `0x51` | Scan Mode Get |  |
| `0x50` | Scan Mode Set |  |
| `0x53` | Scan Conversion Get | Himalaya 1.0 – no |
| `0x52` | Scan Conversion Set | Himalaya 1.0 – no |
| `0x55` | Switch On Delay Get |  |
| `0x54` | Switch On Delay Set |  |
| `0x56` | Factory Reset Set |  |
| `0x5B` | Scheduling Get | Change/Add input |
| `0x5A` | Scheduling Set | Change/Add input |
| `0x5D` | Group ID Get |  |
| `0x5C` | Group ID Set |  |
| `0x3F` | Power On logo Get |  |
| `0x3E` | Power On logo Set |  |
| `0x62` | Fan Speed status Get |  |
| `0x61` | Fan Speed status Set |  |
| `0xD1` | APM status Get |  |
| `0xD0` | APM status Set |  |
| `0xD3` | Power Save status Get |  |
| `0xD2` | Power Save status Set |  |
| `0x12` | Color Temperature 100K – Get |  |
| `0x11` | Color Temperature 100K – Set |  |
| `0xA1` | Model Number, FW, Build | Help ID the PD info |
| `0xFD` | Custom Multi-Win Get | Himalaya 1.0 |
| `0xFC` | Custom Multi-Win Set | Himalaya 1.0 |
| `0xFB` | Custom Multi-Win Set | Himalaya 1.0 |
| `0xFE` | MIC color calibration | Reserved for Future use |
| `0x85` | PIP source Get |  |
| `0x84` | PIP source Set |  |
| `0x28` | MEMC Effect Set |  |
| `0x1E` | Touch Feature Set |  |
| `0x1B` | User Input Control State Get |  |
| `0x1A` | User Input Control State Set |  |
| `0x2D` | Information OSD Features Get |  |
| `0x51` | Scan Mode Get |  |
| `0x52` | Scan Conversion Set |  |
| `0x55` | Switch On Delay Get |  |
| `0x57` | Reboot monitor |  |
| `0x58` | Send screenshot |  |
| `0x59` | Videosignal present |  |
| `0x5E` | Get Horz frame compensation value |  |
| `0x5F` | Set Horz frame compensation value |  |
| `0x67` | Get Vert frame compensation value |  |
| `0x68` | Set Vert frame compensation value |  |
| `0x69` | Set monitor ID |  |
| `0xA6` | Failover Get |  |
| `0xA5` | Failover Set |  |
| `0xA1` | Model Number, FW Version, Build |  |
| `0xB6` | date Volume Limit Speaker out |  |
| `0xB7` | Volume limit Audio out |  |
| `0x16` | Display orientation get |  |
| `0x17` | Display orientation set |  |
| `0x4A` | custom tiling report/get |  |
| `0x4B` | custom tiling set |  |
| `0xB1` | Pixel Shift Get |  |
| `0xB2` | Pixel Shift Set |  |
| `0xB3` | Human sensor Get |  |
| `0xB4` | Human sensor Set |  |
| `0x91` | Off Timer Get |  |
| `0x92` | Off Timer Set |  |
| `0xF1` | External Storage Lock Set |  |
| `0xF2` | External Storage Lock Get |  |
| `0xF3` | Led Control Set |  |
| `0xF4` | Led Control Get |  |
| `0x63` | ECO mode Get |  |
| `0x64` | ECO mode Set |  |
| `0x65` | Picture style Get |  |
| `0x66` | Picture style Set |  |
| `0x46` | Volume mute Get |  |
| `0x47` | Volume mute Set |  |
| `0x71` | Picture mute get |  |
| `0x72` | Picture mute set |  |

## 7. Detailed command reference

The remainder of this file preserves the detailed definitions, payload schemas,
value tables, examples, platform notes, and warnings from sections 2.3 through
14 of the source document. Tables are kept as preformatted text because the
original PDF uses complex merged cells that do not convert reliably to ordinary
Markdown tables.

Treat each `DATA[n]` entry as a byte-level schema. Add typed wrappers only after
testing the raw exchange on the target display.

### 2.3 MESSAGES – SYSTEM

### 2.4 Communication Control

```text

This defines the feedback command from Philips Professional Display to host controller when it receives the
display command from the host controller, depending on the commands availability, the command reported back
to host controller can be one of the ACK, NACK or NAV.
Note: there is no reply message when the wrong ID address is being used.

```

#### 2.4.1 Message-Report

```text

 Bytes            Bytes Description         Bits       Description
 DATA[0]          0x00 =                               Generic report message after Get or Set message
                  Communication
                  Control – Report
 DATA[1]          Communication                        0x06 = Acknowledge (ACK)
                  Control                              0x15 = Not Acknowledge (NACK)
                                                       0x18 = Not Available (NAV). Command not available, not
                                                       relevant or cannot execute

Example
Send:
 MsgSize Control Group              Data (0)       Data (1)    Checksum        Description
 0x06        0x01        0x00       0x00           0x01        0x06
ACK reply: (Display address 01)
 MsgSize Control Group              Data (0)       Data (1)    Checksum        Description
 0x06        0x01        0x00       0x00           0x06        0x01            Command is well executed.

Example
Send:
 MsgSize Control Group              Data (0)       Data (1)    Checksum        Description
 0x06        0x01        0x00       0x17           0x01        0x11
NACK reply: (Display address 01)
 MsgSize Control Group              Data (0)       Data (1)    Checksum        Description
 0x06        0x01        0x00       0x00           0x15        0x12            Wrong command code-Data (0), the system will
                                                                               reply “NACK”.

Example
Send:
 MsgSize Control Group              Data (0)       Data (1)    Checksum        Description
 0x06        0x01        0x00       0x00           0x01        0x06
NAV reply: (Display address 01)
 MsgSize Control Group              Data (0)       Data (1)    Checksum        Description
 0x06        0x01        0x00       0x00           0x18        0x1F            Checksum error, the system will reply “NAV”.

Example
Send:
 MsgSize Control Group              Data (0)       Data (1)    Checksum        Description
 0x06        0x01        0x00       0x00           0x04        0x03
NAV reply: (Display address 01)
 MsgSize Control Group              Data (0)       Data (1)    Checksum        Description
 0x06        0x01        0x00       0x00           0x18        0x1F            Wrong parameter-Data (1), the system will reply
                                                                               “NAV”.





Example
Send:
 MsgSize     Control     Group        Data (0)     Data (1)     Checksum        Description
 0x06        0x01        0x00         0x00         0x01         0x06

NAV reply: (Display address 01)
 MsgSize Control Group                Data (0)     Data (1)     Checksum        Description
 0x06        0x01        0x00         0x00         0x18         0x1F            Command is correct, while system is already in
                                                                                stand–by mode, so reply “NAV”.

Example
Send:
 MsgSize Control Group                 Data (0)    Data (1)     Checksum        Description
 0x06         0x01        0x00         0x00        0x01         0x06
No reply: (Display address 01- not active ID)
 MsgSize Control Group                 Data (0)    Data (1)     Checksum        Description
 0x06         0x01        0x00         0x00        0x18         0x1F            Command is correct, while system would NOT
                                                                                reply any message due to it’s not active.

Example
Send:
 MsgSize Control Group                Data (0)     Data (1)     Checksum        Description
 0x06         0x01        0x00        0x00         0x01         0x06
No reply: (Display address 00- Broadcast ID)
 MsgSize Control Group                Data (0)     Data (1)     Checksum        Description
 0x06         0x01        0x00        0x00         0x18         0x1F            Command is correct; all systems would NOT reply
                                                                                any message due to “Daisy Chain’s limitation-
                                                                                Collision might occur.





 3        Platform, SICP version, Model Number and FW, SW Version numbers

 This command provides the complete set of Model & Version information


```

### 3.1 Message-Get (SICP version, platform information)

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

### 3.2 Message Report (SICP version, platform information)

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

### 3.3 Message-Get (Model Number, FW Version, Build date)

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

### 3.4 Message-Report (Model Number, FW Version, Build date)

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

### 4.1 Power state

```text

This command is used to set/get the power state as it is defined as below.


```

#### 4.1.1 Message-Get

```text

 Bytes         Bytes Description               Bits      Description
 DATA[0]       0x19 = Power state –                      Command requests the display to report its current power
               Get                                       state

Example: (Display address 01)
 MsgSize Control Group              Data (0)      Checksum
 0x05        0x01        0x00       0x19          0x1D

```

#### 4.1.2 Message-Report

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

#### 4.1.3 Message-Set

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

### 4.2 Lock Functions for IR-Remote Control & Keypad

```text

The following commands separately are used to lock/unlock the Remote Control and Keypad.


```

#### 4.2.1 Message-Get (IR-Remote Control)

```text

 Bytes             Bytes Description                         Bits           Description
 DATA[0]           0x1D = Get – Lock Status – IR –                          Get unlock all /lock all /lock all but
                   Remote Control                                           power/lock all but volume/
                                                                            Primary/Secondary status

Example: (Display address 01)
 MsgSize Control Group              Data (0)     Checksum
 0x05        0x01        0x00       0x1D         0x19


```

#### 4.2.2 Message-Report (IR-Remote Control)

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

#### 4.2.3 Message-Set (IR –Remote Control)

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

#### 4.2.3 Message-Get (Keypad)

```text

 Bytes              Bytes Description                           Bits           Description
 DATA[0]            0x1B = Get – Keypad Lock                                   Get unlock all /lock all/lock all but
                    Status                                                     power/ lock all but Volume

Example: (Display address 01)
 MsgSize Control Group                Data (0)      Checksum
 0x05        0x01        0x00         0x1B          0x1F


```

#### 4.2.4 Message-Report (Keypad)

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

#### 4.2.5 Message-Set (Keypad)

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

### 4.3 Power state at Cold Start

```text

Command is used to set the cold start power state, the cold start power state are updated and stored by this
command. In the OSD setting of the monitor it is called “switch on state”.

```

#### 4.3.1 Message-Get

```text

 Bytes              Bytes Description                           Bits           Description
 DATA[0]            0xA4 = Power at Cold Start –                               Get Power state at Cold Start state
                    Get

Example: (Display address 01)
 MsgSize Control Group                Data (0)      Checksum
 0x05        0x01        0x00         0xA4          0xA0


```

#### 4.3.2 Message-Report

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

#### 4.3.3 Message-Set

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

### 4.4 MESSAGES – INPUT SOURCES

```text


```

#### 4.4.1 Input Source

```text

This command is used to change or to get the current input source.


```

##### 4.4.1.1 Message-Set

```text

DATA[1] : set the current source value as below.

DATA[2]: playlist number for PDF player and Media player source input and URL number for source input browser


 Bytes              Bytes Description                           Bits       Description
 DATA[0]            0xAC = Input Source – Set                              Command requests the display to set the current
                                                                           input source
 DATA[1]            Input Source Type/Number                               0x01 = VIDEO
                                                                           0x02 = S-VIDEO
                                                                           0x03 = COMPONENT
                                                                           0x04 = CVI 2 (not applicable)
                                                                           0x05 = VGA
                                                                           0x06 = HDMI 2
                                                                           0x07 = Display Port 2
                                                                           0x08 = USB 2
                                                                           0x09 = Card DVI-D
                                                                           0x0A = Display Port 1
                                                                           0x0B = Card OPS
                                                                           0x0C = USB 1
                                                                           0x0D = HDMI
                                                                           0x0E = DVI-D
                                                                           0x0F = HDMI3
                                                                           0x10 = BROWSER
                                                                           0x11= SMARTCMS
                                                                           0X12= DMS (Digital Media Server)
                                                                           0x13= INTERNAL STORAGE
                                                                           0x14 = Reserved
                                                                           0x15 = Reserved
                                                                           0x16= Media Player
                                                                           0x17= PDF Player
                                                                           0x18= Custom
                                                                           0x19 = HDMI 4
                                                                           0x1A =VGA2
                                                                           0x1B = VGA3
                                                                           0x1C = IWB





  DATA[2]         Start playlist file number on source              0x01 = playlist file 1 or URL 1
                  input media player or PDF player.                 0x02 = playlist file 2 or URL 2
                  Start URL number on browser                       0x03 = playlist file 3 or URL 3
                  input.                                            0x04 = playlist file 4 or URL 4
                  Only working on: Dragon 1, Dragon                 0x05 = playlist file 5 or URL 5
                 1.5, 10BDL3051T, dragon 1.5,                       0x06 = playlist file 6 or URL 6
                 Himalaya 2 & QL3 (see the
                                                                    0x07 = playlist file 7 or URL 7
                 platform list)
                                                                    0x08 = reserved
                 From firmware version : TBC                        0x09 = reserved
                 The monitor will start to display the              0x0A = reserved
                 playlist or URL number.                            0x0B = reserved
                                                                    0x0C = reserved
                                                                    0x0D = reserved
                                                                    0x0E = reserved
                                                                    0x0F = reserved
                                                                    0x10 = reserved
                                                                    0x11 = reserved
                                                                    0X12 = reserved
                                                                    0X13 = reserved
                                                                    0x14 = reserved
                                                                    0x15 = reserved
                                                                    0x16 = reserved
                                                                    0x17 = reserved
                                                                    0x18 = reserved

  DATA[3]         OSD Style                               Bit7      Reserved
                                                          Bit6      Do not switch.
                                                                    Source is made current. Set is updated with the
                                                                    details of this source; however, source change is
                                                                    performed.
                                                                    1 = Do not switch. 0 = Switch
                                                          Bit2.0    Source info. Display Style
                                                                    0 = Reserved
                                                                    1 = Source label
  DATA[4]         Mute Style                              Bit 7     (Reserved, value is 0)
                                                          Bit 6     (Reserved, value is 0)
                                                          Bit 5     (Reserved, value is 0)
                                                          Bit 4     (Reserved, value is 0)
                                                          Bit 3     (Reserved, value is 0)
                                                          Bit 2     (Reserved, value is 0)
                                                          Bit 1     (Reserved, value is 0)
                                                          Bit 0     (Reserved, value is 0)

 Example: Set on DVI-D with Source label displaying on OSD (Display address 01)
  MsgSize Control Group               Data (0)      Data (1)   Data (2)     Data (3)     Data (4)     Checksum
  0x09        0x01       0x00         0xAC          0x09       0x09         0x01         0x00         0xA5

Source command examples:
HDMI 1 :     09 01 00 AC 0D 09 01 00 A1                Ack: 06 01 01 00 06 00
HDMI 2 :     09 01 00 AC 06 09 01 00 AA                Ack: 06 01 01 00 06 00
HDMI 3 :     09 01 00 AC 0F 09 01 00 A3                Ack: 06 01 01 00 06 00
HDMI 4:      09 01 00 AC 19 09 01 00 B5                Ack: 06 01 01 00 06 00
DVI :        09 01 00 AC 0E 09 01 00 A2                Ack: 06 01 01 00 06 00
AV :         09 01 00 AC 01 09 01 00 AD                Ack: 06 01 01 00 06 00
YPBPR :      09 01 00 AC 03 09 01 00 AF                Ack: 06 01 01 00 06 00
VGA :        09 01 00 AC 05 09 01 00 A9                Ack: 06 01 01 00 06 00
DP :         09 01 00 AC 0A 09 01 00 A6                Ack: 06 01 01 00 06 00
USB :        09 01 00 AC 0C 09 01 00 A0                Ack: 06 01 01 00 06 00

OPS :                09 01 00 AC 0B 09 01 00 A7                  Ack: 06 01 01 00 06 00
BROWSER:             09 01 00 AC 10 09 01 00 BC                  Ack: 06 01 01 00 06 00
SMARTCMS:            09 01 00 AC 11 09 01 00 BD                  Ack: 06 01 01 00 06 00
Media player:        09 01 00 AC 16 09 01 00 BA                  Ack: 06 01 01 00 06 00
PDF player:          09 01 00 AC 17 09 01 00 BB                  Ack: 06 01 01 00 06 00
Custom :             09 01 00 AC 18 09 01 00 B4                  Ack: 06 01 01 00 06 00



```

##### 4.4.1.2 Message-Get

```text

  Bytes              Bytes Description                              Bits       Description
  DATA[0]            0xAD = Current Source – Get                               Command requests the display to report the
                                                                               current input source in use.

 Example: (Display address 01)
  MsgSize Control Group                      Data (0)       Checksum
  0x05        0x01        0x00               0xAD           0xA9

```

##### 4.4.1.3 Message-Report

```text

 DATA[1] will get the current source value as below.
 DATA[2] will get the current selected playlist or URL number if current source is PDF player, Browser, Media player.
 DATA[3], DATA[4] can be ignored by requestor or may not be returned by device depending on model .

  Bytes              Bytes Description                              Bits       Description
  DATA[0]            0xAD = Current Source –                                   Command reports to the host controller the
                     Report                                                    current input source in use by the display.
  DATA[1]            Input Source Type/Number                                  0x01 = VIDEO
                                                                               0x02 = S-VIDEO
                                                                               0x03 = COMPONENT
                                                                               0x04 = CVI 2 (not applicable)
                                                                               0x05 = VGA
                                                                               0x06 = HDMI 2
                                                                               0x07 = Display Port 2
                                                                               0x08 = USB 2
                                                                               0x09 = Card DVI-D
                                                                               0x0A = Display Port 1
                                                                               0x0B= Card OPS
                                                                               0x0C = USB 1
                                                                               0x0D= HDMI
                                                                               0x0E= DVI-D
                                                                               0x0F = HDMI3
                                                                               0x10= BROWSER
                                                                               0x11= SMARTCMS
                                                                               0X12= DMS (Digital Media Server)
                                                                               0x13= INTERNAL STORAGE
                                                                               0x14= Reserved
                                                                               0x15= Reserved
                                                                               0x16= Media Player
                                                                               0x17= PDF Player
                                                                               0x18= Custom
                                                                               0x19 = HDMI 4
                                                                               0x1A =VGA2
                                                                               0x1B = VGA3
                                                                               0x1C = IWB





DATA[2]    Get the selected playlist file number             0x00 = no playlist or URL
           on source input media player or                   0x01 = playlist file 1 or URL 1
           PDF player.                                       0x02 = playlist file 2 or URL 2
           Get the selected URL number on                    0x03 = playlist file 3 or URL 3
           browser input.                                    0x04 = playlist file 4 or URL 4
                                                             0x05 = playlist file 5 or URL 5
           Only working on: Dragon 1, Dragon                 0x06 = playlist file 6 or URL 6
          1.5, 10BDL3051T, dragon 1.5,
                                                             0x07 = playlist file 7 or URL 7
          Himalaya 2 & QL3 (see the
          platform list)                                     0x08 = reserved
                                                             0x09 = reserved
           From firmware version : TBC                       0x0A = reserved
                                                             0x0B = reserved
                                                             0x0C = reserved
                                                             0x0D = reserved
                                                             0x0E = reserved
                                                             0x0F = reserved
                                                             0x10 = reserved
                                                             0x11 = reserved
                                                             0X12 = reserved
                                                             0X13 = reserved
                                                             0x14 = reserved
                                                             0x15 = reserved
                                                             0x16 = reserved
                                                             0x17 = reserved
                                                             0x18 = reserved





                                                                   0x17= PDF Player
                                                                   0x18= Custom
 DATA[3]        OSD Style                               Bit7       Reserved
                                                        Bit6       Reserved
                                                        Bit2.0     Source info. Display Style
                                                                   0 = Reserved
                                                                   1 = Source label
 DATA[4]        Mute Style                              Bit 7      (Reserved, value is 0)
                                                        Bit 6      (Reserved, value is 0)
                                                        Bit 5      (Reserved, value is 0)
                                                        Bit 4      (Reserved, value is 0)
                                                        Bit 3      (Reserved, value is 0)
                                                        Bit 2      (Reserved, value is 0)
                                                        Bit 1      (Reserved, value is 0)
                                                        Bit 0      (Reserved, value is 0)

Example: Current Input Source: VIDEO (Display address 01)

 MsgSize    Control    Group       Data (0)   Data          Data       Data         Data        Checksum
                                              (1)           (2)        (3)          (4)
 0x09       0x01       0x00        0xAD       0xFD          0x01       0x00         0x00        0x59





```

### 4.5 Auto Signal Detecting / Failover

```text



Failover means, if current input source has no signal system will switch to another based on settings as defined by commands below.
The specification file explains the usage/behaviour.

```

#### 4.5.1 Message-Get

```text

 Bytes            Bytes Description                             Bits       Description
 DATA[0]          0xAF = Auto Signal                                       Command requests the display to report its current
                  Detecting – Get                                          Auto Signal Detecting status

Example: (Display address 01)
 MsgSize Control Group                      Data (0)       Checksum
 0x05        0x01        0x00               0xAF           0xAB

```

#### 4.5.2 Message-Report

```text

 Bytes            Bytes Description                                 Bits      Description
 DATA[0]          0xAF = Auto Signal Detecting –                              Command reports Auto Signal Detecting Setting
                  Report
 DATA[1]          On / All / PC sources only /                                0x00 = Off
                  Video sources only / Failover                               0x01 = All
                                                                              0x02 = Reserved
                                                                              0x03 = PC sources only
                                                                              0x04 = Video sources only
                                                                              0x05 = Failover

Special Note:

Dragon 1.0 (see platform ) excludes DATA [1] values below
0x03 = PC sources only 0x04 = Video sources only

Example: Current Display settings: Off and All (Display address 01)
 MsgSize Control Group                 Data (0)     Data (1)     Checksum
 0x06       0x01         0x00          0xAF         0x00         0xA8
 0x06       0x01         0x00          0xAF         0x01         0xA9

```

#### 4.5.3 Message-Set

```text

 Bytes            Bytes Description                             Bits       Description
 DATA[0]          0xAE = Auto Signal                                       Command to change the Auto Signal Detecting
                  Detecting – Set                                          setting of the display
 DATA[1]          On / All /PC sources only /                              0x00 = Off
                  Video sources only / Failover                            0x01 = All
                                                                           0x02 = Reserved
                                                                           0x03 = PC sources only
                                                                           0x04 = Video sources only
                                                                           0x05 = Failover





Special Note:

2016 Dragon 1.0 (see platform ) excludes DATA [1] values below
0x03 = PC sources only 0x04 = Video sources only

Example: Set the Display to the fallowing: Auto Signal Detecting Off (Display address 01)
 MsgSize Control Group                 Data (0)     Data (1)     Checksum
 0x06        0x01        0x00          0xAE         0x00         0xA9

```

#### 4.5.4 Message-Get

```text

 Bytes           Bytes Description                      Bits     Description
 DATA[0]         0xA6 = Failover – Get                           Command requests the display to report its
                                                                 current Failover status

Example: (Display address 01)
 MsgSize Control Group                Data (0)      Checksum
 0x05        0x01        0x00         0xA6


```

#### 4.5.5 Message-Report

```text

 Bytes            Bytes Description                         Bits     Description
 DATA[0]          0xA6 = Failover – Report                           Command reports Failover Setting
 DATA[1]          HDMI / Component /                                 1st priority:
                  Composite / Display Port /                         0x00 = HDMI
                  DVI-D / VGA / OPS / USB /                          0x01 = Component
                  Browser / SmartCMS /                               0x02 = Composite
                  Internal Storage / DMS / HDMI                      0x03 = Display Port
                  2/ HDMI 3 / USB Playlist / USB                     0x04 = DVI-D
                  AutoPlay / Media Player / PDF                      0x05 = VGA
                  player / Custom/HMDI 4/                            0x06 = OPS
                  VGA2 / VGA3 / IWB                                  0x07 = USB
                                                                     0x08 = Browser
                                                                     0x09 = SmartCMS
                                                                     0x0A= Internal Storage
                                                                     0x0B = DMS (Digital Media Server)
                                                                     0x0C = HDMI2
                                                                     0x0D = HDMI3
                                                                     0x0E = USB Playlist
                                                                     0x0F = USB AutoPlay
                                                                     0x10= Media Player
                                                                     0x11= PDF Player
                                                                     0x12= Custom
                                                                     0x13= HDMI 4
                                                                     0x14 =VGA2
                                                                     0x15 = VGA3
                                                                     0x16 = IWB





DATA[2]   HDMI / Component /                            2nd priority:
          Composite / Display Port /                    0x00 = HDMI
          DVI-D / VGA / OPS / USB /                     0x01 = Component
          Browser / SmartCMS /                          0x02 = Composite
          Internal Storage / DMS / HDMI                 0x03 = Display Port
          2/ HDMI 3 / USB Playlist / USB                0x04 = DVI-D
          AutoPlay / Media Player / PDF                 0x05 = VGA
          player / Custom/HMDI 4/                       0x06 = OPS
          VGA2 / VGA3 / IWB                             0x07 = USB
                                                        0x08 = Browser
                                                        0x09 = SmartCMS
                                                        0x0A= Internal Storage
                                                        0x0B = DMS (Digital Media Server)
                                                        0x0C = HDMI2
                                                        0x0D = HDMI3
                                                        0x0E = USB Playlist
                                                        0x0F = USB AutoPlay
                                                        0x10= Media Player
                                                        0x11= PDF Player
                                                        0x12= Custom
                                                        0x13 = HDMI 4
                                                        0x14 =VGA2
                                                        0x15 = VGA3
                                                        0x16 = IWB
DATA[3]   HDMI / Component /                            3rd priority:
          Composite / Display Port /                    0x00 = HDMI
          DVI-D / VGA / OPS / USB /                     0x01 = Component
          Browser / SmartCMS /                          0x02 = Composite
          Internal Storage / DMS / HDMI                 0x03 = Display Port
          2/ HDMI 3 / USB Playlist / USB                0x04 = DVI-D
          AutoPlay / Media Player / PDF                 0x05 = VGA
          player / Custom/HMDI 4/                       0x06 = OPS
          VGA2 / VGA3 / IWB                             0x07 = USB
                                                        0x08 = Browser
                                                        0x09 = SmartCMS
                                                        0x0A= Internal Storage
                                                        0x0B = DMS (Digital Media Server)
                                                        0x0C = HDMI2
                                                        0x0D = HDMI3
                                                        0x0E = USB Playlist
                                                        0x0F = USB AutoPlay
                                                        0x10= Media Player
                                                        0x11= PDF Player
                                                        0x12= Custom
                                                        0x13 = HDMI 4
                                                        0x14 =VGA2
                                                        0x15 = VGA3
                                                        0x16 = IWB





DATA[4]   HDMI / Component /                            4th priority:
          Composite / Display Port /                    0x00 = HDMI
          DVI-D / VGA / OPS / USB /                     0x01 = Component
          Browser / SmartCMS /                          0x02 = Composite
          Internal Storage / DMS / HDMI                 0x03 = Display Port
          2/ HDMI 3 / USB Playlist / USB                0x04 = DVI-D
          AutoPlay / Media Player / PDF                 0x05 = VGA
          player / Custom/HMDI 4/                       0x06 = OPS
          VGA2 / VGA3 / IWB                             0x07 = USB
                                                        0x08 = Browser
                                                        0x09 = SmartCMS
                                                        0x0A= Internal Storage
                                                        0x0B = DMS (Digital Media Server)
                                                        0x0C = HDMI2
                                                        0x0D = HDMI3
                                                        0x0E = USB Playlist
                                                        0x0F = USB AutoPlay
                                                        0x10= Media Player
                                                        0x11= PDF Player
                                                        0x12= Custom
                                                        0x13 = HDMI 4
                                                        0x14 =VGA2
                                                        0x15 = VGA3
                                                        0x16 = IWB
DATA[5]   HDMI / Component /                            5th priority:
          Composite / Display Port /                    0x00 = HDMI
          DVI-D / VGA / OPS / USB /                     0x01 = Component
          Browser / SmartCMS /                          0x02 = Composite
          Internal Storage / DMS / HDMI                 0x03 = Display Port
          2/ HDMI 3 / USB Playlist / USB                0x04 = DVI-D
          AutoPlay / Media Player / PDF                 0x05 = VGA
          player / Custom/HMDI 4/                       0x06 = OPS
          VGA2 / VGA3 / IWB                             0x07 = USB
                                                        0x08 = Browser
                                                        0x09 = SmartCMS
                                                        0x0A= Internal Storage
                                                        0x0B = DMS (Digital Media Server)
                                                        0x0C = HDMI2
                                                        0x0D = HDMI3
                                                        0x0E = USB Playlist
                                                        0x0F = USB AutoPlay
                                                        0x10= Media Player
                                                        0x11= PDF Player
                                                        0x12= Custom
                                                        0x13 = HDMI 4
                                                        0x14 =VGA2
                                                        0x15 = VGA3
                                                        0x16 = IWB





DATA[6]   HDMI / Component /                            6th priority:
          Composite / Display Port /                    0x00 = HDMI
          DVI-D / VGA / OPS / USB /                     0x01 = Component
          Browser / SmartCMS /                          0x02 = Composite
          Internal Storage / DMS / HDMI                 0x03 = Display Port
          2/ HDMI 3 / USB Playlist / USB                0x04 = DVI-D
          AutoPlay / Media Player / PDF                 0x05 = VGA
          player / Custom/HMDI 4/                       0x06 = OPS
          VGA2 / VGA3 / IWB                             0x07 = USB
                                                        0x08 = Browser
                                                        0x09 = SmartCMS
                                                        0x0A= Internal Storage
                                                        0x0B = DMS (Digital Media Server)
                                                        0x0C = HDMI2
                                                        0x0D = HDMI3
                                                        0x0E = USB Playlist
                                                        0x0F = USB AutoPlay
                                                        0x10= Media Player
                                                        0x11= PDF Player
                                                        0x12= Custom
                                                        0x13 = HDMI 4
                                                        0x14 =VGA2
                                                        0x15 = VGA3
                                                        0x16 = IWB
DATA[7]   HDMI / Component /                            7th priority:
          Composite / Display Port /                    0x00 = HDMI
          DVI-D / VGA / OPS / USB /                     0x01 = Component
          Browser / SmartCMS /                          0x02 = Composite
          Internal Storage / DMS / HDMI                 0x03 = Display Port
          2/ HDMI 3 / USB Playlist / USB                0x04 = DVI-D
          AutoPlay / Media Player / PDF                 0x05 = VGA
          player / Custom/HMDI 4/                       0x06 = OPS
          VGA2 / VGA3 / IWB                             0x07 = USB
                                                        0x08 = Browser
                                                        0x09 = SmartCMS
                                                        0x0A= Internal Storage
                                                        0x0B = DMS (Digital Media Server)
                                                        0x0C = HDMI2
                                                        0x0D = HDMI3
                                                        0x0E = USB Playlist
                                                        0x0F = USB AutoPlay
                                                        0x10= Media Player
                                                        0x11= PDF Player
                                                        0x12= Custom
                                                        0x13 = HDMI 4
                                                        0x14 =VGA2
                                                        0x15 = VGA3
                                                        0x16 = IWB





DATA[8]   HDMI / Component /                            8th priority:
          Composite / Display Port /                    0x00 = HDMI
          DVI-D / VGA / OPS / USB /                     0x01 = Component
          Browser / SmartCMS /                          0x02 = Composite
          Internal Storage / DMS / HDMI                 0x03 = Display Port
          2/ HDMI 3 / USB Playlist / USB                0x04 = DVI-D
          AutoPlay / Media Player / PDF                 0x05 = VGA
          player / Custom/HMDI 4/                       0x06 = OPS
          VGA2 / VGA3 / IWB                             0x07 = USB
                                                        0x08 = Browser
                                                        0x09 = SmartCMS
                                                        0x0A= Internal Storage
                                                        0x0B = DMS (Digital Media Server)
                                                        0x0C = HDMI2
                                                        0x0D = HDMI3
                                                        0x0E = USB Playlist
                                                        0x0F = USB AutoPlay
                                                        0x10= Media Player
                                                        0x11= PDF Player
                                                        0x12= Custom
                                                        0x13 = HDMI 4
                                                        0x14 =VGA2
                                                        0x15 = VGA3
                                                        0x16 = IWB
DATA[9]   HDMI / Component /                            9th priority:
          Composite / Display Port /                    0x00 = HDMI
          DVI-D / VGA / OPS / USB /                     0x01 = Component
          Browser / SmartCMS /                          0x02 = Composite
          Internal Storage / DMS / HDMI                 0x03 = Display Port
          2/ HDMI 3 / USB Playlist / USB                0x04 = DVI-D
          AutoPlay / Media Player / PDF                 0x05 = VGA
          player / Custom/HMDI 4/                       0x06 = OPS
          VGA2 / VGA3 / IWB                             0x07 = USB
                                                        0x08 = Browser
                                                        0x09 = SmartCMS
                                                        0x0A= Internal Storage
                                                        0x0B = DMS (Digital Media Server)
                                                        0x0C = HDMI2
                                                        0x0D = HDMI3
                                                        0x0E = USB Playlist
                                                        0x0F = USB AutoPlay
                                                        0x10= Media Player
                                                        0x11= PDF Player
                                                        0x12= Custom
                                                        0x13 = HDMI 4
                                                        0x14 =VGA2
                                                        0x15 = VGA3
                                                        0x16 = IWB





DATA[10]   HDMI / Component /                            10th priority:
           Composite / Display Port /                    0x00 = HDMI
           DVI-D / VGA / OPS / USB /                     0x01 = Component
           Browser / SmartCMS /                          0x02 = Composite
           Internal Storage / DMS / HDMI                 0x03 = Display Port
           2/ HDMI 3 / USB Playlist / USB                0x04 = DVI-D
           AutoPlay / Media Player / PDF                 0x05 = VGA
           player / Custom/HMDI 4/                       0x06 = OPS
           VGA2 / VGA3 / IWB                             0x07 = USB
                                                         0x08 = Browser
                                                         0x09 = SmartCMS
                                                         0x0A= Internal Storage
                                                         0x0B = DMS (Digital Media Server)
                                                         0x0C = HDMI2
                                                         0x0D = HDMI3
                                                         0x0E = USB Playlist
                                                         0x0F = USB AutoPlay
                                                         0x10= Media Player
                                                         0x11= PDF Player
                                                         0x12= Custom
                                                         0x13 = HDMI 4
                                                         0x14 =VGA2
                                                         0x15 = VGA3
                                                         0x16 = IWB
DATA[11]   HDMI / Component /                            11th priority:
           Composite / Display Port /                    0x00 = HDMI
           DVI-D / VGA / OPS / USB /                     0x01 = Component
           Browser / SmartCMS /                          0x02 = Composite
           Internal Storage / DMS / HDMI                 0x03 = Display Port
           2/ HDMI 3 / USB Playlist / USB                0x04 = DVI-D
           AutoPlay / Media Player / PDF                 0x05 = VGA
           player / Custom/HMDI 4/                       0x06 = OPS
           VGA2 / VGA3 / IWB                             0x07 = USB
                                                         0x08 = Browser
                                                         0x09 = SmartCMS
                                                         0x0A= Internal Storage
                                                         0x0B = DMS (Digital Media Server)
                                                         0x0C = HDMI2
                                                         0x0D = HDMI3
                                                         0x0E = USB Playlist
                                                         0x0F = USB AutoPlay
                                                         0x10= Media Player
                                                         0x11= PDF Player
                                                         0x12= Custom
                                                         0x13 = HDMI 4
                                                         0x14 =VGA2
                                                         0x15 = VGA3
                                                         0x16 = IWB





DATA[12]   HDMI / Component /                            12th priority:
           Composite / Display Port /                    0x00 = HDMI
           DVI-D / VGA / OPS / USB /                     0x01 = Component
           Browser / SmartCMS /                          0x02 = Composite
           Internal Storage / DMS / HDMI                 0x03 = Display Port
           2/ HDMI 3 / USB Playlist / USB                0x04 = DVI-D
           AutoPlay / Media Player / PDF                 0x05 = VGA
           player / Custom/HMDI 4/                       0x06 = OPS
           VGA2 / VGA3 / IWB                             0x07 = USB
                                                         0x08 = Browser
                                                         0x09 = SmartCMS
                                                         0x0A= Internal Storage
                                                         0x0B = DMS (Digital Media Server)
                                                         0x0C = HDMI2
                                                         0x0D = HDMI3
                                                         0x0E = USB Playlist
                                                         0x0F = USB AutoPlay
                                                         0x10= Media Player
                                                         0x11= PDF Player
                                                         0x12= Custom
                                                         0x13 = HDMI 4
                                                         0x14 =VGA2
                                                         0x15 = VGA3
                                                         0x16 = IWB
DATA[13]   HDMI / Component /                            13th priority:
           Composite / Display Port /                    0x00 = HDMI
           DVI-D / VGA / OPS / USB /                     0x01 = Component
           Browser / SmartCMS /                          0x02 = Composite
           Internal Storage / DMS / HDMI                 0x03 = Display Port
           2/ HDMI 3 / USB Playlist / USB                0x04 = DVI-D
           AutoPlay / Media Player / PDF                 0x05 = VGA
           player / Custom/HMDI 4/                       0x06 = OPS
           VGA2 / VGA3 / IWB                             0x07 = USB
                                                         0x08 = Browser
                                                         0x09 = SmartCMS
                                                         0x0A= Internal Storage
                                                         0x0B = DMS (Digital Media Server)
                                                         0x0C = HDMI2
                                                         0x0D = HDMI3
                                                         0x0E = USB Playlist
                                                         0x0F = USB AutoPlay
                                                         0x10= Media Player
                                                         0x11= PDF Player
                                                         0x12= Custom
                                                         0x13 = HDMI 4
                                                         0x14 =VGA2
                                                         0x15 = VGA3
                                                         0x16 = IWB





DATA[14]   HDMI / Component /                            14th priority:
           Composite / Display Port /                    0x00 = HDMI
           DVI-D / VGA / OPS / USB /                     0x01 = Component
           Browser / SmartCMS /                          0x02 = Composite
           Internal Storage / DMS / HDMI                 0x03 = Display Port
           2/ HDMI 3 / USB Playlist / USB                0x04 = DVI-D
           AutoPlay / Media Player / PDF                 0x05 = VGA
           player / Custom/HMDI 4/                       0x06 = OPS
           VGA2 / VGA3 / IWB                             0x07 = USB
                                                         0x08 = Browser
                                                         0x09 = SmartCMS
                                                         0x0A= Internal Storage
                                                         0x0B = DMS (Digital Media Server)
                                                         0x0C = HDMI2
                                                         0x0D = HDMI3
                                                         0x0E = USB Playlist
                                                         0x0F = USB AutoPlay
                                                         0x10= Media Player
                                                         0x11= PDF Player
                                                         0x12= Custom
                                                         0x13 = HDMI 4
                                                         0x14 =VGA2
                                                         0x15 = VGA3
                                                         0x16 = IWB
DATA[15]   HDMI / Component /                            14th priority:
           Composite / Display Port /                    0x00 = HDMI
           DVI-D / VGA / OPS / USB /                     0x01 = Component
           Browser / SmartCMS /                          0x02 = Composite
           Internal Storage / DMS / HDMI                 0x03 = Display Port
           2/ HDMI 3 / USB Playlist / USB                0x04 = DVI-D
           AutoPlay / Media Player / PDF                 0x05 = VGA
           player / Custom/HMDI 4/                       0x06 = OPS
           VGA2 / VGA3 / IWB                             0x07 = USB
                                                         0x08 = Browser
                                                         0x09 = SmartCMS
                                                         0x0A= Internal Storage
                                                         0x0B = DMS (Digital Media Server)
                                                         0x0C = HDMI2
                                                         0x0D = HDMI3
                                                         0x0E = USB Playlist
                                                         0x0F = USB AutoPlay
                                                         0x10= Media Player
                                                         0x11= PDF Player
                                                         0x12= Custom
                                                         0x13 = HDMI 4
                                                         0x14 =VGA2
                                                         0x15 = VGA3
                                                         0x16 = IWB





 DATA[16]        HDMI / Component /                                14th priority:
                 Composite / Display Port /                        0x00 = HDMI
                 DVI-D / VGA / OPS / USB /                         0x01 = Component
                 Browser / SmartCMS /                              0x02 = Composite
                 Internal Storage / DMS / HDMI                     0x03 = Display Port
                 2/ HDMI 3 / USB Playlist / USB                    0x04 = DVI-D
                 AutoPlay / Media Player / PDF                     0x05 = VGA
                 player / Custom/HMDI 4/                           0x06 = OPS
                 VGA2 / VGA3 / IWB                                 0x07 = USB
                                                                   0x08 = Browser
                                                                   0x09 = SmartCMS
                                                                   0x0A= Internal Storage
                                                                   0x0B = DMS (Digital Media Server)
                                                                   0x0C = HDMI2
                                                                   0x0D = HDMI3
                                                                   0x0E = USB Playlist
                                                                   0x0F = USB AutoPlay
                                                                   0x10= Media Player
                                                                   0x11= PDF Player
                                                                   0x12= Custom
                                                                   0x13 = HDMI 4
                                                                   0x14 =VGA2
                                                                   0x15 = VGA3
                                                                   0x16 = IWB
 DATA[17]        HDMI / Component /                                14th priority:
                 Composite / Display Port /                        0x00 = HDMI
                 DVI-D / VGA / OPS / USB /                         0x01 = Component
                 Browser / SmartCMS /                              0x02 = Composite
                 Internal Storage / DMS / HDMI                     0x03 = Display Port
                 2/ HDMI 3 / USB Playlist / USB                    0x04 = DVI-D
                 AutoPlay / Media Player / PDF                     0x05 = VGA
                 player / Custom/HMDI 4/                           0x06 = OPS
                 VGA2 / VGA3 / IWB                                 0x07 = USB
                                                                   0x08 = Browser
                                                                   0x09 = SmartCMS
                                                                   0x0A= Internal Storage
                                                                   0x0B = DMS (Digital Media Server)
                                                                   0x0C = HDMI2
                                                                   0x0D = HDMI3
                                                                   0x0E = USB Playlist
                                                                   0x0F = USB AutoPlay
                                                                   0x10= Media Player
                                                                   0x11= PDF Player
                                                                   0x12= Custom
                                                                   0x13 = HDMI 4
                                                                   0x14 =VGA2
                                                                   0x15 = VGA3
                                                                   0x16 = IWB




Example: Current Display settings: Sources priority = HDMI – Component – Composite – Display Port – DVI-D –
VGA – OPS – USB – Browser – SmartCMS – Internal Storage – DMS – HDMI 2 – HDMI3 (Display address 01)

 MsgSize       Contro     Group       Data (0)        Data (1)      Data (2)     Data (3)   Data (4)   Data (5)
               l
 0x0D          0x01       0x00        0xA6            0x00          0x01         0x02       0x03       0x04

Data (6)    Data   Data (8)      Data (9)        Data (10)       Data (11)      Data (12)   Data (13)
            (7)
0x05        0x06   0x07          0x08            0x09            0x0A           0x0B          0x0C
Data (14)   Data   Data          Data (17)       Checksum
            (15)   (16)
  0x0D





```

#### 4.5.6 Message-Set

```text

Bytes       Bytes Description                    Bits      Description
DATA[0]     0xA5 = Failover – Set                          Command to change the Failover setting of the
                                                           display
DATA[1]     HDMI / Component /                             1st priority:
            Composite / Display Port /                     0x00 = HDMI
            DVI-D / VGA / OPS / USB /                      0x01 = Component
            Browser / SmartCMS /                           0x02 = Composite
            Internal Storage / DMS / HDMI                  0x03 = Display Port
            2/ HDMI 3 / USB Playlist / USB                 0x04 = DVI-D
            AutoPlay / Media Player / PDF                  0x05 = VGA
            player / Custom/ HDMI 4 /                      0x06 = OPS
            VGA2 / VGA3 / IWB /                            0x07 = USB
                                                           0x08 = Browser
                                                           0x09 = SmartCMS
                                                           0x0A= Internal Storage
                                                           0x0B = DMS (Digital Media Server)
                                                           0x0C = HDMI2
                                                           0x0D = HDMI3
                                                           0x0E = USB Playlist
                                                           0x0F = USB AutoPlay
                                                           0x10= Media Player
                                                           0x11= PDF Player
                                                           0x12= Custom
                                                           0x13 = HDMI 4
                                                           0x14 =VGA2
                                                           0x15 = VGA3
                                                           0x16 = IWB
DATA[2]     HDMI / Component /                             2nd priority:
            Composite / Display Port /                     0x00 = HDMI
            DVI-D / VGA / OPS / USB /                      0x01 = Component
            Browser / SmartCMS /                           0x02 = Composite
            Internal Storage / DMS / HDMI                  0x03 = Display Port
            2/ HDMI 3 / USB Playlist / USB                 0x04 = DVI-D
            AutoPlay / Media Player / PDF                  0x05 = VGA
            player / Custom/ HDMI 4 /                      0x06 = OPS
            VGA2 / VGA3 / IWB /                            0x07 = USB
                                                           0x08 = Browser
                                                           0x09 = SmartCMS
                                                           0x0A= Internal Storage
                                                           0x0B = DMS (Digital Media Server)
                                                           0x0C = HDMI2
                                                           0x0D = HDMI3
                                                           0x0E = USB Playlist
                                                           0x0F = USB AutoPlay
                                                           0x13 = HDMI 4
                                                           0x14 =VGA2
                                                           0x15 = VGA3
                                                           0x16 = IWB





DATA[3]   HDMI / Component /                             3rd priority:
          Composite / Display Port /                     0x00 = HDMI
          DVI-D / VGA / OPS / USB /                      0x01 = Component
          Browser / SmartCMS /                           0x02 = Composite
          Internal Storage / DMS / HDMI                  0x03 = Display Port
          2/ HDMI 3 / USB Playlist / USB                 0x04 = DVI-D
          AutoPlay / Media Player / PDF                  0x05 = VGA
          player / Custom/ HDMI 4 /                      0x06 = OPS
          VGA2 / VGA3 / IWB /                            0x07 = USB
                                                         0x08 = Browser
                                                         0x09 = SmartCMS
                                                         0x0A= Internal Storage
                                                         0x0B = DMS (Digital Media Server)
                                                         0x0C = HDMI2
                                                         0x0D = HDMI3
                                                         0x0E = USB Playlist
                                                         0x0F = USB AutoPlay
                                                         0x13 = HDMI 4
                                                         0x14 =VGA2
                                                         0x15 = VGA3
                                                         0x16 = IWB
DATA[4]   HDMI / Component /                             4th priority:
          Composite / Display Port /                     0x00 = HDMI
          DVI-D / VGA / OPS / USB /                      0x01 = Component
          Browser / SmartCMS /                           0x02 = Composite
          Internal Storage / DMS / HDMI                  0x03 = Display Port
          2/ HDMI 3 / USB Playlist / USB                 0x04 = DVI-D
          AutoPlay / Media Player / PDF                  0x05 = VGA
          player / Custom/ HDMI 4 /                      0x06 = OPS
          VGA2 / VGA3 / IWB /                            0x07 = USB
                                                         0x08 = Browser
                                                         0x09 = SmartCMS
                                                         0x0A= Internal Storage
                                                         0x0B = DMS (Digital Media Server)
                                                         0x0C = HDMI2
                                                         0x0D = HDMI3
                                                         0x0E = USB Playlist
                                                         0x0F = USB AutoPlay
                                                         0x13 = HDMI 4
                                                         0x14 =VGA2
                                                         0x15 = VGA3
                                                         0x16 = IWB
DATA[5]   HDMI / Component /                             5th priority:
          Composite / Display Port /                     0x00 = HDMI
          DVI-D / VGA / OPS / USB /                      0x01 = Component
          Browser / SmartCMS /                           0x02 = Composite
          Internal Storage / DMS / HDMI                  0x03 = Display Port
          2/ HDMI 3 / USB Playlist / USB                 0x04 = DVI-D
          AutoPlay / Media Player / PDF                  0x05 = VGA
          player / Custom/ HDMI 4 /                      0x06 = OPS
          VGA2 / VGA3 / IWB /                            0x07 = USB
                                                         0x08 = Browser
                                                         0x09 = SmartCMS
                                                         0x0A= Internal Storage
                                                         0x0B = DMS (Digital Media Server)
                                                         0x0C = HDMI2
                                                         0x0D = HDMI3
                                                         0x0E = USB Playlist
                                                         0x0F = USB AutoPlay

                                                         0x13 = HDMI 4
                                                         0x14 =VGA2
                                                         0x15 = VGA3
                                                         0x16 = IWB




DATA[6]   HDMI / Component /                             6th priority:
          Composite / Display Port /                     0x00 = HDMI
          DVI-D / VGA / OPS / USB /                      0x01 = Component
          Browser / SmartCMS /                           0x02 = Composite
          Internal Storage / DMS / HDMI                  0x03 = Display Port
          2/ HDMI 3 / USB Playlist / USB                 0x04 = DVI-D
          AutoPlay / Media Player / PDF                  0x05 = VGA
          player / Custom/ HDMI 4 /                      0x06 = OPS
          VGA2 / VGA3 / IWB /                            0x07 = USB
                                                         0x08 = Browser
                                                         0x09 = SmartCMS
                                                         0x0A= Internal Storage
                                                         0x0B = DMS (Digital Media Server)
                                                         0x0C = HDMI2
                                                         0x0D = HDMI3
                                                         0x0E = USB Playlist
                                                         0x0F = USB AutoPlay
                                                         0x13 = HDMI 4
                                                         0x14 =VGA2
                                                         0x15 = VGA3
                                                         0x16 = IWB
DATA[7]   HDMI / Component /                             7th priority:
          Composite / Display Port /                     0x00 = HDMI
          DVI-D / VGA / OPS / USB /                      0x01 = Component
          Browser / SmartCMS /                           0x02 = Composite
          Internal Storage / DMS / HDMI                  0x03 = Display Port
          2/ HDMI 3 / USB Playlist / USB                 0x04 = DVI-D
          AutoPlay / Media Player / PDF                  0x05 = VGA
          player / Custom/ HDMI 4 /                      0x06 = OPS
          VGA2 / VGA3 / IWB /                            0x07 = USB
                                                         0x08 = Browser
                                                         0x09 = SmartCMS
                                                         0x0A= Internal Storage
                                                         0x0B = DMS (Digital Media Server)
                                                         0x0C = HDMI2
                                                         0x0D = HDMI3
                                                         0x0E = USB Playlist
                                                         0x0F = USB AutoPlay
                                                         0x13 = HDMI 4
                                                         0x14 =VGA2

                                                         0x15 = VGA3
                                                         0x16 = IWB




DATA[8]   HDMI / Component /                             8th priority:
          Composite / Display Port /                     0x00 = HDMI
          DVI-D / VGA / OPS / USB /                      0x01 = Component
          Browser / SmartCMS /                           0x02 = Composite
          Internal Storage / DMS / HDMI                  0x03 = Display Port
          2/ HDMI 3 / USB Playlist / USB                 0x04 = DVI-D
          AutoPlay / Media Player / PDF                  0x05 = VGA
          player / Custom/ HDMI 4 /                      0x06 = OPS
          VGA2 / VGA3 / IWB /                            0x07 = USB
                                                         0x08 = Browser
                                                         0x09 = SmartCMS
                                                         0x0A= Internal Storage
                                                         0x0B = DMS (Digital Media Server)
                                                         0x0C = HDMI2
                                                         0x0D = HDMI3
                                                         0x0E = USB Playlist
                                                         0x0F = USB AutoPlay
                                                         0x13 = HDMI 4
                                                         0x14 =VGA2
                                                         0x15 = VGA3
                                                         0x16 = IWB





DATA[9]    HDMI / Component /                             8th priority:
           Composite / Display Port /                     0x00 = HDMI
           DVI-D / VGA / OPS / USB /                      0x01 = Component
           Browser / SmartCMS /                           0x02 = Composite
           Internal Storage / DMS / HDMI                  0x03 = Display Port
           2/ HDMI 3 / USB Playlist / USB                 0x04 = DVI-D
           AutoPlay / Media Player / PDF                  0x05 = VGA
           player / Custom/ HDMI 4 /                      0x06 = OPS
           VGA2 / VGA3 / IWB /                            0x07 = USB
                                                          0x08 = Browser
                                                          0x09 = SmartCMS
                                                          0x0A= Internal Storage
                                                          0x0B = DMS (Digital Media Server)
                                                          0x0C = HDMI2
                                                          0x0D = HDMI3
                                                          0x0E = USB Playlist
                                                          0x0F = USB AutoPlay
                                                          0x13 = HDMI 4
                                                          0x14 =VGA2
                                                          0x15 = VGA3
                                                          0x16 = IWB
DATA[10]   HDMI / Component /                             8th priority:
           Composite / Display Port /                     0x00 = HDMI
           DVI-D / VGA / OPS / USB /                      0x01 = Component
           Browser / SmartCMS /                           0x02 = Composite
           Internal Storage / DMS / HDMI                  0x03 = Display Port
           2/ HDMI 3 / USB Playlist / USB                 0x04 = DVI-D
           AutoPlay / Media Player / PDF                  0x05 = VGA
           player / Custom/ HDMI 4 /                      0x06 = OPS
           VGA2 / VGA3 / IWB /                            0x07 = USB
                                                          0x08 = Browser
                                                          0x09 = SmartCMS
                                                          0x0A= Internal Storage
                                                          0x0B = DMS (Digital Media Server)
                                                          0x0C = HDMI2
                                                          0x0D = HDMI3
                                                          0x0E = USB Playlist
                                                          0x0F = USB AutoPlay
                                                          0x13 = HDMI 4
                                                          0x14 =VGA2
                                                          0x15 = VGA3
                                                          0x16 = IWB
DATA[11]   HDMI / Component /                             8th priority:
           Composite / Display Port /                     0x00 = HDMI
           DVI-D / VGA / OPS / USB /                      0x01 = Component
           Browser / SmartCMS /                           0x02 = Composite
           Internal Storage / DMS / HDMI                  0x03 = Display Port
           2/ HDMI 3 / USB Playlist / USB                 0x04 = DVI-D
           AutoPlay / Media Player / PDF                  0x05 = VGA
           player / Custom/ HDMI 4 /                      0x06 = OPS
           VGA2 / VGA3 / IWB /                            0x07 = USB
                                                          0x08 = Browser
                                                          0x09 = SmartCMS
                                                          0x0A= Internal Storage
                                                          0x0B = DMS (Digital Media Server)
                                                          0x0C = HDMI2
                                                          0x0D = HDMI3
                                                          0x0E = USB Playlist
                                                          0x0F = USB AutoPlay
                                                          0x13 = HDMI 4
                                                          0x14 =VGA2
                                                          0x15 = VGA3
                                                          0x16 = IWB

DATA[12]   HDMI / Component /                             8th priority:
           Composite / Display Port /                     0x00 = HDMI
           DVI-D / VGA / OPS / USB /                      0x01 = Component
           Browser / SmartCMS /                           0x02 = Composite
           Internal Storage / DMS / HDMI                  0x03 = Display Port
           2/ HDMI 3 / USB Playlist / USB                 0x04 = DVI-D
           AutoPlay / Media Player / PDF                  0x05 = VGA
           player / Custom/ HDMI 4 /                      0x06 = OPS
           VGA2 / VGA3 / IWB /                            0x07 = USB
                                                          0x08 = Browser
                                                          0x09 = SmartCMS
                                                          0x0A= Internal Storage
                                                          0x0B = DMS (Digital Media Server)
                                                          0x0C = HDMI2
                                                          0x0D = HDMI3
                                                          0x0E = USB Playlist
                                                          0x0F = USB AutoPlay
                                                          0x13 = HDMI 4
                                                          0x14 =VGA2
                                                          0x15 = VGA3
                                                          0x16 = IWB
DATA[13]   HDMI / Component /                             13th priority:
           Composite / Display Port /                     0x00 = HDMI
           DVI-D / VGA / OPS / USB /                      0x01 = Component
           Browser / SmartCMS /                           0x02 = Composite
           Internal Storage / DMS / HDMI                  0x03 = Display Port
           2/ HDMI 3 / USB Playlist / USB                 0x04 = DVI-D
           AutoPlay / Media Player / PDF                  0x05 = VGA
           player / Custom/ HDMI 4 /                      0x06 = OPS
           VGA2 / VGA3 / IWB /                            0x07 = USB
                                                          0x08 = Browser
                                                          0x09 = SmartCMS
                                                          0x0A= Internal Storage
                                                          0x0B = DMS (Digital Media Server)
                                                          0x0C = HDMI2
                                                          0x0D = HDMI3
                                                          0x0E = USB Playlist
                                                          0x0F = USB AutoPlay
                                                          0x13 = HDMI 4
                                                          0x14 =VGA2
                                                          0x15 = VGA3
                                                          0x16 = IWB
DATA[14]   HDMI / Component /                             14th priority:
           Composite / Display Port /                     0x00 = HDMI
           DVI-D / VGA / OPS / USB /                      0x01 = Component
           Browser / SmartCMS /                           0x02 = Composite
           Internal Storage / DMS / HDMI                  0x03 = Display Port
           2/ HDMI 3 / USB Playlist / USB                 0x04 = DVI-D
           AutoPlay / Media Player / PDF                  0x05 = VGA
           player / Custom/ HDMI 4 /                      0x06 = OPS
           VGA2 / VGA3 / IWB /                            0x07 = USB
                                                          0x08 = Browser
                                                          0x09 = SmartCMS
                                                          0x0A= Internal Storage
                                                          0x0B = DMS (Digital Media Server)
                                                          0x0C = HDMI2
                                                          0x0D = HDMI3
                                                          0x0E = USB Playlist
                                                          0x0F = USB AutoPlay
                                                          0x13 = HDMI 4
                                                          0x14 =VGA2

                                                                     0x15 = VGA3
                                                                     0x16 = IWB




Example: Set the Display to the fallowing: Sources priority = HDMI – Component – Composite – Display Port – DVI-
D – VGA – OPS – USB – Browser – SmartCMS – Internal Storage – DMS – HDMI2 – HDMI3 (Display address 01)

 MsgSize      Control       Group      Data (0)        Data (1)      Data (2)   Data (3)   Data (4)   Data (5)
 0x0D         0x01          0x00       0xA5            0x00          0x01       0x02       0x03       0x04
 Data (6)     Data (7)      Data       Data (9)        Data (10)      Data (11)    Data (12)    Data (13)
                            (8)
 0x05         0x06          0x07       0x08            0x09            0x0A           0x0B          0x0C
 Data         Checksum
 (14)
 0x0D             A8





```

### 4.6 Monitor restart

```text

           The following command is used to restart/reboot the monitor.
           Only possible on android monitors Himalaya 2 and Dragon2 and future models, see platform , from
           firmware version xx TBC


```

#### 4.6.1 Message-Set

```text

  Bytes   Bytes Description                            Bits     Description
  DATA[0] 0x57 = monitor Restart – Set                          Command to restart monitor

  DATA[1]       Select target system to                         0x00 = Android
                restart                                         0x01 = Scalar (?)


 Example: Restart Android system of the monitor (Display address 01)
  MsgSize Control Group           Data (0) Data (1)       Checksum
  0x06      0x01      0x00        0x57       0x00         0x50


```

### 4.7 Backlight On-Off

#### 4.7.1 Get backlight status

```text

  Check if the backlight is off or on
  Supported on models : TBC

  Bytes   Bytes Description                            Bits     Description
  DATA[0] 0x71 = Backlight – Get                                Command to restart monitor


 Example: get the picture mute status
  MsgSize Control Group           Data (0)           Checksum
  0x05      0x01        0x00      0x71               0x50


  Report from monitor
  06 01 00 71 00 76 > get status : backlight is on
  06 01 00 71 01 77 > get status : backlight is off

```

#### 4.7.2 Set backlight on-off

```text

    Set the backlight on or off. (the audio will not be muted/unmuted)

    Message-Set

  Bytes   Bytes Description                            Bits     Description
  DATA[0] 0x72 = Backlight – Set                                Command to switch on-off the backlights

  DATA[1]                                                       0x00 = backlight on
                                                                0x01 = backlight off


 Example: mute the picture (Display address 01)
  MsgSize Control Group           Data (0) Data (1)                  Checksum
  0x06     0x01        0x00       0x72        0x01                   0x74

06 01 00 72 00 75 > set backlight on
06 01 00 72 01 74 > set backlight off


MESSAGES – VIDEO


```

### 5.1 Video Parameters

```text

          The following commands are used to get/set video parameters as it is defined below.
          Those commands (0x32 / 0x33) are not working on platform QL3 on source inputs: browser, PDF
          player, media player, CMND&play, installed apk.


```

#### 5.1.1 Message-Get Video parameters

```text

          Bytes         Bytes Description                       Bits      Description
          DATA[0]       0x33 = Video Parameters –                         Command requests the display to report its current
                        Get                                               video parameters.

         Example: (Display address 01)
          MsgSize Control Group            Data (0)      Checksum
          0x05        0x01        0x00     0x33          0x37


```

#### 5.1.2 Message-Report Video parameters

```text

          Bytes       Bytes Description                     Bits     Description
          DATA[0]     0x33 = Video Parameters –                      Command reports to the host controller the current
                      Report                                         video parameters of the display.
          DATA[1]     Brightness.                                    0 to 100 (%) of the user selectable range of the display.
          DATA[2]     Color.                                         0 to 100 (%) of the user selectable range of the display.
          DATA[3]     Contrast.                                      0 to 100 (%) of the user selectable range of the display.
          DATA[4]     Sharpness.                                     0 to 100 (%) of the user selectable range of the display.
          DATA[5]     Tint (Hue)                                     0 to 100 (%) of the user selectable range of the display.
          DATA[6]     Black Level                                    0 to 100 (%) of the user selectable range of the display.
          DATA[7]     Gamma Selection                                0x01= Native, 0x02 = S gamma, 0x03 = 2.2, 0x04 = 2.4,
                                                                     0x05 = D-image(DICOM gamma)

         SPECIAL NOTE: Following table applicable for Phoenix 2.0 platform only (year 2015
          BDLxx70EL/BDLxx90VL/BDLxx30QL/BDLxx35QL)



          Bytes       Bytes Description                     Bits     Description
          DATA[0]     0x33 = Video Parameters –                      Command reports to the host controller the current
                      Report                                         video parameters of the display.
          DATA[1]     Brightness.                                    0 to 100 (%) of the user selectable range of the display.
          DATA[2]     Color.                                         0 to 100 (%) of the user selectable range of the display.
          DATA[3]     Contrast.                                      0 to 100 (%) of the user selectable range of the display.
          DATA[4]     Sharpness.                                     0 to 10 (%) of the user selectable range of the display.
          DATA[5]     Tint (Hue)                                     -50 to +50 (%) of the user selectable range of the
                                                                     display.
          DATA[6]     Black Level                                    0 to 100 (%) of the user selectable range of the display.
          DATA[7]     Gamma Selection                                0x01= Native, 0x02 = S gamma, 0x03 = 2.2, 0x04 = 2.4,
                                                                     0x05 = D-image(DICOM gamma)



        Example: All video parameters are set to 55 % (0x37) (Display address 01)
MsgSize Control Group Data (0)                Data (1)    Data (2)     Data (3)   Data (4)        Data (5)     Data (6)   Data (7)
0x0C     0x01         0x00      0x33          0x37        0x37         0x37       0x37            0x37         0x37       0x03
Checksum
0x3D

```

#### 5.1.3 Message-Set Video parameters

```text
 This command is not working on platform QL3 on source inputs: browser, PDF player, media player,
         CMND&play,
         installed apk.


 Bytes         Bytes Description                    Bits      Description
 DATA[0]       0x32 = Video Parameters –                      Command to change the current video parameters
               Set
 DATA[1]       Brightness.                                    0 to 100 (%) of the user selectable range of the display.
 DATA[2]       Color.                                         0 to 100 (%) of the user selectable range of the display.
 DATA[3]       Contrast.                                      0 to 100 (%) of the user selectable range of the display.
 DATA[4]       Sharpness.                                     0 to 100 (%) of the user selectable range of the display.
 DATA[5]       Tint (Hue)                                     0 to 100 (%) of the user selectable range of the display.
 DATA[6]       Black Level                                    0 to 100 (%) of the user selectable range of the display.
 DATA[7]       Gamma Selection                                0x01= Native, 0x02 = S gamma, 0x03 = 2.2, 0x04 = 2.4,
                                                              0x05 = D-image(DICOM gamma)

         NOTE: Following table applicable for Phoenix 2.0 platform only (year 2015
         BDLxx70EL/BDLxx90VL/BDLxx30QL/BDLxx35QL)

 Bytes         Bytes Description                    Bits      Description
 DATA[0]       0x32 = Video Parameters –                      Command to change the current video parameters
               Set
 DATA[1]       Brightness.                                    0 to 100 (%) of the user selectable range of the display.
 DATA[2]       Color.                                         0 to 100 (%) of the user selectable range of the display.
 DATA[3]       Contrast.                                      0 to 100 (%) of the user selectable range of the display.
 DATA[4]       Sharpness.                                     0 to 10 (%) of the user selectable range of the display.
 DATA[5]       Tint (Hue)                                     -50 to +50 (%) of the user selectable range of the
                                                              display.
 DATA[6]       Black Level                                    0 to 100 (%) of the user selectable range of the display.
 DATA[7]       Gamma Selection                                0x01= Native, 0x02 = S gamma, 0x03 = 2.2, 0x04 = 2.4,
                                                              0x05 = D-image(DICOM gamma)

         NOTE: Following table applicable for Phoenix 2.0 platform only (year 2015
         BDLxx70EL/BDLxx90VL/BDLxx30QL/BDLxx35QL)

      NOTE: Tint(Hue) value (-50) ～ (-1)

       -50         -49        -48         -47         -46        -45          -44      -43        -42         -41
        0xCE      0xCF       0xD0        0xD1        0xD2       0xD3         0xD4     0xD5       0xD6        0xD7
         -40       -39        -38         -37         -36        -35          -34      -33        -32         -31
        0xD8      0xD9       0xDA        0xDB        0xDC       0xDD         0xDE     0xDF       0xE0        0xE1
         -30       -29        -28         -27         -26        -25          -24      -23        -22         -21
        0xE2      0xE3       0xE4        0xE5        0xE6       0xE7         0xE8     0xE9       0xEA        0xEB
         -20       -19        -18         -17         -16        -15          -14      -13        -12         -11
        0xEC      0xED       0xEE        0xEF        0xF0       0xF1         0xF2     0xF3       0xF4        0xF5
         -10        -9         -8          -7          -6         -5           -4       -3         -2          -1
        0xF6      0xF7       0xF8        0xF9        0xFA       0xFB         0xFC     0xFD       0xFE        0xFF


Example: Set all video parameters to 0x37 (55 %) (Display address 01)
MsgSize Control Group                Data (0)   Data (1)     Data (2)      Data (3)   Data (4)    Data (5)     Data (6)   Data (7)
0x0C       0x01         0x00         0x32       0x37         0x37          0x37       0x37        0x37         0x37       0x03

 Checksum
 0x3C

  The following commands are used to get/set the color temperature.


```

#### 5.1.4 Message-Get Color Temperature

```text

  Bytes           Bytes Description                         Bits     Description
 DATA[0]         0x35 = Color Temperature –                         Command requests the display to report its current
                 Get                                                color temperature.

Example: (Display address 01)
 MsgSize Control Group                Data (0)     Checksum
 0x05        0x01        0x00         0x35         0x31



```

#### 5.1.5 Message-Report Color Temperature

```text

 Bytes         Bytes Description                     Bits     Description
 DATA[0]       0x35 = Color Temperature                       Command reports to the host controller the current
               – Report                                       color temperature of the display.
 DATA[1]       Color temperature                              0x00 = User 1
                                                              0x01 = Native
                                                              0x02 = 11000K(Not applicable)
                                                              0x03 = 10000K
                                                              0x04 = 9300K
                                                              0x05 = 7500K
                                                              0x06 = 6500K
                                                              0x07 = 5770K (Not pplicable)
                                                              0x08 = 5500K(Not applicable)
                                                              0x09 = 5000K
                                                              0x0A = 4000K
                                                              0x0B = 3400K (Not applicable)
                                                              0x0C = 3350K (Not applicable)
                                                              0x0D = 3000K
                                                              0x0E = 2800K (Not pplicable)
                                                              0x0F = 2600K (Not applicable)
                                                              0x10 = 1850K (Notapplicable)
                                                              0x12 = User 2

Example: The current color temperature is set to Native (Display address 01)
 MsgSize Control Group               Data (0)      Data (1)     Checksum
 0x06       0x01         0x00        0x35          0x01         0x33



```

#### 5.1.6 Message-Set Color Temperature

```text

 Bytes         Bytes Description                     Bits      Description
 DATA[0]       0x34 = Color Temperature                        Command to change the current color parameters
               – Set





DATA[1]   Color temperature                             0x00 = User 1
                                                        0x01 = Native
                                                        0x02 = 11000K(Not applicable)
                                                        0x03 = 10000K
                                                        0x04 = 9300K
                                                        0x05 = 7500K
                                                        0x06 = 6500K
                                                        0x07 = 5770K (Not pplicable)
                                                        0x08 = 5500K(Not applicable)
                                                        0x09 = 5000K
                                                        0x0A = 4000K
                                                        0x0B = 3400K (Not applicable)
                                                        0x0C = 3350K (Not applicable)
                                                        0x0D = 3000K





           The following commands are used to get/set the color parameters for specific color temperature.
                                                                   0x0E = 2800K (Not applicable)
                                                                   0x0F = 2600K (Not applicable)
                                                                   0x10 = 1850K (Not applicable)
                                                                   0x12 = User 2

           Example: The current color temperature is set to Native (Display address 01)
            MsgSize Control Group               Data (0)      Data (1)     Checksum
            0x06       0x01         0x00        0x34          0x01         0x32


```

#### 5.1.7 Message-Get RGB parameters

```text
                       This command is not working on platform QL3 on source inputs: browser, PDF player, media player, CMND&play,
                       installed apk.

            Bytes           Bytes Description                        Bits      Description
            DATA[0]         0x37 = Color Parameters –                          Command requests the display to report its current
                            Get                                                color parameters.

           Example: (Display address 01)
            MsgSize Control Group                Data (0)     Checksum
            0x05        0x01        0x00         0x37         0x33



```

#### 5.1.8 Message-Report RGB parameters

```text

            Bytes         Bytes Description                     Bits     Description
            DATA[0]       0x37 = Color Parameters –                      Command reports to the host controller the current
                          Report                                         color parameters of the display.
            DATA[1]       Red color gain value                           0 to 255 of the user selectable range of the display.
            DATA[2]       Green color gain value                         0 to 255 of the user selectable range of the display.
            DATA[3]       Blue color gain value                          0 to 255 of the user selectable range of the display.
            DATA[4]       Red color offset value                         0 to 255 of the user selectable range of the display.
            DATA[5]       Green color offset value                       0 to 255 of the user selectable range of the display.
            DATA[6]       Blue color offset value                        0 to 255 of the user selectable range of the display.

           Example: All color parameters are set to 255 (0xFF) (Display address 01)
 MsgSize      Control Group           Data (0)      Data (1)     Data (2)    Data (3)      Data (4)    Data (5)    Data (6)       Check
 0x0B         0x01         0x00       0x37          0xFF         0xFF        0xFF          0xFF        0xFF        0xFF           0x3D



```

#### 5.1.9 Message-Set RGB parameters

```text
                       This command is not working on platform QL3 on source inputs: browser, PDF player, media player, CMND&play,
                       installed apk.

            Bytes         Bytes Description                     Bits      Description
            DATA[0]       0x36 = Color Parameters –                       Command to change the current color parameters
                          Set
            DATA[1]       Red color gain value                            0 to 255 of the user selectable range of the display.
            DATA[2]       Green color gain value                          0 to 255 of the user selectable range of the display.
            DATA[3]       Blue color gain value                           0 to 255 of the user selectable range of the display.
            DATA[4]       Red color offset value                          0 to 255 of the user selectable range of the display.
            DATA[5]       Green color offset value                        0 to 255 of the user selectable range of the display.
            DATA[6]       Blue color offset value                         0 to 255 of the user selectable range of the display.

           Example: All color parameters are set to 255 (0xFF) (Display address 01)
MsgSize     Control Group            Data (0)      Data (1)    Data (2)     Data (3)      Data (4)    Data (5)    Data (6)      Check
0x0B        0x01         0x00        0x36          0xFF        0xFF         0xFF          0xFF        0xFF        0xFFPage | 44 0x3C

The following commands are used to get/set the color temperature 100K/step adjustment.


```

##### 5.1.9.1 Message-Get Color Temperature 100K steps

```text

 Bytes           Bytes Description                       Bits      Description
 DATA[0]         0x12 = Color Temperature                          Command requests the display to report its current
                 100K steps – Get                                  color temperature 100K steps.

Example: (Display address 01)
 MsgSize Control Group               Data (0)     Checksum
 0x05        0x01        0x00        0x12         0x16


```

##### 5.1.9.2 Message-Report Color Temperature 100K steps

```text

 Bytes         Bytes Description                    Bits     Description
 DATA[0]       0x12 = Color Temperature                      Command reports to the host controller the current
               100K – Report                                 color temperature 100K steps of the display.
 DATA[1]       Color temperature steps                       20 to 100 of the user selectable range of the display.
                                                             0x14(20) = 2000K
                                                             0x15(21)= 2100K
                                                             0x16(22) = 2200K
                                                             ………………
                                                             0x61(97) = 9700K
                                                             0x62(98) = 9800K
                                                             0x63(99) = 9900K
                                                             0x64(100) = 10000K

NOTE: Following table applicable for Phoenix 2.0 platform only (year 2015
BDLxx70EL/BDLxx90VL/BDLxx30QL/BDLxx35QL)

 Bytes         Bytes Description                    Bits     Description
 DATA[0]       0x12 = Color Temperature                      Command reports to the host controller the current
               100K – Report                                 color temperature 100K steps of the display.
 DATA[1]       Color temperature steps                       20 to 100 of the user selectable range of the display.
                                                             0x1A(26) = 2600K
                                                             0x1B(27) = 2700K
                                                             0x1C(28) = 2800K
                                                             ………………
                                                             0x61(97) = 9700K
                                                             0x62(98) = 9800K
                                                             0x63(99) = 9900K
                                                             0x64(100) = 10000K

Example: The current color temperature is set to 10000K (Display address 01)
 MsgSize Control Group               Data (0)      Data (1)   Checksum
 0x06       0x01         0x00        0x12          0x64       0x71



```

##### 5.1.9.3 Message-Set Color Temperature 100K steps

```text

 Bytes         Bytes Description                    Bits     Description
 DATA[0]       0x11 = Color Temperature                      Command to change the current color temperature
               100K steps – Set                              100K steps
 DATA[1]       Color temperature                             20 to 100 of the user selectable range of the display.
                                                             0x14(20) = 2000K


                                                             0x15(21)= 2100K
                                                             0x16(22) = 2200K
                                                             ………………
                                                             0x61(97) = 9700K
                                                             0x62(98) = 9800K
                                                             0x63(99) = 9900K
                                                             0x64(100) = 10000K

NOTE: Following table applicable for Phoenix 2.0 platform only (year 2015
BDLxx70EL/BDLxx90VL/BDLxx30QL/BDLxx35QL)

 Bytes         Bytes Description                    Bits     Description
 DATA[0]       0x11 = Color Temperature                      Command to change the current color temperature
               100K steps – Set                              100K steps
 DATA[1]       Color temperature                             20 to 100 of the user selectable range of the display.
                                                             0x1A(26) = 2600K
                                                             0x1B(27) = 2700K
                                                             0x1C(28) = 2800K
                                                             ………………
                                                             0x61(97) = 9700K
                                                             0x62(98) = 9800K
                                                             0x63(99) = 9900K
                                                             0x64(100) = 10000K

Example: The current color temperature is set to 10000K (Display address 01)
 MsgSize Control Group               Data (0)      Data (1)   Checksum
 0x06       0x01         0x00        0x11          0x64       0x72





```

### 5.2 Picture Format

```text
This command is used to control the display screen format.

```

#### 5.2.1 Message-Get

```text

 Bytes           Bytes Description                 Bits       Description
 DATA[0]         0x3B = Picture Format –                      Command requests the display to report its current
                 Get                                          picture format

Example: (Display address 01)
 MsgSize Control Group               Data (0)      Checksum
 0x05        0x01        0x00        0x3B          0x3F


```

#### 5.2.2 Message-Report

```text

 Bytes           Bytes Description                        Bits       Description
 DATA[0]         0x3B = Picture Format –                             Command report to the host controller the
                 Report                                              current picture format of the display.
 DATA[1]         Picture Format*                          Bit 7..4   Not used.
                                                          Bit 3..0   Picture Format.
                                                                     0x00 = Normal (4:3)
                                                                     0x01 = Custom
                                                                     0x02 = Real (1:1)
                                                                     0x03 = Full
                                                                     0x04 = 21:9
                                                                     0x05 = Dynamic
                                                                     0x06 = 16:9

Special Note:-

DATA [1] value 0x05 = Dynamic not supported in 2016 Dragon 1.0 (see platform list).

* For further explanations, please see section 6.2.3 – Message-Set.

Example: Current Picture Format is Widescreen on Full Display (Display address 01)
 MsgSize Control Group               Data (0)    Data (0)      Checksum
 0x06       0x01         0x00        0x3B        0x03          0x3F


```

#### 5.2.3 Message-Set

```text

 Bytes           Bytes Description                 Bits          Description
 DATA[0]         0x3A = Picture Format –                         Command requests the display to set the specified
                 Set                                             picture format
 DATA[1]         Picture Format                    Bit 7..4      Not used.
                                                   Bit 3..0      Picture Format.
                                                                 0x00 = Normal
                                                                 0x01 = Custom
                                                                 0x02 = Real
                                                                 0x03 = Full
                                                                 0x04 = 21:9
                                                                 0x05 = Dynamic
                                                                 0x06 = 16:9





Special Note:-

DATA [1] value 0x05 = Dynamic not supported in 2016 Dragon 1.x (see platform list)

The display shall respond with NAV if it receives a Picture Format that is not relevant to its Display Aspect
Ratio.
The display shall ignore the [Picture Format – Set] if it receives a Picture Format that it cannot execute.

Example: Set Picture Format to Widescreen on Full Display (Display address 01)
 MsgSize Control Group               Data (0)     Data (0)     Checksum
 0x06        0x01        0x00        0x3A         0x03         0x3E

```

### 5.3 VGA video Parameters

```text
This command is used to control the VGA video parameters.
      Value in(0,10,20,30,40,50,60,70,80,90,100)
```

#### 5.3.1 Message-Get

```text

 Bytes            Bytes Description                       Bits      Description
 DATA[0]          0x39 = VGA Video                                  Command requests the display to report its VGA
                  Parameters – Get                                  current video parameters.

Example: (Display address 01)
 MsgSize Control Group               Data (0)      Checksum
 0x05        0x01        0x00        0x39          0x3D



```

#### 5.3.2 Message-Report

```text

 Bytes           Bytes Description                   Bits     Description
 DATA[0]         0x39 = VGA Video                             Command reports to the host controller the VGA
                 Parameters – Report                          current video parameters of the display.
 DATA[1]         Clock                                        0 to 100 (%) of the user selectable range of the display.
 DATA[2]         Clock Phase                                  0 to 100 (%) of the user selectable range of the display.
 DATA[3]         H. position                                  0 to 100 (%) of the user selectable range of the display.
 DATA[4]         V. Position                                  0 to 100 (%) of the user selectable range of the display.

Example: All VGA video parameters are set to 55 % (0x37) (Display address 01)
 MsgSize Control Group               Data (0)    Data (1)     Data (2)    Data (3)       Data (4)    Checksum
 0x09        0x01       0x00         0x39        0x37         0x37        0x37           0x37        0x31



```

#### 5.3.4 Message-Set

```text

 Bytes           Bytes Description                   Bits      Description
 DATA[0]         0x38 = VGA Video                              Command to change the VGA current video parameters
                 Parameters – Set
 DATA[1]         Clock(Invalid)                                0 to 100 (%) of the user selectable range of the display.
 DATA[2]         Clock Phase(Invalid)                          0 to 100 (%) of the user selectable range of the display.
 DATA[3]         H. position                                   0 to 100 (%) of the user selectable range of the display.
 DATA[4]         V. Position                                   0 to 100 (%) of the user selectable range of the display.

Example: Set all VGA video parameters to 0x37 (55 %) (Display address 01)
 MsgSize Control Group               Data (0)    Data (1)     Data (2)    Data (3)       Data (4)    Checksum
 0x09        0x01        0x00        0x38        0x37         0x37        0x37           0x37        0x30





```

### 5.4 Picture-in-Picture (PIP)

```text

This command is used to control PIP on/off with different Quadrants of the screen.

```

#### 5.4.1 Message-Get

```text

      Bytes        Bytes Description                       Bits        Description
      DATA[0]      0x3D = Picture-in-Picture –                         Command requests the display to get the
                    Get                                                specified PIP settings.

   Example: Get PIP setting (Display address 01)
    MsgSize Control Group               Data (0)       Checksum
    0x05      0x01        0x00          0x3D           0x39

```

#### 5.4.2 Message-Report

```text

      Bytes           Bytes Description                     Bits        Description
      DATA[0]         0x3D = Picture-in-Picture –                       Command reports to the host controller the
                       Report                                           current PIP settings.
      DATA[1]         Picture-in-Picture                    Bit 7..4    ( reserved, default 0 )
                                                            Bit 0..3    0x00 = Off
                                                                        0x01 = On (PIP)
                                                                        0x02 = POP
                                                                        0x03 = Quick swap
                                                                        0x04 = PBP 2win
                                                                        0x05 = PBP 3win
                                                                        0x06 = PBP 4win
                                                                        0x07 = PBP 3win-1
                                                                        0x08 = PBP 3win-2
                                                                        0x09 = PBP 4win-1
                                                                        0x0A = SICP (Custom)

                                                                        Note: platform list
                                                                        1.Eagle 1.3 platform only support (0x00 / 0x01)
                                                                        2.HIMALAYA 1.0 & 1.2 platform only support
                                                                        (0x00 ~0x06)
                                                                        3.DRAGON 1.0, 1.5, 1.6 platform only support
                                                                        (0x00 / 0x01/ 0x03 /0x04 / 0x0A)
                                                                        4.Phoenix platform doesn’t support PIP.
```

## 5 HIMALAYA 2.0 doesn’t support 0X02

```text
      DATA[2]         Additional PIP parameters             Bit 7..3    ( reserved, default 0 )
                                                            Bit 2..0    Position of the PIP window:
                                                                        0x00 = position 0 (typically bottom-left)
                                                                        0x01 = position 1 (typically top-left)
                                                                        0x02 = position 2 (typically top-right)
                                                                        0x03 = position 3 (typically bottom-right)
                                                                        0x04 = position 4 (typically center).
      DATA[3]                                                           ( reserved, default 0 )
      DATA[4]                                                           ( reserved, default 0 )

   Example: Current PIP setting is enabling and located at position 2 (Display address 01)
    MsgSize Control Group                Data (0)     Data (1)      Data (2)     Data (3)     Data (4)   Checksum
    0x09      0x01        0x00           0x3D         0x01          0x02         0x00         0x00       0x36





```

#### 5.4.3 Message-Set

```text

 Bytes        Bytes Description                      Bits        Description
 DATA[0]      0x3C = Picture-in-Picture –                        Command requests the display to set the
              Set                                                specified PIP settings.
 DATA[1]      Picture-in-Picture                     Bit 7..4    ( reserved, default 0 )
                                                     Bit 0..3    0x00 = Off
                                                                 0x01 = On (PIP)
                                                                 0x02 = POP
                                                                 0x03 = Quick swap
                                                                 0x04 = PBP 2win
                                                                 0x05 = PBP 3win
                                                                 0x06 = PBP 4win
                                                                 0x07 = PBP 3win-1
                                                                 0x08 = PBP 3win-2
                                                                 0x09 = PBP 4win-1
                                                                 0x0A = SICP (Custom)

                                                                 Note: platform list
                                                                 1.Eagle 1.3 platform only support (0x00 / 0x01)
                                                                 2.HIMALAYA 1.0 & 1.2 platform only support
                                                                 (0x00 ~0x06)
                                                                 3.DRAGON 1.0, 1.5, 1.6 platform only support
                                                                 (0x00 / 0x01/ 0x03 /0x04 / 0x0A)
                                                                 4.Phoenix platform doesn’t support PIP.
```

## 5 HIMALAYA 2.0 doesn’t support 0X02

```text
 DATA[2]      Additional PIP parameters              Bit 7..2    ( reserved, default 0 )
                                                     Bit 1..0    Position of the PIP window:
                                                                 0x00 = position 0 (typically bottom-left)
                                                                 0x01 = position 1 (typically top-left)
                                                                 0x02 = position 2 (typically top-right)
                                                                 0x03 = position 3 (typically bottom-right)
                                                                 0x04 = position 4 (typically center).
 DATA[3]                                                         ( reserved, default 0 )
 DATA[4]                                                         ( reserved, default 0 )

Example: Set PIP ON, top-right (Display address 01)
 MsgSize       Control Group             Data (0) Data (1)      Data (2)    Data (3)   Data (4)   Checksum
 0x09          0x01         0x00         0x3C       0x01        0x02        0x00       0x00       0x37





```

#### 5.4.4 Picture-In-Picture (PIP) Source

```text

This command is used to control the PIP source settings for each display quadrant on the screen.

Himalaya 1.x & 2.0 platform carries the following PIP Design only
 Example: If display resolution is 4K2K, user can select input source for each Full HD quadrant.


         Q1 (main)                       Q2


           Q3                            Q4




PIP Set/Get can only change input source for Q2, Q3, and Q4 individually by following the commands
below.

Dragon 1.x platform and older platforms (Eagle) carries the following PIP Design only.



     Main Source


                                      PIP source




```

##### 5.4.4.1 Message-Get PIP source

```text


 Bytes          Bytes Description                  Bits    Description
                                                           Command requests the display to report its current
 DATA[0]        0x85 = PIP Source – Get
                                                           PIP source setting.

This command is used to get the source for the PIP window when PIP feature is activated.

Example: Get PIP source setting (Display address 01)
 MsgSize Control Group                Data (0)    Checksum
 0x05      0x01       0x00            0x85        0x81

```

##### 5.4.4.2 Message-Report PIP source

```text

Dragon 1.x & 1.6 platform DATA[3] & DATA[4] are not
available.

 Return bytes are DATA[0]~DATA[2]+Checksum byte.

 Bytes          Bytes Description                  Bits    Description
                                                           Command requests the display to report its current
 DATA[0]        0x85 = PIP Source – Get
                                                           PIP source setting.
                                                           0xFD = Input Source (normal state)
 DATA[1]        Source Type
                                                           0xFE = Reserved for smartcard
                                                           If Source types == 0xFD then…

 DATA[2]        Q2 Source Number                           0x01 = VIDEO
                                                           0x02 = S-VIDEO
                                                           0x03 = COMPONENT
                                                           0x04 = CVI 2 (not applicable)



                                                 0x05 = VGA
                                                 0x06 = HDMI 2
                                                 0x07 = Display Port 2
                                                 0x08 = USB 2
                                                 0x09 = Card DVI-D
                                                 0x0A = Display Port
                                                 0x0B= Card OPS
                                                 0x0C = USB
                                                 0x0D= HDMI
                                                 0x0E= DVI-D
                                                 0x0F = HDMI3
                                                 0x10= BROWSER
                                                 0x11= SMARTCMS
                                                 0X12= DMS (Digital Media Server)
                                                 0x13= INTERNAL STORAGE
                                                 0x14= Reserved
                                                 0x15= Reserved
                                                 0x16= Media Player
                                                 0x17= PDF Player
                                                 0x18= Custom
                                                 0x19 = reserved
                                                 0x1A = VGA2
                                                 0x1B = VGA3
                                                 0x1C = IWB
                                                 If Source type == 0xFD then…

                                                 0x01 = VIDEO
                                                 0x02 = S-VIDEO
                                                 0x03 = COMPONENT
                                                 0x04 = CVI 2 (not applicable)
                                                 0x05 = VGA
                                                 0x06 = HDMI 2
                                                 0x07 = Display Port 2
                                                 0x08 = USB 2
                                                 0x09 = Card DVI-D
                                                 0x0A = Display Port
                                                 0x0B= Card OPS
DATA[3]   Q3 Source Number
                                                 0x0C = USB
                                                 0x0D= HDMI
                                                 0x0E= DVI-D
                                                 0x0F = HDMI3
                                                 0x10= BROWSER
                                                 0x11= SMARTCMS
                                                 0X12= DMS (Digital Media Server)
                                                 0x13= INTERNAL STORAGE
                                                 0x14= Reserved
                                                 0x15= Reserved
                                                 0x16= Media Player
                                                 0x17= PDF Player
                                                 0x18= Custom
                                                 0x19 = reserved
                                                 0x1A = VGA2
                                                 0x1B = VGA3
                                                 0x1C = IWB





                                                 If Source type == 0xFD then…

                                                 0x01 = VIDEO
                                                 0x02 = S-VIDEO
                                                 0x03 = COMPONENT
                                                 0x04 = CVI 2 (not applicable)
DATA[4]   Q4 Source Number
                                                 0x05 = VGA
                                                 0x06 = HDMI 2
                                                 0x07 = Display Port 2
                                                 0x08 = USB 2
                                                 0x09 = Card DVI-D
                                                 0x0A = Display Port





                                                           0x0B= Card OPS
                                                           0x0C = USB
                                                           0x0D= HDMI
                                                           0x0E= DVI-D
                                                           0x0F = HDMI3
                                                           0x10= BROWSER
                                                           0x11= SMARTCMS
                                                           0X12= DMS (Digital Media Server)
                                                           0x13= INTERNAL STORAGE
                                                           0x14= Reserved
                                                           0x15= Reserved
                                                           0x16= Media Player
                                                           0x17= PDF Player
                                                           0x18= Custom
                                                           0x19 = reserved
                                                           0x1A = VGA2
                                                           0x1B = VGA3
                                                           0x1C = IWB


Example: Get PIP source report (Display address 01, Q2 Video, Q3 VGA, Q4 DVI-D)

 MsgSize   Control Group            Data (0)      Data (1)     Data (2)      Data(3)    Data(4)       Checksum
 0x09      0x01    0x00             0x85          0xFD         0x01          0x05       0x0E          0x7A

```

##### 5.4.4.3 Message-Set

```text

This is the PIP source selection command

Dragon 1.x & 2.0 platform – DATA[3] & DATA[4] may not
be send.
Return bytes are DATA[0]~DATA[2]+Checksum byte.

 Bytes         Bytes Description                 Bits      Description
                                                           Command requests the display to set the specified PIP
 DATA[0]       0x84 = PIP Source – Set
                                                           source.
                                                           0xFD = Input Source (normal state)
 DATA[1]       Source Type
                                                           0xFE = Reserved for smartcard





                                                 If Source type == 0xFD then…

                                                 0x01 = VIDEO
                                                 0x02 = S-VIDEO
                                                 0x03 = COMPONENT
                                                 0x04 = CVI 2 (not applicable)
                                                 0x05 = VGA
                                                 0x06 = HDMI 2
                                                 0x07 = Display Port 2
                                                 0x08 = USB 2
                                                 0x09 = Card DVI-D
                                                 0x0A = Display Port
DATA[2]   Q2 Source Number
                                                 0x0B= Card OPS
                                                 0x0C = USB
                                                 0x0D= HDMI
                                                 0x0E= DVI-D
                                                 0x0F = HDMI3
                                                 0x10= BROWSER
                                                 0x11= SMARTCMS
                                                 0X12= DMS (Digital Media Server)
                                                 0x13= INTERNAL STORAGE
                                                 0x14= Reserved
                                                 0x15= Reserved
                                                 0x16= Media Player





                                                  0x17= PDF Player
                                                  0x18= Custom
                                                  0x19 = reserved
                                                  0x1A = VGA2
                                                  0x1B = VGA3
                                                  0x1C = IWB
                                                  If Source type == 0xFD then…

                                                  0x01 = VIDEO
                                                  0x02 = S-VIDEO
                                                  0x03 = COMPONENT
                                                  0x04 = CVI 2 (not applicable)
                                                  0x05 = VGA
                                                  0x06 = HDMI 2
                                                  0x07 = Display Port 2
                                                  0x08 = USB 2
                                                  0x09 = Card DVI-D
                                                  0x0A = Display Port
                                                  0x0B= Card OPS
DATA[3]   Q3 Source Number
                                                  0x0C = USB
                                                  0x0D= HDMI
                                                  0x0E= DVI-D
                                                  0x0F = HDMI3
                                                  0x10= BROWSER
                                                  0x11= SMARTCMS
                                                  0X12= DMS (Digital Media Server)
                                                  0x13= INTERNAL STORAGE
                                                  0x14= Reserved
                                                  0x15= Reserved
                                                  0x16= Media Player
                                                  0x17= PDF Player
                                                  0x18= Custom
                                                  0x19 = reserved
                                                  0x1A = VGA2
                                                  0x1B = VGA3
                                                  0x1C = IWB
                                                  If Source type == 0xFD then…

                                                  0x01 = VIDEO
                                                  0x02 = S-VIDEO
                                                  0x03 = COMPONENT
                                                  0x04 = CVI 2 (not applicable)
                                                  0x05 = VGA
                                                  0x06 = HDMI 2
                                                  0x07 = Display Port 2
                                                  0x08 = USB 2
                                                  0x09 = Card DVI-D
                                                  0x0A = Display Port
                                                  0x0B= Card OPS
DATA[4]   Q4 Source Number
                                                  0x0C = USB
                                                  0x0D= HDMI
                                                  0x0E= DVI-D
                                                  0x0F = HDMI3
                                                  0x10= BROWSER
                                                  0x11= SMARTCMS
                                                  0X12= DMS (Digital Media Server)
                                                  0x13= INTERNAL STORAGE
                                                  0x14= Reserved
                                                  0x15= Reserved
                                                  0x16= Media Player
                                                  0x17= PDF Player
                                                  0x18= Custom
                                                  0x19 = reserved

                                                          0x1A = VGA2
                                                          0x1B = VGA3
                                                          0x1C = IWB




 This command is used to select the source for the PIP window before the PIP feature is activated.

 Example: Set source PIP (Display address 01, Q2 Video, Q3 VGA, Q4 DVI-D)

     MsgSize    Control    Group        Data (0)    Data (1)      Data (2)       Data(3)   Data(4)   Checksum
     0x09       0x01       0x00         0x84        0xFD          0x01           0x05      0x0E      0x7B
Example :
        set PIP source to DP:      07 01 00 84 FD 0A 75
        set PIP source to VGA:     07 01 00 84 FD 05 7A





```

## 6 MESSAGES – AUDIO

### 6.1 Volume

```text

 This command is used to set/get the volume of speaker out and audio out as it is defined as below.

```

#### 6.1.1 Message-Get current volume level speakers and audio out

```text

  Bytes         Bytes Description          Bits      Description
  DATA[0]       0x45 = Volume –                      Command requests the display to report its current Volume
                Get                                  level

 The interface to set Software must be such that they also modify the variables representing these current
 parameters. To mute the display, set Volume = 0. This command does not overwrite the system mute status of
 the display.

 Example: (Display address 01)
  MsgSize Control Group               Data (0)     Checksum
  0x05        0x01        0x00        0x45         0x41

```

#### 6.1.2 Message-Report current volume level speakers and audio out

```text


 This command can get current volume level for speaker & audio out individually. Valid values range from 0x00
 (lowest 0% volume) through 0x64 (highest – 100% volume).
 Some platforms don’t have variable audio out and the report (Ack) is different, see the special note remark in this
 chapter.



  Bytes         Bytes Description                 Bits    Description
  DATA[0]       0x45 = Volume – Report                    Command reports current Volume level
  DATA[1]       Speaker Out Volume level                  0 to 100 (%) of the user selectable range of the display.
  DATA[2]       Audio Out Volume level                    0 to 100 (%) of the user selectable range of the display.


  DATA[1]       Speaker Out Volume level                  0 to 60 (%) of the user selectable range of the display.
  DATA[2]       Audio Out Volume level                    0 to 60 (%) of the user selectable range of the display.

       Example: Current Display settings: Volume:22% (0x16) for Speak out and 10%(0x0A) for Audio out (Display
       address 01)
       MsgSize Control Group                  Data      Data        Data        Checksum
                                              (0)       (1)         (2)
        0x07       0x01         0x00            0x45    0x16        0x0A          0x5F

SPECIAL NOTE:
       HIMALAYA 1.0 & 1.2 and Eagle (platforms) don’t have variable audio out and data(2) is not received.
       See below example: Data(1) is the speaker out volume level 100% ( 0x64).

       MsgSize     Control     Group       Data          Data                Checksum
                                           (0)           (1)
        0x06       0x01        0x01          0x45        0x64                    0x27


```

#### 6.1.3 Message-Set current volume level speakers and audio out

```text

This command can set volume level for speaker & audio out individually. Valid values range from 0x00 (lowest 0%
volume) through 0x64 (highest – 100% volume). If DATA [1] or [2] are higher than 0x64 no action will be taken in the
display and current volume level will be maintained without any effect.
Some platforms don’t have variable audio out and the command is different, see the special note remark in this chapter.



  Bytes         Bytes Description                 Bits    Description

  DATA[0]         0x44 = Volume – Set
  DATA[1]         Speaker Out Volume level                   0 to 100 (%) of the user selectable range of the display.
  DATA[2]         Audio Out Volume level                     0 to 100 (%) of the user selectable range of the display.



    DATA[1]          Speaker Out Volume level                  0 to 60 (%) of the user selectable range of the display.
    DATA[2]          Audio Out Volume level                    0 to 60 (%) of the user selectable range of the display.

         Example: Set the Display Volume to 22% (0x16) for Speaker out and 50 %(0x32) for Audio out (Display
   address 01)
          MsgSize Control Group               Data       Data        Data        Checksum
                                              (0)        (1)         (2)
            0x07        0x01         0x00       0x44        0x16        0x32       0x66

SPECIAL NOTE:
       Himalaya 1 & 1.2 and Eagle (platforms) don’t have variable audio out and data(2) may not be sent.
       See below example: Data(1) is the speaker out volume level 22% ( 0x16).


            MsgSize Control         Group        Data(0) Data(1) Checksum

              0x06        0x01         0x00        0x44        0x16          0x55



```

#### 6.1.4 Message-Set Volume level – step up or step down for Speaker out or Audio Out

```text

   This command can set volume level in step up or step down a count for speaker & audio out individually.
   DATA [1] or [2] must supply “0x00” to count down a step and supply “0x01” to count up a step of volume.
   All other values supplied to DATA [1] or [2] will get no “response” from the display.
   Some platforms don’t have variable audio out and the command is different, see the special note remark in this
   chapter.


    Bytes            Bytes Description               Bits      Description
    DATA[0]          0x41 = Volume +/- – Set                   Adjust volume up/down
    DATA[1]          Speaker Out.                              0 : down, 1: up, 2: no change*
    DATA[2]          Audio Out.                                0 : down, 1: up, 2: no change*

               * “2 no change” will only work in below platforms:
                    Dragon 1.0 : from firmware phase 3 (after V1.3XX ).
                    Dragon 1.5 : from firmware phase 2 (after V1.2XX).
                    Dragon 1.6: from start production
                    Himalay 2.0 : from start production
                    and new platforms

   Example: Set the Display Volume up (0x01) (Display address 01)
    MsgSize Control Group               Data (0)    Data (1)    Data(2)              Checksum
    0x07        0x01        0x00        0x41        0x01        0x00                 0x46


           SPECIAL NOTE:
           Himalaya 1 & 1.2 and Eagle (platforms)don’t have variable audio out and data(2) may not be sent.
           See below example: Data(1) is the speaker out volume.


            MsgSize Control         Group        Data(0) Data(1) Checksum Volume

              0x06        0x01         0x00        0x41        0x00          0x46          Step -
              0x06        0x01         0x00        0x41        0x01          0x47          Step +

```

#### 6.1.5 Volume Limit – Speaker out

```text

 This command is used to set or get the volume limit (minimum, maximum and switch on volume) for speaker
 out
```

##### 6.1.5.1 Message-Set Volume Limit

```text

  Bytes        Bytes Description          Bits Description
   DATA[0]      0xB8 = Volume Limits– Set      The 3 values must conform to the rule :
                for Speaker out                Min <= Switch On <= Max
    DATA[1]     Minimum Volume                 0 to 100 (%) of the user selectable range of the display.
    DATA[2]     Maximum Volume                 0 to 100 (%) of the user selectable range of the display.
    DATA[3]     Switch On Volume               0 to 100 (%) of the user selectable range of the display.

 Example: Set the Display Speaker out to the following: 10% (0x0A), 77% (0x4D), 50% (0x32) (Display address 01)
   MsgSize       Control Group             Data (0)      Data (1)    Data (2)     Data (3)   Checksum
   0x08          0x01       0x00           0xB8          0x0A        0x4D         0x32       0xC4

```

##### 6.1.5.2 Message-Get Volume Limit

```text

```

**2.** Bytes        Bytes Description                 Bits Description

```text
    DATA[0]            0xB6 = Volume Limits–                 The 3 values must conform to the rule :
                       Get for Speaker out                   Min <= Switch On <= Max
    DATA[1]            Minimum Volume                        0 to 100 (%) of the user selectable range of the
                                                             display.
    DATA[2]            Maximum Volume                        0 to 100 (%) of the user selectable range of the
                                                             display.
    DATA[3]            Switch On Volume                      0 to 100 (%) of the user selectable range of the
                                                             display.





Example: Get the Speaker out values as follows: 10% (0x0A), 77% (0x4D), 50% (0x32) (Display address 01)
  MsgSize      Control Group              Data (0)    Data (1)    Data (2)     Data (3)     Checksum
  0x08         0x01       0x00            0xB6        0x0A        0x4D         0x32         0xB0

```

#### 6.1.6 Volume Limit – Audio out

```text

This command is used to set or get the volume limit (minimum, maximum and switch on volume) for Audio
out

```

##### 6.1.6.1 Message-Set Volume Limit – Audio out

```text

 Bytes          Bytes Description          Bits Description
  DATA[0]        0xB9 = Volume Limits– Set      The 3 values must conform to the rule :
                 for Audio out.                 Min <= Switch On <= Max
  DATA[1]        Minimum Volume                 0 to 100 (%) of the user selectable range of the display.
  DATA[2]        Maximum Volume                 0 to 100 (%) of the user selectable range of the display.
  DATA[3]        Switch On Volume               0 to 100 (%) of the user selectable range of the display.

SPECIAL NOTE:
      Following DATA [1], DATA [2], DATA [3], applicable for Phoenix 2.0 platform only (year 2015
      BDLxx70EL/BDLxx90VL/BDLxx30QL/BDLxx35QL)

 DATA[1]        Minimum Volume                          0 to 60 (%) of the user selectable range of the display.
 DATA[2]        Maximum Volume                          0 to 60 (%) of the user selectable range of the display.
 DATA[3]        Switch On Volume                        0 to 60 (%) of the user selectable range of the display.

Example: Set the Display Audio out to the following: 10% (0x0A), 77% (0x4D), 50% (0x32) (Display address 01)
  MsgSize       Control Group              Data (0)     Data (1)   Data (2)     Data (3)     Checksum
  0x08          0x01       0x00            0xB9         0x0A       0x4D         0x32         0xC5

```

##### 6.1.6.2 Message-Get Volume Limit – Audio out

```text

 Bytes          Bytes Description          Bits Description
  DATA[0]        0xB7 = Volume Limits– Get      The 3 values must conform to the rule :
                 values for Audio out.          Min <= Switch On <= Max
  DATA[1]        Minimum Volume                 0 to 100 (%) of the user selectable range of the display.
  DATA[2]        Maximum Volume                 0 to 100 (%) of the user selectable range of the display.
  DATA[3]        Switch On Volume               0 to 100 (%) of the user selectable range of the display.

SPECIAL NOTE:
      Following DATA [1], DATA [2], DATA [3], applicable for Phoenix 2.0 platform only (year 2015
      BDLxx70EL/BDLxx90VL/BDLxx30QL/BDLxx35QL)

 DATA[1]        Minimum Volume                          0 to 60 (%) of the user selectable range of the display.
 DATA[2]        Maximum Volume                          0 to 60 (%) of the user selectable range of the display.
 DATA[3]        Switch On Volume                        0 to 60 (%) of the user selectable range of the display.

Example: Get the Display Audio out values as follows: 10% (0x0A), 77% (0x4D), 50% (0x32) (Display address 01)
  MsgSize      Control Group              Data (0)      Data (1)   Data (2)     Data (3)    Checksum
  0x08         0x01        0x00           0xB7          0x0A       0x4D         0x32        0xCB

```

#### 6.1.7 Audio Parameters

```text

This command is used to set/get the audio parameters as it is defined as below.

```

##### 6.1.7.1 Message-Get

```text



 Bytes         Bytes Description                       Bits        Description
 DATA[0]       0x43 = Audio Parameters –                           Command requests the display to report its current
               Get                                                 audio parameters

Example: (Display address 01)
 MsgSize      Control Group            Data (0)     Checksum
 0x05         0x01        0x00         0x43         0x47

```

##### 6.1.7.2 Message-Report

```text

 Bytes         Bytes Description                            Bits      Description
 DATA[0]       0x43 = Audio Parameters –                              Command reports Audio Parameters
               Report
 DATA[1]       Treble.                                                0 to 100 (%) of the user selectable range of the
                                                                      display.
 DATA[2]       Bass.                                                  0 to 100 (%) of the user selectable range of the
                                                                      display.


SPECIAL NOTE:
      Following DATA [1], DATA [2] applicable for Phoenix 2.0 platform only (year 2015
      BDLxx70EL/BDLxx90VL/BDLxx30QL/BDLxx35QL)

 DATA[1]       Treble.                                                -8 to 8 are the boundaries of the user selectable
                                                                      range of the display.
 DATA[2]       Bass.                                                  -8 to 8 are the boundaries of the user selectable
                                                                      range of the display.


Example: Current Display settings: Treble: 80% (0x50), Bass: 93% (0x5D) (Display address 01)
 MsgSize      Control Group             Data (0)    Data (1)    Data (2)    Checksum
 0x07         0x01        0x00          0x43        0x50        0x5D        0x48

```

##### 6.1.7.3 Message-Set

```text

 Bytes         Bytes Description                       Bits        Description
 DATA[0]       0x42 = Audio Parameters –                           Command to change the Audio Parameters of the
               Set                                                 display
 DATA[1]       Treble.                                             0 to 100 (%) of the user selectable range of the display.
 DATA[2]       Bass.                                               0 to 100 (%) of the user selectable range of the display.

         SPECIAL NOTE:
         Following DATA [1], DATA [2] applicable for Phoenix 2.0 platform only (year 2015
         BDLxx70EL/BDLxx90VL/BDLxx30QL/BDLxx35QL)

 DATA[1]       Treble.                                                -8 to 8 are the boundaries of the user selectable
                                                                      range of the display.
 DATA[2]       Bass.                                                  -8 to 8 are the boundaries of the user selectable
                                                                      range of the display.

         SPECIAL NOTE: Following table applicable for Phoenix 2.0 platform only (year 2015
         BDLxx70EL/BDLxx90VL/BDLxx30QL/BDLxx35QL)

      The value (-8) ～ (-1)
         -8         -7         -6          -5          -4            -3         -2         -1



             0xF8        0xF9      0xFA        0xFB         0xFC       0xFD        0xFE     0xFF

 The interface to set Software must be such that they modify the variables representing these current
 parameters

 Example: Set the Display to the fallowing: Treble: 77% (0x4D), Bass: 77% (0x4D) (Display address 01)
  MsgSize      Control Group             Data (0)     Data (1)    Data (2)    Checksum
  0x07         0x01         0x00         0x42         0x4D        0x4D        0x44

```

#### 6.1.8 Volume mute

```text

               This command mute the volume of the internal speakers and audio out.
               The command is available from firmware version : TBC x.xx on platforms TBC


```

##### 6.1.8.1 Get volume mute

```text
     Bytes      Bytes Description                  Bits    Description
     DATA[0]    0x46 = Volume mute                         Command report current volume mute status
                – Get

                    Example : get volume mute status
     MsgSize        Control Group         Data (0)   checksum
     0x05           0x01       0x00       0x46       0x42


```

##### 6.1.8.2 Message-Report

```text
     Bytes      Bytes Description                  Bits    Description
     DATA[0]    0x46 = Volume mute                         Command report current volume mute status
                – Get
     DATA[1]                                               0x01 = mute on
                                                           0x00= mute off


                    Example: current volume mute is on
     MsgSize        Control Group          Data (0)    Data (1)       checksum
     0x06           0x01      0x00         0x46        0x01           0x40


```

##### 6.1.8.3 Set volume mute

```text

               The command is available from firmware version : TBC x.xx on platforms TBC


     Bytes            Bytes Description            Bits    Description
     DATA[0]          0x47 = Volume mute                   Command set current volume mute
                      – Set
     DATA[1]                                               0x01 = mute on
                                                           0x00= mute off



                    Example: set volume mute off

     MsgSize        Control     Group      Data (0)       Data (1)    checksum
     0x06           0x01        0x00       0x47           0x00        0x40


```

## 7 MISCELLANEOUS

```text


```

### 7.1 Operating Hours

```text

The command is used to record the working hours of the display.

```

#### 7.1.1 Message-Get

```text

 Bytes        Bytes Description          Bits      Description
 DATA[0]      0x0F = Misc. Info –                  Command requests the display to report from miscellaneous
              Get                                  information parameters
 DATA[1]      Item                                 0x02 = Operating Hours
                                                   (All other values are reserved)

Example: (Display address 01)
 MsgSize Control Group             Data (0)      Data (1)     Checksum
 0x06        0x01        0x00      0x0F          0x02         0x0A

```

#### 7.1.2 Message-Report

```text

 Bytes        Bytes Description                 Bits    Description
 DATA[0]      0x0F = Misc. Info –                       Command reports current Operating Hours
              Report
 DATA[1]      Operating Hours
 to                                                     DATA [1] and DATA [2] form the MS Byte and LSByte,
 DATA[2]                                                respectively, of the 16-bit-wide Operational Hours value.


Example: Current Display Operation Hours counter value (Display address 01)
 MsgSize Control Group              Data (0)     Data (1)     Data (2)    Checksum
 0x07       0x01         0x00       0x0F         0x4D         0x00        0x44

```

### 7.2 Power Saving Mode

```text

This command is used for dimming back light power consumption control. Different levels of power
consumptions can be achieved by using this command.

```

#### 7.2.1 Message-Get

```text

 Bytes        Bytes Description                 Bits   Description
 DATA[0]      0xDE = Smart Power –                     Command requests the display to get the specified Power
              Get                                      Saving Mode.

Example: Get the Smart Power Level (Display address 01)
 MsgSize Control Group              Data (0)     Checksum
 0x05       0x01       0x00         0xDE         0xDA





```

#### 7.2.2 Message-Report

```text

 Bytes          Bytes Description                Bits    Description
 DATA[0]        0xDE = Smart Power –                     Command reports Power Saving Mode Setting
                Report
 DATA[1]        Level of Smart Power                     0x00 = OFF
                control                                  0x01 = Low (defined to be same as OFF)
                                                         0x02 = Medium
                                                         0x03 = High

Example: Current Display settings: Power Saving Mode setting is Low (Display address 01)
 MsgSize Control Group                Data (0)    Data (1)      Checksum
 0x06       0x01       0x00           0xDE        0x01          0xD8

```

#### 7.2.3 Message-Set

```text

 Bytes         Bytes Description                 Bits    Description
 DATA[0]       0xDD = Smart Power –                      Command requests the display to set the specified Power
               Set                                       Saving Mode.
 DATA[1]       Level of Smart Power                      For the currently-defined Type = 0:
               control                                    0x00 = OFF         (no special action, default mode)
                                                          0x01 = Low         (defined to be same as OFF)
                                                          0x02 = Medium
                                                          0x03 = High        (highest power-saving mode)

Example: Set the Display to Medium Smart Power Level (Display address 01)
 MsgSize Control Group              Data (0)    Data (1)     Checksum
 0x06        0x01        0x00       0xDD        0x02         0xD8

Note1: This command controls the level of power-saving when the display is active-on.
Note2: Exactly how this feature is implemented, or whether it can be done at all, depends on the platform. It
      is possible that the picture quality might be compromised as a trade-off.

```

### 7.3 Auto Adjust

```text

This command works for VGA (host controller) video auto adjust.


```

#### 7.3.1 Message-Set

```text

 Bytes         Bytes Description                     Bits     Description
 DATA[0]       0x70 = Video Alignment –                       Command requests the display to        make       auto
               Set                                            adjustment on VGA Input source.
 DATA[1]       Item                                           0x40 = Auto Adjust
                                                              (* All other values are reserved *)
 DATA[2]                                                      ( reserved, default 0 )

Example: (Display address 01)
 MsgSize Control Group                Data (0)     Data (1)     Data (2)     Checksum
 0x07        0x01        0x00         0x70         0x40         0x00         0x36





```

### 7.4 Temperature Sensors

```text


Compare two sensor data and report higher value of the two sensors in 1 data byte for reporting.

```

#### 7.4.1 Message-Get

```text

 Bytes         Bytes Description                     Bits         Description
 DATA[0]       0x2F = Temperature Sensor                          Command requests the display to report its value of
               – Get                                              the temperature sensors (±3°C).

Example: (Display address 01)
 MsgSize Control Group              Data (0)     Checksum
 0x05        0x01        0x00       0x2F         0x2B


```

#### 7.4.2 Message-Report

```text

 Bytes         Bytes Description                           Bits      Description
 DATA[0]       0x2F = Temperature Sensor –                           Command reports Temperature sensor value
               Report
 DATA[1]       Temperature Sensor 1                                  0-100 in Celsius degrees represented in hex.
 DATA[2]       Temperature Sensor 2                                  0-100 in Celsius degrees represented in hex.

SPECIAL NOTE: 2016 Dragon 1.0 & 2.0 platform only supports DATA[I] only. DATA[2] value is invalid.

Example: Current Temp Sensor 1 read out: = 28°C (Display address 01)
         Current Temp Sensor 2 read out: = 31°C (Display address 02)

 MsgSize    Control     Group       Data (0)     Data (1)         Data (2)   Checksum
 0x06       0x01        0x00        0x2F         0x1C             0x1F       0x2B

```

### 7.5 Serial Code

```text

```

#### 7.5.1 Message-Get

```text

Bytes        Bytes Description                      Bits       Description
DATA[0]      0x15 = Serial Code Get                            Command requests the display to report its Serial Code
                                                               Number (Production code) 14 digits

Example: (Display address 01)
MsgSize      Control Group          Data (0)     Checksum
0x05         0x01        0x00       0x15         0x11

```

#### 7.5.2 Message-Report

```text

Bytes        Bytes Description                          Bits        Description
DATA[0]      0x15 = Serial Code – Report                            Command reports Serial Code
DATA[1]      1st Character                                          Character acc. ASCII character map (HEX)
DATA[2]      2nd Character
DATA[3]      3rd Character

DATA[14]     14th Character                                         Character acc. ASCII character map (HEX)

Example: Current Display settings: Serial Code = HA1A0917123456 (Display address 01)
MsgSize    Control Group Data (0) Data (1) Data (2) Data (3) Data (4)                       Data (5)   Data (6)     Data (7)
0x13       0x01        0x00         0x15       0x48     0x41     0x31       0x41            0x30       0x39         0x31





Data (8)   Data (9)    Data (10)   Data (11)     Data (12)     Data (13)     Data (14)   Checksum
0x37       0x31        0x32        0x33          0x34          0x35          0x36        0x76


```

### 7.6 Tiling

```text

The command is used to set/get the tiling status as it is defined as below. Tiling is basically splitting video
content to appear in more than one display. Video wall, is an example.


```

#### 7.6.1 Message-Get

```text

 Bytes          Bytes Description                      Bits         Description
 DATA[0]        0x23 = Tiling – Get                                 Command requests the display to report Tiling
                                                                    status.

Example: (Display address 01)
 MsgSize Control Group                Data (0)     Checksum
 0x05        0x01        0x00         0x23         0x27


```

#### 7.6.2 Message-Report

```text

 Bytes          Bytes Description                            Bits      Description
 DATA[0]        0x23 = Tiling – Report                                 Command reports Tiling Setting
 DATA[1]        Enable                                                 0x00 = No
                                                                       0x01 = Yes
 DATA[2]        Frame comp.                                            0x00 = No
                                                                       0x01 = Yes
 DATA[3]        Position                                               0x01 = position 1
                                                                       0x02 = position 2
                                                                       …
                                                                       See Note 1
 DATA[4]        V Monitors, H Monitors                                 0x00 = don’t care
                                                                       0x01 = V Monitors =1, H Monitors =1
                                                                       0x02 = V Monitors =1, H Monitors =2
                                                                       …
                                                                       See Note 2

Note 1:
(1) For Zero Bezel models, the maximum Position value is 150 (hexadecimal value is 0x96).
(2) For other models, the maximum Position value is 25 (hexadecimal value is 0x19).
(3) The Position is counted from left to right, then up to down in the Tiling Wall.
Example: See Figure 3 for the hexadecimal Position value in a 4x3 (H Monitors x V Monitors) Tiling Wall.
Example: See Figure 4 for the hexadecimal Position value in a 5x5 (H Monitors x V Monitors) Tiling Wall.
Example: See Figure 5 for the hexadecimal Position value in a 15x10 (H Monitors x V Monitors) Tiling Wall.

Note 2:
     (20) For Zero Bezel models, the maximum H Monitors are 15 and the maximum V Monitors are 10. The
          formulas for DATA [4], V Monitors, and H Monitors are as follows:
      H Monitors = MOD (Data [4], 15)         (Data [4] ÷ 15, take the remainder)
      V Monitors = INT (Data [4], 15) + 1      (Data [4] ÷ 15, take the quotient and plus one)
      Data [4] = (V Monitors – 1) x 15 + H Monitors
Example: If H Monitors = 12 and V Monitors = 6, the Data [4] value will be (6–1) x 15 + 12 = 87
(2) For other models, the maximum H Monitors and V Monitors are 5, and the formulas for DATA [4], V
Monitors, and H Monitors are as follows:
      H Monitors = MOD (Data [4], 5)        (Data [4] ÷ 5, take the remainder)
     V Monitors = INT (Data [4], 5) + 1      (Data [4] ÷ 5, take the quotient and plus one)





    Data [4] = (V Monitors – 1) x 5 + H Monitors
Example: If H Monitors = 4 and V Monitors = 3, the Data [4] value will be (3–1) x 5 + 4 = 14.



Example for BDL4675XU, Display address 01,
Set the display as follows:
Tiling enabled: Yes
Frame comp.: No
Position: 2
H Monitors: 3
V monitors: 2
Data [4] value will be: (2–1) x 15 + 3 = 18 (hex value: 0x12)
 MsgSize Control Group               Data[0]    Data (1) Data (2)            Data (3)   Data (4)   Checksum
 0x09         0x01          0x00     0x23       0x01        0x00             0x02       0x12       0x3A

Example for BDL4230E, Display address 01
Set the display as follows:
Tiling enabled: Yes
Frame comp.: No
Position: 2
H Monitors: 3
V monitors: 2
Data [4] value will be: (2–1) x 5 + 3 = 8
 MsgSize       Control Group          Data[0]    Data (1)     Data (2)       Data (3)   Data (4)   Checksum
 0x09          0x01         0x00      0x23       0x01         0x00           0x02       0x08       0x20

Figure 3. The hexadecimal Position value in a 4x3 (H Monitors x V Monitors) Tiling Wall.




Figure 4. The hexadecimal Position value in a 5x5 (H Monitors x V Monitors) Tiling Wall.




Figure 5. The hexadecimal Position value in a 15x10 (H Monitors x V Monitors) Tiling Wall.





```

#### 7.6.3 Message-Set

```text

 Bytes        Bytes Description                          Bits       Description
 DATA[0]      0x22 = Tiling – Set                                   Command reports Tiling Setting
 DATA[1]      Enable                                                0x00 = No
                                                                    0x01 = Yes
 DATA[2]      Frame comp.                                           0x00 = No
                                                                    0x01 = Yes
                                                                    0x02 = don’t overwrite (keep previous value)
 DATA[3]      Position                                              0x00 = don’t overwrite (keep previous value)
                                                                    0x01 = position 1
                                                                    0x02 = position 2
                                                                    …
                                                                    See Note 1 at 8.6.2
 DATA[4]      V Monitors, H Monitors                                0x00 = don’t overwrite (keep previous value)
                                                                    0x01 = V Monitors =1, H Monitors =1
                                                                    0x02 = V Monitors =1, H Monitors =2
                                                                    …
                                                                    See Note 2 at 8.6.2

Example for BDL4675XU, Display address: 01
Set the display as follows:
Tiling enabled: Yes
Frame comp.: No
Position: 2
H Monitors: 3
V monitors: 2

Data [4] value will be (2–1) x 15 + 3 = 18 (hex value: 0x12)
 MsgSize     Control Group           Data[0]    Data (1) Data (2)           Data (3)     Data (4)     Checksum
 0x09        0x01        0x00        0x22       0x01        0x00            0x02         0x12         0x3B

Example for BDL4675XU, Display address 01
Set the display as follows:
Tiling enabled: Yes
Frame comp., Position, H Monitors, V Monitors: Keep as before
 MsgSize Control Group               Data[0]      Data (1) Data (2)         Data (3)     Data (4)      Checksum
 0x09         0x01          0x00     0x22         0x01        0x02          0x00         0x00          0x29

Example for BDL4230E, Display address 01
Set the display as follows:
Tiling enabled: Yes
Frame comp.: No
Position: 2
H Monitors: 3
V monitors: 2
 MsgSize       Control Group       Data[0]      Data (1)        Data (2)    Data (3)     Data (4)     Checksum
 0x09          0x01         0x00   0x22         0x01            0x00        0x02         0x08         0x21

 Example for BDL4230E, Display address 01
 Set the display as follows:
 Tiling enabled: Yes
 Frame comp., Position, H Monitors, V Monitors: Keep as before
  MsgSize Control Group               Data[0]      Data (1) Data (2)                Data (3)         Data (4)         Checksum
  0x09         0x01          0x00     0x22         0x01        0x02                 0x00             0x00             0x29


```

### 7.7 AnyTile (Canvas)

```text

Tiling can be set beyond the OSD menu options and therefore can be flexible to a certain extent allowable by
command thresholds.
 SPECIAL NOTE: only 2016 Dragon 1.x, Dragon 1.6 & Himalaya2.0 platform supports these commands
 Those commands only work if the the canvas tiling is activated from the admin menu.



```

#### 7.7.1 AnyTile Assign Group ID and monitor ID

```text

Change the monitor ID & Group ID of the monitor, this command is only working via IP connection and not via
RS232.

  Bytes              Bytes Description                             Bits     Description
  DATA[0]            0xC0 = Set Group ID & Monitor ID                       Change Group ID and monitor ID of the monitor
                     (this command only works via IP)
  DATA[1]            Monitor ID                                             Monitor ID

  DATA[2]            Group ID                                               Group ID


```

#### 7.7.2 Display monitor ID

```text

  Bytes              Bytes Description                             Bits     Description
  DATA[0]            0x4C = Display monitor ID – Set                        Enable or Disable displaying monitor ID on the monitor

  DATA[1]            Monitor ID




```

#### 7.7.3 AnyTile –Report

```text


  Bytes              Bytes Description                             Bits     Description
  DATA[0]            0x4A = Custom Tiling – Report                          Command reports Custom Tiling Setting
  DATA[1]            Enable                                                 0x00 = No
                                                                            0x01 = Yes
  DATA[2]            Rotation (lsb)                                         0 degree > lsb= 0x00 & msb= 0x00
                                                                            90 degree > lsb= 0x5A & msb= 0x00
  DATA[3]            Rotation (msb)                                         270 degree > lsb= 0x0E & msb= 0x10

  DATA[4]            Input H Start(lsb)                                     H Start of captured input picture(lsb).
  DATA[5]            Input H Start(msb)                                     H Start of captured input picture(msb).
  DATA[6]            Input V Start(lsb)                                     V Start of captured input picture(lsb).
  DATA[7]            Input V Start(msb)                                     V Start of captured input picture(msb).
  DATA[8]            Input H Size(lsb)                                      H Size of captured input picture(lsb).
  DATA[9]            Input H Size(msb)                                      H Size of captured input picture(msb).
  DATA[10]           Input V Size(lsb)                                      V Size of captured input picture(lsb).
  DATA[11]           Input V Size(msb                                       V Size of captured input picture(msb).


Data[4] to Data[11] is the pixel value in hex, max value depends of the panel.
If FHD : max = 1920/1080

```

#### 7.7.4 AnyTile Set

```text


 Bytes             Bytes Description                              Bits     Description
 DATA[0]           0x4B = Custom Tiling – Report                           Command reports Custom Tiling Setting
 DATA[1]           Enable                                                  0x00 = No
                                                                           0x01 = Yes
 DATA[2]           Rotation (lsb)                                          0 degree
                                                                           90 degree
 DATA[3]           Rotation (msb)                                          270 degree

 DATA[4]           Input H Start(lsb)                                      H Start of captured input picture(lsb).
 DATA[5]           Input H Start(msb)                                      H Start of captured input picture(msb).
 DATA[6]           Input V Start(lsb)                                      V Start of captured input picture(lsb).
 DATA[7]           Input V Start(msb)                                      V Start of captured input picture(msb).
 DATA[8]           Input H Size(lsb)                                       H Size of captured input picture(lsb).
 DATA[9]           Input H Size(msb)                                       H Size of captured input picture(msb).
 DATA[10]          Input V Size(lsb)                                       V Size of captured input picture(lsb).
 DATA[11]          Input V Size(msb                                        V Size of captured input picture(msb).

```

#### 7.7.4 AnyTile Set/Get Resolution Mode

```text

 Bytes             Bytes Description                              Bits     Description
 DATA[0]           0x4E = Display monitor ID – Get                         Set/get the resolution input mode
                   0x4F = Display monitor ID – Set
 DATA[1]           Mode                                                    0x00 : default
                                                                           0x01 : FHD
                                                                           0x02 : UHD4K




```

### 7.8 Light Sensor

```text
The command is used to set/get the light sensor status as it is defined as below.


```

#### 7.8.1 Message-Get

```text


 Bytes         Bytes Description                           Bits       Description
 DATA[0]       0x25 = Light Sensor – Get                              Command requests the display to report its current
                                                                      light sensor status

Example: (Display address 01)
 MsgSize Control Group                   Data (0)      Checksum
 0x05        0x01        0x00            0x25          0x21


```

#### 7.8.2 Message-Report

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

#### 7.8.3 Message-Set

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

### 7.9 Human Sensor

```text
              The command is used to set/get the external human sensor (CRD41) status as it is defined as below.

              The command is available on Dragon 1.x platform from firmware version: x.xxx (tbc) onwards

              Himalaya 2.0 and Dragon 1.6 platform from production start.




```

#### 7.9.1 Human Sensor Message-Get

```text


 Bytes          Bytes Description                       Bits       Description
 DATA[0]        0xB3 = Human Sensor – Get                          Command requests the display to report its current
                                                                   Human sensor time status

Example: (Display address 01)
 MsgSize Control Group                 Data (0)     Checksum
 0x05        0x01        0x00          0xB3         0xB7




```

#### 7.9.2 Human Sensor Message-Report

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

#### 7.9.3 Human Sensor Message-Set

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

### 7.10 OSD Rotating

```text
The command is used to set/get the OSD menu direction as it is defined as below.


```

#### 7.10.1 Message-Get

```text


 Bytes          Bytes Description                       Bits       Description
 DATA[0]        0x27 = OSD Rotating – Get                          Command requests the display to report its current
                                                                   OSD rotating status

Example: (Display address 01)
 MsgSize Control Group                Data (0)      Checksum
 0x05        0x01        0x00         0x27          0x23


```

#### 7.10.2 Message-Report

```text


 Bytes          Bytes Description                           Bits      Description
 DATA[0]        0x27 = OSD Rotating – Report                          Command reports OSD Rotating Setting
 DATA[1]        On / Off                                              0x00 = Off
                                                                      0x01 = On

Example: Current Display settings: Off and On (Display address 01)
 MsgSize Control Group                 Data (0)    Data (1)     Checksum
 0x06       0x01         0x00          0x27        0x00         0x20
 0x06       0x01         0x00          0x27        0x01         0x21


```

#### 7.10.3 Message-Set

```text


 Bytes          Bytes Description                       Bits       Description
 DATA[0]        0x26 = OSD Rotating – Set                          Command to change the OSD Rotating setting of the
                                                                   display
 DATA[1]        On / Off                                           0x00 = Off
                                                                   0x01 = On

Example: Set the Display to the fallowing: OSD rotating Off (Display address 01)
 MsgSize Control Group                 Data (0)    Data (1)      Checksum
 0x06        0x01        0x00          0x26        0x00          0x21

```

### 7.11 Display Orientation

```text

The command is used to set/get the Orientation of the display.
The command is only available in dragon 1.0 & 1.5 & 1.6 & Himalaya 2.0 platforms & CRD50 from
firmware version x.xx



```

#### 7.11.1 Message-Get

```text


 Bytes        Bytes Description                    Bits       Description
 DATA[0]      0x16 = Display Orientation –                    Command requests the display to report its current
              Get                                             Display orientation status

Example: (Display address 01)
 MsgSize Control Group            Data (0)     Checksum
 0x05        0x01        0x00     0x16         0x12


```

#### 7.11.2 Message-Report

```text

Himalaya2.0 platform only support OSD Rotation(DATA[2]) and Image rotation on main window(DATA[4]).
CRD50 don’t support image OSD rotation & Data4 > 7, the OSD is rotated together with the image.

 Bytes       Bytes Description                         Bits      Description
 DATA[0]     0x16 = Display Orientation                          Command reports Display orientation status
             Report
 DATA[1]     Auto Rotate                                         0x00 = Off
                                                                 0x01 = On
                                                                 (only available on Dragon 1 & 1.5 platform)
 DATA[2]     OSD Rotation                                        0x00 = Landscape
                                                                 0x01 = Portrait
 DATA[3]     Image All                                           0x00 = Off
                                                                 0x01 = On (not supported on the CRD50)
                                                                 0x02 = On Clock Wise*
                                                                 0x03 = On Counter Clock Wise*
                                                                 (*) only supported on the CRD50
 DATA[4]     Display Window 1(Main)                              0x00 = Off
                                                                 0x01 = On
 DATA[5]     Display Window 2(Sub1)                              0x00 = Off
                                                                 0x01 = On
 DATA[6]     Display Window 3(Sub2)                              0x00 = Off
                                                                 0x01 = On
 DATA[7]     Display Window 4(Sub3)                              0x00 = Off
                                                                 0x01 = On


```

#### 7.11.3 Message-Set

```text

    Himalaya2.0 platform only support OSD Rotation(DATA[2]) and Image rotation on main window(DATA[4]).
    CRD50 don’t support image OSD rotation & Data4 > 7, the OSD is rotated together with the image.


 Bytes       Bytes Description                         Bits      Description
 DATA[0]     0x17 = Display Orientation Set                      Command sets Display orientation details
 DATA[1]     Auto Rotate                                         0x00 = Off
                                                                 0x01 = On

                                                                      (only available on Dragon 1 & 1.5 platform)

  DATA[2]       OSD Rotation                                          0x00 = Landscape
                                                                      0x01 = Portrait
  DATA[3]       Image All                                             0x00 = Off
                                                                      0x01 = On (not supported on the CRD50)
                                                                      0x02 = On Clock Wise*
                                                                      0x03 = On Counter Clock Wise*
                                                                      (*) only supported on the CRD50
  DATA[4]       Display Window 1(Main)                                0x00 = Off
                                                                      0x01 = On
  DATA[5]       Display Window 2(Sub1)                                0x00 = Off
                                                                      0x01 = On
  DATA[6]       Display Window 3(Sub2)                                0x00 = Off
                                                                      0x01 = On
  DATA[7]       Display Window 4(Sub3)                                0x00 = Off
                                                                      0x01 = On
Example: 0C 01 00 17 00 00 01 00 00 00 00 1B portrait image, OSD normal

```

### 7.11 Information OSD

```text
 The command is used to set/get the Information OSD Feature as it is defined as below.


```

#### 7.11.1 Message-Get

```text


  Bytes         Bytes Description                       Bits       Description
  DATA[0]       0x2D = Information OSD                             Command requests the display to report its current
                Feature – Get                                      Information OSD Feature status

 Example: (Display address 01)
  MsgSize Control Group               Data (0)      Checksum
  0x05        0x01        0x00        0x2D          0x29


```

#### 7.11.2 Message-Report

```text


  Bytes         Bytes Description                           Bits      Description
  DATA[0]       0x2D = Information OSD                                Command reports the Information OSD Feature
                Feature – Report                                      enabled or disabled
  DATA[1]       Off, 1 – 60                                           0x00 = Off
                                                                      0x01 – 0x3C = 1 – 60

 Example: Current Display Information OSD Feature settings: Off (Display address 01)
  MsgSize Control Group               Data (0)    Data (1)      Checksum
  0x06       0x01         0x00        0x2D        0x00          0x2A


```

#### 7.11.3 Message-Set

```text





 Bytes          Bytes Description                       Bits       Description
 DATA[0]        0x2C = Information OSD                             Command to set the Information OSD Feature of the
                Feature – Set                                      display enabled or disabled
 DATA[1]        Off, 1 – 60                                        0x00 = Off
                                                                   0x01 – 0x3C = 1 – 60

Example: Set the Display to the fallowing: Information OSD Feature: Off (Display address 01)
 MsgSize Control Group                 Data (0)     Data (1)    Checksum
 0x06        0x01        0x00          0x2C         0x00        0x2B

```

### 7.12 MEMC Effect

```text
The command is used to set/get the MEMC effects as it is defined as below.

NOTE: Himalaya 1.0 & 1.2 & Dragon 1.x & 1.6 platform does NOT support MEMC effect



```

#### 7.12.1 Message-Get

```text


 Bytes          Bytes Description                       Bits       Description
 DATA[0]        0x29 = MEMC Effect – Get                           Command requests the display to report its current
                                                                   MEMC effect status

Example: (Display address 01)
 MsgSize Control Group                Data (0)      Checksum
 0x05        0x01        0x00         0x29          0x2D


```

#### 7.12.2 Message-Report

```text


 Bytes          Bytes Description                           Bits      Description
 DATA[0]        0x29 = MEMC Effect – Report                           Command reports the MEMC effect level
 DATA[1]        Off/Low/Medium/High                                   0x00 = Off
                                                                      0x01 = Low
                                                                      0x02 = Medium
                                                                      0x03 = High

Example: Current Display MEMC settings: Off (Display address 01)
 MsgSize Control Group              Data (0)     Data (1)     Checksum
 0x06       0x01         0x00       0x29         0x00         0x2E


```

#### 7.12.3 Message-Set

```text


 Bytes          Bytes Description                       Bits       Description
 DATA[0]        0x28 = MEMC Effect – Set                           Command to set the MEMC level of the display for
                                                                   various picture motion performance
 DATA[1]        Off/Low/Medium/High                                0x00 = Off
                                                                   0x01 = Low
                                                                   0x02 = Medium
                                                                   0x03 = High

Example: Set the Display to the fallowing: MEMC Effect off (Display address 01)





 MsgSize     Control       Group       Data (0)     Data (1)       Checksum
 0x06        0x01          0x00        0x28         0x00           0x2F
```

### 7.13 Touch Feature

```text
The command is used to set/get the Touch Feature as it is defined as below.

NOTE: Himalaya 1.0 & 1.2 Dragon 1.x & 2.0 platform does NOT support this commands.



```

#### 7.13.1 Message-Get

```text


 Bytes          Bytes Description                       Bits       Description
 DATA[0]        0x1F = Touch Feature – Get                         Command requests the display to report its current
                                                                   Touch Feature status

Example: (Display address 01)
 MsgSize Control Group                 Data (0)     Checksum
 0x05        0x01        0x00          0x1F         0x1B


```

#### 7.13.2 Message-Report

```text


 Bytes          Bytes Description                           Bits      Description
 DATA[0]        0x1F = Touch Feature – Report                         Command reports the Touch Feature enabled or
                                                                      disabled
 DATA[1]        On / Off                                              0x00 = Off
                                                                      0x01 = On


Example: Current Display Touch Feature settings: Off (Display address 01)
 MsgSize Control Group              Data (0)      Data (1)      Checksum
 0x06       0x01         0x00       0x1F          0x00          0x18


```

#### 7.13.3 Message-Set

```text


 Bytes          Bytes Description                       Bits       Description
 DATA[0]        0x1E = Touch Feature – Set                         Command to set the Touch Feature of the display
                                                                   enabled or disabled
 DATA[1]        On /Off                                            0x00 = Off
                                                                   0x01 = On

Example: Set the Display to the fallowing: Touch Feature off (Display address 01)
 MsgSize Control Group                 Data (0)    Data (1)      Checksum
 0x06        0x01        0x00          0x1E        0x00          0x19





```

### 7.14 Noise Reduction

```text
The command is used to set/get the Noise reduction Feature as it is defined as below.


```

#### 7.14.1 Message-Get

```text


 Bytes          Bytes Description                        Bits       Description
 DATA[0]        0x2B = Noise Reduction                              Command requests the display to report its current
                Feature – Get                                       Noise Reduction status

Example: (Display address 01)
 MsgSize Control Group                 Data (0)      Checksum
 0x05        0x01        0x00          0x2B          0x2F


```

#### 7.14.2 Message-Report

```text


 Bytes          Bytes Description                            Bits      Description
 DATA[0]        0x2B = Noise reduction Feature                         Command reports the Noise Reduction Feature
                – Report                                               enabled or disabled
 DATA[1]        Off / Low / Middle / High                              0x00 = Off
                                                                       0x01 = Low
                                                                       0x02 = Middle
                                                                       0x03 = High
                                                                       0x04 = default*

(*) only valid for challenger2.1 platform
Example: Current Display Noise Reduction Feature settings: Off (Display address 01)
 MsgSize Control Group              Data (0)      Data (1)      Checksum
 0x06       0x01         0x00       0x2B          0x00          0x2C


```

#### 7.14.3 Message-Set

```text


 Bytes          Bytes Description                        Bits       Description
 DATA[0]        0x2A = Noise reduction                              Command to set the Noise Reduction Feature of the
                Feature – Set                                       display enabled or disabled
 DATA[1]        Off / Low / Middle / High                           0x00 = Off
                                                                    0x01 = Low
                                                                    0x02 = Middle
                                                                    0x03 = High
                                                                    0x04 = default*

(*) only valid for challenger2.1 platform


Example: Set the Display to the fallowing: Noise Reduction Feature off (Display address 01)
 MsgSize Control Group                 Data (0)     Data (1)    Checksum
 0x06        0x01        0x00          0x2A         0x00        0x2D





```

### 7.15 Scan Mode

```text
The command is used to set/get the Scan Mode Feature as it is defined as below.


```

#### 7.15.1 Message-Get

```text


 Bytes         Bytes Description                       Bits         Description
 DATA[0]       0x51 = Scan Mode Feature –                           Command requests the display to report its current
               Get                                                  Scan Mode Feature status

Example: (Display address 01)
 MsgSize Control Group               Data (0)      Checksum
 0x05        0x01        0x00        0x51          0x55


```

#### 7.15.2 Message-Report

```text


 Bytes         Bytes Description                             Bits      Description
 DATA[0]       0x51 = Scan Mode Feature –                              Command reports the Scan Mode Feature
               Report                                                  enabled or disabled
 DATA[1]       Over scan / Under scan                                  0x00 = Over scan (ON)
                                                                       0x01 = Under scan
                                                                       0x02 = Off
                                                                       0x03 > 0x1C (from 0 > 25)*

    (*) From 0 > 25 only valid for challenger 2.1 platform
Example: Current Display Scan Mode Feature settings: Over scan (Display address 01)
 MsgSize Control Group              Data (0)     Data (1)     Checksum
 0x06       0x01         0x00       0x51         0x00         0x56


```

#### 7.15.3 Message-Set

```text


 Bytes         Bytes Description                       Bits         Description
 DATA[0]       0x50 = Scan Mode Feature –                           Command to set the Scan mode Feature of the
               Set                                                  display enabled or disabled
 DATA[1]       Over scan / Under scan                               0x00 = Over scan
                                                                    0x01 = Under scan
                                                                    0x02 = Off
                                                                    0x03 > 0x1C (from 0 > 25)*

    (*) From 0 > 25 only valid for challenger 2.1 platform


Example: Set the Display to the fallowing: Scan Mode Feature over scan (Display address 01)
 MsgSize Control Group                 Data (0)    Data (1)    Checksum
 0x06        0x01        0x00          0x50        0x00        0x57





```

### 7.16 Scan Conversion

```text
The command is used to set/get the Scan Conversion Feature as it is defined as below.

NOTE: Himalaya 1.0 &1.2 & Dragon 1.x & 1.6 platform does NOT support Scan Conversion.



```

#### 7.16.1 Message-Get

```text


 Bytes          Bytes Description                       Bits       Description
 DATA[0]        0x53 = Scan Conversion                             Command requests the display to report its current
                Feature – Get                                      Scan Conversion Feature status

Example: (Display address 01)
 MsgSize Control Group                 Data (0)     Checksum
 0x05        0x01        0x00          0x53         0x57


```

#### 7.16.2 Message-Report

```text


 Bytes          Bytes Description                           Bits      Description
 DATA[0]        0x53 = Scan Conversion Feature                        Command reports the Scan Conversion Feature
                – Report                                              enabled or disabled
 DATA[1]        Progressive / Interlace                               0x00 = Progressive
                                                                      0x01 = Interlace

Example: Current Display Scan Conversion Feature settings: Progressive (Display address 01)
 MsgSize Control Group              Data (0)     Data (1)      Checksum
 0x06       0x01         0x00       0x53         0x00          0x54


```

#### 7.16.3 Message-Set

```text


 Bytes          Bytes Description                       Bits       Description
 DATA[0]        0x52 = Scan Conversion                             Command to set the Scan Conversion Feature of the
                Feature – Set                                      display enabled or disabled
 DATA[1]        Progressive / Interlace                            0x00 = Progressive
                                                                   0x01 = Interlace

Example: Set the Display to the fallowing: Scan Conversion Feature Progressive (Display address 01)
 MsgSize Control Group                 Data (0)    Data (1)     Checksum
 0x06        0x01        0x00          0x52        0x00         0x55





```

### 7.17 Switch On Delay (Tiling)

```text
The command is used to set/get the Switch on Delay (Tiling) Feature as it is defined as below.
Value in (OFF (0), 2, 4, 6, 8, 10, 20, 30, 40, 50, Auto (60))

```

#### 7.17.1 Message-Get

```text

 Bytes             Bytes Description                              Bits       Description
 DATA[0]           0x55 = Switch On Delay                                    Command requests the display to report its current
                   (Tiling) Feature – Get                                    Switch On Delay (Tiling) Feature status

Example: (Display address 01)
 MsgSize Control Group                         Data (0)         Checksum
 0x05        0x01        0x00                  0x55             0x51


```

#### 7.17.2 Message-Report

```text

 Bytes             Bytes Description                                  Bits      Description
 DATA[0]           0x55 = Switch On Delay (Tiling)                              Command reports the Switch On Delay (Tiling)
                   Feature – Report                                             Feature enabled or disabled
 DATA[1]           Switch on delay time                                         0x00 = Off
                                                                                0x01 = Auto
                                                                                0x02 = 2 seconds
                                                                                0x03 = 3 seconds
                                                                                0x04 = 4 seconds
                                                                                ………………….
                                                                                0xFD = 253 seconds
                                                                                0xFE = 254 seconds
                                                                                0xFF = 255 seconds

Example: Current Display Switch On Delay (Tiling) Feature settings: Off (Display address 01)
 MsgSize Control Group              Data (0)       Data (1)     Checksum
 0x06       0x01         0x00       0x55           0x01         0x53


```

#### 7.17.3 Message-Set

```text


 Bytes             Bytes Description                               Bits      Description
 DATA[0]           0x54 = Switch On Delay                                    Command to set the Switch On Delay (Tiling)
                   (Tiling) Feature – Set                                    Feature of the display enabled or disabled
 DATA[1]           Switch on delay time                                      0x00 = Off
                                                                             0x01 = Auto
                                                                             0x02 = 2 seconds
                                                                             0x03 = 3 seconds
                                                                             0x04 = 4 seconds
                                                                             ………………….
                                                                             0xFD = 253 seconds
                                                                             0xFE = 254 seconds
                                                                             0xFF = 255 seconds

Example: Set the Display to the fallowing: Switch On Delay (Tiling) Feature: Off (Display address 01)
 MsgSize Control Group                 Data (0)     Data (1)     Checksum
 0x06        0x01        0x00          0x54         0x00         0x53





```

### 7.18 Factory Reset

```text
 The command is used to set/get the Factory Reset as it is defined as below.


```

#### 7.18.1 Message-Set

```text

  Bytes         Bytes Description                       Bits     Description
  DATA[0]       0x56 = Factory Reset – Set                       Command to do the Factory Reset of the display
                                                                          1     User Input Control: Local
                                                                                Keyboard/Remote Control
                                                                          2     User Input Control State:
                                                                                Remote Control State/Local
                                                                                Keyboard State
                                                                          3     Power at Cold Start
                                                                          4     Auto Signal Detecting
                                                                          5     Video            Parameters: 每個 Input source 設定
                                                                                Brightness/Contrast/Sharpn
                                                                                ess/Color/Tint/Black
                                                                                Level/Gamma
                                                                          6     Color Temperature            每個 Input source 設定
                                                                          7     Color Parameters: Red 每個 Input source 設定
                                                                                Gain/Green        Gain/Blue
                                                                                Gain/Red       Offset/Green
                                                                                Offset/Blue Offset
                                                                          8     Picture Format               每個 Input source 設定
                                                                          9      nVGA Video Parameters: 所有 Input source 儲存
                                                                                Clock/Clock       Phase/Hor
                                                                                Position/Ver Position
                                                                          10    Picture-in-Picture（Disable
                                                                                PIP function）:PIP Off
                                                                          11    Volume
                                                                          12    Volume               Limits:
                                                                                Max/Min/SwitchOn（After
                                                                                reset,   put Max=100   ，
                                                                                Min=0，SwitchOn=0）
                                                                          13    Audio           Parameters: 每個 Input source 設定
                                                                                Treble/Bass
                                                                          14    Smart Power
                                                                          15    Tiling:          Position/V.
                                                                                Monitor/H.Monitor(Clear
                                                                                Tiling    Position=1,     V.
                                                                                Monitor=1, H.Monitor=1)
                                                                          16    Light Sensor                 No supported.
                                                                          17    OSD Rotating                 No supported.
                                                                          18    Information OSD Feature
                                                                          19    MEMC Effect                  No supported.
                                                                          20    Touch Feature                No supported.
                                                                          21    Noise Reduction Feature      每個 Input source 設定
                                                                          22    Scan Mode Feature            每個 Input source 設定
                                                                          23    Scan Conversion Feature      每個 Input source 設定
                                                                          24    Switch On Delay (Tiling)
                                                                                Feature




 Example: Set the Display to factory reset
  MsgSize Control Group                 Data (0)    Checksum
  0x05        0x01        0x00          0x56        0x52





```

### 7.19 Power On logo

```text
The command is used to set/get the Power on logo status as it is defined as below.

```

#### 7.19.1 Message-Get

```text


 Bytes       Bytes Description                     Bits       Description
 DATA[0]     0x3F = Power On logo status                      Command requests the display to report its
             – Get                                            current Power On logo status

Example: (Display address 01)
 MsgSize Control Group            Data (0)       Checksum
 0x05      0x01       0x00        0x3F           0x3B


```

#### 7.19.2 Message-Report

```text


 Bytes       Bytes Description                         Bits     Description
 DATA[0]     0x3F = Power On logo status –                      Command reports the Power On logo
             Report                                             enabled or disabled
 DATA[1]     Off / On / User                                    0x00 = Off
                                                                0x01 = On
                                                                0x02 = User

Example: Current Display Power On logo setting: Off (Display address 01)
 MsgSize Control Group          Data (0) Data (1)        Checksum
 0x06      0x01       0x00      0x3F        0x00         0x38


```

#### 7.19.3 Message-Set

```text


 Bytes       Bytes Description                     Bits       Description
 DATA[0]     0x3E = Power On logo status                      Command to set the Power On logo of the
             – Set                                            display enabled or disabled
 DATA[1]     Off / On / User                                  0x00 = Off
                                                              0x01 = On
                                                              0x02 = User

Example: Set the Display to the fallowing: Power on logo Off (Display address 01)
 MsgSize Control Group            Data (0) Data (1)       Checksum
 0x06      0x01       0x00        0x3E        0x00        0x39





```

### 7.20 Fan Speed

```text
 The command is used to set/get the Fan Speed status as it is defined as below.

 NOTE: Dragon 1.x & 1.6 platform does not support Fan Speed commands.


```

#### 7.20.1 Message-Get

```text


  Bytes          Bytes Description                        Bits       Description
  DATA[0         0x62 = Fan Speed status –                           Command requests the display to report its
  ]              Get                                                 current Fan Speed status
Example: (Display address 01)
  MsgSize Control Group                  Data (0)       Checksum
  0x05        0x01        0x00           0x62           0x66


```

#### 7.20.2 Message-Report

```text


  Bytes          Bytes Description                            Bits      Description
  DATA[0         0x62 = Fan Speed status –                              Command reports the Fan Speed status
  ]              Report                                                 enabled or disabled
  DATA[1         Off / Auto / Low / Middle / High                       0x00 = Off
  ]                                                                     0x01 = Auto
                                                                        0x02 = Low
                                                                        0x03 = Middle
                                                                        0x04 = High

 Example: Current Display Fan Speed settings: Off (Display address 01)
  MsgSize Control Group          Data (0) Data (1)         Checksum
  0x06      0x01       0x00      0x62         0x00         0x65


```

#### 7.20.3 Message-Set

```text


  Bytes          Bytes Description                        Bits       Description
  DATA[0         0x61 = Fan Speed status – Set                       Command to set the Fan Speed status of the
  ]                                                                  display enabled or disabled
  DATA[1         Off / Auto / Low / Middle /                         0x00 = Off
  ]              High                                                0x01 = Auto
                                                                     0x02 = Low
                                                                     0x03 = Middle
                                                                     0x04 = High

 Example: Set the Display to the fallowing: Fan Speed off (Display address 01)
  MsgSize Control Group            Data (0) Data (1)        Checksum
  0x06      0x01       0x00        0x61        0x00         0x66





```

### 7.21 APM status (advanced power management)

```text
 The command is used to set/get the APM status as it is defined as below.

 Supported on Himalaya & eagle 1.3 platform .


```

#### 7.21.1 Message-Get

```text


  Bytes        Bytes Description                      Bits       Description
  DATA[0       0xD1 = APM status – Get                           Command requests the display to report its
  ]                                                              current APM status

 Example: (Display address 01)
  MsgSize Control Group              Data          Checksum
                                     (0)
  0x05        0x01       0x00        0xD1          0xD5


```

#### 7.21.2 Message-Report

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

#### 7.21.3 Message-Set

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

### 7.22 Power saving mode status

```text
The command is used to set/get the Power Saving Mode status as it is defined as below.


```

#### 7.22.1 Message-Get

```text


 Bytes         Bytes Description                    Bits       Description
 DATA[0       0xD3 = Power Saving mode                         Command requests the display to report its
 ]            status – Get                                     current Power Saving Mode status

Example: (Display address 01)
 MsgSize Control Group             Data (0)       Checksum
 0x05      0x01       0x00         0xD3           0xD7


```

#### 7.22.2 Message-Report

```text

Dragon 1.x , 1.6 & Challenger 2.1 platform supports 4 power modes only (0x04 ~ 0x07) are valid

 Bytes         Bytes Description                        Bits     Description
 DATA[0]       0xD3 = Power Saving Mode                          Command reports the Power Saving Mode
               status – Report                                   enabled or disabled
 DATA[1]       Off / On                                          0x00 = RGB Off & Video Off
                                                                 0x01 = RGB Off, Video On
                                                                 0x02 = RGB On, Video Off
                                                                 0x03 = RGB On & Video On
                                                                 0x04 = mode 1
                                                                 0x05 = mode 2
                                                                 0x06 = mode 3
                                                                 0x07 = mode 4


Example: Current Display Power Saving Mode setting: RGB & Video off (Display address 01)
 MsgSize Control Group          Data (0) Data (1) Checksum
 0x06      0x01       0x00      0xD3      0x00        0xD4


```

#### 7.22.3 Message-Set

```text

Dragon 1.x , 1.6 & Challenger 2.1 platform supports 4 power modes only (0x04 ~ 0x07) are valid



 Bytes         Bytes Description                    Bits       Description
 DATA[0]       0xD2 = Power Saving Mode                        Command to set the Power Saving Mode
               status – Set                                    enabled or disabled
 DATA[1]       Off / On                                        0x00 = RGB Off & Video Off
                                                               0x01 = RGB Off, Video On
                                                               0x02 = RGB On, Video Off
                                                               0x03 = RGB On & Video On
                                                               0x04 = mode 1
                                                               0x05 = mode 2
                                                               0x06 = mode 3
                                                               0x07 = mode 4


Example: Set the Display to the fallowing: Power Saving Mode RGB & Video Off (Display address 01)
 MsgSize Control Group            Data (0) Data (1) Checksum

     0x06         0x01          0x00       0xD2           0x00           0xD5


```

### 7.23 Pixel Shift

```text
                  The command is used to set/get the pixel shift value.

                  The command is only available on Dragon 1.0 and Dragon 1.5 platform from firmware version: x.xxx
                  (tbc) onwards.

```

#### 7.23.1 Message-Get Pixel Shift

```text

     Bytes          Bytes Description                       Bits       Description
     DATA[0]        0xB1 = Pixel Shift – Get                           Command requests the display to report its current
                                                                       Pixel shift value

    Example: (Display address 01)
     MsgSize Control Group                Data (0)      Checksum
     0x05        0x01        0x00         0xB1          0xB5


```

#### 7.23.2 Message-Report Pixel Shift

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

#### 7.23.3 Message-Set Pixel Shift

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

### 7.24 Off Timer

```text


                  The command is used to set/get the Off Timer value.

                  The command is only available on Dragon 1.0 and Dragon 1.5 platform from firmware version: x.xxx
                  (tbc) onwards.

```

#### 7.24.1 Message-Get Off Timer

```text


     Bytes         Bytes Description                        Bits       Description
     DATA[0]      0x91 = Off Timer– Get                                Command requests the display to report its current
                                                                       Off timer value

    Example: (Display address 01)
     MsgSize Control Group                Data (0)      Checksum
     0x05        0x01        0x00         0x91          0x95


```

#### 7.24.2 Message-Report Off Timer

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

#### 7.24.3 Message-Set Off Timer

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

### 7.25 ECO mode

```text
                  The command is used to set/get the ECO mode to normal or low power standby.

                  The command is only available on Phoenix 1 & 2 platform from firmware version: x.xxx (tbc) onwards.


 Bytes       Bytes Description                      Bits       Description
 DATA[0]    0x63 = Eco mode– Get                               Command requests the display to report its current
                                                               ECO mode value

Example: (Display address 01)
 MsgSize Control Group             Data (0)     Checksum
 0x05        0x01        0x00      0x63         0x67

```

#### 7.25.1 Message-report ECO mode

```text

   Bytes      Bytes Description                         Bits      Description
 DATA[0]      0x63 = ECO mode                                     Command reports the ECO mode
              status – Report                                     enabled or disabled
 DATA[1]      Low power standby or normal                         0x00 = low power standby
                                                                  0x01 = normal




Example: Current ECO Mode setting: (Display address 01)

 MsgSize    Control    Group        Data (0)      Data (1)       Checksum
 0x06       0x01       0x00         0x63          0x00           0x65              Low power standby
 0x06       0x01       0x00         0x63          0x01           0x64              normal

```

#### 7.25.2 Message- Set ECO mode

```text

   Bytes      Bytes Description                         Bits      Description
 DATA[0]      0x64 = ECO mode                                     Command set the ECO mode
              status – set                                        enabled or disabled
 DATA[1]      Low power standby or normal                         0x00 = low power standby
                                                                  0x01 = normal




Example: Current Display Power Saving Mode setting: RGB & Video off (Display address 01)
 MsgSize Control Group          Data (0) Data (1) Checksum
 0x06      0x01       0x00      0x64      0x00        0x63           Low power standby
 0x06      0x01       0x00      0x64      0x01        0x62           normal



```

### 7.26 Picture Style

```text

            The command is used to set/get the picture style :

            Highbright, sRGB, Vivid, Natural, Standard, Video, Static Signage, Text, Energy saving

            The command is only available on Phoenix 1 & 2 platform from firmware version: x.xx (tbc) onwards.


 Bytes       Bytes Description                      Bits       Description


  DATA[0]      0x65 = Picture Style – Get                           Command requests the display to report its current
                                                                    Picture Style value

 Example: (Display address 01)
  MsgSize Control Group        Data (0)  Checksum
  0x05        0x01        0x00 0x65      0x61
```

#### 7.26.1 Message-report get Picture Style

```text

    Bytes        Bytes Description                           Bits      Description
  DATA[0]        0x65 = Picture Style                                  Command reports the Picture Style
                 status – Report
  DATA[1]        Picture style*                                        0x00 = Highbright
                                                                       0x01 = sRGB
                                                                       0x02 = Vivid
                                                                       0x03 = Natural
                                                                       0x04 = Standard
                                                                       0x05 = Video
                                                                       0x06 = Static Signage
                                                                       0x07 = Text
                                                                       0x08 = Energy saving
                                                                       0x09 = Soft
                                                                       0x0A = User

                *: could be that not all the picture styles are available, check the OSD menu of your monitor
     Example: Current picture style setting: (Display address 01)

  MsgSize  Control Group        Data (0)               Data (1)       Checksum
  0x06     0x01      0x00       0x65                   0x00           0x62              Highbright
  0x06     0x01      0x00       0x65                   0x03           0x61              Natural
```

#### 7.26.2 Message-set Picture Style

```text

   The command is only available on Phoenix 1 & 2 platform from firmware version: x.xx (tbc) onwards.
    Bytes   Bytes Description                       Bits    Description
  DATA[0]   0x66 = Set Picture Style                        Command set the Picture Style

  DATA[1]        Picture style*                                        0x00 = Highbright
                                                                       0x01 = sRGB
                                                                       0x02 = Vivid
                                                                       0x03 = Natural
                                                                       0x04 = Standard
                                                                       0x05 = Video
                                                                       0x06 = Static Signage
                                                                       0x07 = Text
                                                                       0x08 = Energy saving
                                                                       0x09 = Soft
                                                                       0x0A = User


                *: could be that not all the picture styles are available, check the OSD menu of your monitor

Example : set picture style to highbright
  MsgSize Control Group                Data (0)      DATA[1]          Checksum
  0x06        0x01        0x00         0x66          0x00             0x61

```

### 7.27 Send screenshot

```text
Take a screenshot of current source and send it via Email.
Note that
```

**1.** Different model may not have screenshot of all sources. Video layers may not be captured either.

```text
             Means external sources can not be captured.
```

**2.** Email information should be set in Settings-> Signage Display -> Server Settings -> Email Notification

**3.** The screenshot will be named, {yyyy-MM-dd-HH-mm-ss}.png and put under {internal

```text

            storage}/Philips/Screenshots
```

**4.** Only possible on android monitors Himalaya 2 and Dragon2, see platform , from firmware version xx

```text
            TBC

 Bytes   Bytes Description                          Bits       Description
 DATA[0] 0x58 = Take a screenshot and                          Command to take a screenshot
         email– Set

Example: Take a screenshot (Display address 01)
 MsgSize Control Group           Data (0) Checksum
 0x05      0x01       0x00       0x58        0x5C



```

### 7.28 Video signal present

```text

   Is supported from firmware version : tbc
   The following command is used to get information if there is videosignal present or not on the screen.
  Message-Get
   Bytes      Bytes Description                        Bits       Description
 DATA[0]      0x59 = Video Present                                Command requests the display to report its current
              Parameter – Get                                     Video present parameter.

Example: (Display address 01)
 MsgSize Control Group             Data (0)     Data (1)
 0x05        0x01        0x00      0x59         CRC

```

#### 7.28.1 Message-report

```text
    Bytes   Bytes Description                          Bits       Description
 DATA[0]    0x59 = Video Present
            Parameter – Get
 DATA[1]    Video status                                          0x00 video not present
                                                                  0x01 video present

      Report message example
 MsgSize   Control Group            Data (0)      Data (1)       Checksum
 0x06      0x01       0x00          0x59          0x00           0x5E              Video not present
 0x06      0x01       0x00          0x59          0x01           0x5F              Video present




```

### 7.29 Frame compensation Get value Horz value

```text
   Is supported from firmware version : tbc

   Get the Horizontal frame compensation value.


 Bytes        Bytes Description                     Bits       Description
 DATA[0]      0x5E = Frame compensation                        Command requests the display to report its current
              Horz value – Get                                 Frame compensation Horz value

Example: (Display address 01)
 MsgSize Control Group             Data (0)     Checksum
 0x05        0x01        0x00      0x5E         0x5A


   Message-Report

 Bytes        Bytes Description                         Bits      Description

      DATA[0]      0x5E = Frame compensation –                           Horz frame compensation value
                   Horz Report
      DATA[1]                                                            0x00 = 00
                                                                         0x01 = 01
                                                                         …
                                                                         0xFF = 255
9


         Example: Current Display settings:
      MsgSize Control Group               Data (0)     Data (1)       Checksum
      0x06     0x01         0x00          0x5E         0x00           0x59
      0x06     0x01         0x00          0x5E         0x03           0x5A




```

### 7.30 Frame compensation Set value Horz

```text

        Is supported from firmware version : tbc

        Set the Horizontal frame compensation value.


      Bytes        Bytes Description                           Bits      Description
      DATA[0]      0x5F = Frame compensation –                           Set Horz frame compensation value
                   Horz Set
      DATA[1]                                                            0x00 = 00
                                                                         0x01 = 01
                                                                         …
                                                                         0xFF = 255
10


         Example: Current Display settings:
      MsgSize Control Group               Data (0)     Data (1)       Checksum
      0x06     0x01         0x00          0x5F         0x00           0x58
      0x06     0x01         0x00          0x5F         0x03           0x5B

```

### 7.31 Frame compensation Get value Vert value

```text

        Is supported from firmware version : tbc

        Get the Horizontal frame compensation value.


      Bytes        Bytes Description                       Bits       Description
      DATA[0]      0x67 = Frame compensation                          Command requests the display to report its current
                   Vert value – Get                                   Frame compensation Vert value

     Example: (Display address 01)
      MsgSize Control Group               Data (0)     Checksum
      0x05        0x01        0x00        0x67         0x63


        Message-Report

      Bytes        Bytes Description                           Bits      Description
      DATA[0]      0x67 = Frame compensation                             Vert frame compensation value
                   Vert– Report
      DATA[1]                                                            0x00 = 00
                                                                         0x01 = 01
                                                                         …
                                                                         0xFF = 255
11


         Example: Current Display settings:

        MsgSize      Control       Group         Data (0)       Data (1)      Checksum
        0x06         0x01          0x00          0x67           0x00          0x60
        0x06         0x01          0x00          0x67           0x03          0x63




```

### 7.32 Frame compensation Set value Vert

```text
           Set the Vertical frame compensation value.


        Bytes           Bytes Description              Bits                       Description
        DATA[0]         0x68 = Frame compensation Vert                            Set Vert frame compensation value
                        – Set
        DATA[1]                                                                   0x00 = 00
                                                                                  0x01 = 01
                                                                                  …
                                                                                  0xFF = 255
  12


           Example: Current Display settings:
        MsgSize Control Group               Data (0)            Data (1)      Checksum
        0x06     0x01         0x00          0x68                0x00          0x6F
        0x06     0x01         0x00          0x68                0x03          0x6C



```

## 8 Scheduling

```text

```

### 8.1 Scheduling Parameters

```text
       The following commands are used to get/set scheduling parameters as it is defined below.

```

#### 8.1.1 Message-Get

```text

        Bytes              Bytes Description                           Bits       Description
        DATA[0]            0x5B = Scheduling                                      Command requests the display to report its current
                           Parameters – Get                                       Scheduling parameters.
        DATA[1]            Page                                                   1 to 7 of the scheduling pages

       Example: (Display address 01)
        MsgSize Control Group                    Data (0)       Data (1)         Checksum
        0x06        0x01        0x00             0x5B           0x01             0x5D



```

#### 8.1.2 Message-Report

```text

       Only Dragon 1.x & 1.6 & Himalay 2.0 platform supports additional DATA[8] to indicate playlist/bookmark/file number

        Bytes              Bytes Description                       Bits     Description
        DATA[0]            0x5B = Scheduling                                Command reports to the host controller the current
                           Parameters – Report                              Scheduling parameters of the display.
        DATA[1]            Page                                             0: Page disable
                                                                            1: Page enable
        DATA[2]            Start time hour                                  0 to 23 of the start time hour
                                                                            24: NULL
        DATA[3]            Start time minute                                0 to 59 of the start time minute
                                                                            60: NULL
        DATA[4]            End time hour                                    0 to 23 of the end time hour
                                                                            24: NULL


DATA[5]   End time minute                             0 to 59 of the end time minute
                                                      60: NULL
DATA[6]   Video source                                0 to 100 (%) of the user selectable range of the display.
                                                      For video source:
                                                      0x00 = NULL
                                                      0x01 = VIDEO
                                                      0x02 = S-VIDEO
                                                      0x03 = COMPONENT
                                                      0x04 = CVI 2 (not applicable)
                                                      0x05 = VGA
                                                      0x06 = HDMI 2
                                                      0x07 = Display Port 2
                                                      0x08 = USB 2
                                                      0x09 = Card DVI-D
                                                      0x0A = Display Port
                                                      0x0B= Card OPS
                                                      0x0C = USB
                                                      0x0D= HDMI
                                                      0x0E= DVI-D
                                                      0x0F = HDMI3
                                                      0x10= BROWSER
                                                      0x11= SMARTCMS
                                                      0X12= DMS (Digital Media Server)
                                                      0x13= INTERNAL STORAGE





                                                                     0x14= Reserved
                                                                     0x15= Reserved
                                                                     0x16=Media Player
                                                                     0x17=PDF Player
                                                                     0x18=Custom
                                                                     0x19 = HDMI 4
                                                                     0x1A = VGA2
                                                                     0x1B = VGA3
                                                                     0x1C = IWB
 DATA[7]            Working day(s)                                   To set the scheduling working days.
                                                                     Bit0 = 1: every week
                                                                     Bit1 = Monday
                                                                     Bit2 = Tuesday
                                                                     Bit3 = Wednesday
                                                                     Bit4 = Thursday
                                                                     Bit5 = Friday
                                                                     Bit6 = Saturday
                                                                     Bit7 = Sunday
 DATA[8]            Bookmark/Playlist/File Tag(s)                    To set the set Tag from 1 through 7
                                                                     0x01 = Tag 1
                                                                     0x02 = Tag 2
                                                                     0x03 = Tag 3
                                                                     0x04 = Tag 4
                                                                     0x05 = Tag 5
                                                                     0x06 = Tag 6
                                                                     0x07 = Tag 7

Example: Report page1 with HDMI starts at 06:30 and ends at 22:00 every day.
 MsgSize Control Group             Data (0) Data (1)         Data (2)      Data (3)                    Data (4)      Data (5)
 0x0C       0x01       0x00        0x5B        0x01          0x06          0x1E                        0x16          0x00
 Data (6) Data (7) Checksum
 0x0A       0xFF       0xAC

```

#### 8.1.3 Message-Set

```text

Only Dragon 1.x & 1.6 & Himalay 2.0 platform supports additional DATA[8] to indicate playlist/bookmark/file number

 Bytes              Bytes Description                      Bits       Description
 DATA[0]            0x5A = Scheduling                                 Command to change the current Scheduling parameters
                    Parameters – Set
 DATA[1]            Page                                              BIT 7-BIT4:
                                                                      1 to 7 of the scheduling pages
                                                                      BIT 3-BIT0:
                                                                      0: Page disable
                                                                      1: Page enable
 DATA[2]            Start time hour                                   0 to 23 of the start time hour
                                                                      24: NULL
 DATA[3]            Start time minute                                 0 to 59 of the start time minute
                                                                      60: NULL
 DATA[4]            End time hour                                     0 to 23 of the end time hour
                                                                      24: NULL
 DATA[5]            End time minute                                   0 to 59 of the end time minute
                                                                      60: NULL





 DATA[6]         Video source                                0 to 100 (%) of the user selectable range of the display.
                                                             For video source:
                                                             0x00 = NULL
                                                             0x01 = VIDEO
                                                             0x02 = S-VIDEO
                                                             0x03 = COMPONENT
                                                             0x04 = CVI 2 (not applicable)
                                                             0x05 = VGA
                                                             0x06 = HDMI 2
                                                             0x07 = Display Port 2
                                                             0x08 = USB 2
                                                             0x09 = Card DVI-D
                                                             0x0A = Display Port
                                                             0x0B= Card OPS
                                                             0x0C = USB
                                                             0x0D= HDMI
                                                             0x0E= DVI-D
                                                             0x0F = HDMI3
                                                             0x10= BROWSER
                                                             0x11= SMARTCMS
                                                             0X12= DMS (Digital Media Server)
                                                             0x13= INTERNAL STORAGE
                                                             0x14= Reserved
                                                             0x15= Reserved
                                                             0x16=Media Player
                                                             0x17=PDF Player
                                                             0x18=Custom
                                                             0x19= HDMI 4
                                                             0x1A = VGA2
                                                             0x1B = VGA3
                                                             0x1C = IWB
 DATA[7]         Working day(s)                              To set the scheduling working days.
                                                             Bit0 = 1: every week
                                                             Bit1 = Monday
                                                             Bit2 = Tuesday
                                                             Bit3 = Wednesday
                                                             Bit4 = Thursday
                                                             Bit5 = Friday
                                                             Bit6 = Saturday
                                                             Bit7 = Sunday
 DATA[8]         Bookmark/Playlist/File Tag(s)               To set the set Tag from 1 through 7
                                                             0x01 = Tag 1
                                                             0x02 = Tag 2
                                                             0x03 = Tag 3
                                                             0x04 = Tag 4
                                                             0x05 = Tag 5
                                                             0x06 = Tag 6
                                                             0x07 = Tag 7

Example: Set page1 with HDMI starts at 06:30 and ends at 22:00 every day.
 MsgSize Control Group                Data (0)    Data (1)    Data (2)        Data (3)     Data (4)     Data (5)
 0x0C        0x01       0x00          0x5A        0x10        0x06            0x1E         0x16         0x00
 Data (6) Data (7) Checksum
 0x0A        0xFF       0xBC





```

## 9 Group ID

```text
 This command is used to set/get the Group ID as it is defined as below.


```

#### 9.1.1 Message-Get

```text

  Bytes         Bytes Description               Bits      Description
  DATA[0]       0x5D = Group ID – Get                     Command requests the display to report its Group ID

 Example: (Display address 01)
  MsgSize Control Group              Data (0)      Checksum
  0x05        0x01        0x00       0x5D          0x59



```

#### 9.1.2 Message-Report

```text

  Bytes         Bytes Description                      Bits     Description
  DATA[0]       0x5D = group ID – Report                        Command reports Group ID
  DATA[1]       Group ID                                        Group ID range: Off(for old command),1-254
                                                                0x01-0xFE = 1-254
                                                                0xFF = Off, It is for the old command.
 Example: Group ID = 1 (Display address 01)
  MsgSize Control Group              Data (0)      Data (1)       Checksum
  0x06       0x01       0x01         0x5D          0x01           0x5A


```

#### 9.1.3 Message-Set

```text

  Bytes         Bytes Description            Bits        Description
  DATA[0]       0x5C = Group ID Set                      Command to set the Group ID
  DATA[1]       Group ID                                 Group ID range: Off(for old command),1-254
                                                         0x01-0xFE = 1-254
                                                         0xFF = Off, It is for the old command.
 Example: set the Group ID = 1 (Display address 01)
  MsgSize Control Group               Data (0)    Data (1)        Checksum
  0x06        0x01        0x00        0x5C        0x01            0x5A


```

## 10 Custom Multi-Window Settings

```text
 This command is used to set or get screen divisions – called windows on the display screen & configure the
 multi window individually. A window contains the video from a particular input source.

 NOTE: Width, Height parameters can’t be higher than the LCD panel resolution. Aspect ratio 16:9 is only
 supported.

```

#### 10.1.1 Message-Set

```text

  Bytes         Bytes Description                        Bits       Description
  DATA[0]       0xFB = Execute Custom                               Command requests the display to set the image of
                Multi-Win – Set                                     window.
  DATA[1]       Switch Custom Multi-Win                             0x00 = Custom Multi-Win OFF
                                                                    0x01 = Custom Multi-Win ON
  DATA[2]       Windows                                             0x00 = Open one window


                                                                               0x01 = Open two windows
                                                                               0x02 = Open three windows
                                                                               0x03 = Open four windows

Example: Set Display address 01, Custom Multi-Win ON, open 3 windows,
   MsgSize         Control         Group          Data (0)        Data (1)                               Data (2)           Checksum
    0x07             0x01            0x00          0xFB            0x01                                   0x02                0xFE

```

#### 10.1.2 Message-Get (report) –

```text

SPECIAL NOTE: Dragon 1.x & 1.6 platform supports only a maximum of 2 windows. Main window and a sub(x) window.

This message report can be just about which window is currently active or can be very detailed. Both examples are presented after the table.

 Bytes            Bytes Description                                Bits        Description
 DATA[0]          0xFD = Custom Multi-Win –                                    Command report to the host controller the
                  Report                                                       window’s information of the display.
 DATA[1]          Window                                                       0x00 = Main(Display Win1)
                                                                               0x01 = Sub1(Display Win2)
                                                                               0x02 = Sub2(Display Win3)
                                                                               0x03 = Sub3(Display Win4)
 DATA[2]          Image rotation                                               0x00 = ROT_NONE (OFF)
                                                                               0x01 = ROT_90 (ON)
                                                                               0x02 = ROT_270,
                                                                               0x03 = ROT_H_MIRROR
                                                                               0x04 = ROT_V_MIRROR
                                                                               0x05 = ROT_HV_MIRROR
 DATA[3]          X position of image(High byte)                               X position of image(High byte)
 DATA[4]          X position of image(Low byte)                                X position of image(Low byte)
 DATA[5]          Y position of image(High byte)                               Y position of image(High byte)
 DATA[6]          Y position of image(Low byte)                                Y position of image(Low byte)
 DATA[7]          Width of image(High byte)                                    Width of image(High byte)
 DATA[8]          Width of image(Low byte)                                     Width of image(Low byte)
 DATA[9]          Height of image(High byte)                                   Height of image(High byte)
 DATA[10]         Height of image(Low byte)                                    Height of image(Low byte)
 DATA[11]         Picture Format                                               Picture Format.
                                                                               0x00 = Normal (4:3)
                                                                               0x01 = Custom
                                                                               0x02 = Real (1:1)
                                                                               0x03 = Full
                                                                               0x04 = 21:9
                                                                               0x05 = Dynamic
                                                                               0x06 = 16:9
                                                                               0xFF = Current setting(don’t change)

SPECIAL NOTE: Dragon 1.x platform doesn’t support DATA [11] value 0x05.

Example: Display address 01, Main window, ROT_NONE, X:0, Y:0, W:1920, H:1080, Zoom mode: Full
  MsgSize        Control         Group        Data (0)       Data (1)      Data (2)        Data (3)                                         Data (4)
   0x10            0x01           0x01         0xFD           0x00           0x00             0x00                                           0x00
  Data (5)       Data (6)       Data (7)      Data (8)       Data (9)      Data (10)       Data (11)                                       Checksum
   0x00            0x00           0x07         0x80           0x04           0x38             0x03                                           0x55

Example: Get information of Main window (Display address 01)
 MsgSize Control         Group       Data (0)     Data (1)   Checksum
   0x06        0x01        0x00       0xFD         0x00        0xFA

```

#### 10.1.3 Message-Set

```text


  SPECIAL NOTE: 2016 Dragon 1.x platform supports only a maximum of 2 windows. Main window and a sub(x) window.

      Bytes       Bytes Description                          Bits       Description
      DATA[0]     0xFC = Custom Multi-Win –                             Command requests the display to set the image
                  Set                                                   data of window.
      DATA[1]     Window                                                0x00 = Main(Display Win1)
                                                                        0x01 = Sub1(Display Win2)
                                                                        0x02 = Sub2(Display Win3)
                                                                        0x03 = Sub3(Display Win4)
      DATA[2]     Image rotation                                        0x00 = ROT_NONE (OFF)
                                                                        0x01 = ROT_90 (ON)
                                                                        0x02 = ROT_270,
                                                                        0x03 = ROT_H_MIRROR
                                                                        0x04 = ROT_V_MIRROR
                                                                        0x05 = ROT_HV_MIRROR
      DATA[3]     X position of image(High byte)                        X position of image(High byte)
      DATA[4]     X position of image(Low byte)                         X position of image(Low byte)
      DATA[5]     Y position of image(High byte)                        Y position of image(High byte)
      DATA[6]     Y position of image(Low byte)                         Y position of image(Low byte)
      DATA[7]     Width of image(High byte)                             Width of image(High byte)
      DATA[8]     Width of image(Low byte)                              Width of image(Low byte)
      DATA[9]     Height of image(High byte)                            Height of image(High byte)
      DATA[10]    Height of image(Low byte)                             Height of image(Low byte)
      DATA[11]    Picture Format                                        Picture Format.
                                                                        0x00 = Normal
                                                                        0x01 = Custom
                                                                        0x02 = Real
                                                                        0x03 = Full
                                                                        0x04 = 21:9
                                                                        0x05 = Dynamic
                                                                        0x06 = 16:9
                                                                        0xFF = Current setting(don’t change)

  SPECIAL NOTE: Dragon 1.x platform doesn’t support DATA [11] value 0x05.

  Example: Set Display address 01, Main window, ROT_NONE, X:0, Y:0, W:1280, H:2160, Zoom mode: Full
    MsgSize        Control         Group         Data (0)      Data (1)       Data (2)       Data (3)                          Data (4)
     0x10            0x01           0x00          0xFC          0x00            0x00           0x00                             0x00
    Data (5)       Data (6)        Data (7)      Data (8)      Data (9)       Data (10)     Data (11)                         Checksum
     0x00            0x00           0x07           0x80         0x04            0x38           0x03                             0x55


```

## 11 Color Calibration – MIC (TBD)

```text

  This command is used to set color calibration related special operations.

```

### 11.1 Message-Set

```text

        CMD: 0xFE



```

## 12 LED STRIP control for 10BDL3051T

```text

  Both LED strips of the 10BDL3051T can be switched ON or OFF and set to a particular color.
  By default, both LED strips are OFF at all times. The left and right LED stripes are controlled at the
  same time, it is not possible to control only the left or right LED strip.
  The commands can be send to the monitor via LAN , WiFi or via an android apk on localhost:5000.
  The default port is 5000 and can be changed in the admin menu.




Fig A: External front /back view of 10BDL3051T




```

### 12.1 Message-Get (Report)

```text

Use this command to Read status of LED strips such as light up status, and color assigned in terms of R, G and
B values.

 Bytes         Bytes Description              Bits     Description
 DATA[0]       0xF4 = Get                              Command to get LED light up status and color combination
                                                       values currently assigned as R, G and B values
 DATA[1]       Light up status                         0x00 = off (default), 0x01 = on
 DATA[2]       Red value                               Valid return values range from 0x00~0xFF
 DATA[3]       Green value                             Valid return values range from 0x00~0xFF
 DATA[4]       Blue value                              Valid return values range from 0x00~0xFF

Example: The return values indicates LED strips are ON and are of bright Yellow color
 MsgSize Control Group                Data (0) Data (1) Data (2)              Data(3)   Data(4)    Checksum
 0x09       0x01        0x00          0xF4         0x01       0xFF            0xF2      0x00       0xF0

```

### 12.2 Message-Set

```text

Use this command to simultaneously switch on/off LED strips as shown above and set color based on R, G,
and B values.

 Bytes         Bytes Description              Bits     Description
 DATA[0]       0xF3 = Set                              Command to set LED STRIPS ON/OFF and Choose color
 DATA[1]       Light up status                         0x00 = off, 0x01 = on
 DATA[2]       Red value                               Valid Values range from 0x00~0xFF only if DATA[1] = 0x01





  DATA[3]       Green value                             Valid Values range from 0x00~0xFF only if DATA[1] = 0x01
  DATA[4]       Blue value                              Valid Values range from 0x00~0xFF only if DATA[1] = 0x01

 Example: set the RGB values to bright Yellow and light ON the LED strips
  MsgSize Control Group                Data (0) Data (1) Data (2)              Data(3)   Data(4)    Checksum
  0x09        0x01       0x00          0xF3         0x01        0xFF           0xF2      0x00       0xF7

 Fig B: A few R, G, B values shown as decimals against the color they represent for reference purposes.




Examples:
       OFF:
       09 01 00 F3 00 FF 00 00 04

        RED
        09 01 00 F3 01 FF 00 00 05


          GREEN
          09 01 00 F3 01 00 FF 00 05

          BLUE
          09 01 00 F3 01 00 00 FF 05


```

## 13 MicroSD and USB ports Unlock/Lock –

```text
 10BDL3051T USB A type ports, microUSB ports and MicroSD slots – all at once can either be disabled by
 “lock” command or enabled by “unlock” command. Commercial use demands protection from malware
 and other digital instructions.

  These commands are only valid for:

 10BDL3051T
 Dragon 1.0 : from firmware phase 3 (from Android 9_03 & scaler 1_303).
 Dragon 1.5 : from firmware phase 2 (after V1.2XX).
 Dragon 1.6 : from production start

 QL 3.0 from firmware version : tbc

 Individual lock/unlock of MicroSD or any of the USB A type ports or microUSB ports is not available. At
 “lock” state, any USB device or T-Flash/MicroSD memory card plugged into any the USB ports or MicroSD
 slot
 respectively, will not be “accessible” or “recognizable” although they might receive power from the
 monitor. By default MicroSD and USB ports are unlocked.

```

### 13.1 Message-Get (Report)

```text

 Use this command to Read Lock/Unlock status of MicroSD and USB ports.

   Bytes           Bytes Description              Bits     Description
   DATA[0]         0xF2 = Get                              Read status of whether MicroSD and USB ports on
                                                           the monitor is locked or unlocked
   DATA[1]         Read status                             0x00 = unlocked (default)
                                                           0x01 = Locked


Example: Example get lock/unlock status MICROSD and USB ports:

   MsgSize      Control      Group       Data (0)     Checksum
   0x05         0x01         0x00        0xF2         0xF6

Reply message if unlocked:   0x06 0x01 0x01 0XF2 0x00 0xF4
Reply message if locked:     0x06 0x01 0x01 0XF2 0x01 0xF5



```

### 13.2 Message-Set

```text

 Use this command to lock or unlock MicroSD and USB ports in the monitor.

   Bytes           Bytes Description              Bits     Description
   DATA[0]         0xF1 = Set                              Set MicroSD and USB ports to locked or
                                                           unlocked status
   DATA[1]         Set status                              0x00 = unlocked
                                                           0x01 = Locked

 Example: This commands shows how to unlock (enable) MicroSD and USB ports

  MsgSize    Control    Group       Data (0)     Data (1)     Checksum
  0x06       0x01       0x00        0xF1         0x00         0xF6

```

## 14 Monitor ID

```text

This command is working on models tbc
 This command is used to set the monitor ID.


  Bytes        Bytes Description             Bits     Description
  DATA[0]      0x69 = monitor ID Set                  Command to set the Group ID
  DATA[1]      monitor ID                             0x01-0xFF = 1-254



 Example: set the Monitor with monitor ID = 3 to monitor ID = 6
  MsgSize Control Group               Data (0)    Data (1)     Checksum
  0x06        0x03        0x00        0x69        0x06         0x6A





```


## 8. Hardware test record

```markdown
### Test: <command>

- Date:
- Display model:
- Platform:
- Firmware:
- Transport: TCP / RS-232
- Host:
- Monitor ID:
- Group ID:
- Request bytes:
- Response bytes:
- Parsed result:
- Display behavior:
- Result: pass / partial / fail
- Notes:
```

## 9. Implementation checklist

1. Add the code and operation to the registry.
2. Define parameter names, ranges, and symbolic values.
3. Add packet-construction tests from the examples.
4. Add report parsing without discarding unknown values.
5. Test through the raw CLI.
6. Record the exact response and firmware.
7. Add a typed CLI command only after the raw exchange is understood.
8. Represent platform restrictions as metadata.

## 10. Known specification hazards

- Section numbers are sometimes duplicated or incorrect.
- The table of contents and detailed sections sometimes use different names.
- Some descriptions contradict their example bytes.
- Platform support varies substantially.
- `NAV` can mean unsupported, irrelevant, or temporarily impossible.
- Broadcast and some group commands intentionally produce no response.
- Some packets may omit the Group byte on older implementations.
- Preserve raw hexadecimal values and packet logs.
