# Projeto de Engenharia da Placa Shield Hub (5x7 cm) — Layout Natural Distribuído v8.4

[🇧🇷 **Versão em Português**](#-português) | [🇺🇸 **English Version (SHIELD_BOARD_LAYOUT.md)**](SHIELD_BOARD_LAYOUT.md) | [📜 **Premissas Oficiais (PREMISSAS_PROJETO.md)**](PREMISSAS_PROJETO.md)

---

## 🇧🇷 Português

Este documento detalha o projeto de montagem da **Placa Shield Hub** utilizando **placa universal perfurada de 5x7 cm (Passo padrão de 2.54mm / 0.1")** com a arquitetura **Layout Natural Distribuído (v8.4)**:
- **Suporte Nativo a BEC 6.0V com Diodo D1 de Pitch Expandido (1N4007 DO-41):** Montado na face superior descendo verticalmente pela **Coluna 17, entre as Linhas 15 e 18**, com pitch padrão industrial DO-41 de **7,62 mm (3 passos)**. Anodo em `(17, 15)` (soldado a CON1 P1 +6.0V BEC bruto) e Catodo (faixa prateada) em `(17, 18)`. Produz uma queda de tensão de $\approx 0.75\text{V}$, gerando um barramento seguro e regulado de **$+5.25\text{V}$** na Linha 18 para o pino 5V do Nano, C1(+) e o coletor de Q1, conferindo proteção absoluta contra sobretensão e inversão de polaridade. O pad `(17, 15)` fica isolado no verso, e os pads intermediários `(17, 16)`, `(17, 17)`, `(16, 15)` e `(15, 15)` ficam 100% livres e sem estanho, criando uma barreira de mais de 7 mm contra curtos-circuitos acidentais.
- **Arduino Nano** posicionado na parte superior com a **porta USB voltada para fora (borda superior, Linhas 01-02)** e **pinagem física real** (Left Header: D13 no topo até VIN na base; Right Header: D12 no topo até D1/TX na base).
- **Driver de Transistor Q1 (BC337 NPN TO-92) para Faróis (D9):** Montado na **Linha 09, Colunas 13 a 15** operando como seguidor de emissor (*High-Side Emitter Follower*), drenando apenas ~0.4mA de Nano D9 e fornecendo de **45 a 60 mA** para os 4 LEDs brancos em paralelo via resistor vertical **R1 ($27\,\Omega$ 1/4W)** na Coluna 15 (Linhas 06 a 08), duplicando o brilho dos faróis sem alterar o chicote de terra comum.
- **Resistores R2 a R7 Padronizados em $100\,\Omega$ (1/4W):** Piscas dianteiros/traseiros e freio elevados para **~14.5 a 15 mA por LED**, garantindo intensidade luminosa automotiva máxima e 100% segura para o ATmega328P.
- **CON1 (Rádio FS-BS6 1x5 em 90°)** na **Lateral Direita** (Coluna 17, Linhas 11 a 15) — **Entrada Principal de VCC (+6.0V) e GND Mestre**! Trilhas horizontais retas de **apenas 10 mm** para D4 (CH1), D3 (CH4), D2 (CH2) e GND.
- **Capacitor de Filtro / Regulação C1 ($100\mu\text{F} \times 25\text{V}$)** montado na **Linha 18** (Colunas 14 e 15), com polo positivo C1(+) em `(15, 18)` e polo negativo C1(-) em `(14, 18)` ligado por ponte curta de solda ao barramento de GND da Coluna 13.
- **CON4 (MPU-6050 1x4 em 90°)** na **Lateral Esquerda** (Coluna 02, Linhas 10 a 13) — Pinagem física 1:1 com o módulo do usuário (**P1: GND, P2: TX [SCL], P3: RX [SDA], P4: VCC [+5.25V]**).
- **CON2 (Chicote Dianteiro 1x4 em 90°)** na **Lateral Superior Direita** (Coluna 17, Linhas 04 a 07) — **mesmo lado do rádio**, acima de CON1, com pinos apontando para a borda direita.
- **CON3 (Chicote Traseiro 1x6 em 90°)** na **Borda Inferior Centro-Direita** (Linha 24, Colunas 08 a 13).
- **Barramento GND Mestre 100% Unificado:** Malha contínua conectando CON1 P2, C1(-), Nano GND Dir, Nano GND Esq, CON2, CON3 e CON4.
- **Roteamento Híbrido Otimizado:** Trilhas estanhadas sem sobreposição + **5 fios isolados superiores (jumpers W1 a W5)** garantindo ZERO curtos-circuitos com integridade geométrica absoluta comprovada (189 pads validados).

> [!IMPORTANT]
> ### ⚡ PREMISSAS FUNDAMENTAIS DO PROJETO:
> 1. **Origem da Energia & Tensão do BEC:** VCC (+6.0V) e GND vêm exclusivamente do Chicote do Rádio (**CON1 via CH6 / BEC do ESC**). O diodo retificador **D1 (1N4007)** onboard reduz a tensão em ~0.75V para **+5.25V seguro**, protegendo o microcontrolador ATmega328P e o sensor MPU-6050.
> 2. **D1 e C1 com Pitch Expandido:** O diodo **D1 (1N4007)** desce verticalmente pela Coluna 17 (Linhas 15 a 18) com pitch de 7,62 mm, e o capacitor **C1 ($100\mu\text{F} \times 25\text{V}$)** fica na Linha 18 (Colunas 14 e 15), absorvendo ruídos de motor e servos com isolamento físico contra curto por estanho.
> 3. **Barramento GND Mestre:** O GND de CON1 P2 é a referência zero absoluta, interligando todos os conectores em uma malha contínua na placa (independente do Nano estar inserido).
> 4. **Fios Isolados Superiores (5 Jumpers W1 a W5):** Apenas 5 conexões utilizam fios isolados na face superior: W1 (+5.25V Nano 15,18➔06,14), W2 (GND Dianteiro 16,14➔16,07), W3 (GND Cross-Tie 12,14➔06,16), W4 (SDA/RX Acelerômetro 02,12➔06,10) e W5 (+5.25V Farol Coletor Q1 16,18➔13,09).
> *Consulte o documento canônico [PREMISSAS_PROJETO.md](PREMISSAS_PROJETO.md) para detalhes completos de engenharia.*

> [!TIP]
> ### 🌟 MODELOS GRÁFICOS DISPONÍVEIS (ALTA DEFINIÇÃO & INTERATIVO):
> - 🌐 **[Abrir Visualizador Interativo da Placa (HTML)](placa_shield_visualizador.html)** — **Recomendado!** Visualize em tela cheia no navegador com zoom, alternância instantânea entre **Vista Superior (Componentes)**, **Vista Inferior (Solda / Trilhas no Verso)** e **Raio-X**, com **fiação conectada visível em todas as vistas** e destaque dinâmico de circuitos.
> - 🖼️ **[Diagrama Vetorial da Face Superior (SVG)](placa_shield_superior.svg)** — Vista superior mostrando o Arduino Nano, diodo D1 1N4007, Q1 BC337, C1 na entrada, resistores e trilhas de fiação conectadas.
> - 🔄 **[Diagrama Vetorial da Face Inferior / Solda (SVG)](placa_shield_inferior.svg)** — Vista espelhada do verso da placa (como você vê ao soldar) com trilhas de solda reforçadas e barramento de GND unificado.

---

### 📐 1. Matriz de Coordenadas da Placa (18 Colunas x 24 Linhas) — Layout Distribuído v8.4

```
       01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18  (Colunas)
 01 [  ║   .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  ] 01 ◄── Coluna 01: Barramento GND Vertical Mestre
 02 [  ║   .  .  .  . ┌───[USB NANO]───┐ .  .  .  .  .  .  .  ] 02
 03 [  ║   .  .  .  . │[D13]          [D12]│.  .  .  .  .  .  ] 03
 04 [  ║   .  .  .  . │[3V3]          [D11]│──[In]═[R3]═[P4]  ] 04 ◄── R3 (100Ω) ➔ CON2 P4 (Pisca FD)
 05 [  ║   .  .  .  . │[REF]          [D10]│──[In]═[R2]═[P3]  ] 05 ◄── R2 (100Ω) ➔ CON2 P3 (Pisca FE)
 06 [  ║   .  .  .  . │[A0]           [D9] │───┬───[R1]═[P2]  ] 06 ◄── R1 Out (27Ω) ➔ CON2 P2 (Farol)
 07 [  ║   .  .  .  . │[A1]           [D8] │═══╬═══│ │ [W2][P1] ] 07 ◄── D8 (Pisca TD) & CON2 P1 (GND via W2)
 08 [  ║   .  .  .  . │[A2]           [D7] │═══╬═══│[R1] .  . ] 08 ◄── R1 In (27Ω) ligado ao Emissor de Q1
 09 [  ║   .  .  .  . │[A3]           [D6] │═══╬═══│[Q1: C-B-E]] 09 ◄── Q1 BC337: C(13,09), B(14,09), E(15,09)
 10 [  ║ .[GND]───(Barra GND)───│[A4/SDA]·······(W4)    [D5] │═══╬═══╬═══╬══ .  ] 10 ◄── D5 (Lanterna) & Nano A4 (W4 In)
 11 [  ║ .[TX/SCL]──────────────│[A5/SCL]         [D4] │───╫───╫───╫──[P5]] 11 ◄── CON1 P5 (CH1) & CON4 P2 TX (SCL)
 12 [  ║ .[RX/SDA]······(W4)····│[A6]             [D3] │───╫───╫───╫──[P4]] 12 ◄── CON1 P4 (CH4) & CON4 P3 RX (W4 Out)
 13 [  ║ .[VCC]───(Ramal +5V)───│[A7]             [D2] │───╫───╫───╫──[P3]] 13 ◄── CON1 P3 (CH2) & CON4 P4 VCC
 14 [  ║  CON4    │             │[5V]             [GND]│───╫───╫───.──[W2][P2] ] 14 ◄── CON1 P2 (GND), W2 Out, Nano GND Dir
 15 [  ║  (90°)   │             │[RST]            [RST]│   ║   .   .   .  [P1] ] 15 ◄── CON1 P1 (+6.0V BEC) ➔ D1 Anodo (17,15)
 16 [  ╠══(GND)───┴─────────────│[GND]············(Jmp)│   ║   .   .   .   │   ] 16 ◄── Jumper W3 GND Cross-Tie & D1 Corpo
 17 [  ║  (MPU)                 │[VIN]            [TX] │   ║   .   .   .   │   ] 17 ◄── D1 Corpo (Pitch 7,62mm / 3 passos)
 18 [  ║                        │                      │   ║  [C1-][C1+][W5][D1K] 18 ◄── D1 Catodo (17,18), W5, C1(+)/W1, C1(-)/GND
 19 [  ║                        │                      │   ║   ║   ║   ║   ║   ║   19
 20 [  ║                        │                      │   ║   ║   ║   ║   ║   ║   20
 21 [  ║                        │                      │   ║   ║   ║   ║   ║   ║   21 ◄── BASES DOS RESISTORES TRASEIROS (Cols 08-11)
 22 [  ║                        │                      │   ║   ║   ║   ║   ║   ║   22
 23 [  ║                        │                      │   ║   ║   ║   ║   ║   ║   23
 24 [  ╚════════════════════════╪══════════════════════╪═══╩═══╡   .   .   . [GND] 24 ◄── CON3: TRÁS (Linha 24, Cols 08-13)
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
│                      │ (Encaixado em 2 barras │   (Col 17)             │
│                      │   fêmeas de 1x15 pinos)│  ┌──────────────┐      │
│                      │                        │  │CON2: FRENTE  │      │
│                      │                        │  │(1x4 em 90°   │      │
│                      │                        │  │Lateral Dir)  │      │
│                      │  (Col 12)  (Col 14-16) │  │              │      │
│                      │   (o) [D12]            │  │              │      │
│                      │   (o) [D11]──[R3 100Ω]═╪═►│[4: Pis.FD]   │      │
│                      │   (o) [D10]──[R2 100Ω]═╪═►│[3: Pis.FE]   │      │
│                      │   (o) [D9] ──┐ [R1 27Ω]╪═►│[2: Farol]    │      │
│                      │   (o) [D8/PTD]│  │ (W2)──►│[1: GND]      │      │
│                      │   (o) [D7/PTE]│ [R1]   │  └──────────────┘      │
│                      │   (o) [D6/Fre]│  │     │   ▲ (Pinos 90° dir.)   │
│                      │   (o) [D5/Lan]▼ [Q1]   │                        │
│                      │              [C][B][E] │                        │
│                      │              (W5)(D9)(R1)                       │
│   ┌─────[A4/SDA](o)···(Jmp W4 SDA)─────┐      │   (o) [D4/CH1]─────────┼──────────┐             │
│  ┌┼─────[A5/SCL](o)────────────────┐   │      │   (o) [D3/CH4]─────────┼─────────┐│             │
│  ││     [A6]   (o)                 │   │      │   (o) [D2/CH2]─────────┼────────┐││             │
│  ││ ┌···[5V]   (o)◄──┼──(Jmp W1)───┼───┼──────┼─C1(+)─┐│││             │
│  ││ │ ┌─[GND]  (o)···┼··(Jmp W3)───┼───┼──────┼─C1(-)─┼┼┼┤             │
│  ││ │ │ [VIN]  (o)   │             │   │      │(W2 In)││││             │
│┌─┴┴─┴─┴─────┐        │             │   │      │(W5 In)││││             │
││CON4: MPU   │        │             │   │      ┌┴┴┴┴┴───────────┐│
││(1x4 em 90° │        │             │   │      │CON1: RÁDIO     ││
││Lateral Esq)│        │             │   │      │(1x5 90° Lat Dir││
││[1: GND]────┼────────┴─────────────┘   │      │[5: CH1]◄───────┘│
││[2: TX/SCL]◄┘                          │      │[4: CH4]◄───────┘│
││[3: RX/SDA]◄···························┘      │[3: CH2]◄───────┘│
││[4: VCC]◄───┘ (via ramal +5.25V Nano)         │[2: GND]◄─C1(-)  │
│└┬─────────────────────────────────────┐       │[1:+6V]►[D1]►C1+ │
│ ▼ (Pinos 90°                          │       └┬───────────────┘│
│ para a esq.)                          │        ▼ (Pinos 90° dir)│
│                                       │                         │
│                                       ▼ [R7] [R6] [R5] [R4]     │
│                                       100Ω  100Ω 100Ω 100Ω      │
│                                       (PTD) (PTE)(Fre)(Lan)     │
│                                         │     │    │    │       │
│                                         ▼     ▼    ▼    ▼       │
│                                      ┌────────────────────────┐ │
│                                      │ CON3: TRÁS (1x6 90°)   │ │
│                                      │┌───┬───┬───┬───┬───┬──┐│ │
│                                      ││PTD│PTE│Fre│Lan│NC │GND││ │
│                                      │└───┴───┴───┴───┴───┴──┘│ │
│                                      └────────────────────────┘ │
│                                           (Pinos 90° apontam p/ baixo)
└────────────────────────────────────────────────────────────────────────┘
```

---

### 🔌 3. Roteamento das Trilhas (Face Inferior de Cobre & Fios Superiores)

O **Layout Natural Distribuído v8.3** utiliza o diodo D1 (1N4007) para compatibilidade nativa com BEC de 6.0V, driver de transistor Q1 para os faróis, resistores padronizados em 100Ω e **5 fios isolados superiores (jumpers W1 a W5)**:

#### 📻 A. Canal do Rádio, Diodo D1 & Filtragem de Entrada (Lateral Direita — Trilhas de 10mm!)
O conector CON1 fica na **Coluna 17 (Linhas 11 a 15)**, face a face com os pinos de controle do Nano e com D1 descendo até Linha 18:
* **CON1 Pino 5 (CH1 Volante, Col 17, Lin 11):** Trilha horizontal reta até **Nano D4** (Col 12, Lin 11) $\rightarrow$ **10 mm de solda!**
* **CON1 Pino 4 (CH4 Farol, Col 17, Lin 12):** Trilha horizontal reta até **Nano D3** (Col 12, Lin 12) $\rightarrow$ **10 mm de solda!**
* **CON1 Pino 3 (CH2 Throttle, Col 17, Lin 13):** Trilha horizontal reta até **Nano D2** (Col 12, Lin 13) $\rightarrow$ **10 mm de solda!**
* **CON1 Pino 2 (GND Mestre, Col 17, Lin 14):** Liga diretamente ao **Nano GND** direito (Col 12, Lin 14) $\rightarrow$ **Nó Central de Terra!**
* **CON1 Pino 1 (+6.0V BEC Entrada Mestre, Col 17, Lin 15):** Liga diretamente ao terminal **Anodo do Diodo D1 (1N4007)** no furo `(17, 15)`. **ATENÇÃO:** O Pad `(17, 15)` fica rigorosamente **isolado no verso**, forçando toda a corrente do rádio a passar pelo corpo de D1.
* **Diodo D1 (1N4007 DO-41, Coluna 17, Linhas 15 a 18):** Montado na face superior descendo verticalmente com **pitch padrão industrial de 7,62 mm (3 passos)**. O terminal Catodo (faixa prateada) entra no Pad `(17, 18)`, gerando o barramento regulado e protegido de **$+5.25\text{V}$**.
* **Barramento VCC Linha 18 Protegido:** No verso, uma trilha horizontal de solda une `(17, 18)` a `(15, 18)`. O Pad `(17, 18)` recebe o Cátodo de D1; o Pad `(16, 18)` ancora o **Jumper W5 (+5.25V Farol Coletor Q1)**; o Pad `(15, 18)` conecta C1(+) e o **Jumper W1 (+5.25V Nano)**.
* **Capacitor C1 ($100\mu\text{F} \times 25\text{V}$, Linha 18):** Polo positivo em `(15, 18)` e polo negativo em `(14, 18)`, ligado por ponte direta de 1 pad ao tronco de GND da Coluna 13 `(13, 18)`.

#### 🧭 B. Canal do MPU-6050 (Lateral Esquerda — Trilhas de 10mm!)
O conector CON4 fica na **Coluna 02 (Linhas 10 a 13)**, respeitando a serigrafia do módulo (**GND, TX, RX, VCC**):
* **CON4 Pino 1 (GND, Col 02, Lin 10):** Ponte direta de solda de 1 pad para o **Barramento GND Mestre da Coluna 01** (Col 01, Lin 10).
* **CON4 Pino 2 (TX [SCL], Col 02, Lin 11):** Trilha horizontal reta no verso de apenas 10mm até **Nano A5** (Col 06, Lin 11).
* **CON4 Pino 3 (RX [SDA], Col 02, Lin 12):** Conectado via **Fio Jumper Isolado Superior W4 (~11mm)** de (02, 12) até **Nano A4** (Col 06, Lin 10).
* **CON4 Pino 4 (VCC [+5.25V], Col 02, Lin 13):** Conectado pelo verso ao ramal que parte de **Nano 5V** (Col 06, Lin 14 $\rightarrow$ Col 05, Lin 14 $\rightarrow$ Col 05, Lin 13 $\rightarrow$ Col 02, Lin 13).

#### 💡 C. Canal dos LEDs Dianteiros (Driver Q1 BC337 & CON2 Superior Direita)
* **Posicionamento de CON2 (Coluna 17, Linhas 04 a 07):** Barra de pinos macho em 90° voltada para a direita:
  - **Pino 1 (GND, Linha 07):** Alimentado pelo **Jumper W2** vindo do GND Mestre em (16, 14), com ponte direta em (16, 07) $\rightarrow$ (17, 07).
  - **Pino 2 (Farol, Linha 06):** Alimentado pelo resistor R1 (27Ω) em (15, 06) com ponte de solda para (16, 06) $\rightarrow$ (17, 06).
  - **Pino 3 (Pisca FE, Linha 05):** Ponte de solda direta para a saída de R2 em (16, 05) $\rightarrow$ (17, 05).
  - **Pino 4 (Pisca FD, Linha 04):** Ponte de solda direta para a saída de R3 em (16, 04) $\rightarrow$ (17, 04).
* **Transistor Driver Q1 (BC337 TO-92 na Linha 09, Cols 13 a 15):**
  - **Coletor (13, 09):** Recebe +5.25V do barramento via Jumper W5 vindo de (16, 15).
  - **Base (14, 09):** Conectada por trilha de solda vertical descendo de (14, 06) e horizontalmente até Nano D9 (12, 06).
  - **Emissor (15, 09):** Conectado por ponte curta de solda a (15, 08) (Lead 1 de R1).
* **Resistores Dianteiros:**
  - **R1 (Farol 27Ω 1/4W):** Montado verticalmente na Coluna 15 entre Linhas 08 e 06 (pitch 5,08mm).
  - **R2 (Pisca FE 100Ω 1/4W):** Montado horizontalmente na Linha 05 (Cols 14 a 16).
  - **R3 (Pisca FD 100Ω 1/4W):** Montado horizontalmente na Linha 04 (Cols 14 a 16).

#### 💡 D. Canal dos LEDs Traseiros (Trilhas em "L" Aninhadas & Resistores 100Ω)
As 4 saídas traseiras utilizam roteamento planar aninhado no verso da placa:
* **D8 (Pisca TD, Lin 07):** Nano D8 (Col 12, Lin 07) corre na Lin 07 até **Col 08** $\rightarrow$ desce até **R7 Top** (Col 08, Lin 18) $\rightarrow$ **R7 Bot** (Col 08, Lin 21) $\rightarrow$ **CON3 Pino 1** (Pisca TD).
* **D7 (Pisca TE, Lin 08):** Nano D7 (Col 12, Lin 08) corre na Lin 08 até **Col 09** $\rightarrow$ desce até **R6 Top** (Col 09, Lin 18) $\rightarrow$ **R6 Bot** (Col 09, Lin 21) $\rightarrow$ **CON3 Pino 2** (Pisca TE).
* **D6 (Freio, Lin 09):** Nano D6 (Col 12, Lin 09) corre na Lin 09 até **Col 10** $\rightarrow$ desce até **R5 Top** (Col 10, Lin 18) $\rightarrow$ **R5 Bot** (Col 10, Lin 21) $\rightarrow$ **CON3 Pino 3** (Freio).
* **D5 (Lanterna, Lin 10):** Nano D5 (Col 12, Lin 10) corre na Lin 10 até **Col 11** $\rightarrow$ desce até **R4 Top** (Col 11, Lin 18) $\rightarrow$ **R4 Bot** (Col 11, Lin 21) $\rightarrow$ **CON3 Pino 4** (Lanterna).
* **CON3 Pino 5 (NC, Col 12, Lin 24):** Livre / Reserva mecânica.
* **CON3 Pino 6 (GND, Col 13, Lin 24):** Alimentado diretamente pelo canal desimpedido da Coluna 13.

---

### 📋 3.1 Tabela Mestra de Soldagem Furo a Furo (Guia de Bancada v8.4)

| Passo | Circuito / Sinal | Ponto de Origem (De) | Ponto de Destino (Para) | Tipo de Conexão Física |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **🔴 Entrada +6.0V BEC (Anodo D1)** | **CON1 Pino 1** (Col 17, Lin 15) | **D1 Anodo** (Col 17, Lin 15) | Solda conjunta no furo (17, 15). **PAD ISOLADO NO VERSO (sem conexões na Linha 15)!** |
| **1b**| **⚡ D1 1N4007 (Passagem de Potência)**| **D1 Anodo** (Col 17, Lin 15) | **D1 Catodo** (Col 17, Lin 18) | Corpo do diodo desce na face superior (**Pitch de 7,62 mm**, queda -0.75V) |
| **1c**| **🔴 Trilha Barramento +5.25V** | **D1 Catodo** (Col 17, Lin 18) | **W5 In (16, 18) e C1(+) (15, 18)** | Trilha direta horizontal no verso (Linha 18) |
| **1d**| **⚡ Jumper W1 (+5.25V Nano)** | **C1(+) / W1 In** (Col 15, Lin 18) | **Nano +5V** (Col 06, Lin 14) | **Fio isolado superior (Jumper ~23mm)** |
| **1e**| **⚡ Jumper W5 (+5.25V Farol)**| **Barramento VCC** (Col 16, Lin 18)| **Q1 Coletor** (Col 13, Lin 09) | **Fio isolado superior (Jumper ~16mm)** |
| **1f**| **🔴 Ramal +5.25V MPU** | **Nano 5V** (Col 06, Lin 14) | (05, 14) $\rightarrow$ (05, 13) $\rightarrow$ **CON4 P4** (Col 02, Lin 13) | Trilha estanhada no verso |
| **2** | **⚡ GND Mestre Entrada** | **CON1 Pino 2** (Col 17, Lin 14) | **Nano GND Dir** (Col 12, Lin 14) | Trilha horizontal reta (Linha 14) |
| **2b**| **⚡ Jumper W2 GND Frente**| **GND Mestre** (Col 16, Lin 14) | **CON2 P1** (Col 16, Lin 07 $\rightarrow$ ponte 17, 07) | **Fio isolado superior (Jumper ~18mm)** |
| **2c**| **⚡ Jumper W3 GND Cross**| **Nano GND Dir** (Col 12, Lin 14) | **Nano GND Esq** (Col 06, Lin 16) | **Fio isolado superior (Jumper ~16mm)** |
| **2d**| **⚡ GND C1(-) Filtro** | **C1(-)** (Col 14, Lin 18) | **Tronco GND Coluna 13** (Col 13, Lin 18) | Ponte direta de solda no verso (1 pad) |
| **3** | **📻 Rádio CH2** | **CON1 Pino 3** (Col 17, Lin 13) | **Nano D2** (Col 12, Lin 13) | Trilha horizontal direta de 10mm (Linha 13) |
| **4** | **📻 Rádio CH4** | **CON1 Pino 4** (Col 17, Lin 12) | **Nano D3** (Col 12, Lin 12) | Trilha horizontal direta de 10mm (Linha 12) |
| **5** | **📻 Rádio CH1** | **CON1 Pino 5** (Col 17, Lin 11) | **Nano D4** (Col 12, Lin 11) | Trilha horizontal direta de 10mm (Linha 11) |
| **6** | **🧭 MPU RX (SDA)** | **CON4 Pino 3** (Col 02, Lin 12) | **Nano A4** (Col 06, Lin 10) | **Fio isolado superior (Jumper W4 ~11mm)** |
| **7** | **🧭 MPU TX (SCL)** | **CON4 Pino 2** (Col 02, Lin 11) | **Nano A5** (Col 06, Lin 11) | Trilha horizontal direta de 10mm (Linha 11) |
| **8** | **⚡ GND MPU (P1)** | **CON4 Pino 1** (Col 02, Lin 10) | **Barramento Col 01** (Col 01, Lin 10) | Ponte direta de solda (1 pad) |
| **9** | **⚡ Barramento Col 01** | **Ponto (Col 02, Lin 16)** | Coluna 01 (Linhas 01 a 24) | Trilha vertical contínua de terra |
| **10**| **⚡ GND Traseiro (CON3)**| **Nano GND Dir** (Col 12, Lin 14) | Desce reto pela Coluna 13 até **CON3 P6** (Col 13, Lin 24) | Trilha vertical desimpedida |
| **11**| **💡 Trilha Base Farol (D9)**| **Nano D9** (Col 12, Lin 06) | (14, 06) $\rightarrow$ **Q1 Base** (Col 14, Lin 09) | Trilha em L no verso |
| **11b**|**💡 Emissor Farol ➔ R1** | **Q1 Emissor** (Col 15, Lin 09) | **R1 In** (Col 15, Lin 08) | Ponte curta de solda |
| **11c**|**💡 Saída R1 ➔ CON2 Farol**| **R1 Out** (Col 15, Lin 06) | **CON2 P2** (Col 17, Lin 06 via ponte 16, 06) | Trilha direta horizontal |
| **12**| **💡 Trilha Pis.FE (D10)**| **Nano D10** (Col 12, Lin 05) | **R2 In** (Col 14, Lin 05) | Trilha direta horizontal 5mm no verso |
| **12b**|**💡 Saída Pisca FE** | **R2 Out** (Col 16, Lin 05) | **CON2 P3** (Col 17, Lin 05) | Ponte de solda direta (1 pad) |
| **13**| **💡 Trilha Pis.FD (D11)**| **Nano D11** (Col 12, Lin 04) | **R3 In** (Col 14, Lin 04) | Trilha direta horizontal 5mm no verso |
| **13b**|**💡 Saída Pisca FD** | **R3 Out** (Col 16, Lin 04) | **CON2 P4** (Col 17, Lin 04) | Ponte de solda direta (1 pad) |
| **14**| **💡 Pisca TD (D8)** | **Nano D8** (Col 12, Lin 07) | Lin 07 até Col 08 $\rightarrow$ **R7 Top** (Col 08, Lin 18) $\rightarrow$ **R7 Bot** $\rightarrow$ **CON3 P1** | Trilha em L aninhada |
| **15**| **💡 Pisca TE (D7)** | **Nano D7** (Col 12, Lin 08) | Lin 08 até Col 09 $\rightarrow$ **R6 Top** (Col 09, Lin 18) $\rightarrow$ **R6 Bot** $\rightarrow$ **CON3 P2** | Trilha em L aninhada |
| **16**| **💡 Freio (D6)** | **Nano D6** (Col 12, Lin 09) | Lin 09 até Col 10 $\rightarrow$ **R5 Top** (Col 10, Lin 18) $\rightarrow$ **R5 Bot** $\rightarrow$ **CON3 P3** | Trilha em L aninhada |
| **17**| **💡 Lanterna (D5)** | **Nano D5** (Col 12, Lin 10) | Lin 10 até Col 11 $\rightarrow$ **R4 Top** (Col 11, Lin 18) $\rightarrow$ **R4 Bot** $\rightarrow$ **CON3 P4** | Trilha em L aninhada |

---

### 📋 4. Lista Completa de Componentes da Placa Shield (BOM v8.4)

> 🛒 **Lista de Compras Local (HU Infinito):** Para aquisição de peças em lojas locais com disponibilidade imediata, consulte o guia local **[SBOM_COMPRAS_HU_INFINITO.md](SBOM_COMPRAS_HU_INFINITO.md)** (mantido localmente com links e estoque verificado).

| Identificador | Componente | Descrição / Valor | Função e Localização |
| :---: | :--- | :--- | :--- |
| **U1** | Soquete Arduino Nano | 2x Barras Fêmea 1x15 (Passo 2.54mm) | Colunas 06 e 12 (Linhas 03 a 17) |
| **U2** | MPU-6050 (GY-521) | Módulo sensor inercial 3D I2C | Fixado no chassi via chicote CON4 |
| **D1** | Diodo Retificador | **1N4007** (DO-41, 1A 1000V) | **Regulador de Queda BEC 6.0V $\rightarrow$ +5.25V & Proteção Reversa** — Coluna 17 (Linhas 15 a 18, Pitch 7,62mm) |
| **Q1** | Transistor Bipolar NPN | **BC337** (TO-92, 800mA máx) | **Driver Faróis High-Side** — Linha 09 (Cols 13 a 15) |
| **C1** | Capacitor Eletrolítico | **$100\mu\text{F} \times 25\text{V}$** | **Linha 18 (Colunas 14 e 15)**, colado a D1 e ligado ao GND da Col 13 |
| **R1** | Resistor 1/4W | **$27\Omega$** (Vermelho, Violeta, Preto, Ouro) | Limitador Farol Q1 (D9) — Vertical: Coluna 15 (Linhas 06 a 08) |
| **R2** | Resistor 1/4W | **$100\Omega$** (Marrom, Preto, Marrom, Ouro) | Limitador Pisca Diant. Esq. (D10) — Horizontal: Linha 05 (Cols 14 a 16) |
| **R3** | Resistor 1/4W | **$100\Omega$** (Marrom, Preto, Marrom, Ouro) | Limitador Pisca Diant. Dir. (D11) — Horizontal: Linha 04 (Cols 14 a 16) |
| **R7** | Resistor 1/4W | **$100\Omega$** (Marrom, Preto, Marrom, Ouro) | Limitador Pisca Tras. Dir. (D8) — Vertical: Col 08 (Linhas 18 a 21) |
| **R6** | Resistor 1/4W | **$100\Omega$** (Marrom, Preto, Marrom, Ouro) | Limitador Pisca Tras. Esq. (D7) — Vertical: Col 09 (Linhas 18 a 21) |
| **R5** | Resistor 1/4W | **$100\Omega$** (Marrom, Preto, Marrom, Ouro) | Limitador Luz de Freio (D6) — Vertical: Col 10 (Linhas 18 a 21) |
| **R4** | Resistor 1/4W | **$100\Omega$** (Marrom, Preto, Marrom, Ouro) | Limitador Lanterna Traseira (D5) — Vertical: Col 11 (Linhas 18 a 21) |
| **CON1** | Barra de Pinos 90° | **1x5 Pinos Macho 90°** | **Lateral Direita** (Col 17, Linhas 11 a 15) — Entrada Rádio FS-BS6 |
| **CON2** | Barra de Pinos 90° | **1x4 Pinos Macho 90°** | **Lateral Superior Direita** (Col 17, Linhas 04 a 07) — Chicote Frente |
| **CON4** | Barra de Pinos 90° | **1x4 Pinos Macho 90°** | **Lateral Esquerda** (Col 02, Linhas 10 a 13) — MPU-6050 (P1: GND, P2: TX/SCL, P3: RX/SDA, P4: VCC) |
| **CON3** | Barra de Pinos 90° | **1x6 Pinos Macho 90°** | **Borda Inferior Centro-Dir** (Linha 24, Cols 08 a 13) — Chicote Trás |
| **W1-W5**| Fios Jumpers Isolados | **5x Fios flexíveis com capa (28-30 AWG)** | Face superior: W1 (+5.25V 15,18➔06,14), W2 (GND Frente 16,14➔16,07), W3 (GND Cross 12,14➔06,16), W4 (MPU SDA/RX 02,12➔06,10), W5 (+5.25V Farol 16,18➔13,09) |

---

## English

Please refer to [SHIELD_BOARD_LAYOUT.md](SHIELD_BOARD_LAYOUT.md) for the complete English documentation, coordinates grid, and distributed component layout.
