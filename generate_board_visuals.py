"""
Gerador de Visualizações e Documentação Gráfica para Placa Shield RC v8.4
Layout Natural Distribuído com Pinagem Física Real do Arduino Nano:
1. Suporte Nativo a BEC 6.0V com Diodo Retificador D1 (1N4007) com Pitch Expandido:
   - Anodo (Col 17, Linha 15): Conectado diretamente a CON1 P1 (+6.0V BEC bruto do rádio).
   - Catodo (Col 17, Linha 18): Faixa prateada voltada para Linha 18, descendo reto pela Coluna 17 com pitch de 7,62 mm (3 passos).
   - Queda de tensão de ~0.75V: barramento seguro de +5.25V na Linha 18, com separação galvânica de 7,62 mm contra curtos.
   - Pads (16, 15) e (15, 15) ficam 100% livres e desocupados.
   - Barramento VCC na Linha 18 une (17, 18) a (15, 18), conectando C1(+), Jumper W1 (+5.25V Nano) e Jumper W5 (+5.25V Farol).
2. Orientação Real do Nano: Conector USB na borda superior externa (Linhas 01-02).
   - Lado Esquerdo (Col 06, Linhas 03 a 17): D13, 3V3, REF, A0, A1, A2, A3, A4 (SDA), A5 (SCL),
     A6, A7, 5V (Pin 27), RST, GND (Pin 29), VIN (Pin 30).
   - Lado Direito (Col 12, Linhas 03 a 17): D12, D11 (P.FD), D10 (P.FE), D9 (Farol), D8 (P.TD),
     D7 (P.TE), D6 (Freio), D5 (Lant), D4 (CH1), D3 (CH4), D2 (CH2), GND (Pin 04), RST, D0/RX, D1/TX.
3. Driver de Transistor Q1 (BC337 NPN) para Faróis Dianteiros (High-Side Emitter Follower):
   - Coletor (Col 13, Linha 09): Alimentado por +5.25V seguro via Jumper W5 (vindo de 16, 18).
   - Base (Col 14, Linha 09): Excitada por Nano D9 (Col 12, Linha 06) — drena apenas ~0.4mA.
   - Emissor (Col 15, Linha 09): Alimenta R1 (27Ω 1/4W vertical na Col 15, Linhas 06-08) ➔ CON2 P2 (Farol +).
   - Corrente nos 4 LEDs brancos em paralelo: ~45 a 60 mA (dobro de brilho!).
4. Resistores R2 a R7 Calibrados para 100Ω (1/4W):
   - Piscas FE/FD e TE/TD e Freio fornecem ~14.5 a 15 mA por LED (máximo brilho seguro).
5. Conectores Laterais em 90° Face a Face (Diretos na Borda!):
   - CON1 (Rádio): Lateral Direita (Col 17, Linhas 11 a 15).
   - D1 (1N4007): Coluna 17, Linhas 15 a 18 (Pitch 7,62 mm).
   - C1 (100uF x 25V): Colunas 14 e 15, Linha 18.
   - CON4 (MPU-6050): Lateral Esquerda (Col 02, Linhas 10 a 13) — P1 GND, P2 TX/SCL, P3 RX/SDA, P4 VCC.
   - CON2 (Chicote Frente): Lateral Superior Direita (Col 17, Linhas 04 a 07).
6. 5 Fios Isolados Superiores (Jumpers W1 a W5):
   - W1: +5.25V Protegido (C1+ 15,18 ➔ Nano 5V 06,14)
   - W2: GND Dianteiro (GND Mestre 16,14 ➔ CON2 P1 16,07)
   - W3: GND Cross-Tie (Nano GND Dir 12,14 ➔ Nano GND Esq 06,16)
   - W4: RX/SDA Acelerômetro (CON4 P3 02,12 ➔ Nano A4 06,10)
   - W5: +5.25V Farol (Barramento VCC 16,18 ➔ Q1 Coletor 13,09)
"""

import math

