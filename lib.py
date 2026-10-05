import math, re
from reportlab.pdfgen import canvas as cv
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, Color, white, black
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, Spacer, Flowable, Frame, Table, TableStyle, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER

import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_FONT_DIRS = (
    os.path.join(_HERE, 'fonts'),
    '/usr/share/fonts/truetype/dejavu/',
    '/usr/share/fonts/dejavu/',
    '/usr/share/fonts/dejavu-sans-fonts/',
    '/usr/share/fonts/dejavu-sans-mono-fonts/',
)
_FONT_FILES = [
    ('S', 'DejaVuSans.ttf'),
    ('SB', 'DejaVuSans-Bold.ttf'),
    ('SI', 'DejaVuSans-Oblique.ttf'),
    ('SBI', 'DejaVuSans-BoldOblique.ttf'),
    ('M', 'DejaVuSansMono.ttf'),
    ('MB', 'DejaVuSansMono-Bold.ttf'),
]


def _find_font(name):
    for d in _FONT_DIRS:
        path = os.path.join(d, name)
        if os.path.isfile(path):
            return path
    raise FileNotFoundError(
        f'Шрифт {name} не найден. Положи TTF в папку fonts/ рядом со скриптами '
        f'или установи системные DejaVu '
        f'(Fedora: dejavu-sans-fonts dejavu-sans-mono-fonts; '
        f'Debian/Ubuntu: fonts-dejavu-core). Искали в: {", ".join(_FONT_DIRS)}'
    )


for n, f in _FONT_FILES:
    pdfmetrics.registerFont(TTFont(n, _find_font(f)))
pdfmetrics.registerFontFamily('S', normal='S', bold='SB', italic='SI', boldItalic='SBI')
pdfmetrics.registerFontFamily('M', normal='M', bold='MB', italic='M', boldItalic='MB')

W_, H_ = A4
CW = 504
LM = (W_ - CW) / 2


def H(x): return HexColor(x)


def hx(c): return '#' + c.hexval()[2:]


INK = H('#1E2A44'); MUTE = H('#5B6784'); LINEC = H('#D5DAE6')
BLUE = H('#2F80ED'); BLUE_L = H('#E4EEFF')
PURPLE = H('#8E5CE6'); PURPLE_L = H('#F0E9FF')
ORANGE = H('#F2994A'); ORANGE_L = H('#FFF0DE')
GREEN = H('#27AE60'); GREEN_L = H('#DFF6E8')
RED = H('#EB5757'); RED_L = H('#FDE6E6')
YELLOW = H('#F2C94C'); YELLOW_L = H('#FFF8D9')
TEAL = H('#00979D'); TEAL_L = H('#DDF3F4')
CODEBG = H('#1F2430')
THEMES = {'teal': (TEAL, TEAL_L), 'blue': (BLUE, BLUE_L), 'purple': (PURPLE, PURPLE_L),
          'orange': (ORANGE, ORANGE_L), 'green': (GREEN, GREEN_L), 'red': (RED, RED_L),
          'ink': (H('#3B4A6B'), H('#E8ECF5'))}


def mix(a, b, t):
    return Color(a.red * (1 - t) + b.red * t, a.green * (1 - t) + b.green * t, a.blue * (1 - t) + b.blue * t)


# ---------- drawing primitives ----------
def rr(c, x, y, w, h, r=6, fill=None, stroke=None, lw=1):
    c.saveState()
    if fill is not None: c.setFillColor(fill)
    if stroke is not None: c.setStrokeColor(stroke); c.setLineWidth(lw)
    c.roundRect(x, y, w, h, r, fill=int(fill is not None), stroke=int(stroke is not None))
    c.restoreState()


def circ(c, x, y, r, fill=None, stroke=None, lw=1):
    c.saveState()
    if fill is not None: c.setFillColor(fill)
    if stroke is not None: c.setStrokeColor(stroke); c.setLineWidth(lw)
    c.circle(x, y, r, fill=int(fill is not None), stroke=int(stroke is not None))
    c.restoreState()


def line(c, x1, y1, x2, y2, color=INK, lw=1.5, dash=None):
    c.saveState(); c.setStrokeColor(color); c.setLineWidth(lw)
    if dash: c.setDash(*dash)
    c.line(x1, y1, x2, y2); c.restoreState()


