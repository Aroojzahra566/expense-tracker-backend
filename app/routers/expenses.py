from datetime import date
from typing import Annotated

from fastapi import APIRouter, Query

from app.models import Expense, ExpenseCreate, ExpenseUpdate, MessageResponse
from app import storage

router = APIRouter(prefix="/expenses", tags=["Expenses"])


@router.get("", response_model=list[Expense])
def list_expenses(
    category: str | None = Query(default=None),
    expense_date: Annotated[
        date | None,
        Query(
            alias="date",
            description="Filter by full date in YYYY-MM-DD format (e.g. 2026-06-22)",
            examples=["2026-06-22"],
        ),
    ] = None,
) -> list[Expense]:
    return storage.get_all_expenses(
        category=category,
        expense_date=expense_date,
    )


@router.get("/{expense_id}", response_model=Expense)
def get_expense(expense_id: int) -> Expense:
    return storage.get_expense_by_id(expense_id)


@router.post("", response_model=MessageResponse, status_code=201)
def create_expense(payload: ExpenseCreate) -> MessageResponse:
    storage.create_expense(payload)
    return MessageResponse(message="Expense created successfully")


@router.put("/{expense_id}", response_model=MessageResponse)
def update_expense(expense_id: int, payload: ExpenseUpdate) -> MessageResponse:
    storage.update_expense(expense_id, payload)
    return MessageResponse(message="Expense updated successfully")


@router.delete("/{expense_id}", response_model=MessageResponse)
def delete_expense(expense_id: int) -> MessageResponse:
    storage.delete_expense(expense_id)
    return MessageResponse(message="Expense deleted successfully")
