# Skills, Requirements & Troubleshooting — RC Light System v2.0

[🇧🇷 **Versão em Português (HABILIDADES_REQUISITOS.md)**](HABILIDADES_REQUISITOS.md) | [🇺🇸 **English Version**](#-english)

---

## 🇺🇸 English

To successfully build, calibrate, and install this smart lighting system into your RC vehicle, you will need basic electronics tools, manual assembly skills, and materials for vibration and moisture protection.

---

### 🛠️ Required Tools & Materials

| Tool / Material | Purpose in Project | Importance |
|---|---|:---:|
| **Soldering Iron (30W to 60W)** | Create durable electrical joints on the shield board and wiring harnesses. | **Essential** |
| **Solder Wire (with flux core)**| Solder wires, resistors, and MODU pin header strips. | **Essential** |
| **Heat-Shrink Tubing (1.5mm to 5mm)**| Insulate splices, ground return junctions, and exposed LED leads. | **Essential** |
| **Wire Cutters & Strippers** | Cut and strip flexible silicone wires. | **Essential** |
| **Needle-Nose Pliers or Crimper**| Crimp female MODU terminals onto body harness wires. | **Essential** |
| **Digital Multimeter** | Check continuity (shorts), check voltages, and test LED polarity. | **Highly Recommended** |
| **Dielectric Silicone Grease** | Seal MODU quick-disconnect terminals against water, mud, and oxidation. | **Recommended (Off-Road)**|
| **Aluminum Foil Tape** | Secure and conceal harness wires along the underside of the Lexan body. | **Recommended** |
| **Neutral Silicone / Shoe Goo / E6000**| Secure and seal LED backs inside body light buckets. | **Recommended** |
| **Conformal Coating / Clear Polish**| Protect shield board solder traces against moisture and dirt. | **Recommended** |

---

### 🧠 Recommended Technical Skills

1. **Basic Electronics Soldering:** Solder the resistors and male pin headers onto the 5x7cm single-sided perfboard. Heat the copper pad and component leg for 2 seconds before applying solder to create shiny, vibration-proof joints.
2. **Polarity Identification:** LEDs have an **Anode** (positive, longer leg) and a **Cathode** (negative, shorter leg/flat rim). All cathodes join into the common ground return rail.
3. **Multimeter Testing:** Measure continuity between 5V and GND on the shield board before plugging into receiver CH6. If the meter beeps, locate and remove the short circuit before applying power.
4. **Resistor Tuning:** The provided resistor values ($100\Omega$ and $150\Omega$) are standard $20\text{mA}$ safety limits. Increasing resistance to $220\Omega$ or $330\Omega$ saves battery and dims high-efficiency LEDs. Never drop below $82\Omega$ for headlights and $120\Omega$ for other LEDs.

---

### 🔍 Comprehensive Troubleshooting Guide

#### ❌ LED does not turn on:
* Check LED polarity (Anode vs Cathode).
* Verify that the MODU connector is aligned with the correct pin numbering.
* Check the solder joint of the corresponding resistor on the shield board.

#### ❌ Arduino does not respond to transmitter commands:
* Verify the radio harness (CON1): **Pin 1 to GND** and **Pin 2 to +5V (VCC)** on receiver channel **CH6**.
* Check the signal pins: Steering on **CH1 (D4)**, Throttle on **CH2 (D2)**, Headlight on **CH4 (D3)**.

#### ❌ Car powers up but blinkers stay on while driving straight (trim drift):
* Turn off the car, ensure steering and throttle sticks are perfectly centered on the transmitter, and turn the car back on. The auto-centering routine recalibrates neutral in the first 2 seconds.

#### 🎯 How to recalibrate endpoints at the track without a PC:
* Turn on the transmitter, hold the steering wheel **fully turned right (or left)**, and power on the car while holding the wheel for 2 seconds. The Arduino will enter standalone calibration mode guided by the LEDs.

#### ❌ Headlights flicker or trigger randomly under hard acceleration (motor EMI noise):
* Electric motors generate voltage transients. Solder a $100\mu\text{F} \times 16\text{V}$ electrolytic capacitor directly between the 5V and GND pins on the shield board to stabilize the power rail.