def poly(c, pts, fill=None, stroke=None, lw=1, close=True):
    c.saveState()
    if fill is not None: c.setFillColor(fill)
    if stroke is not None: c.setStrokeColor(stroke); c.setLineWidth(lw)
    p = c.beginPath(); p.moveTo(*pts[0])
    for q in pts[1:]: p.lineTo(*q)
    if close: p.close()
    c.drawPath(p, fill=int(fill is not None), stroke=int(stroke is not None)); c.restoreState()


def arrow(c, x1, y1, x2, y2, color=INK, lw=1.6, hs=6.5):
    c.saveState(); c.setStrokeColor(color); c.setFillColor(color); c.setLineWidth(lw)
    a = math.atan2(y2 - y1, x2 - x1)
    c.line(x1, y1, x2 - hs * 0.8 * math.cos(a), y2 - hs * 0.8 * math.sin(a))
    p = c.beginPath(); p.moveTo(x2, y2)
    p.lineTo(x2 - hs * math.cos(a - 0.45), y2 - hs * math.sin(a - 0.45))
    p.lineTo(x2 - hs * math.cos(a + 0.45), y2 - hs * math.sin(a + 0.45)); p.close()
    c.drawPath(p, fill=1, stroke=0); c.restoreState()


def T(c, s, x, y, size=10, font='S', color=INK, al='l'):
    c.saveState(); c.setFillColor(color); c.setFont(font, size)
    if al == 'l': c.drawString(x, y, s)
    elif al == 'c': c.drawCentredString(x, y, s)
    else: c.drawRightString(x, y, s)
    c.restoreState()


def wrap(s, font, size, maxw):
    lines, cur = [], ''
    for w in s.split():
        t = (cur + ' ' + w).strip()
        if stringWidth(t, font, size) <= maxw: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines


def TW(c, s, x, y, maxw, size=9, font='S', color=INK, al='l', lead=None):
    lead = lead or size * 1.32
    for ln in wrap(s, font, size, maxw):
        T(c, ln, x, y, size, font, color, al); y -= lead
    return y


# ---------- flowables ----------
class Dia(Flowable):
    def __init__(self, w, h, fn, *a, **k):
        Flowable.__init__(self); self.w = w; self.h = h; self.fn = fn; self.a = a; self.k = k; self.hAlign = 'CENTER'

    def wrap(self, aw, ah): return self.w, self.h

    def draw(self): self.fn(self.canv, self.w, self.h, *self.a, **self.k)


TYPES = {'int', 'float', 'bool', 'String', 'void', 'unsigned', 'long', 'char', 'byte'}
CTRL = {'if', 'else', 'while', 'for', 'return', 'true', 'false'}
CONST = {'HIGH', 'LOW', 'OUTPUT', 'INPUT', 'INPUT_PULLUP', 'LED_BUILTIN', 'A0'}
C_TEXT = H('#E6E9F0'); C_GRAY = H('#7F8C9A'); C_STR = H('#A5E075'); C_NUM = H('#FFB86C')
C_TYPE = H('#C792EA'); C_KW = H('#FF7AB2'); C_CONST = H('#FFB86C'); C_FUN = H('#7DCFFF')
_tok = re.compile(r'(//.*$)|("[^"]*")|(\b\d+(?:\.\d+)?\b)|([A-Za-z_][A-Za-z_0-9]*)|(\s+)|(.)')


def tokens(ln):
    out = []
    for m in _tok.finditer(ln):
        s = m.group(0)
        if m.group(1): out.append((s, C_GRAY))
        elif m.group(2): out.append((s, C_STR))
        elif m.group(3): out.append((s, C_NUM))
        elif m.group(4):
            nxt = ln[m.end():m.end() + 1]
            if s in TYPES: col = C_TYPE
            elif s in CTRL: col = C_KW
            elif s in CONST: col = C_CONST
            elif nxt == '(' or s == 'Serial': col = C_FUN
            else: col = C_TEXT
            out.append((s, col))
        else: out.append((s, C_TEXT))
    return out


