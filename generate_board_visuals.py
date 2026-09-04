"""
Gerador de Visualizações e Documentação Gráfica para Placa Shield RC v8.0
Layout Natural Distribuído (Zero Cruzamentos, Trilhas Ultracurtas de 10mm):
- Lateral Esquerda (Col 2, Linhas 6-10): CON1 Rádio FS-BS6 (1x5 90°). Trilhas retas de 10mm para D2, D3, D4!
- Lateral Direita (Col 17, Linhas 7-10): CON4 MPU-6050 (1x4 90°) + C1 (Cols 14-15). Trilhas retas de 10mm para A4, A5, 5V, GND!
- Borda Inferior Esquerda (Linha 24, Cols 3-6): CON2 Frente (1x4 90°) via R1, R2, R3 (Linhas 18-21, Cols 4-6).
- Borda Inferior Direita (Linha 24, Cols 8-13): CON3 Trás (1x6 90°) via R4, R5, R6, R7 (Linhas 18-21, Cols 8-11).
- 100% Planar, ZERO fios jumpers cruzando outros circuitos!
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
      <filter id="shadow" x="-10%" y="-10%" width="130%" height="130%">
        <feDropShadow dx="3" dy="4" stdDeviation="4" flood-color="#000" flood-opacity="0.6"/>
      </filter>
    ''')
    svg.append('</defs>')

    pcb_x = margin_x - pitch * 0.75
    pcb_y = margin_y - pitch * 0.75
    pcb_w = (cols - 1) * pitch + pitch * 1.5
    pcb_h = (rows - 1) * pitch + pitch * 1.5

    # PCB Board Base
    svg.append(f'<rect x="{pcb_x}" y="{pcb_y}" width="{pcb_w}" height="{pcb_h}" rx="16" fill="url(#fr4Grad)" stroke="#27ae60" stroke-width="2" filter="url(#shadow)"/>')
    svg.append(f'<rect x="{pcb_x+8}" y="{pcb_y+8}" width="{pcb_w-16}" height="{pcb_h-16}" rx="12" fill="none" stroke="#2ecc71" stroke-width="1" stroke-opacity="0.35"/>')

    # Corner mounting holes
    corner_r = 10
    for hx, hy in [(pcb_x+18, pcb_y+18), (pcb_x+pcb_w-18, pcb_y+18), (pcb_x+18, pcb_y+pcb_h-18), (pcb_x+pcb_w-18, pcb_y+pcb_h-18)]:
        svg.append(f'<circle cx="{hx}" cy="{hy}" r="{corner_r}" fill="#0d1318" stroke="#d4af37" stroke-width="3"/>')

    # Silk screen titles
    svg.append(f'<text x="{board_w/2}" y="{pcb_y-16}" text-anchor="middle" fill="#ecf0f1" font-size="17" font-weight="bold" letter-spacing="1">PLACA SHIELD HUB 5x7cm — LAYOUT DISTRIBUÍDO v8.0</text>')
    svg.append(f'<text x="{board_w/2}" y="{pcb_y+22}" text-anchor="middle" fill="#a2d9ce" font-size="11" font-weight="600" letter-spacing="1.5">BORDA SUPERIOR ◄── PORTA USB NANO PARA CIMA (ZERO CRUZAMENTOS)</text>')

    # Column numbers
    for c in range(1, cols + 1):
        x = cx(c)
        svg.append(f'<text x="{x}" y="{margin_y - 15}" text-anchor="middle" fill="#f1c40f" font-size="12" font-weight="bold">{c:02d}</text>')
        svg.append(f'<text x="{x}" y="{pcb_y + pcb_h + 20}" text-anchor="middle" fill="#f1c40f" font-size="11">{c:02d}</text>')

    # Row numbers
    for r in range(1, rows + 1):
        y = cy(r)
        svg.append(f'<text x="{margin_x - 30}" y="{y + 4}" text-anchor="middle" fill="#f1c40f" font-size="12" font-weight="bold">{r:02d}</text>')
        svg.append(f'<text x="{board_w - margin_x + 30}" y="{y + 4}" text-anchor="middle" fill="#f1c40f" font-size="11">{r:02d}</text>')

    # Copper pads grid
    for r in range(1, rows + 1):
        for c in range(1, cols + 1):
            x = cx(c)
            y = cy(r)
            svg.append(f'<circle cx="{x}" cy="{y}" r="8" fill="url(#copperPad)" opacity="0.85"/>')
            svg.append(f'<circle cx="{x}" cy="{y}" r="4" fill="#0d1f14"/>')

    # Arduino Nano Socket & Body (Cols 6 and 12, Rows 3 to 17)
    nano_x1 = cx(6) - 18
    nano_x2 = cx(12) + 18
    nano_y1 = cy(1) - 6
    nano_y2 = cy(17) + 18
    nano_w = nano_x2 - nano_x1
    nano_h = nano_y2 - nano_y1

    # Female header sockets
    svg.append(f'<rect x="{cx(6)-10}" y="{cy(3)-10}" width="20" height="{14*pitch+20}" rx="3" fill="#181818" stroke="#333" stroke-width="1.5" filter="url(#shadow)"/>')
    svg.append(f'<rect x="{cx(12)-10}" y="{cy(3)-10}" width="20" height="{14*pitch+20}" rx="3" fill="#181818" stroke="#333" stroke-width="1.5" filter="url(#shadow)"/>')

    for r in range(3, 18):
        svg.append(f'<rect x="{cx(6)-4}" y="{cy(r)-4}" width="8" height="8" rx="1" fill="#000" stroke="#d4af37" stroke-width="1"/>')
        svg.append(f'<rect x="{cx(12)-4}" y="{cy(r)-4}" width="8" height="8" rx="1" fill="#000" stroke="#d4af37" stroke-width="1"/>')

    # Nano PCB Body
    svg.append(f'<rect x="{nano_x1}" y="{nano_y1}" width="{nano_w}" height="{nano_h}" rx="8" fill="url(#nanoGrad)" stroke="#1f8cd1" stroke-width="2" filter="url(#shadow)"/>')
    svg.append(f'<rect x="{nano_x1+4}" y="{nano_y1+4}" width="{nano_w-8}" height="{nano_h-8}" rx="6" fill="none" stroke="#fff" stroke-width="0.8" stroke-opacity="0.3"/>')

    # Nano USB Port
    usb_w = 42
    usb_h = 32
    usb_x = (cx(6) + cx(12)) / 2 - usb_w / 2
    usb_y = nano_y1 - 10
    svg.append(f'<rect x="{usb_x}" y="{usb_y}" width="{usb_w}" height="{usb_h}" rx="3" fill="url(#usbGrad)" stroke="#7f8c8d" stroke-width="1.5" filter="url(#shadow)"/>')
    svg.append(f'<rect x="{usb_x+6}" y="{usb_y+2}" width="{usb_w-12}" height="10" rx="1" fill="#2c3e50"/>')
    svg.append(f'<text x="{usb_x+usb_w/2}" y="{usb_y+24}" text-anchor="middle" fill="#333" font-size="9" font-weight="bold">USB</text>')

    # ATmega328P Chip
    chip_size = 46
    chip_cx = (cx(6) + cx(12)) / 2
    chip_cy = cy(8) + 10
    svg.append(f'<g transform="rotate(45 {chip_cx} {chip_cy})">')
    svg.append(f'<rect x="{chip_cx-chip_size/2}" y="{chip_cy-chip_size/2}" width="{chip_size}" height="{chip_size}" rx="3" fill="#1c2833" stroke="#4a6572" stroke-width="1"/>')
    svg.append(f'</g>')
    svg.append(f'<text x="{chip_cx}" y="{chip_cy+4}" text-anchor="middle" fill="#bdc3c7" font-size="8" font-family="monospace" font-weight="bold">ATmega</text>')
    svg.append(f'<text x="{chip_cx}" y="{chip_cy+13}" text-anchor="middle" fill="#bdc3c7" font-size="8" font-family="monospace" font-weight="bold">328P</text>')

    # Pin labels on Nano
    left_pins = [
        ("D1/TX", "#bdc3c7"), ("D0/RX", "#bdc3c7"), ("RST", "#e74c3c"), ("GND", "#1abc9c"),
        ("D2 (CH2)", "#f39c12"), ("D3 (CH4)", "#2ecc71"), ("D4 (CH1)", "#3498db"),
        ("D5 (Lant)", "#e67e22"), ("D6 (Freio)", "#e74c3c"), ("D7 (P.TE)", "#f39c12"), ("D8 (P.TD)", "#3498db"),
        ("D9 (Farol)", "#ffffff"), ("D10 (P.FE)", "#f39c12"), ("D11 (P.FD)", "#3498db"), ("D12", "#bdc3c7")
    ]
    for i, (name, col) in enumerate(left_pins):
        r = 3 + i
        svg.append(f'<text x="{cx(6)-14}" y="{cy(r)+3}" text-anchor="end" fill="{col}" font-size="8" font-weight="bold">{name}</text>')

    right_pins = [
        ("VIN", "#e74c3c"), ("GND", "#1abc9c"), ("RST", "#e74c3c"), ("+5V", "#e74c3c"),
        ("A7", "#bdc3c7"), ("A6", "#bdc3c7"), ("A5 (SCL)", "#ffd32a"), ("A4 (SDA)", "#2ed573"),
        ("A3", "#bdc3c7"), ("A2", "#bdc3c7"), ("A1", "#bdc3c7"), ("A0", "#bdc3c7"),
        ("REF", "#bdc3c7"), ("3V3", "#bdc3c7"), ("D13", "#bdc3c7")
    ]
    for i, (name, col) in enumerate(right_pins):
        r = 3 + i
        svg.append(f'<text x="{cx(12)+14}" y="{cy(r)+3}" text-anchor="start" fill="{col}" font-size="8" font-weight="bold">{name}</text>')

    # Helper: draw vertical resistor
    def draw_resistor(col, r_top, r_bot, name, band_colors):
        x = cx(col)
        y_top = cy(r_top)
        y_bot = cy(r_bot)
        body_h = 24
        body_w = 12
        body_y = (y_top + y_bot) / 2 - body_h / 2
        svg.append(f'<line x1="{x}" y1="{y_top}" x2="{x}" y2="{body_y}" stroke="#bdc3c7" stroke-width="2.5"/>')
        svg.append(f'<line x1="{x}" y1="{body_y+body_h}" x2="{x}" y2="{y_bot}" stroke="#bdc3c7" stroke-width="2.5"/>')
        svg.append(f'<rect x="{x - body_w/2}" y="{body_y}" width="{body_w}" height="{body_h}" rx="4" fill="url(#resistorBody)" stroke="#795548" stroke-width="1" filter="url(#shadow)"/>')
        band_y_start = body_y + 4
        band_gap = 4.5
        for bi, bcolor in enumerate(band_colors):
            by = band_y_start + bi * band_gap
            svg.append(f'<rect x="{x - body_w/2}" y="{by}" width="{body_w}" height="3" fill="{bcolor}"/>')
        svg.append(f'<text x="{x}" y="{body_y + body_h/2 + 3}" text-anchor="middle" fill="#1a252f" font-size="6.5" font-weight="bold" transform="rotate(-90 {x} {body_y + body_h/2})">{name}</text>')

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
    svg.append(f'<text x="{cx(10)}" y="{cy(22)+4}" text-anchor="middle" fill="#e74c3c" font-size="8" font-weight="bold">Freio</text>')

    draw_resistor(11, 18, 21, "R4 150Ω", ["#795548", "#2ecc71", "#795548", "#f1c40f"])
    svg.append(f'<text x="{cx(11)}" y="{cy(22)+4}" text-anchor="middle" fill="#e67e22" font-size="8" font-weight="bold">Lant.</text>')

    # Capacitor C1 (Cols 14-15, Row 6)
    cap_cx = (cx(14) + cx(15)) / 2
    cap_cy = cy(6)
    svg.append(f'<line x1="{cx(14)}" y1="{cy(6)}" x2="{cap_cx-4}" y2="{cap_cy}" stroke="#bdc3c7" stroke-width="2"/>')
    svg.append(f'<line x1="{cx(15)}" y1="{cy(6)}" x2="{cap_cx+4}" y2="{cap_cy}" stroke="#bdc3c7" stroke-width="2"/>')
    cap_r = 14
    svg.append(f'<circle cx="{cap_cx}" cy="{cap_cy}" r="{cap_r}" fill="url(#capGrad)" stroke="#566573" stroke-width="1.5" filter="url(#shadow)"/>')
    svg.append(f'<path d="M {cap_cx-cap_r} {cap_cy-7} A {cap_r} {cap_r} 0 0 1 {cap_cx-4} {cap_cy-12} L {cap_cx-4} {cap_cy+12} A {cap_r} {cap_r} 0 0 1 {cap_cx-cap_r} {cap_cy+7} Z" fill="#ecf0f1"/>')
    svg.append(f'<text x="{cap_cx-8}" y="{cap_cy+3}" fill="#000" font-size="9" font-weight="bold" text-anchor="middle">-</text>')
    svg.append(f'<text x="{cap_cx+4}" y="{cap_cy-2}" fill="#ecf0f1" font-size="6.5" font-weight="bold" text-anchor="middle">100µF</text>')
    svg.append(f'<text x="{cap_cx+4}" y="{cap_cy+7}" fill="#ecf0f1" font-size="6.5" font-weight="bold" text-anchor="middle">C1</text>')

    # ==========================
    # CON1: RÁDIO (Lateral Esquerda - Coluna 02, Linhas 5 a 9) 90° Apontando para Esquerda!
    # ==========================
    con1_x = cx(2) - 12
    con1_y = cy(5) - 12
    con1_w = 24
    con1_h = 4 * pitch + 24
    svg.append(f'<rect x="{con1_x}" y="{con1_y}" width="{con1_w}" height="{con1_h}" rx="3" fill="#1c2833" stroke="#2980b9" stroke-width="1.8" filter="url(#shadow)"/>')
    svg.append(f'<text x="{con1_x-8}" y="{con1_y + con1_h/2}" text-anchor="middle" fill="#2980b9" font-size="9.5" font-weight="bold" transform="rotate(-90 {con1_x-8} {con1_y + con1_h/2})">CON1: RÁDIO (1x5 90°)</text>')

    con1_pins = [
        (5, "+5V", "#e74c3c", "P1"),
        (6, "GND", "#1abc9c", "P2"),
        (7, "CH2", "#f39c12", "P3"),
        (8, "CH4", "#2ecc71", "P4"),
        (9, "CH1", "#3498db", "P5")
    ]
    for r, pname, pcolor, pnum in con1_pins:
        px = cx(2)
        py = cy(r)
        svg.append(f'<circle cx="{px}" cy="{py}" r="4" fill="#f1c40f" stroke="#000" stroke-width="1"/>')
        # 90 deg pin pointing left
        svg.append(f'<rect x="{px-35}" y="{py-2.5}" width="35" height="5" rx="1" fill="#f1c40f" stroke="#b7950b" stroke-width="0.8" filter="url(#shadow)"/>')
        svg.append(f'<text x="{px-42}" y="{py+3}" text-anchor="end" fill="{pcolor}" font-size="8.5" font-weight="bold">{pname}</text>')

    # ==========================
    # CON4: MPU-6050 (Lateral Direita - Coluna 17, Linhas 7 a 10) 90° Apontando para Direita!
    # ==========================
    con4_x = cx(17) - 12
    con4_y = cy(7) - 12
    con4_w = 24
    con4_h = 3 * pitch + 24
    svg.append(f'<rect x="{con4_x}" y="{con4_y}" width="{con4_w}" height="{con4_h}" rx="3" fill="#1c2833" stroke="#f1c40f" stroke-width="1.8" filter="url(#shadow)"/>')
    svg.append(f'<text x="{con4_x+con4_w+8}" y="{con4_y + con4_h/2}" text-anchor="middle" fill="#f1c40f" font-size="9.5" font-weight="bold" transform="rotate(90 {con4_x+con4_w+8} {con4_y + con4_h/2})">CON4: MPU (1x4 90°)</text>')

    con4_pins = [
        (7, "GND", "#1abc9c", "P1"),
        (8, "+5V", "#e74c3c", "P2"),
        (9, "SCL", "#ffd32a", "P3"),
        (10, "SDA", "#2ed573", "P4")
    ]
    for r, pname, pcolor, pnum in con4_pins:
        px = cx(17)
        py = cy(r)
        svg.append(f'<circle cx="{px}" cy="{py}" r="4" fill="#f1c40f" stroke="#000" stroke-width="1"/>')
        # 90 deg pin pointing right
        svg.append(f'<rect x="{px}" y="{py-2.5}" width="35" height="5" rx="1" fill="#f1c40f" stroke="#b7950b" stroke-width="0.8" filter="url(#shadow)"/>')
        svg.append(f'<text x="{px+42}" y="{py+3}" text-anchor="start" fill="{pcolor}" font-size="8.5" font-weight="bold">{pname}</text>')

    # ==========================
    # CON2 (Frente): Linha 24, Colunas 3 a 6 (90° para baixo)
    # ==========================
    def draw_ra_bottom(start_col, num_pins, title, pin_labels, box_color="#27ae60"):
        x_start = cx(start_col) - 14
        w = (num_pins - 1) * pitch + 28
        y = cy(24) - 12
        svg.append(f'<rect x="{x_start}" y="{y}" width="{w}" height="24" rx="3" fill="#1c2833" stroke="{box_color}" stroke-width="1.8" filter="url(#shadow)"/>')
        svg.append(f'<text x="{x_start + w/2}" y="{y - 7}" text-anchor="middle" fill="{box_color}" font-size="10" font-weight="bold">{title}</text>')
        for i, (pnum, pname, pcolor) in enumerate(pin_labels):
            px = cx(start_col + i)
            py = cy(24)
            svg.append(f'<circle cx="{px}" cy="{py}" r="4" fill="#f1c40f" stroke="#000" stroke-width="1"/>')
            pin_ext_len = 38
            svg.append(f'<rect x="{px-2.5}" y="{py+6}" width="5" height="{pin_ext_len}" rx="1" fill="#f1c40f" stroke="#b7950b" stroke-width="0.8" filter="url(#shadow)"/>')
            svg.append(f'<text x="{px}" y="{py+pin_ext_len+16}" text-anchor="middle" fill="{pcolor}" font-size="9" font-weight="bold">{pname}</text>')
            svg.append(f'<text x="{px}" y="{py+pin_ext_len+26}" text-anchor="middle" fill="#95a5a6" font-size="7.5">P{pnum}</text>')

    # CON2 Frente: Cols 3..6
    draw_ra_bottom(3, 4, "CON2: FRENTE (1x4 90°)", [
        (1, "GND", "#1abc9c"),
        (2, "Farol", "#ffffff"),
        (3, "Pis.FE", "#f39c12"),
        (4, "Pis.FD", "#3498db")
    ], "#27ae60")

    # CON3 Trás: Cols 8..13
    draw_ra_bottom(8, 6, "CON3: TRÁS (1x6 90°)", [
        (1, "Pis.TD", "#3498db"),
        (2, "Pis.TE", "#f39c12"),
        (3, "Freio", "#e74c3c"),
        (4, "Lant.", "#e67e22"),
        (5, "NC", "#7f8c8d"),
        (6, "GND", "#1abc9c")
    ], "#e67e22")

    svg.append('</svg>')
    return '\n'.join(svg)


def generate_svg_bottom_solder():
    """
    Solder Bottom View (Mirrored: Col 18 on Left, Col 01 on Right):
    - 100% Planar, ZERO wire crossovers.
    - Ultra-short tracks:
      - Radio: Cols 2..6, Rows 6..10 (Horizontal ~10mm).
      - MPU-6050: Cols 12..17, Rows 7..10 (Horizontal ~10mm).
      - Front LEDs: Cols 4..6, Rows 14..24 (Vertical).
      - Rear LEDs: Cols 8..11, Rows 10..24 (Vertical).
      - Power 5V: Enters at CON1 (Col 2), runs up to Row 2, across Row 2 to Nano 5V (Col 12), C1 and MPU.
      - GND Bus: Clean, heavy solder tracks on Cols 6 and 12, joining all grounds without jumpers!
    """
    cols = 18
    rows = 24
    pitch = 36
    margin_x = 90
    margin_y = 85
    board_w = (cols - 1) * pitch + margin_x * 2
    board_h = (rows - 1) * pitch + margin_y * 2 + 50

    # Mirrored coordinate: Col 18 is at Left (x=margin_x), Col 01 is at Right
    def cx(c):
        return margin_x + (cols - c) * pitch

    def cy(r):
        return margin_y + (r - 1) * pitch

    # Complete solder joints database
    solder_pads_data = {
        # Nano Left Header (Mirrored: Col 6 on Right side)
        (6, 6):   ("gnd", "GND", "Nano GND (Pin 4)", "Solda do GND Esquerdo do Nano no Barramento GND"),
        (6, 7):   ("radio", "D2", "Nano D2 (INT0)", "Solda direta horizontal de 10mm para CON1 CH2 (Lin 7)"),
        (6, 8):   ("radio", "D3", "Nano D3 (INT1)", "Solda direta horizontal de 10mm para CON1 CH4 (Lin 8)"),
        (6, 9):   ("radio", "D4", "Nano D4 (PCINT)", "Solda direta horizontal de 10mm para CON1 CH1 (Lin 9)"),
        (6, 10):  ("led-tras", "D5", "Nano D5 (PWM)", "Trilha horizontal Lin 10 até Col 11 para R4 Top (Lanterna)"),
        (6, 11):  ("led-tras", "D6", "Nano D6", "Trilha horizontal Lin 11 até Col 10 para R5 Top (Freio)"),
        (6, 12):  ("led-tras", "D7", "Nano D7", "Trilha horizontal Lin 12 até Col 09 para R6 Top (Pisca TE)"),
        (6, 13):  ("led-tras", "D8", "Nano D8", "Trilha horizontal Lin 13 até Col 08 para R7 Top (Pisca TD)"),
        (6, 14):  ("led-frente", "D9", "Nano D9 (PWM)", "Trilha horizontal Lin 14 até Col 4 para R1 Top (Farol)"),
        (6, 15):  ("led-frente", "D10", "Nano D10", "Trilha horizontal Lin 15 até Col 5 para R2 Top (Pisca FE)"),
        (6, 16):  ("led-frente", "D11", "Nano D11", "Trilha direta vertical Col 6 para R3 Top (Pisca FD)"),

        # Nano Right Header (Mirrored: Col 12 on Left side)
        (12, 4):  ("gnd", "GND", "Nano GND (Pin 29)", "Solda do GND Direito do Nano no Barramento GND"),
        (12, 6):  ("vcc", "+5V", "Nano +5V (Pin 27)", "Solda de entrada do +5V vindo da Linha de Topo 02"),
        (12, 9):  ("i2c", "A5", "Nano A5 (SCL)", "Trilha direta horizontal de 10mm para CON4 SCL (Lin 9)"),
        (12, 10): ("i2c", "A4", "Nano A4 (SDA)", "Trilha direta horizontal de 10mm para CON4 SDA (Lin 10)"),

        # CON1: Rádio (Lateral Esquerda - Coluna 02, Linhas 5 a 9)
        (2, 5):   ("vcc", "CON1 P1", "CON1 +5V (BEC)", "Entrada de +5V do ESC/Receptor via CH6"),
        (2, 6):   ("gnd", "CON1 P2", "CON1 GND", "Solda de terra do rádio no Barramento GND"),
        (2, 7):   ("radio", "CON1 P3", "CON1 CH2 (Thr)", "Trilha direta horizontal para Nano D2 (10mm, Lin 7)"),
        (2, 8):   ("radio", "CON1 P4", "CON1 CH4 (Farol)", "Trilha direta horizontal para Nano D3 (10mm, Lin 8)"),
        (2, 9):   ("radio", "CON1 P5", "CON1 CH1 (Vol)", "Trilha direta horizontal para Nano D4 (10mm, Lin 9)"),

        # CON4: MPU-6050 (Lateral Direita - Coluna 17, Linhas 7 a 10)
        (17, 7):  ("gnd", "CON4 P1", "CON4 GND", "Solda de terra do acelerômetro no Barramento GND"),
        (17, 8):  ("vcc", "CON4 P2", "CON4 +5V", "Alimentação +5V do acelerômetro"),
        (17, 9):  ("i2c", "CON4 P3", "CON4 SCL", "Trilha direta horizontal para Nano A5 (10mm, Lin 9)"),
        (17, 10): ("i2c", "CON4 P4", "CON4 SDA", "Trilha direta horizontal para Nano A4 (10mm, Lin 10)"),

        # Capacitor C1 (Cols 14-15, Row 6)
        (14, 6):  ("gnd", "C1 (-)", "Capacitor C1 (-)", "Solda do negativo do capacitor de filtro"),
        (15, 6):  ("vcc", "C1 (+)", "Capacitor C1 (+)", "Solda do positivo do capacitor na linha +5V"),

        # Resistores Dianteiros R1, R2, R3 (Cols 4, 5, 6, Rows 18 e 21)
        (4, 18):  ("led-frente", "R1 Top", "R1 Top (Farol 100Ω)", "Entrada vinda de Nano D9"),
        (4, 21):  ("led-frente", "R1 Bot", "R1 Bot (Farol)", "Trilha direta vertical para CON2 Pino 2"),
        (5, 18):  ("led-frente", "R2 Top", "R2 Top (Pis.FE 150Ω)", "Entrada vinda de Nano D10"),
        (5, 21):  ("led-frente", "R2 Bot", "R2 Bot (Pis.FE)", "Trilha direta vertical para CON2 Pino 3"),
        (6, 18):  ("led-frente", "R3 Top", "R3 Top (Pis.FD 150Ω)", "Entrada vinda de Nano D11"),
        (6, 21):  ("led-frente", "R3 Bot", "R3 Bot (Pis.FD)", "Trilha direta vertical para CON2 Pino 4"),

        # Resistores Traseiros R7, R6, R5, R4 (Cols 8, 9, 10, 11, Rows 18 e 21)
        (8, 18):  ("led-tras", "R7 Top", "R7 Top (Pis.TD 150Ω)", "Entrada vinda de Nano D8 (Lin 13)"),
        (8, 21):  ("led-tras", "R7 Bot", "R7 Bot (Pis.TD)", "Trilha direta vertical para CON3 Pino 1"),
        (9, 18):  ("led-tras", "R6 Top", "R6 Top (Pis.TE 150Ω)", "Entrada vinda de Nano D7 (Lin 12)"),
        (9, 21):  ("led-tras", "R6 Bot", "R6 Bot (Pis.TE)", "Trilha direta vertical para CON3 Pino 2"),
        (10, 18): ("led-tras", "R5 Top", "R5 Top (Freio 150Ω)", "Entrada vinda de Nano D6 (Lin 11)"),
        (10, 21): ("led-tras", "R5 Bot", "R5 Bot (Freio)", "Trilha direta vertical para CON3 Pino 3"),
        (11, 18): ("led-tras", "R4 Top", "R4 Top (Lanterna 150Ω)", "Entrada vinda de Nano D5 (Lin 10)"),
        (11, 21): ("led-tras", "R4 Bot", "R4 Bot (Lanterna)", "Trilha direta vertical para CON3 Pino 4"),

        # CON2 (Frente - Linha 24, Cols 3 a 6)
        (3, 24):  ("gnd", "CON2 P1", "CON2 GND", "Solda de terra do chicote dianteiro via Col 01"),
        (4, 24):  ("led-frente", "CON2 P2", "CON2 Farol", "Entrada de farol vinda de R1 Bot"),
        (5, 24):  ("led-frente", "CON2 P3", "CON2 Pis.FE", "Entrada de pisca FE vinda de R2 Bot"),
        (6, 24):  ("led-frente", "CON2 P4", "CON2 Pis.FD", "Entrada de pisca FD vinda de R3 Bot"),

        # CON3 (Trás - Linha 24, Cols 8 a 13)
        (8, 24):  ("led-tras", "CON3 P1", "CON3 Pis.TD", "Entrada de pisca TD vinda de R7 Bot"),
        (9, 24):  ("led-tras", "CON3 P2", "CON3 Pis.TE", "Entrada de pisca TE vinda de R6 Bot"),
        (10, 24): ("led-tras", "CON3 P3", "CON3 Freio", "Entrada de freio vinda de R5 Bot"),
        (11, 24): ("led-tras", "CON3 P4", "CON3 Lant.", "Entrada de lanterna vinda de R4 Bot"),
        (12, 24): ("mech", "CON3 P5", "CON3 NC", "Pino mecânico livre"),
        (13, 24): ("gnd", "CON3 P6", "CON3 GND", "Solda de terra do chicote traseiro via Col 13")
    }

    svg = []
    svg.append(f'<svg id="svg-bottom-root" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {board_w} {board_h}" width="{board_w}" height="{board_h}" style="background:#090d14; font-family:\'Segoe UI\',system-ui,sans-serif;">')
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

    pcb_x = margin_x - pitch * 0.75
    pcb_y = margin_y - pitch * 0.75
    pcb_w = (cols - 1) * pitch + pitch * 1.5
    pcb_h = (rows - 1) * pitch + pitch * 1.5

    svg.append(f'<rect x="{pcb_x}" y="{pcb_y}" width="{pcb_w}" height="{pcb_h}" rx="16" fill="url(#fr4BackDark)" stroke="#1e7e44" stroke-width="2"/>')

    # Titles
    svg.append(f'<text x="{board_w/2}" y="{pcb_y-16}" text-anchor="middle" fill="#ecf0f1" font-size="17" font-weight="bold" letter-spacing="1">MAPA DE SOLDA — VISTA DO VERSO (LAYOUT DISTRIBUÍDO v8.0)</text>')
    svg.append(f'<text x="{board_w/2}" y="{pcb_y+22}" text-anchor="middle" fill="#f1c40f" font-size="12" font-weight="bold">🔍 VISTA ESPELHADA: COLUNA 18 (ESQUERDA) ◄──────► COLUNA 01 (DIREITA) • ZERO CRUZAMENTOS</text>')

    # Column numbers (Mirrored: 18..1)
    for c in range(1, cols + 1):
        x = cx(c)
        svg.append(f'<text x="{x}" y="{margin_y - 15}" text-anchor="middle" fill="#f1c40f" font-size="13" font-weight="bold">{c:02d}</text>')
        svg.append(f'<text x="{x}" y="{pcb_y + pcb_h + 20}" text-anchor="middle" fill="#f1c40f" font-size="11">{c:02d}</text>')

    # Row numbers
    for r in range(1, rows + 1):
        y = cy(r)
        svg.append(f'<text x="{margin_x - 30}" y="{y + 4}" text-anchor="middle" fill="#f1c40f" font-size="12" font-weight="bold">{r:02d}</text>')
        svg.append(f'<text x="{board_w - margin_x + 30}" y="{y + 4}" text-anchor="middle" fill="#f1c40f" font-size="11">{r:02d}</text>')

    # Dimmed background holes for non-soldered pads
    svg.append('<g id="unused-pads" opacity="0.22">')
    for r in range(1, rows + 1):
        for c in range(1, cols + 1):
            if (c, r) not in solder_pads_data:
                x = cx(c)
                y = cy(r)
                svg.append(f'<circle cx="{x}" cy="{y}" r="6" fill="#1b2a1e" stroke="#2d4a34" stroke-width="0.8"/>')
                svg.append(f'<circle cx="{x}" cy="{y}" r="3" fill="#000"/>')
    svg.append('</g>')

    # Nano outlines (Mirrored: Col 12 is Left, Col 6 is Right)
    svg.append(f'<rect x="{cx(12)-14}" y="{cy(3)-14}" width="28" height="{14*pitch+28}" rx="4" fill="none" stroke="#00a8ff" stroke-width="1.2" stroke-dasharray="4,4" opacity="0.6"/>')
    svg.append(f'<text x="{cx(12)}" y="{cy(2)-2}" text-anchor="middle" fill="#00a8ff" font-size="9" font-weight="bold">NANO DIR (5V/A4/A5)</text>')

    svg.append(f'<rect x="{cx(6)-14}" y="{cy(3)-14}" width="28" height="{14*pitch+28}" rx="4" fill="none" stroke="#ff9f1a" stroke-width="1.2" stroke-dasharray="4,4" opacity="0.6"/>')
    svg.append(f'<text x="{cx(6)}" y="{cy(2)-2}" text-anchor="middle" fill="#ff9f1a" font-size="9" font-weight="bold">NANO ESQ (D2..D11)</text>')

    # Helper: draw solder track
    def draw_solder_track(points, color, width, net_id, is_jumper=False, label=""):
        d_str = "M " + " L ".join([f"{p[0]} {p[1]}" for p in points])
        dash_style = 'stroke-dasharray="6,4"' if is_jumper else ''
        glow_filter = 'filter="url(#busGlow)"' if width >= 5 else ''
        svg.append(f'<path class="track-line track-{net_id}" d="{d_str}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" {dash_style} {glow_filter} opacity="0.95"/>')
        if label and len(points) >= 2:
            mid_x = (points[0][0] + points[-1][0]) / 2
            mid_y = (points[0][1] + points[-1][1]) / 2
            svg.append(f'<text x="{mid_x}" y="{mid_y-5}" text-anchor="middle" fill="{color}" font-size="8" font-weight="bold" pointer-events="none">{label}</text>')

    # ==========================================
    # 1. 📻 TRILHAS DO RÁDIO (CON1: Lateral Esquerda - Coluna 02) — APENAS 10mm!
    # ==========================================
    # D2 -> CON1 P3 (Row 7) — Reta horizontal de 10mm!
    draw_solder_track([(cx(6), cy(7)), (cx(2), cy(7))], "#f39c12", 3.5, "radio", label="D2 (10mm)")
    # D3 -> CON1 P4 (Row 8) — Reta horizontal de 10mm!
    draw_solder_track([(cx(6), cy(8)), (cx(2), cy(8))], "#2ecc71", 3.5, "radio", label="D3 (10mm)")
    # D4 -> CON1 P5 (Row 9) — Reta horizontal de 10mm!
    draw_solder_track([(cx(6), cy(9)), (cx(2), cy(9))], "#3498db", 3.5, "radio", label="D4 (10mm)")

    # ==========================================
    # 2. 🧭 TRILHAS DO MPU-6050 (CON4: Lateral Direita - Coluna 17) — APENAS 10mm!
    # ==========================================
    # A5 (SCL) -> CON4 P3 (Row 9) — Reta horizontal de 10mm!
    draw_solder_track([(cx(12), cy(9)), (cx(17), cy(9))], "#ffd32a", 3.5, "i2c", label="SCL (10mm)")
    # A4 (SDA) -> CON4 P4 (Row 10) — Reta horizontal de 10mm!
    draw_solder_track([(cx(12), cy(10)), (cx(17), cy(10))], "#2ed573", 3.5, "i2c", label="SDA (10mm)")

    # ==========================================
    # 3. 🔴 LINHA +5V (ALIMENTAÇÃO BEC DIRETA PELA LINHA 02 DO TOPO)
    # ==========================================
    vcc_track = [
        (cx(2), cy(5)),    # CON1 P1 (+5V BEC)
        (cx(2), cy(2)),    # Sobe livre para Linha 02 no topo
        (cx(12), cy(2)),   # Corre pelo topo desimpedido até Coluna 12
        (cx(12), cy(6)),   # Desce reto até Nano 5V
        (cx(15), cy(6)),   # C1 (+)
        (cx(17), cy(6)),
        (cx(17), cy(8))    # CON4 P2 (+5V MPU)
    ]
    draw_solder_track(vcc_track, "#ff4757", 5, "vcc", label="+5V BUS (Topo)")

    # ==========================================
    # 4. ⚡ BARRAMENTO DE NEUTRO (GND PERIMETRAL SEM NENHUM CRUZAMENTO)
    # ==========================================
    # Tronco Esquerdo: Nano GND (Col 6, Row 6) une a CON1 P2 GND (Col 2, Row 6),
    # segue para Coluna 01 na margem externa e desce desimpedido até CON2 P1 (Col 3, Row 24)
    gnd_left = [
        (cx(6), cy(6)),   # Nano GND (Pin 4)
        (cx(2), cy(6)),   # CON1 P2 GND
        (cx(1), cy(6)),   # Margem externa Coluna 01
        (cx(1), cy(24)),  # Desce livre pela margem esquerda
        (cx(3), cy(24))   # Entra em CON2 P1 GND
    ]
    draw_solder_track(gnd_left, "#00d26a", 5, "gnd", label="GND Esq (Margem Col 01)")

    # Tronco Direito: CON4 P1 GND (Col 17, Row 7) -> C1(-) (Col 14, Row 6) -> Nano GND (Col 12, Row 4)
    # -> Passa para o canal livre Coluna 13 e desce reto até CON3 P6 GND (Col 13, Row 24)
    gnd_right = [
        (cx(17), cy(7)),  # CON4 P1 GND
        (cx(14), cy(6)),  # C1 (-)
        (cx(12), cy(4)),  # Nano GND (Pin 29)
        (cx(13), cy(4)),  # Canal livre Coluna 13
        (cx(13), cy(24))  # Desce reto até CON3 P6 GND
    ]
    draw_solder_track(gnd_right, "#00d26a", 5, "gnd", label="GND Dir (Canal Col 13)")

    # ==========================================
    # 5. 💡 LEDS DIANTEIROS (CON2: Linha 24, Cols 3 a 6) — FLUXO 100% PLANAR
    # ==========================================
    # D9 -> R1 Top (Col 4, Row 18) -> R1 Bot (Col 4, Row 21) -> CON2 P2 (Col 4, Row 24)
    draw_solder_track([(cx(6), cy(14)), (cx(4), cy(14)), (cx(4), cy(18))], "#ffffff", 3, "led-frente", label="D9")
    draw_solder_track([(cx(4), cy(21)), (cx(4), cy(24))], "#ffffff", 4.5, "led-frente")

    # D10 -> R2 Top (Col 5, Row 18) -> R2 Bot (Col 5, Row 21) -> CON2 P3 (Col 5, Row 24)
    draw_solder_track([(cx(6), cy(15)), (cx(5), cy(15)), (cx(5), cy(18))], "#ff9f1a", 3, "led-frente", label="D10")
    draw_solder_track([(cx(5), cy(21)), (cx(5), cy(24))], "#ff9f1a", 4.5, "led-frente")

    # D11 -> R3 Top (Col 6, Row 18) -> R3 Bot (Col 6, Row 21) -> CON2 P4 (Col 6, Row 24)
    draw_solder_track([(cx(6), cy(16)), (cx(6), cy(18))], "#1e90ff", 3, "led-frente", label="D11")
    draw_solder_track([(cx(6), cy(21)), (cx(6), cy(24))], "#1e90ff", 4.5, "led-frente")

    # ==========================================
    # 6. 💡 LEDS TRASEIROS (CON3: Linha 24, Cols 8 a 13) — TRILHAS "L" ANINHADAS (ZERO CRUZAMENTOS!)
    # ==========================================
    # D8 -> R7 Top (Col 8, Row 18) -> R7 Bot (Col 8, Row 21) -> CON3 P1 (Col 8, Row 24)
    draw_solder_track([(cx(6), cy(13)), (cx(8), cy(13)), (cx(8), cy(18))], "#1e90ff", 3, "led-tras", label="D8")
    draw_solder_track([(cx(8), cy(21)), (cx(8), cy(24))], "#1e90ff", 4.5, "led-tras")

    # D7 -> R6 Top (Col 9, Row 18) -> R6 Bot (Col 9, Row 21) -> CON3 P2 (Col 9, Row 24)
    draw_solder_track([(cx(6), cy(12)), (cx(9), cy(12)), (cx(9), cy(18))], "#ffa502", 3, "led-tras", label="D7")
    draw_solder_track([(cx(9), cy(21)), (cx(9), cy(24))], "#ffa502", 4.5, "led-tras")

    # D6 -> R5 Top (Col 10, Row 18) -> R5 Bot (Col 10, Row 21) -> CON3 P3 (Col 10, Row 24)
    draw_solder_track([(cx(6), cy(11)), (cx(10), cy(11)), (cx(10), cy(18))], "#ff4757", 3, "led-tras", label="D6")
    draw_solder_track([(cx(10), cy(21)), (cx(10), cy(24))], "#ff4757", 4.5, "led-tras")

    # D5 -> R4 Top (Col 11, Row 18) -> R4 Bot (Col 11, Row 21) -> CON3 P4 (Col 11, Row 24)
    draw_solder_track([(cx(6), cy(10)), (cx(11), cy(10)), (cx(11), cy(18))], "#ff7f50", 3, "led-tras", label="D5")
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
            lbl_x = x + 24
            lbl_y = y + 3
        elif col == 17:
            lbl_x = x - 24
            lbl_y = y + 3
        elif row == 24:
            lbl_y = y - 14
        elif row == 4 or row == 6:
            lbl_x = x - 22 if col == 12 else x + 22
            lbl_y = y + 3

        svg.append(f'<text class="solder-lbl lbl-{net_id}" x="{lbl_x}" y="{lbl_y}" text-anchor="middle" fill="{n_col}" font-size="7.5" font-weight="bold" pointer-events="none">{pin_lbl}</text>')

    svg.append('</g>')

    # Connectors labels at edges
    # CON1 (Lateral Esquerda)
    svg.append(f'<rect x="{cx(2)-22}" y="{cy(6)-14}" width="44" height="{4*pitch+28}" rx="4" fill="#0a2540" stroke="#00a8ff" stroke-width="1.2"/>')
    svg.append(f'<text x="{cx(2)}" y="{cy(6)+2*pitch+4}" text-anchor="middle" fill="#fff" font-size="10" font-weight="bold" transform="rotate(90 {cx(2)} {cy(6)+2*pitch+4})">CON1: RÁDIO (1x5 90°)</text>')

    # CON4 (Lateral Direita)
    svg.append(f'<rect x="{cx(17)-22}" y="{cy(7)-14}" width="44" height="{3*pitch+28}" rx="4" fill="#2d2805" stroke="#f1c40f" stroke-width="1.2"/>')
    svg.append(f'<text x="{cx(17)}" y="{cy(7)+1.5*pitch+4}" text-anchor="middle" fill="#fff" font-size="10" font-weight="bold" transform="rotate(-90 {cx(17)} {cy(7)+1.5*pitch+4})">CON4: MPU (1x4 90°)</text>')

    # CON2 (Borda Inferior Esquerda)
    svg.append(f'<rect x="{cx(6)-14}" y="{cy(24)+18}" width="{4*pitch}" height="24" rx="4" fill="#0d381e" stroke="#00d26a" stroke-width="1.2"/>')
    svg.append(f'<text x="{(cx(3)+cx(6))/2}" y="{cy(24)+34}" text-anchor="middle" fill="#fff" font-size="10" font-weight="bold">CON2: FRENTE (1x4 90°)</text>')

    # CON3 (Borda Inferior Direita)
    svg.append(f'<rect x="{cx(13)-14}" y="{cy(24)+18}" width="{6*pitch}" height="24" rx="4" fill="#3d1d05" stroke="#ff7f50" stroke-width="1.2"/>')
    svg.append(f'<text x="{(cx(8)+cx(13))/2}" y="{cy(24)+34}" text-anchor="middle" fill="#fff" font-size="10" font-weight="bold">CON3: TRÁS (1x6 90°)</text>')

    svg.append('</svg>')
    return '\n'.join(svg)


def generate_interactive_html():
    svg_top = generate_svg_top()
    svg_bottom = generate_svg_bottom_solder()

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Layout Natural Distribuído v8.0 — Placa Shield Hub 5x7cm</title>
  <style>
    :root {{
      --bg: #090d13;
      --surface: #111722;
      --surface-border: #202d40;
      --text: #e2e8f0;
      --text-muted: #94a3b8;
      --gnd: #00d26a;
      --vcc: #ff4757;
      --accent: #00a8ff;
      --radio: #ffd32a;
      --led-front: #ffffff;
      --led-rear: #ff7f50;
      --i2c: #2ed573;
      --radius: 10px;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      background: var(--bg);
      color: var(--text);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }}
    header {{
      background: linear-gradient(180deg, #162233 0%, #0d1520 100%);
      border-bottom: 1px solid var(--surface-border);
      padding: 14px 24px;
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
    }}
    .title-area h1 {{
      font-size: 1.35rem;
      font-weight: 700;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .badge {{
      background: rgba(0, 210, 106, 0.15);
      color: var(--gnd);
      border: 1px solid var(--gnd);
      font-size: 0.75rem;
      padding: 2px 8px;
      border-radius: 20px;
    }}
    .controls-bar {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: center;
    }}
    .btn-group {{
      display: inline-flex;
      background: #070a0f;
      border: 1px solid var(--surface-border);
      border-radius: 8px;
      padding: 2px;
    }}
    .btn-group button {{
      background: transparent;
      border: none;
      color: var(--text-muted);
      padding: 8px 14px;
      font-size: 0.85rem;
      font-weight: 600;
      cursor: pointer;
      border-radius: 6px;
      transition: all 0.2s;
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .btn-group button:hover {{ color: #fff; background: rgba(255,255,255,0.05); }}
    .btn-group button.active {{
      background: var(--accent);
      color: #fff;
      box-shadow: 0 2px 8px rgba(0, 168, 255, 0.4);
    }}
    .main-layout {{
      display: flex;
      flex: 1;
      overflow: hidden;
      position: relative;
    }}
    .sidebar {{
      width: 440px;
      background: var(--surface);
      border-right: 1px solid var(--surface-border);
      display: flex;
      flex-direction: column;
      overflow-y: auto;
      padding: 20px;
      gap: 18px;
    }}
    @media (max-width: 1080px) {{
      .main-layout {{ flex-direction: column; }}
      .sidebar {{ width: 100%; border-right: none; border-bottom: 1px solid var(--surface-border); }}
    }}
    .step-card {{
      background: #0a0e14;
      border: 1px solid var(--surface-border);
      border-radius: var(--radius);
      padding: 12px 14px;
      cursor: pointer;
      transition: all 0.2s;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}
    .step-card:hover {{ border-color: #3b506b; background: #131b26; }}
    .step-card.active {{
      border-color: var(--accent);
      background: rgba(0, 168, 255, 0.12);
      box-shadow: 0 0 12px rgba(0, 168, 255, 0.2);
    }}
    .step-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.9rem;
      font-weight: 700;
    }}
    .step-badge {{
      font-size: 0.72rem;
      padding: 2px 6px;
      border-radius: 4px;
      font-weight: 600;
    }}
    .step-desc {{ font-size: 0.8rem; color: var(--text-muted); line-height: 1.4; }}
    .step-pads-list {{ display: flex; flex-wrap: wrap; gap: 5px; margin-top: 4px; }}
    .pad-tag {{
      background: rgba(255,255,255,0.08);
      color: #fff;
      font-size: 0.72rem;
      padding: 2px 6px;
      border-radius: 4px;
      font-family: monospace;
    }}
    .inspector-box {{
      background: #0c1219;
      border: 1px solid var(--accent);
      border-radius: var(--radius);
      padding: 14px;
    }}
    .inspector-box h4 {{ color: var(--accent); font-size: 0.95rem; margin-bottom: 8px; }}
    .inspector-row {{
      display: flex;
      justify-content: space-between;
      font-size: 0.82rem;
      padding: 4px 0;
      border-bottom: 1px dashed rgba(255,255,255,0.06);
    }}
    .inspector-row span.lbl {{ color: var(--text-muted); }}
    .inspector-row span.val {{ color: #fff; font-weight: 600; font-family: monospace; }}
    .canvas-area {{
      flex: 1;
      background: #06090d;
      display: flex;
      justify-content: center;
      align-items: center;
      overflow: auto;
      padding: 20px;
      position: relative;
    }}
    .svg-container {{
      max-width: 100%;
      box-shadow: 0 10px 40px rgba(0,0,0,0.8);
      border-radius: 16px;
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
      0% {{ r: 8; stroke-width: 2px; }}
      100% {{ r: 12; stroke-width: 4px; }}
    }}
  </style>
</head>
<body>

<header>
  <div class="title-area">
    <h1>
      ⚡ Layout Natural Distribuído (v8.0)
      <span class="badge">Zero Cruzamentos</span>
    </h1>
    <p style="font-size:0.85rem; color:var(--text-muted); margin-top:2px;">
      Trilhas ultracurtas de 10mm • Rádio na lateral esq. • MPU na lateral dir. • LEDs na borda inferior
    </p>
  </div>
  <div class="controls-bar">
    <div class="btn-group">
      <button id="btn-bottom" class="active" onclick="switchMainView('bottom')">
        🔄 Vista do Verso (Solda Física)
      </button>
      <button id="btn-top" onclick="switchMainView('top')">
        👁️ Vista Superior (Componentes)
      </button>
      <button id="btn-xray" onclick="switchMainView('xray')">
        🩻 Raio-X Sobreposto
      </button>
    </div>
  </div>
</header>

<div class="main-layout">
  <div class="sidebar">
    <div>
      <h3 style="font-size:0.85rem; text-transform:uppercase; letter-spacing:1px; color:var(--text-muted); margin-bottom:10px;">
        📌 Circuitos &amp; Passos de Soldagem
      </h3>

      <div style="display:flex; flex-direction:column; gap:10px;">
        <div class="step-card active" onclick="activateStep('all', this)">
          <div class="step-header">
            <span>✨ Visão Geral do Layout v8.0</span>
            <span class="step-badge" style="background:#202d40; color:#fff;">34 Furos</span>
          </div>
          <div class="step-desc">Mostra todas as ligações organizadas com conexões ultracurtas e ZERO sobreposição de fios.</div>
        </div>

        <div class="step-card" onclick="activateStep('radio', this)">
          <div class="step-header" style="color:var(--radio);">
            <span>1️⃣ Sinais do Rádio (Lateral Esquerda)</span>
            <span class="step-badge" style="background:rgba(255,211,42,0.2); color:var(--radio);">Trilhas de 10mm!</span>
          </div>
          <div class="step-desc">
            CON1 fica na Coluna 02 (Linhas 5 a 9), face a face com D2, D3, D4! Conexões 100% horizontais e paralelas de 10mm sem nenhum desvio.
          </div>
          <div class="step-pads-list">
            <span class="pad-tag">CH2: CON1 P3 (02,07) ➔ D2 (06,07)</span>
            <span class="pad-tag">CH4: CON1 P4 (02,08) ➔ D3 (06,08)</span>
            <span class="pad-tag">CH1: CON1 P5 (02,09) ➔ D4 (06,09)</span>
          </div>
        </div>

        <div class="step-card" onclick="activateStep('i2c', this)">
          <div class="step-header" style="color:var(--i2c);">
            <span>2️⃣ Interface I2C MPU-6050 (Lateral Direita)</span>
            <span class="step-badge" style="background:rgba(46,213,115,0.2); color:var(--i2c);">Trilhas de 10mm!</span>
          </div>
          <div class="step-desc">
            CON4 fica na Coluna 17 (Linhas 7 a 10), face a face com A4 (SDA) e A5 (SCL). Trilhas 100% horizontais retas de 10mm.
          </div>
          <div class="step-pads-list">
            <span class="pad-tag">SCL: CON4 P3 (17,09) ➔ A5 (12,09)</span>
            <span class="pad-tag">SDA: CON4 P4 (17,10) ➔ A4 (12,10)</span>
          </div>
        </div>

        <div class="step-card" onclick="activateStep('vcc', this)">
          <div class="step-header" style="color:var(--vcc);">
            <span>3️⃣ Linha +5V Direta (Linha 02 no Topo)</span>
            <span class="step-badge" style="background:rgba(255,71,87,0.2); color:var(--vcc);">Zero Cruzamento</span>
          </div>
          <div class="step-desc">
            Alimentação do BEC entra em CON1 P1 (Col 02, Lin 05), sobe até a Linha 02 livre no topo e corre desimpedida até Nano 5V (Col 12), C1 e MPU-6050.
          </div>
          <div class="step-pads-list">
            <span class="pad-tag">CON1 P1 (02,05)</span>
            <span class="pad-tag">Linha 02 Topo</span>
            <span class="pad-tag">Nano 5V (12,06)</span>
            <span class="pad-tag">C1 (+) (15,06)</span>
            <span class="pad-tag">CON4 P2 (17,08)</span>
          </div>
        </div>

        <div class="step-card" onclick="activateStep('gnd', this)">
          <div class="step-header" style="color:var(--gnd);">
            <span>4️⃣ Barramento GND Perimetral</span>
            <span class="step-badge" style="background:rgba(0,210,106,0.2); color:var(--gnd);">100% Interligado</span>
          </div>
          <div class="step-desc">
            Dois troncos independentes sem laços nem curtos: Tronco esquerdo corre pela margem da Coluna 01 até CON2 P1 (GND Frente). Tronco direito desce pela Coluna 13 até CON3 P6 (GND Trás).
          </div>
          <div class="step-pads-list">
            <span class="pad-tag">Nano GND Esq (06,06)</span>
            <span class="pad-tag">CON1 P2 (02,06)</span>
            <span class="pad-tag">Margem Col 01 ➔ CON2 P1 (03,24)</span>
            <span class="pad-tag">Nano GND Dir (12,04)</span>
            <span class="pad-tag">C1 (-) (14,06)</span>
            <span class="pad-tag">CON4 P1 (17,07)</span>
            <span class="pad-tag">Canal Col 13 ➔ CON3 P6 (13,24)</span>
          </div>
        </div>

        <div class="step-card" onclick="activateStep('led-frente', this)">
          <div class="step-header" style="color:#ffffff;">
            <span>5️⃣ LEDs Dianteiros (Borda Inferior Esquerda)</span>
            <span class="step-badge" style="background:rgba(255,255,255,0.2); color:#fff;">100% Planar</span>
          </div>
          <div class="step-desc">
            D9, D10, D11 descem em trilhas paralelas por R1, R2, R3 (Linhas 18 a 21) até CON2 (Linha 24, Colunas 3 a 6).
          </div>
          <div class="step-pads-list">
            <span class="pad-tag">D9 ➔ R1 (100Ω) ➔ CON2 P2 (Farol)</span>
            <span class="pad-tag">D10 ➔ R2 (150Ω) ➔ CON2 P3 (Pis.FE)</span>
            <span class="pad-tag">D11 ➔ R3 (150Ω) ➔ CON2 P4 (Pis.FD)</span>
          </div>
        </div>

        <div class="step-card" onclick="activateStep('led-tras', this)">
          <div class="step-header" style="color:var(--led-rear);">
            <span>6️⃣ LEDs Traseiros (Trilhas em "L" Aninhadas)</span>
            <span class="step-badge" style="background:rgba(255,127,80,0.2); color:var(--led-rear);">Zero Cruzamento</span>
          </div>
          <div class="step-desc">
            D5..D8 utilizam roteamento planar com trilhas em "L" aninhadas (cada uma com sua linha e coluna exclusivas): D8➔Col 8, D7➔Col 9, D6➔Col 10, D5➔Col 11.
          </div>
          <div class="step-pads-list">
            <span class="pad-tag">D8 (Lin 13) ➔ R7 (150Ω, Col 8) ➔ CON3 P1 (Pis.TD)</span>
            <span class="pad-tag">D7 (Lin 12) ➔ R6 (150Ω, Col 9) ➔ CON3 P2 (Pis.TE)</span>
            <span class="pad-tag">D6 (Lin 11) ➔ R5 (150Ω, Col 10) ➔ CON3 P3 (Freio)</span>
            <span class="pad-tag">D5 (Lin 10) ➔ R4 (150Ω, Col 11) ➔ CON3 P4 (Lant.)</span>
          </div>
        </div>
      </div>
    </div>

    <div>
      <div id="inspector-card" class="inspector-box">
        <h4>🔎 Inspetor de Solda</h4>
        <p style="font-size:0.8rem; color:var(--text-muted); line-height:1.4;">
          Passe o mouse ou clique sobre qualquer gota prateada de solda para ver a coordenada e a instrução.
        </p>
      </div>
    </div>
  </div>

  <div class="canvas-area">
    <div id="panel-bottom" class="svg-container view-panel active">
      {svg_bottom}
    </div>
    <div id="panel-top" class="svg-container view-panel">
      {svg_top}
    </div>
    <div id="panel-xray" class="svg-container view-panel" style="position:relative;">
      <div style="opacity:0.35; position:absolute; inset:0; pointer-events:none;">
        {svg_top}
      </div>
      <div style="opacity:0.9;">
        {svg_bottom}
      </div>
    </div>
  </div>
</div>

<script>
  function switchMainView(mode) {{
    document.querySelectorAll('.view-panel').forEach(p => p.classList.remove('active'));
    document.querySelectorAll('.btn-group button').forEach(b => b.classList.remove('active'));

    if (mode === 'bottom') {{
      document.getElementById('panel-bottom').classList.add('active');
      document.getElementById('btn-bottom').classList.add('active');
    }} else if (mode === 'top') {{
      document.getElementById('panel-top').classList.add('active');
      document.getElementById('btn-top').classList.add('active');
    }} else if (mode === 'xray') {{
      document.getElementById('panel-xray').classList.add('active');
      document.getElementById('btn-xray').classList.add('active');
    }}
  }}

  function activateStep(stepId, cardElem) {{
    document.querySelectorAll('.step-card').forEach(c => c.classList.remove('active'));
    cardElem.classList.add('active');

    const svgRoot = document.getElementById('svg-bottom-root');
    if (!svgRoot) return;

    if (stepId === 'all') {{
      svgRoot.querySelectorAll('.solder-joint, .solder-ring, .solder-lbl, .track-line').forEach(el => {{
        el.classList.remove('dimmed');
        el.classList.remove('highlight-focus');
      }});
      updateInspector("Visão Geral do Layout v8.0", "34 pontos de solda", "Conexões ultracurtas com zero cruzamentos");
      return;
    }}

    svgRoot.querySelectorAll('.solder-joint, .solder-ring, .solder-lbl').forEach(el => {{
      if (el.classList.contains('pad-' + stepId) || el.classList.contains('lbl-' + stepId)) {{
        el.classList.remove('dimmed');
        el.classList.add('highlight-focus');
      }} else {{
        el.classList.add('dimmed');
        el.classList.remove('highlight-focus');
      }}
    }});

    svgRoot.querySelectorAll('.track-line').forEach(el => {{
      if (el.classList.contains('track-' + stepId)) {{
        el.classList.remove('dimmed');
      }} else {{
        el.classList.add('dimmed');
      }}
    }});
  }}

  function updateInspector(title, colRow, desc, comp) {{
    const box = document.getElementById('inspector-card');
    box.innerHTML = `
      <h4>📍 ${{title}}</h4>
      <div class="inspector-row"><span class="lbl">Coordenada:</span><span class="val">${{colRow}}</span></div>
      ${{comp ? `<div class="inspector-row"><span class="lbl">Componente:</span><span class="val">${{comp}}</span></div>` : ''}}
      <div style="margin-top:8px; font-size:0.82rem; color:#a2d9ce; line-height:1.4;">
        <b>Como soldar:</b> ${{desc}}
      </div>
    `;
  }}

  document.addEventListener('DOMContentLoaded', () => {{
    document.querySelectorAll('.solder-joint').forEach(pad => {{
      pad.addEventListener('mouseenter', () => {{
        const col = pad.getAttribute('data-col');
        const row = pad.getAttribute('data-row');
        const pin = pad.getAttribute('data-pin');
        const comp = pad.getAttribute('data-comp');
        const desc = pad.getAttribute('data-desc');
        updateInspector(pin, `Coluna ${{col.padStart(2,'0')}}, Linha ${{row.padStart(2,'0')}}`, desc, comp);
      }});

      pad.addEventListener('click', () => {{
        const net = pad.getAttribute('data-net');
        const stepCard = document.querySelector(`.step-card[onclick*="'${{net}}'"]`);
        if (stepCard) activateStep(net, stepCard);
      }});
    }});
  }});
</script>

</body>
</html>
"""
    return html

if __name__ == "__main__":
    top_svg = generate_svg_top()
    with open("placa_shield_superior.svg", "w", encoding="utf-8") as f:
        f.write(top_svg)
    print("Generated placa_shield_superior.svg (v8.0)")

    bot_svg = generate_svg_bottom_solder()
    with open("placa_shield_inferior.svg", "w", encoding="utf-8") as f:
        f.write(bot_svg)
    print("Generated placa_shield_inferior.svg (v8.0)")

    html = generate_interactive_html()
    with open("placa_shield_visualizador.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated placa_shield_visualizador.html (v8.0)")
