"""
UI Components Module
Provides custom CSS styling, reusable KPI metric cards, and Plotly chart generators
with a sleek, professional banking dashboard aesthetic.
"""

from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# -------------------------------------------------------------------------
# Custom Banking Dashboard CSS Theme
# -------------------------------------------------------------------------
BANKING_CSS = """
<style>
    /* Main Theme Overrides */
    .stApp {
        background-color: #0e1117;
        color: #e0e6ed;
    }
    
    /* Card Container Styling */
    .kpi-card {
        background: linear-gradient(135deg, #1e2530 0%, #161b22 100%);
        border: 1px solid #2d3748;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .kpi-card:hover {
        border-color: #3182ce;
        transform: translateY(-2px);
    }
    
    .kpi-title {
        color: #a0aec0;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 8px;
    }
    .kpi-value {
        color: #ffffff;
        font-size: 1.8rem;
        font-weight: 700;
        line-height: 1.2;
    }
    .kpi-sub {
        font-size: 0.85rem;
        margin-top: 8px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* Trend Badges */
    .trend-badge-positive {
        background-color: rgba(72, 187, 120, 0.15);
        color: #48bb78;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.8rem;
    }
    .trend-badge-negative {
        background-color: rgba(245, 101, 101, 0.15);
        color: #f56565;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.8rem;
    }

    /* Good / Bad Standing Card Styling */
    .standing-card-good {
        background: linear-gradient(135deg, #1c3d2f 0%, #142820 100%);
        border-left: 5px solid #38a169;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .standing-card-bad {
        background: linear-gradient(135deg, #3d1c1c 0%, #281414 100%);
        border-left: 5px solid #e53e3e;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
</style>
"""

def apply_custom_css():
    """Injects custom CSS theme into Streamlit app."""
    st.markdown(BANKING_CSS, unsafe_allow_html=True)

# -------------------------------------------------------------------------
# Number Formatting Utilities
# -------------------------------------------------------------------------
def format_currency(val: float) -> str:
    """Formats numeric float into compact currency string ($435.76M or $53.98M or $1,234)."""
    if val is None or np.isnan(val):
        return "$0"
    if abs(val) >= 1e9:
        return f"${val / 1e9:.2f}B"
    elif abs(val) >= 1e6:
        return f"${val / 1e6:.2f}M"
    elif abs(val) >= 1e3:
        return f"${val / 1e3:.1f}K"
    else:
        return f"${val:,.0f}"

def format_percentage(val: float) -> str:
    """Formats decimal or float into percentage string (e.g. 12.05%)."""
    if val is None or np.isnan(val):
        return "0.00%"
    # Handle decimal inputs (0.1205 -> 12.05%) vs percentage inputs (12.05 -> 12.05%)
    pct_val = val * 100.0 if abs(val) <= 1.0 else val
    return f"{pct_val:.2f}%"

def render_kpi_card(
    title: str, 
    main_val: float, 
    mtd_val: float, 
    mom_pct: float, 
    is_currency: bool = False, 
    is_pct: bool = False
):
    """Renders a structured HTML KPI Card component."""
    if is_currency:
        val_str = format_currency(main_val)
        mtd_str = f"{format_currency(mtd_val)} MTD"
    elif is_pct:
        val_str = format_percentage(main_val)
        mtd_str = f"{format_percentage(mtd_val)} MTD"
    else:
        val_str = f"{int(main_val):,}"
        mtd_str = f"{int(mtd_val):,} MTD"

    badge_class = "trend-badge-positive" if mom_pct >= 0 else "trend-badge-negative"
    sign = "+" if mom_pct >= 0 else ""
    mom_str = f"{sign}{mom_pct:.2f}% MoM"

    html = f"""
    <div class="kpi-card">
        <div class="kpi-title">{title}</div>
        <div class="kpi-value">{val_str}</div>
        <div class="kpi-sub">
            <span style="color: #a0aec0;">{mtd_str}</span>
            <span class="{badge_class}">{mom_str}</span>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_standing_card(
    title: str,
    count: int,
    funded: float,
    received: float,
    pct_apps: float,
    is_good: bool = True
):
    """Renders a Good/Bad loan standing summary card."""
    card_class = "standing-card-good" if is_good else "standing-card-bad"
    status_color = "#38a169" if is_good else "#e53e3e"
    
    html = f"""
    <div class="{card_class}">
        <div style="font-size: 1.1rem; font-weight: 700; color: {status_color}; margin-bottom: 10px;">{title} ({pct_apps:.1f}% of Total)</div>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px;">
            <div>
                <div style="color: #a0aec0; font-size: 0.75rem;">APPLICATIONS</div>
                <div style="font-size: 1.3rem; font-weight: 700;">{count:,}</div>
            </div>
            <div>
                <div style="color: #a0aec0; font-size: 0.75rem;">FUNDED AMOUNT</div>
                <div style="font-size: 1.3rem; font-weight: 700;">{format_currency(funded)}</div>
            </div>
            <div>
                <div style="color: #a0aec0; font-size: 0.75rem;">RECEIVED AMOUNT</div>
                <div style="font-size: 1.3rem; font-weight: 700;">{format_currency(received)}</div>
            </div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# -------------------------------------------------------------------------
