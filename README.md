# Non-Standard Auto Claims Analytics for Actuarial Data Science

## Executive Summary

This project demonstrates how a non-standard auto insurer can turn operational claims data into actionable actuarial and claims analytics. It models a realistic environment where Guidewire serves as the claims system of record, FNOL captures early loss details, and Hi Marley-style communications add behavioral and operational signals. The repository combines synthetic insurance data, modular Python pipelines, SQL analytics, and predictive models for claim severity and bodily injury exposure. The result is a portfolio-grade example of how claims operations, analytics engineering, and actuarial decision support can be connected in a single end-to-end workflow.

## Why This Project Matters

Non-standard auto insurers manage portfolios with elevated claim frequency, volatile severity, higher attorney involvement, and more operational complexity than preferred auto books. That makes early claim intelligence valuable. This project shows how a carrier can combine:

- Guidewire claim records as the system of record
- FNOL intake data for early loss context
- Hi Marley-style communications for behavioral and escalation signals
- policy exposure data for underwriting and risk context

The result is a realistic analytical workflow that is relevant to actuarial, claims analytics, and insurance data science roles.

## Business Problem

Claims leaders and actuaries need to identify which claims are most likely to:

- develop into higher severity losses
- involve bodily injury exposure
- require closer supervision or escalated handling
- create reserve uncertainty
- reveal operational friction through intake or communication patterns

This repository demonstrates how to build that capability from synthetic but realistic insurance data.

## What The Repository Includes

- Synthetic Guidewire-style claims, FNOL, communications, and policy datasets
- Modular Python pipeline code for data generation, ingestion, cleaning, and feature engineering
- Regression modeling for claim severity
- Classification modeling for bodily injury exposure
- SQL examples for KPI reporting, FNOL triage, and reserve monitoring
- Documentation for architecture, business context, data dictionary, and modeling assumptions
- Jupyter notebooks for exploratory analysis and modeling walkthroughs
- Smoke tests and a GitHub Actions workflow for basic validation

## Repository Structure

```text
.
├── .github/
│   └── workflows/
│       └── ci.yml
├── data/
│   ├── processed/
│   │   ├── analytical_base_table.csv
│   │   └── model_results.json
│   └── raw/
│       ├── synthetic_claims.csv
│       ├── synthetic_fnol.csv
│       ├── synthetic_messages.csv
│       └── synthetic_policy.csv
├── docs/
│   ├── architecture.md
│   ├── business_context.md
│   ├── data_dictionary.md
│   └── modeling_notes.md
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_modeling_claim_severity.ipynb
│   └── 04_modeling_bi_liability.ipynb
├── sql/
│   ├── claims_kpis.sql
│   ├── fnol_triage.sql
│   └── reserve_monitoring.sql
├── src/
│   ├── __init__.py
│   ├── claims_pipeline.py
│   ├── config.py
│   ├── data_cleaning.py
│   ├── data_generation.py
│   ├── data_ingestion.py
│   ├── evaluation.py
│   ├── feature_engineering.py
│   ├── modeling_liability.py
│   ├── modeling_severity.py
│   └── utils.py
├── tests/
│   └── test_pipeline_smoke.py
├── .gitignore
├── LICENSE
├── Makefile
├── README.md
└── requirements.txt
```

## Architecture Summary

1. `src/data_generation.py` creates synthetic operational datasets representing Guidewire claims, FNOL, Hi Marley-style communications, and policy exposure.
2. `src/data_ingestion.py` loads each dataset and validates schema expectations.
3. `src/data_cleaning.py` standardizes dates, booleans, numeric values, and missing fields.
4. `src/feature_engineering.py` builds a claim-level analytical base table used for modeling and analytics.
5. `src/modeling_severity.py` trains a claim severity model using total incurred as the target.
6. `src/modeling_liability.py` trains a bodily injury exposure model for early classification and triage.
7. `src/claims_pipeline.py` orchestrates the end-to-end workflow and saves processed outputs.

Additional detail is documented in [docs/architecture.md](docs/architecture.md).

## Dataset Overview

The project includes four linked synthetic datasets stored in `data/raw/`:

- `synthetic_claims.csv`: claim-level Guidewire-style records with reserve, paid, liability, and closure information
- `synthetic_fnol.csv`: FNOL loss intake details, including reporting channel, police report status, witness presence, and early injury signals
- `synthetic_messages.csv`: Hi Marley-style communication records with sender type, sentiment, response latency, and escalation flags
- `synthetic_policy.csv`: policy exposure records with vehicles, drivers, prior claims, limits, premium, and non-standard tier

The final analytical base table is claim-grain and joins all four subject areas into a single model-ready dataset.

## Modeling Approach

### Claim Severity Model

Target:

- `total_incurred = paid_amount + reserve_amount`

Business use cases:

- severity triage
- reserve monitoring support
- claim segmentation for supervisor review

Technical approach:

- scikit-learn preprocessing pipeline
- missing value handling and categorical encoding
- `HistGradientBoostingRegressor`
- regression evaluation using MAE, RMSE, and R-squared

### Bodily Injury Exposure Model

Target:

- `bodily_injury_flag`

Business use cases:

- early BI identification
- adjuster routing
- claim escalation monitoring
- severity oversight

Technical approach:

- scikit-learn preprocessing pipeline
- `RandomForestClassifier`
- classification evaluation using accuracy, precision, recall, F1, and ROC AUC

Modeling assumptions and business interpretation are documented in [docs/modeling_notes.md](docs/modeling_notes.md).

## Example Output From A Verified Run

The current repository has been executed locally and produces:

- `data/processed/analytical_base_table.csv`
- `data/processed/model_results.json`

Latest verified test metrics from the local run:

- Severity model test MAE: `3467.49`
- Severity model test RMSE: `5904.26`
- Severity model test R-squared: `0.348`
- BI model test accuracy: `0.901`
- BI model test ROC AUC: `0.956`

These results are based on synthetic data and are intended to demonstrate workflow design and modeling structure rather than production calibration.

## How To Run

### Option 1: Use The Makefile

```bash
make setup
make run
make test
```

### Option 2: Run Manually

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m src.claims_pipeline
```

To open the notebooks:

```bash
.venv/bin/jupyter notebook
```

## Project Outputs

Running the pipeline generates:

- `data/raw/synthetic_claims.csv`
- `data/raw/synthetic_fnol.csv`
- `data/raw/synthetic_messages.csv`
- `data/raw/synthetic_policy.csv`
- `data/processed/analytical_base_table.csv`
- `data/processed/model_results.json`

## Technical Review Guide

For a fast technical review, start here:

1. [docs/business_context.md](docs/business_context.md)
2. [docs/architecture.md](docs/architecture.md)
3. [src/feature_engineering.py](src/feature_engineering.py)
4. [src/modeling_severity.py](src/modeling_severity.py)
5. [src/modeling_liability.py](src/modeling_liability.py)
6. [sql/fnol_triage.sql](sql/fnol_triage.sql)

## Business Relevance For Insurance Analytics Roles

This project is tailored for recruiters, hiring managers, and technical reviewers evaluating actuarial or claims analytics candidates. It demonstrates:

- understanding of claims operations and FNOL workflows
- ability to model realistic insurance entities rather than generic tabular data
- integration of operational and actuarial perspectives
- familiarity with Guidewire-style claims structures
- practical application of predictive modeling to insurance decision support

## Assumptions And Limitations

- All data is synthetic and created for portfolio use.
- Guidewire and Hi Marley structures are simplified into analytics-friendly datasets rather than vendor-native schemas.
- Reserve development is represented as a point-in-time proxy, not a full transaction history.
- The repository focuses on severity and BI exposure modeling, while claim frequency context is represented through policy features and documentation.
- Narrative loss descriptions are included for realism but not modeled with NLP in the current implementation.

## Supporting Documentation

- [docs/business_context.md](docs/business_context.md)
- [docs/architecture.md](docs/architecture.md)
- [docs/data_dictionary.md](docs/data_dictionary.md)
- [docs/modeling_notes.md](docs/modeling_notes.md)

## License

This project is released under the [MIT License](LICENSE).