class Code(Flowable):
    def __init__(self, text, title=None, hl=(), size=9.4, width=None, nums=True):
        Flowable.__init__(self)
        self.lines = text.strip('\n').split('\n'); self.title = title; self.hl = set(hl)
        self.size = size; self.width = width; self.nums = nums; self.hAlign = 'CENTER'

    def wrap(self, aw, ah):
        self.w = self.width or aw
        self.lh = self.size * 1.42
        self.tb = 17 if self.title else 0
        self.h = len(self.lines) * self.lh + 14 + self.tb
        cw = stringWidth('0', 'M', self.size)
        x0 = 32 if self.nums else 12
        mx = max(len(l) for l in self.lines) * cw + x0 + 8
        if mx > self.w: print('!! code line too wide', round(mx), '>', round(self.w), self.lines[[len(l) for l in self.lines].index(max(len(l) for l in self.lines))])
        return self.w, self.h

    def draw(self):
        c = self.canv; w, h, tb = self.w, self.h, self.tb
        rr(c, 0, 0, w, h, 7, fill=CODEBG)
        if tb:
            rr(c, 0, h - tb, w, tb, 7, fill=H('#2E354A'))
            c.setFillColor(H('#2E354A')); c.rect(0, h - tb, w, 8, fill=1, stroke=0)
            for i, cl in enumerate([RED, YELLOW, GREEN]): circ(c, 11 + i * 12, h - tb / 2, 3.2, fill=cl)
            T(c, self.title, 54, h - tb / 2 - 3, 8.5, 'M', H('#AEB6C8'))
        x0 = 32 if self.nums else 12
        for i, ln in enumerate(self.lines):
            ytop = h - tb - 7 - i * self.lh
            if (i + 1) in self.hl:
                c.saveState(); c.setFillColor(YELLOW); c.setFillAlpha(0.20)
                c.rect(0, ytop - self.lh + 1, w, self.lh, fill=1, stroke=0); c.restoreState()
            yb = ytop - self.lh * 0.78
            if self.nums: T(c, str(i + 1), 22, yb, self.size - 1.2, 'M', H('#5E6880'), 'r')
            x = x0
            for s, col in tokens(ln):
                T(c, s, x, yb, self.size, 'M', col)
                x += stringWidth(s, 'M', self.size)


# ---------- text helpers ----------
def esc(s): return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def k(s, col='#C2185B'):
    return f'<font name="MB" color="{col}">{esc(s)}</font>'


BODY = ParagraphStyle('body', fontName='S', fontSize=11.2, leading=16.4, textColor=INK)
SMALL = ParagraphStyle('small', parent=BODY, fontSize=9.4, leading=13, textColor=MUTE)
CEN = ParagraphStyle('cen', parent=BODY, alignment=TA_CENTER)
CEN_S = ParagraphStyle('cens', parent=SMALL, alignment=TA_CENTER)


def P(t, st=BODY): return Paragraph(t, st)


def H2(t, col): return Paragraph(t, ParagraphStyle('h2', fontName='SB', fontSize=15, leading=19, textColor=col, spaceBefore=4, spaceAfter=5))


def SP(h=8): return Spacer(1, h)


def BUL(items, col, size=11.2):
    st = ParagraphStyle('bul', parent=BODY, fontSize=size, leading=size * 1.46, leftIndent=15, firstLineIndent=-15, spaceAfter=3)
    return [Paragraph(f'<font color="{hx(col)}"><b>●</b></font>&nbsp;&nbsp;' + t, st) for t in items]


KINDS = {'know': (BLUE, BLUE_L, 'Запомни'), 'warn': (RED, RED_L, 'Осторожно!'), 'try': (GREEN, GREEN_L, 'Попробуй сам'),
         'fun': (H('#C98A00'), YELLOW_L, 'Интересно'), 'idea': (PURPLE, PURPLE_L, 'Подсказка'), 'task': (ORANGE, ORANGE_L, 'Задание')}


