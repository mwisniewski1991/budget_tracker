import streamlit as st
import plotly.express as px
from filters import render_sidebar_filters
from db import run_query

st.set_page_config(page_title="Income vs Expenses", layout="wide")
st.title("Income vs Expenses")

filters = render_sidebar_filters(page="income_vs_expenses")

params = {
    "owner": filters["owner"],
    "date_from": filters["date_from"],
    "date_to": filters["date_to"],
    "fixed_variable": filters["fixed_variable"],
}

# --- Chart 1: Cumulative balance ---
st.header("Cumulative balance")

df_cumulative = run_query("income_vs_expenses/cumulative_monthly.sql", params)

if not df_cumulative.empty:
    fig = px.bar(
        df_cumulative,
        x="Rok miesiąc",
        y="Bilans kumulacyjny [PLN]",
        color_discrete_sequence=["#28A745"],
    )
    fig.update_layout(xaxis_type="category")
    st.plotly_chart(fig, use_container_width=True, key="cumulative_chart")
else:
    st.info("No data for selected date range.")

# --- Chart 2: Income monthly ---
st.header("Income monthly")

df_income = run_query("income_vs_expenses/income_monthly.sql", params)

if not df_income.empty:
    fig = px.bar(
        df_income,
        x="Rok miesiąc",
        y="Przychody [PLN]",
        color_discrete_sequence=["#28A745"],
    )
    fig.update_layout(
        xaxis_type="category",
        yaxis=dict(range=[0, 100000]),
    )
    st.plotly_chart(fig, use_container_width=True, key="income_chart")
else:
    st.info("No data for selected date range.")

# --- Chart 3: Expenses monthly (mirrored) ---
st.header("Expenses monthly")

df_expenses = run_query("income_vs_expenses/expenses_monthly.sql", params)

if not df_expenses.empty:
    fig = px.bar(
        df_expenses,
        x="Rok miesiąc",
        y="Wydatki [PLN]",
        color_discrete_sequence=["#DC3545"],
    )
    fig.update_layout(
        xaxis_type="category",
        yaxis=dict(range=[-100000, 0]),
    )
    st.plotly_chart(fig, use_container_width=True, key="expenses_chart")
else:
    st.info("No data for selected date range.")
