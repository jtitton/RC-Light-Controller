"""
Script de Validação Automatizada de Roteamento — Shield Hub v8.4
Verifica matematicamente que nenhum pad da matriz de 18x24 é compartilhado
por duas redes elétricas distintas, garantindo ZERO curtos-circuitos.
Arquitetura v8.4:
- Proteção e Regulação de Entrada D1 com Pitch Expandido (1N4007 DO-41 descendo na Col 17, Rows 15 a 18):
  * CON1 Pino 1 (+6.0V RAW BEC) entra no Pad (17, 15), isolado no verso.
  * Diodo desce verticalmente com pitch padrão DO-41 de 7,62 mm (3 passos) para o Pad (17, 18), gerando +5.25V.
  * Barramento VCC no verso da Linha 18 conecta (17, 18) a (15, 18).
  * Capacitor C1 (100µF x 25V) na Linha 18: C1(+) em (15, 18) e C1(-) em (14, 18), ligado a GND (13, 18).
  * Jumper W1 (+5.25V Nano 5V) sai de (15, 18) e Jumper W5 (+5.25V Coletor Q1) sai de (16, 18).
  * Pads (16, 15) e (15, 15) ficam 100% livres, criando mais de 7 mm de separação galvânica contra curtos.
- Driver de Transistor Q1 (BC337 NPN) no canal de Farol (D9) em High-Side Emitter Follower:
  * Coletor (Col 13, Linha 09) conectado a +5.25V via Jumper W5.
  * Base (Col 14, Linha 09) excitada por Nano D9 (12, 06).
  * Emissor (Col 15, Linha 09) alimenta R1 (27Ω) em (15, 08).
- Resistor R1 Farol (27Ω 1/4W): Montado verticalmente na Coluna 15 entre Linhas 08 e 06 (pitch 5,08mm).
- Resistores R2 a R7 padronizados em 100Ω (1/4W) para máxima intensidade luminosa segura.
- CON2 (Chicote Frente 1x4 90°) na Borda Superior Direita (Col 17, Linhas 04 a 07).
- CON4 (MPU-6050 1x4 90°) na Lateral Esquerda (Col 02, Linhas 10 a 13): P1 GND, P2 TX/SCL, P3 RX/SDA, P4 VCC.
- CON1 (Rádio 1x5 90°) na Lateral Direita (Col 17, Linhas 11 a 15).
- CON3 (Chicote Traseiro 1x6 90°) e R4-R7 na Borda Inferior (Linha 24 / Cols 08-13).
- 5 Jumpers Superiores Isolados (W1 +5V, W2 GND Frente, W3 GND Cross, W4 SDA/RX MPU, W5 +5V Farol).
"""
import sys
import io

