# Data Dictionary

## Claims Dataset

| Column | Description |
| --- | --- |
| `claim_id` | Unique claim identifier from Guidewire-style claims extract |
| `policy_id` | Policy identifier linked to claim |
| `claimant_id` | Synthetic claimant identifier |
| `loss_date` | Date of loss |
| `report_date` | Date claim was reported |
| `state` | Claim state / jurisdiction |
| `claim_type` | High-level claim type such as collision, BI liability, or mixed damage |
| `injury_flag` | Indicates any injury involvement |
| `attorney_rep_flag` | Indicates claimant attorney representation |
| `bodily_injury_flag` | Indicates BI exposure on the claim |
| `liability_decision` | Simplified liability determination |
| `reserve_amount` | Remaining case reserve amount |
| `paid_amount` | Paid indemnity and expense proxy |
| `closed_flag` | Indicates claim closure |
| `days_to_close` | Days between report and closure for closed claims or projected duration proxy |

## FNOL Dataset

| Column | Description |
| --- | --- |
| `fnol_id` | Unique FNOL identifier |
| `claim_id` | Claim identifier |
| `reporting_channel` | Intake channel such as phone, app, web, or agent |
| `description_of_loss` | Synthetic short-form loss description |
| `police_report_flag` | Police report indicator |
| `witness_flag` | Witness involvement indicator |
| `loss_location` | Location context such as urban arterial, highway, or parking lot |
| `weather_condition` | Weather at time of loss |
| `point_of_impact` | Point of impact such as rear-end or side impact |
| `injury_reported_at_fnol` | Injury indicated during first notice |

## Communications Dataset

| Column | Description |
| --- | --- |
| `message_id` | Unique message identifier |
| `claim_id` | Claim identifier |
| `message_timestamp` | Timestamp of communication event |
| `sender_type` | Message sender such as claimant, adjuster, insured, or attorney |
| `sentiment_score` | Synthetic sentiment score from -1 to 1 |
| `response_latency_minutes` | Approximate response delay |
| `escalation_flag` | Indicates escalated or high-friction communication |

## Policy / Exposure Dataset

| Column | Description |
| --- | --- |
| `policy_id` | Unique policy identifier |
| `policy_state` | Policy state |
| `vehicle_count` | Number of vehicles on policy |
| `driver_count` | Number of rated drivers |
| `prior_claim_count` | Prior claims history count |
| `coverage_limit_bi` | Bodily injury liability limit |
| `coverage_limit_pd` | Property damage limit |
| `premium_amount` | Written premium proxy |
| `nonstandard_risk_tier` | Non-standard segment tier |

## Engineered Features

The analytical base table also includes engineered fields such as:

- `report_lag_days`
- `message_count`
- `avg_sentiment_score`
- `avg_response_latency_minutes`
- `message_escalation_rate`
- `claimant_message_share`
- `total_incurred`
- `paid_to_reserve_ratio`
- `coverage_per_driver`
- `exposure_complexity_index`
- `early_injury_signal`

