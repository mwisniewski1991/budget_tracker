import streamlit as st
from datetime import date
from dateutil.relativedelta import relativedelta
from abc import ABC, abstractmethod
from db import run_query


@st.cache_data(ttl=600)
def _load_owners():
    df = run_query("filter_options/owners.sql", {})
    return list(zip(df["id"].tolist(), df["name_pl"].tolist()))


@st.cache_data(ttl=600)
def _load_categories():
    df = run_query("filter_options/categories.sql", {})
    return list(zip(df["id"].tolist(), df["display_name"].tolist()))


@st.cache_data(ttl=600)
def _load_subcategories(category_id: str):
    df = run_query("filter_options/subcategories.sql", {"category_id": category_id})
    return list(zip(df["id"].tolist(), df["display_name"].tolist()))


@st.cache_data(ttl=600)
def _load_all_categories():
    df = run_query("filter_options/categories_all.sql", {})
    return list(zip(df["id"].tolist(), df["display_name"].tolist(), df["type_id"].tolist()))


@st.cache_data(ttl=600)
def _load_years():
    df = run_query("filter_options/years.sql", {})
    return df["year"].tolist()


class BaseFilterRenderer(ABC):
    """Base class for filter renderers."""
    
    def render_owner_filter(self, key: str = None):
        """Render owner filter."""
        st.subheader("Właściciel")
        owners = _load_owners()
        owner_options = [(-1, "Wszystkie")] + [(oid, name) for oid, name in owners]
        owner_idx = st.selectbox(
            "Właściciel",
            range(len(owner_options)),
            format_func=lambda i: owner_options[i][1],
            label_visibility="collapsed",
            key=key,
        )
        return owner_options[owner_idx][0]
    
    def render_date_range(self):
        """Render date range filter."""
        st.subheader("Zakres dat")
        default_to = date.today().replace(day=1) + relativedelta(months=1)
        default_from = default_to - relativedelta(months=12)
        
        date_from = st.date_input("Data od", value=default_from)
        date_to = st.date_input("Data do", value=default_to)
        return date_from, date_to
    
    def render_fixed_variable(self):
        """Render fixed/variable cost type filter."""
        st.subheader("Typ kosztu")
        fixed_variable = st.radio(
            "Stałe / Zmienne",
            options=["Wszystkie", "Tylko stałe", "Tylko zmienne"],
            index=0,
        )
        fixed_variable_mapping = {
            "Wszystkie": "All",
            "Tylko stałe": "Fixed only",
            "Tylko zmienne": "Variable only"
        }
        return fixed_variable_mapping.get(fixed_variable, fixed_variable)
    
    @abstractmethod
    def render_page_filters(self) -> dict:
        """Render page-specific filters. Must be implemented by subclasses."""
        pass
    
    def render(self) -> dict:
        """Main render method that renders all filters."""
        with st.sidebar:
            st.header("Filtry")
            return self.render_page_filters()


class CategoryFilterRenderer(BaseFilterRenderer):
    """Filter renderer for category page."""
    
    def render_page_filters(self) -> dict:
        date_from, date_to = self.render_date_range()
        owner = self.render_owner_filter()
        fixed_variable = self.render_fixed_variable()
        
        categories = _load_categories()
        st.subheader("Kategoria")
        cat_options = [("-1", "Wszystkie")] + [(cid, name) for cid, name in categories]
        cat_idx = st.selectbox(
            "Kategoria",
            range(len(cat_options)),
            format_func=lambda i: cat_options[i][1],
            label_visibility="collapsed",
        )
        category = cat_options[cat_idx][0]
        
        return {
            "date_from": date_from,
            "date_to": date_to,
            "fixed_variable": fixed_variable,
            "owner": owner,
            "category": category,
            "subcategory": None,
            "income_categories": None,
            "expense_categories": None,
        }


class SubcategoryFilterRenderer(BaseFilterRenderer):
    """Filter renderer for subcategory page."""
    
    def render_page_filters(self) -> dict:
        date_from, date_to = self.render_date_range()
        owner = self.render_owner_filter()
        fixed_variable = self.render_fixed_variable()
        
        categories = _load_categories()
        st.subheader("Kategoria")
        cat_options = [(cid, name) for cid, name in categories]
        if not cat_options:
            st.warning("Nie znaleziono kategorii.")
            return None
        
        cat_idx = st.selectbox(
            "Kategoria",
            range(len(cat_options)),
            format_func=lambda i: cat_options[i][1],
            label_visibility="collapsed",
        )
        category = cat_options[cat_idx][0]
        
        st.subheader("Podkategoria")
        subcategories = _load_subcategories(category)
        sub_options = [("-1", "Wszystkie")] + [(sid, name) for sid, name in subcategories]
        sub_idx = st.selectbox(
            "Podkategoria",
            range(len(sub_options)),
            format_func=lambda i: sub_options[i][1],
            label_visibility="collapsed",
        )
        subcategory = sub_options[sub_idx][0]
        
        return {
            "date_from": date_from,
            "date_to": date_to,
            "fixed_variable": fixed_variable,
            "owner": owner,
            "category": category,
            "subcategory": subcategory,
            "income_categories": None,
            "expense_categories": None,
        }


