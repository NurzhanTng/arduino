from lib import *

WOOD = H('#D9A066'); WOOD_D = H('#8B5A2B'); WOOD_L = H('#C68B4E')
GRAYW = H('#8A93A6')


# ---------- components ----------
def led(c, cx, cy, r, color, on=True, glow=True):
    if on and glow:
        for kk, a in ((2.5, 0.10), (1.9, 0.16), (1.4, 0.26)):
            c.saveState(); c.setFillColor(color); c.setFillAlpha(a); c.circle(cx, cy, r * kk, fill=1, stroke=0); c.restoreState()
    circ(c, cx, cy, r, fill=color if on else mix(color, H('#DCE1EA'), 0.72), stroke=INK, lw=1.3)
    c.saveState(); c.setFillColor(white); c.setFillAlpha(0.6); c.circle(cx - r * .35, cy + r * .35, r * .22, fill=1, stroke=0); c.restoreState()


def led_real(c, cx, cy, color, s=1.0):
    line(c, cx - 4 * s, cy, cx - 4 * s, cy - 36 * s, GRAYW, 1.8 * s)
    line(c, cx + 4 * s, cy, cx + 4 * s, cy - 26 * s, GRAYW, 1.8 * s)
    p = c.beginPath(); p.moveTo(cx - 10 * s, cy); p.lineTo(cx - 10 * s, cy + 14 * s)
    p.arcTo(cx - 10 * s, cy + 4 * s, cx + 10 * s, cy + 24 * s, 180, -180); p.lineTo(cx + 10 * s, cy); p.close()
    c.saveState(); c.setFillColor(color); c.setStrokeColor(INK); c.setLineWidth(1.2); c.drawPath(p, fill=1, stroke=1); c.restoreState()
    rr(c, cx - 12 * s, cy - 2 * s, 24 * s, 4 * s, 1.5, fill=mix(color, black, 0.25), stroke=INK, lw=1)
    c.saveState(); c.setFillColor(white); c.setFillAlpha(0.6); c.circle(cx - 4 * s, cy + 17 * s, 2.6 * s, fill=1, stroke=0); c.restoreState()


def resistor(c, x, y, w, h=13):
    line(c, x, y, x + w, y, GRAYW, 2)
    bx = x + w * 0.18; bw = w * 0.64
    rr(c, bx, y - h / 2, bw, h, 5, fill=H('#E9C58B'), stroke=H('#8B6B3A'), lw=1.1)
    for f, cl in ((0.2, RED), (0.34, RED), (0.48, H('#7B4A1E')), (0.8, H('#D4AF37'))):
        c.saveState(); c.setFillColor(cl); c.rect(bx + bw * f, y - h / 2 + 0.6, 3.4, h - 1.2, fill=1, stroke=0); c.restoreState()


def button_sym(c, cx, cy, s=28, pressed=False):
    rr(c, cx - s / 2, cy - s / 2, s, s, 4, fill=H('#B8BFCC'), stroke=INK, lw=1.2)
    circ(c, cx, cy, s * 0.32, fill=H('#2B3245') if not pressed else H('#566080'))
    c.saveState(); c.setFillColor(white); c.setFillAlpha(0.35); c.circle(cx - s * .1, cy + s * .1, s * .09, fill=1, stroke=0); c.restoreState()
    for dx in (-1, 1):
        for dy in (-1, 1): circ(c, cx + dx * s * .38, cy + dy * s * .38, 1.5, fill=GRAYW)


def board_icon(c, cx, cy):
    rr(c, cx - 48, cy - 31, 96, 62, 5, fill=TEAL, stroke=H('#006a6e'), lw=1.3)
    c.saveState(); c.setFillColor(H('#C9CFDB')); c.setStrokeColor(GRAYW); c.rect(cx - 56, cy + 2, 26, 22, fill=1, stroke=1); c.restoreState()
    c.saveState(); c.setFillColor(H('#20242F')); c.rect(cx - 8, cy - 9, 40, 14, fill=1, stroke=0)
    c.rect(cx - 38, cy + 24, 76, 5, fill=1, stroke=0); c.rect(cx - 30, cy - 29, 60, 5, fill=1, stroke=0); c.restoreState()
    T(c, 'UNO', cx - 26, cy - 8, 9, 'SB', white)


def breadboard_icon(c, cx, cy):
    rr(c, cx - 46, cy - 28, 92, 56, 4, fill=H('#F1EAD8'), stroke=H('#B9AE93'), lw=1)
    line(c, cx - 42, cy + 23, cx + 42, cy + 23, RED, 1.2); line(c, cx - 42, cy + 19, cx + 42, cy + 19, BLUE, 1.2)
    line(c, cx - 42, cy - 19, cx + 42, cy - 19, RED, 1.2); line(c, cx - 42, cy - 23, cx + 42, cy - 23, BLUE, 1.2)
    for blk in (10, -14):
        for r_ in range(4):
            for q in range(14): circ(c, cx - 39 + q * 6, cy + blk - r_ * 4.4, 1.15, fill=H('#8D8672'))


