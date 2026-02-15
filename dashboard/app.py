import streamlit as st

st.set_page_config(
    page_title="Budget Dashboard",
    layout="wide",
)

st.title("Budget Dashboard")
st.markdown("Select a page from the sidebar to view expense charts.")

st.header("📋 Spis treści")

st.markdown("""
### 📊 Category
Analiza wydatków w czasie według kategorii. Zawiera:
- **Całkowite miesięczne wydatki** - wykres wszystkich wydatków w wybranym okresie
- **Wydatki według kategorii** - szczegółowe wykresy dla każdej kategorii z średnią miesięczną

### 📈 Subcategory
Analiza wydatków w czasie według podkategorii. Zawiera:
- **Całkowite miesięczne wydatki dla kategorii** - wykres wydatków dla wybranej kategorii
- **Wydatki według podkategorii** - szczegółowe wykresy dla każdej podkategorii z średnią miesięczną

### 💰 Income vs Expenses
Porównanie przychodów i wydatków. Zawiera:
- **Bilans kumulacyjny** - wykres pokazujący skumulowany bilans finansowy
- **Przychody miesięczne** - wykres przychodów w poszczególnych miesiącach
- **Wydatki miesięczne** - wykres wydatków w poszczególnych miesiącach

### 📅 Month Details
Szczegółowa analiza wybranego miesiąca. Zawiera:
- **Szczegóły kategorii** - wykres wydatków/przychodów według kategorii z całkowitą sumą
- **Szczegóły podkategorii** - wykres wydatków/przychodów według podkategorii (po wyborze kategorii)
- **Szczegóły operacji** - tabela ze wszystkimi transakcjami w wybranym miesiącu
""")
