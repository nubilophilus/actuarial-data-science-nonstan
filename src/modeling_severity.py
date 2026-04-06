from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from .config import RANDOM_SEED
from .evaluation import evaluate_regression


SEVERITY_FEATURES = [
    "state",
    "claim_type",
    "injury_flag",
    "attorney_rep_flag",
    "bodily_injury_flag",
    "liability_decision",
    "closed_flag",
    "days_to_close",
    "report_lag_days",
    "reporting_channel",
    "police_report_flag",
    "witness_flag",
    "loss_location",
    "weather_condition",
    "point_of_impact",
    "injury_reported_at_fnol",
    "message_count",
    "avg_sentiment_score",
    "avg_response_latency_minutes",
    "message_escalation_rate",
    "claimant_message_share",
    "attorney_message_share",
    "policy_state",
    "vehicle_count",
    "driver_count",
    "prior_claim_count",
    "coverage_limit_bi",
    "coverage_limit_pd",
    "premium_amount",
    "nonstandard_risk_tier",
    "coverage_per_driver",
    "exposure_complexity_index",
    "early_injury_signal",
    "high_latency_flag",
    "negative_sentiment_flag",
]


def train_claim_severity_model(analytical_base: pd.DataFrame) -> dict[str, object]:
    model_frame = analytical_base.copy()
    model_frame["severity_target"] = model_frame["total_incurred"].clip(lower=0)

    X = model_frame[SEVERITY_FEATURES]
    y = np.log1p(model_frame["severity_target"])

    categorical_features = X.select_dtypes(include=["object", "string"]).columns.tolist()
    numeric_features = [column for column in X.columns if column not in categorical_features]

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "categorical",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        ("encoder", OneHotEncoder(handle_unknown="ignore")),
                    ]
                ),
                categorical_features,
            ),
            (
                "numeric",
                Pipeline(steps=[("imputer", SimpleImputer(strategy="median"))]),
                numeric_features,
            ),
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("regressor", HistGradientBoostingRegressor(random_state=RANDOM_SEED)),
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=RANDOM_SEED)
    model.fit(X_train, y_train)

    train_pred = np.expm1(model.predict(X_train))
    test_pred = np.expm1(model.predict(X_test))
    y_train_actual = np.expm1(y_train)
    y_test_actual = np.expm1(y_test)

    metrics = {
        "train": evaluate_regression(y_train_actual, train_pred),
        "test": evaluate_regression(y_test_actual, test_pred),
    }

    feature_importance_note = [
        "Severity is typically influenced by injury involvement, attorney representation, policy limits, prior claims, reporting lag, and communication escalation signals."
    ]

    return {
        "model": model,
        "features": SEVERITY_FEATURES,
        "metrics": metrics,
        "feature_interpretation": feature_importance_note,
    }
