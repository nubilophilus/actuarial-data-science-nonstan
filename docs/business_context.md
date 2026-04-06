# Business Context

## Non-Standard Auto Carrier Environment

Non-standard auto insurers generally serve drivers with less stable risk characteristics than preferred auto carriers. This can include prior violations, thinner credit files, coverage affordability constraints, prior loss history, lapses in insurance, or other indicators associated with elevated claim frequency and more volatile severity.

That operating environment makes claims analytics especially valuable. Early signals from intake, communications, and policy history can help the organization allocate adjuster attention, monitor potential bodily injury exposure, and support reserving decisions.

## What FNOL Means In Claims Operations

**FNOL** stands for **First Notice of Loss**. It is the first formal report that a loss event has occurred. FNOL is operationally important because it is the earliest point where the insurer captures:

- what happened
- when and where it happened
- whether injuries were reported
- whether police or witnesses were involved
- how the loss was reported

For a non-standard auto carrier, FNOL quality and speed can materially affect downstream claim handling. Claims reported late or through channels with incomplete information may require more follow-up and can carry more uncertainty.

## How Guidewire Fits Into The Workflow

Guidewire is modeled as the core claims platform and system of record. Once a claim is established, Guidewire stores the official claim number, policy linkage, coverage context, reserve amounts, payments, closure status, and liability decisions.

In practice, actuarial and analytics teams often consume curated Guidewire extracts rather than querying transactional claims tables directly. This project mirrors that pattern by treating the claims dataset as a structured Guidewire-style downstream extract used for reporting and modeling.

## How Hi Marley Data Can Enrich Claims Analytics

Hi Marley-style communication data adds operational behavior that usually sits outside traditional actuarial triangles or summary claim tables. Message activity can reveal:

- customer frustration or negative sentiment
- delayed responses
- repeated escalations
- unusually heavy touch patterns between adjusters and claimants

Those signals can enrich claims analytics because they can act as leading indicators of handling complexity, dissatisfaction, attorney involvement risk, or claim escalation. Even when they do not directly drive severity, they can improve triage and operational segmentation.

## Why Bodily Injury Claims Matter For Severity And Reserving

Bodily injury claims are especially important because they are often more severe, less predictable, and more sensitive to legal representation, liability disputes, and treatment development than property-damage-only claims.

For actuarial and claims teams, bodily injury exposure matters because it can affect:

- reserve adequacy
- expected claim development
- litigation risk
- supervisory escalation needs
- staffing requirements for experienced adjusters

In a non-standard auto book, identifying BI exposure early can improve case routing and help claims leadership focus on the losses most likely to develop adversely.

## How Predictive Modeling Supports Key Stakeholders

### Adjusters

Predictive signals can help adjusters prioritize new losses, identify claims that may require early contact, and recognize combinations of injury, attorney representation, or communication escalation that warrant closer review.

### Supervisors

Supervisors can use severity and BI exposure scores to segment inventories, manage workload, and route complex claims to more experienced handlers.

### Actuaries

Actuaries can use the integrated dataset to study claim severity patterns, link operational claim characteristics to loss outcomes, and evaluate whether certain early indicators align with reserve development risk.

### Claims Leadership

Claims executives and operational leaders can use the outputs for monitoring, triage design, KPI reporting, and strategy decisions around staffing, intake quality, and communication workflows.

