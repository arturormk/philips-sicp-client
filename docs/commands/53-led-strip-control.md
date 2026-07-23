# LED Strip Control

Source: `docs/Philips_SICP_Commands.md`, lines 6127-6216.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 12.1 Message-Get (Report)
- 12.2 Message-Set

## DATA[0] Codes

- `0xF4` - Get                              Command to get LED light up status and color combination
- `0xF3` - Set                              Command to set LED STRIPS ON/OFF and Choose color

## Source Excerpt
#### 12.1 Message-Get (Report)

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

#### 12.2 Message-Set

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

### 13 MicroSD and USB ports Unlock/Lock –

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
