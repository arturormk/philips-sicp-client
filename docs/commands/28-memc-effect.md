# MEMC Effect

Source: `docs/Philips_SICP_Commands.md`, lines 4408-4476.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 7.12.1 Message-Get
- 7.12.2 Message-Report
- 7.12.3 Message-Set

## DATA[0] Codes

- `0x29` - MEMC Effect – Get                           Command requests the display to report its current
- `0x29` - MEMC Effect – Report                           Command reports the MEMC effect level
- `0x28` - MEMC Effect – Set                           Command to set the MEMC level of the display for

## Source Excerpt
#### 7.12 MEMC Effect

```text
The command is used to set/get the MEMC effects as it is defined as below.

NOTE: Himalaya 1.0 & 1.2 & Dragon 1.x & 1.6 platform does NOT support MEMC effect



```

##### 7.12.1 Message-Get

```text


 Bytes          Bytes Description                       Bits       Description
 DATA[0]        0x29 = MEMC Effect – Get                           Command requests the display to report its current
                                                                   MEMC effect status

Example: (Display address 01)
 MsgSize Control Group                Data (0)      Checksum
 0x05        0x01        0x00         0x29          0x2D


```

##### 7.12.2 Message-Report

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

##### 7.12.3 Message-Set

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
