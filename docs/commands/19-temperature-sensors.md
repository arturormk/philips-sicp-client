# Temperature Sensors

Source: `docs/Philips_SICP_Commands.md`, lines 3672-3715.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 7.4.1 Message-Get
- 7.4.2 Message-Report

## DATA[0] Codes

- `0x2F` - Temperature Sensor                          Command requests the display to report its value of
- `0x2F` - Temperature Sensor –                           Command reports Temperature sensor value

## Source Excerpt
#### 7.4 Temperature Sensors

```text


Compare two sensor data and report higher value of the two sensors in 1 data byte for reporting.

```

##### 7.4.1 Message-Get

```text

 Bytes         Bytes Description                     Bits         Description
 DATA[0]       0x2F = Temperature Sensor                          Command requests the display to report its value of
               – Get                                              the temperature sensors (±3°C).

Example: (Display address 01)
 MsgSize Control Group              Data (0)     Checksum
 0x05        0x01        0x00       0x2F         0x2B


```

##### 7.4.2 Message-Report

```text

 Bytes         Bytes Description                           Bits      Description
 DATA[0]       0x2F = Temperature Sensor –                           Command reports Temperature sensor value
               Report
 DATA[1]       Temperature Sensor 1                                  0-100 in Celsius degrees represented in hex.
 DATA[2]       Temperature Sensor 2                                  0-100 in Celsius degrees represented in hex.

SPECIAL NOTE: 2016 Dragon 1.0 & 2.0 platform only supports DATA[I] only. DATA[2] value is invalid.

Example: Current Temp Sensor 1 read out: = 28°C (Display address 01)
         Current Temp Sensor 2 read out: = 31°C (Display address 02)

 MsgSize    Control     Group       Data (0)     Data (1)         Data (2)   Checksum
 0x06       0x01        0x00        0x2F         0x1C             0x1F       0x2B

```
