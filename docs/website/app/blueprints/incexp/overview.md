# Blueprint: incexp

**URL:** `/incexp`  
**Kod:** `website/app/blueprints/incexp/`

Rdzeń aplikacji — obsługa transakcji finansowych (Income/Expense). Użytkownik tu przegląda istniejące wpisy, filtruje je i dodaje nowe lub edytuje istniejące.

## Zawartość

| Element | Opis |
|---------|------|
| `incexp.py` | Trasy: lista transakcji, tworzenie, edycja, usuwanie; endpointy HTMX do kategorii/podkategorii. |
| `forms.py` | Formularze WTForms nagłówka i pozycji transakcji. |
| `utils.py` | Zapytania, szyfrowanie par owner-account, logika zapisu i modyfikacji transakcji. |
| `constants.py` | Stałe modułu (np. domyślny wybór, ID typów wydatku/dochodu). |
| `templates/incexp/` | Widoki: strona główna z filtrami, formularz nowej transakcji, edycja, fragmenty pozycji (HTMX). |

## Szablony

- `home.html.jinja` — lista transakcji z filtrami (właściciel/konto, typ, kategoria, kwota, źródło, powiązanie).
- `utils/new_incexp.html.jinja` — formularz dodawania transakcji.
- `utils/edit_incexp/` — edycja istniejącej transakcji.
- `utils/existing_incexp/` — fragment listy istniejących wpisów (HTMX).
- `utils/incexp_position*.html.jinja` — komponenty pozycji transakcji (kategoria, podkategoria, kwota, komentarz).
