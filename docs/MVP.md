# Rental Verification — MVP Spec

## Objective

Build the core data pipeline: connect a user's bank account via Plaid, fetch 24 months of transactions, and surface likely rent payments using a rules-based detection algorithm.

This MVP does not include landlord verification, report generation, or user confirmation. It is the foundation the full platform will be built on.

---

## Scope

**In scope:**
- Plaid bank connection (one account)
- Transaction fetch (last 24 months)
- Rent payment detection algorithm
- Display of detected rent payment candidates

**Out of scope:**
- Landlord verification
- Lease records
- Payment matching against obligations
- User confirmation or correction
- Report generation or sharing
- Multiple bank accounts

---

## Tech Stack

| Layer    | Technology        |
|----------|-------------------|
| Frontend | React             |
| Backend  | Python / FastAPI  |
| Banking  | Plaid Transactions API |

---

## Plaid Integration

- Use Plaid Link to connect one bank account
- Fetch transactions for the last 24 months
- Normalize each transaction to:
  - `date`
  - `amount` (outflows only)
  - `description` (normalized merchant/payee name)

---

## Detection Algorithm (v1 Rules-Based)

The detection algorithm groups transactions into candidate rent streams and scores them.

### Step 1 — Filter to outflows

Only consider outbound payments (negative amounts / debits).

### Step 2 — Cluster by description similarity

Group transactions with similar payee/description strings. Transactions that cluster together likely share a recipient.

### Step 3 — Score each cluster for rent-like behavior

For each cluster, compute:

| Signal | Description |
|--------|-------------|
| Cadence score | How consistently monthly is the recurrence? |
| Amount stability | How stable is the payment amount across occurrences? |
| Streak length | How many consecutive months does the cluster appear? |
| Magnitude | Is the amount plausible as rent (above a minimum threshold)? |

Minimum qualifying streak: 3 consecutive occurrences.

### Step 4 — Produce candidates

Output a list of `RentCandidate` objects, sorted by confidence score descending.

```
RentCandidate {
  description: str         # clustered payee label
  amount_range: [min, max] # observed payment amounts
  typical_amount: float    # median or modal amount
  first_payment: date
  last_payment: date
  occurrences: int
  cadence: str             # "monthly" | "irregular"
  confidence_score: float  # 0.0 – 1.0
  transactions: list       # raw matched transactions
}
```

---

## API

### `POST /plaid/exchange-token`

Exchange Plaid public token for access token after Link flow completes.

**Request:**
```json
{ "public_token": "string" }
```

**Response:**
```json
{ "access_token": "string" }
```

---

### `POST /transactions/analyze`

Fetch and analyze transactions for a connected account.

**Request:**
```json
{ "access_token": "string" }
```

**Response:**
```json
{
  "period": { "start": "date", "end": "date" },
  "total_transactions_analyzed": 0,
  "candidates": [ RentCandidate ]
}
```

---

## UI

Single-page flow:

1. **Connect bank** — Plaid Link button, user authenticates their bank
2. **Analyzing** — loading state while backend fetches and processes transactions
3. **Results** — raw list of detected rent payment candidates

Each candidate displays:
- Payee / description
- Typical amount
- Date range (first → last payment)
- Number of occurrences
- Confidence score

No editing, confirmation, or interaction with candidates in the MVP.

---

## Success Criteria

- User can connect a bank account and see results in under 2 minutes
- Detection surfaces the correct rent stream in the top result for a straightforward case
- Confidence scores are meaningfully differentiated (not all the same)
- No crashes or unhandled errors on accounts with no rent-like transactions
