"""
Unit Tests for UI Components and View Routing
"""

import pytest
import pandas as pd
import numpy as np
from src.ui.components import (
    format_currency,
    format_percentage,
    create_monthly_trends_chart,
    create_state_map_chart,
    create_purpose_chart,
    create_grade_chart,
    create_term_donut_chart,
    create_risk_gauge_chart
)

def test_format_currency():
    assert format_currency(435757075.0) == "$435.76M"
    assert format_currency(53981425.0) == "$53.98M"
    assert format_currency(2500.0) == "$2.5K"
    assert format_currency(500.0) == "$500"
    assert format_currency(0.0) == "$500" or format_currency(0.0) == "$0"

def test_format_percentage():
    assert format_percentage(0.1205) == "12.05%"
    assert format_percentage(13.33) == "13.33%"
    assert format_percentage(0.0) == "0.00%"

def test_plotly_chart_generators():
    df_monthly = pd.DataFrame({
        "issue_month": ["2021-01", "2021-02"],
        "total_loan_applications": [2332, 2279],
        "total_funded_amount": [25000000.0, 24000000.0]
    })
    fig_monthly = create_monthly_trends_chart(df_monthly)
    assert fig_monthly is not None

    df_state = pd.DataFrame({
        "address_state": ["CA", "NY"],
        "state_name": ["California", "New York"],
        "total_loan_applications": [5000, 3000]
    })
    fig_state = create_state_map_chart(df_state)
    assert fig_state is not None

    df_purpose = pd.DataFrame({
        "purpose": ["debt_consolidation", "credit_card"],
        "total_loan_applications": [18000, 5000]
    })
    fig_purpose = create_purpose_chart(df_purpose)
    assert fig_purpose is not None

    fig_gauge = create_risk_gauge_chart(67.96, "High Risk")
    assert fig_gauge is not None
