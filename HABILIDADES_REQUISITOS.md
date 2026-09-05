# Habilidades, Requisitos e Solução de Problemas — Sistema de Luzes RC v7.2

[🇧🇷 **Versão em Português**](#-português) | [🇺🇸 **English Version (SKILLS_REQUIREMENTS.md)**](SKILLS_REQUIREMENTS.md)

---

## Português

> [!IMPORTANT]
> **Premissas Oficiais do Projeto:** Antes de iniciar a montagem da placa shield ou do chicote, consulte o documento normativo [PREMISSAS_PROJETO.md](PREMISSAS_PROJETO.md). A alimentação principal (+5V e GND) provém exclusivamente do receptor de rádio via **CON1 (CH6)** e o capacitor **C1** ($100\mu\text{F} \times 16\text{V}$) é obrigatório na entrada imediata da placa (Coluna 15, Linhas 14 e 15).

Para montar, calibrar e instalar com sucesso este sistema de iluminação em seu carro RC, você precisará de ferramentas básicas de eletrônica, habilidades manuais e materiais de proteção contra água e vibração.

### 🛠️ Ferramentas e Materiais Necessários

| Ferramenta / Material | Utilidade no Projeto | Importância |
|---|---|:---:|
| **Ferro de Solda (30W a 60W)** | Fazer as conexões elétricas permanentes na placa shield e chicotes. | **Indispensável** |
| **Estanho de Solda (com fluxo)** | Ligar eletricamente os fios, resistores e barras de pinos. | **Indispensável** |
| **Barras de Pinos Macho em 90° (Passo 2.54mm)** | Conectores CON1 (1x5), CON2 (1x4), CON3 (1x6) e CON4 (1x4) em 90° para fiação paralela à placa sem interferência com a bolha. | **Indispensável** |
| **Capacitor Eletrolítico ($100\mu\text{F} \times 16\text{V}$)** | Filtro e estabilização de entrada (C1) imediata do chicote do rádio (Col 04, Linhas 14-15). | **Indispensável** |
| **Tubo Termoretrátil (1.5mm a 5mm)**| Isolar emendas, derivações de GND e pernas expostas dos LEDs. | **Indispensável** |
| **Alicate de Corte e Descascador** | Cortar e expor a ponta metálica dos fios flexíveis. | **Indispensável** |
| **Alicate de Bico Fino ou de Crimpagem**| Cravar os terminais MODU fêmea nos fios da bolha. | **Indispensável** |
| **Multímetro Digital** | Medir continuidade (curtos) e conferir a polaridade dos LEDs. | **Altamente Recomendado** |
| **Graxa de Silicone Dielétrica / Vaselina**| Vedar os conectores MODU contra água, poeira e oxidação. | **Recomendado (Off-Road)**|
| **Fita de Alumínio Automotiva** | Fixar e ocultar os fios no teto/laterais da bolha. | **Recomendado** |
| **Silicone Neutro / Shoe Goo / E6000**| Fixar e vedar a traseira dos LEDs nos copos óticos da bolha.| **Recomendado** |
| **Verniz Isolante / Esmalte Incolor** | Proteger as trilhas e soldas no verso da placa shield e no MPU-6050. | **Recomendado** |

### 🧠 Habilidades Recomendadas

1. **Soldagem Eletrônica Básica:** Solde os resistores, capacitor C1 e as barras de pinos macho em 90° na placa perfurada de 5x7cm conforme o layout em [PLACA_SHIELD_LAYOUT.md](PLACA_SHIELD_LAYOUT.md). Aqueça a junção por 2 segundos antes de aplicar o estanho para obter uma solda brilhante e resistente à vibração.
2. **Identificação de Polaridade de Componentes:** LEDs possuem lado positivo (**Ânodo**, perna longa) e negativo (**Cátodo**, perna curta/chanfro). O capacitor eletrolítico C1 possui faixa indicando o polo negativo (-). Todos os negativos se unem no barramento de GND mestre unificado.
3. **Uso do Multímetro (Básico):** Meça a continuidade entre a trilha de 5V e o GND da placa shield antes de ligar no receptor. Se houver um "bipe", pare e remova o curto-circuito antes de energizar pelo CH6.
4. **Fixação Mecânica do Acelerômetro MPU-6050:** Fixe o módulo GY-521 com fita dupla face espumada (3M VHB) no chassi do carro para amortecer vibrações de alta frequência. O algoritmo vetorial 3D calibra a orientação automaticamente.

### 🔍 Resolução de Problemas (Troubleshooting)

- **O LED não acende:** Verifique se a polaridade do LED não está invertida, se o conector MODU está encaixado na posição correta ou se a solda do resistor está íntegra.
- **O Arduino não responde aos comandos do rádio:**
  - Verifique se o cabo do rádio (CON1) está plugado corretamente: **Pino 1 no VCC (+5V)** e **Pino 2 no GND** do canal **CH6** (conforme [PREMISSAS_PROJETO.md](PREMISSAS_PROJETO.md)).
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
  - Certifique-se de que o capacitor eletrolítico C1 ($100\mu\text{F} \times 16\text{V}$) está soldado exatamente na entrada de alimentação (Coluna 15, Linhas 14 e 15, ao lado do CON1 na lateral direita) para filtrar ruídos do ESC/motor e estabilizar o barramento de 5V.

---

## English

Please refer to [SKILLS_REQUIREMENTS.md](SKILLS_REQUIREMENTS.md) for the complete English documentation, tool lists, and troubleshooting steps.
