from __future__ import annotations

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from .config import RANDOM_SEED
from .evaluation import evaluate_classification


LIABILITY_FEATURES = [
    "state",
    "claim_type",
    "injury_flag",
    "attorney_rep_flag",
    "liability_decision",
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
    "vehicle_count",
    "driver_count",
    "prior_claim_count",
    "coverage_limit_bi",
    "premium_amount",
    "nonstandard_risk_tier",
    "coverage_per_driver",
    "exposure_complexity_index",
    "early_injury_signal",
    "high_latency_flag",
    "negative_sentiment_flag",
]


def train_bodily_injury_model(analytical_base: pd.DataFrame) -> dict[str, object]:
    model_frame = analytical_base.copy()
    X = model_frame[LIABILITY_FEATURES]
    y = model_frame["bodily_injury_flag"].astype(int)

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
            (
                "classifier",
                RandomForestClassifier(
                    n_estimators=250,
                    max_depth=8,
                    min_samples_leaf=4,
                    random_state=RANDOM_SEED,
                ),
            ),
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=RANDOM_SEED,
        stratify=y,
    )
    model.fit(X_train, y_train)

    train_pred = model.predict(X_train)
    test_pred = model.predict(X_test)
    train_prob = model.predict_proba(X_train)[:, 1]
    test_prob = model.predict_proba(X_test)[:, 1]

    metrics = {
        "train": evaluate_classification(y_train, train_pred, train_prob),
        "test": evaluate_classification(y_test, test_pred, test_prob),
    }

    interpretation = [
        "BI exposure is expected to increase with early injury signals, attorney involvement, certain impact types, adverse communications, and higher-risk non-standard segments."
    ]

    return {
        "model": model,
        "features": LIABILITY_FEATURES,
        "metrics": metrics,
        "feature_interpretation": interpretation,
    }
