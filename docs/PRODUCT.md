# Rental History Evidence Report — Product Spec (MVP)

## Overview

A tool that helps renters generate a **bank-verified rental history report** to support rental applications.

This product does NOT replace credit checks or landlord screening systems. It is a **supplementary evidence artifact** for applicants who want to demonstrate rental reliability using transaction history.

---

## Core Use Case

This product is for renters who:

- have weak or thin credit history
- lack strong traditional documentation
- are confident in their rental reliability
- want to strengthen a rental application with behavioral proof

---

## Primary Value Proposition

> Turn historical bank transactions into a structured, shareable rental history report.

---

## Output

A renter-owned report containing:

- Confirmed rent payment streams (tenant-verified from bank data)
- Payment history timeline (confirmed payments only)
- Coverage period (spans full detected stream)
- Gaps in detected payment cadence (always shown — not suppressible by tenant)
- User annotations (clearly separated from detected data)
- Shareable link + optional PDF export

Sharing constraint:
> A stream must be fully reviewed before sharing. If review is incomplete, the report discloses this.

---

## Non-Goals

- No credit scoring system
- No landlord network
- No rental marketplace
- No authoritative lease verification
- No attempt to define legal tenancy truth

---

## Key Principle

> The system does not assert legal truth. It summarizes financial behavior related to rent-like payments.