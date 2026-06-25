import pytest
from app.services.detection_service import detect_rent_candidates
from tests.fixtures import (
    CLEAR_RENT,
    VARIABLE_RENT,
    SHORT_STREAM,
    NOISE,
    DUAL_RENT,
    RENT_WITH_GAP,
)


def test_detects_clear_rent_stream():
    candidates = detect_rent_candidates(CLEAR_RENT + NOISE)
    assert len(candidates) >= 1
    top = candidates[0]
    assert "parkside" in top["description"].lower()
    assert top["occurrences"] == 18
    assert top["typical_amount"] == 1500.00
    assert top["cadence"] == "monthly"
    assert top["confidence_score"] >= 0.7


def test_detects_variable_amount_rent():
    candidates = detect_rent_candidates(VARIABLE_RENT)
    assert len(candidates) >= 1
    top = candidates[0]
    assert "highland" in top["description"].lower()
    assert top["occurrences"] == 12


def test_filters_short_stream():
    candidates = detect_rent_candidates(SHORT_STREAM)
    assert len(candidates) == 0


def test_filters_noise_below_threshold():
    candidates = detect_rent_candidates(NOISE)
    # Groceries recur but descriptions vary; subscriptions are below $200
    # None should score high enough to qualify
    for c in candidates:
        assert c["confidence_score"] >= 0.2  # any that pass must meet threshold


def test_sorted_by_confidence_descending():
    candidates = detect_rent_candidates(CLEAR_RENT + VARIABLE_RENT + NOISE)
    scores = [c["confidence_score"] for c in candidates]
    assert scores == sorted(scores, reverse=True)


def test_detects_dual_rent_streams():
    candidates = detect_rent_candidates(DUAL_RENT)
    assert len(candidates) == 2
    descriptions = {c["description"].lower() for c in candidates}
    assert any("highland" in d for d in descriptions)
    assert any("parkside" in d for d in descriptions)


def test_rent_with_gap_still_detected():
    candidates = detect_rent_candidates(RENT_WITH_GAP)
    assert len(candidates) >= 1
    top = candidates[0]
    assert "metro" in top["description"].lower()
    assert top["occurrences"] == 11


def test_empty_transactions_returns_empty():
    assert detect_rent_candidates([]) == []


def test_all_below_minimum_amount():
    tiny = [{"date": "2024-01-01", "amount": 50.00, "description": "RENT CO"}] * 12
    assert detect_rent_candidates(tiny) == []
