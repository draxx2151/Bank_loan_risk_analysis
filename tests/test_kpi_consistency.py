"""
Unit Tests for KPI Consistency: SQL Queries vs Pandas KPI Engine
Ensures zero numerical discrepancy between database SQL aggregations and Pandas calculations.
"""

import pytest
import pandas as pd
import numpy as np
from src.config import DEFAULT_DB_PATH, CLEANED_DATA_PATH
from src.database.db_manager import DatabaseManager
from src.analytics.kpi_engine import KPIEngine

@pytest.fixture(scope="module")
def loaded_db_and_df():
    """Loads database manager and cleaned Pandas dataframe for cross-validation."""
    db_mgr = DatabaseManager(DEFAULT_DB_PATH)
    if not DEFAULT_DB_PATH.exists():
        pytest.skip("SQLite database does not exist. Run Phase 2 loader first.")
    
    df = pd.read_csv(CLEANED_DATA_PATH, low_memory=False)
    return db_mgr, df

def test_overall_kpi_sql_vs_pandas_consistency(loaded_db_and_df):
    db_mgr, df = loaded_db_and_df

    # 1. SQL Overall Query
    sql = """
    SELECT 
        COUNT(id) AS total_applications,
        SUM(loan_amount) AS total_funded_amount,
        SUM(total_payment) AS total_amount_received,
        AVG(int_rate) AS avg_int_rate,
        AVG(dti) AS avg_dti
    FROM bank_loans;
    """
    sql_res = db_mgr.execute_query(sql).iloc[0].to_dict()

    # 2. Pandas KPI Engine
    pandas_res = KPIEngine.compute_summary_kpis(df)

    # 3. Assert zero numeric discrepancy
    assert sql_res["total_applications"] == pandas_res["total_applications"]
    assert abs(sql_res["total_funded_amount"] - pandas_res["total_funded_amount"]) < 1e-4
    assert abs(sql_res["total_amount_received"] - pandas_res["total_amount_received"]) < 1e-4
    assert abs(sql_res["avg_int_rate"] - pandas_res["avg_int_rate"]) < 1e-6
    assert abs(sql_res["avg_dti"] - pandas_res["avg_dti"]) < 1e-6

def test_mtd_kpi_sql_vs_pandas_consistency(loaded_db_and_df):
    db_mgr, df = loaded_db_and_df

    # Dec 2021 MTD Query
    sql = """
    SELECT 
        COUNT(id) AS applications,
        SUM(loan_amount) AS funded_amount,
        SUM(total_payment) AS amount_received,
        AVG(int_rate) AS avg_int_rate,
        AVG(dti) AS avg_dti
    FROM bank_loans
    WHERE strftime('%Y-%m', issue_date) = '2021-12';
    """
    sql_res = db_mgr.execute_query(sql).iloc[0].to_dict()
    pandas_res = KPIEngine.compute_period_kpis(df, "2021-12")

    assert sql_res["applications"] == pandas_res["applications"]
    assert abs(sql_res["funded_amount"] - pandas_res["funded_amount"]) < 1e-4
    assert abs(sql_res["amount_received"] - pandas_res["amount_received"]) < 1e-4
    assert abs(sql_res["avg_int_rate"] - pandas_res["avg_int_rate"]) < 1e-6
    assert abs(sql_res["avg_dti"] - pandas_res["avg_dti"]) < 1e-6

def test_pmtd_kpi_sql_vs_pandas_consistency(loaded_db_and_df):
    db_mgr, df = loaded_db_and_df

    # Nov 2021 PMTD Query
    sql = """
    SELECT 
        COUNT(id) AS applications,
        SUM(loan_amount) AS funded_amount,
        SUM(total_payment) AS amount_received,
        AVG(int_rate) AS avg_int_rate,
        AVG(dti) AS avg_dti
    FROM bank_loans
    WHERE strftime('%Y-%m', issue_date) = '2021-11';
    """
    sql_res = db_mgr.execute_query(sql).iloc[0].to_dict()
    pandas_res = KPIEngine.compute_period_kpis(df, "2021-11")

    assert sql_res["applications"] == pandas_res["applications"]
    assert abs(sql_res["funded_amount"] - pandas_res["funded_amount"]) < 1e-4
    assert abs(sql_res["amount_received"] - pandas_res["amount_received"]) < 1e-4

def test_good_vs_bad_loans_sql_vs_pandas_consistency(loaded_db_and_df):
    db_mgr, df = loaded_db_and_df

    # Good Loans SQL
    sql_good = "SELECT COUNT(id) AS count, SUM(loan_amount) AS funded FROM bank_loans WHERE loan_status IN ('Fully Paid', 'Current');"
    good_sql = db_mgr.execute_query(sql_good).iloc[0].to_dict()

    # Bad Loans SQL
    sql_bad = "SELECT COUNT(id) AS count, SUM(loan_amount) AS funded FROM bank_loans WHERE loan_status = 'Charged Off';"
    bad_sql = db_mgr.execute_query(sql_bad).iloc[0].to_dict()

    pandas_standing = KPIEngine.compute_good_vs_bad_kpis(df)

    assert good_sql["count"] == pandas_standing["good_loans"]["count"]
    assert abs(good_sql["funded"] - pandas_standing["good_loans"]["funded_amount"]) < 1e-4
    assert bad_sql["count"] == pandas_standing["bad_loans"]["count"]
    assert abs(bad_sql["funded"] - pandas_standing["bad_loans"]["funded_amount"]) < 1e-4

def test_mom_growth_calculation():
    mtd = {"applications": 4314, "funded_amount": 53981425.0, "amount_received": 58074380.0, "avg_int_rate": 0.12356, "avg_dti": 0.13665}
    pmtd = {"applications": 4035, "funded_amount": 47754825.0, "amount_received": 50132030.0, "avg_int_rate": 0.11941, "avg_dti": 0.13302}

    mom = KPIEngine.compute_mom_growth(mtd, pmtd)
    assert round(mom["applications_mom_pct"], 2) == 6.91
    assert round(mom["funded_amount_mom_pct"], 2) == 13.04 or round(mom["funded_amount_mom_pct"], 1) == 13.0

def test_kpi_engine_empty_dataframe_handling():
    empty_df = pd.DataFrame()
    res = KPIEngine.compute_summary_kpis(empty_df)
    assert res["total_applications"] == 0
    assert res["total_funded_amount"] == 0.0

    period_res = KPIEngine.compute_period_kpis(empty_df, "2021-12")
    assert period_res["applications"] == 0

    standing_res = KPIEngine.compute_good_vs_bad_kpis(empty_df)
    assert standing_res["good_loans"]["count"] == 0

    mom_zero = KPIEngine.compute_mom_growth({"applications": 100}, {"applications": 0})
    assert mom_zero["applications_mom_pct"] == 0.0
