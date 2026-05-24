# Guia de Confecção do Chicote de LEDs / Wiring Harness Guide

[**Português**](#português) | [**English**](#english)

---

## Português

A fiação em um carro RC precisa ser robusta, flexível e organizada para suportar vibrações, solavancos e permitir a fácil manutenção do carro (como a remoção da bolha/carroceria).

### 🛠️ Especificação de Cabos e Conectores

- **Cabos Recomendados:** Fios de **26 AWG** ou **28 AWG** com isolamento de **silicone ultra-flexível** são os mais indicados, pois não quebram com a vibração constante do chassi.
- **Conectores Indicados:**
  - **Dupont Fêmea (2.54mm / 0.1"):** Para conectar diretamente nos pinos machos soldados no Arduino Nano.
  - **Conectores JST-RCY (2 pinos):** Para conexões individuais fáceis de LEDs.
  - **Conector Central (Chassi ⟷ Bolha):** Use um conector multilinha (como um **JST-XH de 6 ou 8 pinos**, ou um conector **DB9**) como junção rápida. Dessa forma, você desplugará apenas **um cabo** para separar a carroceria do chassi.

### 📐 Layout Físico do Chicote

```
 ┌────────────────────────────────────────────────────────┐
 │                      BOLHA (CARROCERIA)                │
 │                                                        │
 │   [Pisca Esq] 🟠──┐                              ┌──🟠 [Pisca Dir]
 │                   │                              │     
 │   [Farol Esq] ⬜──┼───────────┐      ┌───────────┼──⬜ [Farol Dir]
 │                   │           │      │           │     
 │                   ▼           ▼      ▼           ▼     
 │                ┌────────────────────────┐              │
 │                │  CONECTOR DE JUNÇÃO    │              │
 │                │   (JST-XH ou DB9)      │              │
 │                └───────────┬────────────┘              │
 │                            │ (Desacoplável)            │
 └────────────────────────────┼───────────────────────────┘
                              ▼
 ┌────────────────────────────┼───────────────────────────┐
 │                            │     CHASSI                │
 │                            ▼                           │
 │                     ┌──────────────┐                   │
 │                     │ Arduino Nano │                   │
 │                     └──────┬───────┘                   │
 │                            │                           │
 │   [Lanterna]  🔴◄──────────┼──────────►🔴 [Lanterna]   │
 │   [Luz Freio] 🔴◄──────────┘          ►🔴 [Luz Freio]  │
 │                                                        │
 └────────────────────────────────────────────────────────┘
```

### 📝 Passo a Passo para Montagem

1. **Dimensionamento e Corte:** Use um barbante para medir o trajeto dos cabos do local do Arduino até os locais dos LEDs na bolha/chassi. Deixe uma **folga de 3 a 5 cm** no comprimento para evitar esticar os fios.
2. **Soldagem e Isolamento:**
   - Deslize um pedaço de **tubo termoretrátil (Spaghetti)** de ~1.5cm em cada fio antes de soldar.
   - Solde o resistor limitador diretamente no terminal positivo (**Ânodo - perna mais longa**) do LED.
   - Solde os fios nos terminais, empurre o termoretrátil sobre as soldas expostas e encolha o tubo usando calor (isqueiro ou soprador).
   - **Trance os fios** de cada LED para reduzir a interferência eletromagnética (EMI) gerada pelo motor.
3. **Fixação física:** Fixe os LEDs nos copos óticos da bolha com **cola quente**, **silicone** ou **Shoe Goo**. Prenda os fios com abraçadeiras de nylon nas canaletas do chassi, longe de partes móveis.

---

## English

Wiring in an RC car needs to be robust, flexible, and organized to withstand constant vibrations and allow easy body shell removal for battery swaps and maintenance.

### 🛠️ Wire and Connector Specifications

- **Recommended Wires:** **26 AWG** or **28 AWG** **ultra-flexible silicone wires** are highly recommended since they do not break under vibration like rigid PVC wires do.
- **Recommended Connectors:**
  - **Female Dupont Connectors (2.54mm / 0.1"):** For plugging directly onto male header pins on the Arduino Nano.
  - **JST-RCY Connectors (2-pin):** For simple, individual plug-and-play LED lines.
  - **Main Harness Connector (Chassis ⟷ Body):** Use a multi-pin connector (such as a **6-pin/8-pin JST-XH** or a **DB9** connector) as a quick disconnect point. This allows you to unplug only **one cable** to separate the body shell from the chassis.

### 📐 Physical Wiring Layout

Refer to the ASCII drawing in the [Português](#português) section. Keep in mind:
- Connectors should decouple the body (holding headlights and blinkers) from the chassis (holding the Arduino, receiver, tail, and brake lights).

### 📝 Step-by-Step Assembly

1. **Measuring and Cutting:** Use a piece of string to trace the wire path from the Arduino mount to the LED mounts on the body or chassis. Add **3 to 5 cm of slack** to prevent tension on the wires.
2. **Soldering and Insulation:**
   - Slide a ~1.5cm piece of **heat-shrink tubing** onto each wire before soldering.
   - Solder the limiting resistor directly to the positive terminal (**Anode - longer leg**) of the LED.
   - Solder the wires to the pins, slide the tubing over the bare connections, and apply heat (lighter or heat gun) to seal them.
   - **Twist the wire pairs** for each LED to minimize electromagnetic interference (EMI) from the motor.
3. **Chassis Routing:** Glue the LEDs into the light buckets of the body shell using **hot glue**, **silicone**, or **Shoe Goo**. Tie wires along the chassis using zip-ties, keeping them away from moving parts (suspension, driveshafts, gears).
