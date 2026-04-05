from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from .config import (
    CLAIMS_FILE,
    CLAIM_TYPES,
    DEFAULT_CLAIM_COUNT,
    FNOL_FILE,
    LIABILITY_DECISIONS,
    MESSAGES_FILE,
    POINTS_OF_IMPACT,
    POLICY_FILE,
    REPORTING_CHANNELS,
    RISK_TIERS,
    STATES,
    WEATHER_CONDITIONS,
    LOSS_LOCATIONS,
    RANDOM_SEED,
)
from .utils import ensure_directories


@dataclass
class SyntheticDataBundle:
    claims: pd.DataFrame
    fnol: pd.DataFrame
    messages: pd.DataFrame
    policy: pd.DataFrame


def _build_policy_frame(rng: np.random.Generator, policy_count: int) -> pd.DataFrame:
    policy_ids = [f"POL{100000 + idx}" for idx in range(policy_count)]
    risk_tiers = rng.choice(RISK_TIERS, size=policy_count, p=[0.16, 0.29, 0.32, 0.23])
    vehicle_count = rng.choice([1, 2, 3, 4], size=policy_count, p=[0.43, 0.35, 0.16, 0.06])
    driver_count = np.clip(vehicle_count + rng.integers(0, 3, size=policy_count), 1, 5)
    prior_claim_count = np.clip(
        rng.poisson(lam=np.select(
            [risk_tiers == "tier_1", risk_tiers == "tier_2", risk_tiers == "tier_3", risk_tiers == "tier_4"],
            [0.4, 0.8, 1.3, 1.8],
            default=1.0,
        )),
        0,
        6,
    )
    coverage_limit_bi = rng.choice([15000, 25000, 50000, 100000], size=policy_count, p=[0.28, 0.36, 0.24, 0.12])
    coverage_limit_pd = rng.choice([5000, 10000, 25000, 50000], size=policy_count, p=[0.25, 0.4, 0.23, 0.12])
    base_premium = 550 + vehicle_count * 180 + driver_count * 125 + prior_claim_count * 210
    tier_load = np.select(
        [risk_tiers == "tier_1", risk_tiers == "tier_2", risk_tiers == "tier_3", risk_tiers == "tier_4"],
        [0.95, 1.05, 1.2, 1.38],
        default=1.1,
    )
    premium_amount = np.round(base_premium * tier_load + rng.normal(0, 85, size=policy_count), 2)

    return pd.DataFrame(
        {
            "policy_id": policy_ids,
            "policy_state": rng.choice(STATES, size=policy_count, p=[0.23, 0.2, 0.21, 0.12, 0.11, 0.13]),
            "vehicle_count": vehicle_count,
            "driver_count": driver_count,
            "prior_claim_count": prior_claim_count,
            "coverage_limit_bi": coverage_limit_bi,
            "coverage_limit_pd": coverage_limit_pd,
            "premium_amount": premium_amount,
            "nonstandard_risk_tier": risk_tiers,
        }
    )


def _sample_claim_type(rng: np.random.Generator, risk_tier: str, prior_claim_count: int) -> str:
    base = np.array([0.24, 0.21, 0.15, 0.28, 0.12])
    if risk_tier in {"tier_3", "tier_4"}:
        base += np.array([-0.02, 0.03, 0.03, -0.03, -0.01])
    if prior_claim_count >= 2:
        base += np.array([-0.01, 0.02, 0.02, -0.01, -0.02])
    base = np.clip(base, 0.05, None)
    base = base / base.sum()
    return rng.choice(CLAIM_TYPES, p=base)


