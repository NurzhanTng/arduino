# Arduino: уроки для юного программиста

PDF-книжка (выпуск 1) собирается из Python-скриптов на reportlab.

## Сборка

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python build.py
```

Результат: `arduino_uroki.pdf` рядом со скриптами.

### Шрифты DejaVu

Скрипт ищет TTF сначала в папке `fonts/` рядом с проектом, затем в системных каталогах (Debian/Fedora).

Если папка `fonts/` пуста, либо положи туда нужные файлы (`DejaVuSans*.ttf`, `DejaVuSansMono*.ttf`), либо установи системные пакеты:

```bash
# Fedora
sudo dnf install -y dejavu-sans-fonts dejavu-sans-mono-fonts

# Debian / Ubuntu
sudo apt install -y fonts-dejavu-core
```

Педагогика, дорожная карта и список материалов — в [docs/](docs/).
# arduino
