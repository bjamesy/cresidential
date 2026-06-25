"""
Mock transaction data for testing the detection pipeline.

Scenarios:
  - CLEAR_RENT: 18 months of consistent $1,500 payments to "Parkside Properties"
  - VARIABLE_RENT: 12 months of rent with slight amount variation ($1,495–$1,510)
  - SHORT_STREAM: only 2 occurrences — should be filtered (below min streak)
  - NOISE: subscriptions, groceries, utilities — should not surface as candidates
  - DUAL_RENT: two rent streams (moved apartments mid-period)
"""

from datetime import date


def make_tx(d: str, amount: float, description: str) -> dict:
    return {"date": d, "amount": amount, "description": description}


# 18 consistent monthly payments — high confidence candidate
CLEAR_RENT = [
    make_tx(f"2024-{m:02d}-03", 1500.00, "Parkside Properties LLC")
    for m in range(1, 13)
] + [
    make_tx(f"2025-{m:02d}-03", 1500.00, "Parkside Properties LLC")
    for m in range(1, 7)
]

# 12 months with slight amount variation — should still detect
VARIABLE_RENT = [
    make_tx("2024-01-02", 1495.00, "HIGHLAND MGMT"),
    make_tx("2024-02-03", 1500.00, "HIGHLAND MGMT"),
    make_tx("2024-03-01", 1500.00, "HIGHLAND MGMT"),
    make_tx("2024-04-02", 1510.00, "HIGHLAND MGMT"),
    make_tx("2024-05-03", 1500.00, "HIGHLAND MGMT"),
    make_tx("2024-06-02", 1500.00, "HIGHLAND MGMT"),
    make_tx("2024-07-01", 1500.00, "HIGHLAND MGMT"),
    make_tx("2024-08-02", 1495.00, "HIGHLAND MGMT"),
    make_tx("2024-09-03", 1500.00, "HIGHLAND MGMT"),
    make_tx("2024-10-02", 1500.00, "HIGHLAND MGMT"),
    make_tx("2024-11-01", 1510.00, "HIGHLAND MGMT"),
    make_tx("2024-12-02", 1500.00, "HIGHLAND MGMT"),
]

# Only 2 payments — below MIN_STREAK of 3, should be filtered
SHORT_STREAM = [
    make_tx("2024-03-01", 1200.00, "OAKWOOD APTS"),
    make_tx("2024-04-01", 1200.00, "OAKWOOD APTS"),
]

# Noise: subscriptions, groceries, utilities — amounts below $200 or irregular
NOISE = [
    make_tx("2024-01-10", 15.99, "Netflix"),
    make_tx("2024-02-10", 15.99, "Netflix"),
    make_tx("2024-03-10", 15.99, "Netflix"),
    make_tx("2024-01-15", 89.00, "SPOTIFY PREMIUM"),
    make_tx("2024-01-20", 312.00, "WHOLE FOODS"),
    make_tx("2024-02-18", 278.00, "WHOLE FOODS"),
    make_tx("2024-03-22", 334.00, "WHOLE FOODS"),
    make_tx("2024-01-25", 145.00, "CON EDISON"),
    make_tx("2024-02-25", 162.00, "CON EDISON"),
    make_tx("2024-03-25", 138.00, "CON EDISON"),
]

# Two rent streams — moved from Highland to Parkside in mid-2024
DUAL_RENT = [
    make_tx("2024-01-02", 1400.00, "HIGHLAND MGMT"),
    make_tx("2024-02-02", 1400.00, "HIGHLAND MGMT"),
    make_tx("2024-03-02", 1400.00, "HIGHLAND MGMT"),
    make_tx("2024-04-02", 1400.00, "HIGHLAND MGMT"),
    make_tx("2024-05-02", 1400.00, "HIGHLAND MGMT"),
    make_tx("2024-06-02", 1400.00, "HIGHLAND MGMT"),
    make_tx("2024-08-01", 1650.00, "Parkside Properties LLC"),
    make_tx("2024-09-01", 1650.00, "Parkside Properties LLC"),
    make_tx("2024-10-01", 1650.00, "Parkside Properties LLC"),
    make_tx("2024-11-01", 1650.00, "Parkside Properties LLC"),
    make_tx("2024-12-01", 1650.00, "Parkside Properties LLC"),
    make_tx("2025-01-01", 1650.00, "Parkside Properties LLC"),
]

# Gap scenario: consistent rent but one month missing
RENT_WITH_GAP = [
    make_tx(f"2024-{m:02d}-01", 1300.00, "METRO REALTY")
    for m in [1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12]  # June missing
]
