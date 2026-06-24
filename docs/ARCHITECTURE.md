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

* Connect bank accounts
* Retrieve transaction history
* Normalize transaction data

---

### 5. Payment Matching Engine

Matches observed transactions against expected lease obligations.

Inputs:

* LeaseRecord
* TransactionHistory

Outputs:

* Verified payments
* Missing expected payments
* Late payments
* Unmatched payments

---

### 6. Report Generation Layer

Produces:

* Lease summary
* Payment verification summary
* Landlord verification summary

---

## Account Model

Two account types:

**TenantAccount** — requests reports, connects Plaid
**LandlordAccount** — sends verification requests, verifies tenancy, views applicant reports

A user may hold both. Reports belong to a `LandlordTenantRelationship`, not to either party alone. A relationship only exists if both parties have accounts. One-time (no-account) flows are ephemeral.

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
* matched_transaction_id
* status (verified | missing | late | partial)

### RentalVerificationReport

* id
* relationship_id
* lease_record_id
* verification_summary
* generated_at
* superseded_by (report_id, nullable — set when regenerated after correction)

---

## Trust Model

Landlord supplies lease obligations.

Bank transactions verify payment behavior.

The system never infers lease terms from transaction data when verified lease information is available.