def wires_icon(c, cx, cy):
    for i, (col, dy) in enumerate(((RED, 14), (BLUE, 0), (H('#333333'), -14))):
        c.saveState(); c.setStrokeColor(col); c.setLineWidth(3.4)
        p = c.beginPath(); p.moveTo(cx - 40, cy + dy - 6); p.curveTo(cx - 15, cy + dy + 22, cx + 15, cy + dy - 22, cx + 40, cy + dy + 6)
        c.drawPath(p, fill=0, stroke=1); c.restoreState()
        for x_ in (cx - 40, cx + 40):
            c.saveState(); c.setFillColor(H('#20242F')); c.rect(x_ - 3, cy + dy + (-9 if x_ < cx else 3), 6, 6, fill=1, stroke=0); c.restoreState()


def box3d(c, cx, by, name, val, col, bw=96, bh=58, nsize=11, vsize=17):
    cwid = max(48, bw * 0.5)
    rr(c, cx - cwid / 2, by + bh - 6, cwid, bh * 0.6, 5, fill=white, stroke=col, lw=2)
    T(c, val, cx, by + bh + 7, vsize, 'MB', col, 'c')
    rr(c, cx - bw / 2, by, bw, bh, 5, fill=WOOD, stroke=WOOD_D, lw=1.5)
    rr(c, cx - bw / 2 - 4, by + bh - 12, bw + 8, 12, 3, fill=WOOD_L, stroke=WOOD_D, lw=1.5)
    rr(c, cx - bw * .36, by + 7, bw * .72, bh * .38, 3, fill=white, stroke=WOOD_D, lw=1)
    T(c, name, cx, by + 7 + bh * .38 / 2 - nsize * .33, nsize, 'MB', INK, 'c')


# ---------- big diagrams ----------
def d_parts(c, w, h):
    cw = (w - 24) / 3; ch = (h - 12) / 2
    items = [('Плата Arduino Uno', 'и USB-кабель к компьютеру', board_icon),
             ('Светодиоды', '3 штуки: красный, жёлтый, зелёный', None),
             ('Резисторы 220 Ом', 'по одному на каждый светодиод', None),
             ('Кнопка', 'одна или две штуки', None),
             ('Провода-перемычки', 'разные цвета — удобнее', wires_icon),
             ('Макетная плата', 'чтобы собирать без пайки', breadboard_icon)]
    for i, (t1, t2, fn) in enumerate(items):
        col, row = i % 3, i // 3
        x = col * (cw + 12); y = (1 - row) * (ch + 12)
        rr(c, x, y, cw, ch, 8, fill=white, stroke=LINEC, lw=1.2)
        cx, cy = x + cw / 2, y + ch - 50
        if fn: fn(c, cx, cy)
        elif i == 1:
            for j, cl in enumerate((RED, YELLOW, GREEN)): led_real(c, cx - 34 + j * 34, cy - 2, cl, 0.95)
        elif i == 2: resistor(c, cx - 40, cy, 80, 15)
        elif i == 3: button_sym(c, cx, cy, 40)
        T(c, t1, cx, y + 22, 9.6, 'SB', INK, 'c'); T(c, t2, cx, y + 10, 7.4, 'S', MUTE, 'c')


def d_roadmap(c, w, h):
    cards = [('1', 'Переменные', 'коробки для чисел', BLUE, BLUE_L), ('2', 'Типы данных', 'коробки разной формы', PURPLE, PURPLE_L),
             ('3', 'if / else', 'развилка на дороге', ORANGE, ORANGE_L), ('4', 'Кнопка', 'Arduino чувствует руку', GREEN, GREEN_L)]
    cw = (w - 3 * 14) / 4
    for i, (n, t1, t2, col, lt) in enumerate(cards):
        x = i * (cw + 14)
        rr(c, x, 0, cw, h, 10, fill=lt, stroke=col, lw=2)
        circ(c, x + cw / 2, h - 30, 18, fill=col); T(c, n, x + cw / 2, h - 37, 20, 'SB', white, 'c')
        T(c, t1, x + cw / 2, h - 70, 11.5, 'SB', col, 'c')
        TW(c, t2, x + cw / 2, h - 88, cw - 16, 9, 'S', INK, 'c')
        if i < 3: arrow(c, x + cw + 1, h / 2 + 8, x + cw + 13, h / 2 + 8, MUTE, 1.6, 5)


