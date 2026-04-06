# Architecture Overview

## Objective

The repository simulates a claims analytics architecture for a non-standard auto insurer where operational data generated through claims handling can be repurposed for actuarial analysis, supervisory reporting, and predictive modeling.

## System Roles

### Guidewire ClaimCenter

Guidewire serves as the **claims system of record**. It holds:

- claim identifiers
- policy linkage
- core claim dates
- injury and liability indicators
- reserve and paid amounts
- closure status

In this project, the claims table represents a curated Guidewire-style extract used for downstream analytics.

### FNOL Intake Workflow

FNOL data captures the earliest structured description of the loss event. It is modeled as an intake layer that sits upstream of formal claim development. FNOL contributes:

- how the loss was reported
- whether police or witnesses were involved
- early injury reporting
- contextual signals such as weather and point of impact

This information is useful for triage because it is available before substantial claim development occurs.

### Hi Marley-Style Messaging Layer

Messaging data is modeled as a separate operational stream that records communication patterns between claimants, insureds, and claims staff. These signals are not usually part of a core actuarial dataset, but they can reveal:

- responsiveness friction
- customer stress or dissatisfaction
- escalation risk
- handling complexity

The project aggregates message-level activity into claim-level communication features.

## Data Flow

1. Synthetic operational extracts are generated for claims, FNOL, messaging, and policy exposure.
2. Raw datasets are validated during ingestion.
3. Cleaning logic standardizes dates, booleans, categorical values, and missing fields.
4. Feature engineering joins claim-centric and policy-centric records into an analytical base table.
5. SQL examples demonstrate KPI, triage, and reserve monitoring use cases.
6. Modeling modules train regression and classification workflows on the analytical base table.
7. Evaluation output is persisted for portfolio review and reproducibility.

## Analytical Design Principles

- **Claim-centric grain**: the final analytical table is one row per claim.
- **Operational realism**: inputs resemble what a claims analytics team could realistically extract from production systems.
- **Business-first features**: engineered fields are chosen to support triage, severity monitoring, and bodily injury exposure assessment.
- **Modularity**: generation, ingestion, cleaning, features, and modeling are separated into focused modules.

## End-State Outputs

The architecture supports several common insurance analytics consumers:

- adjusters reviewing new losses
- supervisors monitoring case mix
- actuaries studying severity and reserve adequacy proxies
- claims leadership reviewing operational KPIs and segmentation outputs

