# Guia de Confecção dos Chicotes — Sistema de Luzes RC v2.0

[🇧🇷 **Versão em Português**](#-português) | [🇺🇸 **English Version (LED_HARNESS.md)**](LED_HARNESS.md)

---

## Português

Este guia orienta a confecção dos **3 chicotes** do automodelo RC utilizando os conectores da **Linha MODU / Dupont (Passo 2.54mm)**:
1. **Chicote do Receptor e Alimentação (5 vias)** — Alimenta o Arduino (VCC + GND) através do **Canal 6 (CH6)** e lê os sinais de controle (CH1, CH2 e CH4).
2. **Chicote Dianteiro da Bolha (4 vias)** — Faróis e piscas dianteiros.
3. **Chicote Traseiro da Bolha (6 vias)** — Lanternas, luz de freio e piscas traseiros (com afunilamento dos 12 fios existentes).

---

### 🛠️ 1. Lista de Materiais e Conectores (HU Infinito)

* **Conectores MODU (Passo 2.54mm):**
  * 1x [Alojamento MODU Fêmea 4 Vias (1x04)](https://www.huinfinito.com.br/conectores/185-conector-modu-femea-alojamento-01x04-180-graus.html) — Para o Chicote Dianteiro.
  * 1x [Alojamento MODU Fêmea 6 Vias (1x06)](https://www.huinfinito.com.br/conectores/547-conector-modu-femea-alojamento-01x06-180-graus.html) — Para o Chicote do Rádio/Alimentação (usa 5 vias).
  * 1x [Alojamento MODU Fêmea 6 Vias (1x06)](https://www.huinfinito.com.br/conectores/547-conector-modu-femea-alojamento-01x06-180-graus.html) — Para o Chicote Traseiro (usa 5 vias).
  * 20x [Terminais MODU Fêmea 1T](https://www.huinfinito.com.br/conectores/186-terminal-modu-femea-1t.html) — Para crimpar/soldar nas pontas dos fios.
  * 1x [Barra de Pinos Macho 1x40 180°](https://www.huinfinito.com.br/conectores/165-conector-barra-de-pinos-macho-1x40x112-180-graus.html) — Para soldar na placa do chassi.
* **Placa Perfurada:**
  * 1x [Placa Universal Perfurada 5x7cm](https://www.huinfinito.com.br/placas-circuito-impresso/1861-placa-universal-perfurada-face-simples-5x7cm.html)
* **Fios Recomendados:** Fios de **28 AWG ou 30 AWG com silicone flexível**.
* **Isolamento:** Tubos termoretráteis de 1.5mm, 2.5mm e 5.0mm.

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
 │                ┌──────────────────┐                    │
 │                │ PLACA HUB SHIELD │◄── Cabo Rádio (5P) ├─── 📡 Receptor FS-BS6
 │                │   (5x7 cm)       │   [VCC/GND no CH6] │    (Chassi)
 │                └──────────────────┘   [CH1, CH2, CH4]  │
 │                       CHASSI                           │
 └────────────────────────────────────────────────────────┘
```

---

### 📝 3. Montagem dos Chicotes Passo a Passo

#### 📡 Chicote A: Cabo do Receptor com Alimentação via CH6 (5 Vias)
Este cabo conecta o receptor FlySky FS-BS6 ao Shield do Arduino. Toda a energia do Arduino e dos LEDs vem da porta **CH6** (alimentada pelo BEC do ESC).

```
LADO PLACA SHIELD (MODU Fêmea)                LADO RECEPTOR FLYSKY FS-BS6
──────────────────────────────                ───────────────────────────
[Pino 1: GND]   (Fio Preto)   ──────────────→ CH6 (Linha Inferior - GND)
[Pino 2: +5V]   (Fio Vermelho)──────────────→ CH6 (Linha Central - VCC +5V)
[Pino 3: CH1]   (Fio Branco)  ──────────────→ CH1 (Linha Superior - Sinal Volante)
[Pino 4: CH2]   (Fio Amarelo) ──────────────→ CH2 (Linha Superior - Sinal Throttle)
[Pino 5: CH4]   (Fio Verde)   ──────────────→ CH4 (Linha Superior - Sinal Chave Farol)
```
* **Comprimento:** ~10 cm a 15 cm.
* **Como montar a ponta do receptor:**
  * Você pode usar **1 conector de servo padrão de 3 vias** com os fios Preto e Vermelho para plugar direto no **CH6**.
  * Use conectores individuais de 1 pino para plugar os fios de sinal nos canais **CH1**, **CH2** e **CH4**.

---

#### 💡 Chicote B: Dianteiro (Alojamento MODU 4 Vias Fêmea)

```
[Pino 1: GND Comum] ──────→ Todos os Cátodos (-) dos LEDs dianteiros unidos
[Pino 2: Farol D9]  ──────→ Ânodos (+) dos LEDs Farol Esq + Farol Dir
[Pino 3: Pisca FE]  ──────→ Ânodo (+) do LED Pisca Dianteiro Esquerdo
[Pino 4: Pisca FD]  ──────→ Ânodo (+) do LED Pisca Dianteiro Direito
```

---

#### 💡 Chicote C: Traseiro (Alojamento MODU 6 Vias Fêmea - Afunilamento de 12 Fios)
Aproveita a fiação traseira existente unindo os fios na ponta:

```
FIOS EXISTENTES DA BOLHA (12 Fios)            CONECTOR FINAL (MODU 6P)
──────────────────────────────────            ────────────────────────
6 Fios GND (Catodos dos LEDs) ───[Soldar juntos]───→ [Pino 1: GND Comum]
2 Fios Positivos das Lanternas ──[Soldar juntos]───→ [Pino 2: Lanternas D5]
2 Fios Positivos dos Freios    ──[Soldar juntos]───→ [Pino 3: Luz Freio D6]
1 Fio Positivo Pisca TE        ────────────────────→ [Pino 4: Pisca TE D7]
1 Fio Positivo Pisca TD        ────────────────────→ [Pino 5: Pisca TD D8]
                                                     [Pino 6: Livre / Reserva]
```

---

### 🛡️ 4. Isolamento e Proteção contra Água e Vibração

1. **Vedação dos Conectores:**
   - Aplique uma pequena porção de **graxa de silicone dielétrica** ou vaselina sólida dentro dos conectores fêmeas antes de plugar na placa. Isso expulsa a água e impede oxidação por barro e umidade.
2. **Proteção da Placa Hub:**
   - Pincele **esmalte incolor**, **verniz isolante (conformal coating)** ou fita isolante líquida sobre as soldas e trilhas no verso da placa perfurada.
3. **Fixação na Bolha:**
   - Prenda os fios com **fita de alumínio** e use **malha náutica (*sleeving*)** nos trechos soltos que ligam a bolha ao chassi.

---

## English

This document provides step-by-step instructions for assembling the 3 wiring harnesses using **MODU / Dupont 2.54mm connectors**:
1. **Radio Receiver Cable (5-pin)**: Powers the Arduino (VCC + GND) via **CH6** and carries control signals (CH1, CH2, CH4).
2. **Front LED Harness (4-pin)**: Headlights and Front Blinkers.
3. **Rear LED Harness (6-pin)**: Tail lights, Brake lights, and Rear Blinkers (condensing 12 body wires into 5 active pins).