def d_wiring(c, w, h, rows):
    bw = 118; n = len(rows); top = h - 20; bot = 58; rowh = (top - bot) / n
    rr(c, 0, 0, bw, h, 10, fill=TEAL, stroke=H('#006a6e'), lw=1.5)
    T(c, 'ARDUINO UNO', bw / 2 - 4, h - 15, 9.5, 'SB', white, 'c')
    c.saveState(); c.setFillColor(H('#20242F')); c.rect(12, h / 2 - 10, 36, 20, fill=1, stroke=0); c.restoreState()
    T(c, 'ATmega', 30, h / 2 - 3, 6.5, 'S', H('#9AA3B5'), 'c')
    xe = w - 22; cxx = bw + 190; gy = 22
    ys = [top - rowh * (i + .5) for i in range(n)]
    for y, r in zip(ys, rows):
        c.saveState(); c.setFillColor(H('#20242F')); c.rect(bw - 4, y - 4.5, 9, 9, fill=1, stroke=0); c.restoreState()
        T(c, 'пин ' + r['pin'], bw - 9, y - 3, 8.5, 'SB', white, 'r')
        sc = r['color'] if r['kind'] == 'led' else ORANGE
        if r['kind'] == 'led':
            line(c, bw + 4, y, bw + 44, y, sc, 2.6)
            resistor(c, bw + 44, y, 92, 14)
            line(c, bw + 136, y, cxx - 14, y, sc, 2.6)
            led(c, cxx, y, 13, r['color'], True, False)
            T(c, '+', cxx - 25, y + 6, 11, 'SB', RED, 'c'); T(c, '−', cxx + 25, y + 6, 12, 'SB', INK, 'c')
            line(c, cxx + 14, y, xe, y, INK, 2.6)
            T(c, '220 Ом', bw + 90, y - 17, 7.6, 'S', MUTE, 'c')
            T(c, r.get('label', 'светодиод'), cxx, y - 26, 7.6, 'S', MUTE, 'c')
        else:
            line(c, bw + 4, y, cxx - 17, y, sc, 2.6)
            button_sym(c, cxx, y, 28)
            line(c, cxx + 17, y, xe, y, INK, 2.6)
            T(c, r.get('label', 'кнопка'), cxx, y - 26, 7.6, 'S', MUTE, 'c')
        circ(c, xe, y, 3, fill=INK)
    line(c, xe, ys[0], xe, gy, INK, 2.6); line(c, xe, gy, bw + 4, gy, INK, 2.6)
    c.saveState(); c.setFillColor(H('#20242F')); c.rect(bw - 4, gy - 4.5, 9, 9, fill=1, stroke=0); c.restoreState()
    T(c, 'GND', bw - 9, gy - 3, 8.5, 'SB', white, 'r')
    T(c, 'общий провод GND («земля», минус)', (xe + bw) / 2, gy - 15, 8, 'S', MUTE, 'c')


def d_vars_boxes(c, w, h):
    items = [('pauza', '500', 'int pauza = 500;', BLUE), ('lampa', '8', 'int lampa = 8;', GREEN), ('schet', '0', 'int schet = 0;', ORANGE)]
    cw = w / 3
    for i, (nm, v, code_, col) in enumerate(items):
        cx = cw * i + cw / 2
        box3d(c, cx, 46, nm, v, col)
        T(c, code_, cx, 20, 11, 'MB', col, 'c')


def d_anatomy(c, w, h):
    code_ = 'int pauza = 500;'; size = 32; cwid = stringWidth('0', 'M', size)
    x0 = (w - len(code_) * cwid) / 2; base = h - 40
    parts = [(0, 3, PURPLE, 'тип', 'какая коробка (целое число)'), (4, 5, BLUE, 'имя', 'что написано на наклейке'),
             (10, 1, RED, 'положить', 'знак «положи внутрь»'), (12, 3, ORANGE, 'значение', 'что лежит внутри'),
             (15, 1, MUTE, 'точка с запятой', 'конец команды')]
    for i, (st, ln, col, lab, desc) in enumerate(parts):
        cx = x0 + (st + ln / 2) * cwid
        yl = base - 44 - (i % 2) * 44
        line(c, cx, base - 12, cx, yl + 12, col, 1.4, (2, 2))
    for i, (st, ln, col, lab, desc) in enumerate(parts):
        cx = x0 + (st + ln / 2) * cwid
        T(c, code_[st:st + ln], x0 + st * cwid, base, size, 'MB', col)
        line(c, x0 + st * cwid, base - 8, x0 + (st + ln) * cwid, base - 8, col, 4)
        yl = base - 44 - (i % 2) * 44
        T(c, lab, cx, yl, 10.5, 'SB', col, 'c')
        TW(c, desc, cx, yl - 11, 74, 8, 'S', MUTE, 'c', 9)


def d_change(c, w, h):
    n = 5; cw = w / n
    for i in range(n):
        cx = cw * i + cw / 2
        box3d(c, cx, 34, 'schet', str(i), ORANGE, bw=70, bh=42, nsize=9, vsize=15)
        if i < n - 1:
            arrow(c, cx + 42, 60, cx + cw - 42, 60, RED, 2)
            T(c, '+ 1', cx + cw / 2, 66, 9.5, 'SB', RED, 'c')
    T(c, 'каждый раз: взяли то, что лежало, добавили 1 и положили обратно', w / 2, 8, 9, 'S', MUTE, 'c')