class IncomeVsExpensesFilterRenderer(BaseFilterRenderer):
    """Filter renderer for income vs expenses page."""
    
    def render_page_filters(self) -> dict:
        date_from, date_to = self.render_date_range()
        owner = self.render_owner_filter()
        fixed_variable = self.render_fixed_variable()
        
        all_categories = _load_all_categories()
        
        # Separate income and expense categories
        income_cat_options = [(cid, name) for cid, name, tid in all_categories if tid == 2]
        expense_cat_options = [(cid, name) for cid, name, tid in all_categories if tid == 1]
        
        # Income Categories
        st.subheader("Kategorie przychodów")
        income_default_selected = list(range(len(income_cat_options)))
        income_selected_indices = st.multiselect(
            "Kategorie przychodów",
            range(len(income_cat_options)),
            default=income_default_selected,
            format_func=lambda i: income_cat_options[i][1],
            label_visibility="collapsed",
        )
        income_categories = [income_cat_options[i][0] for i in income_selected_indices] if income_selected_indices else []
        
        # Expense Categories
        st.subheader("Kategorie wydatków")
        expense_default_selected = list(range(len(expense_cat_options)))
        expense_selected_indices = st.multiselect(
            "Kategorie wydatków",
            range(len(expense_cat_options)),
            default=expense_default_selected,
            format_func=lambda i: expense_cat_options[i][1],
            label_visibility="collapsed",
        )
        expense_categories = [expense_cat_options[i][0] for i in expense_selected_indices] if expense_selected_indices else []
        
        return {
            "date_from": date_from,
            "date_to": date_to,
            "fixed_variable": fixed_variable,
            "owner": owner,
            "category": None,
            "subcategory": None,
            "income_categories": income_categories,
            "expense_categories": expense_categories,
        }


class MonthDetailsFilterRenderer(BaseFilterRenderer):
    """Filter renderer for month details page."""
    
    def render_page_filters(self) -> dict:
        years = _load_years()
        current_year = date.today().year
        current_month = date.today().month
        
        st.subheader("Rok")
        if not years:
            st.warning("Nie znaleziono lat.")
            return None
        
        # Find current year index or default to first
        year_idx = 0
        if current_year in years:
            year_idx = years.index(current_year)
        year = st.selectbox(
            "Rok",
            range(len(years)),
            index=year_idx,
            format_func=lambda i: str(years[i]),
            label_visibility="collapsed",
        )
        year = str(years[year])
        
        st.subheader("Miesiąc")
        month_options = [(-1, "Wszystkie")] + [(i, str(i)) for i in range(1, 13)]
        month_idx = current_month  # Index in month_options (0=All, 1=Jan, 2=Feb, etc.)
        month = st.selectbox(
            "Miesiąc",
            range(len(month_options)),
            index=month_idx,
            format_func=lambda i: month_options[i][1],
            label_visibility="collapsed",
        )
        month = month_options[month][0]
        
        owner = self.render_owner_filter(key="month_details_owner")
        
        st.subheader("Przychody lub Wydatki")
        type_options = [(1, "Wydatki"), (2, "Przychody")]
        type_idx = st.selectbox(
            "Przychody lub Wydatki",
            range(len(type_options)),
            index=0,  # Default to Expenses
            format_func=lambda i: type_options[i][1],
            label_visibility="collapsed",
        )
        type_id = type_options[type_idx][0]
        
        st.subheader("Kategoria")
        all_categories = _load_all_categories()
        # Filter categories based on selected type_id
        if type_id == 1:  # Expenses
            cat_options_list = [(cid, name) for cid, name, tid in all_categories if tid == 1]
        else:  # Income
            cat_options_list = [(cid, name) for cid, name, tid in all_categories if tid == 2]
        
        cat_options = [("All", "Wszystkie")] + cat_options_list
        cat_idx = st.selectbox(
            "Kategoria",
            range(len(cat_options)),
            format_func=lambda i: cat_options[i][1],
            label_visibility="collapsed",
        )
        category = cat_options[cat_idx][0]
        
        st.subheader("Podkategoria")
        if category != "All":
            subcategories = _load_subcategories(category)
            sub_options = [("All", "Wszystkie")] + [(sid, name) for sid, name in subcategories]
        else:
            sub_options = [("All", "Wszystkie")]
        sub_idx = st.selectbox(
            "Podkategoria",
            range(len(sub_options)),
            format_func=lambda i: sub_options[i][1],
            label_visibility="collapsed",
        )
        subcategory = sub_options[sub_idx][0]
        
        return {
            "date_from": None,
            "date_to": None,
            "fixed_variable": None,
            "owner": owner,
            "category": category,
            "subcategory": subcategory,
            "income_categories": None,
            "expense_categories": None,
            "year": year,
            "month": month,
            "type_id": type_id,
        }


def render_sidebar_filters(page: str) -> dict:
    """
    Factory function that creates and renders the appropriate filter renderer.
    
    Args:
        page: Page identifier ("category", "subcategory", "income_vs_expenses", "month_details")
    
    Returns:
        Dictionary with filter values
    """
    renderers = {
        "category": CategoryFilterRenderer,
        "subcategory": SubcategoryFilterRenderer,
        "income_vs_expenses": IncomeVsExpensesFilterRenderer,
        "month_details": MonthDetailsFilterRenderer,
    }
    
    renderer_class = renderers.get(page)
    if renderer_class is None:
        raise ValueError(f"Unknown page: {page}. Available pages: {list(renderers.keys())}")
    
    renderer = renderer_class()
    return renderer.render()