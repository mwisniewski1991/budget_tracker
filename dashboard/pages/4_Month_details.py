import streamlit as st
import plotly.express as px
from filters import render_sidebar_filters
from db import run_query

st.set_page_config(page_title="Month Details", layout="wide")
st.title("Month Details")

filters = render_sidebar_filters(page="month_details")

if filters is None:
    st.stop()

# Build params dict
params = {
    "owner": str(filters["owner"]) if filters["owner"] != -1 else "-1",
    "type_id": filters["type_id"],
    "year": filters["year"],
    "month": filters["month"],
    "category": filters["category"] if filters["category"] != "All" else "All",
    "subcategory": filters["subcategory"] if filters["subcategory"] != "All" else "All",
}

# Determine chart color based on type_id
chart_color = "#DC3545" if filters["type_id"] == 1 else "#28A745"  # Red for expenses, Green for income

# --- Section 1: Category Details and Category Sum ---
st.header("Category Details")

df_category_details = run_query("monthly_details/category_details.sql", params)
df_category_sum = run_query("monthly_details/category_sum.sql", params)
df_total_sum = run_query("monthly_details/total_sum.sql", params)

col_chart, col_metric = st.columns([4, 1])

with col_chart:
    if not df_category_details.empty:
        fig = px.bar(
            df_category_details,
            x="amount",
            y="category_name",
            orientation="h",
            color_discrete_sequence=[chart_color],
            opacity=0.75,
        )
        fig.update_layout(
            xaxis_title="Amount [PLN]",
            yaxis_title="Category",
            yaxis_type="category",
        )
        st.plotly_chart(fig, use_container_width=True, key="category_details_chart")
    else:
        st.info("No data for selected filters.")

with col_metric:
    if not df_total_sum.empty and df_total_sum.iloc[0, 0] is not None:
        total_sum = float(df_total_sum.iloc[0, 0])
        type_label = "Expenses" if filters["type_id"] == 1 else "Income"
        st.metric(f"Total {type_label}", f"{total_sum:,.2f} PLN")
    else:
        st.info("No data.")

# --- Section 3: Subcategories Details ---
if filters["category"] != "All":
    st.header("Subcategories Details")

    df_subcategory_details = run_query("monthly_details/subcategory_details.sql", params)

    col_chart, col_empty = st.columns([4, 1])

    with col_chart:
        if not df_subcategory_details.empty:
            # Aggregate by subcategory_name to sum all transactions per subcategory
            df_aggregated = df_subcategory_details.groupby("subcategory_name", as_index=False)["amount"].sum()
            # Sort by amount descending for better visualization
            df_aggregated = df_aggregated.sort_values("amount", ascending=True)
            
            fig = px.bar(
                df_aggregated,
                x="amount",
                y="subcategory_name",
                orientation="h",
                color_discrete_sequence=[chart_color],
                opacity=0.75,
            )
            fig.update_layout(
                xaxis_title="Amount [PLN]",
                yaxis_title="Subcategory",
                yaxis_type="category",
            )
            st.plotly_chart(fig, use_container_width=True, key="subcategory_details_chart")
        else:
            st.info("No data for selected filters.")
else:
    st.info("Select a specific category to view subcategory details.")

# --- Section 4: Operation Details ---
st.header("Operation Details")

df_operations = run_query("monthly_details/operations_table.sql", params)

if not df_operations.empty:
    # Format the dataframe for better display
    display_df = df_operations.copy()
    # Format amount column
    if "amount" in display_df.columns:
        display_df["amount"] = display_df["amount"].apply(lambda x: f"{float(x):,.2f}" if x is not None else "")
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
    )
else:
    st.info("No data for selected filters.")
