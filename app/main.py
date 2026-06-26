from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import categories, dashboard, expenses
from app import storage

app = FastAPI(
    title="Expense Tracker API",
    version="1.0.0",
    description="API for managing expenses, dashboard statistics, and categories.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(expenses.router)
app.include_router(dashboard.router)
app.include_router(categories.router)


@app.on_event("startup")
def on_startup() -> None:
    storage._ensure_data_files()


def run() -> None:
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    run()
