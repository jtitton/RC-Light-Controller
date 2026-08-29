# Habilidades, Requisitos e Solução de Problemas — Sistema de Luzes RC v6.0

[🇧🇷 **Versão em Português**](#-português) | [🇺🇸 **English Version (SKILLS_REQUIREMENTS.md)**](SKILLS_REQUIREMENTS.md)

---

## Português

Para montar, calibrar e instalar com sucesso este sistema de iluminação em seu carro RC, você precisará de ferramentas básicas de eletrônica, habilidades manuais e materiais de proteção contra água e vibração.

### 🛠️ Ferramentas e Materiais Necessários

| Ferramenta / Material | Utilidade no Projeto | Importância |
|---|---|:---:|
| **Ferro de Solda (30W a 60W)** | Fazer as conexões elétricas permanentes na placa shield e chicotes. | **Indispensável** |
| **Estanho de Solda (com fluxo)** | Ligar eletricamente os fios, resistores e terminais MODU. | **Indispensável** |
| **Tubo Termoretrátil (1.5mm a 5mm)**| Isolar emendas, derivações de GND e pernas expostas dos LEDs. | **Indispensável** |
| **Alicate de Corte e Descascador** | Cortar e expor a ponta metálica dos fios flexíveis. | **Indispensável** |
| **Alicate de Bico Fino ou de Crimpagem**| Cravar os terminais MODU fêmea nos fios da bolha. | **Indispensável** |
| **Multímetro Digital** | Medir continuidade (curtos) e conferir a polaridade dos LEDs. | **Altamente Recomendado** |
| **Graxa de Silicone Dielétrica / Vaselina**| Vedar os conectores MODU contra água, poeira e oxidação. | **Recomendado (Off-Road)**|
| **Fita de Alumínio Automotiva** | Fixar e ocultar os fios no teto/laterais da bolha. | **Recomendado** |
| **Silicone Neutro / Shoe Goo / E6000**| Fixar e vedar a traseira dos LEDs nos copos óticos da bolha.| **Recomendado** |
| **Verniz Isolante / Esmalte Incolor** | Proteger as trilhas e soldas no verso da placa shield. | **Recomendado** |

### 🧠 Habilidades Recomendadas

1. **Soldagem Eletrônica Básica:** Solde os resistores e a barra de pinos macho na placa perfurada de 5x7cm. Aqueça a junção por 2 segundos antes de aplicar o estanho para obter uma solda brilhante e resistente à vibração.
2. **Identificação de Polaridade de Componentes:** LEDs possuem lado positivo (**Ânodo**, perna longa) e negativo (**Cátodo**, perna curta/chanfro). Todos os cátodos se unem no barramento de GND comum.
3. **Uso do Multímetro (Básico):** Meça a continuidade entre a trilha de 5V e o GND da placa shield antes de ligar no receptor. Se houver um "bipe", pare e remova o curto-circuito antes de energizar pelo CH6.
4. **Teste de Luminosidade e Ajuste de Resistência:** Os resistores fornecidos ($100\Omega$ e $150\Omega$) são referências de segurança para $20\text{mA}$. É seguro aumentar a resistência para $220\Omega$ ou $330\Omega$ para economizar bateria ou atenuar o brilho. Nunca reduza abaixo de $82\Omega$ no farol e $120\Omega$ nos demais LEDs.

### 🔍 Resolução de Problemas (Troubleshooting)

- **O LED não acende:** Verifique se a polaridade do LED não está invertida, se o conector MODU está encaixado na posição correta ou se a solda do resistor está íntegra.
- **O Arduino não responde aos comandos do rádio:**
  - Verifique se o cabo do rádio (CON1) está plugado corretamente: **Pino 1 no GND** e **Pino 2 no VCC (+5V)** do canal **CH6**.
  - Verifique os canais de sinal: Volante no **CH1 (D4)**, Acelerador no **CH2 (D2)**, Farol no **CH4 (D3)**.
- **O carro liga mas o neutro está torto ou o pisca fica aceso direto:**
  - Desligue o carro, certifique-se de que o volante e o gatilho estão centralizados no rádio, e ligue o carro novamente. O Arduino recalibrará o neutro automaticamente nos primeiros 2 segundos.
- **Como recalibrar os limites na pista sem computador:**
  - Ligue o rádio, segure o volante **todo virado para a direita (ou esquerda)** e ligue o carro mantendo o volante virado por 2 segundos. O Arduino entrará no modo de calibração autônoma guiada pelos LEDs.
- **Faróis oscilam ou piscam sozinhos sob aceleração forte (ruído eletromagnético):**
  - Adicione um capacitor eletrolítico de $100\mu\text{F} \times 16\text{V}$ entre o pino 5V e o GND da placa shield para filtrar transientes do motor elétrico.

---

## English

To successfully build, calibrate, and install this light system, you will need basic electronics tools, manual skills, and materials for vibration and waterproofing.

### 🛠️ Required Tools & Materials

| Tool / Material | Purpose | Importance |
|---|---|:---:|
| **Soldering Iron (30W to 60W)** | Create permanent electrical connections on the shield board and harness. | **Required** |
| **Solder Wire (with flux core)**| Solder wires, resistors, and MODU pin headers. | **Required** |
| **Heat-Shrink Tubing (1.5mm to 5mm)**| Insulate splices, ground joints, and bare pins. | **Required** |
| **Wire Cutters & Strippers** | Cut and strip flexible silicone wires. | **Required** |
| **Needle-Nose Pliers or Crimper**| Crimp female MODU terminals onto body harness wires. | **Required** |
| **Digital Multimeter** | Check continuity (shorts) and verify LED polarity. | **Highly Recommended** |
| **Dielectric Silicone Grease** | Seal MODU connectors against water, mud, and corrosion. | **Recommended (Off-Road)**|
| **Aluminum Foil Tape** | Secure and hide wiring harnesses along the body shell. | **Recommended** |
| **Silicone / Shoe Goo / E6000**| Secure and seal LED backs inside body light buckets. | **Recommended** |
| **Conformal Coating / Clear Polish**| Protect shield board solder traces against moisture. | **Recommended** |

### 🧠 Recommended Skills

1. **Basic Soldering:** Solder the resistors and male pin headers onto the 5x7cm perfboard. Heat joints for 2 seconds before applying solder to create vibration-resistant joints.
2. **Polarity Identification:** LEDs have an Anode (positive, longer leg) and Cathode (negative, shorter leg/flat rim). All cathodes connect to the common ground rail.
3. **Multimeter Testing:** Check continuity between 5V and GND on the shield board before connecting to the receiver. If you hear a beep, remove the short circuit before powering via CH6.
4. **Brightness Tuning:** The included resistor values ($100\Omega$ and $150\Omega$) are standard $20\text{mA}$ safety limits. Increasing resistance to $220\Omega$ or $330\Omega$ saves battery. Do not drop below $82\Omega$ for headlights and $120\Omega$ for other LEDs.

### 🔍 Troubleshooting

- **LED does not turn on:** Verify LED polarity, ensure the MODU connector is aligned correctly, and check the resistor solder joint.
- **Arduino does not respond to transmitter commands:**
  - Verify CON1 cable: **Pin 1 to GND** and **Pin 2 to VCC (+5V)** on receiver channel **CH6**.
  - Check signal lines: Steering on **CH1 (D4)**, Throttle on **CH2 (D2)**, Headlight on **CH4 (D3)**.
- **Blinkers stay on while driving straight (trim drift):**
  - Power off the car, leave steering and throttle sticks centered, and turn the car back on. The auto-centering routine recalibrates neutral in the first 2 seconds.
- **How to recalibrate endpoints on the track without a PC:**
  - Turn on the transmitter, hold the steering wheel fully turned right (or left), and turn on the car while holding for 2 seconds. The Arduino enters standalone calibration mode guided by the LEDs.
- **Headlights flicker during hard acceleration (motor EMI noise):**
  - Solder a $100\mu\text{F} \times 16\text{V}$ electrolytic capacitor between the 5V and GND pins on the shield board.