def generate_synthetic_insurance_data(
    claim_count: int = DEFAULT_CLAIM_COUNT,
    random_seed: int = RANDOM_SEED,
) -> SyntheticDataBundle:
    rng = np.random.default_rng(random_seed)
    policy_count = max(int(claim_count * 0.72), 850)
    policy = _build_policy_frame(rng, policy_count)

    sampled_policies = policy.sample(n=claim_count, replace=True, random_state=random_seed).reset_index(drop=True)
    claim_ids = [f"CLM{200000 + idx}" for idx in range(claim_count)]
    claimant_ids = [f"CLT{500000 + idx}" for idx in range(claim_count)]

    start_date = np.datetime64("2024-01-01")
    loss_offsets = rng.integers(0, 365, size=claim_count)
    report_lag_days = np.clip(rng.poisson(2.2, size=claim_count) + rng.binomial(1, 0.15, size=claim_count) * 5, 0, 18)
    loss_dates = start_date + loss_offsets.astype("timedelta64[D]")
    report_dates = loss_dates + report_lag_days.astype("timedelta64[D]")

    claim_type = [
        _sample_claim_type(rng, tier, prior_count)
        for tier, prior_count in zip(sampled_policies["nonstandard_risk_tier"], sampled_policies["prior_claim_count"])
    ]
    claim_type = np.array(claim_type)

    injury_probability = (
        0.12
        + 0.23 * np.isin(claim_type, ["rear_end_bi", "side_impact_bi", "mixed_injury"])
        + 0.04 * (sampled_policies["nonstandard_risk_tier"].isin(["tier_3", "tier_4"]).astype(int))
        + 0.03 * (sampled_policies["prior_claim_count"] >= 2).astype(int)
    )
    injury_flag = rng.binomial(1, np.clip(injury_probability, 0.05, 0.72))

    attorney_probability = 0.06 + 0.24 * injury_flag + 0.03 * (report_lag_days >= 5) + 0.04 * (
        sampled_policies["nonstandard_risk_tier"] == "tier_4"
    ).astype(int)
    attorney_rep_flag = rng.binomial(1, np.clip(attorney_probability, 0.03, 0.68))

    bodily_injury_probability = 0.05 + 0.34 * injury_flag + 0.1 * attorney_rep_flag + 0.08 * np.isin(
        claim_type, ["rear_end_bi", "side_impact_bi", "mixed_injury"]
    )
    bodily_injury_flag = rng.binomial(1, np.clip(bodily_injury_probability, 0.02, 0.84))

    liability_decision = rng.choice(
        LIABILITY_DECISIONS,
        size=claim_count,
        p=[0.46, 0.18, 0.19, 0.17],
    )

    severity_index = (
        1500
        + 4200 * bodily_injury_flag
        + 2800 * attorney_rep_flag
        + 900 * injury_flag
        + 650 * (report_lag_days >= 5)
        + 500 * (sampled_policies["prior_claim_count"])
        + 750 * np.isin(claim_type, ["rear_end_bi", "side_impact_bi", "mixed_injury"])
        + np.where(sampled_policies["coverage_limit_bi"] >= 50000, 700, 0)
    )
    paid_amount = np.clip(rng.gamma(shape=2.2, scale=severity_index / 2.4), 150, None)
    reserve_multiplier = 0.18 + 0.38 * (1 - rng.binomial(1, 0.58, size=claim_count)) + 0.22 * bodily_injury_flag
    reserve_amount = np.clip(paid_amount * reserve_multiplier + rng.normal(400, 250, size=claim_count), 0, None)
    closed_probability = 0.74 - 0.26 * bodily_injury_flag - 0.14 * attorney_rep_flag
    closed_flag = rng.binomial(1, np.clip(closed_probability, 0.18, 0.9))
    days_to_close = np.clip(
        rng.normal(
            36 + 58 * bodily_injury_flag + 32 * attorney_rep_flag + 3 * report_lag_days,
            18,
            size=claim_count,
        ),
        5,
        360,
    ).round().astype(int)
    days_to_close = np.where(closed_flag == 0, np.maximum(days_to_close, 60), days_to_close)

    claims = pd.DataFrame(
        {
            "claim_id": claim_ids,
            "policy_id": sampled_policies["policy_id"].values,
            "claimant_id": claimant_ids,
            "loss_date": pd.to_datetime(loss_dates),
            "report_date": pd.to_datetime(report_dates),
            "state": sampled_policies["policy_state"].values,
            "claim_type": claim_type,
            "injury_flag": injury_flag,
            "attorney_rep_flag": attorney_rep_flag,
            "bodily_injury_flag": bodily_injury_flag,
            "liability_decision": liability_decision,
            "reserve_amount": np.round(reserve_amount, 2),
            "paid_amount": np.round(paid_amount, 2),
            "closed_flag": closed_flag,
            "days_to_close": days_to_close,
        }
    )

    reporting_channel = rng.choice(REPORTING_CHANNELS, size=claim_count, p=[0.44, 0.18, 0.16, 0.22])
    police_report_flag = rng.binomial(1, np.clip(0.22 + 0.18 * bodily_injury_flag + 0.08 * injury_flag, 0.05, 0.78))
    witness_flag = rng.binomial(1, np.clip(0.16 + 0.14 * bodily_injury_flag + 0.06 * (claim_type == "side_impact_bi"), 0.03, 0.7))
    injury_reported_at_fnol = rng.binomial(1, np.clip(0.08 + 0.58 * bodily_injury_flag + 0.18 * injury_flag, 0.02, 0.95))
    fnol = pd.DataFrame(
        {
            "fnol_id": [f"FNOL{300000 + idx}" for idx in range(claim_count)],
            "claim_id": claim_ids,
            "reporting_channel": reporting_channel,
            "description_of_loss": [
                f"{impact.replace('_', ' ')} accident with {weather.replace('_', ' ')} conditions"
                for impact, weather in zip(
                    rng.choice(POINTS_OF_IMPACT, size=claim_count),
                    rng.choice(WEATHER_CONDITIONS, size=claim_count),
                )
            ],
            "police_report_flag": police_report_flag,
            "witness_flag": witness_flag,
            "loss_location": rng.choice(LOSS_LOCATIONS, size=claim_count, p=[0.24, 0.2, 0.18, 0.16, 0.22]),
            "weather_condition": rng.choice(WEATHER_CONDITIONS, size=claim_count, p=[0.41, 0.24, 0.08, 0.07, 0.2]),
            "point_of_impact": rng.choice(POINTS_OF_IMPACT, size=claim_count, p=[0.37, 0.18, 0.16, 0.17, 0.12]),
            "injury_reported_at_fnol": injury_reported_at_fnol,
        }
    )

    message_records: list[dict[str, object]] = []
    for claim_row in claims.itertuples(index=False):
        expected_messages = 2 + claim_row.bodily_injury_flag * 3 + claim_row.attorney_rep_flag * 2 + int(not claim_row.closed_flag)
        message_count = int(np.clip(rng.poisson(expected_messages), 1, 12))
        base_sentiment = -0.05 - 0.18 * claim_row.attorney_rep_flag - 0.14 * claim_row.bodily_injury_flag + 0.08 * claim_row.closed_flag
        for msg_idx in range(message_count):
            sender_weights = np.array(
                [0.34, 0.38, 0.2, 0.08 + 0.12 * claim_row.attorney_rep_flag],
                dtype=float,
            )
            sender_weights = sender_weights / sender_weights.sum()
            sender_type = rng.choice(
                ["claimant", "adjuster", "insured", "attorney"],
                p=sender_weights,
            )
            sentiment = float(np.clip(rng.normal(base_sentiment, 0.28), -1, 1))
            latency = float(
                np.clip(
                    rng.gamma(
                        shape=2.0,
                        scale=40 + 16 * claim_row.bodily_injury_flag + 18 * claim_row.attorney_rep_flag,
                    ),
                    3,
                    1200,
                )
            )
            escalation_prob = 0.05 + 0.14 * claim_row.attorney_rep_flag + 0.12 * claim_row.bodily_injury_flag + 0.08 * (sentiment < -0.35)
            message_records.append(
                {
                    "message_id": f"MSG{claim_row.claim_id[-4:]}{msg_idx:02d}",
                    "claim_id": claim_row.claim_id,
                    "message_timestamp": claim_row.report_date + pd.to_timedelta(rng.integers(0, 40), unit="D") + pd.to_timedelta(rng.integers(0, 1440), unit="m"),
                    "sender_type": sender_type,
                    "sentiment_score": round(sentiment, 3),
                    "response_latency_minutes": round(latency, 1),
                    "escalation_flag": int(rng.binomial(1, np.clip(escalation_prob, 0.01, 0.8))),
                }
            )
    messages = pd.DataFrame(message_records)

    for frame in (claims, fnol, messages, policy):
        if rng.random() < 0.9:
            sample_size = max(1, int(len(frame) * 0.01))
            column = rng.choice([col for col in frame.columns if col not in {"claim_id", "policy_id", "fnol_id", "message_id"}])
            frame.loc[frame.sample(sample_size, random_state=random_seed).index, column] = np.nan

    return SyntheticDataBundle(claims=claims, fnol=fnol, messages=messages, policy=policy)


def save_synthetic_datasets(bundle: SyntheticDataBundle) -> None:
    ensure_directories([CLAIMS_FILE.parent])
    bundle.claims.to_csv(CLAIMS_FILE, index=False)
    bundle.fnol.to_csv(FNOL_FILE, index=False)
    bundle.messages.to_csv(MESSAGES_FILE, index=False)
    bundle.policy.to_csv(POLICY_FILE, index=False)


def main() -> None:
    data_bundle = generate_synthetic_insurance_data()
    save_synthetic_datasets(data_bundle)


if __name__ == "__main__":
    main()
