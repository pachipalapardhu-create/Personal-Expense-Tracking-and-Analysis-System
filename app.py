"""Personal Expense Tracking and Analysis System (single-user learning app)."""
from __future__ import annotations

import os
from datetime import date
from decimal import Decimal, InvalidOperation
from functools import wraps
from io import BytesIO

import mysql.connector
from dotenv import load_dotenv
from flask import Flask, abort, flash, redirect, render_template, request, send_file, url_for
from flask_wtf.csrf import CSRFProtect

from analysis import summarize_expenses

load_dotenv()

app = Flask(__name__)
secret_key = os.getenv("FLASK_SECRET_KEY", "").strip()
if not secret_key or secret_key.lower().startswith("replace-"):
    raise RuntimeError("Set FLASK_SECRET_KEY in your environment or .env before starting the app.")
app.config.update(
    SECRET_KEY=secret_key,
    MAX_CONTENT_LENGTH=32 * 1024,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.getenv("COOKIE_SECURE", "0") == "1",
)
CSRFProtect(app)

PAYMENT_METHODS = ("Cash", "Debit card", "Credit card", "Bank transfer", "UPI", "Other")
CURRENCY_SYMBOL = os.getenv("CURRENCY_SYMBOL", "₹")


def db():
    """Open a MySQL connection from environment-based configuration."""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "expense_app"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "expense_tracker"),
        charset="utf8mb4",
    )


def load_categories(conn):
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT category_id, category_name FROM categories ORDER BY category_name")
    rows = cur.fetchall()
    cur.close()
    return rows


def get_expenses(conn, date_from=None, date_to=None, category_id=None):
    sql = """SELECT e.expense_id, e.expense_date, e.category_id, c.category_name,
                    e.amount, e.description, e.payment_method
             FROM expenses e JOIN categories c ON c.category_id=e.category_id
             WHERE (%s IS NULL OR e.expense_date >= %s)
               AND (%s IS NULL OR e.expense_date <= %s)
               AND (%s IS NULL OR e.category_id = %s)
             ORDER BY e.expense_date DESC, e.expense_id DESC"""
    cur = conn.cursor(dictionary=True)
    cur.execute(sql, (date_from, date_from, date_to, date_to, category_id, category_id))
    rows = cur.fetchall()
    cur.close()
    return rows


def parse_filters():
    date_from = request.args.get("date_from", "").strip() or None
    date_to = request.args.get("date_to", "").strip() or None
    category_raw = request.args.get("category_id", "").strip()
    try:
        date_from = date.fromisoformat(date_from) if date_from else None
        date_to = date.fromisoformat(date_to) if date_to else None
        category_id = int(category_raw) if category_raw else None
        if category_id is not None and category_id < 1:
            raise ValueError
        if date_from and date_to and date_from > date_to:
            raise ValueError
    except (ValueError, TypeError):
        abort(400, description="Choose valid dates in ascending order and a valid category.")
    return date_from, date_to, category_id


def parse_expense_form(form):
    try:
        expense_date = date.fromisoformat(form.get("expense_date", "").strip())
        category_id = int(form.get("category_id", ""))
        amount = Decimal(form.get("amount", "").strip()).quantize(Decimal("0.01"))
    except (ValueError, TypeError, InvalidOperation):
        raise ValueError("Enter a valid date, category, and amount.") from None
    description = form.get("description", "").strip()
    payment_method = form.get("payment_method", "").strip()
    if amount <= 0 or amount > Decimal("999999999.99"):
        raise ValueError("Amount must be greater than zero and no more than 999,999,999.99.")
    if not description or len(description) > 240:
        raise ValueError("Description is required and must be 240 characters or fewer.")
    if payment_method not in PAYMENT_METHODS:
        raise ValueError("Choose a listed payment method.")
    return expense_date, category_id, amount, description, payment_method


def save_expense(conn, expense_id, values):
    expense_date, category_id, amount, description, payment_method = values
    cur = conn.cursor()
    cur.execute("SELECT category_id FROM categories WHERE category_id=%s", (category_id,))
    if cur.fetchone() is None:
        cur.close()
        raise ValueError("Choose a category from the list.")
    if expense_id is None:
        cur.execute(
            "INSERT INTO expenses(expense_date,category_id,amount,description,payment_method) VALUES (%s,%s,%s,%s,%s)",
            (expense_date, category_id, amount, description, payment_method),
        )
    else:
        cur.execute(
            "UPDATE expenses SET expense_date=%s,category_id=%s,amount=%s,description=%s,payment_method=%s WHERE expense_id=%s",
            (expense_date, category_id, amount, description, payment_method, expense_id),
        )
    conn.commit()
    cur.close()