def d_brightness(c, w, h):
    vals = [0, 30, 100, 180, 255]; cw = w / len(vals)
    for i, v in enumerate(vals):
        cx = cw * i + cw / 2; cy = h - 36
        t = v / 255
        for kk, a in ((2.6, .10), (2.0, .16), (1.5, .24)):
            if t > 0.05:
                c.saveState(); c.setFillColor(YELLOW); c.setFillAlpha(a * t); c.circle(cx, cy, 14 * kk, fill=1, stroke=0); c.restoreState()
        circ(c, cx, cy, 14, fill=mix(H('#DCE1EA'), YELLOW, t), stroke=INK, lw=1.3)
        T(c, 'yarkost = ' + str(v), cx, 20, 9, 'MB', INK, 'c')
        T(c, ['выключено', 'едва светит', 'тускло', 'ярко', 'на полную'][i], cx, 8, 8, 'S', MUTE, 'c')


def d_types(c, w, h):
    cards = [('int', PURPLE, PURPLE_L, 'целое число', 'сколько? какой номер?', '10   -5   500'),
             ('float', BLUE, BLUE_L, 'число с точкой', 'рост, вес, температура', '1.45   36.6'),
             ('bool', GREEN, GREEN_L, 'да или нет', 'горит ли? нажата ли?', 'true   false'),
             ('String', ORANGE, ORANGE_L, 'текст', 'имя, слово, фраза', '"Anya"')]
    cw = (w - 3 * 10) / 4
    for i, (nm, col, lt, t1, t2, ex) in enumerate(cards):
        x = i * (cw + 10)
        rr(c, x, 0, cw, h, 10, fill=lt, stroke=col, lw=2)
        T(c, nm, x + cw / 2, h - 28, 20, 'MB', col, 'c')
        cx = x + cw / 2; cy = h - 82
        if i == 0:
            rr(c, cx - 26, cy - 24, 52, 48, 5, fill=white, stroke=col, lw=2.5); T(c, '42', cx, cy - 7, 20, 'MB', col, 'c')
        elif i == 1:
            rr(c, cx - 34, cy - 20, 68, 40, 20, fill=white, stroke=col, lw=2.5); T(c, '3.14', cx, cy - 6, 17, 'MB', col, 'c')
        elif i == 2:
            rr(c, cx - 38, cy + 2, 46, 20, 10, fill=GREEN, stroke=INK, lw=1); circ(c, cx + 0, cy + 12, 7.5, fill=white)
            T(c, 'true', cx + 14, cy + 9, 9, 'MB', GREEN)
            rr(c, cx - 38, cy - 24, 46, 20, 10, fill=H('#C9CFDB'), stroke=INK, lw=1); circ(c, cx - 28, cy - 14, 7.5, fill=white)
            T(c, 'false', cx + 14, cy - 17, 9, 'MB', MUTE)
        else:
            for j, ch_ in enumerate('Anya'): 
                rr(c, cx - 39 + j * 19, cy - 13, 17, 26, 3, fill=white, stroke=col, lw=1.6); T(c, ch_, cx - 30.5 + j * 19, cy - 5, 13, 'MB', col, 'c')
            T(c, '"', cx - 46, cy - 3, 16, 'MB', col, 'c'); T(c, '"', cx + 39, cy - 3, 16, 'MB', col, 'c')
        T(c, t1, cx, h - 132, 10, 'SB', INK, 'c')
        TW(c, t2, cx, h - 147, cw - 14, 8.5, 'S', MUTE, 'c')
        rr(c, x + 8, 8, cw - 16, 22, 5, fill=white, stroke=col, lw=1); T(c, ex, cx, 15, 9.2, 'MB', INK, 'c')


def d_serial(c, w, h, lines, title='Монитор порта', baud='9600 бод', tsize=10):
    rr(c, 0, 0, w, h, 7, fill=H('#0F1420'), stroke=H('#3A4157'), lw=1.4)
    rr(c, 0, h - 20, w, 20, 7, fill=H('#39415A')); c.saveState(); c.setFillColor(H('#39415A')); c.rect(0, h - 20, w, 8, fill=1, stroke=0); c.restoreState()
    for i, cl in enumerate([RED, YELLOW, GREEN]): circ(c, 12 + i * 12, h - 10, 3.3, fill=cl)
    T(c, title, w / 2 + 12, h - 14, 8.3, 'SB', white, 'c')
    for i, l in enumerate(lines): T(c, l, 10, h - 38 - i * (tsize + 4.5), tsize, 'M', H('#7CFC9A'))
    T(c, baud, w - 8, 6, 7.5, 'S', H('#8A93A6'), 'r')


# ---------- flowcharts ----------
def pill(c, cx, cy, w, h, text, fill, stroke, size=10, font='SB', tcol=INK):
    rr(c, cx - w / 2, cy - h / 2, w, h, h / 2, fill=fill, stroke=stroke, lw=1.6); T(c, text, cx, cy - size * .35, size, font, tcol, 'c')


