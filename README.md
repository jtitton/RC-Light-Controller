# Sistema de Luzes RC v5.1 — Manual do Usuário / User Manual

[**Português**](#português) | [**English**](#english)

---

## Português

Este projeto consiste em um controlador inteligente de iluminação para carros de controle remoto (RC), baseado no microcontrolador **Arduino Nano** e alimentado pelos sinais de um receptor de rádio **FlySky FS-BS6** (ou qualquer outro compatível).

### 📋 Sumário de Documentação

Todos os documentos estão localizados nesta pasta para fácil acesso:
1. **[README.md](file:///c:/Users/Jonat/OneDrive/Documentos/AI/LuzesArduino/README.md)** (Este arquivo) — Visão geral e instruções de configuração/operação.
2. **[ESQUEMA_LIGACAO.md](file:///c:/Users/Jonat/OneDrive/Documentos/AI/LuzesArduino/ESQUEMA_LIGACAO.md)** — Diagrama de pinos do Arduino, receptor, resistores e LEDs.
3. **[CHICOTE_LEDS.md](file:///c:/Users/Jonat/OneDrive/Documentos/AI/LuzesArduino/CHICOTE_LEDS.md)** — Instruções de confecção do chicote elétrico (harness), conectores e fiação.
4. **[HABILIDADES_REQUISITOS.md](file:///c:/Users/Jonat/OneDrive/Documentos/AI/LuzesArduino/HABILIDADES_REQUISITOS.md)** — Habilidades de soldagem, montagem e ferramentas necessárias para o projeto.

### ⚙️ Principais Características da Versão 5.1

- **100% Baseado em Interrupções (Não-bloqueante):** As leituras dos três canais do rádio (volante, throttle e farol) são capturadas via interrupções de hardware (`INT0`, `INT1` e `PCINT20`). O loop principal roda a mais de **40.000 Hz**.
- **Transição Suave (Fade):** As lanternas traseiras possuem transições suaves de intensidade (fade de ~300ms) ao acender e apagar, imitando lâmpadas reais.
- **Filtro de Ruído Inteligente:** Um filtro de média móvel de 5 amostras remove oscilações. O filtro só processa novos dados à medida que o receptor os envia (~50Hz).
- **Calibração Permanente na EEPROM:** O sistema calibra automaticamente os extremos dos canais de controle e salva os parâmetros na memória não volátil (EEPROM).
- **Auto-centro Resiliente:** A cada inicialização, o Arduino detecta a posição de repouso atual do controle, evitando desalinhamentos.

### ⚙️ Parâmetros e Configuração de Software

No arquivo principal [LuzesArduino.ino](file:///c:/Users/Jonat/OneDrive/Documentos/AI/LuzesArduino/LuzesArduino.ino), você pode editar as seguintes constantes:

```cpp
// Limiar de deflexão do volante para acionar o pisca (70%)
#define STEERING_BLINK_PERCENT   70

// Limiar do acelerador para acionar a luz de freio/desaceleração (5%)
#define THROTTLE_BRAKE_PERCENT   5

// Divisões da chave de 3 posições do farol (Canal 4)
#define HEADLIGHT_THRESH_LOW     33    // Abaixo disso: Farol Desligado
#define HEADLIGHT_THRESH_HIGH    66    // Entre Low e High: 40% | Acima: 100%

// Intervalo de piscar do sinaleiro (250ms ativo / 250ms inativo = 120 piscadas por minuto)
#define BLINK_INTERVAL_MS        250
```

### ⏱ Processo de Calibração Inicial

1. Ligue o rádio transmissor com os manípulos (volante e gatilho) em **posição neutra** (centralizados).
2. Abra o **Monitor Serial** da Arduino IDE e configure a velocidade para **115200 baud**.
3. Digite o caractere **`C`** e aperte **Enter** (ou envie pelo terminal).
4. **Passo 1 (Volante e Gatilho):** Os LEDs de pisca piscarão alternadamente. Mova o volante do controle todo para a esquerda/direita, e o gatilho todo para a frente/trás por 5 segundos.
5. **Passo 2 (Chave do Farol):** O farol dianteiro piscará em pulso suave. Alterne a chave de 3 posições correspondente ao Canal 4 entre os três estágios por 5 segundos.

---

## English

This project consists of an intelligent lighting controller for remote-controlled (RC) cars, based on the **Arduino Nano** microcontroller and powered by the signals of a **FlySky FS-BS6** radio receiver (or any other compatible PPM receiver).

### 📋 Documentation Index

All documents are located in this folder for easy access:
1. **[README.md](file:///c:/Users/Jonat/OneDrive/Documentos/AI/LuzesArduino/README.md)** (This file) — Overview and setup/operation instructions.
2. **[ESQUEMA_LIGACAO.md](file:///c:/Users/Jonat/OneDrive/Documentos/AI/LuzesArduino/ESQUEMA_LIGACAO.md)** — Pinout schematic for the Arduino, receiver, resistors, and LEDs.
3. **[CHICOTE_LEDS.md](file:///c:/Users/Jonat/OneDrive/Documentos/AI/LuzesArduino/CHICOTE_LEDS.md)** — Guide to making the wiring harness, connectors, and routing.
4. **[HABILIDADES_REQUISITOS.md](file:///c:/Users/Jonat/OneDrive/Documentos/AI/LuzesArduino/HABILIDADES_REQUISITOS.md)** — Tools, skills (soldering, mounting) and troubleshooting.

### ⚙️ Main Features of Version 5.1

- **100% Interrupt-Driven (Non-blocking):** All 3 radio channels (steering, throttle, headlight) are read asynchronously via interrupts (`INT0`, `INT1`, and `PCINT20`). The main loop runs at over **40,000 Hz** without blocking calls.
- **Smooth Fade Transition:** The tail lights feature a smooth fade transition (~300ms) to simulate real incandescent bulbs.
- **Smart Noise Filter:** A 5-sample moving average filter removes channel noise. The filter updates strictly when a new pulse is received from the receiver (~50Hz).
- **Persistent EEPROM Calibration:** The system automatically calibrates transmitter limits and saves them to the non-volatile memory (EEPROM).
- **Resilient Auto-Centering:** On boot, the Arduino detects the current stick neutral positions, preventing drift even if transmitter analog trims are adjusted.

### ⚙️ Software Parameters and Configuration

In the main file [LuzesArduino.ino](file:///c:/Users/Jonat/OneDrive/Documentos/AI/LuzesArduino/LuzesArduino.ino), you can edit these constants:

```cpp
// Steering deflection threshold to trigger blinkers (70%)
#define STEERING_BLINK_PERCENT   70

// Throttle threshold to trigger brake lights (5%)
#define THROTTLE_BRAKE_PERCENT   5

// Divisions of the 3-position headlight switch (Channel 4)
#define HEADLIGHT_THRESH_LOW     33    // Below this: Headlight Off
#define HEADLIGHT_THRESH_HIGH    66    // Between Low and High: 40% | Above: 100%

// Blinker toggle interval (250ms on / 250ms off = 120 blinks per minute)
#define BLINK_INTERVAL_MS        250
```

### ⏱ Initial Calibration Process

1. Turn on your transmitter with the steering wheel and throttle trigger in their **neutral (center) positions**.
2. Open the **Serial Monitor** in Arduino IDE and set the speed to **115200 baud**.
3. Send the character **`C`** in the terminal input.
4. **Step 1 (Steering and Throttle):** The blinker LEDs will flash alternately. Move the steering wheel fully left/right, and the throttle trigger fully forward/backward for 5 seconds.
5. **Step 2 (Headlight Switch):** The headlight will pulsate. Toggle the 3-position switch for Channel 4 through all three positions for 5 seconds.
