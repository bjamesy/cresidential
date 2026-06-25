from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import plaid, transactions, jobs

app = FastAPI(title="Rental Verification API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(plaid.router, prefix="/plaid")
app.include_router(transactions.router, prefix="/transactions")
app.include_router(jobs.router, prefix="/jobs")


@app.get("/health")
def health():
    return {"status": "ok"}
