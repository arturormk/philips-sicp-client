# Communication Control

Source: `docs/Philips_SICP_Commands.md`, lines 392-493.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 2.4.1 Message-Report

## DATA[0] Codes

- `0x00` - Generic report message after Get or Set message

## Source Excerpt
#### 2.4 Communication Control

```text

This defines the feedback command from Philips Professional Display to host controller when it receives the
display command from the host controller, depending on the commands availability, the command reported back
to host controller can be one of the ACK, NACK or NAV.
Note: there is no reply message when the wrong ID address is being used.

```

##### 2.4.1 Message-Report

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
