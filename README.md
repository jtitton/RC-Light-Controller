# Sistema de Luzes RC v2.0 — Manual do Usuário

[🇧🇷 **Versão em Português**](#-português) | [🇺🇸 **English Version (README_EN.md)**](README_EN.md)

---

## 🇧🇷 Português

Este projeto consiste em um controlador inteligente de iluminação para carros de controle remoto (RC), baseado no microcontrolador **Arduino Nano** e alimentado diretamente pela porta **Canal 6 (CH6)** de um receptor de rádio **FlySky FS-BS6** (ou qualquer outro receptor PPM compatível).

---

### 📁 Versões do Firmware Disponíveis

O projeto conta com **dois firmwares independentes**, cada um otimizado para uma finalidade:

| Firmware | Propósito | Características Técnicas | Consumo de Recursos |
|---|---|---|:---:|
| **[LuzesArduino.ino](LuzesArduino.ino)** | **Desenvolvimento & Simulação Wokwi** | Comunicação Serial ativa (115200 baud), menu de comandos (`C`, `A`, `P`, `R`), **simulação de pista de 60s (`T`)**, e **pilotagem manual por teclado (`W/S/E/D/F/X`)**. | Flash: 13.8 kB (45%)<br>RAM: 692 B (33%) |
| **[LuzesArduino_Producao.ino](LuzesArduino_Producao/LuzesArduino_Producao.ino)** | **Produção & Corrida na Pista** | **Zero Serial** (UART desligada, 100% autônomo), loop principal a **> 60.000 Hz**, calibração autônoma por gesto no volante e feedback 100% visual nos LEDs da bolha. | **Flash: 5.4 kB (17%)**<br>**RAM: 102 B (4%)** |

> [!TIP]
> * Para testar no computador ou no simulador online: use **[LuzesArduino.ino](LuzesArduino.ino)**.
> * Para gravar no microcontrolador e colocar o carro na pista: use **[LuzesArduino_Producao.ino](LuzesArduino_Producao/LuzesArduino_Producao.ino)**.

---

### 📋 Índice da Documentação

| Documento em Português | Documento em Inglês (English Version) | Descrição do Conteúdo |
|---|---|---|
| **[README.md](README.md)** | **[README_EN.md](README_EN.md)** | Visão geral, comparação de firmwares e guia de operação. |
| **[ESQUEMA_LIGACAO.md](ESQUEMA_LIGACAO.md)** | **[WIRING_SCHEMATIC.md](WIRING_SCHEMATIC.md)** | Diagrama elétrico completo, barramento GND comum, resistores e layout da placa shield (5x7cm). |
| **[CHICOTE_LEDS.md](CHICOTE_LEDS.md)** | **[LED_HARNESS.md](LED_HARNESS.md)** | Guia de montagem dos 3 chicotes MODU (Frente 4P, Trás 6P, Rádio/CH6 5P), catálogo HU Infinito e impermeabilização. |
| **[HABILIDADES_REQUISITOS.md](HABILIDADES_REQUISITOS.md)** | **[SKILLS_REQUIREMENTS.md](SKILLS_REQUIREMENTS.md)** | Ferramentas, soldagem, isolamento contra água, aterramento e resolução de problemas (*troubleshooting*). |
| **[wokwi_diagram.json](wokwi_diagram.json)** | **[wokwi_diagram.json](wokwi_diagram.json)** | Diagrama de componentes e interligações para o simulador Wokwi. |

---

### ⚙️ Principais Características do Sistema

- **100% Baseado em Interrupções (Não-bloqueante):** As leituras dos três canais do rádio (volante, throttle e farol) são capturadas via interrupções de hardware (`INT0`, `INT1` e `PCINT20`). O loop principal roda a mais de **40.000 Hz** (versão Dev) e **60.000 Hz** (versão Produção).
- **Alimentação Integrada via Canal 6 (CH6):** O Arduino e os LEDs são energizados diretamente pela porta CH6 do receptor (usando o BEC do ESC), dispensando baterias extras no carro.
- **Equilíbrio de Neutro e Barramento GND Comum:** O terra do receptor, do Arduino e de todos os LEDs é unificado na placa shield, eliminando flutuações e ruídos no sinal PPM.
- **Transição Suave (Fade):** As lanternas traseiras possuem transições suaves de intensidade (fade de ~300ms) ao acender e apagar, imitando lâmpadas reais.
- **Filtro de Ruído Inteligente:** Um filtro de média móvel de 5 amostras remove oscilações causadas pelo motor elétrico.
- **Calibração Autônoma de Campo por Gesto:** Permite calibrar os extremos dos manípulos diretamente pelo rádio na pista (segurando o volante virado no boot), sem precisar de computador.
- **Auto-centro Resiliente:** A cada inicialização, o Arduino detecta a posição de repouso atual do controle em 2 segundos, compensando automaticamente ajustes de Trim do rádio.

---

### ⚙️ Parâmetros e Configuração de Software

No arquivo principal, você pode ajustar os limiares de controle:

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

---

### ⏱ Inicialização Autônoma e Calibração

#### 🚦 Inicialização Normal de Corrida (No dia a dia)
1. Ligue o rádio transmissor com os manípulos soltos no centro.
2. Ligue o carro.
3. Os 4 piscas acendem durante **2 segundos** (leitura automática do centro de neutro).
4. Os LEDs dão **2 piscadas rápidas** confirmando que o auto-centro foi concluído.
5. Pronto para acelerar!

#### 🎯 Calibração Autônoma de Campo (Por Gesto no Rádio - Sem PC)
Se você trocar de rádio ou quiser recalibrar os limites máximos no meio da pista:
1. Ligue o rádio transmissor e segure o volante **todo virado para a direita (ou esquerda)**.
2. Ligue o carro mantendo o volante virado por 2 segundos.
3. Os LEDs darão **3 piscadas rápidas** indicando a entrada no modo de calibração.
4. **Auto-Centro (2s):** Solte o volante e o gatilho no centro (piscas ficam fixos).
5. **Passo 1 (Extremos - 5s):** Os piscas esquerdo e direito piscarão alternadamente. Mova o volante todo para a esquerda/direita e o gatilho todo para a frente/trás.
6. **Passo 2 (Farol - 5s):** O farol dianteiro começará a pulsar suavemente. Alterne a chave de 3 posições do Canal 4 entre os três estágios.
7. **Fim:** Todos os LEDs dão **5 piscadas rápidas juntas**, salvam os novos dados na EEPROM e o carro fica pronto para correr!

---

### 🎮 Controles no Monitor Serial (Simulador Wokwi & Bancada)

Na versão de desenvolvimento ([LuzesArduino.ino](LuzesArduino.ino)), você pode pilotar o carro pelo teclado no terminal (**115200 baud**).

Cada toque nas teclas de movimento adiciona **+500 ms cumulativos** à ação (ex: 3 toques = 1,5 segundos de ação):

| Tecla / Comando | Ação Simulada | Comportamento / Duração |
| :---: | :--- | :--- |
| **`W`** ou **`w`** | **Acelerar Frente** (+100%) | Freio OFF. **+500 ms** por toque (cumulativo). |
| **`S`** ou **`s`** | **Freiar / Ré** (-100%) | Luz de Freio e Lanternas ON (100%). **+500 ms** por toque (cumulativo). |
| **`A`** ou **`a`** | **Virar para a Esquerda** (-100%) | Piscas Esquerdos piscam (120 bpm). **+500 ms** por toque (cumulativo). |
| **`D`** ou **`d`** | **Virar para a Direita** (+100%) | Piscas Direitos piscam (120 bpm). **+500 ms** por toque (cumulativo). |
| **`F`** ou **`f`** | **Aumentar Farol** | Eleva o brilho: **OFF $\rightarrow$ 40% PWM $\rightarrow$ 100% PWM**. |
| **`G`** ou **`g`** | **Diminuir Farol** | Reduz o brilho: **100% PWM $\rightarrow$ 40% PWM $\rightarrow$ OFF**. |
| **`X`** ou **`x`** | **Centralizar / Neutro Imediato** | Zera os timers e desliga piscas e luz de freio na hora. |
| **`T`** ou **`t`** | **Simulação de Corrida Automática** | Executa a pista virtual de 60 segundos com curvas, ré e freios. |
| **`N`** ou **`n`** | **Modo Normal (Rádio Receptor)** | Sai da simulação manual e volta a ler os pinos físicos do rádio. |
| **`C`** ou **`c`** | **Calibração Completa** | Executa o passo a passo de calibração via terminal. |
| **`Z`** ou **`z`** | **Re-centralizar Sticks (Trim)** | Lê a posição de neutro dos manípulos. |
| **`P`** ou **`p`** | **Imprimir Calibração** | Exibe no terminal os valores atuais salvos na EEPROM. |
| **`?`** | **Menu de Ajuda** | Exibe a lista de comandos no terminal. |
