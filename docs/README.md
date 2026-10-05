# Документация серии занятий

Материалы для родителя и преподавателя. Ученику достаточно PDF-книжки.

Текущий репозиторий — **выпуск 1** (фаза 0→1 дорожной карты): переменные, типы, if/else, кнопка. Дальше планируется по одному выпуску на фазу.

## Оглавление

| Файл | О чём |
|------|--------|
| [pedagogika.md](pedagogika.md) | Принципы: боль → лекарство, «побудь Arduino», одна новая вещь |
| [ritm-zanyatiya.md](ritm-zanyatiya.md) | Ритм занятия 45–60 минут, карточки «лаборатория» |
| [roadmap.md](roadmap.md) | Фазы 0–6, разбивка комплекта, дорожка C++ |
| [materialy.md](materialy.md) | Список деталей комплекта (35 пунктов) |
| [proverka.md](proverka.md) | Что проверить до занятий, безопасность, библиотеки |
| [kniga-vypusk-1.md](kniga-vypusk-1.md) | Статус PDF-книжки: что готово, что ещё нет |

## Как собрать PDF

Из корня репозитория:

```bash
source .venv/bin/activate   # или: python3 -m venv .venv && pip install -r requirements.txt
python build.py
```

Получится `arduino_uroki.pdf`. Нужны reportlab и шрифты DejaVu (локальная папка `fonts/` или системные пакеты) — см. [README](../README.md) в корне.
