# Project synopsis and requirements

## Project

**Personal Expense Tracking and Analysis System (Spendwise)**  
Difficulty: Beginner · Intended user: one person recording their own expenses

## Problem statement

Small day-to-day purchases can be difficult to review from memory. This project gives one user a simple place to record expenses and see totals by month and category.

## Objectives

1. Capture expense date, category, positive amount, description, and payment method.
2. Support create, read, update, and delete operations.
3. Let the user filter records by an inclusive date range and category.
4. Calculate totals and summary statistics from precisely the displayed records.
5. Present category and month patterns with charts and explain how to interpret them.

## Scope and boundaries

This is a single-user learning project using fictional or voluntarily entered data. It is not connected to a bank, does not provide financial advice, and does not verify whether entries are accurate. The intended deployment is a local trusted machine or a private demonstration environment. Multi-user accounts, budgets, recurring expenses, forecasting, imports, and public hosting controls are outside the current version.

## Functional requirements

- Add, edit, delete, and list expenses.
- Choose a category and payment method from configured lists.
- Reject a missing or malformed date, invalid category/payment choice, empty or overlong description, and amount less than or equal to zero.
- Filter the dashboard and transaction list by date range and category.
- Show total, count, mean, median, top category, category totals, and monthly totals.
- Display a category-share pie chart, monthly bar chart, and category-total horizontal bar chart.
- Show a useful empty state when there are no matching records.

## Assumptions

- The database is MySQL 8 and is initialized with `schema.sql`.
- One trusted user operates the app; the database is local or privately networked.
- Amounts are entered as decimal values to two fractional digits. The display currency symbol is configurable; sample records are fictional.
- Date-range endpoints are inclusive.

## Plan

1. Set up schema, seed records, and environment-based connection configuration.
2. Build Flask CRUD routes and validate form inputs.
3. Add filtered analysis and three charts.
4. Document the schema, formulas, limitations, and run instructions.
5. Run calculation and validation checks, then rehearse the demo flow.

## Success criteria

Valid records can be created, edited, filtered, and removed; invalid or non-positive amounts are rejected; filtered totals equal the matching records; reports include month and category summaries; charts have clear titles and units; setup does not require credentials in source control.