@app.context_processor
def inject_display_settings():
    return {
        "currency_symbol": CURRENCY_SYMBOL,
        "payment_methods": PAYMENT_METHODS,
        "today_label": date.today().strftime("%d %b %Y"),
    }


@app.after_request
def add_security_headers(response):
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    return response


@app.route("/")
def dashboard():
    date_from, date_to, category_id = parse_filters()
    conn = db()
    try:
        categories = load_categories(conn)
        expenses = get_expenses(conn, date_from, date_to, category_id)
    finally:
        conn.close()
    summary = summarize_expenses(expenses)
    return render_template(
        "dashboard.html", categories=categories, expenses=expenses, summary=summary,
        date_from=date_from, date_to=date_to, selected_category=category_id,
    )


@app.get("/expenses")
def expense_list():
    date_from, date_to, category_id = parse_filters()
    conn = db()
    try:
        categories = load_categories(conn)
        expenses = get_expenses(conn, date_from, date_to, category_id)
    finally:
        conn.close()
    return render_template(
        "expenses.html", expenses=expenses, categories=categories,
        date_from=date_from, date_to=date_to, selected_category=category_id,
    )


@app.route("/expenses/new", methods=["GET", "POST"])
def expense_new():
    conn = db()
    try:
        categories = load_categories(conn)
        if request.method == "POST":
            try:
                save_expense(conn, None, parse_expense_form(request.form))
            except (ValueError, LookupError) as exc:
                flash(str(exc), "error")
            else:
                flash("Expense added.", "success")
                return redirect(url_for("expense_list"))
    finally:
        conn.close()
    return render_template("expense_form.html", expense=None, categories=categories, today=date.today())


@app.route("/expenses/<int:expense_id>/edit", methods=["GET", "POST"])
def expense_edit(expense_id):
    conn = db()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM expenses WHERE expense_id=%s", (expense_id,))
        expense = cur.fetchone()
        cur.close()
        if expense is None:
            abort(404)
        categories = load_categories(conn)
        if request.method == "POST":
            try:
                save_expense(conn, expense_id, parse_expense_form(request.form))
            except (ValueError, LookupError) as exc:
                flash(str(exc), "error")
            else:
                flash("Expense updated.", "success")
                return redirect(url_for("expense_list"))
    finally:
        conn.close()
    return render_template("expense_form.html", expense=expense, categories=categories, today=date.today())


@app.post("/expenses/<int:expense_id>/delete")
def expense_delete(expense_id):
    conn = db()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM expenses WHERE expense_id=%s", (expense_id,))
        deleted = cur.rowcount > 0
        conn.commit()
        cur.close()
    finally:
        conn.close()
    flash("Expense deleted." if deleted else "Expense was already removed.", "success")
    return redirect(url_for("expense_list"))


@app.get("/reports")
def monthly_report():
    conn = db()
    try:
        expenses = get_expenses(conn)
    finally:
        conn.close()
    summary = summarize_expenses(expenses)
    return render_template("reports.html", summary=summary, expenses=expenses)


@app.get("/charts/<chart_name>.png")
def chart_image(chart_name):
    if chart_name not in {"category-pie", "month-bar", "category-bar"}:
        abort(404)
    date_from, date_to, category_id = parse_filters()
    conn = db()
    try:
        expenses = get_expenses(conn, date_from, date_to, category_id)
    finally:
        conn.close()
    from analysis import render_chart
    image = render_chart(expenses, chart_name)
    return send_file(BytesIO(image), mimetype="image/png", max_age=0)


@app.errorhandler(mysql.connector.Error)
def database_error(error):
    app.logger.error("Database operation failed: %s", error)
    return render_template("error.html", message="The database could not complete that request. Check your connection and database setup."), 503


@app.errorhandler(413)
def request_too_large(_error):
    return render_template("error.html", message="The submitted form is too large."), 413


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "0") == "1")
