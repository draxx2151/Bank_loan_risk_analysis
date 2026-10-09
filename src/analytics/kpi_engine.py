"""
KPI Engine Module
Provides functional and object-oriented calculation routines for domain KPIs
using both Pandas DataFrames and SQL queries against SQLite database.
Handles MTD, PMTD, MoM, Good vs Bad loan portfolio metrics, and edge cases.
"""

from typing import Dict, Any, Optional
import pandas as pd
import numpy as np

class KPIEngine:
    """Computes financial KPIs, standing ratios, and growth metrics."""

    @staticmethod
    def compute_summary_kpis(df: pd.DataFrame) -> Dict[str, Any]:
        """Calculates 5 core summary KPIs from DataFrame."""
        if df is None or df.empty:
            return {
                "total_applications": 0,
                "total_funded_amount": 0.0,
                "total_amount_received": 0.0,
                "avg_int_rate": 0.0,
                "avg_dti": 0.0
            }

        total_apps = int(len(df))
        total_funded = float(df["loan_amount"].sum()) if "loan_amount" in df.columns else 0.0
        total_received = float(df["total_payment"].sum()) if "total_payment" in df.columns else 0.0
        avg_int = float(df["int_rate"].mean()) if "int_rate" in df.columns and total_apps > 0 else 0.0
        avg_dti = float(df["dti"].mean()) if "dti" in df.columns and total_apps > 0 else 0.0

        return {
            "total_applications": total_apps,
            "total_funded_amount": total_funded,
            "total_amount_received": total_received,
            "avg_int_rate": avg_int if not np.isnan(avg_int) else 0.0,
            "avg_dti": avg_dti if not np.isnan(avg_dti) else 0.0
        }

    @staticmethod
    def compute_period_kpis(df: pd.DataFrame, year_month: str) -> Dict[str, Any]:
        """Calculates KPIs for a specific YYYY-MM issue_date period."""
        if df is None or df.empty or "issue_date" not in df.columns:
            return {
                "applications": 0,
                "funded_amount": 0.0,
                "amount_received": 0.0,
                "avg_int_rate": 0.0,
                "avg_dti": 0.0
            }

        # Convert issue_date to datetime series safely
        dt_series = pd.to_datetime(df["issue_date"], errors="coerce")
        period_mask = dt_series.dt.strftime("%Y-%m") == year_month
        period_df = df[period_mask]

        res = KPIEngine.compute_summary_kpis(period_df)
        return {
            "applications": res["total_applications"],
            "funded_amount": res["total_funded_amount"],
            "amount_received": res["total_amount_received"],
            "avg_int_rate": res["avg_int_rate"],
            "avg_dti": res["avg_dti"]
        }

    @staticmethod
    def compute_mom_growth(mtd_metrics: Dict[str, Any], pmtd_metrics: Dict[str, Any]) -> Dict[str, float]:
        """Calculates Month-over-Month (MoM) percentage growth between MTD and PMTD."""
        def pct_change(current: float, previous: float) -> float:
            if previous is None or previous == 0 or np.isnan(previous):
                return 0.0
            return float(((current - previous) / previous) * 100.0)

        return {
            "applications_mom_pct": pct_change(
                mtd_metrics.get("applications", 0), pmtd_metrics.get("applications", 0)
            ),
            "funded_amount_mom_pct": pct_change(
                mtd_metrics.get("funded_amount", 0.0), pmtd_metrics.get("funded_amount", 0.0)
            ),
            "amount_received_mom_pct": pct_change(
                mtd_metrics.get("amount_received", 0.0), pmtd_metrics.get("amount_received", 0.0)
            ),
            "avg_int_rate_mom_pct": pct_change(
                mtd_metrics.get("avg_int_rate", 0.0), pmtd_metrics.get("avg_int_rate", 0.0)
            ),
            "avg_dti_mom_pct": pct_change(
                mtd_metrics.get("avg_dti", 0.0), pmtd_metrics.get("avg_dti", 0.0)
            )
        }

    @staticmethod
    def compute_good_vs_bad_kpis(df: pd.DataFrame) -> Dict[str, Any]:
        """Calculates Good Standing vs Bad Standing portfolio metrics."""
        if df is None or df.empty:
            return {
                "good_loans": {"count": 0, "funded_amount": 0.0, "amount_received": 0.0, "pct_applications": 0.0, "pct_funded": 0.0},
                "bad_loans": {"count": 0, "funded_amount": 0.0, "amount_received": 0.0, "pct_applications": 0.0, "pct_funded": 0.0}
            }

        total_apps = len(df)
        total_funded = float(df["loan_amount"].sum()) if "loan_amount" in df.columns else 0.0

        # Good loans: Fully Paid or Current
        good_mask = df["loan_status"].isin(["Fully Paid", "Current"]) if "loan_status" in df.columns else pd.Series(False, index=df.index)
        good_df = df[good_mask]
        
        # Bad loans: Charged Off
        bad_mask = df["loan_status"] == "Charged Off" if "loan_status" in df.columns else pd.Series(False, index=df.index)
        bad_df = df[bad_mask]

        good_count = len(good_df)
        good_funded = float(good_df["loan_amount"].sum()) if "loan_amount" in good_df.columns else 0.0
        good_received = float(good_df["total_payment"].sum()) if "total_payment" in good_df.columns else 0.0

        bad_count = len(bad_df)
        bad_funded = float(bad_df["loan_amount"].sum()) if "loan_amount" in bad_df.columns else 0.0
        bad_received = float(bad_df["total_payment"].sum()) if "total_payment" in bad_df.columns else 0.0

        return {
            "good_loans": {
                "count": good_count,
                "funded_amount": good_funded,
                "amount_received": good_received,
                "pct_applications": round((good_count / total_apps * 100.0), 2) if total_apps > 0 else 0.0,
                "pct_funded": round((good_funded / total_funded * 100.0), 2) if total_funded > 0 else 0.0
            },
            "bad_loans": {
                "count": bad_count,
                "funded_amount": bad_funded,
                "amount_received": bad_received,
                "pct_applications": round((bad_count / total_apps * 100.0), 2) if total_apps > 0 else 0.0,
                "pct_funded": round((bad_funded / total_funded * 100.0), 2) if total_funded > 0 else 0.0
            }
        }
