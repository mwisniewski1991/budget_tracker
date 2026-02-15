import streamlit as st
from datetime import date
from dateutil.relativedelta import relativedelta
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


def render_sidebar_filters(page: str) -> dict:
    """
    Render sidebar filters and return selected values.

    page: "category" or "subcategory"
    """
    with st.sidebar:
        st.header("Filters")

        # --- Global filters ---
        st.subheader("Date range")
        default_to = date.today().replace(day=1) + relativedelta(months=1)
        default_from = default_to - relativedelta(months=12)

        date_from = st.date_input("Date from", value=default_from)
        date_to = st.date_input("Date to", value=default_to)

        st.subheader("Owner")
        owners = _load_owners()
        owner_options = [(-1, "All")] + [(oid, name) for oid, name in owners]
        owner_idx = st.selectbox(
            "Owner",
            range(len(owner_options)),
            format_func=lambda i: owner_options[i][1],
            label_visibility="collapsed",
        )
        owner = owner_options[owner_idx][0]

        st.subheader("Cost type")
        fixed_variable = st.radio(
            "Fixed / Variable",
            options=["All", "Fixed only", "Variable only"],
            index=0,
        )

        # --- Page filters ---
        category = None
        subcategory = None

        if page == "income_vs_expenses":
            pass

        elif page == "category":
            categories = _load_categories()
            st.subheader("Category")
            cat_options = [("-1", "All")] + [(cid, name) for cid, name in categories]
            cat_idx = st.selectbox(
                "Category",
                range(len(cat_options)),
                format_func=lambda i: cat_options[i][1],
                label_visibility="collapsed",
            )
            category = cat_options[cat_idx][0]
            subcategory = None

        elif page == "subcategory":
            categories = _load_categories()
            st.subheader("Category")
            cat_options = [(cid, name) for cid, name in categories]
            if not cat_options:
                st.warning("No categories found.")
                return None
            cat_idx = st.selectbox(
                "Category",
                range(len(cat_options)),
                format_func=lambda i: cat_options[i][1],
                label_visibility="collapsed",
            )
            category = cat_options[cat_idx][0]

            st.subheader("Subcategory")
            subcategories = _load_subcategories(category)
            sub_options = [("-1", "All")] + [(sid, name) for sid, name in subcategories]
            sub_idx = st.selectbox(
                "Subcategory",
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
    }
