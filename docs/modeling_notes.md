# Modeling Notes

## Modeling Objective

The project includes two predictive workflows that reflect common claims and actuarial use cases in a non-standard auto environment:

- claim severity regression
- bodily injury exposure classification

The intent is to show how operational claims data can be translated into actionable modeling features, not to present a production-calibrated pricing or reserving model.

## Feature Design Philosophy

Features are built to reflect business meaning:

- **Claim development context**: injury indicators, attorney representation, liability decisions, days to close
- **FNOL intake quality**: reporting lag, police report flag, witness flag, injury reported at FNOL, reporting channel
- **Communication friction**: sentiment, response latency, escalation rate, claimant and attorney message share
- **Exposure context**: vehicle count, driver count, prior claims, coverage limits, premium, non-standard tier

These features are suitable for demonstrating how operational and actuarial perspectives can be combined in a claim-level analytical base table.

## Severity Model

### Target

`total_incurred = paid_amount + reserve_amount`

### Why It Matters

Total incurred is a practical severity proxy for triage and reserve monitoring. In a real insurer, the target might be modeled at multiple maturities or paired with reserve adequacy analysis.

### Business Interpretation

Severity should increase when claims show combinations such as:

- bodily injury involvement
- attorney representation
- longer reporting lag
- higher policy limits
- communication escalation
- prior claim history and more complex risk tiers

## Bodily Injury Exposure Model

### Target

`bodily_injury_flag`

### Why It Matters

Early BI identification can improve routing, case management, and supervisor oversight. BI claims are often more volatile and operationally sensitive than property-damage-only claims.

### Business Interpretation

The BI model is expected to respond to:

- injury reported at FNOL
- attorney involvement
- point of impact and witness information
- adverse communication behavior
- higher-risk non-standard segments

## Limitations

- Synthetic data generation embeds relationships intentionally, so model performance is partly driven by designed structure.
- No hyperparameter tuning or cross-validation is included because the portfolio focus is on end-to-end project design.
- No text modeling is applied to loss descriptions.
- No formal explainability library is used; interpretation is documented from a business perspective.

## Reviewer Notes

For technical reviewers, the strongest signals in this project are:

- coherent insurance-specific feature engineering
- modular pipeline design
- clear connection between claim operations and model targets
- reproducible local execution

