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

# Trust Tiers

The product is better understood as a tiered trust model rather than a binary verified/unverified system.

Verified landlord participation produces a report with weight proportional to how that history was sourced — analogous to how a bank loan carries more weight on a credit report than a private loan. A report backed by participating, accountable landlords is meaningfully stronger than one backed by tenant-selected references.

This means the product's value scales with landlord network adoption, not as an all-or-nothing proposition.

---

# Paths to Full Completeness

Two paths could eventually solve the completeness problem:

**Landlord network adoption**
A sufficiently large and trusted network of participating landlords — property management companies, landlord associations, housing co-ops — creates a system where verified history has weight and omissions become conspicuous. This requires solving a cold start problem: early landlord adopters contribute data whose primary benefit flows to the tenant's next landlord, not themselves. The value proposition is access to better applicant signal from a shared infrastructure they all benefit from.

**Government mandate**
A regulated lease registry — where landlords are required to register leases — would solve completeness by default. Tenant history becomes independently registered and cannot be selectively omitted. This is the ideal long-term architecture but requires policy advocacy and is years away at best.

---

# Resolution: The Product Is Scoped, Not Blocked

The project is not blocked by trust. The trust model is understood.

The full vision — a complete, independently verified rental history — requires either landlord network adoption or a government-mandated lease registry. Neither is available today.

However, the product does not need completeness to be useful.

> A single landlord verification, corroborated by Plaid transaction data, is already a stronger signal than a traditional reference letter.

The tenant's first landlord verification is the product. It establishes:

* a confirmed lease record (dates, rent, due day)
* verified payment behavior against that record
* landlord accountability on record

This is meaningful to a prospective landlord even in the absence of a complete history. The product has real value today, and that value grows as landlord participation increases.

---

# Current Design Priorities

1. Make a single landlord verification as credible and friction-free as possible
2. Give participating landlords a reason to return as prospective landlords themselves
3. Build toward network adoption from property management organizations, where one partnership equals many landlords
4. Track regulatory developments in lease registry proposals as a long-term completeness path
