# Wiring Harness Guide — RC Light System v8.4

[🇧🇷 **Versão em Português (CHICOTE_LEDS.md)**](CHICOTE_LEDS.md) | [🇺🇸 **English Version**](#-english) | [📜 **Project Premises (PREMISSAS_PROJETO.md)**](PREMISSAS_PROJETO.md)

---

## 🇺🇸 English

This guide provides step-by-step instructions for assembling the **wiring harnesses** for the RC model using **MODU / Dupont 2.54mm pitch 90° angle connectors** with the v8.4 Distributed Architecture:

1. **Receiver & Power Cable (5 pins 90° on Right Edge - CON1)** — Powers the system through **Channel 6 (CH6)** with **6.0V BEC** (dropped on-board to +5.25V by D1 1N4007) and reads control signals (CH2 Throttle, CH4 Headlight switch, CH1 Steering).
2. **MPU-6050 Accelerometer Cable (4 pins 90° on Left Edge - CON4)** — Direct 1:1 I2C interface (**GND, TX [SCL], RX [SDA], VCC [+5.25V]**) for chassis sensor mounting.
3. **Front Body Shell Harness (4 pins 90° on Upper-Right Edge - CON2)** — **4 White Headlight LEDs in parallel** driven by on-board **Q1 (BC337)** NPN transistor with **R1 ($27\,\Omega$)** resistor (~11 to 14 mA per LED, 45 to 55 mA total), plus front amber blinkers (2 LEDs per side via **$100\,\Omega$**). Located on the **same side as the radio** (right edge, above CON1).
4. **Rear Body Shell Harness (6 pins 90° on Bottom Center-Right Edge - CON3)** — Tail lights, brake lights, and rear turn signals (2 LEDs per channel in parallel, limited by **$100\,\Omega$** on-board resistors), condenses body wires into a single 6-pin connector.

> [!IMPORTANT]
> **ZERO RESISTORS ON BODY SHELL:** All current-limiting resistors and the headlight transistor driver are mounted directly on the **Hub Shield Board**. The body shell wiring contains only the LEDs and clean wire leads, simplifying maintenance and minimizing unsprung shell weight!

---

### 🛠️ 1. Bill of Materials & Connectors

* **MODU / Dupont 2.54mm Pitch Connectors:**
  * 2x **Female MODU Housing 4-Pin (1x04)** — For Front Harness (CON2) and MPU-6050 Cable (CON4).
  * 1x **Female MODU Housing 6-Pin (1x06)** — For Receiver/Power Cable (uses 5 pins).
  * 1x **Female MODU Housing 6-Pin (1x06)** — For Rear Harness (uses 6 pins).
  * 25x **Female Crimp Terminals (1T)** — To crimp/solder onto wire tips.
  * 1x **Right-Angle Male Pin Header Strip (1x40 90°)** — To solder along board edges.
* **Perfboard:**
  * 1x **5x7 cm Single-Sided Universal Perfboard**
* **Recommended Wires:** **28 AWG or 30 AWG flexible silicone wire**.
* **Insulation:** Heat-shrink tubing (1.5mm, 2.5mm, and 5.0mm).

---

### 📐 2. Overall Wiring Architecture

```
 ┌────────────────────────────────────────────────────────┐
 │                   BODY SHELL (LEXAN)                   │
 │                                                        │
 │   [Blinker FL (2x)]🟠─┐              ┌─🟠 [Blinker FR (2x)]
 │                       │              │                 │
 │   [Headlights 4x]  ⬜─┼──────┐┌──────┼─⬜              │
 │   (2 Main + 2 Aux)    │      ││      │                 │
 │                       ▼      ▼▼      ▼                 │
 │                ┌───────────────────────┐               │
 │                │  FRONT HARNESS        │               │
 │                │  (4-Pin MODU Housing) │               │
 │                └──────────┬────────────┘               │
 │                           │                            │
 │   [Blinker RL (2x)]🟠─┐   │ (Quick-Disconnect)         │
 │                       │   │                            │
 │   [Tail Light (2x)]🔴─┼─┐ │                            │
 │                       │ │ │                            │
 │   [Brake Light(2x)]🔴─┼─┼─┤                            │
 │                       │ │ │                            │
 │                       ▼ ▼ ▼                            │
 │                ┌───────────────────────┐               │
 │                │  REAR HARNESS         │               │
 │                │  (6-Pin MODU Housing) │               │
 │                └──────────┬────────────┘               │
 │                           │ (Quick-Disconnect)         │
 └───────────────────────────┼────────────────────────────┘
                             │
 ┌───────────────────────────┼────────────────────────────┐
 │                           │  (CON2 Upper-Right Edge    │
 │                           │   90°)                     │
 │                           │          │                 │
 │ 🧭 MPU-6050 (GY-521) ┌────┴──────────▼─┐ 📡 FS-BS6     │
 │  [A4, A5, +5V, GND]  │ HUB SHIELD BOARD│  (CH6:        │
 │  [CON4 Left Edge     │   (5x7 cm) v8.4 │◄─ +6.0V/GND,  │
 │   90° Header] ──────►│[Q1 BC337 Headlt]│   CH1,2,4)    │
 │                      └────────┬────────┘  [CON1 Right] │
 │                               │ (CON3 90° on           │
 │                               ▼  Bottom Edge)          │
 │                        CHASSIS                         │
 └────────────────────────────────────────────────────────┘
```

---

### 📝 3. Step-by-Step Harness Assembly

#### 📡 Harness A: Receiver & Power Cable via CH6 (5 Pins)
This cable connects the FlySky FS-BS6 receiver to CON1 on the right edge of the Arduino Hub Shield. All power for the Arduino and all LEDs is drawn from **CH6** (supplied by the ESC's 6.0V BEC).

```
SHIELD BOARD SIDE (CON1 MODU Female)            FLYSKY FS-BS6 RECEIVER SIDE
────────────────────────────────────            ───────────────────────────
[Pin 1: +6.0V BEC] (Red Wire)   ──────────────→ CH6 (Center Pin - VCC +6.0V BEC)
[Pin 2: GND]       (Black Wire) ──────────────→ CH6 (Bottom Pin - GND)
[Pin 3: CH2]       (Yellow Wire)──────────────→ CH2 (Top Pin - Throttle Signal D2)
[Pin 4: CH4]       (Green Wire) ──────────────→ CH4 (Top Pin - Headlight Signal D3)
[Pin 5: CH1]       (White Wire) ──────────────→ CH1 (Top Pin - Steering Signal D4)
```
* **Recommended Length:** ~10 cm to 15 cm.
* **Assembly Note:** The 1=+6.0V BEC, 2=GND, 3=CH2, 4=CH4, 5=CH1 order aligns directly with the Nano right header pins (Rows 11-15), producing ultra-short 10mm traces with zero crossovers. Pin 1 feeds directly into the anode of diode D1 (1N4007) on the shield.

---

#### 🧭 Harness B: MPU-6050 Accelerometer Cable (4-Pin Female MODU)
Connects the Hub Shield (CON4 on the left edge, Rows 10 to 13) to the GY-521 sensor module on the vehicle chassis (direct 1:1 pinout with sensor silkscreen):

```
SHIELD BOARD SIDE (CON4 MODU Female)          MPU-6050 SENSOR SIDE (Module Silkscreen)
────────────────────────────────────          ────────────────────────────────────────
[Pin 1: GND]       (Black Wire)   ──────────→ GND Pin
[Pin 2: TX (SCL)]  (Yellow Wire)  ──────────→ TX Pin (I2C Clock / SCL)
[Pin 3: RX (SDA)]  (Green Wire)   ──────────→ RX Pin (I2C Data / SDA)
[Pin 4: VCC (+5V)] (Red Wire)     ──────────→ VCC Pin (+5V)
```
* **Recommended Length:** ~5 cm to 10 cm.
* **Assembly Note:** Straight 1:1 pinout! No crossed wires in the harness: female housing pin 1 connects to sensor pin 1, 2 to 2, 3 to 3, and 4 to 4.

---

#### 💡 Harness C: Front Light Harness (4-Pin Female MODU)
Connects the Hub Shield (CON2 on the upper-right edge, Column 17, Rows 04 to 07 — same side as radio) to the LEDs installed in the front of the body shell:

```
[Pin 1: Common GND] (Black Wire, Row 07)  ──→ Joined Cathodes (-) of all front LEDs (4x Headlights + 4x Blinkers)
[Pin 2: Headlights] (White Wire, Row 06)  ──→ Anodes (+) of 4x White Headlight LEDs in parallel (Powered by Q1 BC337 + R1 27Ω)
[Pin 3: Blinker FL] (Orange Wire, Row 05) ──→ Anodes (+) of 2x Front Left Amber LEDs in parallel (via R2 100Ω)
[Pin 4: Blinker FR] (Blue Wire, Row 04)   ──→ Anodes (+) of 2x Front Right Amber LEDs in parallel (via R3 100Ω)
```

---

#### 💡 Harness D: Rear Light Harness (6-Pin Female MODU)
Condenses the rear wires in the body shell into a single clean connector:

```
BODY SHELL WIRES (Rear LEDs)                   MODU 6-PIN CONNECTOR
────────────────────────────                   ────────────────────
2x Positive Wires (Blinker RR in parallel) ──→ [Pin 1: Blinker RR D8 (via R7 100Ω)]
2x Positive Wires (Blinker RL in parallel) ──→ [Pin 2: Blinker RL D7 (via R6 100Ω)]
2x Positive Wires (Brake LEDs in parallel) ──→ [Pin 3: Brake Lights D6 (via R5 100Ω)]
2x Positive Wires (Tail LEDs in parallel)  ──→ [Pin 4: Tail Lights D5 (via R4 100Ω)]
                                               [Pin 5: Reserved / Key]
All Cathodes (-) Joined (Common GND)       ──→ [Pin 6: Common GND]
```
*(Note: The rear pinout strictly mirrors the planar nested L-traces on the shield board with ZERO track crossovers and GND aligned on pin 6).*

---

### 🛡️ 4. Waterproofing, Vibration & Cable Management

1. **Connector Sealing:**
   * Pack dielectric silicone grease into the female housing cavities before mating. This excludes water, mud, and prevents contact corrosion.
2. **Shield Board & MPU-6050 Protection:**
   * Paint clear conformal coating, nail polish, or liquid electrical tape over all exposed solder traces on the bottom of the perfboard and MPU-6050 module.
3. **Body Mounting:**
   * Secure wiring runs along the roof and fenders using **aluminum tape**.
   * Protect loose wire sections between the body shell and chassis with **braided mesh sleeving**.

---

## 🇧🇷 Português

Consulte [CHICOTE_LEDS.md](CHICOTE_LEDS.md) para o guia detalhado de confecção dos chicotes em Português.
