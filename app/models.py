from datetime import date

from pydantic import BaseModel, Field


class ExpenseBase(BaseModel):
    title: str
    amount: float = Field(gt=0)
    category: str
    date: date
    description: str = ""


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(ExpenseBase):
    pass


class Expense(ExpenseBase):
    id: int


class MessageResponse(BaseModel):
    message: str


class RecentExpense(BaseModel):
    id: int
    title: str
    amount: float


class DashboardSummary(BaseModel):
    totalExpenses: float
    totalTransactions: int
    averageExpense: float
    topCategory: str


class CategorySummaryItem(BaseModel):
    category: str
    total: float
