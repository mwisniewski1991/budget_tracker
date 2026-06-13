# Modele bazodanowe

Dokumentacja modeli SQLAlchemy z pliku `website/app/models.py`.

Aplikacja śledzi dochody i wydatki gospodarstwa domowego. Dane transakcyjne są podzielone na nagłówek (`INCEXP_header`) i pozycje (`INCEXP_position`). Klasyfikacja odbywa się przez hierarchię kategoria → podkategoria, przypisana do typu transakcji (wydatek lub dochód).

## Owners

**Tabela:** `owners`

Osoby (członkowie gospodarstwa domowego), którym przypisuje się transakcje i konta finansowe. Pozwala filtrować i analizować finanse per osoba.

| Kolumna | Opis |
|---------|------|
| `id` | Identyfikator właściciela. Klucz główny, nadawany automatycznie. |
| `name_pl` | Imię lub nazwa właściciela wyświetlana w interfejsie (po polsku). |

**Relacje:** jeden właściciel może mieć wiele kont (`accounts`).

---

## Accounts

**Tabela:** `accounts`

Konta finansowe — np. konto bankowe, gotówka, karta. Każde konto należy do jednego właściciela. Transakcje rejestrują się zawsze w kontekście konkretnego konta.

| Kolumna | Opis |
|---------|------|
| `id` | Identyfikator konta. Dwucyfrowy kod tekstowy (np. `01`), generowany sekwencją `accounts_id_seq`. Klucz główny. |
| `name_pl` | Nazwa konta wyświetlana w interfejsie (po polsku), np. „Konto główne”, „Gotówka”. |
| `owner_id` | Powiązanie z właścicielem (`owners.id`). Określa, do kogo należy konto. |
| `is_active` | Czy konto jest aktywne. `1` — aktywne (domyślnie), `0` — nieaktywne; nieaktywne konta można ukryć z formularzy bez usuwania historii transakcji. |

---

## Type

**Tabela:** `type_dict`

Słownik typów transakcji. Rozróżnia wydatki od dochodów — fundamentalny podział w całej aplikacji i dashboardzie.

| Kolumna | Opis |
|---------|------|
| `id` | Identyfikator typu. Klucz główny. Wartości seedowane: `1` = Wydatek, `2` = Dochód. |
| `name_eng` | Nazwa typu po angielsku (np. „Expense”, „Income”). |
| `name_pl` | Nazwa typu po polsku (np. „Wydatek”, „Dochód”). Używana w UI. |

---

## Category

**Tabela:** `category`

Główne kategorie klasyfikacji transakcji — np. „Spożywcze”, Aktywa”. Każda kategoria należy do jednego typu (wydatek lub dochód).

| Kolumna | Opis |
|---------|------|
| `id` | Identyfikator kategorii. Dwucyfrowy kod tekstowy, generowany sekwencją `category_id_seq`. Klucz główny. |
| `name_pl` | Nazwa kategorii po polsku. |
| `type_id` | Powiązanie z typem transakcji (`type_dict.id`). Określa, czy kategoria dotyczy wydatków (`1`) czy dochodów (`2`). |

**Relacje:** jedna kategoria może mieć wiele podkategorii (`subcategories`).

---

## Subategory

**Tabela:** `subcategory`

Podkategorie — szczegółowa klasyfikacja w ramach kategorii głównej, np dla kategorii 

    - "Spożywcze" podkategorie:
        - "Jedzenie w domu", 
        - "W pracy"

    - "Aktywa":
        - "Odzież"
        - "Elektronika"

> **Uwaga:** nazwa klasy w kodzie to `Subategory` (literówka względem „Subcategory”).

| Kolumna | Opis |
|---------|------|
| `id` | Identyfikator podkategorii. Czterocyfrowy kod tekstowy, generowany sekwencją `subcategory_id_seq`. Klucz główny. |
| `name_pl` | Nazwa podkategorii po polsku. |
| `category_id` | Powiązanie z kategorią nadrzędną (`category.id`). |
| `is_fixed_cost` | Flaga kosztu stałego. `1` = koszt stały (np. czynsz, abonament), `0` = koszt zmienny (domyślnie). Używana w filtrach dashboardu do analizy stałych vs zmiennych wydatków. |

---

## INCEXP_header

