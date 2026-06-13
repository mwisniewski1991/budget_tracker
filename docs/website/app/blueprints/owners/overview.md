# Blueprint: owners

**URL:** `/owners`  
**Kod:** `website/app/blueprints/owners/`

Zarządzanie właścicielami (członkami gospodarstwa) i ich kontami finansowymi.

## Zawartość

| Element | Opis |
|---------|------|
| `owners.py` | Trasy CRUD: lista właścicieli, dodawanie/edycja właściciela, dodawanie/edycja konta przypisanego do właściciela. |
| `templates/owners/` | Widoki listy, formularzy edycji i podglądu właścicieli oraz kont. |

## Szablony

- `home.html.jinja` — lista właścicieli z linkami do edycji i kont.
- `owners_edit.html.jinja` / `owners_read.html.jinja` — edycja i podgląd właściciela.
- `account_edit.html.jinja` / `account_read.html.jinja` — edycja i podgląd konta.
