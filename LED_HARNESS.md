# Wiring Harness Guide — RC Light System v8.0

[🇧🇷 **Versão em Português (CHICOTE_LEDS.md)**](CHICOTE_LEDS.md) | [🇺🇸 **English Version**](#-english)

---

## 🇺🇸 English

This guide provides step-by-step instructions for assembling the **wiring harnesses** for the RC model using **MODU / Dupont 2.54mm pitch 90° angle connectors** with the v8.0 Distributed Architecture:

1. **Receiver & Power Cable (5 pins 90° on Left Edge)** — Powers the Arduino (5V and GND) through **Channel 6 (CH6)** and reads control signals (CH2 Throttle, CH4 Headlight switch, CH1 Steering).
2. **MPU-6050 Accelerometer Cable (4 pins 90° on Right Edge)** — I2C bus interface (GND, +5V, SDA A4, SCL A5) for chassis sensor mounting.
3. **Front Body Shell Harness (4 pins 90° on Bottom-Left Edge)** — Powers dual headlights and front turn signals.
4. **Rear Body Shell Harness (6 pins 90° on Bottom Center-Right Edge)** — Powers tail lights, brake lights, and rear turn signals (condenses 12 body wires into a single 6-pin housing).

---

### 🛠️ 1. Bill of Materials & Connectors

* **MODU / Dupont 2.54mm Pitch Connectors:**
  * 2x **Female MODU Housing 4-Pin (1x04)** — For Front Harness and MPU-6050 Cable.
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
 │   [Blinker FL]🟠──┐                  ┌──🟠 [Blinker FR]│
 │                   │                  │                 │
 │   [Headlight L]⬜─┼──────┐    ┌──────┼──⬜ [Headlight R]
 │                   │      │    │      │                 │
 │                   ▼      ▼    ▼      ▼                 │
 │                ┌───────────────────────┐               │
 │                │  FRONT HARNESS        │               │
 │                │  (4-Pin MODU Housing) │               │
 │                └──────────┬────────────┘               │
 │                           │                            │
 │   [Blinker RL]🟠──┐       │ (Quick-Disconnect)         │
 │                   │       │                            │
 │   [Tail Light]🔴──┼──┐    │                            │
 │                   │  │    │                            │
 │   [Brake Light]🔴─┼──┼─┐  │                            │
 │                   │  │ │  │                            │
 │                   ▼  ▼ ▼  ▼                            │
 │                ┌───────────────────────┐               │
 │                │  REAR HARNESS         │               │
 │                │  (6-Pin MODU Housing) │               │
 │                └──────────┬────────────┘               │
 │                           │ (Quick-Disconnect)         │
 └───────────────────────────┼────────────────────────────┘
                             ▼
 ┌────────────────────────────────────────────────────────┐
 │                           ▼                            │
 │ 📡 FS-BS6 Receiver  ┌──────────────────┐  🧭 MPU-6050  │
 │  (CH6: +5V/GND      │ HUB SHIELD BOARD │   (GY-521)    │
 │   CH1, CH2, CH4) ──►│   (5x7 cm)       │◄── [A4, A5,   │
 │   [CON1 Left Edge   │                  │     +5V, GND] │
 │    90° Header]      │                  │    [CON4 Right│
 │                     └────────┬─────────┘     Edge 90°] │
 │                              │ (CON2 & CON3 90°        │
 │                              ▼  on Bottom Edge)        │
 │                        CHASSIS                         │
 └────────────────────────────────────────────────────────┘
```

---

### 📝 3. Step-by-Step Harness Assembly

#### 📡 Harness A: Receiver & Power Cable via CH6 (5 Pins)
This cable connects the FlySky FS-BS6 receiver to CON1 on the left edge of the Arduino Hub Shield. All power for the Arduino and all 7 LEDs is drawn from **CH6** (supplied by the ESC's BEC).

```
SHIELD BOARD SIDE (CON1 MODU Female)            FLYSKY FS-BS6 RECEIVER SIDE
────────────────────────────────────            ───────────────────────────
[Pin 1: +5V]    (Red Wire)     ──────────────→ CH6 (Center Pin - VCC +5V)
[Pin 2: GND]    (Black Wire)   ──────────────→ CH6 (Bottom Pin - GND)
[Pin 3: CH2]    (Yellow Wire)  ──────────────→ CH2 (Top Pin - Throttle Signal D2)
[Pin 4: CH4]    (Green Wire)   ──────────────→ CH4 (Top Pin - Headlight Signal D3)
[Pin 5: CH1]    (White Wire)   ──────────────→ CH1 (Top Pin - Steering Signal D4)
```
* **Recommended Length:** ~10 cm to 15 cm.
* **Assembly Note:** The 1=5V, 2=GND, 3=CH2, 4=CH4, 5=CH1 order aligns directly with Nano power and D2, D3, D4 pins, producing ultra-short 10mm traces with zero crossovers.

---

#### 🧭 Harness B: MPU-6050 Accelerometer Cable (4-Pin Female MODU)

```
SHIELD BOARD SIDE (MODU Female)                 MPU-6050 SENSOR SIDE
──────────────────────────────                 ────────────────────
[Pin 1: GND]    (Black Wire)   ──────────────→ GND Pin
[Pin 2: +5V]    (Red Wire)     ──────────────→ VCC Pin
[Pin 3: SCL]    (Yellow Wire)  ──────────────→ SCL Pin
[Pin 4: SDA]    (Green Wire)   ──────────────→ SDA Pin
```
* **Recommended Length:** ~5 cm to 10 cm.

---

#### 💡 Harness C: Front Light Harness (4-Pin Female MODU)

```
[Pin 1: Common GND] ──────→ Joined Cathodes (-) of all front LEDs
[Pin 2: Headlights] ──────→ Anodes (+) of Left and Right Headlight LEDs
[Pin 3: Blinker FL] ──────→ Anode (+) of Front Left Blinker LED
[Pin 4: Blinker FR] ──────→ Anode (+) of Front Right Blinker LED
```

---

#### 💡 Harness D: Rear Light Harness (6-Pin Female MODU — 12-to-6 Wire Condensation)
Condenses the 12 existing rear wires in the body shell into a single clean connector:

```
EXISTING BODY WIRES (12 Wires)                 MODU 6-PIN CONNECTOR
──────────────────────────────                 ────────────────────
1x Positive Wire (Blinker RR)  ─────────────────────→ [Pin 1: Blinker RR (D8)]
1x Positive Wire (Blinker RL)  ─────────────────────→ [Pin 2: Blinker RL (D7)]
2x Positive Wires (Brake LEDs) ──[Solder Together]──→ [Pin 3: Brake Lights (D6)]
2x Positive Wires (Tail LEDs)  ──[Solder Together]──→ [Pin 4: Tail Lights (D5)]
                                                      [Pin 5: Reserved / Key]
6x Ground Wires (LED Cathodes) ──[Solder Together]──→ [Pin 6: Common GND]
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
