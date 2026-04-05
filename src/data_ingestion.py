from __future__ import annotations

from pathlib import Path

import pandas as pd

from .config import CLAIMS_FILE, FNOL_FILE, MESSAGES_FILE, POLICY_FILE


REQUIRED_COLUMNS = {
    "claims": {
        "claim_id",
        "policy_id",
        "claimant_id",
        "loss_date",
        "report_date",
        "state",
        "claim_type",
        "injury_flag",
        "attorney_rep_flag",
        "bodily_injury_flag",
        "liability_decision",
        "reserve_amount",
        "paid_amount",
        "closed_flag",
        "days_to_close",
    },
    "fnol": {
        "fnol_id",
        "claim_id",
        "reporting_channel",
        "description_of_loss",
        "police_report_flag",
        "witness_flag",
        "loss_location",
        "weather_condition",
        "point_of_impact",
        "injury_reported_at_fnol",
    },
    "messages": {
        "message_id",
        "claim_id",
        "message_timestamp",
        "sender_type",
        "sentiment_score",
        "response_latency_minutes",
        "escalation_flag",
    },
    "policy": {
        "policy_id",
        "policy_state",
        "vehicle_count",
        "driver_count",
        "prior_claim_count",
        "coverage_limit_bi",
        "coverage_limit_pd",
        "premium_amount",
        "nonstandard_risk_tier",
    },
}


def _validate_columns(df: pd.DataFrame, required_columns: set[str], dataset_name: str) -> None:
    missing_columns = required_columns.difference(df.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"{dataset_name} is missing required columns: {missing}")


def _load_csv(path: Path, dataset_name: str) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Expected {dataset_name} file at {path}")
    return pd.read_csv(path)


def load_datasets() -> dict[str, pd.DataFrame]:
    datasets = {
        "claims": _load_csv(CLAIMS_FILE, "claims"),
        "fnol": _load_csv(FNOL_FILE, "fnol"),
        "messages": _load_csv(MESSAGES_FILE, "messages"),
        "policy": _load_csv(POLICY_FILE, "policy"),
    }
    for dataset_name, frame in datasets.items():
        _validate_columns(frame, REQUIRED_COLUMNS[dataset_name], dataset_name)
    return datasets

