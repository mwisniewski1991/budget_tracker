import streamlit as st
import plotly.express as px
from filters import render_sidebar_filters, _load_subcategories
from db import run_query

st.set_page_config(page_title="Expenses - Subcategory", layout="wide")
st.title("In time expenses - Subcategory")

filters = render_sidebar_filters(page="subcategory")

if filters is None:
    st.stop()

# --- Section 1: All expenses for selected category (subcategory filter does NOT affect this) ---
st.header("Total monthly expenses for category")

params_all = {
    "owner": filters["owner"],
    "category": filters["category"],
    "date_from": filters["date_from"],
    "date_to": filters["date_to"],
    "fixed_variable": filters["fixed_variable"],
}

df_all_chart = run_query(
    "monthly_subcategories/monthly_subcategories_all_chart.sql", params_all
)
df_all_bullet = run_query(
    "monthly_subcategories/monthly_subcategories_all_bullet.sql", params_all
)

col_chart, col_metric = st.columns([4, 1])

with col_chart:
    if not df_all_chart.empty:
        fig = px.bar(
            df_all_chart,
            x="Rok miesiąc",
            y="Wydatki [PLN]",
            color_discrete_sequence=["#DC3545"],
        )
        fig.update_layout(xaxis_type="category")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data for selected date range.")

with col_metric:
    if not df_all_bullet.empty and df_all_bullet.iloc[0, 0] is not None:
        avg_val = float(df_all_bullet.iloc[0, 0])
        st.metric("Average monthly expenses", f"{avg_val:,.0f} PLN")

# --- Section 2: Per-subcategory charts ---
st.header("Expenses by subcategory")

if filters["subcategory"] == "-1":
    subcategories = _load_subcategories(filters["category"])
else:
    subcategories = [(filters["subcategory"], None)]

for sub_id, sub_display in subcategories:
    params_one = {
        "owner": filters["owner"],
        "category": filters["category"],
        "subcategory": sub_id,
        "date_from": filters["date_from"],
        "date_to": filters["date_to"],
        "fixed_variable": filters["fixed_variable"],
    }

    df_chart = run_query(
        "monthly_subcategories/monthly_subcategories_one_chart.sql", params_one
    )

    if df_chart.empty:
        continue

    chart_title = df_chart["Podkategoria"].iloc[0] if "Podkategoria" in df_chart.columns else sub_display
    st.subheader(chart_title)

    df_bullet = run_query(
        "monthly_subcategories/monthly_subcategories_one_bullet.sql", params_one
    )

    col_chart, col_metric = st.columns([4, 1])

    with col_chart:
        fig = px.bar(
            df_chart,
            x="Rok miesiąc",
            y="Wydatki [PLN]",
            color_discrete_sequence=["#DC3545"],
        )
        fig.update_layout(xaxis_type="category")
        st.plotly_chart(fig, use_container_width=True, key=f"sub_chart_{sub_id}")

    with col_metric:
        if not df_bullet.empty:
            avg_val = float(df_bullet["Średnia wartość wydatków [PLN]"].iloc[0])
            st.metric("Average monthly expenses", f"{avg_val:,.0f} PLN")
