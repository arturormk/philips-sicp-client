# Philips SICP v2.03 — Python Client Development Notes

This is a **living implementation document** for building and testing a Python client for the Philips Serial / Ethernet Interface Communication Protocol (SICP v2.03).

It is not intended to reproduce the entire vendor manual at once. Commands should be added here only as they are implemented, tested, and understood.

---

## 1. Development Goals

The client should eventually support:

- TCP communication over port `5000`
- RS-232 communication
- Packet construction
- XOR checksum calculation
- Packet parsing
- ACK / NACK / NAV handling
- GET command reports
- Monitor IDs
- Group IDs
- Broadcast commands
- Retries and timeouts
- Human-readable command wrappers
- Raw packet debugging
- A growing command registry

The initial implementation should remain small and transparent. Avoid building a large abstraction layer before enough commands have been tested against a real display.

---

## 2. Transport

### 2.1 Ethernet

The display accepts SICP commands over TCP.

| Setting | Value |
|---|---|
| Protocol | TCP |
| Default port | `5000` |
| Suggested timeout | `0.5` to `2.0` seconds |
| Packet framing | `MsgSize` byte at start of each packet |

A TCP connection may return one complete packet, several packets, or only part of a packet in a single `recv()` call. The Python implementation must therefore buffer incoming bytes and use the first byte, `MsgSize`, to determine when a complete packet has arrived.

### 2.2 RS-232

| Setting | Value |
|---|---|
| Baud rate | `9600` default |
| Data bits | `8` |
| Parity | None |
| Stop bits | `1` |
| Flow control | None |

The display DB9 connector uses:

| Pin | Signal | Direction relative to display |
|---|---|---|
| 2 | RXD | Input |
| 3 | TXD | Output |
| 5 | GND | Ground |

A crossover/null-modem connection is required between the controller and the display.

---

## 3. Packet Format

A normal packet containing a group byte is:

```text
+---------+------------+----------+---------+-----+---------+----------+
| MsgSize | Monitor ID | Group ID | Data[0] | ... | Data[N] | Checksum |
+---------+------------+----------+---------+-----+---------+----------+
```

The PDF calls the Monitor ID byte `Control`.

### 3.1 Fields

| Offset | Field | Description |
|---:|---|---|
| `0` | `MsgSize` | Total packet size in bytes, including checksum |
| `1` | `Control` | Monitor ID |
| `2` | `Group` | Group ID |
| `3` | `Data[0]` | Command code |
| `4..N-2` | `Data[1..]` | Parameters or report data |
| `N-1` | `Checksum` | XOR of all preceding bytes |

### 3.2 Message size

For a packet with a group byte:

```python
msg_size = 4 + len(data)
```

This counts:

- `MsgSize`
- `Control`
- `Group`
- all data bytes
- `Checksum`

For example, one command byte and no parameters gives a five-byte packet:

```text
05 01 00 19 1D
```

### 3.3 Checksum

The checksum is the XOR of every byte except the checksum byte itself.

```python
def xor_checksum(data: bytes) -> int:
    checksum = 0
    for value in data:
        checksum ^= value
    return checksum
```

Packet construction:

```python
def build_packet(
    command: int,
    *parameters: int,
    monitor_id: int = 1,
    group_id: int = 0,
) -> bytes:
    data = bytes([command, *parameters])
    msg_size = 4 + len(data)

    packet_without_checksum = bytes([
        msg_size,
        monitor_id,
        group_id,
    ]) + data

    checksum = xor_checksum(packet_without_checksum)
    return packet_without_checksum + bytes([checksum])
```

Example:

```python
packet = build_packet(0x19)
assert packet == bytes.fromhex("05 01 00 19 1D")
```

---

## 4. Monitor and Group Addressing

### 4.1 Monitor ID

| Value | Meaning |
|---:|---|
| `0x00` | Broadcast |
| `0x01`–`0xFF` | Individual display |

Broadcast commands do not generate replies.

A command sent to a monitor ID that is not active also receives no reply.

### 4.2 Group ID

| Value | Meaning |
|---:|---|
| `0x00` | Address by Monitor ID |
| `0x01`–`0xFE` | Address by Group ID |
| `0xFF` | Group disabled/off on some older platforms |

The document warns that commands with a non-zero group byte may not produce an ACK.

For initial development, use:

```python
monitor_id = 1
group_id = 0
```

---

## 5. Communication Semantics

### 5.1 SET command

A SET command normally receives a generic communication-control response:

| Response value | Name | Meaning |
|---:|---|---|
| `0x06` | ACK | Command executed |
| `0x15` | NACK | Invalid or corrupt command |
| `0x18` | NAV | Command unavailable, irrelevant, or cannot be executed |

Generic response packet data:

```text
Data[0] = 0x00
Data[1] = ACK, NACK, or NAV
```

