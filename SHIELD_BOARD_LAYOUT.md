# Shield Hub Board Engineering Design (5x7 cm) — Natural Distributed Layout v8.0

[🇧🇷 **Versão em Português (PLACA_SHIELD_LAYOUT.md)**](PLACA_SHIELD_LAYOUT.md) | [🇺🇸 **English Version**](#-english)

---

## 🇺🇸 English

This document provides the complete assembly design for the **Hub Shield Board** built on a **universal 5x7 cm perfboard (standard 2.54mm / 0.1" pitch)** featuring the **Natural Distributed Layout (v8.0)**:
- **Arduino Nano** positioned at the top with its **USB port facing outwards (top edge)**.
- **CON1 (FlySky FS-BS6 Radio 1x5 90°)** located on the **Left Board Edge** (Column 02, Rows 06 to 10) — ultra-short direct traces of **only 10 mm** to D2, D3, D4, and GND!
- **CON4 (MPU-6050 1x4 90°)** located on the **Right Board Edge** (Column 17, Rows 07 to 10) — ultra-short direct traces of **only 10 mm** to A4, A5, 5V, and GND!
- **Capacitive filter C1 ($100\mu\text{F} \times 16\text{V}$)** on the right side (Columns 14-15, Row 06), right next to the Nano 5V and GND pins.
- **CON2 (Front Light Harness 1x4 90°)** on the **Bottom-Left Edge** (Row 24, Columns 03 to 06).
- **CON3 (Rear Light Harness 1x6 90°)** on the **Bottom Center-Right Edge** (Row 24, Columns 08 to 13).
- **100% Planar:** **ZERO wire jumpers crossing other circuits!**

> [!TIP]
> ### 🌟 GRAPHICAL & INTERACTIVE BOARD MODELS AVAILABLE:
> - 🌐 **[Open Interactive Board Visualizer (HTML)](placa_shield_visualizador.html)** — **Recommended!** Fullscreen in-browser viewer with instant toggle between **Top View (Components)**, **Bottom View (Soldering / Verso Traces)**, and **X-Ray**, plus dynamic net filtering (GND, 5V, Headlights, Turn Signals, Brakes, MPU-6050, Radio) and hover coordinate inspector.
> - 🖼️ **[Component Top View Vector Diagram (SVG)](placa_shield_superior.svg)** — Clean top view showing Arduino Nano, actual 4-band resistor color codes, and 90° pin headers.
> - 🔄 **[Solder Bottom View Vector Diagram (SVG)](placa_shield_inferior.svg)** — Horizontally mirrored view matching how you see the board while soldering, with solder traces, ground bus, and zero crossovers.
> - 📸 **[Realistic 3D Assembled Board Render (JPG)](placa_shield_3d.jpg)** — Physical assembly 3D perspective visualization.

---

### 📐 1. Board Coordinates Matrix (18 Columns x 24 Rows Grid) — Distributed v8.0

```
       01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18  (Columns)
 01 [  .  .  .  .  . ┌──────────────────┐ .  .  .  .  .  .  ] 01 ◄── TOP EDGE
 02 [  . [════════════════+5V TOP RAIL═════════] .  .  .  .  ] 02 ◄── Direct +5V Trace
 03 [  .  .  .  .  . │[D1]          [VIN]│.  .  .  .  .  .  ] 03
 04 [  .  .  .  .  . │[D0]          [GND]│.  .  .  .  .  .  ] 04 ◄── Nano Right GND
 05 [  .[+5V] .  .  .│[RST]         [RST]│.  .  .  .  .  .  ] 05 ◄── CON1 P1 (+5V BEC)
 06 [  .[GND] .  .  .│[GND]          [5V]│. [C1: 100uF] .  ] 06 ◄── CON1 P2 (GND) & C1
 07 [  .[CH2] .  .  .│[D2]           [A7]│.  .  .  .  .[GND].] 07 ◄── CON1 P3 (CH2) & CON4 P1
 08 [  .[CH4] .  .  .│[D3]           [A6]│.  .  .  .  .[+5V].] 08 ◄── CON1 P4 (CH4) & CON4 P2
 09 [  .[CH1] .  .  .│[D4]           [A5]│.  .  .  .  .[SCL].] 09 ◄── CON1 P5 (CH1) & CON4 P3
 10 [  .  ▲   .  .  .│[D5]═══════════════╗.  .  .  .  .[SDA].] 10 ◄── D5 (Tail) & CON4 P4
 11 [  .  │   .  .  .│[D6]═══════════╗   ║.  .  .  .  .  ▲  .] 11 ◄── D6 (Brake)
 12 [  . CON1: RADIO │[D7]═══════╗   ║   ║.  .  .  .  CON4  .] 12 ◄── D7 (B.RL)
 13 [  . (1x5 90° L) │[D8]═══╗   ║   ║   ║.  .  .  .   MPU  .] 13 ◄── D8 (B.RR)
 14 [  .  .   .  ╔═══│[D9]   ║   ║   ║   ║.  .  .  . (1x4 90°] 14 ◄── D9 (Headlight)
 15 [  .  .   .  ║ ╔═│[D10]  ║   ║   ║   ║.  .  .  .   R)   .] 15 ◄── D10 (B.FL)
 16 [  .  .   .  ║ ║ │[D11]  ║   ║   ║   ║.  .  .  .  .  .  .] 16 ◄── D11 (B.FR)
 17 [  .  .   .  ║ ║ │[D12]  ║   ║   ║   ║.  .  .  .  .  .  .] 17
 18 [  .  .  . [R1][R2][R3] . [R7][R6][R5][R4] .  .  .  .  .] 18 ◄── RESISTOR TOPS
 19 [  .  .  .  │   │   │   .  │   │   │   │  .  .  .  .  .  ] 19
 20 [  .  .  .  │   │   │   .  │   │   │   │  .  .  .  .  .  ] 20
 21 [  .  .  . [┴] [┴] [┴]  . [┴] [┴] [┴] [┴] .  .  .  .  .  ] 21 ◄── RESISTOR BASES
 22 [  .  .  .  │   │   │   .  │   │   │   │  .  .  .  .  .  ] 22
 23 [  .  .  .  │   │   │   .  │   │   │   │  .  .  .  .  .  ] 23
 24 [  .  . ┌──CON2: FRONT──┐ ┌──CON3: REAR (1x6 90°)──┐ .  ] 24
    [  .  . │[GND][H.L][B.L][B.R]│[B.R][B.L][Brk][Tai][NC][GND]│  ] 24
    [  .  . └──▲──────────────┘ └───────────────────────▲──┘ .  ] 24
               │ (GND via Col 01)        (GND via Col 13)│
```

---

### 🗺️ 2. Top-Down Component Placement Diagram

```
┌────────────────────────────────────────────────────────────────────────┐
│                          TOP BOARD EDGE                                │
│                                                                        │
│                      ┌─── [NANO USB PORT] ────┐                        │
│                      │                        │                        │
│                      │  ARDUINO NANO V3 (DIP) │                        │
│                      │ (Socketed in 2 rows of │                        │
│                      │  1x15 female headers)  │                        │
│                      │                        │                        │
│             (Col 6)  │                        │  (Col 12)              │
│       [D1/TX]  (o)   │                        │   (o)  [VIN]           │
│       [D0/RX]  (o)   │                        │   (o)  [GND] ──┐       │
│ ┌─────[RST]    (o)   │                        │   (o)  [RST]   │       │
│ │ ┌───[GND] ──┐(o)   │                        │   (o)  [5V] ───┼─┐     │
│┌┴─┴─────────┐ │      │                        │   (o)  [A7]    │ │     │
││ CON1: RADIO│ │      │                        │   (o)  [A6]    │ │ [C1]│
││(1x5 90° L) │ │      │                        │   (o)  [A5/SCL]┼─┼──┐│ │
││            │ │      │                        │   (o)  [A4/SDA]┼─┼─┐││ │
││[1: +5V] ◄──┼─┘      │                        │   (o)  [A3]    │ │ │││ │
││[2: GND] ◄──┼─(Row 6)┤ (10mm short traces!)   │   (o)  [A2]    │ │ │││ │
││[3: CH2] ◄──┼─[D2]───┤                        │   (o)  [A1] ┌──┴─┴─┴┴┴┐│
││[4: CH4] ◄──┼─[D3]───┤                        │             │  │CON4: MPU ││
││[5: CH1] ◄──┼─[D4]───┤                        │             │  │(1x4 90° R││
│└┬───────────┘ │      │                        │             │  │          ││
│ │             │ [D5] (o)════════════════════════════════════╗  │[1: GND]◄─┘│
│ ▼             │ [D6] (o)════════════════════════════════╗   ║  │[2: +5V]◄──│
│(90° Pins      │ [D7] (o)════════════════════════════╗   ║   ║  │[3: SCL]◄──┤
│ point left)   │ [D8] (o)════════════════════════╗   ║   ║   ║  │[4: SDA]◄──┘
│               │ [D9] (o)─────┐                  ║   ║   ║   ║  └┬─────────┘
│               │ [D10](o)──┐  │                  ║   ║   ║   ║   │
│               │ [D11](o)─┐│  │                  ║   ║   ║   ║   ▼
│               └──────────┴┴──┴──────────────────╫───╫───╫───╫───(90° Pins right)
│                          ││  │                  ║   ║   ║   ║
│                 [R1]   [R2] [R3]                [R7][R6][R5][R4]
│                 100Ω   150Ω 150Ω                150Ω 150Ω 150Ω 150Ω
│                (Head)  (B.FL)(B.FR)            (BRR)(BRL)(Brk)(Tai)
│                  │      │    │                    │   │   │   │
│                  ▼      ▼    ▼                    ▼   ▼   ▼   ▼
│         ┌───────────────────────┐        ┌────────────────────────┐
│         │ CON2: FRONT (1x4 90°) │        │ CON3: REAR (1x6 90°)   │
│         │┌─────┬───────┬──────┬─┴─┐      │┌───┬───┬───┬───┬───┬──┐│
│         ││ GND │ Head  │ B.FL │B.FR│      ││BRR│BRL│Brk│Tai│NC │GND│
│         │└──┬──┴───┬───┴──┬───┴───┘      │└─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬┘│
│         └───┼──────┼──────┼────────┘     └──┼───┼───┼───┼───┼───┼┘
│             │      │      │                 │   │   │   │   │   │
│             │      ▼      ▼                 ▼   ▼   ▼   ▼   │   │
│             │    (90° Right-Angle Pins point outwards from bottom)│
│             │                                                     │
│             └══════ (GND via Col 01)       (GND via Col 13) ══════╝
└────────────────────────────────────────────────────────────────────────┘
```

---

### 🔌 3. Solder Trace Connections (Bottom Copper Face)

The **v8.0 Natural Distributed Layout** eliminates 100% of wire crossovers using **nested planar L-tracks** and perimeter buses:

#### 📻 A. Radio Input Channel (Left Edge — 10mm Ultra-Short Traces!)
CON1 sits at **Column 02 (Rows 05 to 09)**, directly adjacent to Nano pins:
* **CON1 Pin 1 (+5V BEC, Col 02, Row 05):** Ascends to Row 02 and runs directly across to Nano 5V (Col 12, Row 06).
* **CON1 Pin 2 (GND, Col 02, Row 06):** Direct horizontal solder trace to **Nano GND** (Col 06, Row 06) $\rightarrow$ **10 mm!**
* **CON1 Pin 3 (CH2 Throttle, Col 02, Row 07):** Direct horizontal solder trace to **Nano D2** (Col 06, Row 07) $\rightarrow$ **10 mm!**
* **CON1 Pin 4 (CH4 Headlight, Col 02, Row 08):** Direct horizontal solder trace to **Nano D3** (Col 06, Row 08) $\rightarrow$ **10 mm!**
* **CON1 Pin 5 (CH1 Steering, Col 02, Row 09):** Direct horizontal solder trace to **Nano D4** (Col 06, Row 09) $\rightarrow$ **10 mm!**
* **Crossovers:** **ZERO! 100% parallel lines.**

#### 🧭 B. MPU-6050 & C1 Filter Channel (Right Edge — 10mm Ultra-Short Traces!)
CON4 sits at **Column 17 (Rows 07 to 10)**, directly adjacent to Nano I2C pins:
* **CON4 Pin 1 (GND, Col 17, Row 07):** Soldered to C1 (-) (Col 14, Row 06) and Nano right GND (Col 12, Row 04).
* **CON4 Pin 2 (+5V, Col 17, Row 08):** Soldered to C1 (+) (Col 15, Row 06) and Nano 5V (Col 12, Row 06).
* **CON4 Pin 3 (SCL, Col 17, Row 09):** Direct horizontal solder trace to **Nano A5** (Col 12, Row 09) $\rightarrow$ **10 mm!**
* **CON4 Pin 4 (SDA, Col 17, Row 10):** Direct horizontal solder trace to **Nano A4** (Col 12, Row 10) $\rightarrow$ **10 mm!**
* **Crossovers:** **ZERO! 100% parallel lines.**

#### 💡 C. Front LED Channel (Bottom-Left Edge — Row 24, Columns 03 to 06)
* **D9 (Headlight):** Nano D9 (Col 06, Row 14) $\rightarrow$ runs on Row 14 to Col 04 $\rightarrow$ **R1 Top** (Col 04, Row 18) $\rightarrow$ **R1 Bot** (Col 04, Row 21) $\rightarrow$ **CON2 Pin 2** (Headlight).
* **D10 (Front Left Blinker):** Nano D10 (Col 06, Row 15) $\rightarrow$ runs on Row 15 to Col 05 $\rightarrow$ **R2 Top** (Col 05, Row 18) $\rightarrow$ **R2 Bot** (Col 05, Row 21) $\rightarrow$ **CON2 Pin 3** (B.FL).
* **D11 (Front Right Blinker):** Nano D11 (Col 06, Row 16) $\rightarrow$ drops straight down Col 06 $\rightarrow$ **R3 Top** (Col 06, Row 18) $\rightarrow$ **R3 Bot** (Col 06, Row 21) $\rightarrow$ **CON2 Pin 4** (B.FR).
* **CON2 Pin 1 (GND, Col 03, Row 24):** Fed via the Column 01 left perimeter ground trace.

#### 💡 D. Rear LED Channel (Nested Planar L-Tracks — Zero Crossovers!)
To eliminate all wire intersections, rear channels use nested planar L-tracks:
* **D8 (Rear Right Blinker, Row 13):** Runs on Row 13 to **Col 08** $\rightarrow$ drops to **R7 Top** (Col 08, Row 18) $\rightarrow$ **R7 Bot** (Col 08, Row 21) $\rightarrow$ **CON3 Pin 1** (B.RR).
* **D7 (Rear Left Blinker, Row 12):** Runs on Row 12 to **Col 09** $\rightarrow$ drops to **R6 Top** (Col 09, Row 18) $\rightarrow$ **R6 Bot** (Col 09, Row 21) $\rightarrow$ **CON3 Pin 2** (B.RL).
* **D6 (Brake Light, Row 11):** Runs on Row 11 to **Col 10** $\rightarrow$ drops to **R5 Top** (Col 10, Row 18) $\rightarrow$ **R5 Bot** (Col 10, Row 21) $\rightarrow$ **CON3 Pin 3** (Brake).
* **D5 (Tail Light, Row 10):** Runs on Row 10 to **Col 11** $\rightarrow$ drops to **R4 Top** (Col 11, Row 18) $\rightarrow$ **R4 Bot** (Col 11, Row 21) $\rightarrow$ **CON3 Pin 4** (Tail).
* **CON3 Pin 5 (NC, Col 12, Row 24):** Empty / Key pin.
* **CON3 Pin 6 (GND, Col 13, Row 24):** Fed directly via the unoccupied Column 13 ground channel.

---

### 📋 4. Bill of Materials (Shield Board Only)

| Ref | Component | Description / Value | Purpose & Location |
| :---: | :--- | :--- | :--- |
| **U1** | Arduino Nano Socket | 2x 1x15 Female Headers (2.54mm pitch) | Columns 06 and 12 (Rows 03 to 17) |
| **U2** | MPU-6050 (GY-521) | 3D Inertial Sensor Module | Chassis mounted via CON4 harness |
| **C1** | Electrolytic Capacitor | **$100\mu\text{F} \times 16\text{V}$** | Columns 14 and 15 (Row 06), next to 5V and GND |
| **R1** | 1/4W Resistor | **$100\Omega$** (Brown, Black, Brown, Gold) | Headlight limiter (D9) — Col 04 (Rows 18 to 21) |
| **R2** | 1/4W Resistor | **$150\Omega$** (Brown, Green, Brown, Gold) | Front Left Blinker (D10) — Col 05 (Rows 18 to 21) |
| **R3** | 1/4W Resistor | **$150\Omega$** (Brown, Green, Brown, Gold) | Front Right Blinker (D11) — Col 06 (Rows 18 to 21) |
| **R7** | 1/4W Resistor | **$150\Omega$** (Brown, Green, Brown, Gold) | Rear Right Blinker (D8) — Col 08 (Rows 18 to 21) |
| **R6** | 1/4W Resistor | **$150\Omega$** (Brown, Green, Brown, Gold) | Rear Left Blinker (D7) — Col 09 (Rows 18 to 21) |
| **R5** | 1/4W Resistor | **$150\Omega$** (Brown, Green, Brown, Gold) | Brake Light limiter (D6) — Col 10 (Rows 18 to 21) |
| **R4** | 1/4W Resistor | **$150\Omega$** (Brown, Green, Brown, Gold) | Tail Light limiter (D5) — Col 11 (Rows 18 to 21) |
| **CON1**| 90° Pin Header | **1x5 Male Right-Angle (2.54mm)** | **Left Edge** (Col 02, Rows 05 to 09) — FS-BS6 Radio |
| **CON4**| 90° Pin Header | **1x4 Male Right-Angle (2.54mm)** | **Right Edge** (Col 17, Rows 07 to 10) — MPU-6050 I2C |
| **CON2**| 90° Pin Header | **1x4 Male Right-Angle (2.54mm)** | **Bottom-Left Edge** (Row 24, Cols 03 to 06) — Front Lights |
| **CON3**| 90° Pin Header | **1x6 Male Right-Angle (2.54mm)** | **Bottom Center-Right Edge** (Row 24, Cols 08 to 13) — Rear Lights |
