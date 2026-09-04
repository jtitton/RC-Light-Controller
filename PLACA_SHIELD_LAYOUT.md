# Projeto de Engenharia da Placa Shield Hub (5x7 cm) — Layout Natural Distribuído v8.0

[🇧🇷 **Versão em Português**](#-português) | [🇺🇸 **English Version (SHIELD_BOARD_LAYOUT.md)**](SHIELD_BOARD_LAYOUT.md)

---

## 🇧🇷 Português

Este documento detalha o projeto de montagem da **Placa Shield Hub** utilizando **placa universal perfurada de 5x7 cm (Passo padrão de 2.54mm / 0.1")** com a arquitetura **Layout Natural Distribuído (v8.0)**:
- **Arduino Nano** posicionado na parte superior com a **porta USB voltada para fora (borda de cima)**.
- **CON1 (Rádio FS-BS6 1x5 em 90°)** na **Lateral Esquerda** (Coluna 02, Linhas 06 a 10) — trilhas diretas de **apenas 10 mm** para D2, D3, D4 e GND!
- **CON4 (MPU-6050 1x4 em 90°)** na **Lateral Direita** (Coluna 17, Linhas 07 a 10) — trilhas diretas de **apenas 10 mm** para A4, A5, 5V e GND!
- **Filtro capacitivo C1 ($100\mu\text{F} \times 16\text{V}$)** na lateral direita (Colunas 14 e 15, Linha 06), colado ao pino 5V e GND do Nano.
- **CON2 (Chicote Dianteiro 1x4 em 90°)** na **Borda Inferior Esquerda** (Linha 24, Colunas 03 a 06).
- **CON3 (Chicote Traseiro 1x6 em 90°)** na **Borda Inferior Centro-Direita** (Linha 24, Colunas 08 a 13).
- **100% Planar:** **ZERO fios jumpers cruzando outros circuitos!**

> [!TIP]
> ### 🌟 MODELOS GRÁFICOS DISPONÍVEIS (ALTA DEFINIÇÃO & INTERATIVO):
> - 🌐 **[Abrir Visualizador Interativo da Placa (HTML)](placa_shield_visualizador.html)** — **Recomendado!** Visualize em tela cheia no navegador com zoom, alternância instantânea entre **Vista Superior (Componentes)**, **Vista Inferior (Solda / Trilhas no Verso)** e **Raio-X**, além de destaque dinâmico de circuitos (GND, 5V, Farol, Piscas, Freio, MPU-6050, Rádio) e inspetor de coordenadas no mouse.
> - 🖼️ **[Diagrama Vetorial da Face Superior (SVG)](placa_shield_superior.svg)** — Vista superior limpa com o Arduino Nano, código de cores real dos resistores e conectores em 90°.
> - 🔄 **[Diagrama Vetorial da Face Inferior / Solda (SVG)](placa_shield_inferior.svg)** — Vista espelhada do verso da placa (como você vê ao soldar) com as trilhas de solda, barramento de GND reforçado e zero cruzamentos.
> - 📸 **[Renderização 3D Realista da Placa (JPG)](placa_shield_3d.jpg)** — Visualização tridimensional da montagem física na bancada.

---

### 📐 1. Matriz de Coordenadas da Placa (18 Colunas x 24 Linhas) — Layout Distribuído v8.0

```
       01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18  (Colunas)
 01 [  .  .  .  .  . ┌──────────────────┐ .  .  .  .  .  .  ] 01 ◄── BORDA SUPERIOR
 02 [  . [════════════════+5V TOPO═════════════] .  .  .  .  ] 02 ◄── Trilha +5V Direta
 03 [  .  .  .  .  . │[D1]          [VIN]│.  .  .  .  .  .  ] 03
 04 [  .  .  .  .  . │[D0]          [GND]│.  .  .  .  .  .  ] 04 ◄── Nano GND Dir
 05 [  .[+5V] .  .  .│[RST]         [RST]│.  .  .  .  .  .  ] 05 ◄── CON1 P1 (+5V BEC)
 06 [  .[GND] .  .  .│[GND]          [5V]│. [C1: 100uF] .  ] 06 ◄── CON1 P2 (GND) e C1
 07 [  .[CH2] .  .  .│[D2]           [A7]│.  .  .  .  .[GND].] 07 ◄── CON1 P3 (CH2) e CON4 P1
 08 [  .[CH4] .  .  .│[D3]           [A6]│.  .  .  .  .[+5V].] 08 ◄── CON1 P4 (CH4) e CON4 P2
 09 [  .[CH1] .  .  .│[D4]           [A5]│.  .  .  .  .[SCL].] 09 ◄── CON1 P5 (CH1) e CON4 P3
 10 [  .  ▲   .  .  .│[D5]═══════════════╗.  .  .  .  .[SDA].] 10 ◄── D5 (Lanterna) e CON4 P4
 11 [  .  │   .  .  .│[D6]═══════════╗   ║.  .  .  .  .  ▲  .] 11 ◄── D6 (Freio)
 12 [  . CON1: RÁDIO │[D7]═══════╗   ║   ║.  .  .  .  CON4  .] 12 ◄── D7 (Pisca TE)
 13 [  . (1x5 90° Esq│[D8]═══╗   ║   ║   ║.  .  .  .   MPU  .] 13 ◄── D8 (Pisca TD)
 14 [  .  .   .  ╔═══│[D9]   ║   ║   ║   ║.  .  .  . (1x4 90°] 14 ◄── D9 (Farol)
 15 [  .  .   .  ║ ╔═│[D10]  ║   ║   ║   ║.  .  .  .   Dir) .] 15 ◄── D10 (Pisca FE)
 16 [  .  .   .  ║ ║ │[D11]  ║   ║   ║   ║.  .  .  .  .  .  .] 16 ◄── D11 (Pisca FD)
 17 [  .  .   .  ║ ║ │[D12]  ║   ║   ║   ║.  .  .  .  .  .  .] 17
 18 [  .  .  . [R1][R2][R3] . [R7][R6][R5][R4] .  .  .  .  .] 18 ◄── TOPOS DOS RESISTORES
 19 [  .  .  .  │   │   │   .  │   │   │   │  .  .  .  .  .  ] 19
 20 [  .  .  .  │   │   │   .  │   │   │   │  .  .  .  .  .  ] 20
 21 [  .  .  . [┴] [┴] [┴]  . [┴] [┴] [┴] [┴] .  .  .  .  .  ] 21 ◄── BASES DOS RESISTORES
 22 [  .  .  .  │   │   │   .  │   │   │   │  .  .  .  .  .  ] 22
 23 [  .  .  .  │   │   │   .  │   │   │   │  .  .  .  .  .  ] 23
 24 [  .  . ┌──CON2: FRENTE─┐ ┌──CON3: TRÁS (1x6 90°)──┐ .  ] 24
    [  .  . │[GND][Far][P.E][P.D]│[P.D][P.E][Fre][Lan][NC][GND]│  ] 24
    [  .  . └──▲──────────────┘ └───────────────────────▲──┘ .  ] 24
               │ (GND via Col 01)        (GND via Col 13)│
```

---

### 🗺️ 2. Mapa Visual Superior (Face dos Componentes - Visto de Cima)

```
┌────────────────────────────────────────────────────────────────────────┐
│                        BORDA SUPERIOR DA PLACA                         │
│                                                                        │
│                      ┌─── [PORTA USB NANO] ───┐                        │
│                      │                        │                        │
│                      │  ARDUINO NANO V3 (DIP) │                        │
│                      │ (Encaixado em 2 barras │                        │
│                      │   fêmeas de 1x15 pinos)│                        │
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

### 🔌 3. Roteamento das Trilhas (Face Inferior de Cobre - Soldagem)

O **Layout Natural Distribuído v8.0** elimina 100% dos cruzamentos através de **trilhas em "L" aninhadas** e canais perimetrais dedicados:

#### 📻 A. Canal do Rádio (Lateral Esquerda — Trilhas Ultracurtas de 10mm!)
O conector CON1 fica na **Coluna 02 (Linhas 05 a 09)**, face a face com os pinos do Nano:
* **CON1 Pino 1 (+5V BEC, Col 02, Lin 05):** Sobe livre para a Linha 02 e corre reto no topo desimpedido até o Nano 5V (Col 12, Lin 06).
* **CON1 Pino 2 (GND, Col 02, Lin 06):** Soldado direto em linha reta no **Nano GND** esquerdo (Col 06, Lin 06) $\rightarrow$ **10 mm de solda!**
* **CON1 Pino 3 (CH2 Throttle, Col 02, Lin 07):** Trilha horizontal reta até **Nano D2** (Col 06, Lin 07) $\rightarrow$ **10 mm de solda!**
* **CON1 Pino 4 (CH4 Farol, Col 02, Lin 08):** Trilha horizontal reta até **Nano D3** (Col 06, Lin 08) $\rightarrow$ **10 mm de solda!**
* **CON1 Pino 5 (CH1 Volante, Col 02, Lin 09):** Trilha horizontal reta até **Nano D4** (Col 06, Lin 09) $\rightarrow$ **10 mm de solda!**
* **Cruzamentos:** **ZERO! Conexões 100% paralelas.**

#### 🧭 B. Canal do MPU-6050 & Filtro C1 (Lateral Direita — Trilhas Ultracurtas de 10mm!)
O conector CON4 fica na **Coluna 17 (Linhas 07 a 10)**, face a face com os pinos I2C e alimentação:
* **CON4 Pino 1 (GND, Col 17, Lin 07):** Soldado no terminal (-) de C1 (Col 14, Lin 06) e no Nano GND direito (Col 12, Lin 04).
* **CON4 Pino 2 (+5V, Col 17, Lin 08):** Soldado no terminal (+) de C1 (Col 15, Lin 06) e no Nano 5V (Col 12, Lin 06).
* **CON4 Pino 3 (SCL, Col 17, Lin 09):** Trilha horizontal reta até **Nano A5** (Col 12, Lin 09) $\rightarrow$ **10 mm de solda!**
* **CON4 Pino 4 (SDA, Col 17, Lin 10):** Trilha horizontal reta até **Nano A4** (Col 12, Lin 10) $\rightarrow$ **10 mm de solda!**
* **Cruzamentos:** **ZERO! Conexões 100% paralelas.**

#### 💡 C. Canal dos LEDs Dianteiros (Borda Inferior Esquerda — Linha 24, Colunas 03 a 06)
* **D9 (Farol):** Nano D9 (Col 06, Lin 14) $\rightarrow$ corre na Linha 14 até Col 04 $\rightarrow$ **R1 Top** (Col 04, Lin 18) $\rightarrow$ **R1 Bot** (Col 04, Lin 21) $\rightarrow$ **CON2 Pino 2** (Farol).
* **D10 (Pisca FE):** Nano D10 (Col 06, Lin 15) $\rightarrow$ corre na Linha 15 até Col 05 $\rightarrow$ **R2 Top** (Col 05, Lin 18) $\rightarrow$ **R2 Bot** (Col 05, Lin 21) $\rightarrow$ **CON2 Pino 3** (Pis.FE).
* **D11 (Pisca FD):** Nano D11 (Col 06, Lin 16) $\rightarrow$ desce direto pela Col 06 $\rightarrow$ **R3 Top** (Col 06, Lin 18) $\rightarrow$ **R3 Bot** (Col 06, Lin 21) $\rightarrow$ **CON2 Pino 4** (Pis.FD).
* **CON2 Pino 1 (GND, Col 03, Lin 24):** Alimentado pela Coluna 01 na margem externa.

#### 💡 D. Canal dos LEDs Traseiros (Trilhas em "L" Aninhadas — Zero Cruzamentos!)
Para eliminar 100% dos cruzamentos, as 4 saídas traseiras utilizam roteamento planar aninhado:
* **D8 (Pisca TD, Lin 13):** Corre na Lin 13 até **Col 08** $\rightarrow$ desce até **R7 Top** (Col 08, Lin 18) $\rightarrow$ **R7 Bot** (Col 08, Lin 21) $\rightarrow$ **CON3 Pino 1** (Pisca TD).
* **D7 (Pisca TE, Lin 12):** Corre na Lin 12 até **Col 09** $\rightarrow$ desce até **R6 Top** (Col 09, Lin 18) $\rightarrow$ **R6 Bot** (Col 09, Lin 21) $\rightarrow$ **CON3 Pino 2** (Pisca TE).
* **D6 (Freio, Lin 11):** Corre na Lin 11 até **Col 10** $\rightarrow$ desce até **R5 Top** (Col 10, Lin 18) $\rightarrow$ **R5 Bot** (Col 10, Lin 21) $\rightarrow$ **CON3 Pino 3** (Freio).
* **D5 (Lanterna, Lin 10):** Corre na Lin 10 até **Col 11** $\rightarrow$ desce até **R4 Top** (Col 11, Lin 18) $\rightarrow$ **R4 Bot** (Col 11, Lin 21) $\rightarrow$ **CON3 Pino 4** (Lanterna).
* **CON3 Pino 5 (NC, Col 12, Lin 24):** Livre / Reserva.
* **CON3 Pino 6 (GND, Col 13, Lin 24):** Alimentado diretamente pelo canal desimpedido da Coluna 13.

---

### 📋 3.1 Tabela Mestra de Soldagem Furo a Furo (Guia de Bancada)

| Passo | Circuito / Sinal | Ponto de Origem (De) | Ponto de Destino (Para) | Tipo de Conexão Física |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **🔴 Linha +5V** | **CON1 Pino 1** (Col 02, Lin 05) | Sobe até Lin 02 $\rightarrow$ corre no topo até **Nano 5V** (Col 12, Lin 06), **C1(+)** (Col 15) e **CON4 P2** (Col 17) | Trilha direta pelo topo livre (Linha 02) |
| **2** | **⚡ GND Rádio** | **Nano GND** (Col 06, Lin 06) | **CON1 P2** (Col 02, Lin 06) | Trilha horizontal reta de 10mm (Linha 06) |
| **3** | **📻 Rádio CH2** | **CON1 Pino 3** (Col 02, Lin 07) | **Nano D2** (Col 06, Lin 07) | Trilha horizontal direta de 10mm (Linha 07) |
| **4** | **📻 Rádio CH4** | **CON1 Pino 4** (Col 02, Lin 08) | **Nano D3** (Col 06, Lin 08) | Trilha horizontal direta de 10mm (Linha 08) |
| **5** | **📻 Rádio CH1** | **CON1 Pino 5** (Col 02, Lin 09) | **Nano D4** (Col 06, Lin 09) | Trilha horizontal direta de 10mm (Linha 09) |
| **6** | **🧭 MPU SCL** | **CON4 Pino 3** (Col 17, Lin 09) | **Nano A5** (Col 12, Lin 09) | Trilha horizontal direta de 10mm (Linha 09) |
| **7** | **🧭 MPU SDA** | **CON4 Pino 4** (Col 17, Lin 10) | **Nano A4** (Col 12, Lin 10) | Trilha horizontal direta de 10mm (Linha 10) |
| **8** | **⚡ GND MPU & C1** | **Nano GND** (Col 12, Lin 04) | **C1(-)** (Col 14, Lin 06) e **CON4 P1** (Col 17, Lin 07) | Trilha contínua de solda |
| **9** | **⚡ GND Frente** | **CON1 P2 GND** (Col 02, Lin 06) | Coluna 01 na margem externa até **CON2 P1** (Col 03, Lin 24) | Trilha perimetral desimpedida |
| **10**| **⚡ GND Traseiro**| **Nano GND** (Col 12, Lin 04) | Desce reto pela Coluna 13 até **CON3 P6** (Col 13, Lin 24) | Trilha vertical desimpedida |
| **11**| **💡 Farol** | **Nano D9** (Col 06, Lin 14) | **R1 Top** (Col 04, Lin 18) $\rightarrow$ **R1 Bot** (Col 04, Lin 21) $\rightarrow$ **CON2 P2** (Col 04, Lin 24) | Trilha em L e vertical |
| **12**| **💡 Pisca FE** | **Nano D10** (Col 06, Lin 15) | **R2 Top** (Col 05, Lin 18) $\rightarrow$ **R2 Bot** (Col 05, Lin 21) $\rightarrow$ **CON2 P3** (Col 05, Lin 24) | Trilha em L e vertical |
| **13**| **💡 Pisca FD** | **Nano D11** (Col 06, Lin 16) | **R3 Top** (Col 06, Lin 18) $\rightarrow$ **R3 Bot** (Col 06, Lin 21) $\rightarrow$ **CON2 P4** (Col 06, Lin 24) | Trilha direta vertical |
| **14**| **💡 Pisca TD** | **Nano D8** (Col 06, Lin 13) | **R7 Top** (Col 08, Lin 18) $\rightarrow$ **R7 Bot** (Col 08, Lin 21) $\rightarrow$ **CON3 P1** (Col 08, Lin 24) | Trilha em L aninhada |
| **15**| **💡 Pisca TE** | **Nano D7** (Col 06, Lin 12) | **R6 Top** (Col 09, Lin 18) $\rightarrow$ **R6 Bot** (Col 09, Lin 21) $\rightarrow$ **CON3 P2** (Col 09, Lin 24) | Trilha em L aninhada |
| **16**| **💡 Freio** | **Nano D6** (Col 06, Lin 11) | **R5 Top** (Col 10, Lin 18) $\rightarrow$ **R5 Bot** (Col 10, Lin 21) $\rightarrow$ **CON3 P3** (Col 10, Lin 24) | Trilha em L aninhada |
| **17**| **💡 Lanterna** | **Nano D5** (Col 06, Lin 10) | **R4 Top** (Col 11, Lin 18) $\rightarrow$ **R4 Bot** (Col 11, Lin 21) $\rightarrow$ **CON3 P4** (Col 11, Lin 24) | Trilha em L aninhada |

---

### 📋 4. Lista Completa de Componentes da Placa Shield

| Identificador | Componente | Descrição / Valor | Função e Localização |
| :---: | :--- | :--- | :--- |
| **U1** | Soquete Arduino Nano | 2x Barras Fêmea 1x15 (Passo 2.54mm) | Colunas 06 e 12 (Linhas 03 a 17) |
| **U2** | MPU-6050 (GY-521) | Módulo sensor inercial 3D I2C | Fixado no chassi via chicote CON4 |
| **C1** | Capacitor Eletrolítico | **$100\mu\text{F} \times 16\text{V}$** | Colunas 14 e 15 (Linha 06), colado ao 5V e GND |
| **R1** | Resistor 1/4W | **$100\Omega$** (Marrom, Preto, Marrom, Ouro) | Limitador Farol (D9) — Col 04 (Linhas 18 a 21) |
| **R2** | Resistor 1/4W | **$150\Omega$** (Marrom, Verde, Marrom, Ouro) | Limitador Pisca Diant. Esq. (D10) — Col 05 (Linhas 18 a 21) |
| **R3** | Resistor 1/4W | **$150\Omega$** (Marrom, Verde, Marrom, Ouro) | Limitador Pisca Diant. Dir. (D11) — Col 06 (Linhas 18 a 21) |
| **R7** | Resistor 1/4W | **$150\Omega$** (Marrom, Verde, Marrom, Ouro) | Limitador Pisca Tras. Dir. (D8) — Col 08 (Linhas 18 a 21) |
| **R6** | Resistor 1/4W | **$150\Omega$** (Marrom, Verde, Marrom, Ouro) | Limitador Pisca Tras. Esq. (D7) — Col 09 (Linhas 18 a 21) |
| **R5** | Resistor 1/4W | **$150\Omega$** (Marrom, Verde, Marrom, Ouro) | Limitador Luz de Freio (D6) — Col 10 (Linhas 18 a 21) |
| **R4** | Resistor 1/4W | **$150\Omega$** (Marrom, Verde, Marrom, Ouro) | Limitador Lanterna Traseira (D5) — Col 11 (Linhas 18 a 21) |
| **CON1** | Barra de Pinos 90° | **1x5 Pinos Macho 90°** | **Lateral Esquerda** (Col 02, Linhas 05 a 09) — Rádio FS-BS6 |
| **CON4** | Barra de Pinos 90° | **1x4 Pinos Macho 90°** | **Lateral Direita** (Col 17, Linhas 07 a 10) — MPU-6050 I2C |
| **CON2** | Barra de Pinos 90° | **1x4 Pinos Macho 90°** | **Borda Inferior Esquerda** (Linha 24, Cols 03 a 06) — Frente |
| **CON3** | Barra de Pinos 90° | **1x6 Pinos Macho 90°** | **Borda Inferior Centro-Dir** (Linha 24, Cols 08 a 13) — Trás |

---

## English

Please refer to [SHIELD_BOARD_LAYOUT.md](SHIELD_BOARD_LAYOUT.md) for the complete English documentation, coordinates grid, and distributed component layout.
