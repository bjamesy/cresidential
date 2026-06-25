import uuid
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from app import store
from app.services.pipeline import run_pipeline

router = APIRouter()


class AnalyzeRequest(BaseModel):
    session_id: str


@router.post("/analyze")
def analyze(body: AnalyzeRequest, background_tasks: BackgroundTasks):
    access_token = store.sessions.get(body.session_id)
    if not access_token:
        raise HTTPException(status_code=404, detail="Session not found")

    job_id = str(uuid.uuid4())
    store.jobs[job_id] = {"job_id": job_id, "status": "pending"}
    background_tasks.add_task(run_pipeline, job_id, access_token)
    return {"job_id": job_id}
