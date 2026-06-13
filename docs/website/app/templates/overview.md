# Szablony globalne (`website/app/templates`)

Wspólne szablony Jinja2 używane przez całą aplikację Flask. Blueprinty mają własne szablony w podfolderach `templates/` — ten katalog obejmuje tylko warstwę wspólną.

## Pliki

| Plik | Opis |
|------|------|
| `base.html` | Główny layout aplikacji. Zawiera nagłówek, nawigację (Pozycje, Bilans kont, Właściciele, Kategorie, Import CSV), Bootstrap 5, HTMX oraz blok `{% block content %}` dla treści stron. Większość widoków rozszerza ten szablon. |
| `home.html` | Strona główna aplikacji (legacy). Obecnie `/` przekierowuje na `/incexp`. |
| `about_me.html` | Statyczna strona informacyjna o aplikacji / autorze. |

## Konwencja

Szablony blueprintów dziedziczą z `base.html` i nadpisują blok `content`. Logika prezentacji specyficzna dla modułu (formularze transakcji, listy kategorii itd.) znajduje się w `website/app/blueprints/*/templates/`.
