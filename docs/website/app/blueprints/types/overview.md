# Blueprint: types

**URL:** `/type/<type_id>/category`  
**Kod:** `website/app/blueprints/types/`

Zarządzanie słownikiem kategorii i podkategorii. Osobne widoki dla wydatków (`type_id=1`) i dochodów (`type_id=2`).

## Zawartość

| Element | Opis |
|---------|------|
| `types.py` | Trasy CRUD kategorii i podkategorii w ramach danego typu transakcji. |
| `templates/types/` | Widoki listy, formularzy edycji i podglądu kategorii oraz podkategorii. |

## Szablony

- `home.html.jinja` — lista kategorii dla wybranego typu (dochód/wydatek).
- `category_edit.html.jinja` / `category_read.html.jinja` — edycja i podgląd kategorii.
- `subcategory_edit.html.jinja` / `subcategory_read.html.jinja` — edycja i podgląd podkategorii (w tym flaga kosztu stałego).
