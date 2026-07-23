# MicroSD and USB Ports Unlock Lock

Source: `docs/Philips_SICP_Commands.md`, lines 6217-6260.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 13.1 Message-Get (Report)
- 13.2 Message-Set

## DATA[0] Codes

- `0xF2` - Get                              Read status of whether MicroSD and USB ports on
- `0xF1` - Set                              Set MicroSD and USB ports to locked or

## Source Excerpt
#### 13.1 Message-Get (Report)

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

#### 13.2 Message-Set

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