def CALL(kind, body, title=None, width=CW):
    col, bg, t0 = KINDS[kind]; title = title or t0
    hs = ParagraphStyle('ct', fontName='SB', fontSize=11, leading=14, textColor=col, spaceAfter=2)
    bs = ParagraphStyle('cb', parent=BODY, fontSize=10.4, leading=14.8, spaceAfter=2)
    if isinstance(body, str): body = [body]
    cell = [Paragraph(title, hs)] + [Paragraph(x, bs) if isinstance(x, str) else x for x in body]
    t = Table([[cell]], colWidths=[width])
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), bg), ('LINEBEFORE', (0, 0), (0, -1), 4, col),
                           ('LEFTPADDING', (0, 0), (-1, -1), 12), ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                           ('TOPPADDING', (0, 0), (-1, -1), 7), ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                           ('ROUNDEDCORNERS', [6, 6, 6, 6])]))
    return t


def TB(rows, colw, col, light, head=True, size=10, first_bold=False, center_cols=(), pad=4.5):
    ps = ParagraphStyle('t', fontName='S', fontSize=size, leading=size * 1.32, textColor=INK)
    pc = ParagraphStyle('tc', parent=ps, alignment=TA_CENTER)
    hs = ParagraphStyle('th', parent=ps, fontName='SB', textColor=white)
    data = []
    for i, r in enumerate(rows):
        row = []
        for j, x in enumerate(r):
            if not isinstance(x, str): row.append(x); continue
            if head and i == 0: row.append(Paragraph(x, hs))
            else:
                if first_bold and j == 0: x = '<b>' + x + '</b>'
                row.append(Paragraph(x, pc if j in center_cols else ps))
        data.append(row)
    t = Table(data, colWidths=colw)
    st = [('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('GRID', (0, 0), (-1, -1), 0.6, LINEC),
          ('TOPPADDING', (0, 0), (-1, -1), pad), ('BOTTOMPADDING', (0, 0), (-1, -1), pad),
          ('LEFTPADDING', (0, 0), (-1, -1), 7), ('RIGHTPADDING', (0, 0), (-1, -1), 7),
          ('ROUNDEDCORNERS', [5, 5, 5, 5])]
    if head: st.append(('BACKGROUND', (0, 0), (-1, 0), col))
    for i in range(1 if head else 0, len(rows)):
        st.append(('BACKGROUND', (0, i), (-1, i), light if (i % 2 == (1 if head else 0)) else white))
    t.setStyle(TableStyle(st))
    return t


def SIDE(a, b, wa, wb, gap=0, valign='TOP'):
    t = Table([[a, b]], colWidths=[wa + gap, wb])
    t.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), valign), ('LEFTPADDING', (0, 0), (-1, -1), 0),
                           ('RIGHTPADDING', (0, 0), (0, 0), gap), ('RIGHTPADDING', (1, 0), (1, 0), 0),
                           ('TOPPADDING', (0, 0), (-1, -1), 0), ('BOTTOMPADDING', (0, 0), (-1, -1), 0)]))
    return t


# ---------- document ----------
TOC_DEST = 'toc'


def term_dest(key):
    return 'term_' + re.sub(r'[^A-Za-z0-9_]+', '_', key)


def term_link(key, text=None):
    """Clickable term → glossary entry (destination registered on glossary pages)."""
    label = text if text is not None else key
    return '<link href="%s"><font color="#2F80ED"><u>%s</u></font></link>' % (term_dest(key), label)


