# Database design

## Relationship sketch

```text
+-------------------+          +----------------------+
| categories        | 1      * | expenses             |
|-------------------|----------|----------------------|
| PK category_id    |          | PK expense_id        |
| UQ category_name  |          | FK category_id       |
+-------------------+          | expense_date         |
                               | amount               |
                               | description          |
                               | payment_method       |
                               | created_at           |
                               +----------------------+
```

Each expense has exactly one category. A category can be referenced by many expenses. `categories.category_id` is the primary key and `expenses.category_id` is a foreign key. Deleting a category with attached expenses is prevented by the foreign key, avoiding accidental loss of transaction classification.

## Tables and data dictionary

### `categories`

| Column | Type | Rule | Purpose |
| --- | --- | --- | --- |
| `category_id` | `INT UNSIGNED` | Primary key, auto increment | Internal category identifier |
| `category_name` | `VARCHAR(60)` | Unique, required | Display name |

### `expenses`

| Column | Type | Rule | Purpose |
| --- | --- | --- | --- |
| `expense_id` | `BIGINT UNSIGNED` | Primary key, auto increment | Internal expense identifier |
| `expense_date` | `DATE` | Required, indexed | Date the expense occurred |
| `category_id` | `INT UNSIGNED` | Required foreign key | Category for this expense |
| `amount` | `DECIMAL(12,2)` | Required, `CHECK (amount > 0)` | Positive amount; fixed-point precision |
| `description` | `VARCHAR(240)` | Required | Short user-entered note |
| `payment_method` | `ENUM` | Required, defaults to `Other` | Payment method label |
| `created_at` | `TIMESTAMP` | Defaults to current timestamp | Record creation time |

## Setup and sample data

`schema.sql` creates the database, both tables, indexes, positive-amount constraint, and starter categories. Run it as a database administrator. The application should connect with a separate user that has only `SELECT`, `INSERT`, `UPDATE`, and `DELETE` on `expense_tracker.*`. `seed.sql` inserts eight fictional examples spanning September and October 2026. Running the seed repeatedly adds duplicate demo entries; use it only once on a clean demo database.

## Query and integrity notes

- Expense reads join categories so list pages can show category names.
- Date and category filters are applied in a parameterized SQL query.
- Writes use SQL placeholders rather than string interpolation.
- The database foreign key guarantees every expense has an existing category.
- The app validates positive amounts and the schema repeats that rule as a `CHECK` constraint.
- Amounts use `DECIMAL`, not binary floating point, in storage.