**Tabela:** `incexp_header`

Nagłówek transakcji (Income/Expense header). Zbiera wspólne metadane dla jednego zdarzenia finansowego: data, źródło, typ, właściciel i konto. Jedna transakcja może składać się z wielu pozycji (np. zakupy w kilku kategoriach w ramach jednego paragonu).

| Kolumna | Opis |
|---------|------|
| `id` | Identyfikator nagłówka. Klucz główny, nadawany automatycznie. |
| `date` | Data transakcji — kiedy wydatkek/dochód faktycznie wystąpił. |
| `source` | Źródło transakcji — np. nazwa sklepu, pracodawcy, opis przelewu. Pole tekstowe, opcjonalne; służy też do wyszukiwania i filtrowania. |
| `type_id` | Typ transakcji (`type_dict.id`): wydatek (`1`) lub dochód (`2`). |
| `owner_id` | Właściciel transakcji (`owners.id`) — czyja to operacja finansowa. |
| `account_id` | Konto, na którym zarejestrowano transakcję (`accounts.id`). |
| `created_at_cet` | Znacznik czasu utworzenia rekordu w strefie CET. Ustawiany automatycznie przy INSERT. |
| `created_at_utc` | Znacznik czasu utworzenia rekordu w UTC. Ustawiany automatycznie przy INSERT. |
| `updated_at_cet` | Znacznik czasu ostatniej modyfikacji w strefie CET. |
| `updated_at_utc` | Znacznik czasu ostatniej modyfikacji w UTC. |

**Relacje:** nagłówek ma wiele pozycji (`incexp_positions`) oraz relację do `Type`.

---

## INCEXP_position

**Tabela:** `incexp_position`

Pozycja transakcji (Income/Expense position). Szczegółowy wpis kwotowy przypisany do nagłówka — kategoria, podkategoria, kwota i ewentualne notatki. Klucz główny jest złożony: `(header_id, position_id)`.

| Kolumna | Opis |
|---------|------|
| `header_id` | Powiązanie z nagłówkiem transakcji (`incexp_header.id`). Część klucza głównego. |
| `position_id` | Numer pozycji w ramach danego nagłówka (1, 2, 3…). Część klucza głównego; pozwala na wiele linii w jednej transakcji. |
| `category_id` | Kategoria główna (`category.id`). |
| `subcategory_id` | Podkategoria (`subcategory.id`). |
| `amount` | Kwota transakcji. Dla wydatków zwykle ujemna, dla dochodów dodatnia; dashboard operuje na wartości bezwzględnej z uwzględnieniem typu. |
| `amount_absolute` | Wartość bezwzględna `amount` — kolumna obliczana (`abs(amount)`). Ułatwia agregacje bez ręcznego uwzględniania znaku. |
| `amount_full` | Kwota w najmniejszej jednostce waluty (grosze) — kolumna obliczana (`amount * 100`). Przydatna do operacji całkowitoliczbowych bez błędów zaokrągleń. |
| `comment` | Dowolny komentarz do pozycji — np. notatka wyjaśniająca nietypowy wydatek. |
| `connection` | Powiązanie z inną transakcją lub zdarzeniem — np. identyfikator przelewu między kontami, referencja do powiązanego wpisu. Używane do łączenia logicznie powiązanych operacji. |
| `created_at_cet` | Znacznik czasu utworzenia rekordu w strefie CET. |
| `created_at_utc` | Znacznik czasu utworzenia rekordu w UTC. |
| `updated_at_cet` | Znacznik czasu ostatniej modyfikacji w strefie CET. |
| `updated_at_utc` | Znacznik czasu ostatniej modyfikacji w UTC. |

**Relacje:** pozycja należy do jednego nagłówka oraz ma relacje do `Category` i `Subategory`.

---

## Schematy serializacji (Marshmallow)

W tym samym pliku zdefiniowane są schematy Marshmallow do eksportu/importu JSON przez API — nie są to tabele bazodanowe:

- `AccountsSchema` — serializacja kont
- `OwnersSchema` — serializacja właścicieli wraz z zagnieżdżonymi kontami
- `TypesSchema` — serializacja typów transakcji
- `CategorySchema` — serializacja kategorii
- `SubcategorySchema` — serializacja podkategorii
