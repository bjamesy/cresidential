# Design Blocker: Verifiable Rental Reputation

## Core Product Vision

The purpose of this project is simple:

> Allow reliable tenants to carry years of responsible rental behavior into future rental applications.

Today, that value is largely lost.

Traditional landlord references are weak because applicants choose who provides them, and the resulting references are overwhelmingly positive. Years of reliable tenancy rarely translate into a meaningful advantage during the next application.

This project aims to create a stronger, more objective signal.

---

# Intended Signal

The report should answer a landlord's fundamental question:

> "Has this applicant consistently met their rental obligations over time?"

Ideally, the report would provide objective evidence of:

* verified lease periods
* expected rent obligations
* observed rent payments
* payment consistency
* gaps in payment history
* long-term rental reliability

The value of the product depends entirely on the credibility of this signal.

---

# Current Technical Capability

Using Plaid and Open Banking, the system can reliably observe:

* recurring transactions
* payment dates
* payment amounts
* transaction history

This allows the system to detect payments that strongly resemble rent.

However, transaction history alone cannot establish the obligations those payments were intended to satisfy.

---

# The Missing Source of Truth

The system does not know:

* when a lease began
* when a lease ended
* what rent was contractually due
* which day rent was due
* whether a payment was late
* whether a payment gap represents a missed payment or simply a gap between leases

Without a trusted lease record, every interpretation becomes an inference.

---

# The Completeness Problem

For the report to be trustworthy, it must solve two related but distinct problems:

1. **Boundary accuracy** — knowing the exact start and end of each lease so the expected number of payments is known (the denominator problem)
2. **Completeness** — knowing that no tenancy has been omitted from the history

Both are required. Solving boundary accuracy alone still allows a tenant to omit an unfavorable tenancy. Solving completeness alone still leaves individual lease periods unverifiable.

Completeness is the harder requirement and is load-bearing for the full product vision.

---

# Why Landlord Verification Alone Does Not Solve Completeness

Historical landlords can provide lease information.

However, this introduces new challenges:

* tenants choose which landlords to invite
* historical landlords may not respond
* omitted rental relationships remain undetectable
* participation cannot be guaranteed

The resulting report is stronger than a traditional reference, but it still cannot claim to represent a complete rental history.

---

# Trust Model

The system should be understood as a **graduated trust model**, not a binary verified/unverified system.

Every verified lease contributes an independently corroborated piece of rental history.

A single verified lease consists of:

* landlord-confirmed lease obligations
* applicant-authorized bank transaction verification
* a documented verification trail linking the two

This is already a stronger signal than a traditional reference because it replaces an informal recommendation with structured, verifiable facts.

The strength of the overall report is determined by two independent dimensions:

* **Credibility** — how confidently each individual lease has been verified.
* **Coverage** — how much of the tenant's rental history has been verified.

Credibility is achieved through landlord verification and payment corroboration.

Coverage increases as additional landlords participate.

A report with one verified lease may have high credibility but limited coverage.

A report with ten verified leases approaches a comprehensive rental history.

These dimensions should remain visible to landlords rather than being collapsed into a single score.

---

# Paths Toward Greater Coverage

The current product intentionally accepts incomplete coverage.

The long-term opportunity is to increase the proportion of a tenant's rental history that can be independently verified.

Possible paths include:

## 1. Landlord Network Growth

As more landlords and property management organizations participate, verified lease coverage naturally increases.

This creates a network effect:

* participating landlords contribute stronger signals for future applications
* future landlords receive more complete reports
* tenants accumulate portable rental history over time

The challenge is solving the cold-start problem, since the primary beneficiary of a landlord's verification effort is often the tenant's next landlord.

## 2. Property Management System Integrations

Rather than relying on individual landlords, integrations with lease management platforms could allow lease information to be verified directly from operational systems.

This reduces manual effort while improving consistency.

## 3. Public or Regulatory Infrastructure

If jurisdictions eventually adopt lease registration systems or standardized tenancy reporting, those records could become authoritative sources of lease history.

Such infrastructure would significantly improve completeness but is outside the scope of the current product.

---

# Resolution

The original vision was to create a portable, independently verified rental history.

That vision remains valid.

However, complete rental history should be viewed as a long-term objective rather than an MVP requirement.

The MVP does not attempt to prove a tenant's entire rental history.

Instead, it attempts to answer a narrower question:

> "Can this tenant provide stronger evidence for this verified tenancy than a traditional landlord reference?"

The answer is yes.

A single verified lease, corroborated by bank transaction data, is already a materially stronger application artifact than today's combination of reference letters, PDFs, and bank statements.

The product therefore follows an incremental strategy:

1. Build highly credible verification for individual leases.
2. Increase historical coverage as more landlords participate.
3. Move toward a portable, comprehensive rental history as the verification network grows.

---

# Current Design Priorities

1. Make a single landlord verification as credible and friction-free as possible.
2. Give participating landlords a reason to return as prospective landlords themselves.
3. Build toward network adoption from property management organizations, where one partnership equals many landlords.
4. Track regulatory developments in lease registry proposals as a long-term completeness path.
