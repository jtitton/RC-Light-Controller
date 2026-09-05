# Sistema de Luzes RC v7.2 — Manual do Usuário

[🇧🇷 **Versão em Português**](#-português) | [🇺🇸 **English Version (README_EN.md)**](README_EN.md)

---

## 🇧🇷 Português

Este projeto consiste em um controlador inteligente de iluminação para carros de controle remoto (RC), baseado no microcontrolador **Arduino Nano**, acelerômetro inercial 3D **MPU-6050 (GY-521)** e alimentado diretamente pela porta **Canal 6 (CH6)** de um receptor de rádio **FlySky FS-BS6** (ou qualquer outro receptor PPM compatível).

---

### 📁 Versões do Firmware Disponíveis

O projeto conta com **dois firmwares independentes**, cada um otimizado para uma finalidade:

| Firmware | Propósito | Características Técnicas | Consumo de Recursos |
|---|---|---|:---:|
| **[LuzesArduino.ino](LuzesArduino.ino)** | **Desenvolvimento & Simulação Wokwi** | Comunicação Serial ativa (115200 baud), telemetria inercial (`I`), simulação de capotamento (`K`), menu de comandos (`C`, `Z`, `P`, `R`), **simulação de pista de 60s (`T`)**, e **pilotagem manual por teclado (`W/S/A/D/F/G/X`)**. | Flash: 23.7 kB (77%)<br>RAM: 983 B (47%) |
| **[LuzesArduino_Producao.ino](LuzesArduino_Producao/LuzesArduino_Producao.ino)** | **Produção & Corrida na Pista** | **Zero Serial** (UART desligada, 100% autônomo), leitura I2C Fast-Mode (400kHz), loop principal a **~1–2 kHz com MPU ativo** (~20–30 kHz em fallback sem MPU), auto-alinhamento 3D, alerta de capotamento e feedback 100% visual nos LEDs. | **Flash: 11.5 kB (37%)**<br>**RAM: 363 B (17%)** |

> [!TIP]
> * Para testar no computador ou no simulador online: use **[LuzesArduino.ino](LuzesArduino.ino)**.
> * Para gravar no microcontrolador e colocar o carro na pista: use **[LuzesArduino_Producao.ino](LuzesArduino_Producao/LuzesArduino_Producao.ino)**.

---

### 📋 Índice da Documentação

| Documento em Português | Documento em Inglês (English Version) | Descrição do Conteúdo |
|---|---|---|
| **[README.md](README.md)** | **[README_EN.md](README_EN.md)** | Visão geral, comparação de firmwares, integração inercial e guia de operação. |
| **[PLACA_SHIELD_LAYOUT.md](PLACA_SHIELD_LAYOUT.md)** | **[SHIELD_BOARD_LAYOUT.md](SHIELD_BOARD_LAYOUT.md)** | **Projeto de engenharia da placa perfurada (5x7cm)**: grid de coordenadas 18x24, trilhas de solda, barramento GND e layout de componentes. |
| 🌐 **[Visualizador Interativo da Placa](placa_shield_visualizador.html)** | 🌐 **[Interactive Board Visualizer](placa_shield_visualizador.html)** | **Modelo gráfico visual interativo** (HTML/SVG): vistas superior, inferior espelhada para solda, raio-x e destaque de circuitos. |
| **[ESQUEMA_LIGACAO.md](ESQUEMA_LIGACAO.md)** | **[WIRING_SCHEMATIC.md](WIRING_SCHEMATIC.md)** | Diagrama elétrico completo, barramento I2C MPU-6050 (A4/A5), GND comum e conexões do receptor CH6. |
| **[CHICOTE_LEDS.md](CHICOTE_LEDS.md)** | **[LED_HARNESS.md](LED_HARNESS.md)** | Guia de montagem dos chicotes MODU (Frente 4P, Trás 6P, Rádio/CH6 5P, MPU-6050 4P), catálogo HU e impermeabilização. |
| **[PREMISSAS_PROJETO.md](PREMISSAS_PROJETO.md)** | **[PREMISSAS_PROJETO.md](PREMISSAS_PROJETO.md)** | **Premissas Normativas de Engenharia**: alimentação via rádio (CH6), regulação na entrada com C1 e GND mestre unificado. |
| **[HABILIDADES_REQUISITOS.md](HABILIDADES_REQUISITOS.md)** | **[SKILLS_REQUIREMENTS.md](SKILLS_REQUIREMENTS.md)** | Ferramentas, soldagem, isolamento contra água, aterramento e resolução de problemas (*troubleshooting*). |
| **[wokwi_diagram.json](wokwi_diagram.json)** / **[diagram.json](diagram.json)** | **[wokwi_diagram.json](wokwi_diagram.json)** / **[diagram.json](diagram.json)** | Diagrama de componentes e interligações para o simulador Wokwi (com alimentação de rádio, barramento GND e MPU-6050). |

---

### ⚙️ Principais Características do Sistema (v7.2)

- **Acelerômetro Inercial I2C (MPU-6050) com I2C Fast-Mode (400kHz):** Detecta aceleração e frenagem física real da carroceria independentemente da orientação de montagem do sensor.
- **Algoritmo de Auto-Alinhamento Vetorial 3D:** O sistema calibra a gravidade de repouso $\vec{g}_0$ no boot e extrai o vetor longitudinal de marcha $\vec{u}_{\text{long}}$ por produto escalar $A_{\text{long}} = (\vec{a} - \vec{g}_0) \cdot \vec{u}_{\text{long}}$, permitindo fixar a placa em qualquer posição ou inclinação no chassi.
- **Fusão de Sensores na Frenagem:** A luz de freio é acionada pelo gatilho do rádio (PPM $< -5\%$) **OU** por desaceleração física inercial ($A_{\text{long}} \le -0.20G$), simulando o efeito de freio-motor e frenagem real em pista.
- **Alerta de Capotamento (Roll-Over Safety):** Se o veículo capotar ou tombar lateralmente ($\theta > 81^\circ$), os 4 piscas entram automaticamente em modo de alerta rápido (120ms).
- **Operação Graciosa Resiliente:** Se o módulo MPU-6050 não estiver conectado nos pinos A4/A5, o sistema opera normalmente em modo Rádio PPM exclusivo.
- **100% Baseado em Interrupções (Não-bloqueante):** Leituras PPM de volante, acelerador e farol via `INT0`, `INT1` e `PCINT20`.
- **Alimentação Integrada via Canal 6 (CH6):** O Arduino, os LEDs e o acelerômetro são energizados diretamente pelo receptor (BEC nominal 5.0V do ESC).
- **Transição Suave (Fade):** Lanternas traseiras possuem transições suaves de intensidade (fade de ~300ms) ao acender e apagar.
- **Calibração Autônoma por Gesto no Rádio:** Calibração completa de neutro, extremos e faróis diretamente na pista segurando o volante defletido ($\ge 50\%$) por 1.5 segundos no boot.

---

### ⚙️ Parâmetros e Configuração de Software

No firmware, os limiares de acionamento são configurados como constantes:

```cpp
// --- Acelerômetro MPU-6050 (I2C) ---
#define ACCEL_BRAKE_THRESH_G     0.20f   // Desaceleração >= 0.20G acende a luz de freio
#define ACCEL_ROLLOVER_COS       0.15f   // Ângulo > 81° com a vertical ativa pisca-alerta 4x

// --- Limiares de Rádio (%) ---
#define STEERING_BLINK_PERCENT   70      // Deflexão do volante para ligar pisca (70%)
#define THROTTLE_BRAKE_PERCENT   5       // Desaceleração PPM para acionar freio (5%)
#define HEADLIGHT_THRESH_LOW     33      // Abaixo: Farol OFF | Acima: 40%
#define HEADLIGHT_THRESH_HIGH    66      // Acima: 100%

// --- Intervalos de Pisca ---
#define BLINK_INTERVAL_MS        250     // 120 bpm (setas direcionais)
#define BLINK_HAZARD_MS          120     // 250 bpm (alerta de capotamento)
```

---

### ⏱ Inicialização Autônoma e Calibração

#### 🚦 Inicialização Normal de Corrida (No dia a dia)
1. Ligue o rádio transmissor com os manípulos soltos no centro.
2. Ligue o carro.
3. Os 4 piscas acendem durante **2 segundos** (leitura do centro de neutro e calibração estática da gravidade $\vec{g}_0$).
4. Os LEDs dão **2 piscadas rápidas** confirmando que o sistema está pronto.
5. Pronto para acelerar!

#### 🎯 Calibração Autônoma de Campo (Por Gesto no Rádio - Sem PC)
Se você trocar de rádio ou quiser recalibrar os limites máximos na pista:
1. Ligue o rádio transmissor e segure o volante com **mais de 50% de deflexão para a direita (ou esquerda)**.
2. Ligue o carro mantendo o volante defletido por **1.5 segundos**.
3. Os LEDs darão **3 piscadas rápidas** indicando a entrada no modo de calibração.
4. **Auto-Centro (2s):** Solte o volante e o gatilho no centro (piscas ficam fixos).
5. **Passo 1 (Extremos - 5s):** Os piscas esquerdo e direito piscarão alternadamente. Mova o volante e o acelerador aos batentes.
6. **Passo 2 (Farol - 5s):** O farol dianteiro começará a pulsar suavemente. Alterne a chave do Canal 4 entre os três estágios.
7. **Fim:** Todos os LEDs dão **5 piscadas rápidas juntas**, salvam os dados na EEPROM e o carro está pronto!

---

### 🎮 Controles no Monitor Serial (Simulador Wokwi & Bancada)

Na versão de desenvolvimento ([LuzesArduino.ino](LuzesArduino.ino)), você pode pilotar o carro pelo teclado no terminal (**115200 baud**).

Cada toque nas teclas de movimento adiciona **+500 ms cumulativos** à ação:

| Tecla / Comando | Ação Simulada | Comportamento / Duração |
| :---: | :--- | :--- |
| **`W`** ou **`w`** | **Acelerar Frente** (+100%) | Freio OFF, Força G longitudinal $+0.40G$. **+500 ms** por toque. |
| **`S`** ou **`s`** | **Freiar / Ré** (-100%) | Luz de Freio e Lanternas ON, Força G $-0.60G$. **+500 ms** por toque. |
| **`A`** ou **`a`** | **Virar para a Esquerda** (-100%) | Piscas Esquerdos piscam (120 bpm). **+500 ms** por toque. |
| **`D`** ou **`d`** | **Virar para a Direita** (+100%) | Piscas Direitos piscam (120 bpm). **+500 ms** por toque. |
| **`F`** ou **`f`** | **Aumentar Farol** | Eleva o brilho: **OFF $\rightarrow$ 40% PWM $\rightarrow$ 100% PWM**. |
| **`G`** ou **`g`** | **Diminuir Farol** | Reduz o brilho: **100% PWM $\rightarrow$ 40% PWM $\rightarrow$ OFF**. |
| **`K`** ou **`k`** | **Simular Capotamento** | Alterna estado de tombamento (aciona pisca-alerta 4x a 120ms). |
| **`I`** ou **`i`** | **Telemetria Inercial MPU-6050** | Exibe vetores 3D $\vec{g}_0$, $\vec{u}_{\text{long}}$ e Força G de marcha. |
| **`X`** ou **`x`** | **Centralizar / Neutro Imediato** | Zera os timers e desliga piscas e luz de freio na hora. |
| **`T`** ou **`t`** | **Simulação de Corrida Automática** | Executa a pista virtual de 60 segundos com curvas, ré e freios. |
| **`N`** ou **`n`** | **Modo Normal (Rádio Receptor)** | Sai da simulação manual e volta a ler os pinos físicos do rádio. |
| **`C`** ou **`c`** | **Calibração Completa** | Executa o passo a passo de calibração via terminal. |
| **`Z`** ou **`z`** | **Re-centralizar Sticks (Trim)** | Recalibra ponto de repouso dos servos e gravidade $\vec{g}_0$. |
| **`P`** ou **`p`** | **Imprimir Calibração** | Exibe no terminal os valores salvos na EEPROM. |
| **`?`** | **Menu de Ajuda** | Exibe a lista de comandos no terminal. |
