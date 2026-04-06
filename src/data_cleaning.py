from __future__ import annotations

import pandas as pd


BOOLEAN_COLUMNS = {
    "claims": ["injury_flag", "attorney_rep_flag", "bodily_injury_flag", "closed_flag"],
    "fnol": ["police_report_flag", "witness_flag", "injury_reported_at_fnol"],
    "messages": ["escalation_flag"],
}

DATE_COLUMNS = {
    "claims": ["loss_date", "report_date"],
    "messages": ["message_timestamp"],
}

NUMERIC_FILL_DEFAULTS = {
    "reserve_amount": 0.0,
    "paid_amount": 0.0,
    "days_to_close": 0,
    "sentiment_score": 0.0,
    "response_latency_minutes": 0.0,
    "vehicle_count": 1,
    "driver_count": 1,
    "prior_claim_count": 0,
    "coverage_limit_bi": 25000,
    "coverage_limit_pd": 10000,
    "premium_amount": 0.0,
}


def _coerce_dates(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    for column in columns:
        df[column] = pd.to_datetime(df[column], errors="coerce")
    return df


def _coerce_booleans(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    for column in columns:
        df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0).astype(int)
    return df


def _fill_categoricals(df: pd.DataFrame) -> pd.DataFrame:
    categorical_columns = df.select_dtypes(include=["object", "string"]).columns
    for column in categorical_columns:
        df[column] = df[column].fillna("unknown")
    return df


def _fill_numeric_defaults(df: pd.DataFrame) -> pd.DataFrame:
    for column, default_value in NUMERIC_FILL_DEFAULTS.items():
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce").fillna(default_value)
    return df


def clean_datasets(datasets: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    cleaned = {name: frame.copy() for name, frame in datasets.items()}

    for dataset_name, columns in DATE_COLUMNS.items():
        cleaned[dataset_name] = _coerce_dates(cleaned[dataset_name], columns)

    for dataset_name, columns in BOOLEAN_COLUMNS.items():
        cleaned[dataset_name] = _coerce_booleans(cleaned[dataset_name], columns)

    for dataset_name, frame in cleaned.items():
        cleaned[dataset_name] = _fill_numeric_defaults(frame)
        cleaned[dataset_name] = _fill_categoricals(cleaned[dataset_name])

    cleaned["claims"]["report_lag_days_raw"] = (
        cleaned["claims"]["report_date"] - cleaned["claims"]["loss_date"]
    ).dt.days.fillna(0).clip(lower=0)

    return cleaned
