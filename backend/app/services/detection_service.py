from datetime import date
from statistics import median, stdev, mean
import re


MIN_AMOUNT = 200.0
MIN_STREAK = 3
MIN_CONFIDENCE = 0.2


def normalize_description(desc: str) -> str:
    desc = desc.lower().strip()
    desc = re.sub(r"[^a-z0-9\s]", "", desc)
    desc = re.sub(r"\s+", " ", desc)
    return desc


def description_similarity(a: str, b: str) -> float:
    tokens_a = set(normalize_description(a).split())
    tokens_b = set(normalize_description(b).split())
    if not tokens_a or not tokens_b:
        return 0.0
    return len(tokens_a & tokens_b) / len(tokens_a | tokens_b)


def cluster_by_description(transactions: list[dict]) -> list[list[dict]]:
    clusters: list[list[dict]] = []
    assigned = [False] * len(transactions)

    for i, tx in enumerate(transactions):
        if assigned[i]:
            continue
        cluster = [tx]
        assigned[i] = True
        for j, other in enumerate(transactions):
            if assigned[j] or i == j:
                continue
            if description_similarity(tx["description"], other["description"]) >= 0.5:
                cluster.append(other)
                assigned[j] = True
        clusters.append(cluster)

    return clusters


def cadence_score(dates: list[date]) -> float:
    if len(dates) < 2:
        return 0.0
    sorted_dates = sorted(dates)
    intervals = [(sorted_dates[i + 1] - sorted_dates[i]).days for i in range(len(sorted_dates) - 1)]
    monthly_intervals = [i for i in intervals if 25 <= i <= 35]
    return len(monthly_intervals) / len(intervals)


def amount_stability_score(amounts: list[float]) -> float:
    if len(amounts) < 2:
        return 1.0
    m = mean(amounts)
    if m == 0:
        return 0.0
    cv = stdev(amounts) / m
    return max(0.0, 1.0 - cv)


def streak_score(dates: list[date]) -> float:
    if not dates:
        return 0.0
    sorted_dates = sorted(dates)
    months = {(d.year, d.month) for d in sorted_dates}
    streak = 0
    max_streak = 0
    prev = None
    for ym in sorted(months):
        if prev is None or (ym[0] * 12 + ym[1]) == (prev[0] * 12 + prev[1]) + 1:
            streak += 1
        else:
            streak = 1
        max_streak = max(max_streak, streak)
        prev = ym
    return min(1.0, max_streak / 12)


def detect_rent_candidates(transactions: list[dict]) -> list[dict]:
    outflows = [t for t in transactions if t["amount"] >= MIN_AMOUNT]
    if not outflows:
        return []

    clusters = cluster_by_description(outflows)
    candidates = []

    for cluster in clusters:
        amounts = [t["amount"] for t in cluster]
        dates = [date.fromisoformat(t["date"]) for t in cluster]

        max_streak = _max_streak(dates)
        if max_streak < MIN_STREAK:
            continue

        c_score = cadence_score(dates)
        a_score = amount_stability_score(amounts)
        s_score = streak_score(dates)
        confidence = round((c_score * 0.5) + (a_score * 0.3) + (s_score * 0.2), 3)

        if confidence < MIN_CONFIDENCE:
            continue

        cadence = "monthly" if c_score >= 0.7 else "irregular"

        candidates.append({
            "description": cluster[0]["description"],
            "amount_range": [round(min(amounts), 2), round(max(amounts), 2)],
            "typical_amount": round(median(amounts), 2),
            "first_payment": str(min(dates)),
            "last_payment": str(max(dates)),
            "occurrences": len(cluster),
            "cadence": cadence,
            "confidence_score": confidence,
            "transactions": sorted(cluster, key=lambda t: t["date"]),
        })

    return sorted(candidates, key=lambda c: c["confidence_score"], reverse=True)


def _max_streak(dates: list[date]) -> int:
    months = sorted({(d.year, d.month) for d in dates})
    streak = max_streak = 0
    prev = None
    for ym in months:
        if prev is None or (ym[0] * 12 + ym[1]) == (prev[0] * 12 + prev[1]) + 1:
            streak += 1
        else:
            streak = 1
        max_streak = max(max_streak, streak)
        prev = ym
    return max_streak
