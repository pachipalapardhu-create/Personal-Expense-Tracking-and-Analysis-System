# Spendwise — Personal Expense Tracking and Analysis System

A beginner-friendly, single-user Flask and MySQL website for recording personal expenses and understanding monthly and category-wise spending. It includes expense CRUD, date/category filters, Pandas and NumPy summaries, and three Matplotlib charts.

> This is a learning project, not a banking service or financial advice. It does not connect to a bank, import transactions, provide accounts or multi-user permissions, or recommend financial decisions. Use fictional or voluntarily entered data. Never commit passwords, real banking details, or `.env`.

## Features

- Add, edit, delete, and list expenses with date, category, positive amount, description, and payment method.
- Filter the dashboard and transaction list by date range and category. The amount shown is the sum of the matching records.
- See the selected records' total, transaction count, mean, median, and highest-spending category.
- Explore category share, month-wise spending, and category totals charts.
- Open the monthly report for calendar-month totals and plain-language interpretation.
- Use CSRF-protected forms, parameterized MySQL queries, environment-based database credentials, and MySQL constraints.
- Start with fictional sample records; delete them before entering personal data if they are not wanted.

## Requirements

- Python 3.10 or newer
- MySQL 8.0 or newer
- pip

## Local setup

1. Create the database and tables as a MySQL administrator by running [`schema.sql`](schema.sql). Optionally run [`seed.sql`](seed.sql) afterward for fictional demo expenses.
2. Create a dedicated database account with access only to this project's database. For example, in MySQL, change the example password and run:

   ```sql
   CREATE USER 'expense_app'@'localhost' IDENTIFIED BY 'choose-a-long-local-password';
   GRANT SELECT, INSERT, UPDATE, DELETE ON expense_tracker.* TO 'expense_app'@'localhost';
   ```

   If the app connects over TCP and MySQL does not accept `localhost`, create the account for `127.0.0.1` instead. Avoid using the MySQL root account in the app.

3. Create and activate a virtual environment, then install packages:

   **Windows PowerShell**

   ```powershell
   py -m venv .venv
   .venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   Copy-Item .env.example .env
   ```

   **macOS/Linux**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env
   ```

4. Edit `.env`: set `FLASK_SECRET_KEY` to a unique random value and fill in the MySQL settings. Generate a random key with:

   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

   Keep `.env` private; it is excluded by `.gitignore`. `COOKIE_SECURE=0` is for local HTTP development. Set it to `1` only when serving the site over HTTPS. `CURRENCY_SYMBOL` controls the display symbol.

5. Start the app:

   ```bash
   python app.py
   ```

6. Open `http://127.0.0.1:5000`. If the database is not available, verify the MySQL service, schema, `.env` values, and the app user's database grants.

To run the included checks, use `pytest -q` from the project directory. They cover summary calculations and form validation; they do not require a live MySQL server.

## Project structure

```text
app.py                   Flask routes, database access, CRUD, and validation
analysis.py              Pandas/NumPy summaries and Matplotlib chart generation
schema.sql               MySQL schema, constraints, indexes, and category setup
seed.sql                 Fictional example expenses
templates/               Server-rendered pages and forms
static/style.css         Responsive visual design
analysis_tests.py        Summary calculation checks
tests/                   Expense form validation checks
docs/                    Synopsis, data model, analysis, tests, and demo plan
```

## Database and data flow

`categories.category_id` is the parent key referenced by `expenses.category_id`. The database requires a positive `DECIMAL(12,2)` amount and a valid payment method. The app checks values before insert/update and uses parameterized SQL. Filters are applied in the SQL query before Pandas groups the selected rows. The complete schema and relationship sketch are in [`docs/database-design.md`](docs/database-design.md).

## Analysis definitions

- **Total spending:** sum of amounts in the selected records.
- **Average expense:** arithmetic mean of those record amounts.
- **Median expense:** middle value of sorted amounts (mean of the two middle values when the count is even).
- **Category share:** category sum divided by the selected total; a pie chart shows shares.
- **Highest-spending category:** category with the largest sum among the selected records.
- **Monthly total:** sum grouped by the expense's calendar month (`YYYY-MM`).

The output describes only the entered records. Missing expenses, incorrect categories, cash-flow timing, income, budgets, and external accounts are outside the analysis.

## Routes

See [`docs/api-and-routes.md`](docs/api-and-routes.md) for all page and chart endpoints. This project is a server-rendered website; these routes return HTML or PNG charts, not a public JSON REST API.

## Testing and limitations

Test cases and outcomes are tracked in [`docs/test-report.md`](docs/test-report.md). The application is designed for one trusted local user and has no login or multi-user access control. Before exposing it to the public internet, add authentication, authorization, rate limits, production deployment settings, managed secrets, and an operational privacy/deletion plan. Use HTTPS and set `COOKIE_SECURE=1` for an HTTPS deployment.

## Project deliverables

- Proposal and scope: [`docs/project-synopsis.md`](docs/project-synopsis.md)
- Database design and data dictionary: [`docs/database-design.md`](docs/database-design.md)
- Analysis methodology and example output: [`docs/analysis-methodology.md`](docs/analysis-methodology.md), [`docs/sample-monthly-report.csv`](docs/sample-monthly-report.csv)
- Example chart images made from the fictional seed rows: [`category share`](docs/sample-charts/category-share.png), [`monthly spending`](docs/sample-charts/monthly-spending.png), [`category totals`](docs/sample-charts/category-totals.png)
- Routes: [`docs/api-and-routes.md`](docs/api-and-routes.md)
- Test plan and results: [`docs/test-report.md`](docs/test-report.md)
- 8–12 minute demonstration plan: [`docs/demo-plan.md`](docs/demo-plan.md)

