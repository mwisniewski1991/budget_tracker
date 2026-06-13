# Blueprint: accounts_results

**URL:** `/accounts-results`  
**Kod:** `website/app/blueprints/accounts_results/`

Podgląd zbiorczy stanu kont — suma transakcji per właściciel i konto wraz z datą ostatniej aktualizacji.

## Zawartość

| Element | Opis |
|---------|------|
| `accounts_results.py` | Jedna trasa GET agregująca kwoty z `incexp_header` i `incexp_position`, grupując wynik po właścicielu i koncie. |
| `templates/accounts_results/` | Widok tabelaryczny wyników. |

## Szablony

- `home.html.jinja` — lista właścicieli z zagnieżdżonymi kontami, saldem i datą ostatniej zmiany.
