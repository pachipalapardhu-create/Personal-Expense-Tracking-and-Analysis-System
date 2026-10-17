# Application routes

This is a server-rendered Flask website. Routes return HTML pages or generated PNG chart images; this version does not expose a public JSON REST API. All writes use HTML forms with Flask-WTF CSRF tokens.

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/` | Dashboard; optional `date_from`, `date_to`, and `category_id` query filters |
| `GET` | `/expenses` | List expenses; supports the same optional filters |
| `GET`, `POST` | `/expenses/new` | Display and create an expense |
| `GET`, `POST` | `/expenses/<expense_id>/edit` | Display and update an expense |
| `POST` | `/expenses/<expense_id>/delete` | Delete an expense |
| `GET` | `/reports` | All-time monthly and category summaries |
| `GET` | `/charts/category-pie.png` | Category share chart; accepts dashboard filters |
| `GET` | `/charts/month-bar.png` | Month total chart; accepts dashboard filters |
| `GET` | `/charts/category-bar.png` | Category total chart; accepts dashboard filters |

## Validation and responses

- The amount must be greater than zero and no more than `999,999,999.99`.
- Date, category, description (1–240 characters), and payment method are validated before write.
- Filter dates must be valid ISO dates and `date_from` cannot be after `date_to`.
- Invalid filters return HTTP 400; a missing expense returns HTTP 404; a database failure returns a friendly HTTP 503 page.
- Successful creates, updates, and deletes redirect to the transaction list with a flash message.
- SQL uses parameter placeholders. Database values are not interpolated into statements.
