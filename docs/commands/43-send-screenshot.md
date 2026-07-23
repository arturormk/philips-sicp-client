# Send screenshot

Source: `docs/Philips_SICP_Commands.md`, lines 5491-5529.

This file is generated from the vendor command transcription for quick implementation reference.

## DATA[0] Codes

- `0x58` - Take a screenshot and                          Command to take a screenshot

## Source Excerpt
#### 7.27 Send screenshot

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
