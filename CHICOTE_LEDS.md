# Guia de Confecção dos Chicotes — Sistema de Luzes RC v8.4

[🇧🇷 **Versão em Português**](#-português) | [🇺🇸 **English Version (LED_HARNESS.md)**](LED_HARNESS.md) | [📜 **Premissas Oficiais (PREMISSAS_PROJETO.md)**](PREMISSAS_PROJETO.md)

---

## 🇧🇷 Português

Este guia orienta a confecção dos **4 chicotes desacopláveis** do automodelo RC utilizando conectores da **Linha MODU / Dupont (Passo padrão de 2.54mm / 0.1") em 90°** com o **Layout Natural Distribuído (v8.4)**:

1. **Chicote do Receptor e Alimentação (5 vias em 90° na Lateral Direita - CON1)** — Alimenta o sistema via **Canal 6 (CH6)** com **BEC de 6.0V** (reduzido internamente na placa para +5.25V pelo diodo D1 1N4007) e lê os sinais de controle (CH2 Throttle, CH4 Chave Farol, CH1 Volante).
2. **Chicote do Acelerômetro MPU-6050 (4 vias em 90° na Lateral Esquerda - CON4)** — Interface I2C direta 1:1 (**GND, TX [SCL], RX [SDA], VCC [+5.25V]**) para fixação do sensor GY-521 no chassi.
3. **Chicote Dianteiro da Bolha (4 vias em 90° na Lateral Superior Direita - CON2)** — **4 Faróis Brancos em paralelo** acionados pelo driver transistorizado **Q1 (BC337)** com resistor **R1 ($27\,\Omega$)** na placa (~11 a 14 mA por LED, 45 a 55 mA total), além dos piscas dianteiros (2 LEDs laranjas por lado via **$100\,\Omega$**). Localizado no **mesmo lado do rádio** (lateral direita, acima de CON1).
4. **Chicote Traseiro da Bolha (6 vias em 90° na Borda Inferior Centro-Direita - CON3)** — Lanternas, freios e piscas traseiros (2 LEDs por canal em paralelo, todos limitados por resistores de **$100\,\Omega$** na placa), afunilando os fios da bolha em um conector único.

> [!IMPORTANT]
> **ZERO RESISTORES NA BOLHA:** Todos os resistores limitadores de corrente e o transistor driver dos faróis estão montados diretamente na **Placa Shield Hub**. A fiação da bolha contém unicamente os LEDs e seus respectivos fios, simplificando a instalação e reduzindo o peso na carroceria!

---

### 🛠️ 1. Lista de Materiais e Conectores (HU Infinito)

* **Conectores MODU (Passo 2.54mm):**
  * 2x [Alojamento MODU Fêmea 4 Vias (1x04)](https://www.huinfinito.com.br/conectores/185-conector-modu-femea-alojamento-01x04-180-graus.html) — Para Chicote Dianteiro (CON2) e Chicote MPU-6050 (CON4).
  * 1x [Alojamento MODU Fêmea 6 Vias (1x06)](https://www.huinfinito.com.br/conectores/547-conector-modu-femea-alojamento-01x06-180-graus.html) — Para Chicote do Rádio/Alimentação (usa 5 vias).
  * 1x [Alojamento MODU Fêmea 6 Vias (1x06)](https://www.huinfinito.com.br/conectores/547-conector-modu-femea-alojamento-01x06-180-graus.html) — Para Chicote Traseiro (usa 6 vias).
  * 25x [Terminais MODU Fêmea 1T](https://www.huinfinito.com.br/conectores/186-terminal-modu-femea-1t.html) — Para crimpar/soldar nas pontas dos fios.
  * 1x Barra de Pinos Macho 1x40 90° (para soldar nas bordas da placa Shield em ângulo reto voltado para fora).
* **Placa Perfurada:**
  * 1x [Placa Universal Perfurada 5x7cm](https://www.huinfinito.com.br/placas-circuito-impresso/1861-placa-universal-perfurada-face-simples-5x7cm.html)
* **Fios Recomendados:** Fios de **28 AWG ou 30 AWG com silicone flexível**.
* **Isolamento:** Tubos termorretráteis de 1.5mm, 2.5mm e 5.0mm.

---

### 📐 2. Layout Geral da Fiação

```
 ┌────────────────────────────────────────────────────────┐
 │                   CARROCERIA (BOLHA)                   │
 │                                                        │
 │   [Pisca FE (2x)] 🟠─┐                  ┌─🟠 [Pisca FD (2x)]
 │                      │                  │              │
 │   [Farol 4x LEDs] ⬜─┼──────┐    ┌──────┼─⬜           │
 │   (2 Princ + 2 Aux)  │      │    │      │              │
 │                      ▼      ▼    ▼      ▼              │
 │                   ┌───────────────────────┐            │
 │                   │  CHICOTE DIANTEIRO    │            │
 │                   │ (Alojamento MODU 4P)  │            │
 │                   └──────────┬────────────┘            │
 │                              │                         │
 │   [Pisca TE (2x)] 🟠─┐       │ (Desacoplável)          │
 │                      │       │                         │
 │   [Lanterna (2x)] 🔴─┼──┐    │                         │
 │                      │  │    │                         │
 │   [Luz Freio(2x)] 🔴─┼──┼─┐  │                         │
 │                      │  │ │  │                         │
 │                      ▼  ▼ ▼  ▼                         │
 │                   ┌───────────────────────┐            │
 │                   │  CHICOTE TRASEIRO     │            │
 │                   │ (Alojamento MODU 6P)  │            │
 │                   └──────────┬────────────┘            │
 │                              │ (Desacoplável)          │
 └──────────────────────────────┼─────────────────────────┘
                                │
 ┌──────────────────────────────┼─────────────────────────┐
 │                              │  (CON2 Lateral Superior │
 │                              │   Direita 90°)          │
 │                              │          │              │
 │ 🧭 MPU-6050 (GY-521)    ┌────┴──────────▼─┐  📡 FS-BS6 │
 │  [A4, A5, +5V, GND]     │ PLACA HUB SHIELD│   (CH6:    │
 │  [CON4 Lateral          │   (5x7 cm) v8.4 │◄── +6.0V/GND│
 │   Esquerda 90°]────────►│[Q1 BC337 Faróis]│    CH1,2,4)│
 │                         └────────┬────────┘   [CON1 Dir│
 │                                  │ (CON3 90° na   90°] │
 │                                  ▼  Borda Inferior)    │
 │                           CHASSI                       │
 └────────────────────────────────────────────────────────┘
```

---

### 📝 3. Montagem dos Chicotes Passo a Passo

#### 📡 Chicote A: Cabo do Receptor com Alimentação via CH6 (5 Vias)
Este cabo conecta o receptor FlySky FS-BS6 ao CON1 na lateral direita da placa Shield. Toda a energia do Arduino e dos LEDs vem da porta **CH6** (alimentada pelo BEC de 6.0V do ESC).

```
LADO PLACA SHIELD (CON1 MODU Fêmea)           LADO RECEPTOR FLYSKY FS-BS6
───────────────────────────────────           ───────────────────────────
[Pino 1: +6.0V BEC] (Fio Vermelho)──────────→ CH6 (Linha Central - VCC +6.0V BEC)
[Pino 2: GND]       (Fio Preto)   ──────────→ CH6 (Linha Inferior - GND)
[Pino 3: CH2]       (Fio Amarelo) ──────────→ CH2 (Linha Superior - Sinal Throttle D2)
[Pino 4: CH4]       (Fio Verde)   ──────────→ CH4 (Linha Superior - Sinal Chave Farol D3)
[Pino 5: CH1]       (Fio Branco)  ──────────→ CH1 (Linha Superior - Sinal Volante D4)
```
* **Comprimento:** ~10 cm a 15 cm.
* **Nota de Montagem:** A ordem 1=+6.0V BEC, 2=GND, 3=CH2, 4=CH4, 5=CH1 casa perfeitamente com os pinos de alimentação e D2, D3, D4 na barra direita do Arduino Nano, garantindo trilhas retas de 10mm sem cruzamentos. O pino 1 alimenta diretamente o ânodo do diodo D1 (1N4007) na placa.

---

#### 🧭 Chicote B: Acelerômetro MPU-6050 (4 Vias)
Conecta a placa Shield (CON4 na lateral esquerda, Linhas 10 a 13) ao módulo sensor GY-521 fixado com fita dupla face no chassi do carro (pinagem 1:1 direta com a serigrafia do sensor):

```
LADO PLACA SHIELD (CON4 MODU Fêmea)           LADO MPU-6050 (Serigrafia Sensor)
───────────────────────────────────           ─────────────────────────────────
[Pino 1: GND]       (Fio Preto)   ──────────→ Pino GND
[Pino 2: TX (SCL)]  (Fio Amarelo) ──────────→ Pino TX (Clock I2C / SCL)
[Pino 3: RX (SDA)]  (Fio Verde)   ──────────→ Pino RX (Dados I2C / SDA)
[Pino 4: VCC (+5V)] (Fio Vermelho)──────────→ Pino VCC (+5V)
```
* **Comprimento:** ~5 cm a 10 cm.
* **Nota de Montagem:** Pinagem 1:1 estrita e reta! Não há cruzamento de fios no chicote: o pino 1 do conector fêmea liga ao pino 1 do sensor, 2 no 2, 3 no 3 e 4 no 4.

---

#### 💡 Chicote C: Dianteiro (Alojamento MODU 4 Vias Fêmea)
Conecta a placa Shield (CON2 na lateral superior direita, Coluna 17, Linhas 04 a 07 — mesmo lado do rádio) aos LEDs instalados na dianteira da bolha:

```
[Pino 1: GND Comum] (Fio Preto, Lin 07)   ──→ Todos os Cátodos (-) dos LEDs dianteiros unidos (4x Farol + 4x Piscas)
[Pino 2: Farol D9]  (Fio Branco, Lin 06)  ──→ Ânodos (+) dos 4 LEDs de Farol em paralelo (Alimentado por Q1 BC337 + R1 27Ω)
[Pino 3: Pisca FE]  (Fio Laranja, Lin 05) ──→ Ânodos (+) dos 2 LEDs Pisca Diant. Esquerdo em paralelo (via R2 100Ω)
[Pino 4: Pisca FD]  (Fio Azul, Lin 04)    ──→ Ânodos (+) dos 2 LEDs Pisca Diant. Direito em paralelo (via R3 100Ω)
```

---

#### 💡 Chicote D: Traseiro (Alojamento MODU 6 Vias Fêmea)
Conecta a placa Shield (CON3 na borda inferior, Colunas 08 a 13, Linha 24) aos LEDs instalados na traseira da bolha:

```
FIOS EXISTENTES DA BOLHA (LEDs Traseiros)     CONECTOR FINAL (MODU 6P)
─────────────────────────────────────────     ────────────────────────
2 Fios (+) Pisca TD (em paralelo) ──────────→ [Pino 1: Pisca TD D8 (via R7 100Ω)]
2 Fios (+) Pisca TE (em paralelo) ──────────→ [Pino 2: Pisca TE D7 (via R6 100Ω)]
2 Fios (+) dos Freios (em paralelo) ────────→ [Pino 3: Luz Freio D6 (via R5 100Ω)]
2 Fios (+) das Lanternas (em paralelo) ─────→ [Pino 4: Lanternas D5 (via R4 100Ω)]
                                              [Pino 5: Livre / Reserva]
Todos os Cátodos (-) unidos (GND Comum) ────→ [Pino 6: GND Comum]
```
*(Nota: O arranjo das saídas traseiras segue o roteamento em "L" aninhado da placa, com ZERO cruzamento de trilhas e GND alinhado ao pino 6).*

---

### 🛡️ 4. Isolamento e Proteção contra Água e Vibração

1. **Vedação dos Conectores:**
   - Aplique uma pequena porção de **graxa de silicone dielétrica** ou vaselina sólida dentro dos conectores fêmeas antes de plugar na placa. Isso expulsa a água e impede oxidação por barro e umidade.
2. **Proteção da Placa Hub & MPU-6050:**
   - Pincele **esmalte incolor**, **verniz isolante (conformal coating)** ou fita isolante líquida sobre as soldas e trilhas no verso da placa perfurada e no módulo GY-521.
3. **Fixação na Bolha:**
   - Prenda os fios com **fita de alumínio** e use **malha náutica (*sleeving*)** nos trechos soltos que ligam a bolha ao chassi.

---

## English

Consulte [LED_HARNESS.md](LED_HARNESS.md) para o guia detalhado de confecção dos chicotes em Inglês.

