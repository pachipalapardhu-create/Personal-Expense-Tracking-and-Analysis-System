"""Pandas/NumPy summaries and Matplotlib charts for expense records."""
from __future__ import annotations

from io import BytesIO

import numpy as np
import pandas as pd


def summarize_expenses(expenses):
    """Return totals and groupings for rows already filtered by the caller."""
    frame = pd.DataFrame(expenses)
    if frame.empty:
        empty = pd.DataFrame(columns=["label", "total", "count"])
        return {
            "total": 0.0, "count": 0, "average": 0.0, "median": 0.0,
            "highest_category": None, "categories": empty, "months": empty,
        }
    frame["amount"] = pd.to_numeric(frame["amount"], errors="coerce").fillna(0).astype(float)
    frame["expense_date"] = pd.to_datetime(frame["expense_date"], errors="coerce")
    category = (frame.groupby("category_name", as_index=False)
                .agg(total=("amount", "sum"), count=("amount", "size"))
                .sort_values("total", ascending=False))
    month_frame = frame.dropna(subset=["expense_date"]).copy()
    month_frame["month"] = month_frame["expense_date"].dt.to_period("M").astype(str)
    months = (month_frame.groupby("month", as_index=False)
              .agg(total=("amount", "sum"), count=("amount", "size"))
              .sort_values("month"))
    amount_values = frame["amount"].to_numpy(dtype=float)
    return {
        "total": float(np.sum(amount_values)),
        "count": int(amount_values.size),
        "average": float(np.mean(amount_values)),
        "median": float(np.median(amount_values)),
        "highest_category": category.iloc[0]["category_name"] if not category.empty else None,
        "categories": category.rename(columns={"category_name": "label"}),
        "months": months.rename(columns={"month": "label"}),
    }


def render_chart(expenses, chart_name):
    """Return a PNG chart; the Agg backend works without a desktop display."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    summary = summarize_expenses(expenses)
    fig, ax = plt.subplots(figsize=(7.2, 4.2), constrained_layout=True)
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#ffffff")
    if chart_name == "category-pie":
        data = summary["categories"]
        if data.empty:
            ax.text(.5, .5, "No expenses in this selection", ha="center", va="center", color="#64748b")
            ax.axis("off")
        else:
            ax.pie(data["total"], labels=data["label"], autopct="%1.0f%%", startangle=90,
                   colors=["#138a72", "#f0a44b", "#526bda", "#d46b83", "#62a6aa", "#9475c6"])
            ax.axis("equal")
        ax.set_title("Share of spending by category", loc="left", fontsize=13, fontweight="bold", color="#172b3a")
    elif chart_name == "month-bar":
        data = summary["months"]
        ax.bar(data["label"], data["total"], color="#138a72", width=.68)
        ax.set_title("Monthly spending", loc="left", fontsize=13, fontweight="bold", color="#172b3a")
        ax.set_xlabel("Month")
        ax.set_ylabel("Amount (₹)")
        ax.tick_params(axis="x", rotation=35)
        ax.grid(axis="y", alpha=.18)
    else:
        data = summary["categories"].sort_values("total")
        ax.barh(data["label"], data["total"], color="#526bda")
        ax.set_title("Spending by category", loc="left", fontsize=13, fontweight="bold", color="#172b3a")
        ax.set_xlabel("Amount (₹)")
        ax.set_ylabel("Category")
        ax.grid(axis="x", alpha=.18)
    output = BytesIO()
    fig.savefig(output, format="png", dpi=140, facecolor=fig.get_facecolor())
    plt.close(fig)
    return output.getvalue()
