from __future__ import annotations

import numpy as np
import pandas as pd


def aggregate_message_features(messages: pd.DataFrame) -> pd.DataFrame:
    sender_dummies = pd.get_dummies(messages["sender_type"], prefix="sender")
    message_enriched = pd.concat([messages[["claim_id", "sentiment_score", "response_latency_minutes", "escalation_flag"]], sender_dummies], axis=1)

    aggregated = message_enriched.groupby("claim_id", as_index=False).agg(
        message_count=("claim_id", "size"),
        avg_sentiment_score=("sentiment_score", "mean"),
        min_sentiment_score=("sentiment_score", "min"),
        avg_response_latency_minutes=("response_latency_minutes", "mean"),
        max_response_latency_minutes=("response_latency_minutes", "max"),
        escalated_message_count=("escalation_flag", "sum"),
        sender_adjuster=("sender_adjuster", "sum") if "sender_adjuster" in message_enriched.columns else ("claim_id", "size"),
        sender_attorney=("sender_attorney", "sum") if "sender_attorney" in message_enriched.columns else ("claim_id", "count"),
        sender_claimant=("sender_claimant", "sum") if "sender_claimant" in message_enriched.columns else ("claim_id", "count"),
        sender_insured=("sender_insured", "sum") if "sender_insured" in message_enriched.columns else ("claim_id", "count"),
    )
    aggregated["message_escalation_rate"] = np.where(
        aggregated["message_count"] > 0,
        aggregated["escalated_message_count"] / aggregated["message_count"],
        0.0,
    )
    aggregated["claimant_message_share"] = np.where(
        aggregated["message_count"] > 0,
        aggregated["sender_claimant"] / aggregated["message_count"],
        0.0,
    )
    aggregated["attorney_message_share"] = np.where(
        aggregated["message_count"] > 0,
        aggregated["sender_attorney"] / aggregated["message_count"],
        0.0,
    )
    return aggregated


def build_analytical_base_table(datasets: dict[str, pd.DataFrame]) -> pd.DataFrame:
    claims = datasets["claims"].copy()
    fnol = datasets["fnol"].copy()
    messages = datasets["messages"].copy()
    policy = datasets["policy"].copy()

    message_features = aggregate_message_features(messages)

    analytical = (
        claims.merge(fnol, on="claim_id", how="left", suffixes=("", "_fnol"))
        .merge(message_features, on="claim_id", how="left")
        .merge(policy, on="policy_id", how="left", suffixes=("", "_policy"))
    )

    numeric_defaults = {
        "message_count": 0,
        "avg_sentiment_score": 0.0,
        "min_sentiment_score": 0.0,
        "avg_response_latency_minutes": 0.0,
        "max_response_latency_minutes": 0.0,
        "escalated_message_count": 0,
        "message_escalation_rate": 0.0,
        "claimant_message_share": 0.0,
        "attorney_message_share": 0.0,
        "sender_adjuster": 0,
        "sender_attorney": 0,
        "sender_claimant": 0,
        "sender_insured": 0,
    }
    for column, default_value in numeric_defaults.items():
        analytical[column] = analytical[column].fillna(default_value)

    analytical["report_lag_days"] = (
        analytical["report_date"] - analytical["loss_date"]
    ).dt.days.fillna(analytical["report_lag_days_raw"]).clip(lower=0)
    analytical["total_incurred"] = analytical["paid_amount"] + analytical["reserve_amount"]
    analytical["paid_to_reserve_ratio"] = np.where(
        analytical["reserve_amount"] > 0,
        analytical["paid_amount"] / analytical["reserve_amount"],
        analytical["paid_amount"],
    )
    analytical["coverage_per_driver"] = np.where(
        analytical["driver_count"] > 0,
        analytical["coverage_limit_bi"] / analytical["driver_count"],
        analytical["coverage_limit_bi"],
    )
    analytical["exposure_complexity_index"] = (
        analytical["vehicle_count"]
        + analytical["driver_count"]
        + analytical["prior_claim_count"] * 1.5
        + analytical["attorney_rep_flag"] * 2
        + analytical["message_escalation_rate"] * 3
    )
    analytical["early_injury_signal"] = np.where(
        (analytical["injury_reported_at_fnol"] == 1) | (analytical["injury_flag"] == 1),
        1,
        0,
    )
    analytical["high_latency_flag"] = (analytical["avg_response_latency_minutes"] >= 180).astype(int)
    analytical["negative_sentiment_flag"] = (analytical["avg_sentiment_score"] < -0.2).astype(int)

    analytical = analytical.sort_values("claim_id").reset_index(drop=True)
    return analytical

