# Blueprinty (`website/app/blueprints`)

Moduły funkcjonalne aplikacji Flask. Każdy blueprint to osobny pakiet z własnymi trasami, szablonami i — tam gdzie potrzeba — formularzami oraz narzędziami pomocniczymi. Rejestracja blueprintów odbywa się w `website/app/__init__.py`.

## Struktura typowego blueprintu

```
blueprints/<nazwa>/
├── <nazwa>.py          # trasy i logika widoków
├── forms.py            # opcjonalnie — formularze WTForms
├── utils/              # opcjonalnie — funkcje pomocnicze
├── constants.py        # opcjonalnie — stałe modułu
└── templates/<nazwa>/  # szablony Jinja2 modułu
```

## Moduły

| Blueprint | URL | Opis |
|-----------|-----|------|
| [incexp](incexp/overview.md) | `/incexp` | Główny moduł — przeglądanie, dodawanie, edycja i usuwanie transakcji (dochodów i wydatków). |
| [accounts_results](accounts_results/overview.md) | `/accounts-results` | Podsumowanie sald per właściciel i konto. |
| [owners](owners/overview.md) | `/owners` | CRUD właścicieli i przypisanych do nich kont finansowych. |
| [types](types/overview.md) | `/type/<type_id>/category` | CRUD kategorii i podkategorii dla wydatków (`1`) i dochodów (`2`). |
| [bulk_import](bulk_import/overview.md) | `/bulk-import` | Import transakcji z pliku CSV z podglądem przed zapisem. |

## Trasy poza blueprintami

Główny blueprint `views` (`website/app/views.py`, prefix `/`) obsługuje przekierowanie ze strony głównej oraz REST API (`/api/v1/...`) do odczytu i modyfikacji danych słownikowych i transakcji.