def node(c, cx, cy, w, h, t1, t2, fill, stroke):
    rr(c, cx - w / 2, cy - h / 2, w, h, 7, fill=fill, stroke=stroke, lw=1.8)
    if t2:
        T(c, t1, cx, cy + 4, 9.6, 'SB', INK, 'c'); T(c, t2, cx, cy - 10, 8.4, 'M', MUTE, 'c')
    else: T(c, t1, cx, cy - 3, 9.6, 'SB', INK, 'c')


def diamond(c, cx, cy, w, h, text, fill, stroke, size=10.5):
    poly(c, [(cx, cy + h / 2), (cx + w / 2, cy), (cx, cy - h / 2), (cx - w / 2, cy)], fill, stroke, 1.8)
    T(c, text, cx, cy - size * .33, size, 'MB', INK, 'c')


def d_flow2(c, w, h, cond, yes, no, top='loop() начался', bottom='delay(1000)  и снова сначала'):
    cx = w / 2
    pill_h, node_h = 24, 42
    top_cy = h - 14
    bot_cy = 16
    dcy = h * 0.62
    by = h * 0.36
    ym = h * 0.13
    dw, dh = min(240, w * 0.48), min(70, h * 0.14)
    nw = min(176, w * 0.34)
    bx1, bx2 = w * 0.20, w * 0.80
    spread = min(120, w * 0.24)

    pill(c, cx, top_cy, 150, pill_h, top, H('#E8ECF5'), MUTE, 9.5)
    arrow(c, cx, top_cy - pill_h / 2 - 2, cx, dcy + dh / 2 + 2, MUTE)
    diamond(c, cx, dcy, dw, dh, cond, YELLOW_L, H('#C98A00'))
    line(c, cx - spread, dcy, bx1, dcy, GREEN, 2.2)
    arrow(c, bx1, dcy, bx1, by + node_h / 2, GREEN, 2.2)
    line(c, cx + spread, dcy, bx2, dcy, RED, 2.2)
    arrow(c, bx2, dcy, bx2, by + node_h / 2, RED, 2.2)
    T(c, 'ДА', cx - spread - 10, dcy + 6, 10.5, 'SB', GREEN, 'r')
    T(c, 'НЕТ', cx + spread + 4, dcy + 6, 10.5, 'SB', RED)
    node(c, bx1, by, nw, node_h, yes[0], yes[1], GREEN_L, GREEN)
    node(c, bx2, by, nw, node_h, no[0], no[1], RED_L, RED)
    line(c, bx1, by - node_h / 2, bx1, ym, MUTE, 1.6)
    line(c, bx2, by - node_h / 2, bx2, ym, MUTE, 1.6)
    line(c, bx1, ym, bx2, ym, MUTE, 1.6)
    arrow(c, cx, ym, cx, bot_cy + pill_h / 2 + 2, MUTE)
    pill(c, cx, bot_cy, min(210, w * 0.42), pill_h, bottom, H('#E8ECF5'), MUTE, 9.5)


def d_flow3(c, w, h, conds, outs):
    cx = w * 0.36
    pill_h, node_h = 22, 42
    dw = min(230, w * 0.46)
    dh = min(62, h * 0.11)
    nx = min(cx + 250, w - 100)
    gap = max(72, (h - 50) / 4.2)
    y1 = h - 38 - gap
    y2 = y1 - gap
    y3 = y2 - gap

    pill(c, cx, h - 12, 150, pill_h, 'loop() начался', H('#E8ECF5'), MUTE, 9.5)
    arrow(c, cx, h - 24, cx, y1 + dh / 2 + 2, MUTE)
    for y, cnd in ((y1, conds[0]), (y2, conds[1])):
        diamond(c, cx, y, dw, dh, cnd, YELLOW_L, H('#C98A00'), 10.5)
    for y, (t1, t2, fill, st) in ((y1, outs[0]), (y2, outs[1])):
        arrow(c, cx + dw / 2 + 4, y, nx - 95, y, GREEN, 2.2)
        node(c, nx, y, min(190, w - nx - 10), node_h, t1, t2, fill, st)
        T(c, 'ДА', cx + dw / 2 + 8, y + 6, 10, 'SB', GREEN)
    arrow(c, cx, y1 - dh / 2 - 2, cx, y2 + dh / 2 + 2, RED, 2.2)
    T(c, 'НЕТ', cx + 6, (y1 + y2) / 2, 10, 'SB', RED)
    arrow(c, cx, y2 - dh / 2 - 2, cx, y3 + node_h / 2, RED, 2.2)
    T(c, 'НЕТ', cx + 6, y2 - dh / 2 - 14, 10, 'SB', RED)
    t1, t2, fill, st = outs[2]
    node(c, cx, y3, min(190, w * 0.38), node_h, t1, t2, fill, st)


