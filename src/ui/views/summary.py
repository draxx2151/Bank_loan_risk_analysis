"""
Executive Summary View Page
Displays top-level executive KPIs, MTD/PMTD MoM trends, and Good vs Bad loan portfolio standing.
"""

import pandas as pd
import streamlit as st
from src.analytics.kpi_engine import KPIEngine
from src.ui.components import (
    render_kpi_card,
    render_standing_card,
    format_currency,
    format_percentage
)

def render_summary_page(df: pd.DataFrame):
    st.title("🏦 Bank Loan Portfolio Executive Summary")
    st.markdown("High-level executive dashboard tracking total loan applications, funding, collections, and standing health.")
    st.markdown("---")

    if df is None or df.empty:
        st.warning("No loan data available.")
        return

    # Calculate Summary KPIs & MoM
    summary_kpis = KPIEngine.compute_summary_kpis(df)
    mtd_kpis = KPIEngine.compute_period_kpis(df, "2021-12")
    pmtd_kpis = KPIEngine.compute_period_kpis(df, "2021-11")
    mom_growth = KPIEngine.compute_mom_growth(mtd_kpis, pmtd_kpis)

    # 1. Top 5 KPI Cards Row
    c1, c2, c3, c4, c5 = st.columns(5)
    
    with c1:
        render_kpi_card(
            title="Total Applications",
            main_val=summary_kpis["total_applications"],
            mtd_val=mtd_kpis["applications"],
            mom_pct=mom_growth["applications_mom_pct"],
            is_currency=False
        )

    with c2:
        render_kpi_card(
            title="Total Funded Amount",
            main_val=summary_kpis["total_funded_amount"],
            mtd_val=mtd_kpis["funded_amount"],
            mom_pct=mom_growth["funded_amount_mom_pct"],
            is_currency=True
        )

    with c3:
        render_kpi_card(
            title="Total Received Amount",
            main_val=summary_kpis["total_amount_received"],
            mtd_val=mtd_kpis["amount_received"],
            mom_pct=mom_growth["amount_received_mom_pct"],
            is_currency=True
        )

    with c4:
        render_kpi_card(
            title="Avg Interest Rate",
            main_val=summary_kpis["avg_int_rate"],
            mtd_val=mtd_kpis["avg_int_rate"],
            mom_pct=mom_growth["avg_int_rate_mom_pct"],
            is_pct=True
        )

    with c5:
        render_kpi_card(
            title="Avg DTI Ratio",
            main_val=summary_kpis["avg_dti"],
            mtd_val=mtd_kpis["avg_dti"],
            mom_pct=mom_growth["avg_dti_mom_pct"],
            is_pct=True
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📊 Portfolio Standing Health (Good Standing vs Bad Standing)")

    # 2. Good vs Bad Standing Cards Row
    standing_kpis = KPIEngine.compute_good_vs_bad_kpis(df)
    good = standing_kpis["good_loans"]
    bad = standing_kpis["bad_loans"]

    col_good, col_bad = st.columns(2)
    with col_good:
        render_standing_card(
            title="Good Standing Loans (Fully Paid & Current)",
            count=good["count"],
            funded=good["funded_amount"],
            received=good["amount_received"],
            pct_apps=good["pct_applications"],
            is_good=True
        )

    with col_bad:
        render_standing_card(
            title="Bad Standing Loans (Charged Off)",
            count=bad["count"],
            funded=bad["funded_amount"],
            received=bad["amount_received"],
            pct_apps=bad["pct_applications"],
            is_good=False
        )

    # 3. Loan Status Summary Table Grid
    st.subheader("📋 Loan Status Portfolio Breakdown Grid")
    if "loan_status" in df.columns:
        status_grid = df.groupby("loan_status").agg(
            Applications=("id", "count"),
            Total_Funded=("loan_amount", "sum"),
            Total_Received=("total_payment", "sum"),
            Avg_Interest_Rate=("int_rate", "mean"),
            Avg_DTI=("dti", "mean")
        ).reset_index()

        status_grid["Total_Funded"] = status_grid["Total_Funded"].apply(format_currency)
        status_grid["Total_Received"] = status_grid["Total_Received"].apply(format_currency)
        status_grid["Avg_Interest_Rate"] = status_grid["Avg_Interest_Rate"].apply(format_percentage)
        status_grid["Avg_DTI"] = status_grid["Avg_DTI"].apply(format_percentage)

        st.dataframe(status_grid, use_container_width=True, hide_index=True)
