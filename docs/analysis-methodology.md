# Analysis methodology and sample output

## Processing steps

1. Parse optional date/category filters and apply them in MySQL. Date endpoints are inclusive.
2. Convert returned amount values to numeric data in a Pandas DataFrame; discard invalid numeric values as zero defensively (the database `DECIMAL` and form validation are expected to prevent them).
3. Group by category and by calendar month. NumPy computes the total, mean, and median over the selected amounts.
4. Render charts from the same filtered rows displayed on the dashboard. Empty data produces an explanatory empty chart instead of a misleading zero pie.

## Formulas

- Total: `Σ amountᵢ`
- Mean: `Σ amountᵢ / n`; zero when there are no rows.
- Median: middle sorted amount; average of two middle amounts for even `n`; zero when there are no rows.
- Category total: sum of amounts where category equals that category.
- Category share: category total divided by total for the selected records. The pie chart labels show percent shares.
- Monthly total: sum of amounts where the expense date has the same year and month.
- Highest category: category with the greatest category total; absent for an empty dataset.

## Charts

1. **Share of spending by category:** pie chart; slices show each category's share of the selected total.
2. **Monthly spending:** vertical bar chart; x-axis is calendar month and y-axis is amount in the configured display currency (the sample uses ₹).
3. **Spending by category:** horizontal bar chart; categories are on the y-axis and total amount on the x-axis.

## Example from fictional seed rows

The provided eight sample rows sum to ₹4,020.00: September 2026 totals ₹1,350.00 and October 2026 totals ₹2,670.00. The largest category is Education at ₹1,250.00. The average is ₹502.50 per record and the median is ₹380.00. Example CSV: [`sample-monthly-report.csv`](sample-monthly-report.csv).

These metrics describe only entered sample records. They are not a budget comparison, prediction, or recommendation. Results can be incomplete or misleading if records are missing, duplicated, mistyped, or categorized inconsistently.
