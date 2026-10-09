"""
Detailed Loan Records View Page
Provides a searchable, filterable data grid with CSV export options.
"""

import pandas as pd
import streamlit as st
from src.ui.components import format_currency

def render_details_page(df: pd.DataFrame):
    st.title("📄 Detailed Loan Application Records")
    st.markdown("Search, filter, inspect, and export loan records from the underlying portfolio dataset.")
    st.markdown("---")

    if df is None or df.empty:
        st.warning("No loan records found.")
        return

    # 1. Search Box
    search_query = st.text_input("🔍 Quick Search (Search by ID, State, Purpose, Job Title):", "")
    
    filtered_df = df.copy()

    if search_query:
        q = search_query.strip().lower()
        mask = (
            filtered_df["id"].astype(str).str.lower().str.contains(q) |
            filtered_df["address_state"].astype(str).str.lower().str.contains(q) |
            filtered_df["purpose"].astype(str).str.lower().str.contains(q) |
            filtered_df["emp_title"].astype(str).str.lower().str.contains(q)
        )
        filtered_df = filtered_df[mask]

    # 2. Filtered Summary Metrics Row
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Displayed Records", f"{len(filtered_df):,}")
    with c2:
        funded_sum = filtered_df["loan_amount"].sum() if "loan_amount" in filtered_df.columns else 0.0
        st.metric("Total Funded Amount", format_currency(funded_sum))
    with c3:
        recv_sum = filtered_df["total_payment"].sum() if "total_payment" in filtered_df.columns else 0.0
        st.metric("Total Received Amount", format_currency(recv_sum))

    st.markdown("<br>", unsafe_allow_html=True)

    # 3. CSV Export Button
    csv_data = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Export Filtered Records to CSV",
        data=csv_data,
        file_name="bank_loan_records_filtered.csv",
        mime="text/csv",
        type="primary"
    )

    # 4. Display Columns & Data Grid
    display_cols = [
        "id", "issue_date", "address_state", "emp_length", "grade",
        "home_ownership", "loan_status", "purpose", "loan_amount",
        "int_rate", "dti", "annual_income", "total_payment"
    ]
    available_cols = [c for c in display_cols if c in filtered_df.columns]

    st.dataframe(
        filtered_df[available_cols],
        use_container_width=True,
        hide_index=True,
        height=500
    )
