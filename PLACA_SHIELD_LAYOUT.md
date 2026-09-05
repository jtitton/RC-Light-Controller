# Projeto de Engenharia da Placa Shield Hub (5x7 cm) — Layout Natural Distribuído v7.2

[🇧🇷 **Versão em Português**](#-português) | [🇺🇸 **English Version (SHIELD_BOARD_LAYOUT.md)**](SHIELD_BOARD_LAYOUT.md) | [📜 **Premissas Oficiais (PREMISSAS_PROJETO.md)**](PREMISSAS_PROJETO.md)

---

## 🇧🇷 Português

Este documento detalha o projeto de montagem da **Placa Shield Hub** utilizando **placa universal perfurada de 5x7 cm (Passo padrão de 2.54mm / 0.1")** com a arquitetura **Layout Natural Distribuído (v7.2)**:
- **Arduino Nano** posicionado na parte superior com a **porta USB voltada para fora (borda superior, Linhas 01-02)** e **pinagem física real** (Left Header: D13 no topo até VIN na base; Right Header: D12 no topo até D1/TX na base).
- **CON1 (Rádio FS-BS6 1x5 em 90°)** na **Lateral Direita** (Coluna 17, Linhas 11 a 15) — **Entrada Principal de VCC (+5V) e GND Mestre**! Trilhas horizontais retas de **apenas 10 mm** para D4 (CH1), D3 (CH4), D2 (CH2) e GND.
- **Capacitor de Filtro / Regulação C1 ($100\mu\text{F} \times 16\text{V}$)** montado **diretamente na entrada** (Coluna 15, Linhas 14 e 15), soldado lado a lado com os pinos 1 (+5V) e 2 (GND) de CON1 e GND do Nano.
- **CON4 (MPU-6050 1x4 em 90°)** na **Lateral Esquerda** (Coluna 02, Linhas 10 a 13) — trilhas diretas de **apenas 10 mm** para A4 (SDA), A5 (SCL), +5V e GND!
- **CON2 (Chicote Dianteiro 1x4 em 90°)** na **Borda Inferior Esquerda** (Linha 24, Colunas 03 a 06).
- **CON3 (Chicote Traseiro 1x6 em 90°)** na **Borda Inferior Centro-Direita** (Linha 24, Colunas 08 a 13).
- **Barramento GND Mestre 100% Unificado:** Malha contínua conectando CON1 P2, C1(-), Nano GND Dir, Nano GND Esq, CON2, CON3 e CON4.
- **Roteamento Híbrido Otimizado:** Trilhas estanhadas sem sobreposição + 4 fios isolados superiores (jumpers) para garantir ZERO curtos-circuitos com integridade geométrica absoluta (Farol D9, Pisca D10, +5V Nano e GND Cross-Tie).

> [!IMPORTANT]
> ### ⚡ PREMISSAS FUNDAMENTAIS DO PROJETO:
> 1. **Origem da Energia:** VCC (+5V) e GND vêm exclusivamente do Chicote do Rádio (**CON1 via CH6 / BEC do ESC**). Nenhum outro conector alimenta a placa.
> 2. **Tensão Nominal:** O circuito foi projetado para BEC nominal de **5.0V**. Caso utilize BEC de 6.0V ou superior, instale um diodo 1N4007 em série no pino +5V de CON1 para derrubar ~0.7V antes do Nano 5V.
> 3. **Regulação na Entrada:** O capacitor **C1 ($100\mu\text{F}$)** fica soldado imediatamente junto aos pinos 1 e 2 de CON1 (Coluna 15), absorvendo ruídos de motor e servos logo na entrada.
> 4. **Barramento GND Mestre:** O GND de CON1 P2 é a referência zero absoluta, interligando todos os conectores em uma malha contínua na placa (independente do Nano estar inserido).
> 5. **Fios Isolados Superiores (Jumpers):** Devido à pinagem física real do Nano (LEDs D9-D11 na lateral direita e resistores R1-R3 na lateral esquerda), 4 conexões utilizam pequenos fios isolados com capa na face superior para saltar sobre componentes sem compartilhar pads de cobre no verso.
> *Consulte o documento canônico [PREMISSAS_PROJETO.md](PREMISSAS_PROJETO.md) para detalhes completos de engenharia.*

> [!TIP]
> ### 🌟 MODELOS GRÁFICOS DISPONÍVEIS (ALTA DEFINIÇÃO & INTERATIVO):
> - 🌐 **[Abrir Visualizador Interativo da Placa (HTML)](placa_shield_visualizador.html)** — **Recomendado!** Visualize em tela cheia no navegador com zoom, alternância instantânea entre **Vista Superior (Componentes)**, **Vista Inferior (Solda / Trilhas no Verso)** e **Raio-X**, com **fiação conectada visível em todas as vistas** e destaque dinâmico de circuitos.
> - 🖼️ **[Diagrama Vetorial da Face Superior (SVG)](placa_shield_superior.svg)** — Vista superior mostrando o Arduino Nano, C1 na entrada, resistores e trilhas de fiação conectadas.
> - 🔄 **[Diagrama Vetorial da Face Inferior / Solda (SVG)](placa_shield_inferior.svg)** — Vista espelhada do verso da placa (como você vê ao soldar) com trilhas de solda reforçadas e barramento de GND unificado.
> - 📸 **[Renderização 3D Realista da Placa (JPG)](placa_shield_3d.jpg)** — Visualização tridimensional da montagem física na bancada.

---

### 📐 1. Matriz de Coordenadas da Placa (18 Colunas x 24 Linhas) — Layout Distribuído v7.2

```
       01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18  (Colunas)
 01 [  ╔═════════════════[+5V TOPO LINHA 01]═══════════════╗  ] 01 ◄── Trilha +5V Perimetral
 02 [  ║   .  .  .  . ┌───[USB NANO]───┐ .  .  .  .  .  .  ║  ] 02
 03 [  ║   .  .  .  . │[D13]          [D12]│.  │  .  .  .  ║  ] 03
 04 [  ║   .  .  .  . │[3V3]     ╔════[D11]│.  │  .  .  .  ║  ] 04 ◄── D11 (Pisca FD via Col 07)
 05 [  ║   .  .  .  . │[REF]     ║    [D10]│.  │  .  .  .  ║  ] 05 ◄── D10 ➔ Jumper direto para R2 Top
 06 [  ║   .  .  .  . │[A0]      ║    [D9] │.  │  .  .  .  ║  ] 06 ◄── D9  ➔ Jumper direto para R1 Top
 07 [  ║   .  .  .  . │[A1]      ║    [D8] │═══╬═══╗  .  . ║  ] 07 ◄── D8 (Pisca TD)
 08 [  ║   .  .  .  . │[A2]      ║    [D7] │═══╬═══╬═══╗ . ║  ] 08 ◄── D7 (Pisca TE)
 09 [  ║   .  .  .  . │[A3]      ║    [D6] │═══╬═══╬═══╬══ ║  ] 09 ◄── D6 (Luz Freio)
 10 [  ║ .[SDA]───────│[A4]      ║    [D5] │═══╬═══╬═══╬══ ║  ] 10 ◄── D5 (Lanterna) & CON4 SDA
 11 [  ║ .[SCL]───────│[A5]      ║    [D4] │───╫───╫───╫── ║  ] 11 ◄── CON1 P5 (CH1) & CON4 SCL
 12 [  ╠═.[+5V]       │[A6]      ║    [D3] │───╫───╫───╫── ║  ] 12 ◄── CON1 P4 (CH4) & Ramal CON4 +5V
 13 [  . .[GND]───┐   │[A7]      ║    [D2] │───╫───╫───╫── ║  ] 13 ◄── CON1 P3 (CH2) & CON4 GND
 14 [ [Jmp5V]·····│···│[5V]      ║    [GND]│───╫───╫─[C1-][GND] ] 14 ◄── CON1 P2 (GND), C1(-), Nano GND
 15 [  .  CON4    │   │[RST]     ║    [RST]│   ║   ║ [C1+][+5V]═╝ ] 15 ◄── CON1 P1 (+5V) ➔ Sobe Col 18
 16 [  ╔══(GND)───┴───│[GND]·····║····(Jmp)│   ║   ║   │  CON1  ] 16 ◄── Jumper GND Cross-Tie (12,14➔06,16)
 17 [  ║  (90°)       │[VIN]     ║    [TX] │   ║   ║   │  (90°) ] 17
 18 [  ║              │          ▼    [R7][R6][R5][R4] │        ] 18 ◄── TOPOS DOS RESISTORES
 19 [  ║             [R1] [R2]  [R3]   │   │   │   │   │        ] 19
 20 [  ║              │    │     │     │   │   │   │   │        ] 20
 21 [  ║             [┴]  [┴]   [┴]   [┴] [┴] [┴] [┴]  │        ] 21 ◄── BASES DOS RESISTORES
 22 [  ║              │    │     │     │   │   │   │   │        ] 22
 23 [  ║              │    │     │     │   │   │   │   │        ] 23
 24 [  ╚══════════════╡    │     │     │   │   │   │   │  [GND] ] 24 ◄── CON2 (Cols 03-06) & CON3 (08-13)
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
│         [D13]  (o)   │                        │   (o)  [D12]           │
│         [3V3]  (o)   │                        │   (o)  [D11/P.FD]══╗   │
│         [REF]  (o)   │                        │   (o)  [D10/P.FE]··╫·┐ │ (Jumper D10)
│         [A0]   (o)   │                        │   (o)  [D9/Farol]··╫─┼┐│ (Jumper D9)
│         [A1]   (o)   │                        │   (o)  [D8/PTD]    ║ │││
│         [A2]   (o)   │                        │   (o)  [D7/PTE]    ║ │││
│         [A3]   (o)   │                        │   (o)  [D6/Freio]  ║ │││
│   ┌─────[A4/SDA](o)  │                        │   (o)  [D5/Lant]   ║ │││
│  ┌┼─────[A5/SCL](o)  │                        │   (o)  [D4/CH1]──┐ ║ │││
│  ││     [A6]   (o)   │                        │   (o)  [D3/CH4]─┐│ ║ │││
│  ││     [A7]   (o)   │                        │   (o)  [D2/CH2]┐││ ║ │││
│  ││ ┌···[5V]   (o)   │                        │   (o)  [GND]───┼┼┼─╫─┼┼┤ [CON1 P2]
│  ││ │ ┌─[GND]  (o)···┼························┼···(o)  (JmpGND)│││ ║ ││││
│  ││ │ │ [VIN]  (o)   │                        │   (o)  [TX]    │││ ║ ││││
│┌─┴┴─┴─┴─────┐        │                        │                │││ ║ ││││
││CON4: MPU   │        │                        │               ┌┴┴┴─┴─┴┴┤
││(1x4 em 90° │        │                        │               │CON1:   │
││Lateral Esq)│        │                        │               │RÁDIO   │
││[4: SDA]◄───┘        │                        │               │(1x5 90°│
││[3: SCL]◄───┘        │                        │      [CH1 :5]◄┼────────┘
││[2: +5V]◄──┐         │                        │      [CH4 :4]◄┼───────┘
││[1: GND]◄──┼┐        └────────────────────────┘      [CH2 :3]◄┼──────┘
│└┬──────────┼┴─────────┐       ║  ║  ║                [GND :2]◄┼─C1(-)
│ ▼ (Pinos 90°          │       ║  ║  ║                [+5V :1]◄┼─C1(+) ➔ Col 18
│ para a esq.)          │       ║  ║  ║                └┬───────┘
│                       │       ║  ║  ║                 ▼ (Pinos 90° dir.)
│                       │       ║  ║  ║
│                 [R1]  ▼ [R2]  ▼[R3] ▼[R7][R6][R5][R4]
│                 100Ω    150Ω   150Ω  150Ω 150Ω 150Ω 150Ω
│                (Farol) (P.FE) (P.FD) (PTD)(PTE)(Fre)(Lan)
│                  │       │      │      │   │   │   │
│                  ▼       ▼      ▼      ▼   ▼   ▼   ▼
│         ┌───────────────────────┐   ┌────────────────────────┐
│         │ CON2: FRENTE (1x4 90°)│   │ CON3: TRÁS (1x6 90°)   │
│         │┌─────┬───────┬──────┬─┴─┐ │┌───┬───┬───┬───┬───┬──┐│
│         ││ GND │ Farol │Pis.FE│P.FD│││PTD│PTE│Fre│Lan│NC │GND│
│         │└──┬──┴───┬───┴──┬───┴───┘ │└─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬┘│
│         └───┼──────┼──────┼─────────┘└──┼───┼───┼───┼───┼───┼──┘
│             │      │      │             │   │   │   │   │   │
│             │      ▼      ▼             ▼   ▼   ▼   ▼   │   │
│             │    (Pinos 90° apontam para fora da borda) │   │
│             │                                               │
│             └══════ (GND via Col 01)   (GND via Col 13) ════╝
└────────────────────────────────────────────────────────────────────────┘
```

---

### 🔌 3. Roteamento das Trilhas (Face Inferior de Cobre & Fios Superiores)

O **Layout Natural Distribuído v7.2** elimina 100% dos curtos-circuitos através de **trilhas perimetrais dedicadas** e **4 fios isolados superiores (jumpers)**:

#### 📻 A. Canal do Rádio & Filtragem de Entrada (Lateral Direita — Trilhas de 10mm!)
O conector CON1 fica na **Coluna 17 (Linhas 11 a 15)**, face a face com os pinos de controle do Nano e o capacitor C1:
* **CON1 Pino 5 (CH1 Volante, Col 17, Lin 11):** Trilha horizontal reta até **Nano D4** (Col 12, Lin 11) $\rightarrow$ **10 mm de solda!**
* **CON1 Pino 4 (CH4 Farol, Col 17, Lin 12):** Trilha horizontal reta até **Nano D3** (Col 12, Lin 12) $\rightarrow$ **10 mm de solda!**
* **CON1 Pino 3 (CH2 Throttle, Col 17, Lin 13):** Trilha horizontal reta até **Nano D2** (Col 12, Lin 13) $\rightarrow$ **10 mm de solda!**
* **CON1 Pino 2 (GND Mestre, Col 17, Lin 14):** Liga imediatamente a **C1(-)** (Col 15, Lin 14) e ao **Nano GND** direito (Col 12, Lin 14) $\rightarrow$ **Nó Central de Terra!**
* **CON1 Pino 1 (+5V BEC Entrada Mestre, Col 17, Lin 15):** Liga a **C1(+)** (Col 15, Lin 15), contorna pela margem livre **Coluna 18** até a Linha 01 no topo, cruza até a **Coluna 01** na margem esquerda e desce até a Linha 14:
  - Ramal em (Col 01, Lin 12) $\rightarrow$ **CON4 Pino 2 (+5V MPU)**.
  - Ponto de Jumper em (Col 01, Lin 14) $\rightarrow$ **Fio isolado superior (13mm)** saltando até **Nano +5V** (Col 06, Lin 14).

#### 🧭 B. Canal do MPU-6050 (Lateral Esquerda — Trilhas de 10mm!)
O conector CON4 fica na **Coluna 02 (Linhas 10 a 13)**, face a face com os pinos I2C e alimentação:
* **CON4 Pino 4 (SDA, Col 02, Lin 10):** Trilha horizontal reta até **Nano A4** (Col 06, Lin 10) $\rightarrow$ **10 mm de solda!**
* **CON4 Pino 3 (SCL, Col 02, Lin 11):** Trilha horizontal reta até **Nano A5** (Col 06, Lin 11) $\rightarrow$ **10 mm de solda!**
* **CON4 Pino 2 (+5V, Col 02, Lin 12):** Conectado diretamente ao ramal da linha +5V mestre perimetral (Col 01 $\rightarrow$ Col 02).
* **CON4 Pino 1 (GND, Col 02, Lin 13):** Soldado na linha de terra esquerda unida a **Nano GND esquerdo** (Col 06, Lin 16).

#### 💡 C. Canal dos LEDs Dianteiros (Jumpers Diretos & Canal Central)
* **D9 (Farol):** Fio isolado superior (jumper ~36mm) direto de **Nano D9** (Col 12, Lin 06) até **R1 Top** (Col 04, Lin 18) $\rightarrow$ no verso, trilha reta de **R1 Bot** (Col 04, Lin 21) até **CON2 Pino 2** (Farol).
* **D10 (Pisca FE):** Fio isolado superior (jumper ~38mm) direto de **Nano D10** (Col 12, Lin 05) até **R2 Top** (Col 05, Lin 18) $\rightarrow$ no verso, trilha reta de **R2 Bot** (Col 05, Lin 21) até **CON2 Pino 3** (Pis.FE).
* **D11 (Pisca FD):** Trilha no verso saindo de **Nano D11** (Col 12, Lin 04) pelo canal central livre da **Coluna 07** até Linha 17 $\rightarrow$ entra em **R3 Top** (Col 06, Lin 18) $\rightarrow$ **R3 Bot** (Col 06, Lin 21) $\rightarrow$ **CON2 Pino 4** (Pis.FD).
* **CON2 Pino 1 (GND, Col 03, Lin 24):** Alimentado pela **Coluna 01** na margem perimetral externa.

#### 💡 D. Canal dos LEDs Traseiros (Trilhas em "L" Aninhadas — Zero Cruzamentos!)
As 4 saídas traseiras utilizam roteamento planar aninhado no verso da placa:
* **D8 (Pisca TD, Lin 07):** Nano D8 (Col 12, Lin 07) corre na Lin 07 até **Col 08** $\rightarrow$ desce até **R7 Top** (Col 08, Lin 18) $\rightarrow$ **R7 Bot** (Col 08, Lin 21) $\rightarrow$ **CON3 Pino 1** (Pisca TD).
* **D7 (Pisca TE, Lin 08):** Nano D7 (Col 12, Lin 08) corre na Lin 08 até **Col 09** $\rightarrow$ desce até **R6 Top** (Col 09, Lin 18) $\rightarrow$ **R6 Bot** (Col 09, Lin 21) $\rightarrow$ **CON3 Pino 2** (Pisca TE).
* **D6 (Freio, Lin 09):** Nano D6 (Col 12, Lin 09) corre na Lin 09 até **Col 10** $\rightarrow$ desce até **R5 Top** (Col 10, Lin 18) $\rightarrow$ **R5 Bot** (Col 10, Lin 21) $\rightarrow$ **CON3 Pino 3** (Freio).
* **D5 (Lanterna, Lin 10):** Nano D5 (Col 12, Lin 10) corre na Lin 10 até **Col 11** $\rightarrow$ desce até **R4 Top** (Col 11, Lin 18) $\rightarrow$ **R4 Bot** (Col 11, Lin 21) $\rightarrow$ **CON3 Pino 4** (Lanterna).
* **CON3 Pino 5 (NC, Col 12, Lin 24):** Livre / Reserva mecânica.
* **CON3 Pino 6 (GND, Col 13, Lin 24):** Alimentado diretamente pelo canal desimpedido da Coluna 13.

---

### 📋 3.1 Tabela Mestra de Soldagem Furo a Furo (Guia de Bancada)

| Passo | Circuito / Sinal | Ponto de Origem (De) | Ponto de Destino (Para) | Tipo de Conexão Física |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **🔴 Linha +5V Perimetral** | **CON1 Pino 1** (Col 17, Lin 15) | **C1(+)** (Col 15, Lin 15) $\rightarrow$ Col 18 $\rightarrow$ Topo Lin 01 $\rightarrow$ Margem Col 01 $\rightarrow$ Lin 14 | Trilha de solda perimetral contornando a placa |
| **1b**| **🔴 Ramal +5V MPU** | **Margem Col 01** (Col 01, Lin 12) | **CON4 Pino 2** (Col 02, Lin 12) | Trilha horizontal direta de 1 pad |
| **1c**| **⚡ Jumper +5V Nano** | **Margem Col 01** (Col 01, Lin 14) | **Nano +5V** (Col 06, Lin 14) | **Fio isolado superior (Jumper 13mm)** saltando sobre a placa |
| **2** | **⚡ GND Mestre Entrada** | **CON1 Pino 2** (Col 17, Lin 14) | **C1(-)** (Col 15, Lin 14) e **Nano GND Dir** (Col 12, Lin 14) | Trilha horizontal reta (Linha 14) |
| **2b**| **⚡ Jumper GND Cross-Tie**| **Nano GND Dir** (Col 12, Lin 14) | **Nano GND Esq** (Col 06, Lin 16) | **Fio isolado superior (Jumper 16mm)** unindo os barramentos |
| **3** | **📻 Rádio CH2** | **CON1 Pino 3** (Col 17, Lin 13) | **Nano D2** (Col 12, Lin 13) | Trilha horizontal direta de 10mm (Linha 13) |
| **4** | **📻 Rádio CH4** | **CON1 Pino 4** (Col 17, Lin 12) | **Nano D3** (Col 12, Lin 12) | Trilha horizontal direta de 10mm (Linha 12) |
| **5** | **📻 Rádio CH1** | **CON1 Pino 5** (Col 17, Lin 11) | **Nano D4** (Col 12, Lin 11) | Trilha horizontal direta de 10mm (Linha 11) |
| **6** | **🧭 MPU SDA** | **CON4 Pino 4** (Col 02, Lin 10) | **Nano A4** (Col 06, Lin 10) | Trilha horizontal direta de 10mm (Linha 10) |
| **7** | **🧭 MPU SCL** | **CON4 Pino 3** (Col 02, Lin 11) | **Nano A5** (Col 06, Lin 11) | Trilha horizontal direta de 10mm (Linha 11) |
| **8** | **⚡ GND Esquerdo & MPU**| **Nano GND Esq** (Col 06, Lin 16) | Lin 16 até Col 02 $\rightarrow$ sobe Col 02 até **CON4 P1** (Col 02, Lin 13) | Trilha estanhada no verso |
| **9** | **⚡ GND Frente (CON2)** | **Ponto (Col 02, Lin 16)** | Coluna 01 na margem externa até **CON2 P1** (Col 03, Lin 24) | Trilha perimetral desimpedida |
| **10**| **⚡ GND Traseiro (CON3)**| **Nano GND Dir** (Col 12, Lin 14) | Desce reto pela Coluna 13 até **CON3 P6** (Col 13, Lin 24) | Trilha vertical desimpedida |
| **11**| **💡 Farol (D9)** | **Nano D9** (Col 12, Lin 06) | **R1 Top** (Col 04, Lin 18) | **Fio isolado superior (Jumper ~36mm)** |
| **11b**|**💡 Saída Farol** | **R1 Bot** (Col 04, Lin 21) | **CON2 P2** (Col 04, Lin 24) | Trilha vertical reta no verso |
| **12**| **💡 Pisca FE (D10)** | **Nano D10** (Col 12, Lin 05) | **R2 Top** (Col 05, Lin 18) | **Fio isolado superior (Jumper ~38mm)** |
| **12b**|**💡 Saída Pisca FE** | **R2 Bot** (Col 05, Lin 21) | **CON2 P3** (Col 05, Lin 24) | Trilha vertical reta no verso |
| **13**| **💡 Pisca FD (D11)** | **Nano D11** (Col 12, Lin 04) | Lin 04 até Col 07 $\rightarrow$ desce Col 07 até **R3 Top** (Col 06, Lin 18) | Trilha em L no verso |
| **13b**|**💡 Saída Pisca FD** | **R3 Bot** (Col 06, Lin 21) | **CON2 P4** (Col 06, Lin 24) | Trilha vertical reta no verso |
| **14**| **💡 Pisca TD (D8)** | **Nano D8** (Col 12, Lin 07) | Lin 07 até Col 08 $\rightarrow$ **R7 Top** (Col 08, Lin 18) $\rightarrow$ **R7 Bot** $\rightarrow$ **CON3 P1** | Trilha em L aninhada |
| **15**| **💡 Pisca TE (D7)** | **Nano D7** (Col 12, Lin 08) | Lin 08 até Col 09 $\rightarrow$ **R6 Top** (Col 09, Lin 18) $\rightarrow$ **R6 Bot** $\rightarrow$ **CON3 P2** | Trilha em L aninhada |
| **16**| **💡 Freio (D6)** | **Nano D6** (Col 12, Lin 09) | Lin 09 até Col 10 $\rightarrow$ **R5 Top** (Col 10, Lin 18) $\rightarrow$ **R5 Bot** $\rightarrow$ **CON3 P3** | Trilha em L aninhada |
| **17**| **💡 Lanterna (D5)** | **Nano D5** (Col 12, Lin 10) | Lin 10 até Col 11 $\rightarrow$ **R4 Top** (Col 11, Lin 18) $\rightarrow$ **R4 Bot** $\rightarrow$ **CON3 P4** | Trilha em L aninhada |

---

### 📋 4. Lista Completa de Componentes da Placa Shield

| Identificador | Componente | Descrição / Valor | Função e Localização |
| :---: | :--- | :--- | :--- |
| **U1** | Soquete Arduino Nano | 2x Barras Fêmea 1x15 (Passo 2.54mm) | Colunas 06 e 12 (Linhas 03 a 17) |
| **U2** | MPU-6050 (GY-521) | Módulo sensor inercial 3D I2C | Fixado no chassi via chicote CON4 |
| **C1** | Capacitor Eletrolítico | **$100\mu\text{F} \times 16\text{V}$** | **Coluna 15 (Linhas 14 e 15)**, na entrada de alimentação de CON1 |
| **R1** | Resistor 1/4W | **$100\Omega$** (Marrom, Preto, Marrom, Ouro) | Limitador Farol (D9) — Col 04 (Linhas 18 a 21) |
| **R2** | Resistor 1/4W | **$150\Omega$** (Marrom, Verde, Marrom, Ouro) | Limitador Pisca Diant. Esq. (D10) — Col 05 (Linhas 18 a 21) |
| **R3** | Resistor 1/4W | **$150\Omega$** (Marrom, Verde, Marrom, Ouro) | Limitador Pisca Diant. Dir. (D11) — Col 06 (Linhas 18 a 21) |
| **R7** | Resistor 1/4W | **$150\Omega$** (Marrom, Verde, Marrom, Ouro) | Limitador Pisca Tras. Dir. (D8) — Col 08 (Linhas 18 a 21) |
| **R6** | Resistor 1/4W | **$150\Omega$** (Marrom, Verde, Marrom, Ouro) | Limitador Pisca Tras. Esq. (D7) — Col 09 (Linhas 18 a 21) |
| **R5** | Resistor 1/4W | **$150\Omega$** (Marrom, Verde, Marrom, Ouro) | Limitador Luz de Freio (D6) — Col 10 (Linhas 18 a 21) |
| **R4** | Resistor 1/4W | **$150\Omega$** (Marrom, Verde, Marrom, Ouro) | Limitador Lanterna Traseira (D5) — Col 11 (Linhas 18 a 21) |
| **CON1** | Barra de Pinos 90° | **1x5 Pinos Macho 90°** | **Lateral Direita** (Col 17, Linhas 11 a 15) — Entrada Rádio FS-BS6 |
| **CON4** | Barra de Pinos 90° | **1x4 Pinos Macho 90°** | **Lateral Esquerda** (Col 02, Linhas 10 a 13) — MPU-6050 I2C |
| **CON2** | Barra de Pinos 90° | **1x4 Pinos Macho 90°** | **Borda Inferior Esquerda** (Linha 24, Cols 03 a 06) — Frente |
| **CON3** | Barra de Pinos 90° | **1x6 Pinos Macho 90°** | **Borda Inferior Centro-Dir** (Linha 24, Cols 08 a 13) — Trás |
| **W1-W4**| Fios Jumpers Isolados | **4x Fios flexíveis com capa (28-30 AWG)** | Face superior: D9 (~36mm), D10 (~38mm), +5V (~13mm) e GND (~16mm) |

---

## English

Please refer to [SHIELD_BOARD_LAYOUT.md](SHIELD_BOARD_LAYOUT.md) for the complete English documentation, coordinates grid, and distributed component layout.
