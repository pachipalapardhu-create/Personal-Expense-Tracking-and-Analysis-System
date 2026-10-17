# Test plan and results

## Test scope

The automated checks cover the summary formulas and expense form validation without requiring a live MySQL connection. Database permissions and connection failure handling still need a manual demonstration against a configured MySQL instance.

## Cases

| ID | Scenario | Expected result |
| --- | --- | --- |
| A1 | Several records in two categories and months | Grand total, count, average, median, category sum, top category, and month sum match the inputs |
| A2 | Empty result set | Total/count are zero; no highest category; category/month tables are empty |
| A3 | One record on a month boundary | Amount is preserved and grouped under the correct `YYYY-MM` |
| V1 | Valid form with positive decimal amount | Parsed values returned with a two-decimal amount |
| V2 | Amount of zero or less | Rejected with a validation message |
| V3 | Blank, nonnumeric, non-finite, excessive, or more-than-two-decimal amount | Rejected with a validation message |
| V4 | Missing/malformed date or category | Rejected with a validation message |
| V5 | Empty/overlong description or unlisted payment method | Rejected with a validation message |
| D1 | No records match the selected filters | Dashboard and charts show empty states and zero total |
| D2 | Date and category filters together | Only matching rows contribute to displayed totals and chart groupings |
| DB1 | Database unavailable or access denied | App returns a useful service-unavailable page; no credentials appear in the response |

## Automated checks

`analysis_tests.py` covers A1–A3. `tests/test_validation.py` covers V1–V5. Run `pytest -q` from the project root. Record the actual command result below after running it in the target environment.

**Automated result:** `py -m pytest -q` — 16 passed. This ran the summary and form-validation checks in the build environment; it did not exercise a live MySQL server or browser workflow.

## Manual acceptance checklist

- [ ] Run `schema.sql`, then optionally `seed.sql` on a test database.
- [ ] Add an expense and confirm it appears in the list and dashboard.
- [ ] Edit it and confirm amount/category/date changes are reflected.
- [ ] Try zero and negative amounts and confirm they are rejected.
- [ ] Filter by a date range and category together; reconcile visible records with the total.
- [ ] Delete a record and confirm it no longer affects summaries.
- [ ] Check all three chart titles, labels, units, and empty states.
- [ ] Stop MySQL and confirm the application shows the friendly error page.

The manual checklist is not a claim that every item has already been exercised. Capture screenshots from a configured local MySQL run before presenting the app as demonstrated.

