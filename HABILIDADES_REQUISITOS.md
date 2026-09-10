# Habilidades, Requisitos e Solução de Problemas — Sistema de Luzes RC v8.4

[🇧🇷 **Versão em Português**](#-português) | [🇺🇸 **English Version (SKILLS_REQUIREMENTS.md)**](SKILLS_REQUIREMENTS.md)

---

## Português

> [!IMPORTANT]
> **Premissas Oficiais do Projeto:** Antes de iniciar a montagem da placa shield ou do chicote, consulte o documento normativo [PREMISSAS_PROJETO.md](PREMISSAS_PROJETO.md). A alimentação principal (+6.0V nominal do BEC e GND) provém exclusivamente do receptor de rádio via **CON1 (CH6)**. A placa integra onboard o diodo regulador **D1 (1N4007)** (Coluna 17, Linhas 15 a 18) para gerar o barramento seguro de $+5.25\text{V}$ e o capacitor de desacoplamento **C1** ($100\mu\text{F} \times 25\text{V}$) na Linha 18 (Pads 15,18 e 14,18).

Para montar, calibrar e instalar com sucesso este sistema de iluminação em seu carro RC, você precisará de ferramentas básicas de eletrônica, habilidades manuais e materiais de proteção contra água e vibração.

### 🛠️ Ferramentas e Materiais Necessários

| Ferramenta / Material | Utilidade no Projeto | Importância |
|---|---|:---:|
| **Ferro de Solda (30W a 60W)** | Fazer as conexões elétricas permanentes na placa shield e chicotes. | **Indispensável** |
| **Estanho de Solda (com fluxo)** | Ligar eletricamente os fios, resistores, transistores e barras de pinos. | **Indispensável** |
| **Placa Perfurada Ilhada (5x7 cm)** | Base física do Shield Hub (18 colunas x 24 linhas, passo 2.54mm). | **Indispensável** |
| **Barras de Pinos Macho em 90° (Passo 2.54mm)** | Conectores CON1 (1x5), CON2 (1x4), CON3 (1x6) e CON4 (1x4) em 90° para fiação paralela à placa sem colidir com a bolha. | **Indispensável** |
| **Diodo Retificador 1N4007 (DO-41)** | Diodo D1 na Coluna 17 (Linhas 15 a 18, pitch 7.62mm): reduz BEC 6.0V em ~0.75V para +5.25V seguro e protege contra inversão. | **Indispensável** |
| **Transistor BC337 NPN (TO-92)** | Driver Q1 seguidor de emissor para fornecer até 60mA aos 4 faróis dianteiros sem sobrecarregar o microcontrolador. | **Indispensável** |
| **Resistor 27Ω 1/4W (Filme de Carbono)** | Resistor R1 de limitação de corrente dos 4 faróis em paralelo acionados por Q1. | **Indispensável** |
| **Resistores 100Ω 1/4W (6 unidades)** | Resistores R2 a R7 dos canais diretos (piscas dianteiros/traseiros, freio e lanternas). | **Indispensável** |
| **Capacitor Eletrolítico ($100\mu\text{F} \times 25\text{V}$)** | Filtro e desacoplamento de entrada C1 na Linha 18 (Pads 15,18 e 14,18), absorvendo transientes do ESC e servo. | **Indispensável** |
| **Tubo Termoretrátil (1.0mm a 3.0mm)**| Isolar emendas, derivações de GND, pernas de componentes e terminais dos chicotes. | **Indispensável** |
| **Alicate de Corte e Descascador** | Cortar e expor a ponta metálica dos fios flexíveis. | **Indispensável** |
| **Alicate de Bico Fino ou de Crimpagem**| Cravar os terminais MODU fêmea nos fios da bolha e do rádio. | **Indispensável** |
| **Multímetro Digital** | Medir continuidade (curtos), testar polaridade dos LEDs e verificar tensões. | **Altamente Recomendado** |
| **Graxa de Silicone Dielétrica / Vaselina**| Vedar os conectores MODU contra água, poeira e oxidação. | **Recomendado (Off-Road)**|
| **Fita de Alumínio Automotiva** | Fixar e ocultar os fios no teto/laterais da bolha Lexan. | **Recomendado** |
| **Silicone Neutro / Shoe Goo / E6000**| Fixar e vedar a traseira dos LEDs nos copos óticos da bolha.| **Recomendado** |
| **Verniz Isolante / Esmalte Incolor** | Proteger as trilhas e soldas no verso da placa shield e no MPU-6050. | **Recomendado** |

### 🧠 Habilidades Recomendadas

1. **Soldagem Eletrônica Básica:** Solde os resistores, transistor Q1, diodo D1, capacitor C1 e as barras de pinos macho em 90° na placa perfurada de 5x7cm conforme o layout em [PLACA_SHIELD_LAYOUT.md](PLACA_SHIELD_LAYOUT.md). Aqueça a ilha de cobre e o terminal do componente por 2 segundos antes de aplicar o estanho para obter uma junta brilhante e resistente à vibração.
2. **Identificação de Polaridade de Componentes:** 
   - **LEDs:** Ânodo (+, perna longa) e Cátodo (-, perna curta / chanfro).
   - **Diodo D1 (1N4007):** Terminal Cátodo indicado pela **faixa prateada**, inserido no Pad `(17, 18)`.
   - **Capacitor C1:** Polo Negativo (-) identificado pela faixa cinza/branca com sinal de menos, inserido no Pad `(14, 18)`.
   - **Transistor Q1 (BC337 TO-92):** Com a face plana voltada para a esquerda, a pinagem é Coletor `(13, 09)`, Base `(14, 09)` e Emissor `(15, 09)`.
3. **Uso do Multímetro (Básico):** Meça a continuidade entre a trilha de 5V e o GND da placa shield antes de ligar no receptor. Se houver um "bipe", pare e remova o curto-circuito antes de energizar pelo CH6.
4. **Fixação Mecânica do Acelerômetro MPU-6050:** Fixe o módulo GY-521 com fita dupla face espumada (3M VHB) no chassi do carro para amortecer vibrações de alta frequência. O algoritmo vetorial 3D calibra a orientação automaticamente.

### 🔍 Resolução de Problemas (Troubleshooting)

- **O LED não acende:** Verifique se a polaridade do LED não está invertida, se o conector MODU está encaixado na posição correta ou se a solda do resistor está íntegra.
- **O Arduino não responde aos comandos do rádio:**
  - Verifique se o cabo do rádio (CON1) está plugado corretamente: **Pino 1 no VCC (+6.0V BEC)** e **Pino 2 no GND** do canal **CH6** (conforme [PREMISSAS_PROJETO.md](PREMISSAS_PROJETO.md)).
  - Verifique os canais de sinal: Volante no **CH1 (D4)**, Acelerador no **CH2 (D2)**, Farol no **CH4 (D3)**.
- **O acelerômetro MPU-6050 não é detectado:**
  - Verifique as conexões I2C: **SDA no pino A4** e **SCL no pino A5**. O sistema possui inicialização graciosa e continua funcionando via rádio mesmo sem o sensor.
- **Piscas entram em alerta 4x constante (como se estivesse capotado):**
  - O carro precisa estar apoiado sobre as 4 rodas no chão durante os primeiros 2 segundos após ligar para calibrar o vetor estático de gravidade $\vec{g}_0$.
- **O carro liga mas o neutro está torto ou o pisca fica aceso direto:**
  - Desligue o carro, certifique-se de que o volante e o gatilho estão centralizados no rádio, e ligue o carro novamente. O Arduino recalibrará o neutro automaticamente nos primeiros 2 segundos.
- **Como recalibrar os limites na pista sem computador (Gesto de Calibração):**
  - Ligue o rádio, segure o volante com **mais de 50% de deflexão para a direita (ou esquerda)** e ligue o carro mantendo o volante defletido por **1.5 segundos**. O Arduino confirmará com 3 piscadas e entrará no modo de calibração autônoma guiada pelos LEDs.
- **Faróis oscilam ou piscam sozinhos sob aceleração forte (ruído eletromagnético / queda de tensão):**
  - Certifique-se de que o capacitor eletrolítico C1 ($100\mu\text{F} \times 25\text{V}$) está soldado exatamente na Linha 18 (Pads 15,18 e 14,18) e que o diodo D1 (1N4007) está bem soldado na Coluna 17 para filtrar ruídos do ESC/motor e estabilizar o barramento de +5.25V.

---

## English

Please refer to [SKILLS_REQUIREMENTS.md](SKILLS_REQUIREMENTS.md) for the complete English documentation, tool lists, and troubleshooting steps.
