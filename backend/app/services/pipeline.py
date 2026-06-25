from app import store
from app.services.plaid_service import fetch_transactions
from app.services.detection_service import detect_rent_candidates
from datetime import date, timedelta


def run_pipeline(job_id: str, access_token: str):
    try:
        store.jobs[job_id]["status"] = "fetching"
        transactions = fetch_transactions(access_token)

        store.jobs[job_id]["status"] = "detecting"
        candidates = detect_rent_candidates(transactions)

        end_date = date.today()
        start_date = end_date - timedelta(days=365 * 2)

        store.jobs[job_id] = {
            "job_id": job_id,
            "status": "complete",
            "result": {
                "period": {"start": str(start_date), "end": str(end_date)},
                "total_transactions_analyzed": len(transactions),
                "candidates": candidates,
            },
        }
    except Exception as e:
        store.jobs[job_id] = {
            "job_id": job_id,
            "status": "error",
            "error": str(e),
        }
