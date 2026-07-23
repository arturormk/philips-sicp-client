# Factory Reset

Source: `docs/Philips_SICP_Commands.md`, lines 4829-4900.

This file is generated from the vendor command transcription for quick implementation reference.

## Operations

- 7.18.1 Message-Set

## DATA[0] Codes

- `0x56` - Factory Reset – Set                       Command to do the Factory Reset of the display

## Source Excerpt
#### 7.18 Factory Reset

```text
 The command is used to set/get the Factory Reset as it is defined as below.


```

##### 7.18.1 Message-Set

```text

  Bytes         Bytes Description                       Bits     Description
  DATA[0]       0x56 = Factory Reset – Set                       Command to do the Factory Reset of the display
                                                                          1     User Input Control: Local
                                                                                Keyboard/Remote Control
                                                                          2     User Input Control State:
                                                                                Remote Control State/Local
                                                                                Keyboard State
                                                                          3     Power at Cold Start
                                                                          4     Auto Signal Detecting
                                                                          5     Video            Parameters: 每個 Input source 設定
                                                                                Brightness/Contrast/Sharpn
                                                                                ess/Color/Tint/Black
                                                                                Level/Gamma
                                                                          6     Color Temperature            每個 Input source 設定
                                                                          7     Color Parameters: Red 每個 Input source 設定
                                                                                Gain/Green        Gain/Blue
                                                                                Gain/Red       Offset/Green
                                                                                Offset/Blue Offset
                                                                          8     Picture Format               每個 Input source 設定
                                                                          9      nVGA Video Parameters: 所有 Input source 儲存
                                                                                Clock/Clock       Phase/Hor
                                                                                Position/Ver Position
                                                                          10    Picture-in-Picture（Disable
                                                                                PIP function）:PIP Off
                                                                          11    Volume
                                                                          12    Volume               Limits:
                                                                                Max/Min/SwitchOn（After
                                                                                reset,   put Max=100   ，
                                                                                Min=0，SwitchOn=0）
                                                                          13    Audio           Parameters: 每個 Input source 設定
                                                                                Treble/Bass
                                                                          14    Smart Power
                                                                          15    Tiling:          Position/V.
                                                                                Monitor/H.Monitor(Clear
                                                                                Tiling    Position=1,     V.
                                                                                Monitor=1, H.Monitor=1)
                                                                          16    Light Sensor                 No supported.
                                                                          17    OSD Rotating                 No supported.
                                                                          18    Information OSD Feature
                                                                          19    MEMC Effect                  No supported.
                                                                          20    Touch Feature                No supported.
                                                                          21    Noise Reduction Feature      每個 Input source 設定
                                                                          22    Scan Mode Feature            每個 Input source 設定
                                                                          23    Scan Conversion Feature      每個 Input source 設定
                                                                          24    Switch On Delay (Tiling)
                                                                                Feature




 Example: Set the Display to factory reset
  MsgSize Control Group                 Data (0)    Checksum
  0x05        0x01        0x00          0x56        0x52





```