Example ACK:

```text
06 01 00 00 06 01
```

### 5.2 GET command

A GET command normally receives a command-specific report, not a generic ACK.

For example:

```text
Get power:
05 01 00 19 1D

Power-on report:
06 01 00 19 02 1C
```

The client should distinguish between:

- generic communication-control responses, where `Data[0] == 0x00`
- command-specific reports, where `Data[0]` identifies the report command

### 5.3 Timing

The specification recommends waiting for the previous command to be answered before sending another.

A retry may be attempted when no response is received within approximately `500 ms`.

For development, start conservatively:

```python
timeout = 2.0
retries = 1
```

Reduce the timeout after the display's real behavior is understood.

---

## 6. Packet Parsing

A minimal parsed representation:

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class SicpPacket:
    raw: bytes
    msg_size: int
    monitor_id: int
    group_id: int
    data: bytes
    checksum: int

    @property
    def command(self) -> int | None:
        return self.data[0] if self.data else None

    @property
    def parameters(self) -> bytes:
        return self.data[1:] if len(self.data) > 1 else b""
```

Parser:

```python
def parse_packet(raw: bytes) -> SicpPacket:
    if len(raw) < 4:
        raise ValueError("SICP packet is too short")

    msg_size = raw[0]

    if len(raw) != msg_size:
        raise ValueError(
            f"Packet length mismatch: header says {msg_size}, "
            f"received {len(raw)}"
        )

    expected_checksum = xor_checksum(raw[:-1])
    actual_checksum = raw[-1]

    if actual_checksum != expected_checksum:
        raise ValueError(
            f"Checksum mismatch: expected 0x{expected_checksum:02X}, "
            f"received 0x{actual_checksum:02X}"
        )

    return SicpPacket(
        raw=raw,
        msg_size=msg_size,
        monitor_id=raw[1],
        group_id=raw[2],
        data=raw[3:-1],
        checksum=raw[-1],
    )
```

---

## 7. TCP Receive Strategy

Do not assume one `recv()` call equals one packet.

```python
def recv_packet(sock) -> bytes:
    buffer = bytearray()

    while len(buffer) < 1:
        chunk = sock.recv(1024)
        if not chunk:
            raise ConnectionError("Connection closed before packet header")
        buffer.extend(chunk)

    msg_size = buffer[0]

    while len(buffer) < msg_size:
        chunk = sock.recv(1024)
        if not chunk:
            raise ConnectionError("Connection closed before complete packet")
        buffer.extend(chunk)

    packet = bytes(buffer[:msg_size])

    # A production implementation should preserve any extra bytes in a
    # connection-level receive buffer rather than discard them.
    return packet
```

A later implementation should maintain a persistent receive buffer so multiple replies can be handled safely.

---

## 8. Suggested Python API

Initial low-level API:

```python
class SicpClient:
    def __init__(
        self,
        host: str,
        port: int = 5000,
        monitor_id: int = 1,
        group_id: int = 0,
        timeout: float = 2.0,
    ):
        ...

    def transact(self, command: int, *parameters: int) -> SicpPacket:
        ...

    def send_raw(self, packet: bytes) -> SicpPacket | None:
        ...
```

Command wrappers should remain simple:

```python
def get_power_state(self) -> bool:
    ...

def set_power_state(self, on: bool) -> None:
    ...
```

The low-level raw packet method should always remain available for testing undocumented or newly added commands.

---

## 9. Command Documentation Template

Every command added to this document should use the following structure.

```markdown
## Command Name

**Status:** untested / partially tested / tested

### GET

- Command:
- Parameters:
- Expected report:
- Example request:
- Example response:

### SET

- Command:
- Parameters:
- Expected response:
- Example request:
- Example response:

### Python API

```python
...
```

### Test Notes

- Display model:
- Firmware:
- Transport:
- Date tested:
- Result:
- Unexpected behavior:
```

---

# 10. Implemented Commands

## 10.1 Power State

**Status:** partially tested

The display uses separate command codes for GET and SET.

### GET Power State

| Field | Value |
|---|---|
| GET/report command | `0x19` |
| Parameters | None |

Request:

```text
05 01 00 19 1D
```

Known response values:

| `Data[1]` | Meaning |
|---:|---|
| `0x01` | Power off |
| `0x02` | Power on |

Example power-on response:

```text
06 01 00 19 02 1C
```

Python wrapper:

```python
def get_power_state(self) -> bool:
    response = self.transact(0x19)

    if response.command != 0x19:
        raise RuntimeError(
            f"Expected power report 0x19, got {response.command!r}"
        )

    if len(response.parameters) != 1:
        raise RuntimeError("Malformed power-state report")

    value = response.parameters[0]

    if value == 0x01:
        return False
    if value == 0x02:
        return True

    raise RuntimeError(f"Unknown power-state value: 0x{value:02X}")