class Doc:
    def __init__(self, path, title):
        self.path = path
        self.c = cv.Canvas(path, pagesize=A4)
        self.c.setTitle(title)
        self.c.setAuthor('Arduino для юного программиста')
        self.n = 0
        self.registry = []
        self._outline_seen = set()
        self.terms = {}

    def register_term(self, key, definition):
        self.terms[key] = definition

    def page(self, theme, tag, title, story, num=None, term_keys=None):
        c = self.c
        col, lt = THEMES[theme]
        self.n += 1
        dest = 'p%d' % self.n
        level = 0 if tag not in self._outline_seen else 1
        self._outline_seen.add(tag)
        self.registry.append({'n': self.n, 'tag': tag, 'title': title, 'dest': dest, 'level': level})

        c.setFillColor(H('#FBFCFF')); c.rect(0, 0, W_, H_, fill=1, stroke=0)
        hh = 74
        c.setFillColor(col); c.rect(0, H_ - hh, W_, hh, fill=1, stroke=0)
        c.setFillColor(mix(col, black, 0.2)); c.rect(0, H_ - hh, W_, 5, fill=1, stroke=0)
        c.saveState(); c.setFillColor(white); c.setFillAlpha(0.13)
        c.circle(W_ - 30, H_ - 14, 62, fill=1, stroke=0); c.circle(W_ - 120, H_ - 72, 30, fill=1, stroke=0); c.restoreState()
        if num is not None:
            circ(c, LM + 22, H_ - hh / 2 + 2, 19, fill=white)
            T(c, str(num), LM + 22, H_ - hh / 2 - 5, 20, 'SB', col, 'c'); tx = LM + 54
        else:
            tx = LM
        T(c, tag, tx, H_ - 24, 9, 'SB', mix(col, white, 0.78))
        size = min(21, 372 / stringWidth(title, 'SB', 1))
        T(c, title, tx, H_ - 53, size, 'SB', white)
        for i, cl in enumerate([RED, YELLOW, GREEN]):
            circ(c, W_ - LM - 52 + i * 26, H_ - hh / 2 + 2, 8.5, fill=cl, stroke=white, lw=1.6)
        fr = Frame(LM, 40, CW, H_ - hh - 40 - 16, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        st = list(story); fr.addFromList(st, c)
        free = fr._y - fr._y1
        print(f'p{self.n:>2} {title[:34]:<34} free={free:6.1f}' + ('   <<< OVERFLOW %d' % len(st) if st else ''))
        line(c, LM, 32, LM + CW, 32, LINEC, 0.8)
        toc_label = '← Содержание'
        T(c, toc_label, LM, 19, 8, 'S', BLUE)
        tw = stringWidth(toc_label, 'S', 8)
        c.linkRect('', TOC_DEST, (LM, 14, LM + tw + 4, 30), relative=0)
        circ(c, LM + CW - 10, 21, 10, fill=col); T(c, str(self.n), LM + CW - 10, 18, 8.5, 'SB', white, 'c')
        c.bookmarkPage(dest)
        if tag == 'СОДЕРЖАНИЕ':
            c.bookmarkPage(TOC_DEST)
        for key in (term_keys or ()):
            c.bookmarkPage(term_dest(key))
        c.addOutlineEntry('%s — %s' % (tag, title) if level == 0 else title, dest, level, 0)
        c.showPage()

    def toc_story(self, entries):
        usable = [e for e in entries if e['tag'] not in ('ОБЛОЖКА', 'СОДЕРЖАНИЕ')]
        if not usable:
            return [P('Страницы появятся после сборки.')]
        ps = ParagraphStyle('toc', fontName='S', fontSize=8.2, leading=10.2, textColor=INK)
        mid = (len(usable) + 1) // 2
        cols = [usable[:mid], usable[mid:]]
        tables = []
        col_w = (CW - 12) / 2
        for chunk in cols:
            rows = []
            for e in chunk:
                cell = Paragraph(
                    '<font color="#5B6784" size="6.5">%s</font> '
                    '<link href="%s">%s</link> '
                    '<link href="%s"><font color="#2F80ED"><b>%d</b></font></link>'
                    % (e['tag'], e['dest'], e['title'], e['dest'], e['n']), ps)
                rows.append([cell])
            t = Table(rows, colWidths=[col_w])
            t.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('TOPPADDING', (0, 0), (-1, -1), 1.2),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 1.2),
                ('LINEBELOW', (0, 0), (-1, -2), 0.25, LINEC),
                ('LEFTPADDING', (0, 0), (-1, -1), 2),
                ('RIGHTPADDING', (0, 0), (-1, -1), 2),
            ]))
            tables.append(t)
        if len(tables) == 1:
            tables.append(SP(1))
        wrap = Table([[tables[0], tables[1]]], colWidths=[col_w, col_w])
        wrap.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (0, 0), 6),
            ('RIGHTPADDING', (1, 0), (1, 0), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]))
        return [
            P('Нажми название или номер. Внизу страниц — <b>← Содержание</b>.', SMALL),
            SP(4),
            wrap,
        ]

    def save(self):
        self.c.save()
