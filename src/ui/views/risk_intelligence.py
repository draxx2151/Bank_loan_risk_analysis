"""
Risk Intelligence View Page
Provides an interactive AI Credit Risk Simulator and Underwriting Assessment Tool.
"""

import pandas as pd
import streamlit as st
from src.ml.risk_scoring import CreditRiskScoringEngine
from src.ui.components import create_risk_gauge_chart

@st.cache_resource
def get_scoring_engine():
    """Caches loaded ML CreditRiskScoringEngine instance."""
    try:
        return CreditRiskScoringEngine()
    except Exception as e:
        return None

def render_risk_intelligence_page(df: pd.DataFrame):
    st.title("🤖 AI Credit Risk Intelligence & Underwriting Simulator")
    st.markdown("Evaluate borrower credit default risk, simulate underwriting applications, and score loan portfolios using trained machine learning models.")
    st.markdown("---")

    engine = get_scoring_engine()
    if engine is None:
        st.error("⚠️ Model pipeline artifact not found. Please ensure Phase 4 model training was executed.")
        return

    # Model Status Header Callout
    st.info("ℹ️ **Model Pipeline Active**: Logistic Regression Pipeline (v1.0.0) | Test ROC-AUC: **0.6953** | Positive Target: Default (`Charged Off`)")

    tab1, tab2 = st.tabs(["📝 Single Application Simulator", "📊 Portfolio Batch Risk Distribution"])

    # Tab 1: Single Record Underwriting Simulator
    with tab1:
        st.subheader("Simulate Applicant Risk Assessment")
        st.caption("Input applicant underwriting parameters (pre-origination features only) to generate a predicted default probability.")

        col1, col2, col3 = st.columns(3)

        with col1:
            loan_amount = st.number_input("Loan Amount Requested ($)", min_value=500, max_value=50000, value=15000, step=500)
            annual_income = st.number_input("Annual Income ($)", min_value=10000, max_value=500000, value=60000, step=2500)
            dti = st.slider("Debt-to-Income Ratio (DTI %)", min_value=0.0, max_value=50.0, value=18.0, step=0.5) / 100.0
            int_rate = st.slider("Assigned Interest Rate (%)", min_value=5.0, max_value=30.0, value=12.5, step=0.25) / 100.0

        with col2:
            term = st.selectbox("Loan Term", ["36 months", "60 months"])
            grade = st.selectbox("Risk Grade", ["A", "B", "C", "D", "E", "F", "G"], index=1)
            home_ownership = st.selectbox("Home Ownership", ["RENT", "MORTGAGE", "OWN", "OTHER"])
            emp_length_years = st.slider("Employment Length (Years)", min_value=0, max_value=10, value=5, step=1)

        with col3:
            purpose = st.selectbox("Loan Purpose", ["debt_consolidation", "credit_card", "home_improvement", "car", "major_purchase", "other"])
            address_state = st.selectbox("State of Residence", ["CA", "NY", "TX", "FL", "GA", "IL", "PA", "OH", "NC", "VA"], index=0)
            verification_status = st.selectbox("Verification Status", ["Verified", "Source Verified", "Not Verified"])
            total_acc = st.number_input("Total Credit Lines", min_value=1, max_value=100, value=15, step=1)

        input_record = {
            "loan_amount": loan_amount,
            "annual_income": annual_income,
            "dti": dti,
            "int_rate": int_rate,
            "emp_length_years": float(emp_length_years),
            "total_acc": total_acc,
            "term": term,
            "grade": grade,
            "home_ownership": home_ownership,
            "verification_status": verification_status,
            "purpose": purpose,
            "address_state": address_state
        }

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 Calculate Credit Risk Score", type="primary", use_container_width=True):
            res = engine.score_record(input_record)

            if res["status"] == "SUCCESS":
                prob_pct = res["risk_score_pct"]
                category = res["risk_category"]

                r_col1, r_col2 = st.columns([1, 1])

                with r_col1:
                    fig_gauge = create_risk_gauge_chart(prob_pct, category)
                    st.plotly_chart(fig_gauge, use_container_width=True)

                with r_col2:
                    st.markdown("### Underwriting Assessment Summary")
                    st.metric("Predicted Default Probability", f"{prob_pct:.1f}%")
                    
                    if category == "Low Risk":
                        st.success(f"✅ **Assigned Tier**: {category} (< 15% default risk)\n\n**Recommendation**: Standard Underwriting Approval.")
                    elif category == "Medium Risk":
                        st.warning(f"⚠️ **Assigned Tier**: {category} (15% - 35% default risk)\n\n**Recommendation**: Manual Underwriting Review Required.")
                    else:
                        st.error(f"🚨 **Assigned Tier**: {category} (>= 35% default risk)\n\n**Recommendation**: High Adverse Risk Flag. Additional collateral/guarantor required.")

                    st.caption("🔒 *Model outputs are for academic decision support and experimental analysis, not automated credit rejection.*")

                # Display Top Global Feature Drivers (Model Explainability)
                st.markdown("<br>", unsafe_allow_html=True)
                st.subheader("🔍 Key Model Feature Drivers (Logistic Regression Coefficients)")
                df_exp = engine.get_model_explainability(top_n=10)
                if not df_exp.empty:
                    st.dataframe(
                        df_exp[["feature", "coefficient", "impact_direction"]],
                        use_container_width=True,
                        hide_index=True
                    )
            else:
                st.error(f"Scoring Error: {res.get('error')}")

    # Tab 2: Batch Risk Analysis
    with tab2:
        st.subheader("Portfolio Batch Risk Scoring")
        st.caption("Score all currently filtered portfolio records and analyze the risk tier distribution.")

        if st.button("📊 Score Current Filtered Dataset Batch"):
            with st.spinner("Scoring batch records..."):
                scored_batch = engine.score_batch(df)

            st.success(f"Successfully scored {len(scored_batch):,} loan records!")
            
            b_col1, b_col2 = st.columns(2)

            with b_col1:
                st.subheader("Risk Category Counts")
                cat_counts = scored_batch["risk_category"].value_counts().reset_index()
                cat_counts.columns = ["Risk Category", "Loan Count"]
                st.dataframe(cat_counts, use_container_width=True, hide_index=True)

            with b_col2:
                st.subheader("Default Probability Histogram")
                st.bar_chart(scored_batch["risk_category"].value_counts())

            st.dataframe(
                scored_batch[[
                    "id", "loan_amount", "grade", "address_state",
                    "predicted_default_prob", "predicted_risk_score_pct", "risk_category"
                ]],
                use_container_width=True,
                hide_index=True
            )
