from fastapi import FastAPI
from routers import (
    users,
    categories,
    transactions
)


app = FastAPI()

app.include_router(users.router, prefix="/api/v1")
app.include_router(categories.router, prefix="/api/v1")
app.include_router(transactions.router, prefix="/api/v1")