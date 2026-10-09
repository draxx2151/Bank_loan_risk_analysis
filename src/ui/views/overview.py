"""
Loan Overview View Page
Provides interactive breakdown tabs for monthly trends, regional US geography,
loan purpose, risk grades, and terms.
"""

import pandas as pd
import streamlit as st
from src.ui.components import (
    create_monthly_trends_chart,
    create_state_map_chart,
    create_purpose_chart,
    create_grade_chart,
    create_term_donut_chart
)

def render_overview_page(df: pd.DataFrame):
    st.title("📈 Loan Portfolio Analytical Overview")
    st.markdown("Explore multi-dimensional distributions across time, geography, risk grades, loan terms, and borrower demographics.")
    st.markdown("---")

    if df is None or df.empty:
        st.warning("No loan data available for current filter selection.")
        return

    tab1, tab2, tab3, tab4 = st.tabs([
        "📅 Monthly Trends",
        "🗺️ Regional Geography",
        "🎯 Purpose & Demographics",
        "🏷️ Grade & Term Ratios"
    ])

    # Tab 1: Monthly Trends
    with tab1:
        st.subheader("Monthly Issue Date Trends")
        if "issue_date" in df.columns:
            df_temp = df.copy()
            df_temp["issue_month"] = pd.to_datetime(df_temp["issue_date"], errors="coerce").dt.strftime("%Y-%m")
            monthly_agg = df_temp.groupby("issue_month").agg(
                total_loan_applications=("id", "count"),
                total_funded_amount=("loan_amount", "sum"),
                total_amount_received=("total_payment", "sum")
            ).reset_index().sort_values("issue_month")

            fig_monthly = create_monthly_trends_chart(monthly_agg)
            st.plotly_chart(fig_monthly, use_container_width=True)

    # Tab 2: Regional Geography
    with tab2:
        st.subheader("US Regional Application Distribution")
        if "address_state" in df.columns:
            state_agg = df.groupby("address_state").agg(
                total_loan_applications=("id", "count"),
                total_funded_amount=("loan_amount", "sum")
            ).reset_index()
            if "States" in df.columns:
                state_names = df.groupby("address_state")["States"].first().reset_index()
                state_agg = state_agg.merge(state_names, on="address_state", how="left")
                state_agg["state_name"] = state_agg["States"].fillna(state_agg["address_state"])

            fig_state = create_state_map_chart(state_agg)
            st.plotly_chart(fig_state, use_container_width=True)

    # Tab 3: Loan Purpose & Demographics
    with tab3:
        st.subheader("Loan Applications by Stated Purpose & Employment Length")
        c1, c2 = st.columns(2)
        with c1:
            if "purpose" in df.columns:
                purpose_agg = df.groupby("purpose").agg(
                    total_loan_applications=("id", "count")
                ).reset_index()
                fig_purpose = create_purpose_chart(purpose_agg)
                st.plotly_chart(fig_purpose, use_container_width=True)

        with c2:
            if "emp_length" in df.columns:
                emp_agg = df.groupby("emp_length").agg(
                    total_loan_applications=("id", "count")
                ).reset_index()
                st.write("**Applications by Employment Length**")
                st.bar_chart(emp_agg.set_index("emp_length")["total_loan_applications"])

    # Tab 4: Risk Grade & Term Ratios
    with tab4:
        st.subheader("Risk Grade & Loan Term Ratios")
        c1, c2 = st.columns(2)
        with c1:
            if "grade" in df.columns:
                grade_agg = df.groupby("grade").agg(
                    total_loan_applications=("id", "count")
                ).reset_index().sort_values("grade")
                fig_grade = create_grade_chart(grade_agg)
                st.plotly_chart(fig_grade, use_container_width=True)

        with c2:
            if "term" in df.columns:
                term_agg = df.groupby("term").agg(
                    total_loan_applications=("id", "count")
                ).reset_index()
                fig_term = create_term_donut_chart(term_agg)
                st.plotly_chart(fig_term, use_container_width=True)
