# Rental Verification Report — Architecture

## System Overview

The platform combines:

1. Landlord-provided lease data
2. Plaid transaction data
3. Verification logic

to produce structured rental verification reports.

---

## High-Level Flow

Tenant provides previous landlord contact info to prospective landlord
↓
Prospective landlord sends verification link to previous landlord
↓
Previous landlord submits lease details → LeaseRecord (locked on submission)
↓
Tenant connects Plaid bank account
↓
Payment Matching Engine (transactions vs. LeaseRecord obligations)
↓
Rental Verification Report (scoped to prospective landlord–tenant relationship)

---

## Core Components

### 1. Tenant Application Layer

Responsibilities:

* Collect landlord contact information
* Manage report generation requests
* Manage sharing permissions

---

### 2. Landlord Verification Layer

Responsibilities:

* Verify tenancy
* Provide lease metadata
* Confirm good standing status

Required fields:

* Tenant name
* Property address
* Lease start date
* Lease end date
* Monthly rent amount
* Due day
* Current or former tenancy status

---

### 3. Lease Record Service

Creates canonical lease records.

Example:

LeaseRecord

* lease_start
* lease_end
* monthly_rent
* due_day
* landlord_verification_timestamp

This becomes the source of truth for expected payment obligations.

---

### 4. Plaid Integration Layer

Responsibilities:

* Connect bank accounts one at a time
* Fetch transaction history once per account and store it
* Normalize transaction data

Stored transaction data is used for all future report generations and regenerations — no re-fetching from Plaid after initial connection.

Report access:

* Accessible to the landlord account that initiated the request only
* Tenant does not have access to the generated report
* Report access is locked to the initiating account

---

### 5. Payment Matching Engine

Matches observed transactions against expected lease obligations.

Inputs:

* LeaseRecord
* TransactionHistory (one or more bank accounts, scoped to lease period only)

Matching rules:

* Primary signal: amount proximity to expected rent + due date proximity
* Match window: 1 month (due date N to due date N+1)
* Secondary signal: recipient identifier (system-detected, not tenant-provided)
* Low-confidence matches → automated resolution → manual fallback if unresolved
* Tenant does not participate in match resolution
* If duplicate match found across accounts → highest confidence match wins, duplicate flagged
* Transactions outside the lease period are ignored

Final month rule:
* Final month payment expected unless a double-rent payment is detected before lease start
* System detects prepayment automatically — no landlord input required

Outputs per payment period:

* due_date
* matched_transaction (date, amount) or null
* status: verified | unverified | gap

No lateness classification — system reports due date and payment date only.

---

### 6. Report Generation Layer

Produces a single chronological timeline interleaving expected due dates and observed payments.

Sections:

* Lease Verification (property, period, rent, due day)
* Payment Timeline (due dates + matched payments interleaved; gaps shown, not interpreted)
* Landlord Verification (confirmed tenancy, good standing)

The system presents facts. The prospective landlord interprets them.

---

## Account Model

Two account types:

**TenantAccount** — requests reports, connects Plaid
**LandlordAccount** — sends verification requests, verifies tenancy, views applicant reports

A user may hold both. Reports belong to a `LandlordTenantRelationship`, not to either party alone. A relationship only exists if both parties have accounts. One-time (no-account) flows are ephemeral.

Account deletion: accounts are deactivated with a flag, not deleted. Associated reports and relationships are retained but access is revoked.

---

## Data Model

### User

* id
* email
* account_type (tenant | landlord | both)

### LandlordTenantRelationship

* id
* landlord_account_id
* tenant_account_id
* status

### LandlordVerificationRequest

* id
* relationship_id
* previous_landlord_email
* sent_by (prospective_landlord_account_id)
* status

### LeaseRecord

* id
* verification_request_id
* property_address
* lease_start
* lease_end
* monthly_rent
* due_day
* submitted_at
* locked (bool)

### LeaseRecordCorrection

* id
* lease_record_id
* requested_at
* reviewed_at
* status
* original_snapshot (preserved for audit)

### Transaction

* id
* date
* amount
* description

### PaymentVerification

* expected_payment_date
* matched_transaction_id (nullable)
* matched_amount (nullable)
* status (verified | unverified | gap)

### RentalVerificationReport

* id
* relationship_id
* lease_record_id
* generated_at
* superseded_by (report_id, nullable — set when regenerated after correction)

Report lifecycle:
* Report and its history persist independently of the relationship
* Each relationship has its own report history
* A report request is always scoped to a specific landlord–tenant relationship
* On LeaseRecord correction approval, report is regenerated within the relationship's history
* Original report is retained (via superseded_by chain) for audit

---

## Trust Model

Landlord supplies lease obligations.

Bank transactions verify payment behavior.

The system never infers lease terms from transaction data when verified lease information is available.
