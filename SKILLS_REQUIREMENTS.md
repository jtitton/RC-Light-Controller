# Skills, Requirements & Troubleshooting — RC Light System v7.2

[🇧🇷 **Versão em Português (HABILIDADES_REQUISITOS.md)**](HABILIDADES_REQUISITOS.md) | [🇺🇸 **English Version**](#-english)

---

## 🇺🇸 English

> [!IMPORTANT]
> **Official Project Premises:** Before assembling the shield board or wire harnesses, consult the normative document [PREMISSAS_PROJETO.md](PREMISSAS_PROJETO.md). Main power (+5V and GND) originates exclusively from the radio receiver via **CON1 (CH6)**, and capacitor **C1** ($100\mu\text{F} \times 16\text{V}$) is mandatory right at the power entrance (Column 15, Rows 14 and 15).

To successfully build, calibrate, and install this smart lighting system into your RC vehicle, you will need basic electronics tools, manual assembly skills, and materials for vibration and moisture protection.

---

### 🛠️ Required Tools & Materials

| Tool / Material | Purpose in Project | Importance |
|---|---|:---:|
| **Soldering Iron (30W to 60W)** | Create durable electrical joints on the shield board and wiring harnesses. | **Essential** |
| **Solder Wire (with flux core)**| Solder wires, resistors, and 90° pin header strips. | **Essential** |
| **90° Angled Male Pin Headers (2.54mm Pitch)** | CON1 (1x5), CON2 (1x4), CON3 (1x6), and CON4 (1x4) 90° headers for parallel low-profile wiring. | **Essential** |
| **Electrolytic Capacitor ($100\mu\text{F} \times 16\text{V}$)** | Input filtering and voltage regulation (C1) at radio harness entrance (Col 04, Rows 14-15). | **Essential** |
| **Heat-Shrink Tubing (1.5mm to 5mm)**| Insulate splices, ground return junctions, and exposed LED leads. | **Essential** |
| **Wire Cutters & Strippers** | Cut and strip flexible silicone wires. | **Essential** |
| **Needle-Nose Pliers or Crimper**| Crimp female MODU terminals onto body harness wires. | **Essential** |
| **Digital Multimeter** | Check continuity (shorts), check voltages, and test LED polarity. | **Highly Recommended** |
| **Dielectric Silicone Grease** | Seal MODU quick-disconnect terminals against water, mud, and oxidation. | **Recommended (Off-Road)**|
| **Aluminum Foil Tape** | Secure and conceal harness wires along the underside of the Lexan body. | **Recommended** |
| **Neutral Silicone / Shoe Goo / E6000**| Secure and seal LED backs inside body light buckets. | **Recommended** |
| **Conformal Coating / Clear Polish**| Protect shield board and MPU-6050 solder traces against moisture and dirt. | **Recommended** |

---

### 🧠 Recommended Technical Skills

1. **Basic Electronics Soldering:** Solder the resistors, capacitor C1, and 90° male pin headers onto the 5x7cm single-sided perfboard per [PLACA_SHIELD_LAYOUT.md](PLACA_SHIELD_LAYOUT.md). Heat the copper pad and component leg for 2 seconds before applying solder to create shiny, vibration-proof joints.
2. **Polarity Identification:** LEDs have an **Anode** (positive, longer leg) and a **Cathode** (negative, shorter leg/flat rim). Electrolytic capacitor C1 has a polarity stripe indicating the negative (-) lead. All negative leads join into the unified master ground bus.
3. **Multimeter Testing:** Measure continuity between 5V and GND on the shield board before plugging into receiver CH6. If the meter beeps, locate and remove the short circuit before applying power.
4. **MPU-6050 Mounting:** Secure the sensor to the chassis using foam double-sided tape (3M VHB) to absorb high-frequency motor vibration. The 3D auto-vector alignment algorithm handles orientation automatically.

---

### 🔍 Comprehensive Troubleshooting Guide

#### ❌ LED does not turn on:
* Check LED polarity (Anode vs Cathode).
* Verify that the MODU connector is aligned with the correct pin numbering.
* Check the solder joint of the corresponding resistor on the shield board.

#### ❌ Arduino does not respond to transmitter commands:
* Verify the radio harness (CON1): **Pin 1 to VCC (+5V)** and **Pin 2 to GND** on receiver channel **CH6** (per [PREMISSAS_PROJETO.md](PREMISSAS_PROJETO.md)).
* Check the signal pins: Steering on **CH1 (D4)**, Throttle on **CH2 (D2)**, Headlight on **CH4 (D3)**.

#### ❌ MPU-6050 is not detected:
* Check I2C wiring: **SDA to A4** and **SCL to A5**. The firmware features graceful fallback and will operate via radio even without the sensor.

#### ❌ Hazard lights flash continuously on power-up:
* Ensure the car is sitting on all 4 wheels on a flat surface during the initial 2-second boot auto-centering to accurately capture the static gravity vector $\vec{g}_0$.

#### ❌ Car powers up but blinkers stay on while driving straight (trim drift):
* Turn off the car, ensure steering and throttle sticks are perfectly centered on the transmitter, and turn the car back on. The auto-centering routine recalibrates neutral in the first 2 seconds.

#### 🎯 How to recalibrate endpoints at the track without a PC (Calibration Gesture):
* Turn on the transmitter, hold the steering wheel deflected **over 50% to the right (or left)**, and power on the car while holding the wheel for **1.5 seconds**. The Arduino will flash all LEDs 3 times and enter standalone calibration mode guided by the LEDs.

#### ❌ Headlights flicker or trigger randomly under hard acceleration (motor EMI noise / voltage drops):
* Electric motors generate voltage transients. Solder a $100\mu\text{F} \times 16\text{V}$ electrolytic capacitor directly at the power entrance (Column 15, Rows 14 and 15, next to CON1 on the right edge) as per Premise #2 to stabilize the 5V rail and prevent brownouts.