# Ensure UTF-8 output on Windows consoles
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def verify_board_routing():
    grid = {}
    conflicts = []

    def assign_pad(c, r, net_name):
        pad = (c, r)
        if pad in grid:
            existing = grid[pad]
            if existing != net_name:
                conflicts.append((c, r, existing, net_name))
                return False
        grid[pad] = net_name
        return True

    def assign_line(p1, p2, net_name):
        c1, r1 = p1
        c2, r2 = p2
        if c1 == c2: # vertical
            step = 1 if r2 >= r1 else -1
            for r in range(r1, r2 + step, step):
                assign_pad(c1, r, net_name)
        elif r1 == r2: # horizontal
            step = 1 if c2 >= c1 else -1
            for c in range(c1, c2 + step, step):
                assign_pad(c, r1, net_name)
        else:
            print(f"ERRO: Linha não ortogonal: {p1} -> {p2}")
            return False
        return True

    # 1. Pinos Físicos do Arduino Nano (Pinagem Real docs.arduino.cc)
    # Left Header: Col 06, Rows 03 a 17
    left_pins = [
        (3, "D13"), (4, "3V3"), (5, "REF"), (6, "A0"), (7, "A1"), (8, "A2"), (9, "A3"),
        (10, "SDA"), (11, "SCL"), (12, "A6"), (13, "A7"), (14, "VCC"), (15, "RST"),
        (16, "GND"), (17, "VIN")
    ]
    for r, name in left_pins:
        assign_pad(6, r, name)

    # Right Header: Col 12, Rows 03 a 17
    right_pins = [
        (3, "D12"), (4, "D11"), (5, "D10"), (6, "D9"), (7, "D8"), (8, "D7"), (9, "D6"),
        (10, "D5"), (11, "CH1"), (12, "CH4"), (13, "CH2"), (14, "GND"), (15, "RST"),
        (16, "RX"), (17, "TX")
    ]
    for r, name in right_pins:
        assign_pad(12, r, name)

    # 2. Conectores e Componentes
    # CON1 (Rádio e Alimentação): Col 17, Rows 11 a 15
    assign_pad(17, 11, "CH1")
    assign_pad(17, 12, "CH4")
    assign_pad(17, 13, "CH2")
    assign_pad(17, 14, "GND")
    assign_pad(17, 15, "V_IN_BEC")  # Entrada +6.0V do BEC do ESC (v8.3)

    # Diodo D1 (1N4007 DO-41 v8.4): Col 17, Rows 15 a 18 (Pitch expandido de 7,62mm / 3 passos)
    # Anodo (+) em (17, 15) [V_IN_BEC]
    # Catodo (- faixa prateada) em (17, 18) [VCC +5.25V]
    assign_pad(17, 15, "V_IN_BEC")
    assign_pad(17, 18, "VCC")

    # Linha VCC Protegida na Linha 18 (Saída de D1 Cátodo em 17,18 -> W5 em 16,18 -> C1+ em 15,18)
    assign_line((17, 18), (15, 18), "VCC")

    # Capacitor C1 (100µF x 25V v8.4): Col 15 (+) e Col 14 (-), Row 18
    assign_pad(15, 18, "VCC")
    assign_pad(14, 18, "GND")

    # Ponte de solda GND C1(-): (14, 18) -> (13, 18) [Tronco GND Mestre Col 13]
    assign_line((14, 18), (13, 18), "GND")

    # CON4 (MPU-6050 v8.1/v8.2/v8.3): Col 02, Rows 10 a 13
    assign_pad(2, 10, "GND")
    assign_pad(2, 11, "SCL")
    assign_pad(2, 12, "SDA")
    assign_pad(2, 13, "VCC")

    # CON2 (Chicote Dianteiro): Col 17, Rows 04 a 07
    assign_pad(17, 7, "GND")
    assign_pad(17, 6, "D9_out")
    assign_pad(17, 5, "D10_out")
    assign_pad(17, 4, "D11_out")

    # Resistores R2 e R3 Dianteiros (100Ω): Cols 14 a 16, Rows 05 e 04
    # R2 (Pisca FE 100Ω): Lead 1 (14, 05) [D10 in], Lead 2 (16, 05) [D10_out]
    assign_pad(14, 5, "D10")
    assign_pad(16, 5, "D10_out")
    # R3 (Pisca FD 100Ω): Lead 1 (14, 04) [D11 in], Lead 2 (16, 04) [D11_out]
    assign_pad(14, 4, "D11")
    assign_pad(16, 4, "D11_out")

    # Driver de Transistor Q1 (BC337 NPN Farol v8.2/v8.3): Row 09, Cols 13 a 15
    # Pin 1: Coletor (13, 09) [VCC vindo de W5]
    # Pin 2: Base (14, 09) [D9 vindo de Nano D9]
    # Pin 3: Emissor (15, 09) [D9_emitter]
    assign_pad(13, 9, "VCC")
    assign_pad(14, 9, "D9")
    assign_pad(15, 9, "D9_emitter")

    # Resistor R1 Farol (27Ω 1/4W v8.2/v8.3): Col 15, Rows 08 a 06 (Vertical)
    # Lead 1: (15, 08) [D9_emitter]
    # Lead 2: (15, 06) [D9_out]
    assign_pad(15, 8, "D9_emitter")
    assign_pad(15, 6, "D9_out")

    # Resistores R7, R6, R5, R4 Traseiros (100Ω): Rows 18 (Top) e 21 (Bot)
    assign_pad(8, 18, "D8")
    assign_pad(8, 21, "D8_out")
    assign_pad(9, 18, "D7")
    assign_pad(9, 21, "D7_out")
    assign_pad(10, 18, "D6")
    assign_pad(10, 21, "D6_out")
    assign_pad(11, 18, "D5")
    assign_pad(11, 21, "D5_out")

    # CON3 (Chicote Traseiro): Row 24, Cols 08 a 13
    assign_pad(8, 24, "D8_out")
    assign_pad(9, 24, "D7_out")
    assign_pad(10, 24, "D6_out")
    assign_pad(11, 24, "D5_out")
    assign_pad(13, 24, "GND")

    # 3. Trilhas de Solda do Rádio (10mm face a face)
    assign_line((17, 11), (12, 11), "CH1")
    assign_line((17, 12), (12, 12), "CH4")
    assign_line((17, 13), (12, 13), "CH2")

    # 4. Trilhas de Solda do MPU-6050
    # P2 (TX / SCL): Trilha reta horizontal de 10mm para Nano A5 (Linha 11)
    assign_line((6, 11), (2, 11), "SCL")
    # P1 (GND): Ponte direta para o Barramento GND Coluna 01
    assign_line((2, 10), (1, 10), "GND")

    # 5. Trilhas de Solda dos LEDs Traseiros (Trilhas L aninhadas)
    assign_line((12, 7), (8, 7), "D8")
    assign_line((8, 7), (8, 18), "D8")
    assign_line((8, 21), (8, 24), "D8_out")

    assign_line((12, 8), (9, 8), "D7")
    assign_line((9, 8), (9, 18), "D7")
    assign_line((9, 21), (9, 24), "D7_out")

    assign_line((12, 9), (10, 9), "D6")
    assign_line((10, 9), (10, 18), "D6")
    assign_line((10, 21), (10, 24), "D6_out")

    assign_line((12, 10), (11, 10), "D5")
    assign_line((11, 10), (11, 18), "D5")
    assign_line((11, 21), (11, 24), "D5_out")

    # 6. Trilhas de Solda dos LEDs Dianteiros
    # R2 Pisca FE D10 (Row 05)
    assign_line((12, 5), (14, 5), "D10")
    assign_line((16, 5), (17, 5), "D10_out")
    # R3 Pisca FD D11 (Row 04)
    assign_line((12, 4), (14, 4), "D11")
    assign_line((16, 4), (17, 4), "D11_out")

    # Farol Driver v8.2/v8.3:
    # Base de Q1: Nano D9 (12, 06) -> (14, 06) -> (14, 09)
    assign_line((12, 6), (14, 6), "D9")
    assign_line((14, 6), (14, 9), "D9")

    # Emissor de Q1 -> R1 In: (15, 09) -> (15, 08)
    assign_line((15, 9), (15, 8), "D9_emitter")

    # R1 Out -> CON2 P2: (15, 6) -> (17, 6)
    assign_line((15, 6), (17, 6), "D9_out")

    # 7. Barramento GND Mestre
    # Tronco Direito: CON1 P2 (17,14) -> C1(-) (15,14) -> Nano GND Dir (12,14)
    assign_line((17, 14), (12, 14), "GND")
    # Canal Col 13 desce até CON3 P6 (13,24)
    assign_line((13, 14), (13, 24), "GND")
    # Tronco Esquerdo: Nano GND Esq (06,16) -> Barramento Coluna 01
    assign_line((6, 16), (1, 16), "GND")
    # Margem Col 01: Barramento Vertical GND unificado de Row 01 a Row 24
    assign_line((1, 1), (1, 24), "GND")
    # Ponte de terra para CON2 P1 (17, 07): Col 16 Lin 07 -> Col 17 Lin 07
    assign_line((16, 7), (17, 7), "GND")

    # 8. Linha VCC Protegida (Nano 5V -> CON4 P4)
    # Ramal de alimentação para CON4 P4 (Linha 13): Nano 5V (06,14) -> (05,14) -> (05,13) -> CON4 P4 (02,13)
    assign_line((6, 14), (5, 14), "VCC")
    assign_line((5, 14), (5, 13), "VCC")
    assign_line((5, 13), (2, 13), "VCC")

    # 9. Fios Isolados Superiores (5 Jumpers v8.4)
    # Jumper W1: +5.25V de C1(+) (15,18) para Nano 5V (06,14)
    assign_pad(15, 18, "VCC")
    assign_pad(6, 14, "VCC")

    # Jumper W2: GND Dianteiro de GND Mestre (16,14) para CON2 P1 (16,07)
    assign_pad(16, 14, "GND")
    assign_pad(16, 7, "GND")

    # Jumper W3: GND Cross-Tie de Nano GND Dir (12,14) para Nano GND Esq (06,16)
    assign_pad(12, 14, "GND")
    assign_pad(6, 16, "GND")

    # Jumper W4: SDA / RX de CON4 P3 (02,12) para Nano A4 (06,10)
    assign_pad(2, 12, "SDA")
    assign_pad(6, 10, "SDA")

    # Jumper W5: +5.25V Farol de Barramento VCC (16,18) para Q1 Coletor (13,09)
    assign_pad(16, 18, "VCC")
    assign_pad(13, 9, "VCC")

    # Relatório de Conflitos
    if conflicts:
        print(f"❌ FALHA: Foram encontrados {len(conflicts)} conflitos de pads:")
        for c, r, net1, net2 in conflicts:
            print(f"   Pad ({c:02d},{r:02d}): Rede '{net1}' em curto com '{net2}'")
        return False
    else:
        print("=" * 60)
        print("✅ SUCESSO: ZERO CONFLITOS DE PADS NA MATRIZ 18x24 (v8.4)!")
        print("=" * 60)
        print(f"Total de pads ocupados com segurança: {len(grid)} / {18*24}")
        
        from collections import Counter
        counts = Counter(grid.values())
        print("\nDistribuição de Pads por Rede:")
        for net, count in counts.most_common():
            print(f"  • {net:12s}: {count:2d} pads")
        return True

if __name__ == "__main__":
    ok = verify_board_routing()
    sys.exit(0 if ok else 1)
