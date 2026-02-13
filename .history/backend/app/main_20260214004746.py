from fastapi import FastAPI
from .database import engine
from app.workers.tasks import enrich_company_task
from . import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/test-task")
def trigger_test_task(domain: str):
    enrich_company_task.delay(domain)
    return {"message": "Task submitted", "domain": domain}