```

### SET Power State

| Field | Value |
|---|---|
| SET command | `0x18` |

Values:

| Parameter | Meaning |
|---:|---|
| `0x01` | Power off |
| `0x02` | Power on |

Power off:

```text
06 01 00 18 01 1E
```

Power on:

```text
06 01 00 18 02 1D
```

Expected successful response:

```text
06 01 00 00 06 01
```

Python wrapper:

```python
def set_power_state(self, on: bool) -> None:
    value = 0x02 if on else 0x01
    response = self.transact(0x18, value)
    require_ack(response)
```

### Tested observations

The following exchange has been observed over TCP port 5000:

Request:

```text
05 01 00 19 1D
```

Response:

```text
06 01 01 19 02 1D
```

This response is notable because the returned Group byte is `0x01`, even though the request used Group `0x00`.

The parser should therefore not assume that the response group byte always exactly matches the request group byte.

The response still decodes as:

```text
MsgSize   = 0x06
MonitorID = 0x01
GroupID   = 0x01
Command   = 0x19
State     = 0x02
Checksum  = 0x1D
```

Checksum verification:

```text
06 XOR 01 XOR 01 XOR 19 XOR 02 = 1D
```

Result:

```text
Power state = On
```

---

## 10.2 Communication Control

**Status:** documented, not independently tested for every response type

Generic report command:

```text
Data[0] = 0x00
```

Response values:

| `Data[1]` | Meaning |
|---:|---|
| `0x06` | ACK |
| `0x15` | NACK |
| `0x18` | NAV |

Parser helper:

```python
class SicpAckError(RuntimeError):
    pass


class SicpNackError(SicpAckError):
    pass


class SicpNavError(SicpAckError):
    pass


def require_ack(packet: SicpPacket) -> None:
    if packet.command != 0x00:
        raise SicpAckError(
            f"Expected communication-control response, "
            f"got command 0x{packet.command:02X}"
        )

    if len(packet.parameters) != 1:
        raise SicpAckError("Malformed communication-control response")

    status = packet.parameters[0]

    if status == 0x06:
        return
    if status == 0x15:
        raise SicpNackError("Display returned NACK")
    if status == 0x18:
        raise SicpNavError("Display returned NAV")

    raise SicpAckError(
        f"Unknown communication-control status: 0x{status:02X}"
    )
```

---

# 11. Commands To Add Next

A practical implementation order:

1. Power state
2. Input source
3. Volume
4. Audio mute
5. Picture mute
6. Monitor restart
7. Model number
8. Firmware version
9. Platform and SICP version
10. Video signal present
11. Operating hours
12. Temperature
13. Keypad lock
14. Remote-control lock
15. Display orientation

Each command should be added only after:

- extracting its format from the vendor PDF
- generating known-good packet bytes
- testing it against the real display
- recording the response
- adding a Python wrapper
- adding a unit test

---

# 12. Test Record Template

```markdown
### Test: command name

- Date:
- Display model:
- Firmware:
- Connection: Ethernet / RS-232
- Monitor ID:
- Group ID:
- Request:
- Raw response:
- Parsed response:
- Result:
- Notes:
```

---

# 13. Unit-Test Strategy

Packet construction can be tested without hardware.

```python
def test_get_power_packet():
    assert build_packet(0x19) == bytes.fromhex("05 01 00 19 1D")


def test_set_power_off_packet():
    assert build_packet(0x18, 0x01) == bytes.fromhex(
        "06 01 00 18 01 1E"
    )


def test_set_power_on_packet():
    assert build_packet(0x18, 0x02) == bytes.fromhex(
        "06 01 00 18 02 1D"
    )


def test_parse_power_on_report():
    packet = parse_packet(bytes.fromhex("06 01 00 19 02 1C"))
    assert packet.command == 0x19
    assert packet.parameters == bytes([0x02])
```

Hardware integration tests should be optional and separated from ordinary unit tests.

---

# 14. Open Questions

These should be resolved experimentally:

- Does the display keep TCP connections open across multiple commands?
- Does it ever send unsolicited reports?
- Does it always return one SICP packet per command?
- Why did the tested GET response return Group ID `0x01`?
- Does power-on work while the display is in every standby mode?
- Does the network interface remain active during deep sleep?
- Does a SET command sometimes close the TCP connection?
- Are there platform-specific differences in ACK/NAV behavior?
- Which commands require the Android system to be fully awake?
- Are commands accepted while an OSD menu is open?

---

# 15. Source

Based on the Philips/TPV document:

**Serial / Ethernet Interface Communication Protocol Specification — SICP v2.03, 14 June 2019**

The vendor document should remain the authoritative source for command definitions, while this Markdown file records the behavior actually observed in the target display.
