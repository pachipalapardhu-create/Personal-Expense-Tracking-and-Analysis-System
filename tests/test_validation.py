import os
from datetime import date
from decimal import Decimal

import pytest

os.environ.setdefault("FLASK_SECRET_KEY", "test-only-secret-key-for-unit-tests")
from app import parse_expense_form  # noqa: E402


def valid_form(**changes):
    values = {
        "expense_date": "2026-10-17",
        "category_id": "1",
        "amount": "12.30",
        "description": "Lunch",
        "payment_method": "UPI",
    }
    values.update(changes)
    return values


def test_valid_expense_parses_to_decimal():
    result = parse_expense_form(valid_form())
    assert result == (date(2026, 10, 17), 1, Decimal("12.30"), "Lunch", "UPI")


@pytest.mark.parametrize("amount", ["0", "-0.01"])
def test_amount_must_be_positive(amount):
    with pytest.raises(ValueError, match="greater than zero"):
        parse_expense_form(valid_form(amount=amount))


@pytest.mark.parametrize("amount", ["abc", "", "1000000000", "NaN", "Infinity", "1.239"])
def test_invalid_or_too_large_amount_is_rejected(amount):
    with pytest.raises(ValueError):
        parse_expense_form(valid_form(amount=amount))


@pytest.mark.parametrize("field,value", [
    ("expense_date", "17-10-2026"), ("expense_date", ""),
    ("category_id", "not-a-number"), ("category_id", ""),
    ("description", ""), ("description", "x" * 241),
    ("payment_method", "Crypto"),
])
def test_invalid_fields_are_rejected(field, value):
    with pytest.raises(ValueError):
        parse_expense_form(valid_form(**{field: value}))

