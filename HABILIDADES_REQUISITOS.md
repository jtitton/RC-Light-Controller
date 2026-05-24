# Habilidades, Requisitos e Ferramentas / Skills and Requirements

[**Português**](#português) | [**English**](#english)

---

## Português

Para montar, calibrar e instalar com sucesso este sistema de luzes em seu carro RC, você precisará de algumas ferramentas de eletrônica básica e certas habilidades manuais.

### 🛠️ Ferramentas Necessárias

| Ferramenta | Utilidade no Projeto | Importância |
|---|---|:---:|
| **Ferro de Solda (30W a 60W)** | Fazer as conexões elétricas permanentes e seguras. | **Indispensável** |
| **Estanho de Solda (com fluxo)** | Ligar eletricamente os fios, resistores e LEDs. | **Indispensável** |
| **Tubo Termoretrátil (1mm a 3mm)**| Isolar as emendas de fios e pernas expostas dos LEDs. | **Indispensável** |
| **Alicate de Corte e Descascador** | Cortar e expor a ponta metálica dos fios. | **Indispensável** |
| **Multímetro Digital** | Medir continuidade (curtos) e testar a polaridade de LEDs. | **Altamente Recomendado** |
| **Pistola de Cola Quente ou Silicone**| Fixar os LEDs nos suportes óticos e prender fios na bolha.| **Recomendado** |

### 🧠 Habilidades Recomendadas

1. **Soldagem Eletrônica Básica:** Você precisará soldar fios nos terminais dos LEDs e resistores. Aqueça a junção por 2 segundos antes de aplicar o estanho para obter uma solda brilhante e resistente.
2. **Identificação de Polaridade de Componentes:** LEDs possuem lado positivo (Anodo, perna longa) e negativo (Catodo, perna curta/chanfro). O resistor deve ser soldado preferencialmente na perna positiva (Anodo).
3. **Uso do Multímetro (Básico):** Meça a continuidade entre o pino de 5V e o GND antes de alimentar a placa. Se houver um "bipe", pare e procure por curto-circuitos para evitar queimar o Arduino ou o BEC.
4. **Teste de Luminosidade e Ajuste de Resistência:** Os resistores fornecidos no projeto são estimativas de segurança. É de extrema importância que você **faça testes de bancada provisórios** antes de soldar definitivamente:
   - **Ajuste de intensidade:** LEDs de diferentes marcas possuem eficiências distintas. Se a intensidade ficar inadequada (muito forte ou muito fraca), sinta-se à vontade para trocar o resistor para mais ou para menos resistência.
   - **Segurança física:** Aumentar a resistência é seguro e economiza bateria. Se decidir diminuir a resistência para aumentar o brilho, não baixe de $82\Omega$ para o farol branco e $120\Omega$ para os demais LEDs para evitar sobrecorrente.

### 🔍 Resolução de Problemas (Troubleshooting)

- **O LED não acende:** Verifique se não está invertido, se a solda não se soltou ou se o resistor não é de valor alto demais (ex: usar $15\text{k}\Omega$ ao invés de $150\Omega$).
- **O Arduino não responde aos comandos:** Verifique se o pino GND do receptor de rádio está ligado ao GND do Arduino (referência comum). Verifique os pinos corretos: Volante no D4, Aceleração no D2, Farol no D3. Configure o Monitor Serial para **115200 baud**.
- **O farol pisca ou oscila sozinho (ruído):** Motores elétricos geram interferência. Use um capacitor de $100\mu\text{F}$ entre o pino 5V e o GND do Arduino Nano para estabilizar a tensão.

---

## English

To successfully build, calibrate, and install this light system, you will need basic electronics tools and some manual assembly skills.

### 🛠️ Required Tools

| Tool | Purpose | Importance |
|---|---|:---:|
| **Soldering Iron (30W to 60W)** | Create permanent and secure electrical connections. | **Required** |
| **Solder Wire (with flux core)**| Electronically connect wires, resistors, and LEDs. | **Required** |
| **Heat-Shrink Tubing (1mm to 3mm)**| Insulate bare solder joints and LED legs. | **Required** |
| **Wire Cutters & Strippers** | Cut wires and strip insulation to expose copper. | **Required** |
| **Digital Multimeter** | Check continuity (shorts) and test LED polarity. | **Highly Recommended** |
| **Hot Glue Gun or Silicone** | Secure LEDs inside light buckets and route wires. | **Recommended** |

### 🧠 Recommended Skills

1. **Basic Soldering:** You will need to solder wires onto LEDs and resistors. Heat the joint for 2 seconds before applying solder to get a shiny, reliable connection.
2. **Polarity Identification:** LEDs have a positive side (Anode, longer leg) and a negative side (Cathode, shorter leg/flat side). The resistor should be soldered to the positive leg (Anode).
3. **Multimeter Usage (Basic):** Measure continuity between 5V and GND before powering the board. If the multimeter "beeps", you have a short circuit. Find and fix it to avoid damaging the Arduino or BEC.
4. **Brightness Testing and Resistor Tuning:** Resistors calculated in this project are safety estimates. It is crucial to **run temporary tests on a breadboard** before final assembly:
   - **Brightness tuning:** LEDs from different manufacturers have varying light output. If you find the brightness inadequate (too dim or too bright), swap the resistor for one with more or less resistance.
   - **Safety limits:** Increasing resistance is safe and saves battery. If reducing resistance to increase brightness, do not go below $82\Omega$ for the white headlight and $120\Omega$ for other LEDs to avoid overcurrent.

### 🔍 Troubleshooting

- **LED does not light up:** Check if the LED is reversed, if there is a loose solder joint, or if the resistor value is too high (e.g. using $15\text{k}\Omega$ instead of $150\Omega$).
- **Arduino does not respond to the transmitter:** Ensure the receiver's GND is connected to the Arduino's GND (common reference). Double-check pins: Steering on D4, Throttle on D2, Headlight on D3. Set the Serial Monitor to **115200 baud**.
- **Headlights flicker or trigger randomly (noise):** Electric motors generate noise. Place a $100\mu\text{F}$ capacitor between the 5V and GND pins of the Arduino Nano to stabilize the power line.
