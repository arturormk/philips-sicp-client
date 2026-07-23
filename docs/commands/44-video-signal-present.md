# Video signal present

Source: `docs/Philips_SICP_Commands.md`, lines 5530-5565.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 7.28.1 Message-report

## DATA[0] Codes

- `0x59` - Video Present                                Command requests the display to report its current
- `0x59` - Video Present

## Source Excerpt
#### 7.28 Video signal present

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

##### 7.28.1 Message-report

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
