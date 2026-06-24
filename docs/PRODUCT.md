# Rental Verification Report — Product Spec

## Overview

A system that transforms traditional landlord references into structured tenancy verification reports.

Instead of asking a previous landlord for a subjective reference, renters invite previous landlords to verify objective tenancy details. The renter may then connect their bank accounts via Plaid to verify payment behavior against the confirmed lease information.

The result is a portable rental verification report that combines:

* Landlord-confirmed lease information
* Bank-verified payment history
* Structured tenancy records

---

## Problem

Traditional landlord references are weak signals.

Landlords frequently report that:

* References are overwhelmingly positive
* References are difficult to verify
* Information is inconsistent across landlords
* Valuable tenant history is not portable

A reliable tenant receives little benefit from years of good rental behavior.

---

## Core Value Proposition

> Replace subjective landlord references with structured tenancy verification and payment validation.

---

## Primary User

Renters who:

* Have a strong rental history
* Want to strengthen a rental application
* Want a portable record of prior tenancy

---

## How It Works

### Step 1

Tenant provides previous landlord contact information to the prospective landlord.

### Step 2

**Prospective landlord** sends the verification link to the previous landlord.

Previous landlord confirms:

* Tenant identity
* Property address
* Lease start date
* Lease end date
* Monthly rent amount
* Rent due day
* Good standing status

Response is locked on submission. Corrections require a manual review request to our team.

### Step 3

Tenant connects bank accounts via Plaid.

### Step 4

System verifies observed payments against expected lease obligations from the confirmed lease record.

### Step 5

System generates the Rental Verification Report, scoped to the prospective landlord–tenant relationship.

---

## Account Model

Two distinct account types:

**Tenant account**
* Request verification reports
* Connect bank accounts via Plaid
* Share reports with prospective landlords

**Landlord account**
* Receive and send verification requests
* Verify tenancy details for current and former tenants
* View reports for their own applicants

A user may hold both account types. Reports belong to the landlord–tenant relationship, not to either party individually. A relationship only persists if both parties have accounts. One-time flows (no account) are ephemeral — the report is consumed and not retained.

---

## Corrections

If a previous landlord submits incorrect lease details:

* They submit a correction request
* Our team reviews manually
* Prospective landlord is notified that a correction is pending
* If approved, the report is regenerated from the corrected lease record
* The original report is preserved in our records for audit purposes

---

## Report Contents

### Lease Verification

* Property
* Lease period
* Monthly rent
* Due day

### Payment Verification

* Expected payment cycles
* Verified payment cycles
* Missing payment cycles
* Payment consistency metrics

### Landlord Verification

* Confirmation of tenancy
* Good standing status

---

## Non-Goals

* Tenant scoring
* Social reputation systems
* Credit replacement
* Public reputation profiles
* Lease inference from transactions alone

---

## Key Principle

> Lease facts come from the landlord. Payment verification comes from bank data.
