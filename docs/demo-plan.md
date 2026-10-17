# Final demonstration plan (8–12 minutes)

1. **Problem and objective — 1 minute:** Explain that the app records daily expenses and makes category/month totals easier to review.
2. **Scope and data safety — 1 minute:** State it is a single-user learning project, uses voluntary entries or fictional data, and is not connected to a bank or financial advice.
3. **Database design — 1 minute:** Show `categories` and `expenses`, the one-to-many relationship, positive `DECIMAL` amount constraint, and environment-based database connection.
4. **End-to-end CRUD — 2 minutes:** Add an expense, show it in the list, edit one field, and delete a demonstration row.
5. **Filters — 1 minute:** Select a date range and category, then reconcile the total with matching rows.
6. **Analysis and charts — 2 minutes:** Explain total, average, median, top category, monthly grouping, category pie, monthly bars, and category bars in plain language.
7. **Testing — 1 minute:** Show automated formula/validation checks and walk through the manual database and filter acceptance checklist.
8. **Limitations and conclusion — 1 minute:** Mention one user, no bank import/authentication, record accuracy depends on entries, and how the app could be extended safely.

For a smooth demo, initialize MySQL, use the fictional seed records, set `.env`, and confirm the dashboard works before presenting. Do not show `.env` or enter real banking details.