def generate_svg_top():
    cols = 18
    rows = 24
    pitch = 36
    margin_x = 90
    margin_y = 85
    board_w = (cols - 1) * pitch + margin_x * 2
    board_h = (rows - 1) * pitch + margin_y * 2 + 50

    def cx(c):
        return margin_x + (c - 1) * pitch

    def cy(r):
        return margin_y + (r - 1) * pitch

    svg = []
    svg.append(f'<svg id="svg-top-root" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {board_w} {board_h}" width="{board_w}" height="{board_h}" style="background:#090d14; font-family:\'Segoe UI\',system-ui,sans-serif;">')
    svg.append('<defs>')
    svg.append('''
      <linearGradient id="fr4Grad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#143d23"/>
        <stop offset="50%" stop-color="#0e2a18"/>
        <stop offset="100%" stop-color="#07190e"/>
      </linearGradient>
      <linearGradient id="nanoGrad" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stop-color="#0b5394"/>
        <stop offset="50%" stop-color="#083866"/>
        <stop offset="100%" stop-color="#052442"/>
      </linearGradient>
      <linearGradient id="usbGrad" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#bdc3c7"/>
        <stop offset="50%" stop-color="#ecf0f1"/>
        <stop offset="100%" stop-color="#95a5a6"/>
      </linearGradient>
      <linearGradient id="copperPad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#e6b800"/>
        <stop offset="50%" stop-color="#d4af37"/>
        <stop offset="100%" stop-color="#aa8800"/>
      </linearGradient>
      <linearGradient id="resistorBody" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#e8d5b5"/>
        <stop offset="40%" stop-color="#fdf3e2"/>
        <stop offset="100%" stop-color="#d1b894"/>
      </linearGradient>
      <linearGradient id="capGrad" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#2c3e50"/>
        <stop offset="60%" stop-color="#1a252f"/>
        <stop offset="100%" stop-color="#0d1318"/>
      </linearGradient>
      <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">
        <feDropShadow dx="2" dy="4" stdDeviation="3" flood-color="#000000" flood-opacity="0.6"/>
      </filter>
      <filter id="wireGlow" x="-20%" y="-20%" width="140%" height="140%">
        <feGaussianBlur stdDeviation="2" result="blur"/>
        <feComposite in="SourceGraphic" in2="blur" operator="over"/>
      </filter>
    ''')
    svg.append('</defs>')

    # PCB Base (FR4 Perfboard 5x7cm)
    pcb_x = margin_x - pitch/2
    pcb_y = margin_y - pitch/2
    pcb_w = (cols - 1) * pitch + pitch
    pcb_h = (rows - 1) * pitch + pitch
    svg.append(f'<rect x="{pcb_x}" y="{pcb_y}" width="{pcb_w}" height="{pcb_h}" rx="10" fill="url(#fr4Grad)" stroke="#1e6838" stroke-width="3" filter="url(#shadow)"/>')

    # Grid Lines (Dark subtle guide)
    for c in range(1, cols + 1):
        x = cx(c)
        svg.append(f'<line x1="{x}" y1="{cy(1)}" x2="{x}" y2="{cy(rows)}" stroke="#11331c" stroke-width="1" opacity="0.6"/>')
        svg.append(f'<text x="{x}" y="{pcb_y - 10}" text-anchor="middle" fill="#68d391" font-size="11" font-weight="bold">{c:02d}</text>')
        svg.append(f'<text x="{x}" y="{pcb_y + pcb_h + 22}" text-anchor="middle" fill="#68d391" font-size="11" font-weight="bold">{c:02d}</text>')

    for r in range(1, rows + 1):
        y = cy(r)
        svg.append(f'<line x1="{cx(1)}" y1="{y}" x2="{cx(cols)}" y2="{y}" stroke="#11331c" stroke-width="1" opacity="0.6"/>')
        svg.append(f'<text x="{margin_x - 30}" y="{y + 4}" text-anchor="middle" fill="#f1c40f" font-size="11">{r:02d}</text>')
        svg.append(f'<text x="{board_w - margin_x + 30}" y="{y + 4}" text-anchor="middle" fill="#f1c40f" font-size="11">{r:02d}</text>')

    # Copper pads grid
    for r in range(1, rows + 1):
        for c in range(1, cols + 1):
            x = cx(c)
            y = cy(r)
            svg.append(f'<circle cx="{x}" cy="{y}" r="5.5" fill="url(#copperPad)" stroke="#8c7300" stroke-width="0.8"/>')
            svg.append(f'<circle cx="{x}" cy="{y}" r="2.2" fill="#0d1912"/>')

    # =========================================================
    # ⚡ CAMADA DE FIAÇÃO E CONEXÕES VISÍVEIS NA FACE SUPERIOR
    # =========================================================
    def draw_top_wire(points, color, width, net_id, label=""):
        d_str = "M " + " L ".join([f"{p[0]} {p[1]}" for p in points])
        svg.append(f'<path class="track-line track-{net_id}" d="{d_str}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" opacity="0.85" filter="url(#wireGlow)"/>')
        if label and len(points) >= 2:
            mid_x = (points[0][0] + points[-1][0]) / 2
            mid_y = (points[0][1] + points[-1][1]) / 2
            svg.append(f'<text class="solder-lbl lbl-{net_id}" x="{mid_x}" y="{mid_y-5}" text-anchor="middle" fill="{color}" font-size="8" font-weight="bold" pointer-events="none">{label}</text>')

    def draw_top_jumper(points, color, width, net_id, label=""):
        d_str = "M " + " L ".join([f"{p[0]} {p[1]}" for p in points])
        svg.append(f'<path class="track-line track-{net_id} jumper-wire" d="{d_str}" fill="none" stroke="{color}" stroke-width="{width}" stroke-dasharray="6,4" stroke-linecap="round" stroke-linejoin="round" opacity="0.95" filter="url(#wireGlow)"/>')
        for p in [points[0], points[-1]]:
            svg.append(f'<circle cx="{p[0]}" cy="{p[1]}" r="4" fill="{color}" stroke="#ffffff" stroke-width="1.2"/>')
        if label and len(points) >= 2:
            mid_x = (points[0][0] + points[-1][0]) / 2
            mid_y = (points[0][1] + points[-1][1]) / 2
            svg.append(f'<rect x="{mid_x - 38}" y="{mid_y - 12}" width="76" height="14" rx="3" fill="#090d14" opacity="0.85"/>')
            svg.append(f'<text class="solder-lbl lbl-{net_id}" x="{mid_x}" y="{mid_y-2}" text-anchor="middle" fill="{color}" font-size="7.5" font-weight="bold" pointer-events="none">⚡ {label}</text>')

    svg.append('<g id="top-wiring-layer">')

    # 1. Linha de Alimentação Protegida (v8.4: CON1 P1 ➔ D1 1N4007 ➔ Barramento Linha 18 +5.25V ➔ Jumpers W1/W5)
    # Trilha VCC na Linha 18: (17, 18) ➔ (15, 18)
    draw_top_wire([(cx(17), cy(18)), (cx(15), cy(18))], "#ff4757", 5.0, "vcc", label="+5.25V Bus")
    # Ramal de alimentação para CON4 P4 (+5.25V MPU Linha 13): Nano 5V (06,14) ➔ (05,14) ➔ (05,13) ➔ CON4 P4 (02,13)
    vcc_mpu = [
        (cx(6), cy(14)),
        (cx(5), cy(14)),
        (cx(5), cy(13)),
        (cx(2), cy(13))
    ]
    draw_top_wire(vcc_mpu, "#ff4757", 4.2, "vcc", label="+5.25V MPU")

    # 2. Barramento GND Mestre Unificado
    # Tronco Direito: CON1 P2 (17,14) ➔ Nano GND Dir (12,14), desce canal livre Coluna 13 até CON3 P6 (13,24)
    gnd_top_dir = [
        (cx(17), cy(14)),  # CON1 P2 (GND Mestre do Rádio)
        (cx(12), cy(14)),  # Nano GND Dir (Pin 04)
        (cx(13), cy(14)),  # Tronco Coluna 13
        (cx(13), cy(24))   # CON3 P6 (GND Traseiro)
    ]
    draw_top_wire(gnd_top_dir, "#00d26a", 5.5, "gnd", label="GND Mestre (Do Rádio)")

    # Ponte de terra C1(-) na Linha 18 para Tronco Col 13
    draw_top_wire([(cx(14), cy(18)), (cx(13), cy(18))], "#00d26a", 5.0, "gnd", label="C1 GND")

    draw_top_wire([(cx(16), cy(7)), (cx(17), cy(7))], "#00d26a", 5.0, "gnd", label="GND")

    # Tronco Esquerdo de Terra: Nano GND Esq (06,16) ➔ Barramento Vertical Coluna 01
    draw_top_wire([(cx(6), cy(16)), (cx(1), cy(16))], "#00d26a", 5.0, "gnd")
    draw_top_wire([(cx(1), cy(1)), (cx(1), cy(24))], "#00d26a", 5.5, "gnd", label="Barramento GND (Col 01)")
    # Conexão de terra de CON4 P1 (GND Linha 10) ao Barramento Coluna 01
    draw_top_wire([(cx(2), cy(10)), (cx(1), cy(10))], "#00d26a", 5.0, "gnd", label="GND MPU")

    # 3. Sinais de Rádio (CON1 ➔ Nano Col 12): Trilhas 100% retas de 10mm na Lateral Direita!
    draw_top_wire([(cx(17), cy(11)), (cx(12), cy(11))], "#3498db", 3.8, "radio", label="CH1 (10mm)")
    draw_top_wire([(cx(17), cy(12)), (cx(12), cy(12))], "#2ecc71", 3.8, "radio", label="CH4 (10mm)")
    draw_top_wire([(cx(17), cy(13)), (cx(12), cy(13))], "#f39c12", 3.8, "radio", label="CH2 (10mm)")

    # 4. Sinais do Acelerômetro MPU-6050 (CON4 Linhas 10 a 13 - v8.1)
    # P2 (TX / SCL Linha 11): Trilha reta horizontal de 10mm para Nano A5
    draw_top_wire([(cx(6), cy(11)), (cx(2), cy(11))], "#ffd32a", 4.0, "i2c", label="TX / SCL (10mm)")

    # 5. Saídas dos LEDs Dianteiros (v8.0: Trilhas retas Nano ➔ R1..R3 ➔ CON2 na Lateral Direita!)
    # D11 Pisca FD (Row 04): Nano D11 (12,04) ➔ R3 In (14,04) e R3 Out (16,04) ➔ CON2 P4 (17,04)
    draw_top_wire([(cx(12), cy(4)), (cx(14), cy(4))], "#1e90ff", 3.6, "led-frente", label="D11")
    draw_top_wire([(cx(16), cy(4)), (cx(17), cy(4))], "#1e90ff", 5.0, "led-frente", label="Pis.FD")

    # D10 Pisca FE (Row 05): Nano D10 (12,05) ➔ R2 In (14,05) e R2 Out (16,05) ➔ CON2 P3 (17,05)
    draw_top_wire([(cx(12), cy(5)), (cx(14), cy(5))], "#ff9f1a", 3.6, "led-frente", label="D10")
    draw_top_wire([(cx(16), cy(5)), (cx(17), cy(5))], "#ff9f1a", 5.0, "led-frente", label="Pis.FE")

    # Farol v8.2 com Transistor Driver Q1 (BC337):
    # Nano D9 (12,06) -> Base Q1 (14,09) via trilha de solda:
    draw_top_wire([(cx(12), cy(6)), (cx(14), cy(6)), (cx(14), cy(9))], "#ffffff", 3.6, "led-frente", label="D9 (Base)")
    # Q1 Emissor (15,09) -> R1 In (15,08):
    draw_top_wire([(cx(15), cy(9)), (cx(15), cy(8))], "#ffffff", 4.0, "led-frente")
    # R1 Out (15,06) -> CON2 P2 (17,06):
    draw_top_wire([(cx(15), cy(6)), (cx(17), cy(6))], "#ffffff", 5.0, "led-frente", label="Farol")

    # 6. Saídas dos LEDs Traseiros (Nano Col 12 ➔ Trilhas em L Aninhadas ➔ Resistores R4-R7 ➔ CON3)
    # D8 Pisca TD: Col 12 Lin 7 -> Col 8 Lin 7 -> Col 8 Lin 18 (R7 Top)
    draw_top_wire([(cx(12), cy(7)), (cx(8), cy(7)), (cx(8), cy(18))], "#1e90ff", 3.0, "led-tras")
    draw_top_wire([(cx(8), cy(21)), (cx(8), cy(24))], "#1e90ff", 4.5, "led-tras", label="Pis.TD")

    # D7 Pisca TE: Col 12 Lin 8 -> Col 9 Lin 8 -> Col 9 Lin 18 (R6 Top)
    draw_top_wire([(cx(12), cy(8)), (cx(9), cy(8)), (cx(9), cy(18))], "#ffa502", 3.0, "led-tras")
    draw_top_wire([(cx(9), cy(21)), (cx(9), cy(24))], "#ffa502", 4.5, "led-tras", label="Pis.TE")

    # D6 Freio: Col 12 Lin 9 -> Col 10 Lin 9 -> Col 10 Lin 18 (R5 Top)
    draw_top_wire([(cx(12), cy(9)), (cx(10), cy(9)), (cx(10), cy(18))], "#ff4757", 3.0, "led-tras")
    draw_top_wire([(cx(10), cy(21)), (cx(10), cy(24))], "#ff4757", 4.5, "led-tras", label="Freio")

    # D5 Lanterna: Col 12 Lin 10 -> Col 11 Lin 10 -> Col 11 Lin 18 (R4 Top)
    draw_top_wire([(cx(12), cy(10)), (cx(11), cy(10)), (cx(11), cy(18))], "#ff7f50", 3.0, "led-tras")
    draw_top_wire([(cx(11), cy(21)), (cx(11), cy(24))], "#ff7f50", 4.5, "led-tras", label="Lant.")

    svg.append('</g>')

    # =========================================================
    # COMPONENTES FÍSICOS (ARDUINO NANO REAL, C1, RESISTORES, CONECTORES)
    # =========================================================

    # Arduino Nano Socket Body (Cols 6 a 12, Rows 3 a 17)
    nano_x = cx(6) - 10
    nano_y = cy(3) - 10
    nano_w = (12 - 6) * pitch + 20
    nano_h = (17 - 3) * pitch + 20
    svg.append(f'<rect x="{nano_x}" y="{nano_y}" width="{nano_w}" height="{nano_h}" rx="6" fill="url(#nanoGrad)" stroke="#1a5276" stroke-width="2.5" filter="url(#shadow)"/>')

    # Nano Mini-B/Type-C USB Connector (Voltado para Borda Superior Externa: Linhas 01-02)
    usb_w = 44
    usb_h = 24
    usb_x = (cx(6) + cx(12)) / 2 - usb_w / 2
    usb_y = nano_y - 12
    svg.append(f'<rect x="{usb_x}" y="{usb_y}" width="{usb_w}" height="{usb_h}" rx="3" fill="url(#usbGrad)" stroke="#7f8c8d" stroke-width="1.5" filter="url(#shadow)"/>')
    svg.append(f'<text x="{usb_x + usb_w/2}" y="{usb_y + 15}" text-anchor="middle" fill="#2c3e50" font-size="9" font-weight="bold">USB NANO</text>')

    # Nano Silkscreen text
    svg.append(f'<text x="{(cx(6)+cx(12))/2}" y="{cy(3)+20}" text-anchor="middle" fill="#ffffff" font-size="12" font-weight="bold" letter-spacing="1">ARDUINO NANO V3</text>')
    svg.append(f'<text x="{(cx(6)+cx(12))/2}" y="{cy(4)+8}" text-anchor="middle" fill="#85c1e9" font-size="8.5">(Pinagem Física Real: docs.arduino.cc)</text>')

    # PINAGEM FÍSICA REAL DO NANO (USB NO TOPO):
    # Left Header: D13 no topo (Lin 03) até VIN na base (Lin 17)
    left_pins = [
        ("D13", "#bdc3c7"),
        ("3V3", "#bdc3c7"),
        ("REF", "#bdc3c7"),
        ("A0", "#bdc3c7"),
        ("A1", "#bdc3c7"),
        ("A2", "#bdc3c7"),
        ("A3", "#bdc3c7"),
        ("A4 (SDA)", "#2ed573"),
        ("A5 (SCL)", "#ffd32a"),
        ("A6", "#bdc3c7"),
        ("A7", "#bdc3c7"),
        ("5V", "#ff4757"),
        ("RST", "#e74c3c"),
        ("GND", "#00d26a"),
        ("VIN", "#e74c3c")
    ]
    for i, (name, col) in enumerate(left_pins):
        r = 3 + i
        svg.append(f'<text x="{cx(6)-14}" y="{cy(r)+3}" text-anchor="end" fill="{col}" font-size="8" font-weight="bold">{name}</text>')

    # Right Header: D12 no topo (Lin 03) até D1/TX na base (Lin 17)
    right_pins = [
        ("D12", "#bdc3c7"),
        ("D11 (P.FD)", "#3498db"),
        ("D10 (P.FE)", "#f39c12"),
        ("D9 (Farol)", "#ffffff"),
        ("D8 (P.TD)", "#3498db"),
        ("D7 (P.TE)", "#f39c12"),
        ("D6 (Freio)", "#e74c3c"),
        ("D5 (Lant)", "#e67e22"),
        ("D4 (CH1)", "#3498db"),
        ("D3 (CH4)", "#2ecc71"),
        ("D2 (CH2)", "#f39c12"),
        ("GND", "#00d26a"),
        ("RST", "#e74c3c"),
        ("D0/RX", "#bdc3c7"),
        ("D1/TX", "#bdc3c7")
    ]
    for i, (name, col) in enumerate(right_pins):
        r = 3 + i
        svg.append(f'<text x="{cx(12)+14}" y="{cy(r)+3}" text-anchor="start" fill="{col}" font-size="8" font-weight="bold">{name}</text>')

    # Helper: draw resistor
    def draw_resistor(col, r_top, r_bot, label, bands):
        x = cx(col)
        y1 = cy(r_top)
        y2 = cy(r_bot)
        rw = 16
        rh = (y2 - y1) * 0.52
        ry = (y1 + y2) / 2 - rh / 2
        # Leads
        svg.append(f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{ry}" stroke="#95a5a6" stroke-width="2"/>')
        svg.append(f'<line x1="{x}" y1="{ry+rh}" x2="{x}" y2="{y2}" stroke="#95a5a6" stroke-width="2"/>')
        # Body
        svg.append(f'<rect x="{x-rw/2}" y="{ry}" width="{rw}" height="{rh}" rx="4" fill="url(#resistorBody)" stroke="#b89770" stroke-width="1.2" filter="url(#shadow)"/>')
        # Color bands
        band_y = ry + 4
        band_h = 3
        for b_col in bands:
            svg.append(f'<rect x="{x-rw/2}" y="{band_y}" width="{rw}" height="{band_h}" fill="{b_col}"/>')
            band_y += band_h + 3
        # Label
        svg.append(f'<text x="{x}" y="{ry+rh/2+3}" text-anchor="middle" fill="#2c3e50" font-size="7" font-weight="bold">{label}</text>')

    # Helper: draw horizontal resistor
    def draw_resistor_h(row, c_left, c_right, label, bands):
        y = cy(row)
        x1 = cx(c_left)
        x2 = cx(c_right)
        rh = 14
        rw = (x2 - x1) * 0.52
        rx = (x1 + x2) / 2 - rw / 2
        # Leads
        svg.append(f'<line x1="{x1}" y1="{y}" x2="{rx}" y2="{y}" stroke="#95a5a6" stroke-width="2"/>')
        svg.append(f'<line x1="{rx+rw}" y1="{y}" x2="{x2}" y2="{y}" stroke="#95a5a6" stroke-width="2"/>')
        # Body
        svg.append(f'<rect x="{rx}" y="{y-rh/2}" width="{rw}" height="{rh}" rx="4" fill="url(#resistorBody)" stroke="#b89770" stroke-width="1.2" filter="url(#shadow)"/>')
        # Color bands (vertical stripes)
        band_x = rx + 6
        band_w = 3.5
        for b_col in bands:
            svg.append(f'<rect x="{band_x}" y="{y-rh/2}" width="{band_w}" height="{rh}" fill="{b_col}"/>')
            band_x += band_w + 3.5
        # Label
        svg.append(f'<text x="{(x1+x2)/2}" y="{y-9}" text-anchor="middle" fill="#ecf0f1" font-size="7.5" font-weight="bold">{label}</text>')

    # Front Resistors R3 (Row 04) e R2 (Row 05) Horizontais (100Ω 1/4W)
    draw_resistor_h(4, 14, 16, "R3 100Ω", ["#795548", "#000000", "#795548", "#f1c40f"])
    svg.append(f'<text x="{cx(15)}" y="{cy(4)+14}" text-anchor="middle" fill="#3498db" font-size="7.5" font-weight="bold">Pis.FD</text>')

    draw_resistor_h(5, 14, 16, "R2 100Ω", ["#795548", "#000000", "#795548", "#f1c40f"])
    svg.append(f'<text x="{cx(15)}" y="{cy(5)+14}" text-anchor="middle" fill="#f39c12" font-size="7.5" font-weight="bold">Pis.FE</text>')

    # Resistor R1 Farol (Vertical: Coluna 15, Linhas 06 a 08 — 27Ω 1/4W: Vermelho, Violeta, Preto, Ouro)
    draw_resistor(15, 6, 8, "R1 27Ω", ["#e74c3c", "#8e44ad", "#000000", "#f1c40f"])
    svg.append(f'<text x="{cx(15)+20}" y="{cy(7)+3}" text-anchor="start" fill="#ffffff" font-size="7.5" font-weight="bold">Farol</text>')

    # ==========================
    # TRANSISTOR Q1: BC337 NPN DRIVER FAROL (Linha 09, Colunas 13 a 15) TO-92
    # Face reta voltada para o Sul (Linha 24), arco arredondado para o Norte (Linha 01)
    # ==========================
    q1_cx = cx(14)
    q1_cy = cy(9)
    # Terminais de solda saindo do corpo
    svg.append(f'<line x1="{cx(13)}" y1="{cy(9)}" x2="{cx(13)}" y2="{cy(9)+7}" stroke="#95a5a6" stroke-width="2.5"/>')
    svg.append(f'<line x1="{cx(14)}" y1="{cy(9)}" x2="{cx(14)}" y2="{cy(9)+7}" stroke="#95a5a6" stroke-width="2.5"/>')
    svg.append(f'<line x1="{cx(15)}" y1="{cy(9)}" x2="{cx(15)}" y2="{cy(9)+7}" stroke="#95a5a6" stroke-width="2.5"/>')

    # Corpo D-shape do TO-92
    svg.append(f'<path d="M {q1_cx-26} {q1_cy+7} L {q1_cx+26} {q1_cy+7} A 26 20 0 0 0 {q1_cx-26} {q1_cy+7} Z" fill="url(#capGrad)" stroke="#1a252f" stroke-width="1.8" filter="url(#shadow)"/>')
    svg.append(f'<text x="{q1_cx}" y="{q1_cy-2}" text-anchor="middle" fill="#ffffff" font-size="8" font-weight="bold">BC337</text>')
    svg.append(f'<text x="{q1_cx}" y="{q1_cy+5}" text-anchor="middle" fill="#2ed573" font-size="6" font-weight="bold">Q1 Driver</text>')
    # Rótulos dos pinos
    svg.append(f'<text x="{cx(13)}" y="{cy(9)+18}" text-anchor="middle" fill="#ff4757" font-size="7" font-weight="bold">C (W5)</text>')
    svg.append(f'<text x="{cx(14)}" y="{cy(9)+18}" text-anchor="middle" fill="#ffffff" font-size="7" font-weight="bold">B (D9)</text>')
    svg.append(f'<text x="{cx(15)}" y="{cy(9)+18}" text-anchor="middle" fill="#2ed573" font-size="7" font-weight="bold">E (R1)</text>')

    # Rear Resistors R7, R6, R5, R4 (Cols 8, 9, 10, 11, Rows 18-21, 100Ω 1/4W)
    draw_resistor(8, 18, 21, "R7 100Ω", ["#795548", "#000000", "#795548", "#f1c40f"])
    svg.append(f'<text x="{cx(8)}" y="{cy(22)+4}" text-anchor="middle" fill="#3498db" font-size="8" font-weight="bold">Pis.TD</text>')

    draw_resistor(9, 18, 21, "R6 100Ω", ["#795548", "#000000", "#795548", "#f1c40f"])
    svg.append(f'<text x="{cx(9)}" y="{cy(22)+4}" text-anchor="middle" fill="#f39c12" font-size="8" font-weight="bold">Pis.TE</text>')

    draw_resistor(10, 18, 21, "R5 100Ω", ["#795548", "#000000", "#795548", "#f1c40f"])
    svg.append(f'<text x="{cx(10)}" y="{cy(22)+4}" text-anchor="middle" fill="#ff4757" font-size="8" font-weight="bold">Freio</text>')

    draw_resistor(11, 18, 21, "R4 100Ω", ["#795548", "#000000", "#795548", "#f1c40f"])
    svg.append(f'<text x="{cx(11)}" y="{cy(22)+4}" text-anchor="middle" fill="#e67e22" font-size="8" font-weight="bold">Lant.</text>')

    # ==========================
    # CAPACITOR C1 DE FILTRO / REGULAÇÃO (Coluna 15 (+) e Coluna 14 (-), Linha 18) - v8.4
    # POSICIONADO COM FOLGA NA LINHA 18 COM POLO NEGATIVO DIRETO NO GND DA COLUNA 13!
    # ==========================
    cap_cx = (cx(14) + cx(15)) / 2
    cap_cy = cy(18)
    cap_r = 15

    # Pernas de conexão do capacitor
    svg.append(f'<line x1="{cx(15)}" y1="{cy(18)}" x2="{cap_cx+cap_r-2}" y2="{cap_cy}" stroke="#ff4757" stroke-width="2.5"/>')
    svg.append(f'<line x1="{cx(14)}" y1="{cy(18)}" x2="{cap_cx-cap_r+2}" y2="{cap_cy}" stroke="#00d26a" stroke-width="2.5"/>')

    # Corpo cilíndrico do capacitor
    svg.append(f'<circle cx="{cap_cx}" cy="{cap_cy}" r="{cap_r}" fill="url(#capGrad)" stroke="#ff4757" stroke-width="1.8" filter="url(#shadow)"/>')
    # Faixa branca indicadora do polo negativo (GND na coluna 14)
    svg.append(f'<path d="M {cap_cx-6} {cap_cy-cap_r+4} A {cap_r} {cap_r} 0 0 0 {cap_cx-6} {cap_cy+cap_r-4} L {cap_cx-cap_r+1} {cap_cy+cap_r-2} A {cap_r} {cap_r} 0 0 1 {cap_cx-cap_r+1} {cap_cy-cap_r+2} Z" fill="#ecf0f1"/>')
    svg.append(f'<text x="{cap_cx-7}" y="{cap_cy+3}" fill="#000" font-size="8" font-weight="bold" text-anchor="middle">-</text>')
    # Texto C1 e valor
    svg.append(f'<text x="{cap_cx+4}" y="{cap_cy-2}" fill="#ecf0f1" font-size="7" font-weight="bold" text-anchor="middle">C1 Filtro</text>')
    svg.append(f'<text x="{cap_cx+4}" y="{cap_cy+7}" fill="#ffd32a" font-size="6.5" font-weight="bold" text-anchor="middle">100µF 25V</text>')
    svg.append(f'<text x="{cx(14)}" y="{cy(18)+24}" fill="#00d26a" font-size="7.5" font-weight="bold" text-anchor="middle">C1 (-)</text>')
    svg.append(f'<text x="{cx(15)}" y="{cy(18)+24}" fill="#ff4757" font-size="7.5" font-weight="bold" text-anchor="middle">C1 (+)</text>')

    # ==========================
    # DIODO D1: 1N4007 RETIFICADOR / REGULADOR DE TENSÃO BEC 6.0V (Coluna 17, Linhas 15 a 18) DO-41 - v8.4
    # Pitch de 7,62 mm (3 passos) descendo pela Coluna 17!
    # Anodo na Linha 15 (Pad 17, 15 - CON1 P1 +6.0V BEC)
    # Catodo (Faixa Prateada) na Linha 18 (Pad 17, 18 - Barramento VCC +5.25V)
    # ==========================
    d1_x = cx(17)
    d1_y_anode = cy(15)
    d1_y_cathode = cy(18)
    d1_body_w = 14
    d1_body_h = 44
    d1_cy = (d1_y_anode + d1_y_cathode) / 2
    d1_ry = d1_cy - d1_body_h / 2

    # Terminais de solda do diodo D1 (verticais)
    svg.append(f'<line x1="{d1_x}" y1="{d1_y_anode}" x2="{d1_x}" y2="{d1_ry}" stroke="#95a5a6" stroke-width="2.2"/>')
    svg.append(f'<line x1="{d1_x}" y1="{d1_ry + d1_body_h}" x2="{d1_x}" y2="{d1_y_cathode}" stroke="#95a5a6" stroke-width="2.2"/>')

    # Corpo cilíndrico preto do encapsulamento DO-41
    svg.append(f'<rect x="{d1_x - d1_body_w/2}" y="{d1_ry}" width="{d1_body_w}" height="{d1_body_h}" rx="3" fill="#1c2833" stroke="#2c3e50" stroke-width="1.2" filter="url(#shadow)"/>')

    # Faixa prateada do catodo (voltada para baixo / Linha 18)
    svg.append(f'<rect x="{d1_x - d1_body_w/2}" y="{d1_ry + d1_body_h - 7}" width="{d1_body_w}" height="5" fill="#ecf0f1" stroke="#bdc3c7" stroke-width="0.5"/>')

    # Texto D1 1N4007 (vertical)
    svg.append(f'<text x="{d1_x}" y="{d1_cy - 4}" text-anchor="middle" fill="#f1c40f" font-size="7" font-weight="bold" transform="rotate(-90 {d1_x} {d1_cy - 4})">1N4007</text>')
    svg.append(f'<text x="{d1_x + 28}" y="{d1_cy}" text-anchor="start" fill="#ffd32a" font-size="7.5" font-weight="bold">D1 (-0.75V)</text>')
    svg.append(f'<text x="{d1_x + 28}" y="{d1_cy + 10}" text-anchor="start" fill="#95a5a6" font-size="6.5">Pitch 7.62mm</text>')
    svg.append(f'<text x="{d1_x + 18}" y="{d1_y_anode + 3}" text-anchor="start" fill="#ff4757" font-size="7.5" font-weight="bold">A (+6.0V)</text>')
    svg.append(f'<text x="{d1_x + 18}" y="{d1_y_cathode + 3}" text-anchor="start" fill="#2ed573" font-size="7.5" font-weight="bold">K (+5.25V)</text>')

    # ==========================
    # CON1: RÁDIO (Lateral Direita - Coluna 17, Linhas 11 a 15) 90° Apontando para Direita!
    # ENTRADA PRINCIPAL DE VCC (+6.0V) E GND DO CARRO!
    # ==========================
    con1_x = cx(17) - 12
    con1_y = cy(11) - 12
    con1_w = 24
    con1_h = 4 * pitch + 24
    svg.append(f'<rect x="{con1_x}" y="{con1_y}" width="{con1_w}" height="{con1_h}" rx="3" fill="#1c2833" stroke="#ff4757" stroke-width="2.2" filter="url(#shadow)"/>')
    svg.append(f'<text x="{con1_x+con1_w+8}" y="{con1_y + con1_h/2}" text-anchor="middle" fill="#ff4757" font-size="9" font-weight="bold" transform="rotate(90 {con1_x+con1_w+8} {con1_y + con1_h/2})">CON1: RÁDIO / ENTRADA BEC (90°)</text>')

    con1_pins = [
        (11, "CH1 (Dir)", "#3498db", "P5"),
        (12, "CH4 (Farol)", "#2ecc71", "P4"),
        (13, "CH2 (Thr)", "#f39c12", "P3"),
        (14, "GND (Mestre)", "#00d26a", "P2"),
        (15, "+6.0V BEC (D1)", "#ff4757", "P1")
    ]
    for r, pname, pcolor, pnum in con1_pins:
        px = cx(17)
        py = cy(r)
        svg.append(f'<circle cx="{px}" cy="{py}" r="4.5" fill="#f1c40f" stroke="#000" stroke-width="1.2"/>')
        # 90 deg pin pointing right
        svg.append(f'<rect x="{px}" y="{py-2.5}" width="35" height="5" rx="1" fill="#f1c40f" stroke="#b7950b" stroke-width="0.8" filter="url(#shadow)"/>')
        svg.append(f'<text x="{px+42}" y="{py+3}" text-anchor="start" fill="{pcolor}" font-size="8.5" font-weight="bold">{pname}</text>')

    # ==========================
    # CON2: CHICOTE DIANTEIRO (Lateral Superior Direita - Coluna 17, Linhas 04 a 07 - v8.0) 90° Apontando para Direita!
    # ==========================
    con2_x = cx(17) - 12
    con2_y = cy(4) - 12
    con2_w = 24
    con2_h = 3 * pitch + 24
    svg.append(f'<rect x="{con2_x}" y="{con2_y}" width="{con2_w}" height="{con2_h}" rx="3" fill="#1c2833" stroke="#2ecc71" stroke-width="1.8" filter="url(#shadow)"/>')
    svg.append(f'<text x="{con2_x+con2_w+8}" y="{con2_y + con2_h/2}" text-anchor="middle" fill="#2ecc71" font-size="9" font-weight="bold" transform="rotate(90 {con2_x+con2_w+8} {con2_y + con2_h/2})">CON2: FRENTE (1x4 90°)</text>')

    con2_pins = [
        (4, "Pis.FD", "#3498db", "P4"),
        (5, "Pis.FE", "#f39c12", "P3"),
        (6, "Farol", "#ffffff", "P2"),
        (7, "GND", "#00d26a", "P1")
    ]
    for r, pname, pcolor, pnum in con2_pins:
        px = cx(17)
        py = cy(r)
        svg.append(f'<circle cx="{px}" cy="{py}" r="4.5" fill="#f1c40f" stroke="#000" stroke-width="1.2"/>')
        # 90 deg pin pointing right
        svg.append(f'<rect x="{px}" y="{py-2.5}" width="35" height="5" rx="1" fill="#f1c40f" stroke="#b7950b" stroke-width="0.8" filter="url(#shadow)"/>')
        svg.append(f'<text x="{px+42}" y="{py+3}" text-anchor="start" fill="{pcolor}" font-size="8.5" font-weight="bold">{pname}</text>')

    # ==========================
    # CON4: MPU-6050 (Lateral Esquerda - Coluna 02, Linhas 10 a 13) 90° Apontando para Esquerda!
    # ==========================
    con4_x = cx(2) - 12
    con4_y = cy(10) - 12
    con4_w = 24
    con4_h = 3 * pitch + 24
    svg.append(f'<rect x="{con4_x}" y="{con4_y}" width="{con4_w}" height="{con4_h}" rx="3" fill="#1c2833" stroke="#f1c40f" stroke-width="1.8" filter="url(#shadow)"/>')
    svg.append(f'<text x="{con4_x-8}" y="{con4_y + con4_h/2}" text-anchor="middle" fill="#f1c40f" font-size="9" font-weight="bold" transform="rotate(-90 {con4_x-8} {con4_y + con4_h/2})">CON4: MPU (1x4 90°)</text>')

    con4_pins = [
        (10, "GND", "#00d26a", "P1"),
        (11, "TX (SCL)", "#ffd32a", "P2"),
        (12, "RX (SDA)", "#2ed573", "P3"),
        (13, "VCC (+5V)", "#ff4757", "P4")
    ]
    for r, pname, pcolor, pnum in con4_pins:
        px = cx(2)
        py = cy(r)
        svg.append(f'<circle cx="{px}" cy="{py}" r="4.5" fill="#f1c40f" stroke="#000" stroke-width="1.2"/>')
        # 90 deg pin pointing left
        svg.append(f'<rect x="{px-35}" y="{py-2.5}" width="35" height="5" rx="1" fill="#f1c40f" stroke="#b7950b" stroke-width="0.8" filter="url(#shadow)"/>')
        svg.append(f'<text x="{px-42}" y="{py+3}" text-anchor="end" fill="{pcolor}" font-size="8.5" font-weight="bold">{pname}</text>')

    # ==========================
    # CON3: CHICOTE TRASEIRO (Linha 24, Colunas 8 a 13) 90° Apontando para Baixo!
    # ==========================
    con3_x = cx(8) - 12
    con3_y = cy(24) - 12
    con3_w = 5 * pitch + 24
    con3_h = 24
    svg.append(f'<rect x="{con3_x}" y="{con3_y}" width="{con3_w}" height="{con3_h}" rx="3" fill="#1c2833" stroke="#e67e22" stroke-width="1.8" filter="url(#shadow)"/>')
    svg.append(f'<text x="{con3_x + con3_w/2}" y="{con3_y + 16}" text-anchor="middle" fill="#e67e22" font-size="9" font-weight="bold">CON3: TRÁS (1x6 90°)</text>')

    con3_pins = [
        (8, "Pis.TD", "#3498db", "P1"),
        (9, "Pis.TE", "#f39c12", "P2"),
        (10, "Freio", "#ff4757", "P3"),
        (11, "Lant.", "#e67e22", "P4"),
        (12, "NC", "#7f8c8d", "P5"),
        (13, "GND", "#00d26a", "P6")
    ]
    for c, pname, pcolor, pnum in con3_pins:
        px = cx(c)
        py = cy(24)
        svg.append(f'<circle cx="{px}" cy="{py}" r="4.5" fill="#f1c40f" stroke="#000" stroke-width="1.2"/>')
        svg.append(f'<rect x="{px-2.5}" y="{py}" width="5" height="35" rx="1" fill="#f1c40f" stroke="#b7950b" stroke-width="0.8" filter="url(#shadow)"/>')
        svg.append(f'<text x="{px}" y="{py+48}" text-anchor="middle" fill="{pcolor}" font-size="8" font-weight="bold">{pname}</text>')

    # =========================================================
    # ⚡ CAMADA DE JUMPERS SUPERIORES ISOLADOS (W1 A W5 - v8.4)
    # Renderizados no topo dos componentes para 100% de visibilidade!
    # =========================================================
    svg.append('<g id="top-jumpers-layer">')
    # Jumper W1 (+5.25V Protegido): C1(+) / W1 (15,18) ➔ Nano 5V (06,14)
    draw_top_jumper([(cx(15), cy(18)), (cx(6), cy(14))], "#ff4757", 4.0, "vcc", label="W1 (+5.25V)")
    # Jumper W2 (GND Dianteiro): GND Mestre (16,14) ➔ CON2 P1 (16,07)
    draw_top_jumper([(cx(16), cy(14)), (cx(16), cy(7))], "#00d26a", 3.8, "gnd", label="W2 (GND Frente)")
    # Jumper W3 (GND Cross-Tie): Nano GND Dir (12,14) ➔ Nano GND Esq (06,16)
    draw_top_jumper([(cx(12), cy(14)), (cx(6), cy(16))], "#00d26a", 3.8, "gnd", label="W3 (GND Cross)")
    # Jumper W4 (RX/SDA Acelerômetro): CON4 P3 (02,12) ➔ Nano A4 (06,10)
    draw_top_jumper([(cx(2), cy(12)), (cx(6), cy(10))], "#2ed573", 4.0, "i2c", label="W4 (RX/SDA)")
    # Jumper W5 (+5.25V Farol): Barramento VCC (16,18) ➔ Q1 Coletor (13,09)
    draw_top_jumper([(cx(16), cy(18)), (cx(13), cy(9))], "#ff4757", 3.8, "vcc", label="W5 (+5.25V Farol)")
    svg.append('</g>')

    # Board Title and Version Legend
    svg.append(f'<text x="{board_w/2}" y="{pcb_y - 45}" text-anchor="middle" fill="#ecf0f1" font-size="16" font-weight="bold">PLACA SHIELD HUB 5x7cm — VISTA SUPERIOR (COMPONENTES &amp; FIAÇÃO)</text>')
    svg.append(f'<text x="{board_w/2}" y="{pcb_y - 25}" text-anchor="middle" fill="#00d26a" font-size="11">Layout Natural Distribuído v8.4 — Suporte BEC 6.0V (D1 1N4007 Pitch 7.62mm) &amp; Driver Farol BC337</text>')

    svg.append('</svg>')
    return "".join(svg)


def generate_svg_bottom_solder():
    cols = 18
    rows = 24
    pitch = 36
    margin_x = 90
    margin_y = 85
    board_w = (cols - 1) * pitch + margin_x * 2
    board_h = (rows - 1) * pitch + margin_y * 2 + 50

    # Horizontal mirror: Column c becomes (cols - c + 1)
    def cx(c):
        mirrored_c = cols - c + 1
        return margin_x + (mirrored_c - 1) * pitch

    def cy(r):
        return margin_y + (r - 1) * pitch

    solder_pads_data = {
        # Nano Left Header (Pinagem Real: D13..VIN na Coluna 06. Espelhado: fica no lado direito visual)
        (6, 3):   ("mech", "D13", "Nano D13 (SCK)", "Pino 16 do Nano"),
        (6, 4):   ("mech", "3V3", "Nano 3V3", "Pino 17 do Nano"),
        (6, 5):   ("mech", "REF", "Nano AREF", "Pino 18 do Nano"),
        (6, 6):   ("mech", "A0", "Nano A0", "Pino 19 do Nano"),
        (6, 7):   ("mech", "A1", "Nano A1", "Pino 20 do Nano"),
        (6, 8):   ("mech", "A2", "Nano A2", "Pino 21 do Nano"),
        (6, 9):   ("mech", "A3", "Nano A3", "Pino 22 do Nano"),
        (6, 10):  ("i2c", "A4", "Nano A4 (SDA)", "Terminal do Jumper W4 (RX/SDA vindo de CON4 P3 Linha 12)"),
        (6, 11):  ("i2c", "A5", "Nano A5 (SCL)", "Trilha direta horizontal de 10mm para CON4 P2 TX/SCL (Linha 11)"),
        (6, 12):  ("mech", "A6", "Nano A6", "Pino 25 do Nano"),
        (6, 13):  ("mech", "A7", "Nano A7", "Pino 26 do Nano"),
        (6, 14):  ("vcc", "+5V", "Nano +5V (Pin 27)", "Terminal do Jumper W1 (+5V) e início do ramal para CON4 P4 (Linha 13)"),
        (6, 15):  ("mech", "RST", "Nano RST", "Pino 28 do Nano"),
        (6, 16):  ("gnd", "GND", "Nano GND Esq (Pin 29)", "Barramento GND Esquerdo & Terminal Jumper W3 GND Cross-Tie"),
        (6, 17):  ("mech", "VIN", "Nano VIN", "Pino 30 do Nano (desconectado)"),

        # Nano Right Header (Pinagem Real: D12..D1/TX na Coluna 12. Espelhado: fica no lado esquerdo visual)
        (12, 3):  ("mech", "D12", "Nano D12 (MISO)", "Pino 15 do Nano"),
        (12, 4):  ("led-frente", "D11", "Nano D11 (Pis.FD)", "Saída para R3 In via trilha direta 5mm (Col 14 Lin 04)"),
        (12, 5):  ("led-frente", "D10", "Nano D10 (Pis.FE)", "Saída para R2 In via trilha direta 5mm (Col 14 Lin 05)"),
        (12, 6):  ("led-frente", "D9", "Nano D9 (Farol)", "Saída para R1 In via trilha direta 5mm (Col 14 Lin 06)"),
        (12, 7):  ("led-tras", "D8", "Nano D8 (Pis.TD)", "Trilha Col 8 para R7 Top"),
        (12, 8):  ("led-tras", "D7", "Nano D7 (Pis.TE)", "Trilha Col 9 para R6 Top"),
        (12, 9):  ("led-tras", "D6", "Nano D6 (Freio)", "Trilha Col 10 para R5 Top"),
        (12, 10): ("led-tras", "D5", "Nano D5 (Lant)", "Trilha Col 11 para R4 Top"),
        (12, 11): ("radio", "D4", "Nano D4 (CH1)", "Trilha direta horizontal de 10mm para CON1 P5 (Lin 11)"),
        (12, 12): ("radio", "D3", "Nano D3 (CH4)", "Trilha direta horizontal de 10mm para CON1 P4 (Lin 12)"),
        (12, 13): ("radio", "D2", "Nano D2 (CH2)", "Trilha direta horizontal de 10mm para CON1 P3 (Lin 13)"),
        (12, 14): ("gnd", "GND", "Nano GND Dir (Pin 04)", "Barramento GND Direito & Origem Jumper W3 GND Cross-Tie"),
        (12, 16): ("mech", "D0", "Nano D0/RX", "Pino serial RX"),
        (12, 17): ("mech", "D1", "Nano D1/TX", "Pino serial TX"),

        # CON1: Rádio (Lateral Direita - Coluna 17, Linhas 11 a 15) — ENTRADA DE ENERGIA MESTRE
        (17, 11): ("radio", "CON1 P5", "CON1 CH1 (Vol)", "Trilha direta horizontal para Nano D4 (10mm, Lin 11)"),
        (17, 12): ("radio", "CON1 P4", "CON1 CH4 (Farol)", "Trilha direta horizontal para Nano D3 (10mm, Lin 12)"),
        (17, 13): ("radio", "CON1 P3", "CON1 CH2 (Thr)", "Trilha direta horizontal para Nano D2 (10mm, Lin 13)"),
        (17, 14): ("gnd", "CON1 P2", "CON1 GND Mestre", "Entrada de GND Mestre do rádio no Barramento de Terra"),
        (17, 15): ("vcc", "CON1 P1", "CON1 +6.0V (BEC)", "Entrada +6.0V bruta do BEC / Anodo do D1 1N4007 (Pad isolado no verso, pitch 7,62mm descendo até Linha 18)"),

        # D1 1N4007 Catodo, C1 e Linha 18 (v8.4)
        (17, 18): ("vcc", "D1-K", "D1 Catodo (+5.25V)", "Saída regulada de +5.25V do diodo D1 (1N4007 com pitch de 7,62mm)"),
        (16, 18): ("vcc", "W5 In", "Origem Jumper W5", "Barramento VCC +5.25V para Jumper W5 (Farol Q1 Coletor)"),
        (15, 18): ("vcc", "C1(+)/W1", "C1(+) & W1 In", "Polo positivo do capacitor C1 e origem do Jumper W1 (+5.25V Nano 5V)"),
        (14, 18): ("gnd", "C1 (-)", "Capacitor C1 (-)", "Polo negativo de C1 com ponte direta de solda para GND Coluna 13"),

        # CON4: MPU-6050 (Lateral Esquerda - Coluna 02, Linhas 10 a 13 - v8.1)
        (2, 10):  ("gnd", "CON4 P1", "CON4 GND", "Ponto de solda de terra ligado ao Barramento GND Coluna 01"),
        (2, 11):  ("i2c", "CON4 P2", "CON4 TX (SCL)", "Trilha direta horizontal de 10mm para Nano A5 (Linha 11)"),
        (2, 12):  ("i2c", "CON4 P3", "CON4 RX (SDA)", "Terminal do Jumper W4 isolado superior para Nano A4 (Linha 10)"),
        (2, 13):  ("vcc", "CON4 P4", "CON4 +5V (VCC)", "Alimentação +5V do acelerômetro via ramal vindo de Nano 5V"),

        # CON2: Chicote Dianteiro (Lateral Superior Direita - Coluna 17, Linhas 04 a 07 - v8.0)
        (17, 7):  ("gnd", "CON2 P1", "CON2 GND", "Solda de terra do chicote dianteiro (via Jumper W2)"),
        (17, 6):  ("led-frente", "CON2 P2", "CON2 Farol", "Ponte de solda para R1 Out (Farol dianteiro)"),
        (17, 5):  ("led-frente", "CON2 P3", "CON2 Pis.FE", "Ponte de solda para R2 Out (Pisca dianteiro esquerdo)"),
        (17, 4):  ("led-frente", "CON2 P4", "CON2 Pis.FD", "Ponte de solda para R3 Out (Pisca dianteiro direito)"),

        # Resistores Dianteiros R2 e R3 (Horizontal: Rows 04 e 05, Cols 14 a 16, 100Ω 1/4W)
        (14, 5):  ("led-frente", "R2 In", "R2 In (Pis.FE 100Ω)", "Trilha direta horizontal de Nano D10 (12, 05)"),
        (16, 5):  ("led-frente", "R2 Out", "R2 Out (Pis.FE 100Ω)", "Ponte de solda direta para CON2 P3 (17, 05)"),
        (14, 4):  ("led-frente", "R3 In", "R3 In (Pis.FD 100Ω)", "Trilha direta horizontal de Nano D11 (12, 04)"),
        (16, 4):  ("led-frente", "R3 Out", "R3 Out (Pis.FD 100Ω)", "Ponte de solda direta para CON2 P4 (17, 04)"),

        # Driver de Farol Q1 (BC337 NPN) na Linha 09, Cols 13 a 15 (v8.2)
        (13, 9):  ("vcc", "Q1 Coletor", "Q1 Coletor (BC337)", "Terminal Coletor ligado a +5.25V via Jumper W5"),
        (14, 9):  ("led-frente", "Q1 Base", "Q1 Base (BC337)", "Terminal Base excitado por Nano D9 via trilha de solda (14,06)"),
        (15, 9):  ("led-frente", "Q1 Emissor", "Q1 Emissor (BC337)", "Terminal Emissor ligado a R1 In (15, 08)"),

        # Resistor R1 Farol (Vertical: Col 15, Rows 06 e 08, 27Ω 1/4W v8.2)
        (15, 8):  ("led-frente", "R1 In", "R1 In (Farol 27Ω)", "Ponte de solda com Emissor de Q1 (15, 09)"),
        (15, 6):  ("led-frente", "R1 Out", "R1 Out (Farol 27Ω)", "Saída para CON2 P2 (Farol) via trilha para (17, 06)"),

        # Terminais dos Jumpers Superiores (W2 GND e W5 +5V)
        (16, 7):  ("gnd", "W2 In", "Jumper W2 GND", "Terminal de terra dianteiro e ponte para CON2 P1"),
        (16, 14): ("gnd", "W2 Out", "GND Mestre W2", "Origem do Jumper W2 no barramento GND"),
        (16, 15): ("vcc", "W5 In", "Jumper W5 (+5.25V)", "Ponte de solda com (15,15) alimentando Jumper W5 para Coletor de Q1"),

        # Resistores Traseiros R7, R6, R5, R4 (Cols 8, 9, 10, 11, Rows 18 e 21, 100Ω 1/4W)
        (8, 18):  ("led-tras", "R7 Top", "R7 Top (Pis.TD 100Ω)", "Entrada vinda de Nano D8 (Lin 7)"),
        (8, 21):  ("led-tras", "R7 Bot", "R7 Bot (Pis.TD)", "Trilha direta vertical para CON3 Pino 1"),
        (9, 18):  ("led-tras", "R6 Top", "R6 Top (Pis.TE 100Ω)", "Entrada vinda de Nano D7 (Lin 8)"),
        (9, 21):  ("led-tras", "R6 Bot", "R6 Bot (Pis.TE)", "Trilha direta vertical para CON3 Pino 2"),
        (10, 18): ("led-tras", "R5 Top", "R5 Top (Freio 100Ω)", "Entrada vinda de Nano D6 (Lin 9)"),
        (10, 21): ("led-tras", "R5 Bot", "R5 Bot (Freio)", "Trilha direta vertical para CON3 Pino 3"),
        (11, 18): ("led-tras", "R4 Top", "R4 Top (Lant. 100Ω)", "Entrada vinda de Nano D5 (Lin 10)"),
        (11, 21): ("led-tras", "R4 Bot", "R4 Bot (Lant.)", "Trilha direta vertical para CON3 Pino 4"),

        # CON3: Chicote Traseiro (Linha 24, Colunas 8 a 13)
        (8, 24):  ("led-tras", "CON3 P1", "CON3 Pis.TD", "Alimentação do pisca traseiro direito"),
        (9, 24):  ("led-tras", "CON3 P2", "CON3 Pis.TE", "Alimentação do pisca traseiro esquerdo"),
        (10, 24): ("led-tras", "CON3 P3", "CON3 Freio", "Alimentação das luzes de freio"),
        (11, 24): ("led-tras", "CON3 P4", "CON3 Lant.", "Alimentação das lanternas traseiras"),
        (13, 24): ("gnd", "CON3 P6", "CON3 GND", "Solda de terra comum do chicote traseiro via Col 13")
    }

    svg = []
    svg.append(f'<svg id="svg-bottom-root" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {board_w} {board_h}" width="{board_w}" height="{board_h}" style="background:#060a08; font-family:\'Segoe UI\',system-ui,sans-serif;">')
    svg.append('<defs>')
    svg.append('''
      <linearGradient id="fr4BackDark" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#0a1f12"/>
        <stop offset="50%" stop-color="#06150c"/>
        <stop offset="100%" stop-color="#030b06"/>
      </linearGradient>
      <linearGradient id="solderDome" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#ffffff"/>
        <stop offset="30%" stop-color="#f1f5f9"/>
        <stop offset="70%" stop-color="#94a3b8"/>
        <stop offset="100%" stop-color="#334155"/>
      </linearGradient>
      <filter id="padGlow" x="-50%" y="-50%" width="200%" height="200%">
        <feGaussianBlur stdDeviation="3" result="blur"/>
        <feComposite in="SourceGraphic" in2="blur" operator="over"/>
      </filter>
      <filter id="busGlow" x="-30%" y="-30%" width="160%" height="160%">
        <feGaussianBlur stdDeviation="3" result="blur"/>
        <feComposite in="SourceGraphic" in2="blur" operator="over"/>
      </filter>
    ''')
    svg.append('</defs>')

    # PCB Board Base (Mirrored)
    pcb_x = margin_x - pitch/2
    pcb_y = margin_y - pitch/2
    pcb_w = (cols - 1) * pitch + pitch
    pcb_h = (rows - 1) * pitch + pitch
    svg.append(f'<rect x="{pcb_x}" y="{pcb_y}" width="{pcb_w}" height="{pcb_h}" rx="10" fill="url(#fr4BackDark)" stroke="#143d23" stroke-width="3"/>')

    # Grid & Coordinates (Mirrored column numbers)
    for c in range(1, cols + 1):
        x = cx(c)
        svg.append(f'<line x1="{x}" y1="{cy(1)}" x2="{x}" y2="{cy(rows)}" stroke="#092011" stroke-width="1" opacity="0.8"/>')
        svg.append(f'<text x="{x}" y="{pcb_y - 12}" text-anchor="middle" fill="#2ed573" font-size="11" font-weight="bold">{c:02d}</text>')
        svg.append(f'<text x="{x}" y="{pcb_y + pcb_h + 24}" text-anchor="middle" fill="#2ed573" font-size="11" font-weight="bold">{c:02d}</text>')

    for r in range(1, rows + 1):
        y = cy(r)
        svg.append(f'<line x1="{cx(cols)}" y1="{y}" x2="{cx(1)}" y2="{y}" stroke="#092011" stroke-width="1" opacity="0.8"/>')
        svg.append(f'<text x="{margin_x - 30}" y="{y + 4}" text-anchor="middle" fill="#ffd32a" font-size="11">{r:02d}</text>')
        svg.append(f'<text x="{board_w - margin_x + 30}" y="{y + 4}" text-anchor="middle" fill="#ffd32a" font-size="11">{r:02d}</text>')

    # Copper pad holes
    for r in range(1, rows + 1):
        for c in range(1, cols + 1):
            x = cx(c)
            y = cy(r)
            svg.append(f'<circle cx="{x}" cy="{y}" r="5.5" fill="#8c7300" stroke="#594900" stroke-width="0.8" opacity="0.7"/>')
            svg.append(f'<circle cx="{x}" cy="{y}" r="2.2" fill="#030805"/>')

    # Helper: draw heavy, highly visible solder track with authentic metallic luster
    def draw_solder_track(points, color, width, net_id, label=""):
        d_str = "M " + " L ".join([f"{p[0]} {p[1]}" for p in points])
        # 1. Base solder track (thick glowing run)
        svg.append(f'<path class="track-line track-{net_id}" d="{d_str}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" opacity="0.95" filter="url(#busGlow)"/>')
        # 2. Inner bright metallic solder core (tin highlight)
        core_w = max(2.0, width * 0.35)
        svg.append(f'<path class="track-line track-{net_id} track-core" d="{d_str}" fill="none" stroke="#ffffff" stroke-width="{core_w}" stroke-linecap="round" stroke-linejoin="round" opacity="0.4" pointer-events="none"/>')
        # 3. Solder joint beads at every node
        for p in points:
            svg.append(f'<circle class="solder-node node-{net_id}" cx="{p[0]}" cy="{p[1]}" r="{width * 0.72}" fill="{color}" stroke="#ffffff" stroke-width="1.2" opacity="0.95"/>')
        # 4. High-contrast label with dark pill background
        if label and len(points) >= 2:
            mid_x = (points[0][0] + points[-1][0]) / 2
            mid_y = (points[0][1] + points[-1][1]) / 2
            lbl_w = len(label) * 6.8 + 14
            svg.append(f'<rect x="{mid_x - lbl_w/2}" y="{mid_y - 14}" width="{lbl_w}" height="16" rx="3.5" fill="#04080c" stroke="{color}" stroke-width="1.0" opacity="0.92"/>')
            svg.append(f'<text class="solder-lbl lbl-{net_id}" x="{mid_x}" y="{mid_y-2.5}" text-anchor="middle" fill="{color}" font-size="9" font-weight="bold" pointer-events="none">{label}</text>')

    def draw_bottom_jumper_guide(points, color, width, net_id, label=""):
        d_str = "M " + " L ".join([f"{p[0]} {p[1]}" for p in points])
        svg.append(f'<path class="track-line track-{net_id} jumper-guide" d="{d_str}" fill="none" stroke="{color}" stroke-width="{width}" stroke-dasharray="6,4" stroke-linecap="round" stroke-linejoin="round" opacity="0.85"/>')
        for p in [points[0], points[-1]]:
            svg.append(f'<circle cx="{p[0]}" cy="{p[1]}" r="6.0" fill="none" stroke="{color}" stroke-width="2.2"/>')
            svg.append(f'<circle cx="{p[0]}" cy="{p[1]}" r="2.5" fill="{color}"/>')
        if label and len(points) >= 2:
            mid_x = (points[0][0] + points[-1][0]) / 2
            mid_y = (points[0][1] + points[-1][1]) / 2
            lbl_w = len(label) * 6.8 + 14
            svg.append(f'<rect x="{mid_x - lbl_w/2}" y="{mid_y - 14}" width="{lbl_w}" height="16" rx="3.5" fill="#04080c" stroke="{color}" stroke-width="0.8" opacity="0.92"/>')
            svg.append(f'<text class="solder-lbl lbl-{net_id}" x="{mid_x}" y="{mid_y-2.5}" text-anchor="middle" fill="{color}" font-size="8.5" font-weight="bold" font-style="italic" opacity="0.95" pointer-events="none">⚡ {label}</text>')

    svg.append('<g id="solder-tracks-layer">')

    # ==========================================
    # 1. 📡 SINAIS DO RÁDIO (CON1: Lateral Direita - Coluna 17, Linhas 11 a 13 ➔ Nano Col 12) — APENAS 10mm!
    # ==========================================
    draw_solder_track([(cx(17), cy(11)), (cx(12), cy(11))], "#3498db", 6.0, "radio", label="D4/CH1 (10mm)")
    draw_solder_track([(cx(17), cy(12)), (cx(12), cy(12))], "#2ecc71", 6.0, "radio", label="D3/CH4 (10mm)")
    draw_solder_track([(cx(17), cy(13)), (cx(12), cy(13))], "#f39c12", 6.0, "radio", label="D2/CH2 (10mm)")

    # ==========================================
    # 2. 🧭 TRILHAS DO MPU-6050 (CON4: Lateral Esquerda - Coluna 02, Linhas 10 a 13 - v8.1)
    # ==========================================
    # P2 (TX / SCL Linha 11): Trilha horizontal reta de 10mm para Nano A5
    draw_solder_track([(cx(2), cy(11)), (cx(6), cy(11))], "#ffd32a", 6.5, "i2c", label="TX / SCL (10mm)")
    # P1 (GND Linha 10): Ponte curta para o Barramento GND da Coluna 01
    draw_solder_track([(cx(2), cy(10)), (cx(1), cy(10))], "#00d26a", 6.5, "gnd", label="GND MPU")
    # P3 (RX / SDA Linha 12): Guia tracejada do Jumper W4 isolado na face superior para Nano A4 (Lin 10)
    draw_bottom_jumper_guide([(cx(2), cy(12)), (cx(6), cy(10))], "#2ed573", 3.2, "i2c", label="W4 (RX/SDA)")

    # ==========================================
    # 3. 🔴 LINHA +5.25V PROTEGIDA (VCC REGULADO POR D1 1N4007 COM C1 E JUMPERS W1 / W5 - v8.4)
    # ==========================================
    # Trilha de Solda no Verso na Linha 18: D1-K (17,18) ➔ W5 In (16,18) ➔ C1(+) / W1 In (15,18)
    # ATENÇÃO v8.4: O Pad (17,15) fica ISOLADO no verso! D1 desce pela Coluna 17 até (17,18) com pitch de 7,62mm.
    draw_solder_track([(cx(17), cy(18)), (cx(15), cy(18))], "#ff4757", 7.5, "vcc", label="+5.25V Bus")
    # Ponte de solda C1(-) para GND Mestre da Coluna 13 na Linha 18: (14,18) ➔ (13,18)
    draw_solder_track([(cx(14), cy(18)), (cx(13), cy(18))], "#00d26a", 6.5, "gnd", label="C1 GND")
    # Indicação do Jumper W1 isolado superior (+5.25V): C1(+) (15,18) ➔ Nano 5V (06,14)
    draw_bottom_jumper_guide([(cx(15), cy(18)), (cx(6), cy(14))], "#ff4757", 3.2, "vcc", label="W1 (+5.25V)")
    # Indicação do Jumper W5 isolado superior (+5.25V Farol): Barramento VCC (16,18) ➔ Q1 Coletor (13,09)
    draw_bottom_jumper_guide([(cx(16), cy(18)), (cx(13), cy(9))], "#ff4757", 3.2, "vcc", label="W5 (+5.25V Farol)")
    # Ramal de alimentação para CON4 P4 (+5V MPU Linha 13): Nano 5V (06,14) ➔ (05,14) ➔ (05,13) ➔ CON4 P4 (02,13)
    vcc_track_bottom = [
        (cx(6), cy(14)),
        (cx(5), cy(14)),
        (cx(5), cy(13)),
        (cx(2), cy(13))
    ]
    draw_solder_track(vcc_track_bottom, "#ff4757", 6.5, "vcc", label="+5V MPU")

    # ==========================================
    # 4. ⚡ BARRAMENTO DE NEUTRO MESTRE (GND UNIFICADO E 100% INTERLIGADO)
    # ==========================================
    # Tronco Direito: CON1 P2 GND (Col 17, Lin 14) une a Nano GND Dir (Col 12, Lin 14)
    gnd_right = [
        (cx(17), cy(14)),  # CON1 P2 (GND Mestre do Rádio)
        (cx(12), cy(14))   # Nano GND Dir (Pin 04)
    ]
    draw_solder_track(gnd_right, "#00d26a", 7.5, "gnd", label="GND Mestre (Do Rádio)")

    # Canal livre Coluna 13 desce reto até CON3 P6 GND (Trás)
    draw_solder_track([(cx(13), cy(14)), (cx(13), cy(24))], "#00d26a", 7.5, "gnd", label="GND Canal Col 13")

    # Jumper W3 Cross-Tie de Terra Transversal (Face Superior)
    draw_bottom_jumper_guide([(cx(12), cy(14)), (cx(6), cy(16))], "#00d26a", 3.2, "gnd", label="W3 (GND Cross)")

    # Jumper W2 de Terra Dianteiro (Face Superior)
    draw_bottom_jumper_guide([(cx(16), cy(14)), (cx(16), cy(7))], "#00d26a", 3.2, "gnd", label="W2 (GND Frente)")
    draw_solder_track([(cx(16), cy(7)), (cx(17), cy(7))], "#00d26a", 6.5, "gnd", label="GND")

    # Tronco Esquerdo: Nano GND Esq Col 06 Linha 16 conecta direto ao Barramento Coluna 01
    draw_solder_track([(cx(6), cy(16)), (cx(1), cy(16))], "#00d26a", 7.0, "gnd")
    # Barramento Coluna 01 (Terra unificado)
    draw_solder_track([(cx(1), cy(1)), (cx(1), cy(24))], "#00d26a", 7.5, "gnd", label="GND Bus (Col 01)")

    # ==========================================
    # 5. 💡 LEDS DIANTEIROS (CON2: Lateral Superior Direita, Linhas 04 a 07 - v8.2)
    # ==========================================
    # Farol Driver v8.2 com Transistor Q1 (BC337) e R1 27Ω
    # Nano D9 (12, 06) -> Base Q1 (14, 09):
    draw_solder_track([(cx(12), cy(6)), (cx(14), cy(6)), (cx(14), cy(9))], "#ffffff", 6.0, "led-frente", label="D9 -> Base Q1")
    # Emissor Q1 (15, 09) -> R1 In (15, 08):
    draw_solder_track([(cx(15), cy(9)), (cx(15), cy(8))], "#ffffff", 6.5, "led-frente")
    # R1 Out (15, 06) -> CON2 P2 (17, 06):
    draw_solder_track([(cx(15), cy(6)), (cx(17), cy(6))], "#ffffff", 6.5, "led-frente", label="Farol")

    # R2 Pisca FE D10 (Row 05)
    draw_solder_track([(cx(12), cy(5)), (cx(14), cy(5))], "#ff9f1a", 6.0, "led-frente", label="D10 (5mm)")
    draw_solder_track([(cx(16), cy(5)), (cx(17), cy(5))], "#ff9f1a", 6.5, "led-frente", label="Pis.FE")

    # R3 Pisca FD D11 (Row 04)
    draw_solder_track([(cx(12), cy(4)), (cx(14), cy(4))], "#1e90ff", 6.0, "led-frente", label="D11 (5mm)")
    draw_solder_track([(cx(16), cy(4)), (cx(17), cy(4))], "#1e90ff", 6.5, "led-frente", label="Pis.FD")

    # ==========================================
    # 6. 💡 LEDS TRASEIROS (CON3: Linha 24, Cols 8 a 13) — TRILHAS "L" ANINHADAS (ZERO CRUZAMENTOS!)
    # ==========================================
    draw_solder_track([(cx(12), cy(7)), (cx(8), cy(7)), (cx(8), cy(18))], "#1e90ff", 5.5, "led-tras", label="D8")
    draw_solder_track([(cx(8), cy(21)), (cx(8), cy(24))], "#1e90ff", 6.5, "led-tras")

    draw_solder_track([(cx(12), cy(8)), (cx(9), cy(8)), (cx(9), cy(18))], "#ffa502", 5.5, "led-tras", label="D7")
    draw_solder_track([(cx(9), cy(21)), (cx(9), cy(24))], "#ffa502", 6.5, "led-tras")

    draw_solder_track([(cx(12), cy(9)), (cx(10), cy(9)), (cx(10), cy(18))], "#ff4757", 5.5, "led-tras", label="D6")
    draw_solder_track([(cx(10), cy(21)), (cx(10), cy(24))], "#ff4757", 6.5, "led-tras")

    draw_solder_track([(cx(12), cy(10)), (cx(11), cy(10)), (cx(11), cy(18))], "#ff7f50", 5.5, "led-tras", label="D5")
    draw_solder_track([(cx(11), cy(21)), (cx(11), cy(24))], "#ff7f50", 6.5, "led-tras")

    # ==========================
    # SOLDER PADS & GLOW RINGS
    # ==========================
    net_colors = {
        "gnd": "#00d26a",
        "vcc": "#ff4757",
        "radio": "#ffd32a",
        "i2c": "#2ed573",
        "led-frente": "#ffffff",
        "led-tras": "#ff7f50",
        "mech": "#747d8c"
    }

    svg.append('<g id="solder-pads-layer">')
    for (col, row), (net_id, pin_lbl, comp_name, solder_desc) in solder_pads_data.items():
        x = cx(col)
        y = cy(row)
        n_col = net_colors.get(net_id, "#fff")

        # Outer glowing ring
        svg.append(f'<circle class="solder-ring pad-{net_id}" cx="{x}" cy="{y}" r="11" fill="none" stroke="{n_col}" stroke-width="2.5" filter="url(#padGlow)"/>')
        # Solder dome
        svg.append(f'<circle class="solder-joint pad-{net_id}" data-col="{col}" data-row="{row}" data-net="{net_id}" data-pin="{pin_lbl}" data-comp="{comp_name}" data-desc="{solder_desc}" cx="{x}" cy="{y}" r="8" fill="url(#solderDome)" stroke="#334155" stroke-width="1.5" style="cursor:pointer;"/>')
        # Hole center
        svg.append(f'<circle cx="{x}" cy="{y}" r="2.5" fill="#0f172a" pointer-events="none"/>')

        # Label position
        lbl_x = x
        lbl_y = y - 13
        if col == 2:
            lbl_x = x + 26
            lbl_y = y + 3
        elif row == 9 and col in (13, 14, 15):
            lbl_y = y + 16
        elif col == 15 and (row == 6 or row == 8):
            lbl_x = x - 26
            lbl_y = y + 3
        elif col == 16 and row == 15:
            lbl_x = x
            lbl_y = y + 16
        elif col == 14 or col == 16:
            lbl_x = x - 20
            lbl_y = y + 3
        elif col == 17:
            lbl_x = x + 26
            lbl_y = y + 3
        elif col == 15 and (row == 14 or row == 15):
            lbl_x = x - 26
            lbl_y = y + 3
        elif row == 24:
            lbl_y = y - 14
        elif row == 14 or row == 16:
            lbl_x = x + 22 if col == 6 else x - 22
            lbl_y = y + 3

        svg.append(f'<text class="solder-lbl lbl-{net_id}" x="{lbl_x}" y="{lbl_y}" text-anchor="middle" fill="{n_col}" font-size="7.5" font-weight="bold" pointer-events="none">{pin_lbl}</text>')

    svg.append('</g>')

    # Board Title and Solder Legend
    svg.append(f'<text x="{board_w/2}" y="{pcb_y - 45}" text-anchor="middle" fill="#ecf0f1" font-size="16" font-weight="bold">PLACA SHIELD HUB 5x7cm — VISTA INFERIOR (TRILHAS DE SOLDA NO VERSO)</text>')
    svg.append(f'<text x="{board_w/2}" y="{pcb_y - 25}" text-anchor="middle" fill="#2ed573" font-size="11">Layout Natural Distribuído v8.4 — Suporte BEC 6.0V (D1 1N4007 Pitch 7.62mm) &amp; Driver Farol BC337</text>')

    svg.append('</svg>')
    return "".join(svg)


def generate_interactive_html(svg_top_str, svg_bottom_str):
    html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Placa Shield Hub 5x7cm (v8.4) — Visualizador Interativo &amp; Premissas</title>
  <style>
    :root {{
      --bg-dark: #090d14;
      --bg-panel: #0f172a;
      --bg-card: #1e293b;
      --border: #334155;
      --primary: #3b82f6;
      --accent: #10b981;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --gnd: #00d26a;
      --vcc: #ff4757;
      --radio: #ffd32a;
      --i2c: #2ed573;
      --led-frente: #ffffff;
      --led-tras: #ff7f50;
      --jumper: #a855f7;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--bg-dark);
      color: var(--text-main);
      font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
      display: flex;
      flex-direction: column;
      height: 100vh;
      overflow: hidden;
    }}
    header {{
      background: var(--bg-panel);
      border-bottom: 1px solid var(--border);
      padding: 10px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 12px;
      z-index: 10;
    }}
    .header-title {{
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }}
    .header-title h1 {{
      font-size: 1.1rem;
      font-weight: 700;
      letter-spacing: 0.5px;
      background: linear-gradient(90deg, #60a5fa, #34d399);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
    .header-title .badge {{
      background: #1e3a8a;
      color: #93c5fd;
      font-size: 0.72rem;
      padding: 3px 8px;
      border-radius: 9999px;
      font-weight: 600;
      border: 1px solid #3b82f6;
    }}
    .header-title .badge-norm {{
      background: rgba(16, 185, 129, 0.15);
      color: #34d399;
      font-size: 0.72rem;
      padding: 3px 8px;
      border-radius: 9999px;
      font-weight: 600;
      border: 1px solid rgba(52, 211, 153, 0.4);
    }}
    .controls {{
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }}
    .btn-group {{
      display: flex;
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 8px;
      overflow: hidden;
    }}
    .btn-group button {{
      background: transparent;
      border: none;
      color: var(--text-muted);
      padding: 7px 14px;
      font-size: 0.82rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .btn-group button.active {{
      background: var(--primary);
      color: white;
      box-shadow: 0 0 10px rgba(59, 130, 246, 0.4);
    }}
    .btn-group button:hover:not(.active) {{
      color: white;
      background: rgba(255,255,255,0.05);
    }}
    .btn-premissas-modal {{
      background: linear-gradient(135deg, #059669, #10b981);
      border: 1px solid #34d399;
      color: white;
      padding: 7px 14px;
      border-radius: 8px;
      font-size: 0.82rem;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
      transition: all 0.2s;
    }}
    .btn-premissas-modal:hover {{
      background: linear-gradient(135deg, #047857, #059669);
      transform: translateY(-1px);
      box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
    }}
    .main-layout {{
      display: grid;
      grid-template-columns: 380px 1fr;
      flex: 1;
      height: calc(100vh - 60px);
      overflow: hidden;
    }}
    @media (max-width: 960px) {{
      .main-layout {{ grid-template-columns: 1fr; height: auto; }}
    }}
    .sidebar {{
      background: var(--bg-panel);
      border-right: 1px solid var(--border);
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }}
    .sidebar-tabs {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      background: var(--bg-card);
      border-bottom: 1px solid var(--border);
    }}
    .sidebar-tab-btn {{
      background: transparent;
      border: none;
      color: var(--text-muted);
      padding: 10px;
      font-size: 0.82rem;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.2s;
      border-bottom: 2px solid transparent;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
    }}
    .sidebar-tab-btn.active {{
      color: white;
      border-bottom-color: var(--primary);
      background: rgba(59, 130, 246, 0.1);
    }}
    .sidebar-content {{
      padding: 14px;
      overflow-y: auto;
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}
    .step-card, .premissa-card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 12px;
      cursor: pointer;
      transition: all 0.2s;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}
    .step-card:hover, .premissa-card:hover {{
      border-color: var(--primary);
      transform: translateX(3px);
      box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }}
    .step-card.active, .premissa-card.active {{
      border-color: var(--accent);
      background: rgba(16, 185, 129, 0.08);
      box-shadow: 0 0 14px rgba(16, 185, 129, 0.2);
    }}
    .step-header, .premissa-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 0.86rem;
      font-weight: 700;
    }}
    .step-badge, .premissa-badge {{
      font-size: 0.7rem;
      padding: 2px 7px;
      border-radius: 9999px;
      font-weight: 600;
    }}
    .step-desc, .premissa-desc {{
      font-size: 0.8rem;
      color: var(--text-muted);
      line-height: 1.4;
    }}
    .step-pads-list, .premissa-tags {{
      display: flex;
      flex-wrap: wrap;
      gap: 4px;
      margin-top: 4px;
    }}
    .pad-tag, .premissa-tag {{
      background: rgba(255,255,255,0.06);
      border: 1px solid rgba(255,255,255,0.1);
      color: #e2e8f0;
      font-size: 0.72rem;
      padding: 2px 6px;
      border-radius: 4px;
      font-family: ui-monospace, monospace;
    }}
    .premissa-tag-active {{
      background: rgba(16, 185, 129, 0.2);
      border-color: rgba(52, 211, 153, 0.4);
      color: #6ee7b7;
    }}
    .viewer-area {{
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: auto;
      padding: 20px;
      background: #040706;
      position: relative;
    }}
    .zoom-controls {{
      position: absolute;
      top: 18px;
      right: 18px;
      background: rgba(15, 23, 42, 0.9);
      backdrop-filter: blur(8px);
      border: 1px solid var(--border);
      border-radius: 8px;
      display: flex;
      align-items: center;
      overflow: hidden;
      z-index: 50;
      box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }}
    .zoom-controls button {{
      background: transparent;
      border: none;
      color: var(--text-main);
      padding: 7px 12px;
      cursor: pointer;
      font-weight: 700;
      font-size: 0.95rem;
      transition: background 0.15s;
    }}
    .zoom-controls button:hover {{
      background: rgba(255,255,255,0.1);
    }}
    .zoom-controls span {{
      padding: 6px 10px;
      font-size: 0.78rem;
      font-family: ui-monospace, monospace;
      color: var(--text-muted);
      border-left: 1px solid var(--border);
      border-right: 1px solid var(--border);
      cursor: pointer;
      user-select: none;
    }}
    .zoom-controls span:hover {{
      color: white;
    }}
    .pad-hud {{
      position: absolute;
      bottom: 16px;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(15, 23, 42, 0.94);
      backdrop-filter: blur(10px);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 9px 18px;
      color: var(--text-main);
      font-size: 0.82rem;
      max-width: 90%;
      box-shadow: 0 10px 30px rgba(0,0,0,0.6);
      pointer-events: none;
      z-index: 50;
      transition: all 0.2s ease;
      text-align: center;
      white-space: nowrap;
      text-overflow: ellipsis;
      overflow: hidden;
    }}
    .pad-hud.active {{
      border-color: var(--primary);
      box-shadow: 0 0 18px rgba(59, 130, 246, 0.35);
    }}
    .hud-tag {{
      display: inline-block;
      padding: 2px 7px;
      border-radius: 4px;
      font-family: ui-monospace, monospace;
      font-weight: 700;
      font-size: 0.76rem;
      margin-right: 6px;
    }}
    .hud-tag-gnd {{ background: rgba(0, 210, 106, 0.2); color: #00d26a; border: 1px solid #00d26a; }}
    .hud-tag-vcc {{ background: rgba(255, 71, 87, 0.2); color: #ff4757; border: 1px solid #ff4757; }}
    .hud-tag-radio {{ background: rgba(255, 211, 42, 0.2); color: #ffd32a; border: 1px solid #ffd32a; }}
    .hud-tag-i2c {{ background: rgba(46, 213, 115, 0.2); color: #2ed573; border: 1px solid #2ed573; }}
    .hud-tag-led-frente {{ background: rgba(255, 255, 255, 0.2); color: #ffffff; border: 1px solid #ffffff; }}
    .hud-tag-led-tras {{ background: rgba(255, 127, 80, 0.2); color: #ff7f50; border: 1px solid #ff7f50; }}
    .svg-container {{
      max-width: 100%;
      height: auto;
      box-shadow: 0 10px 30px rgba(0,0,0,0.6);
      border-radius: 12px;
      overflow: hidden;
      border: 1px solid #1e293b;
      transition: transform 0.2s ease-out;
    }}
    .view-panel {{
      display: none;
    }}
    .view-panel.active {{
      display: block;
    }}
    /* Net highlight effects */
    .track-line, .solder-ring, .solder-lbl {{
      transition: all 0.3s ease;
    }}
    .dimmed {{
      opacity: 0.12 !important;
    }}
    .highlighted {{
      opacity: 1 !important;
      stroke-width: 6.5px !important;
      filter: drop-shadow(0 0 6px currentColor) !important;
    }}
    .solder-ring.highlighted {{
      stroke-width: 4px !important;
      r: 13px !important;
    }}
    /* Modal Styles */
    .modal-backdrop {{
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background: rgba(0, 0, 0, 0.8);
      backdrop-filter: blur(6px);
      z-index: 1000;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }}
    .modal-backdrop.open {{
      display: flex;
    }}
    .modal-card {{
      background: var(--bg-panel);
      border: 1px solid var(--border);
      border-radius: 12px;
      width: 100%;
      max-width: 820px;
      max-height: 85vh;
      display: flex;
      flex-direction: column;
      box-shadow: 0 20px 50px rgba(0,0,0,0.8);
      animation: modalSlideUp 0.25s ease-out;
    }}
    @keyframes modalSlideUp {{
      from {{ transform: translateY(20px); opacity: 0; }}
      to {{ transform: translateY(0); opacity: 1; }}
    }}
    .modal-header {{
      padding: 16px 22px;
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: var(--bg-card);
    }}
    .modal-header h2 {{
      font-size: 1.15rem;
      color: #60a5fa;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .modal-close-btn {{
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-size: 1.5rem;
      cursor: pointer;
      padding: 0 4px;
      line-height: 1;
    }}
    .modal-close-btn:hover {{
      color: white;
    }}
    .modal-body {{
      padding: 20px 24px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}
    .norm-block {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 14px 16px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}
    .norm-title {{
      font-size: 0.95rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}
    .norm-text {{
      font-size: 0.84rem;
      color: #cbd5e1;
      line-height: 1.5;
    }}
    .norm-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.78rem;
      margin-top: 6px;
    }}
    .norm-table th, .norm-table td {{
      padding: 6px 10px;
      border: 1px solid var(--border);
      text-align: left;
    }}
    .norm-table th {{
      background: rgba(255,255,255,0.05);
      color: #94a3b8;
    }}
    .norm-btn {{
      background: var(--primary);
      color: white;
      border: none;
      padding: 6px 12px;
      border-radius: 6px;
      font-size: 0.75rem;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      align-self: flex-start;
      margin-top: 4px;
    }}
    .norm-btn:hover {{
      background: #2563eb;
    }}
  </style>
</head>
<body>

<header>
  <div class="header-title">
    <h1>🛡️ Shield Hub 5x7cm — Visualizador &amp; Engenharia</h1>
    <span class="badge">v8.4 Suporte BEC 6.0V</span>
    <span class="badge-norm" style="border-color:#eab308; color:#fde047;">Diodo D1 1N4007 Pitch 7.62mm (-0.75V)</span>
    <span class="badge-norm" style="border-color:#3b82f6; color:#93c5fd;">Driver Farol Q1 (BC337)</span>
    <span class="badge-norm" style="border-color:#10b981; color:#34d399;">Resistores 100Ω &amp; 5 Jumpers</span>
  </div>

  <div class="controls">
    <div class="btn-group">
      <button id="btn-bottom" class="active" onclick="switchMainView('bottom')">🔍 Verso (Trilhas de Solda)</button>
      <button id="btn-top" onclick="switchMainView('top')">🧩 Face Superior (Componentes)</button>
      <button id="btn-xray" onclick="switchMainView('xray')">⚡ Raio-X Sobreposto</button>
    </div>

    <button class="btn-premissas-modal" onclick="openPremissasModal()">
      📜 5 Premissas de Projeto
    </button>
  </div>
</header>

<div class="main-layout">
  <div class="sidebar">
    <div class="sidebar-tabs">
      <button id="tab-btn-steps" class="sidebar-tab-btn active" onclick="switchSidebarTab('steps')">
        🔍 Inspeção por Rede
      </button>
      <button id="tab-btn-premissas" class="sidebar-tab-btn" onclick="switchSidebarTab('premissas')">
        📜 5 Premissas
      </button>
    </div>

    <!-- ABA 1: ROTEAMENTO PASSO A PASSO -->
    <div id="tab-content-steps" class="sidebar-content">
      <div class="step-card active" onclick="activateStep('all', this)">
        <div class="step-header" style="color:var(--primary);">
          <span>👁️ Visão Geral Completa</span>
          <span class="step-badge" style="background:rgba(59,130,246,0.2); color:#60a5fa;">Tudo Ativo</span>
        </div>
        <div class="step-desc">
          Exibe todas as redes elétricas simultaneamente com a pinagem física real do Arduino Nano (USB no Topo) e Diodo D1 (1N4007) para BEC 6.0V. Matriz 18x24 com <strong>0 conflitos de pads</strong>, CON2 na borda superior direita e CON4 com pinagem (GND, TX, RX, VCC).
        </div>
      </div>

      <div class="step-card" onclick="activateStep('radio', this)">
        <div class="step-header" style="color:var(--radio);">
          <span>1️⃣ Sinais do Rádio (10mm Diretos na Lateral Direita)</span>
          <span class="step-badge" style="background:rgba(255,211,42,0.2); color:var(--radio);">Face a Face</span>
        </div>
        <div class="step-desc">
          CON1 fica na <strong>Coluna 17 (Linhas 11 a 15)</strong>. Os sinais CH1 (D4), CH4 (D3) e CH2 (D2) conectam-se horizontalmente ao Nano na Coluna 12 por trilhas de 10mm!
        </div>
        <div class="step-pads-list">
          <span class="pad-tag">CON1 P5 ➔ Nano D4 (CH1)</span>
          <span class="pad-tag">CON1 P4 ➔ Nano D3 (CH4)</span>
          <span class="pad-tag">CON1 P3 ➔ Nano D2 (CH2)</span>
        </div>
      </div>

      <div class="step-card" onclick="activateStep('i2c', this)">
        <div class="step-header" style="color:var(--i2c);">
          <span>2️⃣ Acelerômetro MPU-6050 (CON4: GND, TX, RX, VCC)</span>
          <span class="step-badge" style="background:rgba(46,213,115,0.2); color:var(--i2c);">v8.1</span>
        </div>
        <div class="step-desc">
          CON4 fica na <strong>Coluna 02 (Linhas 10 a 13)</strong>. P1 GND conecta ao Barramento Coluna 01. P2 TX (SCL) liga por trilha direta horizontal de 10mm no verso a Nano A5. P3 RX (SDA) conecta via <strong>jumper isolado superior W4</strong> a Nano A4. P4 VCC (+5V) conecta ao ramal do Nano 5V.
        </div>
        <div class="step-pads-list">
          <span class="pad-tag">CON4 P1 (GND, 02,10) ➔ Col 01</span>
          <span class="pad-tag">CON4 P2 (TX/SCL, 02,11) ➔ Nano A5</span>
          <span class="pad-tag">CON4 P3 (RX/SDA, 02,12) ➔ Jumper W4 ➔ Nano A4</span>
          <span class="pad-tag">CON4 P4 (VCC, 02,13) ➔ Nano 5V</span>
        </div>
      </div>

      <div class="step-card" onclick="activateStep('vcc', this)">
        <div class="step-header" style="color:var(--vcc);">
          <span>3️⃣ Linha +5.25V Protegida (BEC 6.0V, D1 1N4007 Pitch 7.62mm, C1 &amp; Jumpers W1/W5)</span>
          <span class="step-badge" style="background:rgba(255,71,87,0.2); color:var(--vcc);">Premissas #1 &amp; #2</span>
        </div>
        <div class="step-desc">
          <strong>Origem de VCC com Proteção:</strong> O +6.0V entra por CON1 P1 (Col 17, Lin 15) e passa pelo <strong>diodo retificador D1 (1N4007)</strong> descendo reto pela Coluna 17 com pitch de 7,62 mm (3 passos) até (Col 17, Lin 18). O drop de ~0.75V gera um barramento de <strong>+5.25V seguro e regulado</strong> na Linha 18, conectado ao capacitor C1 (100µF x 25V) e aos <strong>jumpers W1</strong> (Nano 5V) e <strong>W5</strong> (Q1 Coletor Farol), com mais de 7 mm de separação galvânica contra curtos.
        </div>
        <div class="step-pads-list">
          <span class="pad-tag">CON1 P1 (+6.0V BEC, 17,15)</span>
          <span class="pad-tag">D1 1N4007 (-0.75V, 17,15➔17,18)</span>
          <span class="pad-tag">Barramento VCC Linha 18 (17,18➔15,18)</span>
          <span class="pad-tag">C1 (+) Filtro (15,18)</span>
          <span class="pad-tag">Jumper W1 (+5.25V) ➔ Nano 5V (06,14)</span>
          <span class="pad-tag">Jumper W5 (+5.25V) ➔ Q1 Coletor (13,09)</span>
          <span class="pad-tag">Trilha Verso ➔ CON4 P4 (02,13)</span>
        </div>
      </div>

      <div class="step-card" onclick="activateStep('gnd', this)">
        <div class="step-header" style="color:var(--gnd);">
          <span>4️⃣ Barramento GND Mestre Unificado</span>
          <span class="step-badge" style="background:rgba(0,210,106,0.2); color:var(--gnd);">Premissas #1 &amp; #3</span>
        </div>
        <div class="step-desc">
          <strong>Premissa de Terra:</strong> O GND Mestre entra por CON1 P2 (Col 17, Lin 14), passa por C1(-) (Col 15, Lin 14) e conecta-se a Nano GND Dir (12,14). O canal livre Coluna 13 desce até CON3 P6 (13,24). O <strong>jumper de terra W2</strong> conecta o GND Mestre (16,14) a CON2 P1 (16,07/17,07). Um <strong>jumper transversal W3</strong> une Nano GND Dir (12,14) a Nano GND Esq (06,16). Na esquerda, o barramento vertical da Coluna 01 fornece terra a CON4 P1 (02,10).
        </div>
        <div class="step-pads-list">
          <span class="pad-tag">CON1 P2 (GND Mestre, 17,14)</span>
          <span class="pad-tag">C1 (-) Entrada (15,14)</span>
          <span class="pad-tag">Jumper W2 GND ➔ CON2 P1 (17,07)</span>
          <span class="pad-tag">Canal Col 13 ➔ CON3 P6 (13,24)</span>
          <span class="pad-tag">Jumper W3 GND Cross (12,14 ➔ 06,16)</span>
          <span class="pad-tag">Barramento Col 01 ➔ CON4 P1 (02,10)</span>
        </div>
      </div>

      <div class="step-card" onclick="activateStep('led-frente', this)">
        <div class="step-header" style="color:#ffffff;">
          <span>5️⃣ LEDs Dianteiros (Driver Q1 BC337 &amp; CON2 Superior Direito)</span>
          <span class="step-badge" style="background:rgba(255,255,255,0.2); color:#fff;">Farol 45-60mA</span>
        </div>
        <div class="step-desc">
          <strong>Farol com Driver High-Side (Q1 BC337 NPN):</strong> O Nano D9 (12,06) excita a Base de Q1 (14,09) drenando apenas ~0.4mA. O Coletor (13,09) recebe +5.25V via jumper W5. O Emissor (15,09) alimenta o resistor vertical R1 (27Ω 1/4W nas Linhas 06 a 08) entregando 45 a 60 mA para os 4 LEDs brancos em paralelo via CON2 P2 (17,06). Os piscas D10 (FE) e D11 (FD) utilizam resistores horizontais de 100Ω (1/4W) entregando ~14.5mA por LED.
        </div>
        <div class="step-pads-list">
          <span class="pad-tag">Nano D9 (12,06) ➔ Q1 Base (14,09)</span>
          <span class="pad-tag">Jumper W5 (+5.25V) ➔ Q1 Coletor (13,09)</span>
          <span class="pad-tag">Q1 Emissor (15,09) ➔ R1 (27Ω) ➔ CON2 P2 (Farol)</span>
          <span class="pad-tag">Nano D10 (12,05) ➔ R2 (100Ω) ➔ CON2 P3 (Pis.FE)</span>
          <span class="pad-tag">Nano D11 (12,04) ➔ R3 (100Ω) ➔ CON2 P4 (Pis.FD)</span>
          <span class="pad-tag">Jumper W2 GND ➔ CON2 P1 (GND, 17,07)</span>
        </div>
      </div>

      <div class="step-card" onclick="activateStep('led-tras', this)">
        <div class="step-header" style="color:var(--led-tras);">
          <span>6️⃣ LEDs Traseiros (Trilhas em "L" Aninhadas &amp; 100Ω)</span>
          <span class="step-badge" style="background:rgba(255,127,80,0.2); color:var(--led-tras);">Zero Cruzamento</span>
        </div>
        <div class="step-desc">
          D5, D6, D7, D8 saem do Nano Col 12 (Linhas 07 a 10) e formam trilhas em "L" paralelas até os resistores R4 a R7 (100Ω 1/4W, Linhas 18 a 21) e CON3 (Linha 24, Colunas 8 a 13). Freio e piscas fornecem ~15mA por LED; Lanterna usa PWM suave ~20%.
        </div>
      </div>
    </div>

    <!-- ABA 2: 5 PREMISSAS OFICIAIS DE PROJETO -->
    <div id="tab-content-premissas" class="sidebar-content" style="display:none;">
      <div class="premissa-card" onclick="activatePremissa('vcc', this)">
        <div class="premissa-header" style="color:var(--vcc);">
          <span>⚡ Premissa #1: Origem de Energia (BEC 6.0V &amp; D1)</span>
          <span class="premissa-badge" style="background:rgba(255,71,87,0.2); color:var(--vcc);">CON1 / CH6</span>
        </div>
        <div class="premissa-desc">
          Toda a alimentação provém exclusivamente de <strong>CON1 via CH6 do Rádio</strong> (BEC 6.0V / 3A máx). O <strong>Diodo D1 (1N4007)</strong> onboard reduz a tensão em ~0.75V para <strong>+5.25V</strong>, garantindo operação 100% segura do Nano e proteção contra polaridade reversa. Pino <strong>VIN desconectado</strong>; Nano alimentado no pino 5V.
        </div>
      </div>

      <div class="premissa-card" onclick="activatePremissa('vcc', this)">
        <div class="premissa-header" style="color:#ffd32a;">
          <span>🔋 Premissa #2: Regulação D1 &amp; Filtragem C1 na Linha 18</span>
          <span class="premissa-badge" style="background:rgba(255,211,42,0.2); color:#ffd32a;">Col 14-17 (Lin 15-18)</span>
        </div>
        <div class="premissa-desc">
          Diodo <strong>D1 (1N4007)</strong> descendo na Coluna 17 entre (17,15) e (17,18) com pitch de 7,62mm e capacitor eletrolítico <strong>C1 (100µF x 25V)</strong> na Linha 18 (Colunas 14 e 15). Absorvem ruído EMI e brownouts de servo e motor com isolamento total contra curtos.
        </div>
      </div>

      <div class="premissa-card" onclick="activatePremissa('gnd', this)">
        <div class="premissa-header" style="color:var(--gnd);">
          <span>🌐 Premissa #3: GND Mestre Unificado</span>
          <span class="premissa-badge" style="background:rgba(0,210,106,0.2); color:var(--gnd);">R &lt; 0.05Ω</span>
        </div>
        <div class="premissa-desc">
          O GND de CON1 P2 é a <strong>referência 0V absoluta</strong>. A malha é 100% contínua e interligada na placa, garantindo continuidade mesmo se o Arduino Nano for retirado do soquete.
        </div>
      </div>

      <div class="premissa-card" onclick="activatePremissa('all', this)">
        <div class="premissa-header" style="color:#a855f7;">
          <span>📐 Premissa #4: Roteamento Híbrido &amp; 5 Jumpers Superiores</span>
          <span class="premissa-badge" style="background:rgba(168,85,247,0.2); color:#a855f7;">0 Curtos</span>
        </div>
        <div class="premissa-desc">
          Pinagem real do Nano (USB no topo). Diodo D1 (1N4007) descendo de Linha 15 a 18 (Pitch 7,62mm), Driver Q1 BC337 na Linha 09 e R1 vertical na Coluna 15. <strong>Apenas 5 fios isolados superiores (W1-W5)</strong> para alimentação segura (+5.25V), terra, cruzamento de SDA/RX e coletor do farol, com 0 curtos-circuitos.
        </div>
        <div class="premissa-tags">
          <span class="premissa-tag premissa-tag-active">W1: +5.25V (23mm)</span>
          <span class="premissa-tag premissa-tag-active">W2: GND Frente (18mm)</span>
          <span class="premissa-tag premissa-tag-active">W3: GND Cross (16mm)</span>
          <span class="premissa-tag premissa-tag-active">W4: SDA/RX MPU (11mm)</span>
          <span class="premissa-tag premissa-tag-active">W5: +5.25V Farol (16mm)</span>
        </div>
      </div>

      <div class="premissa-card" onclick="activatePremissa('radio', this)">
        <div class="premissa-header" style="color:#38bdf8;">
          <span>🔌 Premissa #5: Conectores em 90° nas Bordas</span>
          <span class="premissa-badge" style="background:rgba(56,189,248,0.2); color:#38bdf8;">MODU 90°</span>
        </div>
        <div class="premissa-desc">
          Todos os conectores utilizam barras de pinos macho em 90° voltadas para fora: CON1 e CON2 na borda lateral direita, CON4 na lateral esquerda, CON3 na borda inferior e USB no topo. Desconexão em &lt;5s na pista sem retirar a bolha.
        </div>
        <div class="premissa-tags">
          <span class="premissa-tag premissa-tag-active">CON1: Direita (Rádio)</span>
          <span class="premissa-tag premissa-tag-active">CON2: Superior Direita (Frente)</span>
          <span class="premissa-tag premissa-tag-active">CON4: Lateral Esquerda (MPU)</span>
          <span class="premissa-tag premissa-tag-active">CON3: Borda Inferior (Trás)</span>
          <span class="premissa-tag">USB: Borda Superior</span>
        </div>
      </div>

      <button class="norm-btn" style="width:100%; justify-content:center; padding:10px; margin-top:6px;" onclick="openPremissasModal()">
        📖 Abrir Memorial de Cálculo &amp; Detalhes Normativos
      </button>
    </div>
  </div>

  <div class="viewer-area">
    <!-- Zoom Controls -->
    <div class="zoom-controls">
      <button onclick="changeZoom(-0.15)" title="Diminuir Zoom (−)">−</button>
      <span id="zoom-val" onclick="resetZoom()" title="Clique para redefinir para 100%">100%</span>
      <button onclick="changeZoom(0.15)" title="Aumentar Zoom (+)">+</button>
      <button onclick="resetZoom()" title="Redefinir Zoom (100%)">⟲</button>
    </div>

    <div id="panel-bottom" class="view-panel active svg-container">
      {svg_bottom_str}
    </div>

    <div id="panel-top" class="view-panel svg-container">
      {svg_top_str}
    </div>

    <div id="panel-xray" class="view-panel svg-container" style="position:relative;">
      <div style="opacity:0.4; filter:contrast(1.2);">
        {svg_top_str}
      </div>
      <div style="position:absolute; top:0; left:0; width:100%; height:100%; mix-blend-mode:screen; opacity:0.85; pointer-events:none;">
        {svg_bottom_str}
      </div>
    </div>

    <!-- Pad Inspector HUD Floating Bar -->
    <div id="pad-hud" class="pad-hud">
      <span style="color:#94a3b8;">⚡ Passe o mouse sobre qualquer ponto de solda ou terminal na placa para ver coordenadas e função técnica.</span>
    </div>
  </div>
</div>

<!-- MODAL COM O TEXTO COMPLETO DAS 5 PREMISSAS DE PROJETO -->
<div id="modal-premissas" class="modal-backdrop" onclick="handleModalBackdropClick(event)">
  <div class="modal-card">
    <div class="modal-header">
      <h2>📜 Premissas Fundamentais de Engenharia (v8.4)</h2>
      <button class="modal-close-btn" onclick="closePremissasModal()">&times;</button>
    </div>
    <div class="modal-body">
      <div style="background:#0f172a; border-left:4px solid #10b981; padding:10px 14px; border-radius:4px; font-size:0.82rem; color:#94a3b8;">
        Estas premissas são <strong>normativas e inegociáveis</strong>. Qualquer modificação física, esquemática ou no código do firmware deve respeitar estritamente estes 5 postulados de projeto.
      </div>

      <!-- Premissa 1 -->
      <div class="norm-block">
        <div class="norm-title" style="color:var(--vcc);">
          <span>⚡ Premissa #1: Origem Absoluta de Energia (BEC 6.0V &amp; Diodo D1)</span>
          <span class="step-badge" style="background:rgba(255,71,87,0.2); color:var(--vcc);">CON1 / CH6 do Rádio</span>
        </div>
        <div class="norm-text">
          Toda a alimentação elétrica da placa shield provém única e exclusivamente do <strong>Receptor FlySky FS-BS6</strong> através de <strong>CON1 (CH6 / BEC 6.0V do ESC)</strong>. Nenhum outro conector fornece energia à placa. O <strong>Diodo Retificador D1 (1N4007)</strong> integrado diretamente descendo pela Coluna 17 entre (17,15) e (17,18) reduz a tensão em ~0.75V para um nível seguro de <strong>+5.25V</strong>, com pitch de 7,62 mm e isolamento total contra curtos. O pino <strong>VIN permanece desconectado</strong>; o Arduino Nano é alimentado diretamente no pino <strong>5V (Coluna 06, Linha 14)</strong> via jumper superior W1.
          <table class="norm-table">
            <thead>
              <tr>
                <th>Ponto Elétrico</th>
                <th>Função Elétrica</th>
                <th>Tensão Operacional</th>
                <th>Capacidade / Consumo</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>CON1 P1 (Col 17, Lin 15)</strong></td>
                <td>VCC Bruto BEC (Anodo D1)</td>
                <td>+6.0V nominal (+6.5V máx)</td>
                <td>Conector: 3.0A | Entrada Rádio</td>
              </tr>
              <tr>
                <td><strong>Catodo D1 (Col 17, Lin 18)</strong></td>
                <td>Barramento VCC Seguro Placa</td>
                <td>+5.25V nominal (&le; 5.5V seguro)</td>
                <td>Alimenta Nano 5V, C1(+), Q1 Coletor</td>
              </tr>
              <tr>
                <td><strong>CON1 P2 (Col 17, Lin 14)</strong></td>
                <td>GND Mestre (Ref. 0V Central)</td>
                <td>0V (Terra Absoluto)</td>
                <td>Conector: 3.0A | Sistema Total: ~210mA</td>
              </tr>
            </tbody>
          </table>
        </div>
        <button class="norm-btn" onclick="highlightFromPremissa('vcc')">🔍 Destacar Barramento +5.25V</button>
      </div>

      <!-- Premissa 2 -->
      <div class="norm-block">
        <div class="norm-title" style="color:#ffd32a;">
          <span>🔋 Premissa #2: Regulação D1 &amp; Filtragem C1 na Linha 18</span>
          <span class="step-badge" style="background:rgba(255,211,42,0.2); color:#ffd32a;">D1 (1N4007 Pitch 7.62mm) &amp; C1 (100µF)</span>
        </div>
        <div class="norm-text">
          O diodo retificador <strong>D1 (1N4007)</strong> e o capacitor eletrolítico <strong>C1 (100µF x 25V)</strong> atuam em conjunto na entrada. D1 desce pela Coluna 17 entre Linha 15 e 18, com pitch padrão de 7,62 mm, e C1 fica na Linha 18:
          <ul style="margin: 8px 0 0 18px; font-size: 0.8rem; color: #cbd5e1;">
            <li><strong>Anodo D1 (17, 15):</strong> Soldado diretamente ao pino CON1 P1 (+6.0V BEC). Pad isolado no verso.</li>
            <li><strong>Catodo D1 (17, 18):</strong> Saída de +5.25V regulada, ligada por trilha no verso a W5 In (16, 18) e C1(+) (15, 18).</li>
            <li><strong>Polo Positivo C1 (+) (15, 18):</strong> Barramento seguro de +5.25V e origem do Jumper W1 para Nano 5V.</li>
            <li><strong>Polo Negativo C1 (-) (14, 18):</strong> Interligado por ponte direta de solda de 1 pad ao tronco de GND da Coluna 13.</li>
          </ul>
        </div>
        <button class="norm-btn" onclick="highlightFromPremissa('vcc')">🔍 Destacar D1 e C1</button>
      </div>

      <!-- Premissa 3 -->
      <div class="norm-block">
        <div class="norm-title" style="color:var(--gnd);">
          <span>🌐 Premissa #3: Barramento de Terra (GND) Mestre Unificado</span>
          <span class="step-badge" style="background:rgba(0,210,106,0.2); color:var(--gnd);">R &lt; 0.05Ω Contínuo</span>
        </div>
        <div class="norm-text">
          O GND originário de <strong>CON1 P2 (Coluna 17, Linha 14)</strong> forma uma malha 100% contínua e interligada na placa, <strong>garantindo integridade mesmo se o Arduino Nano for retirado do soquete</strong>:
          <ul style="margin: 8px 0 0 18px; font-size: 0.8rem; color: #cbd5e1;">
            <li><strong>Tronco Direito (Col 13):</strong> Desce de Nano GND Dir (12, 14) até CON3 P6 (GND Traseiro, 13, 24).</li>
            <li><strong>Jumper W2 GND Dianteiro:</strong> Conecta do barramento GND Mestre (Col 16, Lin 14) até CON2 P1 (Col 16, Lin 07 ➔ 17, 07).</li>
            <li><strong>Jumper W3 GND Cross-Tie:</strong> Cruza a placa da Col 12 Lin 14 até Nano GND Esq (Col 06, Lin 16).</li>
            <li><strong>Tronco Esquerdo (Col 01):</strong> Fornece terra a CON4 P1 (GND MPU-6050, 02, 10).</li>
          </ul>
        </div>
        <button class="norm-btn" onclick="highlightFromPremissa('gnd')">🔍 Destacar Malha de Terra (GND)</button>
      </div>

      <!-- Premissa 4 -->
      <div class="norm-block">
        <div class="norm-title" style="color:#a855f7;">
          <span>📐 Premissa #4: Roteamento Híbrido, Driver Farol Q1 &amp; 5 Jumpers Superiores</span>
          <span class="step-badge" style="background:rgba(168,85,247,0.2); color:#a855f7;">Zero Curtos</span>
        </div>
        <div class="norm-text">
          O Arduino Nano é posicionado com a porta <strong>USB voltada para a borda superior (Linhas 01-02)</strong>. O diodo <strong>D1 (1N4007)</strong> descendo pela Coluna 17 garante redução segura para +5.25V com pitch padrão de 7,62 mm. O canal de Farol utiliza o transistor <strong>Q1 (BC337 NPN TO-92)</strong> operando como seguidor de emissor (High-Side), fornecendo 45-60 mA para 4 LEDs brancos em paralelo via resistor R1 vertical (27Ω 1/4W), drenando apenas 0.4mA de Nano D9. Os demais canais usam resistores de <strong>100Ω 1/4W</strong>. São necessários <strong>apenas 5 fios isolados superiores (W1–W5)</strong> na placa inteira, com 0 conflitos de pads:
          <ul style="margin: 8px 0 0 18px; font-size: 0.8rem; color: #cbd5e1;">
            <li><strong>W1 (+5.25V Nano, ~23mm):</strong> C1(+) / W1 In (Col 15, Lin 18) ➔ Nano 5V (Col 06, Lin 14)</li>
            <li><strong>W2 (GND Dianteiro, ~18mm):</strong> GND Mestre (Col 16, Lin 14) ➔ CON2 P1 (Col 16, Lin 07 ➔ 17, 07)</li>
            <li><strong>W3 (GND Cross-Tie, ~16mm):</strong> Nano GND Dir (Col 12, Lin 14) ➔ Nano GND Esq (Col 06, Lin 16)</li>
            <li><strong>W4 (SDA/RX Acelerômetro, ~11mm):</strong> CON4 P3 (Col 02, Lin 12) ➔ Nano A4 (Col 06, Lin 10)</li>
            <li><strong>W5 (+5.25V Farol Coletor Q1, ~16mm):</strong> Barramento VCC (Col 16, Lin 18) ➔ Q1 Coletor (Col 13, Lin 09)</li>
          </ul>
        </div>
        <button class="norm-btn" onclick="highlightFromPremissa('all')">🔍 Ver Roteamento Híbrido Completo</button>
      </div>

      <!-- Premissa 5 -->
      <div class="norm-block">
        <div class="norm-title" style="color:#38bdf8;">
          <span>🔌 Premissa #5: Conectores em Ângulo Reto (90°) nas Bordas da Placa</span>
          <span class="step-badge" style="background:rgba(56,189,248,0.2); color:#38bdf8;">Layout Mecânico</span>
        </div>
        <div class="norm-text">
          Para que a placa caiba no chassi sem encostar na bolha de policarbonato, todos os conectores são barras macho em 90° voltadas para fora:
          <ul style="margin: 8px 0 0 18px; font-size: 0.8rem; color: #cbd5e1;">
            <li><strong>CON1 (Rádio):</strong> Borda lateral direita (Coluna 17, Linhas 11 a 15).</li>
            <li><strong>CON2 (Chicote Dianteiro):</strong> Borda lateral superior direita (Coluna 17, Linhas 04 a 07) — mesmo lado do rádio.</li>
            <li><strong>CON4 (MPU-6050):</strong> Borda lateral esquerda (Coluna 02, Linhas 10 a 13) — P1 GND, P2 TX [SCL], P3 RX [SDA], P4 VCC.</li>
            <li><strong>CON3 (Chicote Traseiro):</strong> Borda inferior (Linha 24, Colunas 08 a 13).</li>
            <li><strong>USB do Nano:</strong> Borda superior externa (Linhas 01 a 02) — gravação de firmware sem desmontar a placa.</li>
          </ul>
        </div>
        <button class="norm-btn" onclick="highlightFromPremissa('radio')">🔍 Destacar Conectores de Borda</button>
      </div>
    </div>
  </div>
</div>

<script>
  let currentView = 'bottom';
  let currentFilter = 'all';
  let zoomLevel = 1.0;

  function setZoom(val) {{
    zoomLevel = Math.max(0.6, Math.min(2.5, Math.round(val * 100) / 100));
    document.querySelectorAll('.view-panel.active svg').forEach(svg => {{
      svg.style.transform = 'scale(' + zoomLevel + ')';
      svg.style.transformOrigin = 'top center';
      svg.style.transition = 'transform 0.15s ease-out';
    }});
    const lbl = document.getElementById('zoom-val');
    if (lbl) lbl.textContent = Math.round(zoomLevel * 100) + '%';
  }}

  function changeZoom(delta) {{
    setZoom(zoomLevel + delta);
  }}

  function resetZoom() {{
    setZoom(1.0);
  }}

  function switchMainView(mode) {{
    currentView = mode;
    document.querySelectorAll('.view-panel').forEach(p => p.classList.remove('active'));
    document.querySelectorAll('.btn-group button').forEach(b => b.classList.remove('active'));

    document.getElementById('panel-' + mode).classList.add('active');
    document.getElementById('btn-' + mode).classList.add('active');
    setZoom(zoomLevel);
    applyHighlightFilter();
    setupPadInspection();
  }}

  function switchSidebarTab(tabName) {{
    document.querySelectorAll('.sidebar-tab-btn').forEach(btn => btn.classList.remove('active'));
    document.getElementById('tab-btn-' + tabName).classList.add('active');

    document.getElementById('tab-content-steps').style.display = tabName === 'steps' ? 'flex' : 'none';
    document.getElementById('tab-content-premissas').style.display = tabName === 'premissas' ? 'flex' : 'none';
  }}

  function activateStep(netId, element) {{
    document.querySelectorAll('.step-card').forEach(c => c.classList.remove('active'));
    if (element) element.classList.add('active');
    currentFilter = netId;
    applyHighlightFilter();
  }}

  function activatePremissa(netId, element) {{
    document.querySelectorAll('.premissa-card').forEach(c => c.classList.remove('active'));
    if (element) element.classList.add('active');
    currentFilter = netId;
    applyHighlightFilter();
  }}

  function openPremissasModal() {{
    document.getElementById('modal-premissas').classList.add('open');
  }}

  function closePremissasModal() {{
    document.getElementById('modal-premissas').classList.remove('open');
  }}

  function handleModalBackdropClick(event) {{
    if (event.target.id === 'modal-premissas') {{
      closePremissasModal();
    }}
  }}

  function highlightFromPremissa(netId) {{
    closePremissasModal();
    switchSidebarTab('premissas');
    currentFilter = netId;
    applyHighlightFilter();
  }}

  function setupPadInspection() {{
    const hud = document.getElementById('pad-hud');
    if (!hud) return;
    const activePanel = document.querySelector('.view-panel.active');
    if (!activePanel) return;

    activePanel.querySelectorAll('.solder-joint').forEach(pad => {{
      pad.onmouseenter = () => {{
        const col = pad.getAttribute('data-col') || '??';
        const row = pad.getAttribute('data-row') || '??';
        const pin = pad.getAttribute('data-pin') || '';
        const comp = pad.getAttribute('data-comp') || '';
        const desc = pad.getAttribute('data-desc') || '';
        const net = pad.getAttribute('data-net') || 'mech';
        hud.innerHTML = '<span class="hud-tag hud-tag-' + net + '">[Col ' + col.padStart(2, '0') + ', Lin ' + row.padStart(2, '0') + ']</span> <strong>' + comp + '</strong> (' + pin + ') &mdash; <em>' + desc + '</em>';
        hud.classList.add('active');
      }};
      pad.onmouseleave = () => {{
        hud.innerHTML = '<span style="color:#94a3b8;">⚡ Passe o mouse sobre qualquer ponto de solda ou terminal na placa para ver coordenadas e função técnica.</span>';
        hud.classList.remove('active');
      }};
    }});
  }}

  function applyHighlightFilter() {{
    const activePanel = document.querySelector('.view-panel.active');
    if (!activePanel) return;

    const tracks = activePanel.querySelectorAll('.track-line');
    const rings = activePanel.querySelectorAll('.solder-ring');
    const labels = activePanel.querySelectorAll('.solder-lbl');
    const pads = activePanel.querySelectorAll('.solder-joint');

    if (currentFilter === 'all') {{
      tracks.forEach(t => t.classList.remove('dimmed', 'highlighted'));
      rings.forEach(r => r.classList.remove('dimmed', 'highlighted'));
      labels.forEach(l => l.classList.remove('dimmed', 'highlighted'));
      pads.forEach(p => p.classList.remove('dimmed'));
      return;
    }}

    tracks.forEach(t => {{
      if (t.classList.contains('track-' + currentFilter)) {{
        t.classList.remove('dimmed');
        t.classList.add('highlighted');
      }} else {{
        t.classList.remove('highlighted');
        t.classList.add('dimmed');
      }}
    }});

    rings.forEach(r => {{
      if (r.classList.contains('pad-' + currentFilter)) {{
        r.classList.remove('dimmed');
        r.classList.add('highlighted');
      }} else {{
        r.classList.remove('highlighted');
        r.classList.add('dimmed');
      }}
    }});

    labels.forEach(l => {{
      if (l.classList.contains('lbl-' + currentFilter)) {{
        l.classList.remove('dimmed');
        l.classList.add('highlighted');
      }} else {{
        l.classList.remove('highlighted');
        l.classList.add('dimmed');
      }}
    }});

    pads.forEach(p => {{
      if (p.getAttribute('data-net') === currentFilter) {{
        p.classList.remove('dimmed');
      }} else {{
        p.classList.add('dimmed');
      }}
    }});
  }}

  window.addEventListener('keydown', (e) => {{
    if (e.key === 'Escape') {{
      closePremissasModal();
    }} else if (e.key === '+' || e.key === '=') {{
      changeZoom(0.15);
    }} else if (e.key === '-' || e.key === '_') {{
      changeZoom(-0.15);
    }} else if (e.key === '0') {{
      resetZoom();
    }} else if (e.key === '1') {{
      switchMainView('bottom');
    }} else if (e.key === '2') {{
      switchMainView('top');
    }} else if (e.key === '3') {{
      switchMainView('xray');
    }}
  }});

  document.addEventListener('DOMContentLoaded', () => {{
    switchMainView('bottom');
    activateStep('all', document.querySelector('.step-card.active'));
    setupPadInspection();
  }});
</script>

</body>
</html>
'''
    return html


def main():
    svg_top = generate_svg_top()
    with open("placa_shield_superior.svg", "w", encoding="utf-8") as f:
        f.write(svg_top)
    print("Generated placa_shield_superior.svg (v8.4)")

    svg_bottom = generate_svg_bottom_solder()
    with open("placa_shield_inferior.svg", "w", encoding="utf-8") as f:
        f.write(svg_bottom)
    print("Generated placa_shield_inferior.svg (v8.4)")

    html_content = generate_interactive_html(svg_top, svg_bottom)
    with open("placa_shield_visualizador.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Generated placa_shield_visualizador.html (v8.4)")

if __name__ == "__main__":
    main()
