# Monitor restart

Source: `docs/Philips_SICP_Commands.md`, lines 2033-2061.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 4.6.1 Message-Set

## DATA[0] Codes

- `0x57` - monitor Restart – Set                          Command to restart monitor

## Source Excerpt
#### 4.6 Monitor restart

```text

           The following command is used to restart/reboot the monitor.
           Only possible on android monitors Himalaya 2 and Dragon2 and future models, see platform , from
           firmware version xx TBC


```

##### 4.6.1 Message-Set

```text

  Bytes   Bytes Description                            Bits     Description
  DATA[0] 0x57 = monitor Restart – Set                          Command to restart monitor

  DATA[1]       Select target system to                         0x00 = Android
                restart                                         0x01 = Scalar (?)


 Example: Restart Android system of the monitor (Display address 01)
  MsgSize Control Group           Data (0) Data (1)       Checksum
  0x06      0x01      0x00        0x57       0x00         0x50


```
