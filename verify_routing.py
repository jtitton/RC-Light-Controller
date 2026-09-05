"""
Script de Validação Automatizada de Roteamento — Shield Hub v7.2
Verifica matematicamente que nenhum pad da matriz de 18x24 é compartilhado
por duas redes elétricas distintas, garantindo ZERO curtos-circuitos.
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
    # CON1 (Rádio): Col 17, Rows 11 a 15
    assign_pad(17, 11, "CH1")
    assign_pad(17, 12, "CH4")
    assign_pad(17, 13, "CH2")
    assign_pad(17, 14, "GND")
    assign_pad(17, 15, "VCC")

    # Capacitor C1: Col 15, Rows 14 e 15
    assign_pad(15, 14, "GND")
    assign_pad(15, 15, "VCC")

    # CON4 (MPU-6050): Col 02, Rows 10 a 13
    assign_pad(2, 10, "SDA")
    assign_pad(2, 11, "SCL")
    assign_pad(2, 12, "VCC")
    assign_pad(2, 13, "GND")

    # Resistores R1-R3 Dianteiros: Rows 18 (Top) e 21 (Bot)
    assign_pad(4, 18, "D9")
    assign_pad(4, 21, "D9_out")
    assign_pad(5, 18, "D10")
    assign_pad(5, 21, "D10_out")
    assign_pad(6, 18, "D11")
    assign_pad(6, 21, "D11_out")

    # Resistores R7, R6, R5, R4 Traseiros: Rows 18 (Top) e 21 (Bot)
    assign_pad(8, 18, "D8")
    assign_pad(8, 21, "D8_out")
    assign_pad(9, 18, "D7")
    assign_pad(9, 21, "D7_out")
    assign_pad(10, 18, "D6")
    assign_pad(10, 21, "D6_out")
    assign_pad(11, 18, "D5")
    assign_pad(11, 21, "D5_out")

    # CON2 (Chicote Dianteiro): Row 24, Cols 03 a 06
    assign_pad(3, 24, "GND")
    assign_pad(4, 24, "D9_out")
    assign_pad(5, 24, "D10_out")
    assign_pad(6, 24, "D11_out")

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

    # 4. Trilhas de Solda do MPU-6050 (10mm face a face)
    assign_line((6, 10), (2, 10), "SDA")
    assign_line((6, 11), (2, 11), "SCL")

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
    # D11: corre pelo canal central livre Col 07 até R3 Top (06,18)
    assign_line((12, 4), (7, 4), "D11")
    assign_line((7, 4), (7, 17), "D11")
    assign_pad(6, 18, "D11")
    assign_line((6, 21), (6, 24), "D11_out")

    # Saídas de R1 e R2 para CON2
    assign_line((4, 21), (4, 24), "D9_out")
    assign_line((5, 21), (5, 24), "D10_out")

    # 7. Barramento GND Mestre
    # Tronco Direito: CON1 P2 (17,14) -> C1(-) (15,14) -> Nano GND Dir (12,14)
    assign_line((17, 14), (12, 14), "GND")
    # Canal Col 13 desce até CON3 P6 (13,24)
    assign_line((13, 14), (13, 24), "GND")
    # Tronco Esquerdo: Nano GND Esq (06,16) -> CON4 P1 (02,13)
    assign_line((6, 16), (2, 16), "GND")
    assign_line((2, 16), (2, 13), "GND")
    # Margem Col 01 até CON2 P1 (03,24)
    assign_line((2, 16), (1, 16), "GND")
    assign_line((1, 16), (1, 24), "GND")
    assign_line((1, 24), (3, 24), "GND")

    # 8. Linha +5V Mestre (Perimetral)
    # CON1 P1 (17,15) -> C1(+) (15,15)
    assign_line((17, 15), (15, 15), "VCC")
    # Margem Col 18 até Topo Lin 01
    assign_line((17, 15), (18, 15), "VCC")
    assign_line((18, 15), (18, 1), "VCC")
    assign_line((18, 1), (1, 1), "VCC")
    assign_line((1, 1), (1, 14), "VCC")
    # Ramal CON4 P2 (+5V)
    assign_line((1, 12), (2, 12), "VCC")

    # 9. Fios Isolados Superiores (Jumpers - conectam somente os 2 terminais)
    # Jumper 1: +5V de (01,14) para Nano +5V (06,14)
    assign_pad(1, 14, "VCC")
    assign_pad(6, 14, "VCC")

    # Jumper 2: Farol D9 de Nano D9 (12,06) para R1 Top (04,18)
    assign_pad(12, 6, "D9")
    assign_pad(4, 18, "D9")

    # Jumper 3: Pisca FE D10 de Nano D10 (12,05) para R2 Top (05,18)
    assign_pad(12, 5, "D10")
    assign_pad(5, 18, "D10")

    # Jumper 4: GND Cross-Tie de Nano GND Dir (12,14) para Nano GND Esq (06,16)
    assign_pad(12, 14, "GND")
    assign_pad(6, 16, "GND")

    # Relatório de Conflitos
    if conflicts:
        print(f"❌ FALHA: Foram encontrados {len(conflicts)} conflitos de pads:")
        for c, r, net1, net2 in conflicts:
            print(f"   Pad ({c:02d},{r:02d}): Rede '{net1}' em curto com '{net2}'")
        return False
    else:
        print("=" * 60)
        print("✅ SUCESSO: ZERO CONFLITOS DE PADS NA MATRIZ 18x24!")
        print("=" * 60)
        print(f"Total de pads ocupados com segurança: {len(grid)} / {18*24}")
        
        from collections import Counter
        counts = Counter(grid.values())
        print("\nDistribuição de Pads por Rede:")
        for net, count in counts.most_common():
            print(f"  • {net:10s}: {count:2d} pads")
        return True

if __name__ == "__main__":
    ok = verify_board_routing()
    sys.exit(0 if ok else 1)
