# MVP Implementation Plan

## Project Structure

```
cresidential/
├── backend/
│   ├── pyproject.toml
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── routers/
│   │   │   ├── plaid.py
│   │   │   └── transactions.py
│   │   └── services/
│   │       ├── plaid_service.py
│   │       └── detection_service.py
├── frontend/
│   ├── package.json
│   ├── vite.config.ts
│   └── src/
│       ├── App.tsx
│       ├── components/
│       │   ├── ConnectBank.tsx
│       │   ├── Analyzing.tsx
│       │   └── CandidateList.tsx
│       └── api/
│           └── client.ts
├── .env
├── .gitignore
└── docs/
```

---

## Backend

### Setup

```bash
cd backend
poetry init
poetry add fastapi uvicorn plaid-python python-dotenv
```

### Environment variables (root `.env`)

```
PLAID_CLIENT_ID=
PLAID_SANDBOX_SECRET_KEY=
PLAID_ENV=sandbox
```

### Session model

Access tokens never leave the server. On token exchange, the backend:

1. Exchanges `public_token` for `access_token` via Plaid API
2. Stores `access_token` in an in-memory dict: `{ session_id: access_token }`
3. Returns only `session_id` (UUID) to the frontend

All subsequent calls pass `session_id`. The backend looks up the access token internally.

---

### API Endpoints

#### `POST /plaid/create-link-token`

Creates a Plaid Link token to initialize the Link flow on the frontend.

**Response:**
```json
{ "link_token": "string" }
```

---

#### `POST /plaid/exchange-token`

Exchanges Plaid `public_token` for an `access_token`. Stores access token server-side.

**Request:**
```json
{ "public_token": "string" }
```

**Response:**
```json
{ "session_id": "uuid" }
```

---

#### `POST /transactions/analyze`

Fetches 24 months of transactions for the session and runs detection.

**Request:**
```json
{ "session_id": "uuid" }
```

**Response:**
```json
{
  "period": { "start": "YYYY-MM-DD", "end": "YYYY-MM-DD" },
  "total_transactions_analyzed": 0,
  "candidates": [
    {
      "description": "string",
      "amount_range": [0.0, 0.0],
      "typical_amount": 0.0,
      "first_payment": "YYYY-MM-DD",
      "last_payment": "YYYY-MM-DD",
      "occurrences": 0,
      "cadence": "monthly | irregular",
      "confidence_score": 0.0,
      "transactions": []
    }
  ]
}
```

---

### Detection Service

**Input:** list of normalized transactions (date, amount, description)

**Pipeline:**

1. **Filter outflows** — keep only debits above a minimum threshold (e.g. $200)

2. **Cluster by description** — fuzzy-match payee strings into groups using token overlap or edit distance; transactions with similar descriptions are treated as the same payee

3. **Score each cluster:**

   | Signal | Method |
   |--------|--------|
   | Cadence | Compute intervals between payments; score higher if intervals cluster near 28–31 days |
   | Amount stability | Coefficient of variation of payment amounts; lower variance = higher score |
   | Streak length | Count consecutive months with a payment; minimum 3 to qualify |
   | Magnitude | Flag amounts below $200 as unlikely rent |

4. **Combine signals** into a `confidence_score` (0.0–1.0)

5. **Filter** clusters with streak < 3 or confidence < 0.2

6. **Sort** by confidence descending

---

## Frontend

### Setup

```bash
cd frontend
npm create vite@latest . -- --template react-ts
npm install react-plaid-link axios
```

### Flow

```
App
 └── ConnectBank      → Plaid Link button, calls /plaid/create-link-token on mount
      ↓ on success
     Analyzing        → calls /transactions/analyze with session_id, shows spinner
      ↓ on result
     CandidateList    → renders list of RentCandidate objects
```

### State machine

```
idle → connecting → analyzing → results | error
```

### Plaid Link integration

- Use `react-plaid-link` (`usePlaidLink` hook)
- Fetch link token from backend on component mount
- On `onSuccess(public_token)` → POST to `/plaid/exchange-token` → store `session_id` in React state
- Immediately trigger `/transactions/analyze` with `session_id`

---

## Build Order

1. Backend scaffold — FastAPI app, config, health check endpoint
2. Plaid link token endpoint — verify Plaid credentials work
3. Token exchange endpoint — complete Link flow end-to-end in sandbox
4. Transaction fetch — pull raw transactions, log to verify data shape
5. Detection service — implement and unit test against sandbox data
6. Analyze endpoint — wire detection service to API
7. Frontend scaffold — Vite + React, proxy config to backend
8. Connect flow — Plaid Link integration
9. Results display — CandidateList component
10. End-to-end test in sandbox

---

## Notes

- Plaid sandbox provides test credentials (`user_good` / `pass_good`) and synthetic transaction data
- Access token storage is in-memory only — server restart clears all sessions (acceptable for MVP)
- No authentication in MVP — endpoints are open
- CORS configured for `localhost:5173` (Vite default) in development

## Known Security Gaps

**session_id does not provide meaningful access control.**
The session_id protects the Plaid access token from being exposed in the browser, but any caller who obtains a valid session_id can call `/transactions/analyze` and retrieve the associated transaction data. Within this system, a session_id is functionally equivalent to the access token it represents — only Plaid itself is protected.

The correct fix is user authentication: access tokens are stored against authenticated user records, and all endpoints require a verified session. This eliminates the need for the session_id indirection entirely.

This gap is accepted for the MVP (sandbox, single-user, no real financial data). It must be resolved before any production deployment.
