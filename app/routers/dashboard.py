from fastapi import APIRouter

from app.models import CategorySummaryItem, DashboardSummary, RecentExpense
from app import storage

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary", response_model=DashboardSummary)
def dashboard_summary() -> DashboardSummary:
    return DashboardSummary(**storage.get_dashboard_summary())


@router.get("/recent", response_model=list[RecentExpense])
def recent_expenses() -> list[RecentExpense]:
    return [RecentExpense(**item) for item in storage.get_recent_expenses()]


@router.get("/category-summary", response_model=list[CategorySummaryItem])
def category_summary() -> list[CategorySummaryItem]:
    return [CategorySummaryItem(**item) for item in storage.get_category_summary()]
