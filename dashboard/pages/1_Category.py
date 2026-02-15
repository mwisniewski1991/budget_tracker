import streamlit as st
import plotly.express as px
from filters import render_sidebar_filters, _load_categories
from db import run_query

st.set_page_config(page_title="Expenses - Category", layout="wide")
st.title("In time expenses - Category")

filters = render_sidebar_filters(page="category")

# --- Section 1: All expenses monthly (owner/category filters do NOT affect this) ---
st.header("Total monthly expenses")

params_all = {
    "owner": -1,
    "date_from": filters["date_from"],
    "date_to": filters["date_to"],
    "fixed_variable": filters["fixed_variable"],
}

df_all_chart = run_query(
    "monthly_categories/monthly_categories_all_chart.sql", params_all
)
df_all_bullet = run_query(
    "monthly_categories/monthly_categories_all_bullet.sql", params_all
)

col_chart, col_metric = st.columns([4, 1])

with col_chart:
    if not df_all_chart.empty:
        fig = px.bar(
            df_all_chart,
            x="Rok miesiąc",
            y="Wydatki [PLN]",
        )
        fig.update_layout(xaxis_type="category")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data for selected date range.")

with col_metric:
    if not df_all_bullet.empty and df_all_bullet.iloc[0, 0] is not None:
        avg_val = float(df_all_bullet.iloc[0, 0])
        st.metric("Average monthly expenses", f"{avg_val:,.0f} PLN")

# --- Section 2: Per-category charts ---
st.header("Expenses by category")

if filters["category"] == "-1":
    categories = _load_categories()
else:
    categories = [(filters["category"], None)]

for cat_id, cat_display in categories:
    params_one = {
        "owner": filters["owner"],
        "category": cat_id,
        "date_from": filters["date_from"],
        "date_to": filters["date_to"],
        "fixed_variable": filters["fixed_variable"],
    }

    df_chart = run_query(
        "monthly_categories/monthly_categories_one_chart.sql", params_one
    )

    if df_chart.empty:
        continue

    chart_title = df_chart["Kategoria"].iloc[0] if "Kategoria" in df_chart.columns else cat_display
    st.subheader(chart_title)

    df_bullet = run_query(
        "monthly_categories/monthly_categories_one_bullet.sql", params_one
    )

    col_chart, col_metric = st.columns([4, 1])

    with col_chart:
        fig = px.bar(
            df_chart,
            x="Rok miesiąc",
            y="Wydatki [PLN]",
        )
        fig.update_layout(xaxis_type="category")
        st.plotly_chart(fig, use_container_width=True, key=f"cat_chart_{cat_id}")

    with col_metric:
        if not df_bullet.empty:
            avg_val = float(df_bullet["Średnia wartość wydatków [PLN]"].iloc[0])
            st.metric("Average monthly expenses", f"{avg_val:,.0f} PLN")