def d_timeline(c, w, h, lab1, lab2, items, lamp_col=YELLOW):
    n = len(items); x0 = 78; cw = (w - x0) / n
    T(c, lab1, 2, h - 22, 10, 'MB', MUTE); T(c, lab2, 2, 24, 9.5, 'SB', MUTE)
    for i, (top, on, bot) in enumerate(items):
        cx = x0 + cw * i + cw / 2
        rr(c, x0 + cw * i + 3, 2, cw - 6, h - 4, 8, fill=GREEN_L if on else H('#F1F3F8'), stroke=GREEN if on else LINEC, lw=1.4)
        T(c, top, cx, h - 22, 11, 'MB', INK, 'c')
        led(c, cx, h / 2 - 4, 12, lamp_col, on, True)
        T(c, bot, cx, 9, 7.6, 'SB', GREEN if on else MUTE, 'c')


def traffic(c, cx, cy, on):
    rr(c, cx - 19, cy - 45, 38, 90, 8, fill=H('#20242F'))
    for dy, nm, col in ((28, 'red', RED), (0, 'yellow', YELLOW), (-28, 'green', GREEN)):
        led(c, cx, cy + dy, 11, col, nm == on, False) if nm != on else led(c, cx, cy + dy, 11, col, True, True)


def d_traffic_row(c, w, h, states):
    n = len(states)
    cw = w / n
    housing = 90
    pad_top = 8
    label_h = 32
    cy = h - pad_top - housing / 2
    cap_y = cy - housing / 2 - 14
    sub_y = cap_y - 13
    for i, (on, cap, sub) in enumerate(states):
        cx = cw * i + cw / 2
        traffic(c, cx, cy, on)
        T(c, cap, cx, cap_y, 9.6, 'SB', INK, 'c')
        T(c, sub, cx, sub_y, 8, 'M', MUTE, 'c')
        if i < n - 1:
            arrow(c, cx + 22, cy, cx + cw - 22, cy, MUTE, 1.8, 6)


def d_button_inside(c, w, h):
    pw = w / 3
    # panel 1: top view
    ox = 0; cx = ox + pw / 2; cy = 84
    T(c, 'Кнопка сверху', cx, h - 14, 10.5, 'SB', GREEN, 'c')
    rr(c, cx - 30, cy - 30, 60, 60, 6, fill=H('#C9CFDB'), stroke=INK, lw=1.5); circ(c, cx, cy, 16, fill=H('#2B3245'))
    for (sx, sy, sel) in ((-1, 1, True), (-1, -1, False), (1, 1, False), (1, -1, True)):
        rr(c, cx + sx * 30 + (0 if sx > 0 else -15), cy + sy * 18 - 3, 15, 6, 1.5, fill=GREEN if sel else GRAYW, stroke=INK, lw=.8)
    line(c, cx - 22, cy - 18, cx - 22, cy + 18, BLUE, 2.6); line(c, cx + 22, cy - 18, cx + 22, cy + 18, BLUE, 2.6)
    T(c, 'зелёные ножки — наши', cx, cy + 44, 8.8, 'SB', GREEN, 'c')
    TW(c, 'Ножки с одной стороны всегда соединены (синие линии). Нажатие соединяет левую пару с правой.', cx, cy - 46, pw - 26, 8, 'S', MUTE, 'c')
    # panels 2, 3: side view
    for j, pressed in enumerate((False, True)):
        cx = pw * (j + 1) + pw / 2; y0 = 62
        T(c, 'Нажата' if pressed else 'Не нажата', cx, h - 14, 10.5, 'SB', RED if not pressed else GREEN, 'c')
        rr(c, cx - 50, y0, 100, 10, 2, fill=H('#C9CFDB'), stroke=INK, lw=1)
        for sx in (-1, 1):
            c.saveState(); c.setFillColor(H('#20242F')); c.rect(cx + sx * 34 - 2, y0 - 22, 4, 22, fill=1, stroke=0); c.restoreState()
            rr(c, cx + sx * 34 - 6, y0 + 10, 12, 14, 2, fill=H('#C77D3A'), stroke=INK, lw=.8)
        yb = y0 + (24 if pressed else 46)
        rr(c, cx - 44, yb, 88, 5, 2, fill=H('#9AA3B5'), stroke=INK, lw=.8)
        rr(c, cx - 22, yb + 5, 44, 22, 6, fill=H('#2B3245'))
        if pressed:
            arrow(c, cx, yb + 52, cx, yb + 32, RED, 2.2)
            poly(c, [(cx - 34, y0 - 22), (cx - 34, y0 + 26), (cx + 34, y0 + 26), (cx + 34, y0 - 22)], None, ORANGE, 2.6, False)
            TW(c, 'Цепь замкнута — ток идёт', cx, 24, pw - 20, 9, 'SB', GREEN, 'c')
        else:
            line(c, cx - 34, y0 - 22, cx - 34, y0 + 24, ORANGE, 2.6, (3, 2))
            TW(c, 'Между контактами зазор — тока нет', cx, 24, pw - 20, 9, 'SB', RED, 'c')
    T(c, 'ножка', pw + pw / 2 - 34, y0 - 32, 7.5, 'S', MUTE, 'c')


