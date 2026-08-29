# Wiring Harness Guide — RC Light System v2.0

[🇧🇷 **Versão em Português (CHICOTE_LEDS.md)**](CHICOTE_LEDS.md) | [🇺🇸 **English Version**](#-english)

---

## 🇺🇸 English

This guide provides step-by-step instructions for assembling the **3 wiring harnesses** for the RC model using **MODU / Dupont 2.54mm pitch connectors**:

1. **Receiver & Power Cable (5 pins)** — Powers the Arduino (5V and GND) through **Channel 6 (CH6)** and reads control signals (CH1 Steering, CH2 Throttle, CH4 Headlight switch).
2. **Front Body Shell Harness (4 pins)** — Powers the dual headlights and front turn signals.
3. **Rear Body Shell Harness (6 pins)** — Powers the tail lights, brake lights, and rear turn signals (condenses 12 body wires into a single 6-pin housing).

---

### 🛠️ 1. Bill of Materials & Connectors

* **MODU / Dupont 2.54mm Pitch Connectors:**
  * 1x **Female MODU Housing 4-Pin (1x04)** — For Front Harness.
  * 1x **Female MODU Housing 6-Pin (1x06)** — For Receiver/Power Cable (uses 5 pins).
  * 1x **Female MODU Housing 6-Pin (1x06)** — For Rear Harness (uses 5 pins).
  * 20x **Female Crimp Terminals (1T)** — To crimp/solder onto wire tips.
  * 1x **Straight Male Pin Header Strip (1x40 180°)** — To solder onto the chassis shield perfboard.
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
 │                 ┌──────────────────┐                   │
 │                 │ HUB SHIELD BOARD │◄── Radio Cable ├── 📡 FS-BS6 Receiver
 │                 │   (5x7 cm)       │   [VCC/GND @CH6]  │    (Chassis)
 │                 └──────────────────┘   [CH1, CH2, CH4] │
 │                        CHASSIS                         │
 └────────────────────────────────────────────────────────┘
```

---

### 📝 3. Step-by-Step Harness Assembly

#### 📡 Harness A: Receiver & Power Cable via CH6 (5 Pins)
This cable connects the FlySky FS-BS6 receiver to the Arduino Hub Shield. All power for the Arduino and all 7 LEDs is drawn from **CH6** (supplied by the ESC's BEC).

```
SHIELD BOARD SIDE (MODU Female)                 FLYSKY FS-BS6 RECEIVER SIDE
──────────────────────────────                 ───────────────────────────
[Pin 1: GND]    (Black Wire)   ──────────────→ CH6 (Bottom Pin - GND)
[Pin 2: +5V]    (Red Wire)     ──────────────→ CH6 (Center Pin - VCC +5V)
[Pin 3: CH1]    (White Wire)   ──────────────→ CH1 (Top Pin - Steering Signal)
[Pin 4: CH2]    (Yellow Wire)  ──────────────→ CH2 (Top Pin - Throttle Signal)
[Pin 5: CH4]    (Green Wire)   ──────────────→ CH4 (Top Pin - Headlight Signal)
```
* **Recommended Length:** ~10 cm to 15 cm.
* **Assembly Tips:**
  * Use a standard 3-pin servo plug housing for the Black/Red wires to plug directly into receiver **CH6**.
  * Use individual 1-pin housings for the signal wires to plug into **CH1**, **CH2**, and **CH4**.

---

#### 💡 Harness B: Front Light Harness (4-Pin Female MODU)

```
[Pin 1: Common GND] ──────→ Joined Cathodes (-) of all front LEDs
[Pin 2: Headlights] ──────→ Anodes (+) of Left and Right Headlight LEDs
[Pin 3: Blinker FL] ──────→ Anode (+) of Front Left Blinker LED
[Pin 4: Blinker FR] ──────→ Anode (+) of Front Right Blinker LED
```

---

#### 💡 Harness C: Rear Light Harness (6-Pin Female MODU — 12-to-6 Wire Condensation)
Condenses the 12 existing rear wires in the body shell into a single clean connector:

```
EXISTING BODY WIRES (12 Wires)                 MODU 6-PIN CONNECTOR
──────────────────────────────                 ────────────────────
6x Ground Wires (LED Cathodes) ──[Solder Together]──→ [Pin 1: Common GND]
2x Positive Wires (Tail LEDs)  ──[Solder Together]──→ [Pin 2: Tail Lights (D5)]
2x Positive Wires (Brake LEDs) ──[Solder Together]──→ [Pin 3: Brake Lights (D6)]
1x Positive Wire (Blinker RL)  ─────────────────────→ [Pin 4: Blinker RL (D7)]
1x Positive Wire (Blinker RR)  ─────────────────────→ [Pin 5: Blinker RR (D8)]
                                                      [Pin 6: Reserved / Key]
```

---

### 🛡️ 4. Waterproofing, Vibration & Cable Management

1. **Connector Sealing:**
   * Pack dielectric silicone grease (or solid petroleum jelly) into the female housing cavities before mating. This excludes water, mud, and prevents contact corrosion.
2. **Shield Board Protection:**
   * Paint clear conformal coating, nail polish, or liquid electrical tape over all exposed solder traces on the bottom of the perfboard.
3. **Body Mounting:**
   * Secure wiring runs along the roof and fenders using **aluminum tape**.
   * Protect loose wire sections between the body shell and chassis with **braided mesh sleeving**.
