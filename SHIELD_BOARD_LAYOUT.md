# Shield Hub Board Engineering Design (5x7 cm) — Natural Distributed Layout v7.2

[🇧🇷 **Versão em Português (PLACA_SHIELD_LAYOUT.md)**](PLACA_SHIELD_LAYOUT.md) | [🇺🇸 **English Version**](#-english) | [📜 **Official Premises (PREMISSAS_PROJETO.md)**](PREMISSAS_PROJETO.md)

---

## 🇺🇸 English

This document provides the complete assembly design for the **Hub Shield Board** built on a **universal 5x7 cm perfboard (standard 2.54mm / 0.1" pitch)** featuring the **Natural Distributed Layout (v7.2)**:
- **Arduino Nano** positioned at the top with its **USB port facing outwards (top edge, Rows 01-02)** and **real physical pinout** (Left Header: D13 at top down to VIN at bottom; Right Header: D12 at top down to D1/TX at bottom).
- **CON1 (FlySky FS-BS6 Radio 1x5 90°)** on the **Right Board Edge** (Column 17, Rows 11 to 15) — **Primary VCC (+5V) and Master GND Power Input**! Direct horizontal traces of **only 10 mm** to D4 (CH1), D3 (CH4), D2 (CH2), and GND.
- **Filter / Regulation Capacitor C1 ($100\mu\text{F} \times 16\text{V}$)** mounted **directly at the power entrance** (Column 15, Rows 14 and 15), soldered side-by-side with CON1 Pins 1 (+5V) and 2 (GND) and Nano GND.
- **CON4 (MPU-6050 1x4 90°)** on the **Left Board Edge** (Column 02, Rows 10 to 13) — direct traces of **only 10 mm** to A4 (SDA), A5 (SCL), +5V, and GND!
- **CON2 (Front Light Harness 1x4 90°)** on the **Bottom-Left Edge** (Row 24, Columns 03 to 06).
- **CON3 (Rear Light Harness 1x6 90°)** on the **Bottom Center-Right Edge** (Row 24, Columns 08 to 13).
- **Unified Continuous Master GND Bus:** Continuous loop connecting CON1 P2, C1(-), Nano GND Right, Nano GND Left, CON2, CON3, and CON4.
- **Optimized Hybrid Routing:** Solder traces on underside without overlaps + 4 top insulated jumper wires to guarantee ZERO short-circuits with absolute geometric integrity (Headlight D9, Blinker D10, Nano +5V, and GND Cross-Tie).

> [!IMPORTANT]
> ### ⚡ ESSENTIAL PROJECT PREMISES:
> 1. **Power Origin:** Main VCC (+5V) and Master GND originate exclusively from the Radio Harness (**CON1 via CH6 / ESC BEC**). No other connector powers the board.
> 2. **Nominal Voltage:** Designed for nominal **5.0V** BEC systems. If a 6.0V+ BEC is used, insert a 1N4007 diode in series on CON1 Pin 1 to drop ~0.7V prior to Nano 5V.
> 3. **Regulation at Entrance:** Capacitor **C1 ($100\mu\text{F}$)** is soldered immediately across CON1 Pins 1 (+5V) and 2 (GND) at Column 15, absorbing motor EMI and servo transients right at the board's entrance.
> 4. **Master GND Bus:** CON1 Pin 2 is the vehicle's absolute 0V reference, interconnected across the entire board independently of whether the Nano module is socketed.
> 5. **Top Insulated Jumper Wires:** Due to the Nano's real physical pinout (LED outputs D9-D11 on the right side and resistors R1-R3 on the left side), 4 connections use small insulated wires on the top side to hop over components without sharing copper pads on the underside.
> *Refer to [PREMISSAS_PROJETO.md](PREMISSAS_PROJETO.md) for complete engineering documentation.*

> [!TIP]
> ### 🌟 GRAPHICAL & INTERACTIVE BOARD MODELS AVAILABLE:
> - 🌐 **[Open Interactive Board Visualizer (HTML)](placa_shield_visualizador.html)** — **Recommended!** Fullscreen in-browser viewer with instant toggle between **Top View (Components)**, **Bottom View (Soldering / Verso Traces)**, and **X-Ray**, featuring **fully connected visible wiring in all views** and dynamic circuit highlights.
> - 🖼️ **[Component Top View Vector Diagram (SVG)](placa_shield_superior.svg)** — Clean top view showing Arduino Nano, C1 at entrance, resistors, and connected traces.
> - 🔄 **[Solder Bottom View Vector Diagram (SVG)](placa_shield_inferior.svg)** — Horizontally mirrored view matching how you see the board while soldering, with heavy solder traces and unified ground bus.
> - 📸 **[Realistic 3D Assembled Board Render (JPG)](placa_shield_3d.jpg)** — Physical assembly 3D perspective visualization.

---

### 📐 1. Board Coordinates Matrix (18 Columns x 24 Rows Grid) — Distributed v7.2

```
       01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18  (Columns)
 01 [  ╔═════════════════[+5V TOP ROW 01]══════════════════╗  ] 01 ◄── Perimeter +5V Solder Trace
 02 [  ║   .  .  .  . ┌───[USB NANO]───┐ .  .  .  .  .  .  ║  ] 02
 03 [  ║   .  .  .  . │[D13]          [D12]│.  │  .  .  .  ║  ] 03
 04 [  ║   .  .  .  . │[3V3]     ╔════[D11]│.  │  .  .  .  ║  ] 04 ◄── D11 (B.FR via Col 07)
 05 [  ║   .  .  .  . │[REF]     ║    [D10]│.  │  .  .  .  ║  ] 05 ◄── D10 ➔ Direct Jumper to R2 Top
 06 [  ║   .  .  .  . │[A0]      ║    [D9] │.  │  .  .  .  ║  ] 06 ◄── D9  ➔ Direct Jumper to R1 Top
 07 [  ║   .  .  .  . │[A1]      ║    [D8] │═══╬═══╗  .  . ║  ] 07 ◄── D8 (B.RR)
 08 [  ║   .  .  .  . │[A2]      ║    [D7] │═══╬═══╬═══╗ . ║  ] 08 ◄── D7 (B.RL)
 09 [  ║   .  .  .  . │[A3]      ║    [D6] │═══╬═══╬═══╬══ ║  ] 09 ◄── D6 (Brake)
 10 [  ║ .[SDA]───────│[A4]      ║    [D5] │═══╬═══╬═══╬══ ║  ] 10 ◄── D5 (Tail) & CON4 SDA
 11 [  ║ .[SCL]───────│[A5]      ║    [D4] │───╫───╫───╫── ║  ] 11 ◄── CON1 P5 (CH1) & CON4 SCL
 12 [  ╠═.[+5V]       │[A6]      ║    [D3] │───╫───╫───╫── ║  ] 12 ◄── CON1 P4 (CH4) & CON4 +5V Branch
 13 [  . .[GND]───┐   │[A7]      ║    [D2] │───╫───╫───╫── ║  ] 13 ◄── CON1 P3 (CH2) & CON4 GND
 14 [ [Jmp5V]·····│···│[5V]      ║    [GND]│───╫───╫─[C1-][GND] ] 14 ◄── CON1 P2 (GND), C1(-), Nano GND
 15 [  .  CON4    │   │[RST]     ║    [RST]│   ║   ║ [C1+][+5V]═╝ ] 15 ◄── CON1 P1 (+5V) ➔ Climbs Col 18
 16 [  ╔══(GND)───┴───│[GND]·····║····(Jmp)│   ║   ║   │  CON1  ] 16 ◄── Jumper GND Cross-Tie (12,14➔06,16)
 17 [  ║  (90°)       │[VIN]     ║    [TX] │   ║   ║   │  (90°) ] 17
 18 [  ║              │          ▼    [R7][R6][R5][R4] │        ] 18 ◄── RESISTOR TOPS
 19 [  ║             [R1] [R2]  [R3]   │   │   │   │   │        ] 19
 20 [  ║              │    │     │     │   │   │   │   │        ] 20
 21 [  ║             [┴]  [┴]   [┴]   [┴] [┴] [┴] [┴]  │        ] 21 ◄── RESISTOR BASES
 22 [  ║              │    │     │     │   │   │   │   │        ] 22
 23 [  ║              │    │     │     │   │   │   │   │        ] 23
 24 [  ╚══════════════╡    │     │     │   │   │   │   │  [GND] ] 24 ◄── CON2 (Cols 03-06) & CON3 (08-13)
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
│         [D13]  (o)   │                        │   (o)  [D12]           │
│         [3V3]  (o)   │                        │   (o)  [D11/B.FR]══╗   │
│         [REF]  (o)   │                        │   (o)  [D10/B.FL]··╫·┐ │ (Jumper D10)
│         [A0]   (o)   │                        │   (o)  [D9/Head] ··╫─┼┐│ (Jumper D9)
│         [A1]   (o)   │                        │   (o)  [D8/BRR]    ║ │││
│         [A2]   (o)   │                        │   (o)  [D7/BRL]    ║ │││
│         [A3]   (o)   │                        │   (o)  [D6/Brake]  ║ │││
│   ┌─────[A4/SDA](o)  │                        │   (o)  [D5/Tail]   ║ │││
│  ┌┼─────[A5/SCL](o)  │                        │   (o)  [D4/CH1]──┐ ║ │││
│  ││     [A6]   (o)   │                        │   (o)  [D3/CH4]─┐│ ║ │││
│  ││     [A7]   (o)   │                        │   (o)  [D2/CH2]┐││ ║ │││
│  ││ ┌···[5V]   (o)   │                        │   (o)  [GND]───┼┼┼─╫─┼┼┤ [CON1 P2]
│  ││ │ ┌─[GND]  (o)···┼························┼···(o)  (JmpGND)│││ ║ ││││
│  ││ │ │ [VIN]  (o)   │                        │   (o)  [TX]    │││ ║ ││││
│┌─┴┴─┴─┴─────┐        │                        │                │││ ║ ││││
││CON4: MPU   │        │                        │               ┌┴┴┴─┴─┴┴┤
││(1x4 90°    │        │                        │               │CON1:   │
││Left Edge)  │        │                        │               │RADIO   │
││[4: SDA]◄───┘        │                        │               │(1x5 90°│
││[3: SCL]◄───┘        │                        │      [CH1 :5]◄┼────────┘
││[2: +5V]◄──┐         │                        │      [CH4 :4]◄┼───────┘
││[1: GND]◄──┼┐        └────────────────────────┘      [CH2 :3]◄┼──────┘
│└┬──────────┼┴─────────┐       ║  ║  ║                [GND :2]◄┼─C1(-)
│ ▼ (90° Pins           │       ║  ║  ║                [+5V :1]◄┼─C1(+) ➔ Col 18
│ point left)           │       ║  ║  ║                └┬───────┘
│                       │       ║  ║  ║                 ▼ (90° Pins right)
│                       │       ║  ║  ║
│                 [R1]  ▼ [R2]  ▼[R3] ▼[R7][R6][R5][R4]
│                 100Ω    150Ω   150Ω  150Ω 150Ω 150Ω 150Ω
│                (Head)  (B.FL) (B.FR) (BRR)(BRL)(Brk)(Tai)
│                  │       │      │      │   │   │   │
│                  ▼       ▼      ▼      ▼   ▼   ▼   ▼
│         ┌───────────────────────┐   ┌────────────────────────┐
│         │ CON2: FRONT (1x4 90°) │   │ CON3: REAR (1x6 90°)   │
│         │┌─────┬───────┬──────┬─┴─┐ │┌───┬───┬───┬───┬───┬──┐│
│         ││ GND │ Head  │B.FL  │B.FR│││BRR│BRL│Brk│Tai│NC │GND│
│         │└──┬──┴───┬───┴──┬───┴───┘ │└─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬┘│
│         └───┼──────┼──────┼─────────┘└──┼───┼───┼───┼───┼───┼──┘
│             │      │      │             │   │   │   │   │   │
│             │      ▼      ▼             ▼   ▼   ▼   ▼   │   │
│             │    (90° Pins point outward from bottom)   │   │
│             │                                               │
│             └══════ (GND via Col 01)   (GND via Col 13) ════╝
└────────────────────────────────────────────────────────────────────────┘
```

---

### 🔌 3. Solder Routing (Bottom View & Top Jumpers)

The **Natural Distributed Layout v7.2** eliminates 100% of short-circuits via **dedicated perimeter routing channels** and **4 top insulated jumper wires**:

#### 📻 A. Radio Channel & Entrance Regulation (Right Edge — 10mm Short Traces!)
CON1 is on **Column 17 (Rows 11 to 15)**, directly facing Nano control pins and capacitor C1:
* **CON1 Pin 5 (CH1 Steering, Col 17, Row 11):** Direct horizontal solder trace to **Nano D4** (Col 12, Row 11) $\rightarrow$ **10 mm trace!**
* **CON1 Pin 4 (CH4 Headlight, Col 17, Row 12):** Direct horizontal solder trace to **Nano D3** (Col 12, Row 12) $\rightarrow$ **10 mm trace!**
* **CON1 Pin 3 (CH2 Throttle, Col 17, Row 13):** Direct horizontal solder trace to **Nano D2** (Col 12, Row 13) $\rightarrow$ **10 mm trace!**
* **CON1 Pin 2 (Master GND, Col 17, Row 14):** Directly solders to **C1(-)** (Col 15, Row 14) and to **Nano GND Right** (Col 12, Row 14) $\rightarrow$ **Central 0V Reference Node!**
* **CON1 Pin 1 (+5V BEC Master Input, Col 17, Row 15):** Directly solders to **C1(+)** (Col 15, Row 15), routes along unobstructed outer **Column 18** up to Row 01 at the top, crosses over to outer **Column 01** on the left margin, and drops down to Row 14:
  - Branch at (Col 01, Row 12) $\rightarrow$ **CON4 Pin 2 (+5V MPU)**.
  - Jumper point at (Col 01, Row 14) $\rightarrow$ **Top insulated wire (~13mm)** hopping over to **Nano +5V** (Col 06, Row 14).

#### 🧭 B. MPU-6050 Channel (Left Edge — 10mm Short Traces!)
CON4 is on **Column 02 (Rows 10 to 13)**, directly facing Nano I2C pins and power:
* **CON4 Pin 4 (SDA, Col 02, Row 10):** Direct horizontal solder trace to **Nano A4** (Col 06, Row 10) $\rightarrow$ **10 mm trace!**
* **CON4 Pin 3 (SCL, Col 02, Row 11):** Direct horizontal solder trace to **Nano A5** (Col 06, Row 11) $\rightarrow$ **10 mm trace!**
* **CON4 Pin 2 (+5V, Col 02, Row 12):** Connected directly to the branch of the perimeter +5V master bus (Col 01 $\rightarrow$ Col 02).
* **CON4 Pin 1 (GND, Col 02, Row 13):** Soldered to the left ground rail joined to **Nano GND Left** (Col 06, Row 16).

#### 💡 C. Front LED Channel (Direct Jumpers & Central Channel)
* **D9 (Headlight):** Top insulated wire (jumper ~36mm) directly from **Nano D9** (Col 12, Row 06) to **R1 Top** (Col 04, Row 18) $\rightarrow$ on underside, straight solder trace from **R1 Bot** (Col 04, Row 21) to **CON2 Pin 2** (Headlight).
* **D10 (Front Left Blinker):** Top insulated wire (jumper ~38mm) directly from **Nano D10** (Col 12, Row 05) to **R2 Top** (Col 05, Row 18) $\rightarrow$ on underside, straight solder trace from **R2 Bot** (Col 05, Row 21) to **CON2 Pin 3** (B.FL).
* **D11 (Front Right Blinker):** Underside solder trace from **Nano D11** (Col 12, Row 04) through the free central channel of **Column 07** down to Row 17 $\rightarrow$ enters **R3 Top** (Col 06, Row 18) $\rightarrow$ **R3 Bot** (Col 06, Row 21) $\rightarrow$ **CON2 Pin 4** (B.FR).
* **CON2 Pin 1 (GND, Col 03, Row 24):** Fed by **Column 01** on the outer perimeter margin.

#### 💡 D. Rear LED Channel (Nested L-Traces — Zero Crossovers!)
The 4 rear LED outputs utilize planar nested L-traces on the board underside:
* **D8 (Rear Right Blinker, Row 07):** Nano D8 (Col 12, Row 07) runs on Row 07 to **Col 08** $\rightarrow$ drops to **R7 Top** (Col 08, Row 18) $\rightarrow$ **R7 Bot** (Col 08, Row 21) $\rightarrow$ **CON3 Pin 1** (B.RR).
* **D7 (Rear Left Blinker, Row 08):** Nano D7 (Col 12, Row 08) runs on Row 08 to **Col 09** $\rightarrow$ drops to **R6 Top** (Col 09, Row 18) $\rightarrow$ **R6 Bot** (Col 09, Row 21) $\rightarrow$ **CON3 Pin 2** (B.RL).
* **D6 (Brake, Row 09):** Nano D6 (Col 12, Row 09) runs on Row 09 to **Col 10** $\rightarrow$ drops to **R5 Top** (Col 10, Row 18) $\rightarrow$ **R5 Bot** (Col 10, Row 21) $\rightarrow$ **CON3 Pin 3** (Brake).
* **D5 (Tail, Row 10):** Nano D5 (Col 12, Row 10) runs on Row 10 to **Col 11** $\rightarrow$ drops to **R4 Top** (Col 11, Row 18) $\rightarrow$ **R4 Bot** (Col 11, Row 21) $\rightarrow$ **CON3 Pin 4** (Tail).
* **CON3 Pin 5 (NC, Col 12, Row 24):** Unconnected / Mechanical key.
* **CON3 Pin 6 (GND, Col 13, Row 24):** Fed directly by the unobstructed vertical channel of Column 13.

---

### 📋 3.1 Point-to-Point Master Soldering Schedule

| Step | Net / Signal | Origin (From) | Destination (To) | Physical Connection Type |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **🔴 Perimeter +5V Bus** | **CON1 Pin 1** (Col 17, Row 15) | **C1(+)** (Col 15, Row 15) $\rightarrow$ Col 18 $\rightarrow$ Top Row 01 $\rightarrow$ Margin Col 01 $\rightarrow$ Row 14 | Perimeter solder trace along board edges |
| **1b**| **🔴 MPU +5V Branch** | **Margin Col 01** (Col 01, Row 12) | **CON4 Pin 2** (Col 02, Row 12) | Direct 1-pad horizontal trace |
| **1c**| **⚡ Nano +5V Jumper** | **Margin Col 01** (Col 01, Row 14) | **Nano +5V** (Col 06, Row 14) | **Top insulated wire (~13mm jumper)** hopping over board |
| **2** | **⚡ Master GND Entrance** | **CON1 Pin 2** (Col 17, Row 14) | **C1(-)** (Col 15, Row 14) & **Nano GND Right** (Col 12, Row 14) | Direct horizontal solder trace (Row 14) |
| **2b**| **⚡ GND Cross-Tie Jumper**| **Nano GND Right** (Col 12, Row 14) | **Nano GND Left** (Col 06, Row 16) | **Top insulated wire (~16mm jumper)** linking ground planes |
| **3** | **📻 Radio CH2** | **CON1 Pin 3** (Col 17, Row 13) | **Nano D2** (Col 12, Row 13) | Direct 10mm horizontal trace (Row 13) |
| **4** | **📻 Radio CH4** | **CON1 Pin 4** (Col 17, Row 12) | **Nano D3** (Col 12, Row 12) | Direct 10mm horizontal trace (Row 12) |
| **5** | **📻 Radio CH1** | **CON1 Pin 5** (Col 17, Row 11) | **Nano D4** (Col 12, Row 11) | Direct 10mm horizontal trace (Row 11) |
| **6** | **🧭 MPU SDA** | **CON4 Pin 4** (Col 02, Row 10) | **Nano A4** (Col 06, Row 10) | Direct 10mm horizontal trace (Row 10) |
| **7** | **🧭 MPU SCL** | **CON4 Pin 3** (Col 02, Row 11) | **Nano A5** (Col 06, Row 11) | Direct 10mm horizontal trace (Row 11) |
| **8** | **⚡ Left GND & MPU** | **Nano GND Left** (Col 06, Row 16) | Row 16 to Col 02 $\rightarrow$ climbs Col 02 to **CON4 P1** (Col 02, Row 13) | Underside solder trace |
| **9** | **⚡ Front GND (CON2)** | **Point (Col 02, Row 16)** | Outer Col 01 down to **CON2 P1** (Col 03, Row 24) | Unobstructed perimeter solder trace |
| **10**| **⚡ Rear GND (CON3)** | **Nano GND Right** (Col 12, Row 14) | Straight down Column 13 to **CON3 P6** (Col 13, Row 24) | Unobstructed vertical solder trace |
| **11**| **💡 Headlights (D9)** | **Nano D9** (Col 12, Row 06) | **R1 Top** (Col 04, Row 18) | **Top insulated wire (~36mm jumper)** |
| **11b**|**💡 Headlight Output** | **R1 Bot** (Col 04, Row 21) | **CON2 P2** (Col 04, Row 24) | Straight vertical trace on underside |
| **12**| **💡 Front Left Blinker (D10)**| **Nano D10** (Col 12, Row 05) | **R2 Top** (Col 05, Row 18) | **Top insulated wire (~38mm jumper)** |
| **12b**|**💡 Front Left Blinker Out** | **R2 Bot** (Col 05, Row 21) | **CON2 P3** (Col 05, Row 24) | Straight vertical trace on underside |
| **13**| **💡 Front Right Blinker (D11)**| **Nano D11** (Col 12, Row 04) | Row 04 to Col 07 $\rightarrow$ drops Col 07 to **R3 Top** (Col 06, Row 18) | L-trace on underside |
| **13b**|**💡 Front Right Blinker Out**| **R3 Bot** (Col 06, Row 21) | **CON2 P4** (Col 06, Row 24) | Straight vertical trace on underside |
| **14**| **💡 Rear Right Blinker (D8)**| **Nano D8** (Col 12, Row 07) | Row 07 to Col 08 $\rightarrow$ **R7 Top** (Col 08, Row 18) $\rightarrow$ **R7 Bot** $\rightarrow$ **CON3 P1** | Nested L-trace on underside |
| **15**| **💡 Rear Left Blinker (D7)** | **Nano D7** (Col 12, Row 08) | Row 08 to Col 09 $\rightarrow$ **R6 Top** (Col 09, Row 18) $\rightarrow$ **R6 Bot** $\rightarrow$ **CON3 P2** | Nested L-trace on underside |
| **16**| **💡 Brake Lights (D6)** | **Nano D6** (Col 12, Row 09) | Row 09 to Col 10 $\rightarrow$ **R5 Top** (Col 10, Row 18) $\rightarrow$ **R5 Bot** $\rightarrow$ **CON3 P3** | Nested L-trace on underside |
| **17**| **💡 Tail Lights (D5)** | **Nano D5** (Col 12, Row 10) | Row 10 to Col 11 $\rightarrow$ **R4 Top** (Col 11, Row 18) $\rightarrow$ **R4 Bot** $\rightarrow$ **CON3 P4** | Nested L-trace on underside |

---

### 📋 4. Complete Bill of Materials (BOM)

| Designator | Component | Description / Value | Purpose and Location |
| :---: | :--- | :--- | :--- |
| **U1** | Arduino Nano Socket | 2x Female Header 1x15 (2.54mm Pitch) | Columns 06 and 12 (Rows 03 to 17) |
| **U2** | MPU-6050 (GY-521) | 3D Inertial Sensor Module | Mounted on chassis via CON4 harness |
| **C1** | Electrolytic Capacitor | **$100\mu\text{F} \times 16\text{V}$** | **Column 15 (Rows 14 and 15)**, at CON1 power entrance |
| **R1** | 1/4W Resistor | **$100\Omega$** (Brown, Black, Brown, Gold) | Headlight Limiter (D9) — Col 04 (Rows 18 to 21) |
| **R2** | 1/4W Resistor | **$150\Omega$** (Brown, Green, Brown, Gold) | Front Left Blinker Limiter (D10) — Col 05 (Rows 18 to 21) |
| **R3** | 1/4W Resistor | **$150\Omega$** (Brown, Green, Brown, Gold) | Front Right Blinker Limiter (D11) — Col 06 (Rows 18 to 21) |
| **R7** | 1/4W Resistor | **$150\Omega$** (Brown, Green, Brown, Gold) | Rear Right Blinker Limiter (D8) — Col 08 (Rows 18 to 21) |
| **R6** | 1/4W Resistor | **$150\Omega$** (Brown, Green, Brown, Gold) | Rear Left Blinker Limiter (D7) — Col 09 (Rows 18 to 21) |
| **R5** | 1/4W Resistor | **$150\Omega$** (Brown, Green, Brown, Gold) | Brake Light Limiter (D6) — Col 10 (Rows 18 to 21) |
| **R4** | 1/4W Resistor | **$150\Omega$** (Brown, Green, Brown, Gold) | Tail Light Limiter (D5) — Col 11 (Rows 18 to 21) |
| **CON1** | 90° Male Pin Header | **1x5 90° Male Header** | **Right Board Edge** (Col 17, Rows 11 to 15) — Radio Input |
| **CON4** | 90° Male Pin Header | **1x4 90° Male Header** | **Left Board Edge** (Col 02, Rows 10 to 13) — MPU-6050 I2C |
| **CON2** | 90° Male Pin Header | **1x4 90° Male Header** | **Bottom-Left Edge** (Row 24, Cols 03 to 06) — Front Harness |
| **CON3** | 90° Male Pin Header | **1x6 90° Male Header** | **Bottom Center-Right** (Row 24, Cols 08 to 13) — Rear Harness |
| **W1-W4**| Insulated Jumper Wires | **4x Stranded insulated wire (28-30 AWG)** | Top side: D9 (~36mm), D10 (~38mm), +5V (~13mm) and GND (~16mm) |

---

## 🇧🇷 Português

Consulte [PLACA_SHIELD_LAYOUT.md](PLACA_SHIELD_LAYOUT.md) para a documentação técnica completa em Português com a matriz de coordenadas e especificações de montagem.