def d_pullup(c, w, h):
    pw = w / 2
    for j, pressed in enumerate((False, True)):
        ox = pw * j
        T(c, 'Кнопка нажата' if pressed else 'Кнопка НЕ нажата', ox + pw / 2, h - 12, 10.5, 'SB', GREEN if pressed else RED, 'c')
        c.saveState(); c.setStrokeColor(GRAYW); c.setLineWidth(1.2); c.setDash(4, 3); c.roundRect(ox + 8, 14, 124, h - 40, 8, fill=0, stroke=1); c.restoreState()
        T(c, 'внутри Arduino', ox + 70, h - 40, 7.6, 'S', MUTE, 'c')
        cxr = ox + 70; ytop = h - 62; ynode = 78
        T(c, '+5V', cxr, ytop + 6, 10, 'SB', RED, 'c')
        pts = [(cxr, ytop), (cxr, ytop - 8)]
        yy = ytop - 8
        for q in range(6): pts.append((cxr + (9 if q % 2 == 0 else -9), yy - 5 - q * 5))
        pts.append((cxr, yy - 36)); pts.append((cxr, ynode))
        poly(c, pts, None, INK, 1.8, False)
        T(c, 'пружинка', cxr + 16, ytop - 28, 7.6, 'S', MUTE)
        xs = ox + 196
        line(c, cxr, ynode, xs, ynode, INK, 1.8); circ(c, cxr, ynode, 3.3, fill=INK)
        T(c, 'пин 2', cxr + 8, ynode + 5, 8.6, 'SB', INK)
        line(c, xs, ynode, xs, 62, INK, 1.8); line(c, xs, 34, xs, 26, INK, 1.8)
        circ(c, xs, 62, 2.6, fill=INK); circ(c, xs, 36, 2.6, fill=INK)
        if pressed: line(c, xs, 62, xs, 36, INK, 2.2)
        else: line(c, xs, 62, xs + 14, 42, INK, 2.2)
        T(c, 'GND', xs, 15, 8.5, 'SB', INK, 'c')
        T(c, 'кнопка', xs + 20, 50, 7.8, 'S', MUTE)
        if pressed:
            poly(c, [(cxr, ytop), (cxr, ynode), (xs, ynode), (xs, 36)], None, ORANGE, 3, False)
            T(c, 'ток течёт вниз', xs - 8, ynode + 12, 7.8, 'SB', ORANGE, 'r')
        rr(c, ox + 14, 20, 112, 22, 5, fill=GREEN_L if pressed else RED_L, stroke=GREEN if pressed else RED, lw=1.3)
        T(c, 'пин 2 = LOW (0)' if pressed else 'пин 2 = HIGH (1)', ox + 70, 27, 9, 'MB', INK, 'c')


def d_bounce(c, w, h):
    pw = w / 2
    for j in range(2):
        ox = pw * j + 10; ww = pw - 30; yh = h - 50; yl = 34
        T(c, 'Как ты думаешь' if j == 0 else 'Как на самом деле', ox + ww / 2 + 10, h - 12, 10.5, 'SB', GREEN if j == 0 else RED, 'c')
        line(c, ox + 22, 20, ox + ww, 20, MUTE, 1.2); arrow(c, ox + ww - 10, 20, ox + ww, 20, MUTE, 1.2, 5)
        T(c, 'HIGH', ox + 18, yh - 3, 8, 'MB', MUTE, 'r'); T(c, 'LOW', ox + 18, yl - 3, 8, 'MB', MUTE, 'r')
        t0 = ox + 22 + ww * 0.34
        if j == 0: pts = [(ox + 22, yh), (t0, yh), (t0, yl), (ox + ww - 6, yl)]
        else:
            pts = [(ox + 22, yh), (t0, yh), (t0, yl)]; xx = t0
            for q in range(5):
                xx += 6; pts.append((xx, yh if q % 2 == 0 else yl)); xx += 0; pts.append((xx, yh if q % 2 == 0 else yl))
            xx += 6; pts += [(xx, yl), (ox + ww - 6, yl)]
        poly(c, pts, None, BLUE, 2.2, False)
        arrow(c, t0, 12, t0, 22, RED, 1.6, 5); T(c, 'нажал', t0 + 4, 5, 7.6, 'SB', RED)
        T(c, 'Arduino видит: 1 нажатие' if j == 0 else 'Arduino видит: несколько нажатий!', ox + ww / 2 + 10, h - 26, 8.6, 'S', MUTE, 'c')


