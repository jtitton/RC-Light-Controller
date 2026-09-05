# RC Car Smart Lighting System v7.2 — User Manual

[🇧🇷 **Portuguese Version (README.md)**](README.md) | [🇺🇸 **English Version**](#-english)

---

## 🇺🇸 English

This project consists of an intelligent lighting controller for radio-controlled (RC) cars, based on the **Arduino Nano** microcontroller, **MPU-6050 (GY-521)** 3D inertial accelerometer, and powered directly through the **Channel 6 (CH6)** port of a **FlySky FS-BS6** receiver (or any standard PPM receiver).

---

### 📁 Available Firmware Versions

The project provides **two independent firmwares**, each optimized for a specific workflow:

| Firmware | Intended Purpose | Technical Highlights | Resource Footprint |
|---|---|---|:---:|
| **[LuzesArduino.ino](LuzesArduino.ino)** | **Development & Wokwi Simulation** | Active Serial communication (115200 baud), inertial telemetry (`I`), rollover crash simulation (`K`), interactive menus (`C`, `Z`, `P`, `R`), **60s automatic track demo (`T`)**, and **manual keyboard driving (`W/S/A/D/F/G/X`)**. | Flash: 23.7 kB (77%)<br>RAM: 983 B (47%) |
| **[LuzesArduino_Producao.ino](LuzesArduino_Producao/LuzesArduino_Producao.ino)** | **Production & Track Racing** | **Zero Serial** (UART fully disabled, 100% standalone), I2C Fast-Mode (400kHz), loop speed **~1–2 kHz with active MPU** (~20–30 kHz in fallback without MPU), 3D auto-vector alignment, roll-over hazard alert, and visual LED feedback. | **Flash: 11.5 kB (37%)**<br>**RAM: 363 B (17%)** |

> [!TIP]
> * For bench testing, USB debugging, or Wokwi online simulation: use **[LuzesArduino.ino](LuzesArduino.ino)**.
> * For flashing the Arduino Nano inside your RC chassis and racing at the track: use **[LuzesArduino_Producao.ino](LuzesArduino_Producao/LuzesArduino_Producao.ino)**.

---

### 📋 Documentation Index

| English Document | Portuguese Document (Versão em Português) | Content Summary |
|---|---|---|
| **[README_EN.md](README_EN.md)** | **[README.md](README.md)** | Project overview, firmware comparisons, inertial integration, and operation guide. |
| **[SHIELD_BOARD_LAYOUT.md](SHIELD_BOARD_LAYOUT.md)** | **[PLACA_SHIELD_LAYOUT.md](PLACA_SHIELD_LAYOUT.md)** | **Perfboard Engineering Design (5x7cm)**: 18x24 grid coordinate matrix, solder traces, common GND rail, and component placement. |
| 🌐 **[Interactive Board Visualizer](placa_shield_visualizador.html)** | 🌐 **[Visualizador Interativo da Placa](placa_shield_visualizador.html)** | **Interactive Graphical Board Model** (HTML/SVG): component top view, mirrored solder bottom view, x-ray, and dynamic net highlighting. |
| **[WIRING_SCHEMATIC.md](WIRING_SCHEMATIC.md)** | **[ESQUEMA_LIGACAO.md](ESQUEMA_LIGACAO.md)** | Full circuit diagram, MPU-6050 I2C bus (A4/A5), common ground rail, resistor calculations, and CH6 receiver power supply. |
| **[LED_HARNESS.md](LED_HARNESS.md)** | **[CHICOTE_LEDS.md](CHICOTE_LEDS.md)** | Build guide for MODU quick-disconnect harnesses (Front 4P, Rear 6P, Radio/CH6 5P, MPU-6050 4P), connector part numbers, and waterproofing. |
| **[PREMISSAS_PROJETO.md](PREMISSAS_PROJETO.md)** | **[PREMISSAS_PROJETO.md](PREMISSAS_PROJETO.md)** | **Normative Engineering Premises**: dedicated radio power (CH6), C1 entrance regulation, and unified master GND bus. |
| **[SKILLS_REQUIREMENTS.md](SKILLS_REQUIREMENTS.md)** | **[HABILIDADES_REQUISITOS.md](HABILIDADES_REQUISITOS.md)** | Required tools, soldering best practices, waterproofing techniques, and comprehensive troubleshooting. |
| **[wokwi_diagram.json](wokwi_diagram.json)** / **[diagram.json](diagram.json)** | **[wokwi_diagram.json](wokwi_diagram.json)** / **[diagram.json](diagram.json)** | Complete wiring and visual component schematic for Wokwi online simulation (including radio power, master GND bus, and MPU-6050). |

---

### ⚙️ Main System Features (v7.2)

- **I2C Inertial Accelerometer (MPU-6050) with Fast-Mode (400kHz):** Measures true physical vehicle acceleration and deceleration regardless of mounting orientation.
- **3D Auto-Vector Alignment Algorithm:** Automatically establishes static gravity $\vec{g}_0$ at boot and computes longitudinal dynamic force $A_{\text{long}} = (\vec{a} - \vec{g}_0) \cdot \vec{u}_{\text{long}}$ through vector projection, allowing the sensor to be mounted at any angle or position.
- **Braking Sensor Fusion:** Brake lights illuminate on transmitter reverse command (PPM $< -5\%$) **OR** true physical deceleration ($A_{\text{long}} \le -0.20G$), accurately simulating engine braking and track friction.
- **Roll-Over Safety Alert:** If the vehicle flips or rolls over on its side ($\theta > 81^\circ$), all 4 turn signals automatically enter high-speed hazard flash mode (120ms).
- **Graceful Fallback:** If the MPU-6050 sensor is not connected on A4/A5, the system automatically falls back to 100% PPM radio operation without crashing or lagging.
- **100% Interrupt-Driven (Non-blocking):** All 3 radio channels are read asynchronously via hardware interrupts (`INT0`, `INT1`, and `PCINT20`).
- **CH6 Integrated Power Supply:** Powered directly through receiver channel CH6 via the ESC's Battery Elimination Circuit (nominal 5.0V BEC).
- **Smooth Fade Transitions:** Tail lights feature smooth ~300ms fade transitions.
- **Standalone Field Gesture Calibration:** Recalibrate all stick and headlight endpoints directly at the track by holding steering wheel deflected ($\ge 50\%$) for 1.5 seconds during power-up.

---

### ⚙️ Software Parameters and Configuration

In the main sketch, you can customize control thresholds:

```cpp
// --- MPU-6050 Accelerometer (I2C) ---
#define ACCEL_BRAKE_THRESH_G     0.20f   // Physical deceleration >= 0.20G triggers brake light
#define ACCEL_ROLLOVER_COS       0.15f   // Angle > 81° with vertical triggers 4x hazard alert

// --- Radio Control Thresholds (%) ---
#define STEERING_BLINK_PERCENT   70      // Steering deflection threshold for blinkers (70%)
#define THROTTLE_BRAKE_PERCENT   5       // Throttle threshold for brake lights (5%)
#define HEADLIGHT_THRESH_LOW     33      // Below this: Headlight Off
#define HEADLIGHT_THRESH_HIGH    66      // Above this: 100% Brightness

// --- Blinker Timing ---
#define BLINK_INTERVAL_MS        250     // 120 bpm (standard turn signal)
#define BLINK_HAZARD_MS          120     // 250 bpm (rollover safety alert)
```

---

### ⏱ Standalone Operation & Calibration

#### 🚦 Normal Boot Procedure (Everyday Racing)
1. Turn on the transmitter with sticks centered.
2. Power on the RC car.
3. All 4 blinkers turn on steady for **2 seconds** (measuring neutral trim and calibrating static gravity $\vec{g}_0$).
4. LEDs flash **2 quick confirmation blinks**.
5. Ready to race!

#### 🎯 Field Gesture Calibration (Without a Computer)
To recalibrate endpoints on the track:
1. Turn on the transmitter and hold the steering wheel deflected **over 50% to the right (or left)**.
2. Power on the car while holding the wheel for **1.5 seconds**.
3. LEDs flash **3 times** to confirm calibration mode.
4. **Auto-Center (2s):** Release sticks to neutral (blinkers stay solid).
5. **Step 1 (Endpoints - 5s):** Blinkers alternate left/right. Move steering and throttle to full extremes.
6. **Step 2 (Headlight - 5s):** Headlight pulses smoothly. Toggle the 3-position switch through all 3 stages.
7. **Done:** LEDs flash **5 times together**, save parameters to EEPROM, and return to normal driving mode.

---

### 🎮 Serial Terminal & Keyboard Controls (Wokwi & Bench Testing)

In the development sketch ([LuzesArduino.ino](LuzesArduino.ino)), you can interactively drive the car using your keyboard in the Serial Monitor (**115200 baud**).

Each keypress on movement controls adds **+500 ms cumulative duration** to the action:

| Key / Command | Simulated Action | Behavior / Timing |
| :---: | :--- | :--- |
| **`W`** ou **`w`** | **Forward Throttle** (+100%) | Brake OFF, $+0.40G$ longitudinal force. **+500 ms** per keypress. |
| **`S`** ou **`s`** | **Brake / Reverse** (-100%) | Brake Lights and Tail Lights ON, $-0.60G$ deceleration force. **+500 ms** per keypress. |
| **`A`** ou **`a`** | **Turn Left** (-100%) | Left Blinkers flash (120 bpm). **+500 ms** per keypress. |
| **`D`** ou **`d`** | **Turn Right** (+100%) | Right Blinkers flash (120 bpm). **+500 ms** per keypress. |
| **`F`** ou **`f`** | **Increase Headlight Brightness** | Increases step: **OFF $\rightarrow$ 40% PWM $\rightarrow$ 100% PWM**. |
| **`G`** ou **`g`** | **Decrease Headlight Brightness** | Decreases step: **100% PWM $\rightarrow$ 40% PWM $\rightarrow$ OFF**. |
| **`K`** ou **`k`** | **Simulate Rollover Crash** | Toggles rollover hazard state (4-way flashers at 120ms). |
| **`I`** ou **`i`** | **MPU-6050 Inertial Telemetry** | Displays $\vec{g}_0$, $\vec{u}_{\text{long}}$, and live longitudinal G-force. |
| **`X`** ou **`x`** | **Immediate Neutral / Center** | Resets timers, clears blinkers and turns off brake lights immediately. |
| **`T`** ou **`t`** | **Automated 60s Race Simulation** | Runs the 60-second virtual test track with turns, brakes, and headlights. |
| **`N`** ou **`n`** | **Normal Receiver Mode** | Exits manual simulation and resumes reading physical receiver PPM signals. |
| **`C`** ou **`c`** | **Full Calibration** | Runs the interactive terminal calibration wizard. |
| **`Z`** ou **`z`** | **Re-center Sticks (Trim)** | Measures stick neutral center positions and static gravity $\vec{g}_0$. |
| **`P`** ou **`p`** | **Print Calibration** | Prints stored EEPROM parameters to terminal. |
| **`?`** | **Help Menu** | Displays the full list of keyboard commands. |
