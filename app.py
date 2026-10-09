"""
Main Streamlit Application Entrypoint
AI-Assisted Bank Loan Analysis & Risk Intelligence Dashboard
"""

import pandas as pd
import numpy as np
import streamlit as st

from src.config import CLEANED_DATA_PATH, RAW_DATA_PATH
from src.data_processing.cleaner import clean_bank_loan_data
from src.ui.components import apply_custom_css
from src.ui.views.summary import render_summary_page
from src.ui.views.overview import render_overview_page
from src.ui.views.details import render_details_page
from src.ui.views.risk_intelligence import render_risk_intelligence_page

# Page Configuration
st.set_page_config(
    page_title="Bank Loan Risk Intelligence Dashboard",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Theme CSS
apply_custom_css()

@st.cache_data(show_spinner="Loading portfolio dataset...")
def load_data() -> pd.DataFrame:
    """Loads cleaned data CSV if available, else cleans raw dataset on the fly."""
    if CLEANED_DATA_PATH.exists():
        df = pd.read_csv(CLEANED_DATA_PATH, low_memory=False)
    else:
        df_raw = pd.read_csv(RAW_DATA_PATH, low_memory=False)
        df = clean_bank_loan_data(df_raw)
    return df

def main():
    # Load Data
    df_raw = load_data()

    # -------------------------------------------------------------------------
    # Sidebar Navigation & Global Filters
    # -------------------------------------------------------------------------
    st.sidebar.title("🏦 Bank Loan Portal")
    st.sidebar.caption("Risk Intelligence & Analytics")

    # Multi-page Navigation Selection
    page = st.sidebar.radio(
        "Navigation Pages:",
        [
            "📌 Executive Summary",
            "📈 Loan Overview",
            "📄 Detailed Loan Records",
            "🤖 Risk Intelligence"
        ]
    )

    st.sidebar.markdown("---")
    st.sidebar.subheader("🎯 Filter Controls")

    # Filter 1: State Filter
    all_states = sorted(list(df_raw["address_state"].dropna().unique())) if "address_state" in df_raw.columns else []
    selected_states = st.sidebar.multiselect(
        "US State:",
        options=all_states,
        default=[]
    )

    # Filter 2: Loan Status Filter
    all_statuses = sorted(list(df_raw["loan_status"].dropna().unique())) if "loan_status" in df_raw.columns else []
    selected_statuses = st.sidebar.multiselect(
        "Loan Status:",
        options=all_statuses,
        default=[]
    )

    # Filter 3: Risk Grade Filter
    all_grades = sorted(list(df_raw["grade"].dropna().unique())) if "grade" in df_raw.columns else []
    selected_grades = st.sidebar.multiselect(
        "Risk Grade:",
        options=all_grades,
        default=[]
    )

    # Filter 4: Loan Purpose Filter
    all_purposes = sorted(list(df_raw["purpose"].dropna().unique())) if "purpose" in df_raw.columns else []
    selected_purposes = st.sidebar.multiselect(
        "Loan Purpose:",
        options=all_purposes,
        default=[]
    )

    # Apply Filters to DataFrame
    df_filtered = df_raw.copy()

    if selected_states:
        df_filtered = df_filtered[df_filtered["address_state"].isin(selected_states)]
    if selected_statuses:
        df_filtered = df_filtered[df_filtered["loan_status"].isin(selected_statuses)]
    if selected_grades:
        df_filtered = df_filtered[df_filtered["grade"].isin(selected_grades)]
    if selected_purposes:
        df_filtered = df_filtered[df_filtered["purpose"].isin(selected_purposes)]

    st.sidebar.markdown("---")
    st.sidebar.info(f"📊 **Filtered Universe**: {len(df_filtered):,} of {len(df_raw):,} loans")

    # -------------------------------------------------------------------------
    # Multi-page Routing
    # -------------------------------------------------------------------------
    if page == "📌 Executive Summary":
        render_summary_page(df_filtered)
    elif page == "📈 Loan Overview":
        render_overview_page(df_filtered)
    elif page == "📄 Detailed Loan Records":
        render_details_page(df_filtered)
    elif page == "🤖 Risk Intelligence":
        render_risk_intelligence_page(df_filtered)

    # Footer
    st.markdown("---")
    st.caption("🔒 **AI-Assisted Bank Loan Analysis & Risk Intelligence System** | SQLite Database active | Zero Synthetic Data Policy Enforced")

if __name__ == "__main__":
    main()
