# Esquema de Ligação — Sistema de Luzes RC v7.0

[🇧🇷 **Versão em Português**](#-português) | [🇺🇸 **English Version (WIRING_SCHEMATIC.md)**](WIRING_SCHEMATIC.md)

---

## Português

Este documento detalha o mapeamento de pinos, o design da **Placa Shield Hub (em placa perfurada 5x7cm)** com os conectores do **Conjunto 1 (Linha MODU / Dupont 2.54mm)**, a interface I2C com o acelerômetro **MPU-6050 (GY-521)** nos pinos **A4/A5**, a alimentação via **Canal 6 (CH6)** do receptor e o barramento de **GND Comum (Equilíbrio de Neutro)**.

---

### 🔌 1. Diagrama Geral de Blocos do Sistema

```mermaid
flowchart TD
    subgraph RECEPTOR["📡 Receptor FlySky FS-BS6 (Alimentado pelo ESC)"]
        RX_CH6_VCC["CH6 - VCC (+5V/6V Pino Central)"]
        RX_CH6_GND["CH6 - GND (Pino Inferior)"]
        RX_CH1["CH1 - Sinal Volante (Pino Superior)"]
        RX_CH2["CH2 - Sinal Throttle/Freio (Pino Superior)"]
        RX_CH4["CH4 - Sinal Chave Farol (Pino Superior)"]
    end

    subgraph MPU["🧭 Acelerômetro Inercial 3D MPU-6050 (GY-521)"]
        MPU_VCC["VCC (+5V)"]
        MPU_GND["GND (Terra)"]
        MPU_SDA["SDA (Dados I2C)"]
        MPU_SCL["SCL (Clock I2C)"]
    end

    subgraph SHIELD["🟢 Placa Hub / Shield (Placa Perfurada 5x7cm)"]
        direction TB
        GND_BUS["⚡ BARRAMENTO DE GND COMUM (Equilíbrio de Neutro)"]
        
        subgraph ARDUINO["🔵 Arduino Nano"]
            NANO_5V["Pino 5V (Alimentação)"]
            A4["A4 (I2C SDA)"]
            A5["A5 (I2C SCL)"]
            D2["D2 (INT0)"]
            D3["D3 (INT1)"]
            D4["D4 (PCINT20)"]
            D5["D5 (PWM)"]
            D6["D6 (PWM)"]
            D7["D7"]
            D8["D8"]
            D9["D9 (PWM)"]
            D10["D10"]
            D11["D11"]
            NANO_GND["Pino GND"]
        end

        subgraph RESISTORES["📦 Resistores Limitadores na Placa"]
            R_FAROL["R1: 100Ω"]
            R_PISCA_FE["R2: 150Ω"]
            R_PISCA_FD["R3: 150Ω"]
            R_LANTERNA["R4: 150Ω"]
            R_FREIO["R5: 150Ω"]
            R_PISCA_TE["R6: 150Ω"]
            R_PISCA_TD["R7: 150Ω"]
        end

        subgraph CONECTORES_PLACA["🔌 Barras de Pinos Macho (180°)"]
            CON_RADIO["CON1: RÁDIO & ALIMENTAÇÃO (1x5 Pinos)"]
            CON_FRENTE["CON2: DIANTEIRO (1x4 Pinos)"]
            CON_TRAS["CON3: TRASEIRO (1x6 Pinos)"]
            CON_MPU["CON4: MPU-6050 I2C (1x4 Pinos)"]
        end
    end

    subgraph CHICOTES["🚗 Chicotes da Carroceria / Bolha (Alojamentos MODU Fêmea)"]
        CHICOTE_DIANT["Chicote Frente (4 Vias)\n[GND + Faróis + Piscas FE/FD]"]
        CHICOTE_TRAS["Chicote Trás (6 Vias)\n[GND + Lanternas + Freio + Piscas TE/TD]"]
    end

    %% Alimentação e Sinais vindos do Receptor
    RX_CH6_GND -->|"Fio Preto (GND)"| CON_RADIO
    RX_CH6_VCC -->|"Fio Vermelho (+5V)"| CON_RADIO
    RX_CH1     -->|"Fio Branco (Sinal)"| CON_RADIO
    RX_CH2     -->|"Fio Amarelo (Sinal)"| CON_RADIO
    RX_CH4     -->|"Fio Verde (Sinal)"| CON_RADIO

    %% Roteamento interno do CON1
    CON_RADIO --> NANO_5V
    CON_RADIO --> NANO_GND
    CON_RADIO --> D4
    CON_RADIO --> D2
    CON_RADIO --> D3

    %% Conexões MPU-6050
    CON_MPU <--> MPU
    CON_MPU --> NANO_5V
    CON_MPU --> GND_BUS
    CON_MPU --> A4
    CON_MPU --> A5

    %% GND Comum
    NANO_GND --- GND_BUS
    GND_BUS --- CON_RADIO
    GND_BUS --- CON_FRENTE
    GND_BUS --- CON_TRAS
    GND_BUS --- CON_MPU

    %% Saídas para Resistores
    D9  --> R_FAROL      --> CON_FRENTE
    D10 --> R_PISCA_FE   --> CON_FRENTE
    D11 --> R_PISCA_FD   --> CON_FRENTE

    D5  --> R_LANTERNA   --> CON_TRAS
    D6  --> R_FREIO      --> CON_TRAS
    D7  --> R_PISCA_TE   --> CON_TRAS
    D8  --> R_PISCA_TD   --> CON_TRAS

    %% Saídas para Bolha
    CON_FRENTE <==|Engate Rápido 4P|==> CHICOTE_DIANT
    CON_TRAS   <==|Engate Rápido 6P|==> CHICOTE_TRAS
```

---

### 🗺️ 2. Layout Físico da Placa Hub / Shield (Placa Perfurada 5x7cm) — v8.0 Distribuído

```
┌────────────────────────────────────────────────────────────────────────┐
│               PLACA HUB SHIELD DE ILUMINAÇÃO (5x7 cm) - v8.0           │
│                                                                        │
│                      ┌─── [PORTA USB NANO] ───┐                        │
│                      │                        │                        │
│                      │  ARDUINO NANO V3 (DIP) │                        │
│                      │                        │                        │
│             (Col 6)  │                        │  (Col 12)              │
│       [D1/TX]  (o)   │                        │   (o)  [VIN]           │
│       [D0/RX]  (o)   │                        │   (o)  [GND] ──┐       │
│ ┌─────[RST]    (o)   │                        │   (o)  [RST]   │       │
│ │ ┌───[GND] ──┐(o)   │                        │   (o)  [5V] ───┼─┐     │
│┌┴─┴─────────┐ │      │                        │   (o)  [A7]    │ │     │
││ CON1: RÁDIO│ │      │                        │   (o)  [A6]    │ │ [C1]│
││(1x5 em 90° │ │      │                        │   (o)  [A5/SCL]┼─┼──┐│ │
││Lateral Esq)│ │      │                        │   (o)  [A4/SDA]┼─┼─┐││ │
││            │ │      │                        │   (o)  [A3]    │ │ │││ │
││[1: +5V] ◄──┼─┘      │                        │   (o)  [A2]    │ │ │││ │
││[2: GND] ◄──┼─(Lin 6)┤ (Trilhas de 10mm!)     │   (o)  [A1] ┌──┴─┴─┴┴┴┐│
││[3: CH2] ◄──┼─[D2]───┤                        │             │  │CON4: MPU ││
││[4: CH4] ◄──┼─[D3]───┤                        │             │  │(1x4 90°  ││
││[5: CH1] ◄──┼─[D4]───┤                        │             │  │Lat. Dir) ││
│└┬───────────┘ │      │                        │             │  │          ││
│ │             │ [D5] (o)════════════════════════════════════╗  │[1: GND]◄─┘│
│ ▼             │ [D6] (o)════════════════════════════════╗   ║  │[2: +5V]◄──│
│(Pinos 90°     │ [D7] (o)════════════════════════════╗   ║   ║  │[3: SCL]◄──┤
│ para a esq.)  │ [D8] (o)════════════════════════╗   ║   ║   ║  │[4: SDA]◄──┘
│               │ [D9] (o)─────┐                  ║   ║   ║   ║  └┬─────────┘
│               │ [D10](o)──┐  │                  ║   ║   ║   ║   │
│               │ [D11](o)─┐│  │                  ║   ║   ║   ║   ▼
│               └──────────┴┴──┴──────────────────╫───╫───╫───╫───(Pinos 90° dir)
│                          ││  │                  ║   ║   ║   ║
│                 [R1]   [R2] [R3]                [R7][R6][R5][R4]
│                 100Ω   150Ω 150Ω                150Ω 150Ω 150Ω 150Ω
│                (Farol)(P.FE)(P.FD)             (PTD)(PTE)(Fre)(Lan)
│                  │      │    │                    │   │   │   │
│                  ▼      ▼    ▼                    ▼   ▼   ▼   ▼
│         ┌───────────────────────┐        ┌────────────────────────┐
│         │ CON2: FRENTE (1x4 90°)│        │ CON3: TRÁS (1x6 90°)   │
│         │┌─────┬───────┬──────┬─┴─┐      │┌───┬───┬───┬───┬───┬──┐│
│         ││ GND │ Farol │Pis.FE│P.FD│      ││PTD│PTE│Fre│Lan│NC │GND│
│         │└──┬──┴───┬───┴──┬───┴───┘      │└─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬┘│
│         └───┼──────┼──────┼────────┘     └──┼───┼───┼───┼───┼───┼┘
│             │      │      │                 │   │   │   │   │   │
│             │      ▼      ▼                 ▼   ▼   ▼   ▼   │   │
│             │    (Pinos 90° apontam para fora da borda inferior)│
│             │                                                   │
│             └══════ (GND via Col 01)       (GND via Col 13) ════╝
└────────────────────────────────────────────────────────────────────────┘
```

---

### 📍 3. Pinagem dos Conectores (Conjunto 1 - Linha MODU)

#### 📡 CON1: Conector do Receptor de Rádio e Alimentação (1x5 Pinos 90° — Lateral Esquerda)
*Posicionado na **Lateral Esquerda** (Coluna 02, Linhas 05 a 09), face a face com os pinos D2, D3, D4 e GND do Nano. Trilhas ultracurtas de 10mm!*

| Pino | Identificação | Ligação no Shield | Ligação no Receptor FS-BS6 | Cor do Fio |
| :---: | :---: | :--- | :--- | :---: |
| **1** | **VCC (+5V)** | Linha 02 no Topo $\rightarrow$ **Nano 5V** (Col 12, Lin 06), C1(+) e CON4 P2 | **CH6 — Linha Central (Pino VCC +5V/6V)** | 🟥 Vermelho |
| **2** | **GND** | **Nano GND** (Col 06, Lin 06) [10mm] e Margem Col 01 (GND Dianteiro) | **CH6 — Linha Inferior (Pino GND)** | ⬛ Preto |
| **3** | **CH2 (Sinal)** | **Nano D2** (Col 06, Lin 07) [10mm] | **CH2 — Linha Superior (Sinal Throttle)** | 🟨 Amarelo |
| **4** | **CH4 (Sinal)** | **Nano D3** (Col 06, Lin 08) [10mm] | **CH4 — Linha Superior (Sinal Chave Farol)**| 🟩 Verde |
| **5** | **CH1 (Sinal)** | **Nano D4** (Col 06, Lin 09) [10mm] | **CH1 — Linha Superior (Sinal Volante)** | ⬜ Branco |

---

#### 🧭 CON4: Conector do Acelerômetro MPU-6050 (1x4 Pinos 90° — Lateral Direita)
*Posicionado na **Lateral Direita** (Coluna 17, Linhas 07 a 10), face a face com os pinos I2C e alimentação do Nano. Trilhas ultracurtas de 10mm!*

| Pino | Identificação | Ligação no Shield | Ligação no MPU-6050 | Cor do Fio |
| :---: | :---: | :--- | :--- | :---: |
| **1** | **GND** | Nano GND (Col 12, Lin 04) e C1 (-) (Col 14, Lin 06) | Pino GND do MPU-6050 | ⬛ Preto |
| **2** | **VCC (+5V)** | Nano 5V (Col 12, Lin 06) e C1 (+) (Col 15, Lin 06) | Pino VCC do MPU-6050 | 🟥 Vermelho |
| **3** | **SCL** | Nano A5 (Col 12, Lin 09) [10mm] | Pino SCL do MPU-6050 | 🟨 Amarelo |
| **4** | **SDA** | Nano A4 (Col 12, Lin 10) [10mm] | Pino SDA do MPU-6050 | 🟩 Verde |

---

#### 💡 CON2: Conector do Chicote Dianteiro (1x4 Pinos 90° — Borda Inferior Esquerda)
*Posicionado na **Linha 24, Colunas 03 a 06** com pinos em 90° apontando para baixo.*

| Pino | Função | Componente na Placa | Destino na Bolha | Cor do Fio |
| :---: | :--- | :--- | :--- | :---: |
| **1** | **GND** | Barramento GND Perimetral (Col 01) | Negativo comum dos LEDs dianteiros | ⬛ Preto |
| **2** | **Farol Dianteiro** | Pino D9 $\rightarrow$ Resistor R1 ($100\Omega$, Col 04) | Ânodo (+) dos LEDs Brancos de Farol | ⬜ Branco |
| **3** | **Pisca Diant. Esq.** | Pino D10 $\rightarrow$ Resistor R2 ($150\Omega$, Col 05) | Ânodo (+) do LED Laranja Esquerdo | 🟧 Laranja |
| **4** | **Pisca Diant. Dir.** | Pino D11 $\rightarrow$ Resistor R3 ($150\Omega$, Col 06) | Ânodo (+) do LED Laranja Direito | 🟦 Azul |

---

#### 💡 CON3: Conector do Chicote Traseiro (1x6 Pinos 90° — Borda Inferior Centro-Direita)
*Posicionado na **Linha 24, Colunas 08 a 13** com pinos em 90° apontando para baixo. Trilhas em L aninhadas com ZERO cruzamentos!*

| Pino | Função | Componente na Placa | Destino na Bolha | Cor do Fio |
| :---: | :--- | :--- | :--- | :---: |
| **1** | **Pisca Tras. Dir.** | Pino D8 $\rightarrow$ Resistor R7 ($150\Omega$, Col 08) | Ânodo (+) do LED Laranja Traseiro Dir. | 🟦 Azul |
| **2** | **Pisca Tras. Esq.** | Pino D7 $\rightarrow$ Resistor R6 ($150\Omega$, Col 09) | Ânodo (+) do LED Laranja Traseiro Esq. | 🟧 Laranja |
| **3** | **Luz de Freio** | Pino D6 $\rightarrow$ Resistor R5 ($150\Omega$, Col 10) | Ânodo (+) dos LEDs de Freio Vermelhos | 🟥 Vermelho |
| **4** | **Lanternas** | Pino D5 $\rightarrow$ Resistor R4 ($150\Omega$, Col 11) | Ânodo (+) das Lanternas Vermelhas | 🟫 Marrom |
| **5** | **Reserva / Guia** | Desconectado (NC, Col 12) | Pino cego / Guia mecânica / Expansão | ⚪ Cinza / Livre |
| **6** | **GND Comum** | Barramento GND Direto (Col 13) | Negativo comum dos LEDs traseiros | ⬛ Preto |

---

### 📦 4. Dimensionamento de Resistores (Todos na Placa)

| Resistor | Canal | LEDs Conectados | Valor | Posição na Placa | Potência |
| :---: | :---: | :--- | :---: | :---: | :---: |
| **R1** | D9 | 2x LEDs Farol Branco | **$100\Omega$** | Coluna 04 (Linhas 18 a 21) | 1/4W |
| **R2** | D10 | 1x LED Pisca Diant. Esquerdo | **$150\Omega$** | Coluna 05 (Linhas 18 a 21) | 1/4W |
| **R3** | D11 | 1x LED Pisca Diant. Direito | **$150\Omega$** | Coluna 06 (Linhas 18 a 21) | 1/4W |
| **R7** | D8 | 1x LED Pisca Tras. Direito | **$150\Omega$** | Coluna 08 (Linhas 18 a 21) | 1/4W |
| **R6** | D7 | 1x LED Pisca Tras. Esquerdo | **$150\Omega$** | Coluna 09 (Linhas 18 a 21) | 1/4W |
| **R5** | D6 | 2x LEDs Luz de Freio Vermelha | **$150\Omega$** | Coluna 10 (Linhas 18 a 21) | 1/4W |
| **R4** | D5 | 2x LEDs Lanterna Vermelha | **$150\Omega$** | Coluna 11 (Linhas 18 a 21) | 1/4W |

---

## English

This document provides the full pinout and physical shield board design (5x7cm perfboard) utilizing **Set 1 (MODU / Dupont 2.54mm)** connectors. The Arduino is directly powered through **Channel 6 (CH6)** of the FlySky FS-BS6 receiver (VCC + GND), featuring full common ground reference, MPU-6050 I2C bus on pins A4 (SDA) and A5 (SCL), and quick-disconnect harness connectors.
