# Blueprint: bulk_import

**URL:** `/bulk-import`  
**Kod:** `website/app/blueprints/bulk_import/`

Import wielu transakcji naraz z pliku CSV — z etapem podglądu przed zapisem do bazy.

## Zawartość

| Element | Opis |
|---------|------|
| `bulk_import.py` | Trasy: formularz uploadu, podgląd sparsowanych danych, zapis transakcji do bazy. |
| `utils/parsers.py` | Parsery CSV — mapowanie wierszy pliku na strukturę nagłówka i pozycji transakcji. |
| `templates/bulk_import/` | Formularz importu i widok podglądu z możliwością korekty przed zatwierdzeniem. |

## Szablony

- `home.html.jinja` — wybór konta i upload pliku CSV.
- `preview.html.jinja` — podgląd zaimportowanych wierszy z formularzem zatwierdzenia.
- `utils/incexp_position_render_catsub_preview.html.jinja` — fragment wyboru kategorii/podkategorii w podglądzie.
