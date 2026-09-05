"""
Gerador de Visualizações e Documentação Gráfica para Placa Shield RC v7.2
Layout Natural Distribuído com Pinagem Física Real do Arduino Nano:
1. Orientação Real do Nano: Conector USB na borda superior externa (Linhas 01-02).
   - Lado Esquerdo (Col 06, Linhas 03 a 17): D13, 3V3, REF, A0, A1, A2, A3, A4 (SDA), A5 (SCL),
     A6, A7, 5V (Pin 27), RST, GND (Pin 29), VIN (Pin 30).
   - Lado Direito (Col 12, Linhas 03 a 17): D12, D11 (P.FD), D10 (P.FE), D9 (Farol), D8 (P.TD),
     D7 (P.TE), D6 (Freio), D5 (Lant), D4 (CH1), D3 (CH4), D2 (CH2), GND (Pin 04), RST, D0/RX, D1/TX.
2. Origem de Energia: VCC (+5V) e GND provêm exclusivamente do Chicote do Rádio (CON1 via CH6 do FS-BS6 / BEC 5.0V do ESC).
3. Conectores Laterais em 90° Face a Face (10mm diretos!):
   - CON1 (Rádio): Lateral Direita (Col 17, Linhas 11 a 15) — face a face com D4, D3, D2 e GND (Col 12).
   - C1 (100uF x 16V): Coluna 15, Linhas 14 e 15 — montado imediatamente colado em CON1 P1 (+5V) e P2 (GND).
   - CON4 (MPU-6050): Lateral Esquerda (Col 02, Linhas 10 a 13) — face a face com A4 (SDA), A5 (SCL), 5V e GND (Col 06).
4. Barramento GND Mestre: 100% interligado e unificado em toda a placa (CON1, C1, Nano GNDs, CON2, CON3 e CON4).
5. Roteamento com Fios Isolados Superiores (Jumpers): Elimina 100% dos curtos-circuitos com integridade geométrica total (Farol D9, Pisca D10, +5V Nano e GND Cross-Tie).
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

    # 1. Linha +5V Mestre (Entra em CON1 P1 Col 17 Lin 15, C1(+) Col 15 Lin 15, contorna por Col 18 e Linha 01 até Col 01, alimenta CON4 P2 e Jumper para Nano 5V)
    vcc_top = [
        (cx(15), cy(15)),  # C1 (+) na entrada
        (cx(17), cy(15)),  # CON1 P1 (+5V do Rádio)
        (cx(18), cy(15)),  # Sobe pela margem Col 18 desimpedida
        (cx(18), cy(1)),   # Topo direito
        (cx(1), cy(1)),    # Topo esquerdo (Linha 01)
        (cx(1), cy(14))    # Desce pela margem externa Coluna 01 até Linha 14
    ]
    draw_top_wire(vcc_top, "#ff4757", 4.5, "vcc", label="+5V Bus Perimetral")
    # Ramal para CON4 P2 (+5V MPU)
    draw_top_wire([(cx(1), cy(12)), (cx(2), cy(12))], "#ff4757", 4.0, "vcc", label="+5V MPU")
    # Jumper isolado de +5V: da Coluna 01 Linha 14 para Nano +5V (Col 06, Lin 14)
    draw_top_jumper([(cx(1), cy(14)), (cx(6), cy(14))], "#ff4757", 3.2, "vcc", label="Jumper +5V")

    # 2. Barramento GND Mestre Unificado
    # Tronco Direito: CON1 P2 (17,14) ➔ C1(-) (15,14) ➔ Nano GND Dir (12,14), desce canal livre Coluna 13 até CON3 P6 (13,24)
    gnd_top_dir = [
        (cx(17), cy(14)),  # CON1 P2 (GND Mestre do Rádio)
        (cx(15), cy(14)),  # C1 (-) na entrada!
        (cx(12), cy(14)),  # Nano GND Dir (Pin 04)
        (cx(13), cy(14)),  # Tronco Coluna 13
        (cx(13), cy(24))   # CON3 P6 (GND Traseiro)
    ]
    draw_top_wire(gnd_top_dir, "#00d26a", 5, "gnd", label="GND Mestre (Do Rádio)")

    # Jumper Cross-Tie de Terra Transversal: liga Nano GND Dir (12,14) a Nano GND Esq (06,16)
    draw_top_jumper([(cx(12), cy(14)), (cx(6), cy(16))], "#00d26a", 3.5, "gnd", label="Jumper GND")

    # Tronco Esquerdo de Terra: Nano GND Esq (06,16) ➔ CON4 P1 (02,13) e Borda Inferior CON2 P1 (03,24)
    gnd_top_esq = [
        (cx(6), cy(16)),   # Nano GND Esq (Pin 29)
        (cx(2), cy(16)),
        (cx(2), cy(13))    # CON4 P1 (GND MPU-6050)
    ]
    draw_top_wire(gnd_top_esq, "#00d26a", 4.5, "gnd", label="GND MPU (Lin 16-13)")

    gnd_front = [
        (cx(2), cy(16)),
        (cx(1), cy(16)),
        (cx(1), cy(24)),   # Desce livre pela margem Col 01
        (cx(3), cy(24))    # CON2 P1 (GND Dianteiro)
    ]
    draw_top_wire(gnd_front, "#00d26a", 4.5, "gnd", label="GND Frente (Col 01)")

    # 3. Sinais de Rádio (CON1 ➔ Nano Col 12): Trilhas 100% retas de 10mm na Lateral Direita!
    draw_top_wire([(cx(17), cy(11)), (cx(12), cy(11))], "#3498db", 3, "radio", label="CH1 (10mm)")
    draw_top_wire([(cx(17), cy(12)), (cx(12), cy(12))], "#2ecc71", 3, "radio", label="CH4 (10mm)")
    draw_top_wire([(cx(17), cy(13)), (cx(12), cy(13))], "#f39c12", 3, "radio", label="CH2 (10mm)")

    # 4. Sinais I2C (Nano Col 06 ➔ CON4 Col 02): Trilhas 100% retas de 10mm na Lateral Esquerda!
    draw_top_wire([(cx(6), cy(10)), (cx(2), cy(10))], "#2ed573", 3, "i2c", label="SDA (10mm)")
    draw_top_wire([(cx(6), cy(11)), (cx(2), cy(11))], "#ffd32a", 3, "i2c", label="SCL (10mm)")

    # 5. Saídas dos LEDs Dianteiros
    # D9 Farol: Jumper isolado superior de Nano D9 (12,06) direto para R1 Top (04,18)
    draw_top_jumper([(cx(12), cy(6)), (cx(4), cy(18))], "#ffffff", 2.8, "led-frente", label="Jumper Farol D9")
    draw_top_wire([(cx(4), cy(21)), (cx(4), cy(24))], "#ffffff", 3.5, "led-frente", label="Farol")

    # D10 Pisca FE: Jumper isolado superior de Nano D10 (12,05) direto para R2 Top (05,18)
    draw_top_jumper([(cx(12), cy(5)), (cx(5), cy(18))], "#ff9f1a", 2.8, "led-frente", label="Jumper Pis.FE D10")
    draw_top_wire([(cx(5), cy(21)), (cx(5), cy(24))], "#ff9f1a", 3.5, "led-frente", label="Pis.FE")

    # D11 Pisca FD: Canal central livre Col 07 até Lin 17 ➔ entra em R3 Top (06,18)
    draw_top_wire([(cx(12), cy(4)), (cx(7), cy(4)), (cx(7), cy(17)), (cx(6), cy(18))], "#1e90ff", 2.5, "led-frente")
    draw_top_wire([(cx(6), cy(21)), (cx(6), cy(24))], "#1e90ff", 3.5, "led-frente", label="Pis.FD")

    # 6. Saídas dos LEDs Traseiros (Nano Col 12 ➔ Trilhas em L Aninhadas ➔ Resistores R4-R7 ➔ CON3)
    # D8 Pisca TD: Col 12 Lin 7 -> Col 8 Lin 7 -> Col 8 Lin 18 (R7 Top)
    draw_top_wire([(cx(12), cy(7)), (cx(8), cy(7)), (cx(8), cy(18))], "#1e90ff", 2.5, "led-tras")
    draw_top_wire([(cx(8), cy(21)), (cx(8), cy(24))], "#1e90ff", 3.5, "led-tras", label="Pis.TD")

    # D7 Pisca TE: Col 12 Lin 8 -> Col 9 Lin 8 -> Col 9 Lin 18 (R6 Top)
    draw_top_wire([(cx(12), cy(8)), (cx(9), cy(8)), (cx(9), cy(18))], "#ffa502", 2.5, "led-tras")
    draw_top_wire([(cx(9), cy(21)), (cx(9), cy(24))], "#ffa502", 3.5, "led-tras", label="Pis.TE")

    # D6 Freio: Col 12 Lin 9 -> Col 10 Lin 9 -> Col 10 Lin 18 (R5 Top)
    draw_top_wire([(cx(12), cy(9)), (cx(10), cy(9)), (cx(10), cy(18))], "#ff4757", 2.5, "led-tras")
    draw_top_wire([(cx(10), cy(21)), (cx(10), cy(24))], "#ff4757", 3.5, "led-tras", label="Freio")

    # D5 Lanterna: Col 12 Lin 10 -> Col 11 Lin 10 -> Col 11 Lin 18 (R4 Top)
    draw_top_wire([(cx(12), cy(10)), (cx(11), cy(10)), (cx(11), cy(18))], "#ff7f50", 2.5, "led-tras")
    draw_top_wire([(cx(11), cy(21)), (cx(11), cy(24))], "#ff7f50", 3.5, "led-tras", label="Lant.")

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

    # Front Resistors R1, R2, R3 (Cols 4, 5, 6, Rows 18-21)
    draw_resistor(4, 18, 21, "R1 100Ω", ["#795548", "#000000", "#795548", "#f1c40f"])
    svg.append(f'<text x="{cx(4)}" y="{cy(22)+4}" text-anchor="middle" fill="#ffffff" font-size="8" font-weight="bold">Farol</text>')

    draw_resistor(5, 18, 21, "R2 150Ω", ["#795548", "#2ecc71", "#795548", "#f1c40f"])
    svg.append(f'<text x="{cx(5)}" y="{cy(22)+4}" text-anchor="middle" fill="#f39c12" font-size="8" font-weight="bold">Pis.FE</text>')

    draw_resistor(6, 18, 21, "R3 150Ω", ["#795548", "#2ecc71", "#795548", "#f1c40f"])
    svg.append(f'<text x="{cx(6)}" y="{cy(22)+4}" text-anchor="middle" fill="#3498db" font-size="8" font-weight="bold">Pis.FD</text>')

    # Rear Resistors R7, R6, R5, R4 (Cols 8, 9, 10, 11, Rows 18-21)
    draw_resistor(8, 18, 21, "R7 150Ω", ["#795548", "#2ecc71", "#795548", "#f1c40f"])
    svg.append(f'<text x="{cx(8)}" y="{cy(22)+4}" text-anchor="middle" fill="#3498db" font-size="8" font-weight="bold">Pis.TD</text>')

    draw_resistor(9, 18, 21, "R6 150Ω", ["#795548", "#2ecc71", "#795548", "#f1c40f"])
    svg.append(f'<text x="{cx(9)}" y="{cy(22)+4}" text-anchor="middle" fill="#f39c12" font-size="8" font-weight="bold">Pis.TE</text>')

    draw_resistor(10, 18, 21, "R5 150Ω", ["#795548", "#2ecc71", "#795548", "#f1c40f"])
    svg.append(f'<text x="{cx(10)}" y="{cy(22)+4}" text-anchor="middle" fill="#ff4757" font-size="8" font-weight="bold">Freio</text>')

    draw_resistor(11, 18, 21, "R4 150Ω", ["#795548", "#2ecc71", "#795548", "#f1c40f"])
    svg.append(f'<text x="{cx(11)}" y="{cy(22)+4}" text-anchor="middle" fill="#e67e22" font-size="8" font-weight="bold">Lant.</text>')

    # ==========================
    # CAPACITOR C1 DE FILTRO / REGULAÇÃO (Coluna 15, Linhas 14 e 15)
    # POSICIONADO DIRETAMENTE NA ENTRADA DO RÁDIO (CON1 P1=+5V / CON1 P2=GND)!
    # ==========================
    cap_cx = cx(15)
    cap_cy = (cy(14) + cy(15)) / 2
    cap_r = 15

    # Pernas de conexão do capacitor
    svg.append(f'<line x1="{cx(15)}" y1="{cy(15)}" x2="{cap_cx}" y2="{cap_cy+cap_r-2}" stroke="#ff4757" stroke-width="2.5"/>')
    svg.append(f'<line x1="{cx(15)}" y1="{cy(14)}" x2="{cap_cx}" y2="{cap_cy-cap_r+2}" stroke="#00d26a" stroke-width="2.5"/>')

    # Corpo cilíndrico do capacitor
    svg.append(f'<circle cx="{cap_cx}" cy="{cap_cy}" r="{cap_r}" fill="url(#capGrad)" stroke="#ff4757" stroke-width="1.8" filter="url(#shadow)"/>')
    # Faixa branca indicadora do polo negativo (GND na linha 14)
    svg.append(f'<path d="M {cap_cx-cap_r+4} {cap_cy-6} A {cap_r} {cap_r} 0 0 1 {cap_cx+cap_r-4} {cap_cy-6} L {cap_cx+cap_r-2} {cap_cy-cap_r+1} A {cap_r} {cap_r} 0 0 0 {cap_cx-cap_r+2} {cap_cy-cap_r+1} Z" fill="#ecf0f1"/>')
    svg.append(f'<text x="{cap_cx}" y="{cap_cy-7}" fill="#000" font-size="8" font-weight="bold" text-anchor="middle">-</text>')
    # Texto C1 e valor
    svg.append(f'<text x="{cap_cx}" y="{cap_cy+1}" fill="#ecf0f1" font-size="7" font-weight="bold" text-anchor="middle">C1 Filtro</text>')
    svg.append(f'<text x="{cap_cx}" y="{cap_cy+9}" fill="#ffd32a" font-size="6.5" font-weight="bold" text-anchor="middle">100µF 16V</text>')
    svg.append(f'<text x="{cap_cx-22}" y="{cy(14)+3}" fill="#00d26a" font-size="7.5" font-weight="bold" text-anchor="end">C1 (-)</text>')
    svg.append(f'<text x="{cap_cx-22}" y="{cy(15)+3}" fill="#ff4757" font-size="7.5" font-weight="bold" text-anchor="end">C1 (+)</text>')

    # ==========================
    # CON1: RÁDIO (Lateral Direita - Coluna 17, Linhas 11 a 15) 90° Apontando para Direita!
    # ENTRADA PRINCIPAL DE VCC (+5V) E GND DO CARRO!
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
        (15, "+5V (BEC)", "#ff4757", "P1")
    ]
    for r, pname, pcolor, pnum in con1_pins:
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
        (10, "SDA", "#2ed573", "P4"),
        (11, "SCL", "#ffd32a", "P3"),
        (12, "+5V", "#ff4757", "P2"),
        (13, "GND", "#00d26a", "P1")
    ]
    for r, pname, pcolor, pnum in con4_pins:
        px = cx(2)
        py = cy(r)
        svg.append(f'<circle cx="{px}" cy="{py}" r="4.5" fill="#f1c40f" stroke="#000" stroke-width="1.2"/>')
        # 90 deg pin pointing left
        svg.append(f'<rect x="{px-35}" y="{py-2.5}" width="35" height="5" rx="1" fill="#f1c40f" stroke="#b7950b" stroke-width="0.8" filter="url(#shadow)"/>')
        svg.append(f'<text x="{px-42}" y="{py+3}" text-anchor="end" fill="{pcolor}" font-size="8.5" font-weight="bold">{pname}</text>')

    # ==========================
    # CON2: CHICOTE DIANTEIRO (Linha 24, Colunas 3 a 6) 90° Apontando para Baixo!
    # ==========================
    con2_x = cx(3) - 12
    con2_y = cy(24) - 12
    con2_w = 3 * pitch + 24
    con2_h = 24
    svg.append(f'<rect x="{con2_x}" y="{con2_y}" width="{con2_w}" height="{con2_h}" rx="3" fill="#1c2833" stroke="#2ecc71" stroke-width="1.8" filter="url(#shadow)"/>')
    svg.append(f'<text x="{con2_x + con2_w/2}" y="{con2_y + 16}" text-anchor="middle" fill="#2ecc71" font-size="9" font-weight="bold">CON2: FRENTE (1x4 90°)</text>')

    con2_pins = [
        (3, "GND", "#00d26a", "P1"),
        (4, "Farol", "#ffffff", "P2"),
        (5, "Pis.FE", "#f39c12", "P3"),
        (6, "Pis.FD", "#3498db", "P4")
    ]
    for c, pname, pcolor, pnum in con2_pins:
        px = cx(c)
        py = cy(24)
        svg.append(f'<circle cx="{px}" cy="{py}" r="4.5" fill="#f1c40f" stroke="#000" stroke-width="1.2"/>')
        svg.append(f'<rect x="{px-2.5}" y="{py}" width="5" height="35" rx="1" fill="#f1c40f" stroke="#b7950b" stroke-width="0.8" filter="url(#shadow)"/>')
        svg.append(f'<text x="{px}" y="{py+48}" text-anchor="middle" fill="{pcolor}" font-size="8" font-weight="bold">{pname}</text>')

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

    # Board Title and Version Legend
    svg.append(f'<text x="{board_w/2}" y="{pcb_y - 45}" text-anchor="middle" fill="#ecf0f1" font-size="16" font-weight="bold">PLACA SHIELD HUB 5x7cm — VISTA SUPERIOR (COMPONENTES &amp; FIAÇÃO)</text>')
    svg.append(f'<text x="{board_w/2}" y="{pcb_y - 25}" text-anchor="middle" fill="#00d26a" font-size="11">Layout Natural Distribuído v7.2 — Pinagem Física Real do Arduino Nano (USB no Topo)</text>')

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
        (6, 10):  ("i2c", "A4", "Nano A4 (SDA)", "Trilha direta horizontal de 10mm para CON4 SDA (Lin 10)"),
        (6, 11):  ("i2c", "A5", "Nano A5 (SCL)", "Trilha direta horizontal de 10mm para CON4 SCL (Lin 11)"),
        (6, 12):  ("mech", "A6", "Nano A6", "Pino 25 do Nano"),
        (6, 13):  ("mech", "A7", "Nano A7", "Pino 26 do Nano"),
        (6, 14):  ("vcc", "+5V", "Nano +5V (Pin 27)", "Terminal do Jumper de +5V vindo da Coluna 01 Linha 14"),
        (6, 15):  ("mech", "RST", "Nano RST", "Pino 28 do Nano"),
        (6, 16):  ("gnd", "GND", "Nano GND Esq (Pin 29)", "Barramento GND Esquerdo & Terminal Jumper GND Cross-Tie"),
        (6, 17):  ("mech", "VIN", "Nano VIN", "Pino 30 do Nano (desconectado)"),

        # Nano Right Header (Pinagem Real: D12..D1/TX na Coluna 12. Espelhado: fica no lado esquerdo visual)
        (12, 3):  ("mech", "D12", "Nano D12 (MISO)", "Pino 15 do Nano"),
        (12, 4):  ("led-frente", "D11", "Nano D11 (Pis.FD)", "Trilha Col 7 para R3 Top"),
        (12, 5):  ("led-frente", "D10", "Nano D10 (Pis.FE)", "Origem do Jumper Pis.FE para R2 Top (Col 05 Lin 18)"),
        (12, 6):  ("led-frente", "D9", "Nano D9 (Farol)", "Origem do Jumper Farol para R1 Top (Col 04 Lin 18)"),
        (12, 7):  ("led-tras", "D8", "Nano D8 (Pis.TD)", "Trilha Col 8 para R7 Top"),
        (12, 8):  ("led-tras", "D7", "Nano D7 (Pis.TE)", "Trilha Col 9 para R6 Top"),
        (12, 9):  ("led-tras", "D6", "Nano D6 (Freio)", "Trilha Col 10 para R5 Top"),
        (12, 10): ("led-tras", "D5", "Nano D5 (Lant)", "Trilha Col 11 para R4 Top"),
        (12, 11): ("radio", "D4", "Nano D4 (CH1)", "Trilha direta horizontal de 10mm para CON1 P5 (Lin 11)"),
        (12, 12): ("radio", "D3", "Nano D3 (CH4)", "Trilha direta horizontal de 10mm para CON1 P4 (Lin 12)"),
        (12, 13): ("radio", "D2", "Nano D2 (CH2)", "Trilha direta horizontal de 10mm para CON1 P3 (Lin 13)"),
        (12, 14): ("gnd", "GND", "Nano GND Dir (Pin 04)", "Barramento GND Direito & Origem Jumper GND Cross-Tie"),
        (12, 16): ("mech", "D0", "Nano D0/RX", "Pino serial RX"),
        (12, 17): ("mech", "D1", "Nano D1/TX", "Pino serial TX"),

        # CON1: Rádio (Lateral Direita - Coluna 17, Linhas 11 a 15) — ENTRADA DE ENERGIA MESTRE
        (17, 11): ("radio", "CON1 P5", "CON1 CH1 (Vol)", "Trilha direta horizontal para Nano D4 (10mm, Lin 11)"),
        (17, 12): ("radio", "CON1 P4", "CON1 CH4 (Farol)", "Trilha direta horizontal para Nano D3 (10mm, Lin 12)"),
        (17, 13): ("radio", "CON1 P3", "CON1 CH2 (Thr)", "Trilha direta horizontal para Nano D2 (10mm, Lin 13)"),
        (17, 14): ("gnd", "CON1 P2", "CON1 GND Mestre", "Entrada de GND Mestre do rádio no Barramento de Terra"),
        (17, 15): ("vcc", "CON1 P1", "CON1 +5V (BEC)", "Entrada de +5V Mestre do ESC/Receptor via CH6 (liga a C1+ e Col 18)"),

        # Capacitor C1 (Coluna 15, Linhas 14 e 15) — LOCALIZADO NA ENTRADA DA ALIMENTAÇÃO
        (15, 14): ("gnd", "C1 (-)", "Capacitor C1 (-)", "Solda do polo negativo do capacitor no GND Mestre de CON1"),
        (15, 15): ("vcc", "C1 (+)", "Capacitor C1 (+)", "Solda do polo positivo do capacitor na entrada de +5V de CON1"),

        # CON4: MPU-6050 (Lateral Esquerda - Coluna 02, Linhas 10 a 13)
        (2, 10):  ("i2c", "CON4 P4", "CON4 SDA", "Trilha direta horizontal para Nano A4 (10mm, Lin 10)"),
        (2, 11):  ("i2c", "CON4 P3", "CON4 SCL", "Trilha direta horizontal para Nano A5 (10mm, Lin 11)"),
        (2, 12):  ("vcc", "CON4 P2", "CON4 +5V", "Alimentação +5V do acelerômetro via ramal da Coluna 01"),
        (2, 13):  ("gnd", "CON4 P1", "CON4 GND", "Solda de terra do acelerômetro no Barramento GND"),

        # Resistores Dianteiros R1, R2, R3 (Cols 4, 5, 6, Rows 18 e 21)
        (4, 18):  ("led-frente", "R1 Top", "R1 Top (Farol 100Ω)", "Terminal do Jumper vindo de Nano D9"),
        (4, 21):  ("led-frente", "R1 Bot", "R1 Bot (Farol)", "Trilha direta vertical para CON2 Pino 2"),
        (5, 18):  ("led-frente", "R2 Top", "R2 Top (Pis.FE 150Ω)", "Terminal do Jumper vindo de Nano D10"),
        (5, 21):  ("led-frente", "R2 Bot", "R2 Bot (Pis.FE)", "Trilha direta vertical para CON2 Pino 3"),
        (6, 18):  ("led-frente", "R3 Top", "R3 Top (Pis.FD 150Ω)", "Entrada vinda de Nano D11 via Col 07"),
        (6, 21):  ("led-frente", "R3 Bot", "R3 Bot (Pis.FD)", "Trilha direta vertical para CON2 Pino 4"),

        # Resistores Traseiros R7, R6, R5, R4 (Cols 8, 9, 10, 11, Rows 18 e 21)
        (8, 18):  ("led-tras", "R7 Top", "R7 Top (Pis.TD 150Ω)", "Entrada vinda de Nano D8 (Lin 7)"),
        (8, 21):  ("led-tras", "R7 Bot", "R7 Bot (Pis.TD)", "Trilha direta vertical para CON3 Pino 1"),
        (9, 18):  ("led-tras", "R6 Top", "R6 Top (Pis.TE 150Ω)", "Entrada vinda de Nano D7 (Lin 8)"),
        (9, 21):  ("led-tras", "R6 Bot", "R6 Bot (Pis.TE)", "Trilha direta vertical para CON3 Pino 2"),
        (10, 18): ("led-tras", "R5 Top", "R5 Top (Freio 150Ω)", "Entrada vinda de Nano D6 (Lin 9)"),
        (10, 21): ("led-tras", "R5 Bot", "R5 Bot (Freio)", "Trilha direta vertical para CON3 Pino 3"),
        (11, 18): ("led-tras", "R4 Top", "R4 Top (Lant. 150Ω)", "Entrada vinda de Nano D5 (Lin 10)"),
        (11, 21): ("led-tras", "R4 Bot", "R4 Bot (Lant.)", "Trilha direta vertical para CON3 Pino 4"),

        # CON2: Chicote Dianteiro (Linha 24, Colunas 3 a 6)
        (3, 24):  ("gnd", "CON2 P1", "CON2 GND", "Solda de terra comum do chicote dianteiro vinda de Col 01"),
        (4, 24):  ("led-frente", "CON2 P2", "CON2 Farol", "Alimentação dos faróis dianteiros"),
        (5, 24):  ("led-frente", "CON2 P3", "CON2 Pis.FE", "Alimentação do pisca dianteiro esquerdo"),
        (6, 24):  ("led-frente", "CON2 P4", "CON2 Pis.FD", "Alimentação do pisca dianteiro direito"),

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

    # Helper: draw heavy solder track
    def draw_solder_track(points, color, width, net_id, label=""):
        d_str = "M " + " L ".join([f"{p[0]} {p[1]}" for p in points])
        svg.append(f'<path class="track-line track-{net_id}" d="{d_str}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" opacity="0.92" filter="url(#busGlow)"/>')
        if label and len(points) >= 2:
            mid_x = (points[0][0] + points[-1][0]) / 2
            mid_y = (points[0][1] + points[-1][1]) / 2
            svg.append(f'<text class="solder-lbl lbl-{net_id}" x="{mid_x}" y="{mid_y-6}" text-anchor="middle" fill="{color}" font-size="8.5" font-weight="bold" pointer-events="none">{label}</text>')

    def draw_bottom_jumper_guide(points, color, width, net_id, label=""):
        d_str = "M " + " L ".join([f"{p[0]} {p[1]}" for p in points])
        svg.append(f'<path class="track-line track-{net_id} jumper-guide" d="{d_str}" fill="none" stroke="{color}" stroke-width="{width}" stroke-dasharray="5,4" stroke-linecap="round" stroke-linejoin="round" opacity="0.55"/>')
        for p in [points[0], points[-1]]:
            svg.append(f'<circle cx="{p[0]}" cy="{p[1]}" r="4.5" fill="none" stroke="{color}" stroke-width="1.8"/>')
        if label and len(points) >= 2:
            mid_x = (points[0][0] + points[-1][0]) / 2
            mid_y = (points[0][1] + points[-1][1]) / 2
            svg.append(f'<text class="solder-lbl lbl-{net_id}" x="{mid_x}" y="{mid_y-5}" text-anchor="middle" fill="{color}" font-size="7.5" font-style="italic" opacity="0.8" pointer-events="none">({label})</text>')

    svg.append('<g id="solder-tracks-layer">')

    # ==========================================
    # 1. 📡 SINAIS DO RÁDIO (CON1: Lateral Direita - Coluna 17, Linhas 11 a 13 ➔ Nano Col 12) — APENAS 10mm!
    # ==========================================
    draw_solder_track([(cx(17), cy(11)), (cx(12), cy(11))], "#3498db", 3.5, "radio", label="D4/CH1 (10mm)")
    draw_solder_track([(cx(17), cy(12)), (cx(12), cy(12))], "#2ecc71", 3.5, "radio", label="D3/CH4 (10mm)")
    draw_solder_track([(cx(17), cy(13)), (cx(12), cy(13))], "#f39c12", 3.5, "radio", label="D2/CH2 (10mm)")

    # ==========================================
    # 2. 🧭 TRILHAS DO MPU-6050 (CON4: Lateral Esquerda - Coluna 02, Linhas 10 e 11 ➔ Nano Col 06) — APENAS 10mm!
    # ==========================================
    draw_solder_track([(cx(2), cy(10)), (cx(6), cy(10))], "#2ed573", 3.5, "i2c", label="SDA (10mm)")
    draw_solder_track([(cx(2), cy(11)), (cx(6), cy(11))], "#ffd32a", 3.5, "i2c", label="SCL (10mm)")

    # ==========================================
    # 3. 🔴 LINHA +5V (ALIMENTAÇÃO VCC DO RÁDIO VIA CON1 COM C1 NA ENTRADA)
    # ==========================================
    vcc_track = [
        (cx(15), cy(15)),  # C1 (+) Soldado na entrada
        (cx(17), cy(15)),  # CON1 P1 (+5V Entrada Mestre)
        (cx(18), cy(15)),  # Contorna por Col 18 desimpedida
        (cx(18), cy(1)),   # Sobe até Linha 01 no topo
        (cx(1), cy(1)),    # Cruza topo até Coluna 01
        (cx(1), cy(14))    # Desce pela margem Col 01 até Linha 14
    ]
    draw_solder_track(vcc_track, "#ff4757", 5.5, "vcc", label="+5V BUS (Perímetro Col 18/Lin 01/Col 01)")
    # Ramal para CON4 P2 (+5V MPU)
    draw_solder_track([(cx(1), cy(12)), (cx(2), cy(12))], "#ff4757", 4.5, "vcc", label="+5V MPU")
    # Indicação do Jumper isolado superior de +5V para Nano +5V
    draw_bottom_jumper_guide([(cx(1), cy(14)), (cx(6), cy(14))], "#ff4757", 2.2, "vcc", label="Jumper +5V (Face Sup.)")

    # ==========================================
    # 4. ⚡ BARRAMENTO DE NEUTRO MESTRE (GND UNIFICADO E 100% INTERLIGADO)
    # ==========================================
    # Tronco Direito: CON1 P2 GND (Col 17, Lin 14) une a C1(-) (Col 15, Lin 14) e Nano GND Dir (Col 12, Lin 14)
    gnd_right = [
        (cx(17), cy(14)),  # CON1 P2 (GND Mestre do Rádio)
        (cx(15), cy(14)),  # C1 (-) Soldado na entrada!
        (cx(12), cy(14))   # Nano GND Dir (Pin 04)
    ]
    draw_solder_track(gnd_right, "#00d26a", 5.5, "gnd", label="GND Mestre (Do Rádio)")

    # Canal livre Coluna 13 desce reto até CON3 P6 GND (Trás)
    draw_solder_track([(cx(13), cy(14)), (cx(13), cy(24))], "#00d26a", 5.0, "gnd", label="GND Canal Col 13")

    # Jumper Cross-Tie de Terra Transversal (Face Superior)
    draw_bottom_jumper_guide([(cx(12), cy(14)), (cx(6), cy(16))], "#00d26a", 2.5, "gnd", label="Jumper GND Cross-Tie (Face Sup.)")

    # Tronco Esquerdo: Nano GND Esq Col 06 Linha 16 cruza desimpedido até Coluna 02 e sobe até CON4 P1 (MPU)
    gnd_left = [
        (cx(6), cy(16)),   # Nano GND Esq (Pin 29)
        (cx(2), cy(16)),
        (cx(2), cy(13))    # CON4 P1 GND (MPU-6050)
    ]
    draw_solder_track(gnd_left, "#00d26a", 4.5, "gnd", label="Ponte GND (Lin 16-13)")

    # Desce pela margem externa Coluna 01 até CON2 P1 (Frente)
    gnd_front = [
        (cx(2), cy(16)),
        (cx(1), cy(16)),   # Margem externa Coluna 01
        (cx(1), cy(24)),   # Desce livre pela margem esquerda
        (cx(3), cy(24))    # Entra em CON2 P1 GND (Frente)
    ]
    draw_solder_track(gnd_front, "#00d26a", 5, "gnd", label="GND Frente (Col 01)")

    # ==========================================
    # 5. 💡 LEDS DIANTEIROS (CON2: Linha 24, Cols 3 a 6)
    # ==========================================
    # D9 Farol: Jumper Face Superior de Nano D9 (12,06) direto para R1 Top (04,18)
    draw_bottom_jumper_guide([(cx(12), cy(6)), (cx(4), cy(18))], "#ffffff", 2.2, "led-frente", label="Jumper D9 (Face Sup.)")
    draw_solder_track([(cx(4), cy(21)), (cx(4), cy(24))], "#ffffff", 4.5, "led-frente", label="Farol")

    # D10 Pisca FE: Jumper Face Superior de Nano D10 (12,05) direto para R2 Top (05,18)
    draw_bottom_jumper_guide([(cx(12), cy(5)), (cx(5), cy(18))], "#ff9f1a", 2.2, "led-frente", label="Jumper D10 (Face Sup.)")
    draw_solder_track([(cx(5), cy(21)), (cx(5), cy(24))], "#ff9f1a", 4.5, "led-frente", label="Pis.FE")

    # D11 Pisca FD: Col 12 Lin 4 -> corre livre na Lin 4 até Col 7 -> desce até Lin 17 -> entra em R3 Top (Col 6 Lin 18)
    draw_solder_track([(cx(12), cy(4)), (cx(7), cy(4)), (cx(7), cy(17)), (cx(6), cy(18))], "#1e90ff", 3, "led-frente", label="D11")
    draw_solder_track([(cx(6), cy(21)), (cx(6), cy(24))], "#1e90ff", 4.5, "led-frente", label="Pis.FD")

    # ==========================================
    # 6. 💡 LEDS TRASEIROS (CON3: Linha 24, Cols 8 a 13) — TRILHAS "L" ANINHADAS (ZERO CRUZAMENTOS!)
    # ==========================================
    draw_solder_track([(cx(12), cy(7)), (cx(8), cy(7)), (cx(8), cy(18))], "#1e90ff", 3, "led-tras", label="D8")
    draw_solder_track([(cx(8), cy(21)), (cx(8), cy(24))], "#1e90ff", 4.5, "led-tras")

    draw_solder_track([(cx(12), cy(8)), (cx(9), cy(8)), (cx(9), cy(18))], "#ffa502", 3, "led-tras", label="D7")
    draw_solder_track([(cx(9), cy(21)), (cx(9), cy(24))], "#ffa502", 4.5, "led-tras")

    draw_solder_track([(cx(12), cy(9)), (cx(10), cy(9)), (cx(10), cy(18))], "#ff4757", 3, "led-tras", label="D6")
    draw_solder_track([(cx(10), cy(21)), (cx(10), cy(24))], "#ff4757", 4.5, "led-tras")

    draw_solder_track([(cx(12), cy(10)), (cx(11), cy(10)), (cx(11), cy(18))], "#ff7f50", 3, "led-tras", label="D5")
    draw_solder_track([(cx(11), cy(21)), (cx(11), cy(24))], "#ff7f50", 4.5, "led-tras")

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
        elif col == 15 and (row == 14 or row == 15):
            lbl_x = x - 24
            lbl_y = y + 3
        elif col == 17:
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
    svg.append(f'<text x="{board_w/2}" y="{pcb_y - 25}" text-anchor="middle" fill="#2ed573" font-size="11">Layout Natural Distribuído v7.2 — Vista Espelhada Horizontal (Como Você Vê ao Soldar)</text>')

    svg.append('</svg>')
    return "".join(svg)


def generate_interactive_html(svg_top_str, svg_bottom_str):
    html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Placa Shield Hub 5x7cm (v7.2) — Visualizador Interativo &amp; Premissas</title>
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
      --led-front: #ffffff;
      --led-rear: #ff7f50;
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
      color: var(--text-main);
      background: var(--bg-panel);
      border-bottom: 2px solid var(--primary);
    }}
    .sidebar-content {{
      padding: 14px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 12px;
      flex: 1;
    }}
    .step-card, .premissa-card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 12px;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .step-card:hover, .premissa-card:hover {{
      border-color: #60a5fa;
      transform: translateY(-1px);
    }}
    .step-card.active, .premissa-card.active {{
      border-color: var(--primary);
      background: #1e293b;
      box-shadow: 0 0 12px rgba(59, 130, 246, 0.3);
    }}
    .step-header, .premissa-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 6px;
      font-weight: 600;
      font-size: 0.88rem;
    }}
    .step-badge, .premissa-badge {{
      font-size: 0.68rem;
      padding: 2px 6px;
      border-radius: 4px;
      font-weight: bold;
    }}
    .step-desc, .premissa-desc {{
      font-size: 0.78rem;
      color: var(--text-muted);
      line-height: 1.45;
    }}
    .step-pads-list, .premissa-tags {{
      display: flex;
      flex-wrap: wrap;
      gap: 4px;
      margin-top: 8px;
    }}
    .pad-tag, .premissa-tag {{
      background: #0f172a;
      border: 1px solid #334155;
      font-size: 0.68rem;
      padding: 1px 6px;
      border-radius: 3px;
      color: #94a3b8;
    }}
    .premissa-tag-active {{
      background: rgba(16, 185, 129, 0.15);
      border-color: rgba(52, 211, 153, 0.4);
      color: #34d399;
    }}
    .viewer-area {{
      background: #030708;
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
      overflow: auto;
      padding: 16px;
    }}
    .svg-container {{
      max-width: 100%;
      max-height: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.3s ease;
    }}
    .svg-container svg {{
      display: block;
      width: 100%;
      height: auto;
      max-height: 85vh;
    }}
    .view-panel {{ display: none; }}
    .view-panel.active {{ display: block; }}

    .dimmed {{ opacity: 0.08 !important; transition: opacity 0.2s; }}
    .highlight-focus {{
      stroke-width: 4px !important;
      animation: pulseGlow 1.2s infinite alternate;
    }}
    @keyframes pulseGlow {{
      from {{ filter: drop-shadow(0 0 2px currentColor); }}
      to {{ filter: drop-shadow(0 0 10px currentColor); }}
    }}

    /* MODAL DE PREMISSAS NORMATIVAS */
    .modal-backdrop {{
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background: rgba(3, 7, 18, 0.82);
      backdrop-filter: blur(12px);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 1000;
      padding: 20px;
    }}
    .modal-backdrop.open {{
      display: flex;
    }}
    .modal-card {{
      background: #0f172a;
      border: 1px solid var(--border);
      border-radius: 12px;
      width: 100%;
      max-width: 900px;
      max-height: 90vh;
      display: flex;
      flex-direction: column;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
      overflow: hidden;
    }}
    .modal-header {{
      background: #1e293b;
      border-bottom: 1px solid var(--border);
      padding: 16px 22px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}
    .modal-header h2 {{
      font-size: 1.15rem;
      color: #f8fafc;
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .modal-close-btn {{
      background: transparent;
      border: none;
      color: #94a3b8;
      font-size: 1.5rem;
      cursor: pointer;
      padding: 0 6px;
      border-radius: 4px;
      transition: all 0.2s;
    }}
    .modal-close-btn:hover {{
      color: white;
      background: rgba(255, 255, 255, 0.1);
    }}
    .modal-body {{
      padding: 20px 24px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}
    .norm-block {{
      background: #1e293b;
      border: 1px solid #334155;
      border-radius: 8px;
      padding: 16px;
      transition: all 0.2s;
    }}
    .norm-block:hover {{
      border-color: #60a5fa;
    }}
    .norm-title {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 0.96rem;
      font-weight: 700;
      margin-bottom: 8px;
    }}
    .norm-text {{
      font-size: 0.84rem;
      color: #cbd5e1;
      line-height: 1.5;
    }}
    .norm-table {{
      width: 100%;
      border-collapse: collapse;
      margin-top: 10px;
      font-size: 0.78rem;
    }}
    .norm-table th, .norm-table td {{
      padding: 6px 10px;
      text-align: left;
      border-bottom: 1px solid #334155;
    }}
    .norm-table th {{
      background: #0f172a;
      color: #94a3b8;
      font-weight: 600;
    }}
    .norm-btn {{
      margin-top: 10px;
      background: #0f172a;
      border: 1px solid #3b82f6;
      color: #93c5fd;
      padding: 5px 12px;
      border-radius: 6px;
      font-size: 0.75rem;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }}
    .norm-btn:hover {{
      background: #1e3a8a;
      color: white;
    }}
  </style>
</head>
<body>

<header>
  <div class="header-title">
    <h1>PLACA SHIELD HUB 5x7cm</h1>
    <span class="badge">v7.2 Distribuído Natural</span>
    <span class="badge-norm">5 Premissas de Engenharia Ativas</span>
    <span style="font-size:0.75rem; color:var(--text-muted);">Arduino Nano Real (docs.arduino.cc)</span>
  </div>

  <div class="controls">
    <button class="btn-premissas-modal" onclick="openPremissasModal()">
      <span>📜 Premissas Normativas</span>
    </button>
    <div class="btn-group">
      <button id="btn-bottom" class="active" onclick="switchMainView('bottom')">🔄 Solda (Verso)</button>
      <button id="btn-top" onclick="switchMainView('top')">🖼️ Componentes (Topo)</button>
      <button id="btn-xray" onclick="switchMainView('xray')">⚡ Raio-X</button>
    </div>
  </div>
</header>

<div class="main-layout">
  <div class="sidebar">
    <div class="sidebar-tabs">
      <button id="tab-btn-steps" class="sidebar-tab-btn active" onclick="switchSidebarTab('steps')">
        🛠️ Roteiro de Solda
      </button>
      <button id="tab-btn-premissas" class="sidebar-tab-btn" onclick="switchSidebarTab('premissas')">
        📜 Premissas (5)
      </button>
    </div>

    <!-- ABA 1: ROTEIRO DE SOLDA PASSO A PASSO -->
    <div id="tab-content-steps" class="sidebar-content">
      <div style="font-size:0.75rem; text-transform:uppercase; letter-spacing:1px; color:var(--text-muted); font-weight:bold;">
        Passos Sequenciais na Bancada
      </div>

      <div class="step-card active" onclick="activateStep('all', this)">
        <div class="step-header">
          <span>👁️ Exibir Todos os Circuitos</span>
          <span class="step-badge" style="background:#334155; color:#fff;">Completo</span>
        </div>
        <div class="step-desc">Visualização global de todas as conexões, trilhas de cobre e componentes da placa.</div>
      </div>

      <div class="step-card" onclick="activateStep('radio', this)">
        <div class="step-header" style="color:var(--radio);">
          <span>1️⃣ Rádio CH1, CH4, CH2 (Lateral Direita)</span>
          <span class="step-badge" style="background:rgba(255,211,42,0.2); color:var(--radio);">10mm Diretos</span>
        </div>
        <div class="step-desc">
          CON1 fica na <strong>Coluna 17 (Linhas 11 a 15)</strong>, face a face com os pinos D4, D3, D2 do Nano na Coluna 12. Trilhas horizontais retas sem cruzamentos!
        </div>
        <div class="step-pads-list">
          <span class="pad-tag">CON1 P5 ➔ Nano D4 (Lin 11)</span>
          <span class="pad-tag">CON1 P4 ➔ Nano D3 (Lin 12)</span>
          <span class="pad-tag">CON1 P3 ➔ Nano D2 (Lin 13)</span>
        </div>
      </div>

      <div class="step-card" onclick="activateStep('i2c', this)">
        <div class="step-header" style="color:var(--i2c);">
          <span>2️⃣ MPU-6050 SDA &amp; SCL (Lateral Esquerda)</span>
          <span class="step-badge" style="background:rgba(46,213,115,0.2); color:var(--i2c);">10mm Diretos</span>
        </div>
        <div class="step-desc">
          CON4 fica na <strong>Coluna 02 (Linhas 10 a 13)</strong>, face a face com os pinos I2C A4 (SDA) e A5 (SCL) do Nano na Coluna 06.
        </div>
        <div class="step-pads-list">
          <span class="pad-tag">CON4 P4 ➔ Nano A4 (Lin 10)</span>
          <span class="pad-tag">CON4 P3 ➔ Nano A5 (Lin 11)</span>
        </div>
      </div>

      <div class="step-card" onclick="activateStep('vcc', this)">
        <div class="step-header" style="color:var(--vcc);">
          <span>3️⃣ Linha +5V &amp; C1 (Filtragem na Entrada &amp; Rota Perimetral)</span>
          <span class="step-badge" style="background:rgba(255,71,87,0.2); color:var(--vcc);">Premissa #1 &amp; #2</span>
        </div>
        <div class="step-desc">
          <strong>Origem Única de VCC:</strong> O +5V entra por CON1 P1 (Col 17, Lin 15) com C1 (100uF x 16V) em (15,15). A trilha de cobre contorna pela margem livre Coluna 18, sobe até Linha 01 no topo, cruza até Coluna 01 na esquerda e desce até Linha 14 (alimentando CON4 P2 em 02,12). Um <strong>jumper isolado superior</strong> salta da Coluna 01 Linha 14 diretamente para o Nano 5V (Col 06, Lin 14).
        </div>
        <div class="step-pads-list">
          <span class="pad-tag">CON1 P1 (+5V BEC, 17,15)</span>
          <span class="pad-tag">C1 (+) Entrada (15,15)</span>
          <span class="pad-tag">Margem Col 18 ➔ Topo Lin 01</span>
          <span class="pad-tag">Margem Esq Col 01 ➔ CON4 P2 (02,12)</span>
          <span class="pad-tag">Jumper 5V ➔ Nano 5V (06,14)</span>
        </div>
      </div>

      <div class="step-card" onclick="activateStep('gnd', this)">
        <div class="step-header" style="color:var(--gnd);">
          <span>4️⃣ Barramento GND Mestre Unificado</span>
          <span class="step-badge" style="background:rgba(0,210,106,0.2); color:var(--gnd);">Premissas #1 &amp; #3</span>
        </div>
        <div class="step-desc">
          <strong>Premissa de Terra:</strong> O GND Mestre entra por CON1 P2 (Col 17, Lin 14), passa por C1(-) (Col 15, Lin 14) e conecta-se a Nano GND Dir (12,14). O canal livre Coluna 13 desce até CON3 P6 (13,24). Um <strong>jumper de terra transversal</strong> une Nano GND Dir (12,14) a Nano GND Esq (06,16). Na esquerda, a trilha estanhada conecta a CON4 P1 (02,13) e desce pela margem Coluna 01 até CON2 P1 (03,24).
        </div>
        <div class="step-pads-list">
          <span class="pad-tag">CON1 P2 (GND Mestre, 17,14)</span>
          <span class="pad-tag">C1 (-) Entrada (15,14)</span>
          <span class="pad-tag">Nano GND Dir (12,14)</span>
          <span class="pad-tag">Canal Col 13 ➔ CON3 P6 (13,24)</span>
          <span class="pad-tag">Jumper GND (12,14 ➔ 06,16)</span>
          <span class="pad-tag">Nano GND Esq (06,16) ➔ CON4 P1 (02,13)</span>
          <span class="pad-tag">Margem Col 01 ➔ CON2 P1 (03,24)</span>
        </div>
      </div>

      <div class="step-card" onclick="activateStep('led-frente', this)">
        <div class="step-header" style="color:#ffffff;">
          <span>5️⃣ LEDs Dianteiros (Jumpers Diretos &amp; Canal Central)</span>
          <span class="step-badge" style="background:rgba(255,255,255,0.2); color:#fff;">Zero Conflitos</span>
        </div>
        <div class="step-desc">
          D9 (Farol) e D10 (Pis.FE) utilizam <strong>fios isolados superiores (jumpers)</strong> diretos de Nano D9 (12,06) para R1 Top (04,18) e de Nano D10 (12,05) para R2 Top (05,18), saltando sobre o Nano e evitando cruzamentos com trilhas de cobre. D11 corre pelo canal central livre Col 07 até R3 Top (06,18).
        </div>
        <div class="step-pads-list">
          <span class="pad-tag">Jumper D9 ➔ R1 (100Ω) ➔ CON2 P2 (Farol)</span>
          <span class="pad-tag">Jumper D10 ➔ R2 (150Ω) ➔ CON2 P3 (Pis.FE)</span>
          <span class="pad-tag">Trilha D11 ➔ R3 (150Ω) ➔ CON2 P4 (Pis.FD)</span>
        </div>
      </div>

      <div class="step-card" onclick="activateStep('led-tras', this)">
        <div class="step-header" style="color:var(--led-rear);">
          <span>6️⃣ LEDs Traseiros (Trilhas em "L" Aninhadas)</span>
          <span class="step-badge" style="background:rgba(255,127,80,0.2); color:var(--led-rear);">Zero Cruzamento</span>
        </div>
        <div class="step-desc">
          D5, D6, D7, D8 saem do Nano Col 12 (Linhas 07 a 10) e formam trilhas em "L" paralelas e perfeitamente aninhadas até R4 a R7 (Linhas 18 a 21) e CON3 (Linha 24, Colunas 8 a 13).
        </div>
        <div class="step-pads-list">
          <span class="pad-tag">D8 ➔ R7 (150Ω) ➔ CON3 P1 (Pis.TD)</span>
          <span class="pad-tag">D7 ➔ R6 (150Ω) ➔ CON3 P2 (Pis.TE)</span>
          <span class="pad-tag">D6 ➔ R5 (150Ω) ➔ CON3 P3 (Freio)</span>
          <span class="pad-tag">D5 ➔ R4 (150Ω) ➔ CON3 P4 (Lant.)</span>
        </div>
      </div>
    </div>

    <!-- ABA 2: 5 PREMISSAS OFICIAIS DE PROJETO -->
    <div id="tab-content-premissas" class="sidebar-content" style="display:none;">
      <div style="font-size:0.75rem; text-transform:uppercase; letter-spacing:1px; color:#34d399; font-weight:bold;">
        Regras Inegociáveis de Engenharia
      </div>

      <div class="premissa-card" onclick="activatePremissa('vcc', this)">
        <div class="premissa-header" style="color:var(--vcc);">
          <span>⚡ Premissa #1: Origem de Energia</span>
          <span class="premissa-badge" style="background:rgba(255,71,87,0.2); color:var(--vcc);">CON1 / CH6</span>
        </div>
        <div class="premissa-desc">
          Toda a alimentação provém exclusivamente de <strong>CON1 via CH6 do Rádio</strong> (BEC 5.0V / 3A máx). Nenhum outro conector alimenta a placa. Pino <strong>VIN desconectado</strong>; Nano é alimentado no pino 5V. Consumo total: <strong>~162mA</strong>.
        </div>
        <div class="premissa-tags">
          <span class="premissa-tag premissa-tag-active">BEC 5.0V (máx 5.5V)</span>
          <span class="premissa-tag">Diodo 1N4007 p/ BEC 6V</span>
          <span class="premissa-tag">CON1 P1 (+5V)</span>
          <span class="premissa-tag">CON1 P2 (GND)</span>
        </div>
      </div>

      <div class="premissa-card" onclick="activatePremissa('vcc', this)">
        <div class="premissa-header" style="color:#ffd32a;">
          <span>🔋 Premissa #2: Regulação C1 na Entrada</span>
          <span class="premissa-badge" style="background:rgba(255,211,42,0.2); color:#ffd32a;">Col 15 (14-15)</span>
        </div>
        <div class="premissa-desc">
          Capacitor eletrolítico <strong>C1 (100µF x 16V)</strong> soldado diretamente na entrada colado a CON1 P1/P2 e Nano GND. Absorve ruído EMI e brownouts gerados por servo de direção e motor.
        </div>
        <div class="premissa-tags">
          <span class="premissa-tag premissa-tag-active">C1 (+) Col 15 Lin 15</span>
          <span class="premissa-tag premissa-tag-active">C1 (-) Col 15 Lin 14</span>
          <span class="premissa-tag">Filtro de Brownouts</span>
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
        <div class="premissa-tags">
          <span class="premissa-tag premissa-tag-active">Continuidade Independente</span>
          <span class="premissa-tag">CON1 P2 Central</span>
          <span class="premissa-tag">Nano GND Dir &amp; Esq</span>
          <span class="premissa-tag">Malha Traseira &amp; Frente</span>
        </div>
      </div>

      <div class="premissa-card" onclick="activatePremissa('all', this)">
        <div class="premissa-header" style="color:#a855f7;">
          <span>📐 Premissa #4: Roteamento Híbrido &amp; 4 Jumpers</span>
          <span class="premissa-badge" style="background:rgba(168,85,247,0.2); color:#a855f7;">0 Curtos</span>
        </div>
        <div class="premissa-desc">
          Pinagem real do Nano (USB no topo). Trilhas retas de 10mm para Rádio e MPU no verso. <strong>4 fios isolados superiores (W1-W4)</strong> saltam sobre componentes sem compartilhar cobre, eliminando 100% dos curtos-circuitos.
        </div>
        <div class="premissa-tags">
          <span class="premissa-tag premissa-tag-active">W1: +5V (13mm)</span>
          <span class="premissa-tag premissa-tag-active">W2: D9 Farol (36mm)</span>
          <span class="premissa-tag premissa-tag-active">W3: D10 Pis.FE (38mm)</span>
          <span class="premissa-tag premissa-tag-active">W4: GND Cross (16mm)</span>
        </div>
      </div>

      <div class="premissa-card" onclick="activatePremissa('radio', this)">
        <div class="premissa-header" style="color:#38bdf8;">
          <span>🔌 Premissa #5: Conectores em 90° nas Bordas</span>
          <span class="premissa-badge" style="background:rgba(56,189,248,0.2); color:#38bdf8;">MODU 90°</span>
        </div>
        <div class="premissa-desc">
          Todos os conectores utilizam barras de pinos macho em 90° voltadas para fora: CON1 à direita, CON4 à esquerda, CON2/CON3 na borda inferior e USB no topo. Desconexão em &lt;5s na pista sem retirar a bolha.
        </div>
        <div class="premissa-tags">
          <span class="premissa-tag premissa-tag-active">CON1: Direita</span>
          <span class="premissa-tag premissa-tag-active">CON4: Esquerda</span>
          <span class="premissa-tag premissa-tag-active">CON2 &amp; CON3: Borda Inferior</span>
          <span class="premissa-tag">USB: Borda Superior</span>
        </div>
      </div>

      <button class="norm-btn" style="width:100%; justify-content:center; padding:10px; margin-top:6px;" onclick="openPremissasModal()">
        📖 Abrir Memorial de Cálculo &amp; Detalhes Normativos
      </button>
    </div>
  </div>

  <div class="viewer-area">
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
  </div>
</div>

<!-- MODAL COM O TEXTO COMPLETO DAS 5 PREMISSAS DE PROJETO -->
<div id="modal-premissas" class="modal-backdrop" onclick="handleModalBackdropClick(event)">
  <div class="modal-card">
    <div class="modal-header">
      <h2>📜 Premissas Fundamentais de Engenharia (v7.2)</h2>
      <button class="modal-close-btn" onclick="closePremissasModal()">&times;</button>
    </div>
    <div class="modal-body">
      <div style="background:#0f172a; border-left:4px solid #10b981; padding:10px 14px; border-radius:4px; font-size:0.82rem; color:#94a3b8;">
        Estas premissas são <strong>normativas e inegociáveis</strong>. Qualquer modificação física, esquemática ou no código do firmware deve respeitar estritamente estes 5 postulados de projeto.
      </div>

      <!-- Premissa 1 -->
      <div class="norm-block">
        <div class="norm-title" style="color:var(--vcc);">
          <span>⚡ Premissa #1: Origem Absoluta de Energia (VCC e GND)</span>
          <span class="step-badge" style="background:rgba(255,71,87,0.2); color:var(--vcc);">Alimentação Única</span>
        </div>
        <div class="norm-text">
          Toda a energia elétrica da placa provém única e exclusivamente do <strong>Receptor de Rádio FlySky FS-BS6</strong> através de <strong>CON1 (CH6 / BEC do ESC)</strong>. Nenhum outro conector alimenta o sistema. O pino <strong>VIN do Arduino permanece desconectado</strong>; a placa é alimentada diretamente no pino <strong>5V</strong> (Col 06, Lin 14).
        </div>
        <table class="norm-table">
          <tr><th>Terminal Rádio</th><th>Pino CON1</th><th>Função</th><th>Tensão Recomendada</th><th>Consumo / Capacidade</th></tr>
          <tr><td>CH6 Central (Vermelho)</td><td>CON1 Pino 1 (17,15)</td><td>VCC Principal</td><td>+5.0V nominal (+5.5V máx)</td><td>Carga: ~162mA | Conector: 3.0A</td></tr>
          <tr><td>CH6 Inferior (Preto)</td><td>CON1 Pino 2 (17,14)</td><td>GND Mestre</td><td>0V (Terra Mestre)</td><td>Referência Zero Absoluta</td></tr>
        </table>
        <div style="margin-top:8px; font-size:0.78rem; color:#94a3b8;">
          💡 <em>Se o ESC tiver BEC de 6.0V+, instale um diodo 1N4007 ou 1N5819 em série na entrada do +5V para derrubar ~0.4–0.7V, mantendo o circuito na faixa de 5.3V segura do ATmega328P.</em>
        </div>
        <button class="norm-btn" onclick="highlightFromPremissa('vcc')">🔍 Destacar Rota de +5V no Visualizador</button>
      </div>

      <!-- Premissa 2 -->
      <div class="norm-block">
        <div class="norm-title" style="color:#ffd32a;">
          <span>🔋 Premissa #2: Regulação e Filtragem Imediata na Entrada (C1)</span>
          <span class="step-badge" style="background:rgba(255,211,42,0.2); color:#ffd32a;">Capacitor C1</span>
        </div>
        <div class="norm-text">
          O capacitor eletrolítico de desacoplamento <strong>C1 (100µF x 16V)</strong> é soldado colado aos pinos de entrada em <strong>Coluna 15 (Linhas 14 e 15)</strong>. O pólo (+) liga a CON1 P1 (+5V) e o pólo (-) liga a CON1 P2 (GND) e Nano GND. Atua absorvendo quedas bruscas de tensão (brownouts) e ruídos de alta corrente provocados pelo servo de direção e motor elétrico.
        </div>
        <button class="norm-btn" onclick="highlightFromPremissa('vcc')">🔍 Destacar Posição de C1 e Entrada</button>
      </div>

      <!-- Premissa 3 -->
      <div class="norm-block">
        <div class="norm-title" style="color:var(--gnd);">
          <span>🌐 Premissa #3: Barramento de Terra (GND) Mestre Unificado</span>
          <span class="step-badge" style="background:rgba(0,210,106,0.2); color:var(--gnd);">Equilíbrio de Neutro</span>
        </div>
        <div class="norm-text">
          O terra de CON1 P2 é a <strong>referência zero absoluta do veículo</strong>. A placa possui uma malha contínua reforçada de solda ($R &lt; 0.05\,\Omega$) interligando CON1, C1, Nano GND Dir, Nano GND Esq, CON2, CON3 e CON4. A integridade do terra existe na própria placa <strong>independentemente do módulo Arduino Nano estar inserido no soquete</strong>.
        </div>
        <button class="norm-btn" onclick="highlightFromPremissa('gnd')">🔍 Destacar Malha de GND Unificada</button>
      </div>

      <!-- Premissa 4 -->
      <div class="norm-block">
        <div class="norm-title" style="color:#a855f7;">
          <span>📐 Premissa #4: Roteamento Híbrido Otimizado &amp; 4 Jumpers Isolados Superiores</span>
          <span class="step-badge" style="background:rgba(168,85,247,0.2); color:#a855f7;">Zero Curtos</span>
        </div>
        <div class="norm-text">
          O Arduino Nano é posicionado com a porta <strong>USB voltada para a borda superior (Linhas 01-02)</strong> com sua pinagem física oficial (docs.arduino.cc). Como todos os pinos de LED do Nano (D5 a D11) residem na lateral direita, foram implementados <strong>4 fios isolados com capa na face superior (W1–W4)</strong> para saltar sobre componentes sem cruzamento de cobre no verso, com 0 conflitos de pads matematicamente comprovados:
          <ul style="margin: 8px 0 0 18px; font-size: 0.8rem; color: #cbd5e1;">
            <li><strong>W1 (+5V Nano, ~13mm):</strong> Ponto (Col 01, Lin 14) ➔ Nano 5V (Col 06, Lin 14)</li>
            <li><strong>W2 (Farol D9, ~36mm):</strong> Nano D9 (Col 12, Lin 06) ➔ R1 Top (Col 04, Lin 18)</li>
            <li><strong>W3 (Pisca FE D10, ~38mm):</strong> Nano D10 (Col 12, Lin 05) ➔ R2 Top (Col 05, Lin 18)</li>
            <li><strong>W4 (GND Cross-Tie, ~16mm):</strong> Nano GND Dir (Col 12, Lin 14) ➔ Nano GND Esq (Col 06, Lin 16)</li>
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
            <li><strong>CON4 (MPU-6050):</strong> Borda lateral esquerda (Coluna 02, Linhas 10 a 13).</li>
            <li><strong>CON2 (Frente) &amp; CON3 (Traseira):</strong> Borda inferior (Linha 24).</li>
            <li><strong>USB do Nano:</strong> Borda superior externa (Linha 01) — gravação de firmware sem desmontar a placa.</li>
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

  function switchMainView(mode) {{
    currentView = mode;
    document.querySelectorAll('.view-panel').forEach(p => p.classList.remove('active'));
    document.querySelectorAll('.btn-group button').forEach(b => b.classList.remove('active'));

    document.getElementById('panel-' + mode).classList.add('active');
    document.getElementById('btn-' + mode).classList.add('active');
    applyHighlightFilter();
  }}

  function switchSidebarTab(tabName) {{
    document.querySelectorAll('.sidebar-tab-btn').forEach(btn => btn.classList.remove('active'));
    document.getElementById('tab-btn-' + tabName).classList.add('active');

    document.getElementById('tab-content-steps').style.display = tabName === 'steps' ? 'flex' : 'none';
    document.getElementById('tab-content-premissas').style.display = tabName === 'premissas' ? 'flex' : 'none';
  }}

  function activateStep(netId, cardElem) {{
    currentFilter = netId;
    document.querySelectorAll('.step-card, .premissa-card').forEach(c => c.classList.remove('active'));
    if (cardElem) cardElem.classList.add('active');
    applyHighlightFilter();
  }}

  function activatePremissa(netId, cardElem) {{
    currentFilter = netId;
    document.querySelectorAll('.step-card, .premissa-card').forEach(c => c.classList.remove('active'));
    if (cardElem) cardElem.classList.add('active');
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
    currentFilter = netId;
    applyHighlightFilter();
  }}

  document.addEventListener('keydown', (e) => {{
    if (e.key === 'Escape') closePremissasModal();
  }});

  function applyHighlightFilter() {{
    const allTracks = document.querySelectorAll('.track-line');
    const allPads = document.querySelectorAll('.solder-joint, .solder-ring, .solder-lbl');

    if (currentFilter === 'all') {{
      allTracks.forEach(t => t.classList.remove('dimmed', 'highlight-focus'));
      allPads.forEach(p => p.classList.remove('dimmed', 'highlight-focus'));
      return;
    }}

    allTracks.forEach(t => {{
      if (t.classList.contains('track-' + currentFilter)) {{
        t.classList.remove('dimmed');
        t.classList.add('highlight-focus');
      }} else {{
        t.classList.add('dimmed');
        t.classList.remove('highlight-focus');
      }}
    }});

    allPads.forEach(p => {{
      if (p.classList.contains('pad-' + currentFilter) || p.classList.contains('lbl-' + currentFilter)) {{
        p.classList.remove('dimmed');
        p.classList.add('highlight-focus');
      }} else {{
        p.classList.add('dimmed');
        p.classList.remove('highlight-focus');
      }}
    }});
  }}

  document.addEventListener('DOMContentLoaded', () => {{
    switchMainView('bottom');
    activateStep('all', document.querySelector('.step-card.active'));
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
    print("Generated placa_shield_superior.svg (v7.2)")

    svg_bottom = generate_svg_bottom_solder()
    with open("placa_shield_inferior.svg", "w", encoding="utf-8") as f:
        f.write(svg_bottom)
    print("Generated placa_shield_inferior.svg (v7.2)")

    html_content = generate_interactive_html(svg_top, svg_bottom)
    with open("placa_shield_visualizador.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Generated placa_shield_visualizador.html (v7.2)")

if __name__ == "__main__":
    main()
