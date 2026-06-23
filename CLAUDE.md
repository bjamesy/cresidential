# Rental Evidence Report MVP — Claude Build Spec

## Objective

Build a system that extracts and summarizes rent-like financial behavior from bank transaction data and allows user confirmation to produce a rental evidence report.

This is NOT a scoring system or truth system.

It is a **structured financial behavior summary tool for rental applications**.

---

## Core Constraint

Do NOT build:
- credit scoring
- landlord verification network
- legal lease validation
- predictive risk models for eviction or default
- authoritative “on-time rent truth”

Only build:
> behavioral summarization of bank transaction data

---

## System Modules

### 1. Plaid Integration Module

- Connect bank accounts
- Retrieve transaction history
- Normalize transaction data

---

### 2. Recurring Detection Module

Detect candidate rent streams using:

- recurrence cadence detection
- amount consistency analysis
- streak length (minimum 3 occurrences)
- clustering by description similarity

Output:
- recurring payment candidates with confidence scores

---

### 3. User Confirmation Module

User may:
- confirm rent stream
- reject candidate
- merge multiple streams
- annotate missing or unusual payments
- add contextual notes (non-authoritative)

Constraints:
> User input is annotation only, not structural override.
> User cannot influence timing metrics or cadence inference.
> A stream must be fully reviewed before the report can be shared. If review is incomplete, the report must clearly disclose this.

---

### 4. Rental Evidence Report Generator

Generate structured output:

```json
{
  "summary": {
    "detected_rent_streams": [],
    "total_payments": 0,
    "coverage_period": "",
    "consistency_score": null
  },
  "timeline": [],
  "gaps": [],
  "annotations": []
}
```

Coverage and gap rules:
- `coverage_period` spans the full detected stream, not just confirmed payments
- `gaps` = breaks in detected payment cadence (not missed calendar months)
- Cadence is computed from the full detected stream and is immutable once confirmed
- Report shows only tenant-confirmed payments; unconfirmed detections do not appear
- Gaps always appear in the report regardless of tenant annotations