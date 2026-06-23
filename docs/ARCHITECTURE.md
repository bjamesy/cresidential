# Rental Evidence Report System — Architecture

## System Overview

The system extracts and summarizes **rent-like financial behavior** from bank transaction data using Plaid, then allows user verification to produce a structured rental history report.

---

## High-Level Flow

Plaid Bank Data
↓
Transaction Ingestion Layer
↓
Recurring Payment Detection Engine
↓
Rent Stream Candidate Generation
↓
User Confirmation & Annotation Layer
↓
Rental Evidence Report Generator


---

## Core Components

### 1. Bank Data Layer (Plaid)

- Connect user bank accounts
- Retrieve transaction history (24–60 months)
- Normalize transaction data

---

### 2. Transaction Processing Layer

Standardize:
- date
- amount
- description

No semantic assumptions beyond normalization.

---

### 3. Recurring Detection Engine (Heuristic v1)

Detect recurring outflows using:

- cadence detection (monthly/biweekly patterns)
- amount stability thresholds
- recurrence streak length
- description similarity clustering

Output:
- candidate recurring payment streams with inferred cadence

Cadence rules:
- Cadence is computed from the full detected stream
- Cadence becomes immutable once the tenant confirms the stream
- Tenant cannot influence cadence inference at any point

---

### 4. Rent Stream Identification Layer

System proposes:
- “likely rent streams”

NOT definitive classification.

User confirms:
- “this is rent”
- or rejects/adjusts stream

Sharing constraint:
- A stream must be fully reviewed before the report can be shared
- If review is incomplete, the report discloses this explicitly

---

### 5. User Annotation Layer

Users may:
- label rent streams
- merge split payments
- correct misclassified transactions
- annotate gaps (context only, non-authoritative)

Constraints:
> User annotations do not override detected financial events.
> User cannot alter timing metrics, cadence, or coverage period.
> Unconfirmed payments do not appear in the shared report, but their absence creates gaps.

---

### 6. Report Generation Layer

Produces:

- timeline of confirmed rent-like payments
- coverage period (spans full detected stream, not just confirmed subset)
- gaps (breaks in detected cadence — always shown, not suppressible)
- user annotations (clearly separated from detected data)

Gap definition:
- A gap is triggered by a break in the detected payment cadence
- Calendar-month gaps are NOT used — cadence-break gaps are

---

## Data Model (Core Entities)

- User
- BankConnection
- Transaction
- RecurringStreamCandidate
- ConfirmedRentStream
- RentalEvidenceReport

---

## Key Design Constraint

> The system only asserts what is directly observed in bank data. All interpretation is probabilistic and explicitly labeled.