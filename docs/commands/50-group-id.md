# Group ID

Source: `docs/Philips_SICP_Commands.md`, lines 5899-5953.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 9.1.1 Message-Get
- 9.1.2 Message-Report
- 9.1.3 Message-Set

## DATA[0] Codes

- `0x5D` - Group ID – Get                     Command requests the display to report its Group ID
- `0x5D` - group ID – Report                        Command reports Group ID
- `0x5C` - Group ID Set                      Command to set the Group ID

## Source Excerpt
### 9 Group ID

```text
 This command is used to set/get the Group ID as it is defined as below.


```

##### 9.1.1 Message-Get

```text

  Bytes         Bytes Description               Bits      Description
  DATA[0]       0x5D = Group ID – Get                     Command requests the display to report its Group ID

 Example: (Display address 01)
  MsgSize Control Group              Data (0)      Checksum
  0x05        0x01        0x00       0x5D          0x59



```

##### 9.1.2 Message-Report

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

##### 9.1.3 Message-Set

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
