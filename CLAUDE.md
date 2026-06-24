# Rental Verification Report — Claude Implementation Spec

## Objective

Build a platform that converts traditional landlord references into structured tenancy verification reports.

The system combines:

* Landlord-confirmed lease information
* Plaid transaction data
* Payment verification logic

to produce portable rental verification reports.

---

## Core Design Principle

Do not infer lease facts from bank transactions when a landlord verification exists.

Use landlord-confirmed lease records as the authoritative source of expected obligations.

Use Plaid data to verify performance against those obligations.

---

## Functional Modules

### 1. Landlord Verification Module

The **prospective landlord** sends a verification link to the **previous landlord**.

Previous landlord submits:

* Tenant identity
* Property address
* Lease dates
* Monthly rent
* Rent due day
* Good standing status

Constraints:
* Response is locked on submission
* Corrections require a manual review request; our team reviews and approves
* Prospective landlord is notified when a correction request is pending
* On correction approval, report is regenerated; original is preserved for audit

Output: LeaseRecord (immutable after submission)

---

### 2. Plaid Integration Module

Retrieve:

* Transaction history
* Account information

Normalize transactions for matching.

---

### 3. Payment Matching Engine

Input:

* LeaseRecord
* TransactionHistory (one or more bank accounts, scoped to lease period only)

Matching logic:

* Match on amount + due date proximity
* Match window = 1 month (from one due date to the next)
* Amounts shown as-is — no interpretation of partial vs. full payment
* Recipient identifier used as secondary signal; system detects automatically, no tenant input
* Low-confidence matches → automated resolution → manual fallback
* Tenant does not resolve matches
* Duplicate match across accounts → highest confidence wins, duplicate flagged
* Final month payment expected unless double-rent prepayment detected before lease start (system-detected)

Output per payment period:

* due_date
* matched_transaction (date, amount) or null
* status: verified | unverified | gap

No lateness determination — system shows due date and payment date; prospective landlord interprets.

---

### 4. Report Generation Module

Generate RentalVerificationReport as a single chronological timeline interleaving:

* Expected due dates (from LeaseRecord)
* Observed payments (from matched transactions)

Prospective landlord reads the relationship between the two — system does not interpret it.

Report sections:

**Lease Verification**
* Property address
* Lease period
* Monthly rent
* Due day

**Payment Timeline**
* Chronological interleaved list of due dates and matched payments
* Gaps shown where two due dates occur with no intervening match
* Payment amounts shown as-is

**Landlord Verification**
* Confirmed tenancy
* Good standing status

---

## Report Philosophy

The report is not a reputation score.

The report is a structured summary of:

* Verified tenancy
* Verified payment behavior

---

## Success Criteria

* Landlord can complete verification in under 2 minutes
* Tenant can generate report in under 10 minutes
* Lease obligations become machine-readable
* Payment verification can be performed without manual statement review

---

## Trust Model

Source of Truth Hierarchy:

1. Landlord-confirmed lease record
2. Bank transaction data
3. Tenant-provided information

Tenant-provided information may assist onboarding but never overrides landlord-confirmed lease data.
