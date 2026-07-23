# Color Calibration MIC

Source: `docs/Philips_SICP_Commands.md`, lines 6089-6126.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 11.1 Message-Set

## Source Excerpt
### 11 Color Calibration – MIC (TBD)

```text

  This command is used to set color calibration related special operations.

```

#### 11.1 Message-Set

```text

        CMD: 0xFE



```

### 12 LED STRIP control for 10BDL3051T

```text

  Both LED strips of the 10BDL3051T can be switched ON or OFF and set to a particular color.
  By default, both LED strips are OFF at all times. The left and right LED stripes are controlled at the
  same time, it is not possible to control only the left or right LED strip.
  The commands can be send to the monitor via LAN , WiFi or via an android apk on localhost:5000.
  The default port is 5000 and can be changed in the admin menu.




Fig A: External front /back view of 10BDL3051T




```
