# Guia de Confecção dos Chicotes — Sistema de Luzes RC v8.0

[🇧🇷 **Versão em Português**](#-português) | [🇺🇸 **English Version (LED_HARNESS.md)**](LED_HARNESS.md)

---

## 🇧🇷 Português

Este guia orienta a confecção dos **4 chicotes desacopláveis** do automodelo RC utilizando conectores da **Linha MODU / Dupont (Passo padrão de 2.54mm / 0.1") em 90°** com o **Layout Natural Distribuído (v8.0)**:

1. **Chicote do Receptor e Alimentação (5 vias em 90° na Lateral Esquerda)** — Alimenta o Arduino (5V e GND) através do **Canal 6 (CH6)** e lê os sinais de controle (CH2 Throttle, CH4 Chave Farol, CH1 Volante).
2. **Chicote do Acelerômetro MPU-6050 (4 vias em 90° na Lateral Direita)** — Interface I2C (GND, +5V, SCL A5, SDA A4) para fixação do sensor GY-521 no chassi.
3. **Chicote Dianteiro da Bolha (4 vias em 90° na Borda Inferior Esquerda)** — Faróis duplos e piscas dianteiros.
4. **Chicote Traseiro da Bolha (6 vias em 90° na Borda Inferior Centro-Direita)** — Lanternas, freios e piscas traseiros (afunilamento dos 12 fios da bolha em um conector único).

---

### 🛠️ 1. Lista de Materiais e Conectores (HU Infinito)

* **Conectores MODU (Passo 2.54mm):**
  * 2x [Alojamento MODU Fêmea 4 Vias (1x04)](https://www.huinfinito.com.br/conectores/185-conector-modu-femea-alojamento-01x04-180-graus.html) — Para Chicote Dianteiro e Chicote MPU-6050.
  * 1x [Alojamento MODU Fêmea 6 Vias (1x06)](https://www.huinfinito.com.br/conectores/547-conector-modu-femea-alojamento-01x06-180-graus.html) — Para Chicote do Rádio/Alimentação (usa 5 vias).
  * 1x [Alojamento MODU Fêmea 6 Vias (1x06)](https://www.huinfinito.com.br/conectores/547-conector-modu-femea-alojamento-01x06-180-graus.html) — Para Chicote Traseiro (usa 6 vias).
  * 25x [Terminais MODU Fêmea 1T](https://www.huinfinito.com.br/conectores/186-terminal-modu-femea-1t.html) — Para crimpar/soldar nas pontas dos fios.
  * 1x [Barra de Pinos Macho 1x40 90°](https://www.huinfinito.com.br/conectores/165-conector-barra-de-pinos-macho-1x40x112-180-graus.html) — Para soldar nas bordas da placa Shield.
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
 │   [Pisca FE] 🟠──┐                  ┌──🟠 [Pisca FD]   │
 │                  │                  │                  │
 │   [Farol Esq]⬜──┼──────┐    ┌──────┼──⬜ [Farol Dir]  │
 │                  │      │    │      │                  │
 │                  ▼      ▼    ▼      ▼                  │
 │               ┌───────────────────────┐                │
 │               │  CHICOTE DIANTEIRO    │                │
 │               │ (Alojamento MODU 4P)  │                │
 │               └──────────┬────────────┘                │
 │                          │                             │
 │   [Pisca TE] 🟠──┐       │ (Desacoplável)              │
 │                  │       │                             │
 │   [Lanterna] 🔴──┼──┐    │                             │
 │                  │  │    │                             │
 │   [Luz Freio]🔴──┼──┼─┐  │                             │
 │                  │  │ │  │                             │
 │                  ▼  ▼ ▼  ▼                             │
 │               ┌───────────────────────┐                │
 │               │  CHICOTE TRASEIRO     │                │
 │               │ (Alojamento MODU 6P)  │                │
 │               └──────────┬────────────┘                │
 │                          │ (Desacoplável)              │
 └──────────────────────────┼─────────────────────────────┘
                            ▼
 ┌────────────────────────────────────────────────────────┐
 │                          ▼                             │
 │ 📡 Receptor FS-BS6  ┌──────────────────┐  🧭 MPU-6050  │
 │  (CH6: +5V/GND      │ PLACA HUB SHIELD │   (GY-521)    │
 │   CH1, CH2, CH4) ──►│   (5x7 cm)       │◄── [A4, A5,   │
 │   [CON1 Lateral     │                  │     +5V, GND] │
 │    Esquerda 90°]    │                  │    [CON4 Lat. │
 │                     └────────┬─────────┘     Dir. 90°] │
 │                              │ (CON2 & CON3 90°        │
 │                              ▼  na Borda Inferior)     │
 │                       CHASSI                           │
 └────────────────────────────────────────────────────────┘
```

---

### 📝 3. Montagem dos Chicotes Passo a Passo

#### 📡 Chicote A: Cabo do Receptor com Alimentação via CH6 (5 Vias)
Este cabo conecta o receptor FlySky FS-BS6 ao CON1 na lateral esquerda da placa Shield. Toda a energia do Arduino e dos LEDs vem da porta **CH6** (alimentada pelo BEC do ESC).

```
LADO PLACA SHIELD (CON1 MODU Fêmea)           LADO RECEPTOR FLYSKY FS-BS6
───────────────────────────────────           ───────────────────────────
[Pino 1: +5V]   (Fio Vermelho)──────────────→ CH6 (Linha Central - VCC +5V)
[Pino 2: GND]   (Fio Preto)   ──────────────→ CH6 (Linha Inferior - GND)
[Pino 3: CH2]   (Fio Amarelo) ──────────────→ CH2 (Linha Superior - Sinal Throttle D2)
[Pino 4: CH4]   (Fio Verde)   ──────────────→ CH4 (Linha Superior - Sinal Chave Farol D3)
[Pino 5: CH1]   (Fio Branco)  ──────────────→ CH1 (Linha Superior - Sinal Volante D4)
```
* **Comprimento:** ~10 cm a 15 cm.
* **Nota de Montagem:** A ordem 1=5V, 2=GND, 3=CH2, 4=CH4, 5=CH1 casa perfeitamente com os pinos de alimentação e D2, D3, D4 do Arduino Nano, garantindo trilhas retas de 10mm sem cruzamentos.

---

#### 🧭 Chicote B: Acelerômetro MPU-6050 (4 Vias)
Conecta a placa Shield ao módulo sensor GY-521 fixado com fita dupla face no chassi do carro:

```
LADO PLACA SHIELD (MODU Fêmea)                LADO MPU-6050 (GY-521)
──────────────────────────────                ──────────────────────
[Pino 1: GND]   (Fio Preto)   ──────────────→ Pino GND
[Pino 2: +5V]   (Fio Vermelho)──────────────→ Pino VCC
[Pino 3: SCL]   (Fio Amarelo) ──────────────→ Pino SCL
[Pino 4: SDA]   (Fio Verde)   ──────────────→ Pino SDA
```
* **Comprimento:** ~5 cm a 10 cm.

---

#### 💡 Chicote C: Dianteiro (Alojamento MODU 4 Vias Fêmea)

```
[Pino 1: GND Comum] ──────→ Todos os Cátodos (-) dos LEDs dianteiros unidos
[Pino 2: Farol D9]  ──────→ Ânodos (+) dos LEDs Farol Esq + Farol Dir
[Pino 3: Pisca FE]  ──────→ Ânodo (+) do LED Pisca Dianteiro Esquerdo
[Pino 4: Pisca FD]  ──────→ Ânodo (+) do LED Pisca Dianteiro Direito
```

---

#### 💡 Chicote D: Traseiro (Alojamento MODU 6 Vias Fêmea - Afunilamento de 12 Fios)
Aproveita a fiação traseira existente unindo os fios na ponta:

```
FIOS EXISTENTES DA BOLHA (12 Fios)            CONECTOR FINAL (MODU 6P)
──────────────────────────────────            ────────────────────────
1 Fio Positivo Pisca TD        ────────────────────→ [Pino 1: Pisca TD D8]
1 Fio Positivo Pisca TE        ────────────────────→ [Pino 2: Pisca TE D7]
2 Fios Positivos dos Freios    ──[Soldar juntos]───→ [Pino 3: Luz Freio D6]
2 Fios Positivos das Lanternas ──[Soldar juntos]───→ [Pino 4: Lanternas D5]
                                                     [Pino 5: Livre / Reserva]
6 Fios GND (Catodos dos LEDs) ───[Soldar juntos]───→ [Pino 6: GND Comum]
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

This document provides step-by-step instructions for assembling the quick-disconnect wiring harnesses using **MODU / Dupont 2.54mm connectors**:
1. **Radio Receiver Cable (5-pin)**: Powers the Arduino (VCC + GND) via **CH6** and carries control signals (CH1, CH2, CH4).
2. **MPU-6050 Accelerometer Cable (4-pin)**: I2C bus interface (GND, +5V, SDA A4, SCL A5).
3. **Front LED Harness (4-pin)**: Headlights and Front Blinkers.
4. **Rear LED Harness (6-pin)**: Tail lights, Brake lights, and Rear Blinkers.
