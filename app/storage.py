import json
from collections import Counter
from datetime import date
from pathlib import Path

from fastapi import HTTPException

from app.models import Expense, ExpenseCreate, ExpenseUpdate

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
EXPENSES_FILE = DATA_DIR / "expenses.json"
CATEGORIES_FILE = DATA_DIR / "categories.json"

DEFAULT_CATEGORIES = [
    "Food",
    "Travel",
    "Shopping",
    "Bills",
    "Entertainment",
    "Healthcare",
    "Education",
]


def _ensure_data_files() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not EXPENSES_FILE.exists():
        EXPENSES_FILE.write_text("[]", encoding="utf-8")
    if not CATEGORIES_FILE.exists():
        CATEGORIES_FILE.write_text(
            json.dumps(DEFAULT_CATEGORIES, indent=2),
            encoding="utf-8",
        )


def _read_expenses() -> list[dict]:
    _ensure_data_files()
    with EXPENSES_FILE.open(encoding="utf-8") as file:
        return json.load(file)


def _write_expenses(expenses: list[dict]) -> None:
    with EXPENSES_FILE.open("w", encoding="utf-8") as file:
        json.dump(expenses, file, indent=2)


def _parse_date(value: str) -> date:
    return date.fromisoformat(value)


def get_all_expenses(
    *,
    category: str | None = None,
    expense_date: date | None = None,
) -> list[Expense]:
    expenses = [_to_expense(item) for item in _read_expenses()]

    if category is not None:
        expenses = [e for e in expenses if e.category.lower() == category.lower()]

    if expense_date is not None:
        expenses = [e for e in expenses if e.date == expense_date]

    return expenses


def get_expense_by_id(expense_id: int) -> Expense:
    for item in _read_expenses():
        if item["id"] == expense_id:
            return _to_expense(item)
    raise HTTPException(status_code=404, detail="Expense not found")


def create_expense(payload: ExpenseCreate) -> None:
    expenses = _read_expenses()
    next_id = max((item["id"] for item in expenses), default=0) + 1
    expenses.append(
        {
            "id": next_id,
            "title": payload.title,
            "amount": payload.amount,
            "category": payload.category,
            "date": payload.date.isoformat(),
            "description": payload.description,
        }
    )
    _write_expenses(expenses)


def update_expense(expense_id: int, payload: ExpenseUpdate) -> None:
    expenses = _read_expenses()
    for index, item in enumerate(expenses):
        if item["id"] == expense_id:
            expenses[index] = {
                "id": expense_id,
                "title": payload.title,
                "amount": payload.amount,
                "category": payload.category,
                "date": payload.date.isoformat(),
                "description": payload.description,
            }
            _write_expenses(expenses)
            return
    raise HTTPException(status_code=404, detail="Expense not found")


def delete_expense(expense_id: int) -> None:
    expenses = _read_expenses()
    updated = [item for item in expenses if item["id"] != expense_id]
    if len(updated) == len(expenses):
        raise HTTPException(status_code=404, detail="Expense not found")
    _write_expenses(updated)


def get_categories() -> list[str]:
    _ensure_data_files()
    with CATEGORIES_FILE.open(encoding="utf-8") as file:
        return json.load(file)


def get_dashboard_summary() -> dict:
    expenses = get_all_expenses()
    total_transactions = len(expenses)
    total_expenses = sum(e.amount for e in expenses)
    average_expense = total_expenses / total_transactions if total_transactions else 0.0

    if expenses:
        category_counts = Counter(e.category for e in expenses)
        top_category = category_counts.most_common(1)[0][0]
    else:
        top_category = ""

    return {
        "totalExpenses": total_expenses,
        "totalTransactions": total_transactions,
        "averageExpense": round(average_expense, 2),
        "topCategory": top_category,
    }


def get_recent_expenses(limit: int = 5) -> list[dict]:
    expenses = get_all_expenses()
    expenses.sort(key=lambda e: (e.date, e.id), reverse=True)
    return [
        {"id": e.id, "title": e.title, "amount": e.amount}
        for e in expenses[:limit]
    ]


def get_category_summary() -> list[dict]:
    totals: dict[str, float] = {}
    for expense in get_all_expenses():
        totals[expense.category] = totals.get(expense.category, 0.0) + expense.amount
    return [
        {"category": category, "total": total}
        for category, total in sorted(totals.items(), key=lambda item: item[1], reverse=True)
    ]


def _to_expense(item: dict) -> Expense:
    return Expense(
        id=item["id"],
        title=item["title"],
        amount=item["amount"],
        category=item["category"],
        date=_parse_date(item["date"]),
        description=item.get("description", ""),
    )