# Plotly Chart Generators
# -------------------------------------------------------------------------
PLOTLY_TEMPLATE = "plotly_dark"
COLOR_PRIMARY = "#3182ce"
COLOR_SUCCESS = "#38a169"
COLOR_DANGER = "#e53e3e"
COLOR_ACCENT = "#805ad5"

def create_monthly_trends_chart(df_monthly: pd.DataFrame) -> go.Figure:
    """Generates a line chart showing Monthly Loan Applications & Funded Amount trends."""
    fig = go.Figure()
    
    if df_monthly is not None and not df_monthly.empty:
        fig.add_trace(go.Bar(
            x=df_monthly["issue_month"],
            y=df_monthly["total_funded_amount"] / 1e6,
            name="Funded Amount ($M)",
            marker_color=COLOR_PRIMARY,
            opacity=0.7
        ))
        
        fig.add_trace(go.Scatter(
            x=df_monthly["issue_month"],
            y=df_monthly["total_loan_applications"],
            name="Loan Applications",
            mode="lines+markers",
            line=dict(color="#ecc94b", width=3),
            yaxis="y2"
        ))

    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        title="Monthly Trend Analysis (Funded Amount vs Applications)",
        xaxis_title="Issue Month",
        yaxis=dict(title="Funded Amount ($ Millions)", showgrid=False),
        yaxis2=dict(title="Loan Applications Count", overlaying="y", side="right", showgrid=False),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=40, t=60, b=40)
    )
    return fig

def create_state_map_chart(df_state: pd.DataFrame) -> go.Figure:
    """Generates US Choropleth Map or State Bar Chart of Applications by State."""
    if df_state is not None and not df_state.empty:
        fig = px.choropleth(
            df_state,
            locations="address_state",
            locationmode="USA-states",
            color="total_loan_applications",
            scope="usa",
            hover_name="state_name" if "state_name" in df_state.columns else "address_state",
            color_continuous_scale="Blues",
            title="Loan Applications Geography by US State"
        )
        fig.update_layout(
            template=PLOTLY_TEMPLATE,
            geo=dict(bgcolor="rgba(0,0,0,0)", lakecolor="rgba(0,0,0,0)"),
            margin=dict(l=20, r=20, t=50, b=20)
        )
        return fig
    return go.Figure()

def create_purpose_chart(df_purpose: pd.DataFrame) -> go.Figure:
    """Generates Horizontal Bar Chart of Loan Applications by Purpose."""
    if df_purpose is not None and not df_purpose.empty:
        df_sorted = df_purpose.sort_values("total_loan_applications", ascending=True)
        fig = px.bar(
            df_sorted,
            x="total_loan_applications",
            y="purpose",
            orientation="h",
            text="total_loan_applications",
            color="total_loan_applications",
            color_continuous_scale="Purples",
            title="Loan Breakdown by Stated Purpose"
        )
        fig.update_layout(template=PLOTLY_TEMPLATE, showlegend=False, margin=dict(l=40, r=40, t=50, b=40))
        return fig
    return go.Figure()

def create_grade_chart(df_grade: pd.DataFrame) -> go.Figure:
    """Generates Bar Chart of Applications by Risk Grade A-G."""
    if df_grade is not None and not df_grade.empty:
        fig = px.bar(
            df_grade,
            x="grade",
            y="total_loan_applications",
            color="grade",
            color_discrete_sequence=px.colors.qualitative.Bold,
            text="total_loan_applications",
            title="Loan Applications Distribution by Risk Grade"
        )
        fig.update_layout(template=PLOTLY_TEMPLATE, showlegend=False, margin=dict(l=40, r=40, t=50, b=40))
        return fig
    return go.Figure()

def create_term_donut_chart(df_term: pd.DataFrame) -> go.Figure:
    """Generates Donut Chart for 36 vs 60 Month Loan Terms."""
    if df_term is not None and not df_term.empty:
        fig = px.pie(
            df_term,
            names="term",
            values="total_loan_applications",
            hole=0.5,
            color_discrete_sequence=[COLOR_PRIMARY, COLOR_ACCENT],
            title="Loan Term Ratio (36 vs 60 Months)"
        )
        fig.update_layout(template=PLOTLY_TEMPLATE, margin=dict(l=20, r=20, t=50, b=20))
        return fig
    return go.Figure()

def create_risk_gauge_chart(prob_pct: float, risk_category: str) -> go.Figure:
    """Generates Gauge Chart for Credit Risk Score Probability."""
    gauge_color = COLOR_SUCCESS if risk_category == "Low Risk" else ("#ecc94b" if risk_category == "Medium Risk" else COLOR_DANGER)
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=prob_pct,
        number={"suffix": "%", "valueformat": ".1f"},
        title={"text": f"Predicted Default Risk ({risk_category})", "font": {"size": 18}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1},
            "bar": {"color": gauge_color},
            "steps": [
                {"range": [0, 15], "color": "rgba(72, 187, 120, 0.2)"},
                {"range": [15, 35], "color": "rgba(236, 201, 75, 0.2)"},
                {"range": [35, 100], "color": "rgba(245, 101, 101, 0.2)"}
            ],
            "threshold": {
                "line": {"color": "white", "width": 3},
                "thickness": 0.75,
                "value": prob_pct
            }
        }
    ))
    fig.update_layout(template=PLOTLY_TEMPLATE, height=300, margin=dict(l=30, r=30, t=50, b=20))
    return fig
