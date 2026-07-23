# Monitor ID

Source: `docs/Philips_SICP_Commands.md`, lines 6261-6285.

This file is generated from the vendor command transcription for quick implementation reference.

## DATA[0] Codes

- `0x69` - monitor ID Set                  Command to set the Group ID

## Source Excerpt
### 14 Monitor ID

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
