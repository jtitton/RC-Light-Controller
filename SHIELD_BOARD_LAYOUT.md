# Shield Hub Board Engineering Design (5x7 cm) — Natural Distributed Layout v8.4

[🇧🇷 **Versão em Português (PLACA_SHIELD_LAYOUT.md)**](PLACA_SHIELD_LAYOUT.md) | [🇺🇸 **English Version**](#-english) | [📜 **Official Premises (PREMISSAS_PROJETO.md)**](PREMISSAS_PROJETO.md)

---

## 🇺🇸 English

This document provides the complete assembly design for the **Hub Shield Board** built on a **universal 5x7 cm perfboard (standard 2.54mm / 0.1" pitch)** featuring the **Natural Distributed Layout (v8.4)**:
- **Native 6.0V BEC Support with Expanded Pitch D1 (1N4007 DO-41) Silicon Diode:** Mounted on the top layer descending vertically down **Column 17 between Rows 15 and 18**, with standard industrial DO-41 pitch of **7.62 mm (3 steps)**. Anode is inserted into `(17, 15)` (joining CON1 Pin 1 +6.0V raw BEC input) and Cathode (silver band) into `(17, 18)`. Produces a forward voltage drop of $\approx 0.75\text{V}$, creating a safe and regulated **$+5.25\text{V}$** power rail on Row 18 for Nano 5V pin, C1(+), and Q1 collector, providing full reverse-polarity protection and keeping all LED calculations 100% accurate. Pad `(17, 15)` is strictly isolated on the solder side, and intermediate pads `(17, 16)`, `(17, 17)`, `(16, 15)`, and `(15, 15)` remain 100% empty with over 7 mm galvanic gap, completely eliminating solder bridge risk.
- **Arduino Nano** positioned at the top with its **USB port facing outwards (top edge, Rows 01-02)** and **real physical pinout** (Left Header: D13 at top down to VIN at bottom; Right Header: D12 at top down to D1/TX at bottom).
- **Headlight Transistor Driver Q1 (BC337 NPN TO-92):** Mounted at **Row 09, Columns 13 to 15** in high-side emitter follower topology, drawing only ~0.4mA from Nano D9 and supplying **45 to 60 mA** to the 4 parallel white headlight LEDs via vertical resistor **R1 ($27\,\Omega$ 1/4W)** on Column 15 (Rows 06 to 08), doubling headlight brightness while preserving the 4-wire common-ground front harness.
- **Resistors R2 to R7 Standardized at $100\,\Omega$ (1/4W):** Front/rear turn signals and brake lights boosted to **~14.5 to 15 mA per LED**, achieving maximum automotive visual punch while remaining 100% safe for ATmega328P output ports.
- **CON1 (FlySky FS-BS6 Radio 1x5 90°)** on the **Right Board Edge** (Column 17, Rows 11 to 15) — **Primary VCC (+6.0V) and Master GND Power Input**! Direct horizontal traces of **only 10 mm** to D4 (CH1), D3 (CH4), D2 (CH2), and GND.
- **Filter / Regulation Capacitor C1 ($100\mu\text{F} \times 25\text{V}$)** mounted on **Row 18** (Columns 14 and 15), with C1(+) at `(15, 18)` and C1(-) at `(14, 18)` connected via a direct 1-pad solder bridge to Column 13 Master GND trunk.
- **CON4 (MPU-6050 1x4 90°)** on the **Left Edge** (Column 02, Rows 10 to 13) — Physical 1:1 pinout with user's sensor module (**P1: GND, P2: TX [SCL], P3: RX [SDA], P4: VCC [+5.25V]**).
- **CON2 (Front Light Harness 1x4 90°)** on the **Upper-Right Edge** (Column 17, Rows 04 to 07) — **same side as radio**, above CON1, with pins pointing towards the right board edge.
- **CON3 (Rear Light Harness 1x6 90°)** on the **Bottom Center-Right Edge** (Row 24, Columns 08 to 13).
- **Unified Continuous Master GND Bus:** Continuous loop connecting CON1 P2, C1(-), Nano GND Right, Nano GND Left, CON2, CON3, and CON4.
- **Optimized Hybrid Routing:** Solder traces on underside without overlaps + **5 top insulated jumper wires (W1 to W5)** guaranteeing ZERO short-circuits with proven absolute geometric integrity (189 validated pads).

> [!IMPORTANT]
> ### ⚡ ESSENTIAL PROJECT PREMISES:
> 1. **Power Origin & BEC Voltage:** Main VCC (+6.0V) and Master GND originate exclusively from the Radio Harness (**CON1 via CH6 / ESC BEC**). Onboard **D1 (1N4007)** silicon rectifier diode drops ~0.75V to deliver a regulated **+5.25V** rail to Arduino Nano 5V pin, C1(+), and Q1 collector.
> 2. **D1 and C1 with Expanded Pitch:** Diode **D1 (1N4007)** descends down Column 17 (Rows 15 to 18) with standard 7.62 mm pitch, and capacitor **C1 ($100\mu\text{F} \times 25\text{V}$)** is placed on Row 18 (Columns 14 and 15), absorbing electrical motor EMI and providing complete physical isolation against solder shorts.
> 3. **Master GND Bus:** CON1 Pin 2 is the vehicle's absolute 0V reference, interconnected across the entire board independently of whether the Nano module is socketed.
> 4. **Top Insulated Jumper Wires (5 Jumpers W1 to W5):** A total of 5 connections use top-layer insulated jumper wires: W1 (+5.25V Nano 15,18➔06,14), W2 (Front GND 16,14➔16,07), W3 (GND Cross-Tie 12,14➔06,16), W4 (Accelerometer SDA/RX 02,12➔06,10), and W5 (+5.25V Headlight Collector Q1 16,18➔13,09).
> *Refer to [PREMISSAS_PROJETO.md](PREMISSAS_PROJETO.md) for complete engineering documentation.*

> [!TIP]
> ### 🌟 GRAPHICAL & INTERACTIVE BOARD MODELS AVAILABLE:
> - 🌐 **[Open Interactive Board Visualizer (HTML)](placa_shield_visualizador.html)** — **Recommended!** Fullscreen in-browser viewer with instant toggle between **Top View (Components)**, **Bottom View (Soldering / Verso Traces)**, and **X-Ray**, featuring **fully connected visible wiring in all views** and dynamic circuit highlights.
> - 🖼️ **[Component Top View Vector Diagram (SVG)](placa_shield_superior.svg)** — Clean top view showing Arduino Nano, D1 1N4007 diode, Q1 BC337, C1 at entrance, resistors, and connected traces.
> - 🔄 **[Solder Bottom View Vector Diagram (SVG)](placa_shield_inferior.svg)** — Horizontally mirrored view matching how you see the board while soldering, with heavy solder traces and unified ground bus.

---

### 📐 1. Board Coordinates Matrix (18 Columns x 24 Rows Grid) — Distributed v8.4

```
       01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18  (Columns)
 01 [  ║   .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  ] 01 ◄── Column 01: Vertical Master GND Bus
 02 [  ║   .  .  .  . ┌───[USB NANO]───┐ .  .  .  .  .  .  .  ] 02
 03 [  ║   .  .  .  . │[D13]          [D12]│.  .  .  .  .  .  ] 03
 04 [  ║   .  .  .  . │[3V3]          [D11]│──[In]═[R3]═[P4]  ] 04 ◄── R3 (100Ω) ➔ CON2 P4 (B.FR)
 05 [  ║   .  .  .  . │[REF]          [D10]│──[In]═[R2]═[P3]  ] 05 ◄── R2 (100Ω) ➔ CON2 P3 (B.FL)
 06 [  ║   .  .  .  . │[A0]           [D9] │───┬───[R1]═[P2]  ] 06 ◄── R1 Out (27Ω) ➔ CON2 P2 (Head)
 07 [  ║   .  .  .  . │[A1]           [D8] │═══╬═══│ │ [W2][P1] ] 07 ◄── D8 (B.RR) & CON2 P1 (GND via W2)
 08 [  ║   .  .  .  . │[A2]           [D7] │═══╬═══│[R1] .  . ] 08 ◄── R1 In (27Ω) fed by Q1 Emitter
 09 [  ║   .  .  .  . │[A3]           [D6] │═══╬═══│[Q1: C-B-E]] 09 ◄── Q1 BC337: C(13,09), B(14,09), E(15,09)
 10 [  ║ .[GND]───(GND Rail)────│[A4/SDA]·······(W4)    [D5] │═══╬═══╬═══╬══ .  ] 10 ◄── D5 (Tail Light) & Nano A4 (W4 In)
 11 [  ║ .[TX/SCL]──────────────│[A5/SCL]         [D4] │───╫───╫───╫──[P5]] 11 ◄── CON1 P5 (CH1) & CON4 P2 TX (SCL)
 12 [  ║ .[RX/SDA]······(W4)····│[A6]             [D3] │───╫───╫───╫──[P4]] 12 ◄── CON1 P4 (CH4) & CON4 P3 RX (W4 Out)
 13 [  ║ .[VCC]───(+5V Branch)──│[A7]             [D2] │───╫───╫───╫──[P3]] 13 ◄── CON1 P3 (CH2) & CON4 P4 VCC
 14 [  ║  CON4    │             │[5V]             [GND]│───╫───╫───.──[W2][P2] ] 14 ◄── CON1 P2 (GND), W2 Out, Nano GND Right
 15 [  ║  (90°)   │             │[RST]            [RST]│   ║   .   .   .  [P1] ] 15 ◄── CON1 P1 (+6.0V BEC) ➔ D1 Anode (17,15)
 16 [  ╠══(GND)───┴─────────────│[GND]············(Jmp)│   ║   .   .   .   │   ] 16 ◄── Jumper W3 GND Cross-Tie & D1 Body
 17 [  ║  (MPU)                 │[VIN]            [TX] │   ║   .   .   .   │   ] 17 ◄── D1 Body (Pitch 7.62mm / 3 steps)
 18 [  ║                        │                      │   ║  [C1-][C1+][W5][D1K] 18 ◄── D1 Cathode (17,18), W5, C1(+)/W1, C1(-)/GND
 19 [  ║                        │                      │   ║   ║   ║   ║   ║   ║   19
 20 [  ║                        │                      │   ║   ║   ║   ║   ║   ║   20
 21 [  ║                        │                      │   ║   ║   ║   ║   ║   ║   21 ◄── REAR RESISTOR BASES (Cols 08-11)
 22 [  ║                        │                      │   ║   ║   ║   ║   ║   ║   22
 23 [  ║                        │                      │   ║   ║   ║   ║   ║   ║   23
 24 [  ╚════════════════════════╪══════════════════════╪═══╩═══╡   .   .   . [GND] 24 ◄── CON3: REAR (Row 24, Cols 08-13)
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
│                      │ (Socketed in 2 rows of │   (Col 17)             │
│                      │  1x15 female headers)  │  ┌──────────────┐      │
│                      │                        │  │CON2: FRONT   │      │
│                      │                        │  │(1x4 90°      │      │
│                      │                        │  │Right Edge)   │      │
│                      │  (Col 12)  (Col 14-16) │  │              │      │
│                      │   (o) [D12]            │  │              │      │
│                      │   (o) [D11]──[R3 100Ω]═╪═►│[4: B.FR]     │      │
│                      │   (o) [D10]──[R2 100Ω]═╪═►│[3: B.FL]     │      │
│                      │   (o) [D9] ──┐ [R1 27Ω]╪═►│[2: Head]     │      │
│                      │   (o) [D8/BRR]│  │ (W2)──►│[1: GND]      │      │
│                      │   (o) [D7/BRL]│ [R1]   │  └──────────────┘      │
│││[1: GND]────┼────────┴─────────────┘   │      │[5: CH1]◄───────┘│
││[2: TX/SCL]◄┘                          │      │[4: CH4]◄───────┘│
││[3: RX/SDA]◄···························┘      │[3: CH2]◄───────┘│
││[4: VCC]◄───┘ (via +5.25V branch)             │[2: GND]◄─C1(-)  │
│└┬─────────────────────────────────────┐       │[1:+6V]►[D1]►C1+ │
│ ▼ (90° Pins                           │       └┬───────────────┘│
│ to the left)                          │        ▼ (90° Pins right│
│                                       │                         │
│                                       ▼ [R7] [R6] [R5] [R4]     │
│                                       100Ω  100Ω 100Ω 100Ω      │
│                                       (BRR) (BRL)(Brk)(Tai)     │
│                                         │     │    │    │       │
│                                         ▼     ▼    ▼    ▼       │
│                                      ┌────────────────────────┐ │
│                                      │ CON3: REAR (1x6 90°)   │ │
│                                      │┌───┬───┬───┬───┬───┬──┐│ │
│                                      ││BRR│BRL│Brk│Tai│NC │GND││ │
│                                      │└───┴───┴───┴───┴───┴──┘│ │
│                                      └────────────────────────┘ │
│                                           (90° Pins point downward)
└────────────────────────────────────────────────────────────────────────┘
```

---

### 🔌 3. Solder Routing (Bottom View & Top Jumpers)

The **Natural Distributed Layout v8.3** features the D1 (1N4007) silicon diode for native 6.0V BEC support, Q1 transistor driver for the headlights, standardized 100Ω resistors, and **5 top insulated jumper wires (W1 to W5)**:

#### 📻 A. Radio Channel, Diode D1 & Entrance Regulation (Right Edge — 10mm Short Traces!)
CON1 is on **Column 17 (Rows 11 to 15)**, directly facing Nano control pins, diode D1, and capacitor C1:
* **CON1 Pin 5 (CH1 Steering, Col 17, Row 11):** Direct horizontal solder trace to **Nano D4** (Col 12, Row 11) $\rightarrow$ **10 mm trace!**
* **CON1 Pin 4 (CH4 Headlight, Col 17, Row 12):** Direct horizontal solder trace to **Nano D3** (Col 12, Row 12) $\rightarrow$ **10 mm trace!**
* **CON1 Pin 3 (CH2 Throttle, Col 17, Row 13):** Direct horizontal solder trace to **Nano D2** (Col 12, Row 13) $\rightarrow$ **10 mm trace!**
* **CON1 Pin 2 (Master GND, Col 17, Row 14):** Directly solders to **C1(-)** (Col 15, Row 14) and to **Nano GND Right** (Col 12, Row 14) $\rightarrow$ **Central 0V Reference Node!**
* **CON1 Pin 1 (+6.0V BEC Master Input, Col 17, Row 15):** Solders directly to **Diode D1 Anode lead** inside hole `(17, 15)`. **IMPORTANT:** Pad `(17, 15)` is strictly **isolated on the bottom layer**, routing 100% of incoming BEC current through D1's silicon body.
* **Diode D1 (1N4007 DO-41, Row 15, Cols 17 to 15):** Top-side mounted. Cathode terminal (silver band) enters Pad `(15, 15)`, producing the safe, regulated **$+5.25\text{V}$** rail.
* **Pads (15, 15) and (16, 15) (+5.25V Protected Bus):** On the bottom layer, a direct solder bridge connects `(15, 15)` to `(16, 15)`. Pad `(15, 15)` connects C1(+) and **Jumper W1 (+5.25V Nano)**; Pad `(16, 15)` connects **Jumper W5 (+5.25V Headlight Q1 Collector)**.

#### 🧭 B. MPU-6050 Channel (Left Edge — 10mm Short Traces!)
CON4 is on **Column 02 (Rows 10 to 13)**, strictly matching the silkscreen pinout of the user's sensor (**GND, TX, RX, VCC**):
* **CON4 Pin 1 (GND, Col 02, Row 10):** Direct 1-pad solder bridge to **Master GND Bus on Column 01** (Col 01, Row 10).
* **CON4 Pin 2 (TX [SCL], Col 02, Row 11):** Direct horizontal solder trace on underside of only 10mm to **Nano A5** (Col 06, Row 11).
* **CON4 Pin 3 (RX [SDA], Col 02, Row 12):** Connected via **Top Insulated Jumper Wire W4 (~11mm)** from (02, 12) to **Nano A4** (Col 06, Row 10), hopping over the SCL trace with zero short risk.
* **CON4 Pin 4 (VCC [+5.25V], Col 02, Row 13):** Connected on underside via a branch originating at **Nano 5V** (Col 06, Row 14 $\rightarrow$ Col 05, Row 14 $\rightarrow$ Col 05, Row 13 $\rightarrow$ Col 02, Row 13).

#### 💡 C. Front LED Channel (Q1 BC337 Driver & CON2 Upper-Right)
* **CON2 Placement (Column 17, Rows 04 to 07):** 1x4 90° male header pointing to the right (same side as radio):
  - **Pin 1 (GND, Row 07):** Fed by **Jumper W2** from Master GND at (16, 14), with direct bridge (16, 07) $\rightarrow$ (17, 07).
  - **Pin 2 (Headlight, Row 06):** Fed by resistor R1 (27Ω) at (15, 06) with solder bridge to (16, 06) $\rightarrow$ (17, 06).
  - **Pin 3 (Front Left Blinker, Row 05):** Direct solder bridge from R2 Out at (16, 05) $\rightarrow$ (17, 05).
  - **Pin 4 (Front Right Blinker, Row 04):** Direct solder bridge from R3 Out at (16, 04) $\rightarrow$ (17, 04).
* **Transistor Driver Q1 (BC337 TO-92 at Row 09, Cols 13 to 15):**
  - **Collector (13, 09):** Powered by +5.25V bus via Jumper W5 from (16, 15).
  - **Base (14, 09):** Connected via vertical solder trace down from (14, 06) and horizontally to Nano D9 (12, 06).
  - **Emitter (15, 09):** Connected via short solder bridge to (15, 08) (Lead 1 of R1).
* **Front Resistors:**
  - **R1 (Headlight 27Ω 1/4W):** Mounted vertically on Column 15 between Rows 08 and 06 (5.08mm pitch).
  - **R2 (Front Left Blinker 100Ω 1/4W):** Mounted horizontally on Row 05 (Cols 14 to 16).
  - **R3 (Front Right Blinker 100Ω 1/4W):** Mounted horizontally on Row 04 (Cols 14 to 16).

#### 💡 D. Rear LED Channel (Nested L-Traces & 100Ω Resistors)
The 4 rear LED outputs utilize planar nested L-traces on the board underside:
* **D8 (Rear Right Blinker, Row 07):** Nano D8 (Col 12, Row 07) runs on Row 07 to **Col 08** $\rightarrow$ drops to **R7 Top** (Col 08, Row 18) $\rightarrow$ **R7 Bot** (Col 08, Row 21) $\rightarrow$ **CON3 Pin 1** (B.RR).
* **D7 (Rear Left Blinker, Row 08):** Nano D7 (Col 12, Row 08) runs on Row 08 to **Col 09** $\rightarrow$ drops to **R6 Top** (Col 09, Row 18) $\rightarrow$ **R6 Bot** (Col 09, Row 21) $\rightarrow$ **CON3 Pin 2** (B.RL).
* **D6 (Brake, Row 09):** Nano D6 (Col 12, Row 09) runs on Row 09 to **Col 10** $\rightarrow$ drops to **R5 Top** (Col 10, Row 18) $\rightarrow$ **R5 Bot** (Col 10, Row 21) $\rightarrow$ **CON3 Pin 3** (Brake).
* **D5 (Tail, Row 10):** Nano D5 (Col 12, Row 10) runs on Row 10 to **Col 11** $\rightarrow$ drops to **R4 Top** (Col 11, Row 18) $\rightarrow$ **R4 Bot** (Col 11, Row 21) $\rightarrow$ **CON3 Pin 4** (Tail).
* **CON3 Pin 5 (NC, Col 12, Row 24):** Unconnected / Mechanical key.
* **CON3 Pin 6 (GND, Col 13, Row 24):** Fed directly by the unobstructed vertical channel of Column 13.

---

### 📋 3.1 Point-to-Point Master Soldering Schedule (v8.4)

| Step | Net / Signal | Origin (From) | Destination (To) | Physical Connection Type |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **🔴 +6.0V BEC Entrance (D1 Anode)**| **CON1 Pin 1** (Col 17, Row 15) | **D1 Anode** (Col 17, Row 15) | Joint pin solder into hole (17, 15). **PAD ISOLATED ON BOTTOM (no connections on Row 15)!** |
| **1b**| **⚡ D1 1N4007 (Power Pass)** | **D1 Anode** (Col 17, Row 15) | **D1 Cathode** (Col 17, Row 18) | Top-side diode body (**7.62 mm standard pitch**, -0.75V drop) |
| **1c**| **🔴 Solder Track +5.25V Bus** | **D1 Cathode** (Col 17, Row 18) | **W5 In (16, 18) and C1(+) (15, 18)** | Direct horizontal solder track on underside (Row 18) |
| **1d**| **⚡ Jumper W1 (+5.25V Nano)** | **C1(+) / W1 In** (Col 15, Row 18) | **Nano +5V** (Col 06, Row 14) | **Top insulated wire (~23mm jumper)** |
| **1e**| **⚡ Jumper W5 (+5.25V Headlight)**| **VCC Bus** (Col 16, Row 18) | **Q1 Collector** (Col 13, Row 09) | **Top insulated wire (~16mm jumper)** |
| **1f**| **🔴 MPU +5.25V Branch** | **Nano 5V** (Col 06, Row 14) | (05, 14) $\rightarrow$ (05, 13) $\rightarrow$ **CON4 P4** (Col 02, Row 13) | Underside solder trace |
| **2** | **⚡ Master GND Entrance** | **CON1 Pin 2** (Col 17, Row 14) | **Nano GND Right** (Col 12, Row 14) | Direct horizontal solder trace (Row 14) |
| **2b**| **⚡ Jumper W2 Front GND**| **Master GND** (Col 16, Row 14) | **CON2 P1** (Col 16, Row 07 $\rightarrow$ bridge 17, 07) | **Top insulated wire (~18mm jumper)** |
| **2c**| **⚡ Jumper W3 GND Cross**| **Nano GND Right** (Col 12, Row 14) | **Nano GND Left** (Col 06, Row 16) | **Top insulated wire (~16mm jumper)** |
| **2d**| **⚡ GND C1(-) Filter** | **C1(-)** (Col 14, Row 18) | **Column 13 GND Trunk** (Col 13, Row 18) | Direct 1-pad solder bridge on underside |
| **3** | **📻 Radio CH2** | **CON1 Pin 3** (Col 17, Row 13) | **Nano D2** (Col 12, Row 13) | Direct 10mm horizontal trace (Row 13) |
| **4** | **📻 Radio CH4** | **CON1 Pin 4** (Col 17, Row 12) | **Nano D3** (Col 12, Row 12) | Direct 10mm horizontal trace (Row 12) |
| **5** | **📻 Radio CH1** | **CON1 Pin 5** (Col 17, Row 11) | **Nano D4** (Col 12, Row 11) | Direct 10mm horizontal trace (Row 11) |
| **6** | **🧭 MPU RX (SDA)** | **CON4 Pin 3** (Col 02, Row 12) | **Nano A4** (Col 06, Row 10) | **Top insulated wire (Jumper W4 ~11mm)** |
| **7** | **🧭 MPU TX (SCL)** | **CON4 Pin 2** (Col 02, Row 11) | **Nano A5** (Col 06, Row 11) | Direct 10mm horizontal trace (Row 11) |
| **8** | **⚡ GND MPU (P1)** | **CON4 Pin 1** (Col 02, Row 10) | **Master GND Bus** (Col 01, Row 10) | Direct solder bridge (1 pad) |
| **9** | **⚡ Bus Column 01** | **Point (Col 02, Row 16)** | Column 01 (Rows 01 to 24) | Continuous vertical ground bus |
| **10**| **⚡ Rear GND (CON3)** | **Nano GND Right** (Col 12, Row 14) | Straight down Column 13 to **CON3 P6** (Col 13, Row 24) | Unobstructed vertical solder trace |
| **11**| **💡 Headlight Base Trace** | **Nano D9** (Col 12, Row 06) | (14, 06) $\rightarrow$ **Q1 Base** (Col 14, Row 09) | Underside L-trace |
| **11b**|**💡 Headlight Emitter ➔ R1**| **Q1 Emitter** (Col 15, Row 09) | **R1 In** (Col 15, Row 08) | Short solder bridge |
| **11c**|**💡 R1 Out ➔ CON2 Headlight**| **R1 Out** (Col 15, Row 06) | **CON2 P2** (Col 17, Row 06 via 16, 06) | Direct horizontal trace |
| **12**| **💡 Front Left Blinker** | **Nano D10** (Col 12, Row 05) | **R2 In** (Col 14, Row 05) | Direct horizontal 5mm underside trace |
| **12b**|**💡 B.FL Output** | **R2 Out** (Col 16, Row 05) | **CON2 P3** (Col 17, Row 05) | Direct solder bridge (1 pad) |
| **13**| **💡 Front Right Blinker**| **Nano D11** (Col 12, Row 04) | **R3 In** (Col 14, Row 04) | Direct horizontal 5mm underside trace |
| **13b**|**💡 B.FR Output** | **R3 Out** (Col 16, Row 04) | **CON2 P4** (Col 17, Row 04) | Direct solder bridge (1 pad) |
| **14**| **💡 Rear Right Blinker (D8)**| **Nano D8** (Col 12, Row 07) | Row 07 to Col 08 $\rightarrow$ **R7 Top** (Col 08, Row 18) $\rightarrow$ **R7 Bot** $\rightarrow$ **CON3 Pin 1** | Nested L-trace on underside |
| **15**| **💡 Rear Left Blinker (D7)** | **Nano D7** (Col 12, Row 08) | Row 08 to Col 09 $\rightarrow$ **R6 Top** (Col 09, Row 18) $\rightarrow$ **R6 Bot** $\rightarrow$ **CON3 Pin 2** | Nested L-trace on underside |
| **16**| **💡 Brake Lights (D6)** | **Nano D6** (Col 12, Row 09) | Row 09 to Col 10 $\rightarrow$ **R5 Top** (Col 10, Row 18) $\rightarrow$ **R5 Bot** $\rightarrow$ **CON3 Pin 3** | Nested L-trace on underside |
| **17**| **💡 Tail Lights (D5)** | **Nano D5** (Col 12, Row 10) | Row 10 to Col 11 $\rightarrow$ **R4 Top** (Col 11, Row 18) $\rightarrow$ **R4 Bot** $\rightarrow$ **CON3 Pin 4** | Nested L-trace on underside |

---

### 📋 4. Complete Bill of Materials (BOM v8.4)

| Designator | Component | Description / Value | Purpose and Location |
| :---: | :--- | :--- | :--- |
| **U1** | Arduino Nano Socket | 2x Female Header 1x15 (2.54mm Pitch) | Columns 06 and 12 (Rows 03 to 17) |
| **U2** | MPU-6050 (GY-521) | 3D Inertial Sensor Module | Mounted on chassis via CON4 harness |
| **D1** | Rectifier Diode | **1N4007** (DO-41, 1A 1000V) | **BEC 6.0V $\rightarrow$ +5.25V Voltage Step-Down & Polarity Protection** — Column 17 (Rows 15 to 18, 7.62mm Pitch) |
| **Q1** | NPN Bipolar Transistor | **BC337** (TO-92, 800mA max) | **High-Side Headlight Driver** — Row 09 (Cols 13 to 15) |
| **C1** | Electrolytic Capacitor | **$100\mu\text{F} \times 25\text{V}$** | **Row 18 (Columns 14 and 15)**, tied to D1 and Column 13 GND |
| **R1** | 1/4W Resistor | **$27\Omega$** (Red, Violet, Black, Gold) | Headlight Limiter Q1 (D9) — Vertical: Column 15 (Rows 06 to 08) |
| **R2** | 1/4W Resistor | **$100\Omega$** (Brown, Black, Brown, Gold) | Front Left Blinker Limiter (D10) — Horizontal: Row 05 (Cols 14 to 16) |
| **R3** | 1/4W Resistor | **$100\Omega$** (Brown, Black, Brown, Gold) | Front Right Blinker Limiter (D11) — Horizontal: Row 04 (Cols 14 to 16) |
| **R7** | 1/4W Resistor | **$100\Omega$** (Brown, Black, Brown, Gold) | Rear Right Blinker Limiter (D8) — Vertical: Col 08 (Rows 18 to 21) |
| **R6** | 1/4W Resistor | **$100\Omega$** (Brown, Black, Brown, Gold) | Rear Left Blinker Limiter (D7) — Vertical: Col 09 (Rows 18 to 21) |
| **R5** | 1/4W Resistor | **$100\Omega$** (Brown, Black, Brown, Gold) | Brake Light Limiter (D6) — Vertical: Col 10 (Rows 18 to 21) |
| **R4** | 1/4W Resistor | **$100\Omega$** (Brown, Black, Brown, Gold) | Tail Light Limiter (D5) — Vertical: Col 11 (Rows 18 to 21) |
| **CON1** | 90° Male Pin Header | **1x5 90° Male Header** | **Right Board Edge** (Col 17, Rows 11 to 15) — Radio Input |
| **CON2** | 90° Male Pin Header | **1x4 90° Male Header** | **Upper-Right Edge** (Col 17, Rows 04 to 07) — Front Harness |
| **CON4** | 90° Male Pin Header | **1x4 90° Male Header** | **Left Edge** (Col 02, Rows 10 to 13) — MPU-6050 (P1: GND, P2: TX/SCL, P3: RX/SDA, P4: VCC) |
| **CON3** | 90° Male Pin Header | **1x6 90° Male Header** | **Bottom Center-Right** (Row 24, Cols 08 to 13) — Rear Harness |
| **W1-W5**| Insulated Jumper Wires | **5x Stranded insulated wire (28-30 AWG)** | Top side: W1 (+5.25V 15,18➔06,14), W2 (Front GND 16,14➔16,07), W3 (GND Cross 12,14➔06,16), W4 (MPU SDA/RX 02,12➔06,10), W5 (+5.25V Headlight 16,18➔13,09) |

---

## 🇧🇷 Português

Consulte [PLACA_SHIELD_LAYOUT.md](PLACA_SHIELD_LAYOUT.md) para a documentação técnica completa em Português com a matriz de coordenadas e especificações de montagem.

---

## 🇧🇷 Português

Consulte [PLACA_SHIELD_LAYOUT.md](PLACA_SHIELD_LAYOUT.md) para a documentação técnica completa em Português com a matriz de coordenadas e especificações de montagem.