def d_reaction(c, w, h):
    cw = 108; gap = (w - 4 * cw) / 3
    for i in range(4):
        x = i * (cw + gap); cx = x + cw / 2
        rr(c, x, 0, cw, h, 9, fill=white, stroke=LINEC, lw=1.4)
        circ(c, x + 13, h - 13, 9, fill=GREEN); T(c, str(i + 1), x + 13, h - 17, 10, 'SB', white, 'c')
        if i == 0: led(c, cx, h - 46, 13, YELLOW, False)
        elif i == 1: led(c, cx, h - 46, 13, YELLOW, True)
        elif i == 2: button_sym(c, cx, h - 46, 28, True)
        else:
            rr(c, cx - 30, h - 62, 60, 30, 4, fill=H('#0F1420')); T(c, '245', cx, h - 52, 13, 'MB', H('#7CFC9A'), 'c')
        heads = ['Ждём случайное время', 'Лампа загорелась!', 'Нажал — считаем', 'Показываем время']
        subs = ['random(2000, 6000)', 'start = millis()', 'millis() - start', 'Serial.println']
        TW(c, heads[i], cx, h - 82, cw - 12, 8.8, 'SB', INK, 'c', 10.5)
        T(c, subs[i], cx, 9, 6.6 if i in (0, 3) else 7.2, 'M', MUTE, 'c')
        if i < 3: arrow(c, x + cw + 2, h / 2, x + cw + gap - 2, h / 2, MUTE, 1.8, 6)


def d_cover(c, W, Hh):
    c.setFillColor(H('#0F2A3F')); c.rect(0, 0, W, Hh, fill=1, stroke=0)
    c.saveState()
    for i in range(14):
        c.setStrokeColor(H('#1D4560')); c.setLineWidth(1.4)
        y = 60 + i * 56; c.line(0, y, W, y)
    c.restoreState()
    c.saveState(); c.setFillColor(TEAL); c.setFillAlpha(.22); c.circle(W - 30, Hh - 120, 210, fill=1, stroke=0)
    c.setFillColor(YELLOW); c.setFillAlpha(.10); c.circle(60, 160, 170, fill=1, stroke=0); c.restoreState()
    T(c, 'УРОКИ ДЛЯ ЮНОГО ПРОГРАММИСТА', W / 2, Hh - 110, 11, 'SB', mix(TEAL, white, .55), 'c')
    T(c, 'Arduino', W / 2, Hh - 175, 62, 'SB', white, 'c')
    T(c, 'думает и чувствует', W / 2, Hh - 215, 25, 'SB', YELLOW, 'c')
    for i, (cl, nm) in enumerate(((BLUE, 'переменные'), (PURPLE, 'типы данных'), (ORANGE, 'if / else'), (GREEN, 'кнопка'))):
        x = W / 2 - 200 + i * 100
        rr(c, x, Hh - 262, 92, 26, 13, fill=cl); T(c, nm, x + 46, Hh - 253, 9.5, 'SB', white, 'c')
    # illustration: board + leds + button
    cx, cy = W / 2, Hh / 2 - 60
    rr(c, cx - 190, cy - 110, 380, 220, 18, fill=TEAL, stroke=H('#00686c'), lw=3)
    c.saveState(); c.setFillColor(H('#C9CFDB')); c.setStrokeColor(GRAYW); c.rect(cx - 210, cy + 30, 70, 62, fill=1, stroke=1); c.restoreState()
    c.saveState(); c.setFillColor(H('#20242F'))
    c.rect(cx - 100, cy - 30, 130, 36, fill=1, stroke=0); c.rect(cx - 160, cy + 92, 320, 12, fill=1, stroke=0); c.rect(cx - 130, cy - 106, 260, 12, fill=1, stroke=0); c.restoreState()
    T(c, 'ARDUINO UNO', cx + 20, cy - 60, 22, 'SB', white, 'c')
    for i, cl in enumerate((RED, YELLOW, GREEN)): led(c, cx - 90 + i * 60, cy + 56, 15, cl, True, True)
    button_sym(c, cx + 120, cy + 40, 44, True)
    T(c, 'Имя: ______________________', W / 2, 92, 15, 'S', white, 'c')
    T(c, 'Уровень:  ☆ ☆ ☆ ☆ ☆', W / 2, 62, 13, 'S', YELLOW, 'c')


def d_numline(c, w, h):
    rows = [('schet < 5', lambda n: n < 5), ('schet <= 5', lambda n: n <= 5)]
    x0 = 130; cw = (w - x0 - 6) / 9
    for r, (txt, fn) in enumerate(rows):
        y = h - 30 - r * 52
        T(c, txt, 2, y - 4, 11, 'MB', INK)
        for n in range(1, 10):
            cx = x0 + cw * (n - 0.5); ok = fn(n)
            circ(c, cx, y, 15, fill=GREEN if ok else H('#EEF0F5'), stroke=GREEN if ok else LINEC, lw=1.6)
            T(c, str(n), cx, y - 5, 12, 'MB', white if ok else MUTE, 'c')
    T(c, 'зелёные числа — там, где условие верно (ДА)', x0, 6, 8.5, 'S', MUTE)
