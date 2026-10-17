"""Small acceptance checks for analysis calculations (run: pytest -q)."""
from datetime import date
from decimal import Decimal

from analysis import summarize_expenses


def row(day, amount, category):
    return {"expense_date": date.fromisoformat(day), "amount": Decimal(amount), "category_name": category}


def test_summary_totals_and_highest_category_match_records():
    result = summarize_expenses([
        row("2026-10-01", "10.00", "Food"),
        row("2026-10-02", "20.00", "Food"),
        row("2026-09-02", "25.00", "Transport"),
    ])
    assert result["total"] == 55.0
    assert result["count"] == 3
    assert result["average"] == 55 / 3
    assert result["highest_category"] == "Transport"
    assert result["categories"].set_index("label").loc["Food", "total"] == 30
    assert result["months"].set_index("label").loc["2026-10", "total"] == 30


def test_empty_dataset_has_zero_totals_and_no_highest_category():
    result = summarize_expenses([])
    assert result["total"] == 0
    assert result["count"] == 0
    assert result["highest_category"] is None
    assert result["categories"].empty


def test_single_record_is_a_boundary_case():
    result = summarize_expenses([row("2026-01-31", "0.01", "Other")])
    assert result["total"] == 0.01
    assert result["average"] == 0.01
    assert result["months"].iloc[0]["label"] == "2026-01"
