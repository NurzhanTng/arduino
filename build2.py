from lib import *
from diagrams import *
import os
import copy

BOOK_TITLE = 'Arduino: выпуск 2 — повторение'
OUT = 'arduino_uroki_2.pdf'
TOC_SLOTS = 1


def _cover(doc):
    c = doc.c
    d_cover(c, W_, H_)
    T(c, 'ВЫПУСК 2 · ПОВТОРЕНИЕ', W_ / 2, 130, 14, 'SB', YELLOW, 'c')
    c.bookmarkPage('p1')
    c.addOutlineEntry('Обложка', 'p1', 0, 0)
    c.showPage()
    doc.n = 1
    doc.registry.append({'n': 1, 'tag': 'ОБЛОЖКА', 'title': 'Обложка', 'dest': 'p1', 'level': 0})


def _toc_pages(doc, toc_from):
    if toc_from is None:
        doc.page('teal', 'СОДЕРЖАНИЕ', 'Содержание', [
            P('Сейчас собирается оглавление…'),
        ])
        return
    usable = [e for e in toc_from if e['tag'] not in ('ОБЛОЖКА', 'СОДЕРЖАНИЕ')]
    doc.page('teal', 'СОДЕРЖАНИЕ', 'Содержание', doc.toc_story(usable))


def _body():
    global doc, c
    c = doc.c

    for f in ('p6.py', 'p7.py', 'p8.py', 'p9.py', 'p10.py', 'p11.py', 'p12.py'):
        if os.path.exists(f):
            exec(open(f, encoding='utf-8').read(), globals())


def build_book(path, toc_from=None):
    global doc, c
    doc = Doc(path, BOOK_TITLE)
    c = doc.c
    _cover(doc)
    _toc_pages(doc, toc_from)
    _body()
    doc.save()
    return doc


if __name__ == '__main__':
    pass1 = os.path.join(os.path.dirname(os.path.abspath(__file__)) or '.', '_pass1_v2.pdf')
    print('--- pass 1 ---')
    d1 = build_book(pass1, None)
    print('--- pass 2 (final) ---')
    build_book(OUT, copy.deepcopy(d1.registry))
    try:
        os.remove(pass1)
    except OSError:
        pass
