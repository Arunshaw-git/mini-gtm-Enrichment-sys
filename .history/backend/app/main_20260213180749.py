from fastapi import FastAPI
from app.workers.tasks import test_task
from .database import engine
from . import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def health():
    return {"status": "ok"}



@app.post("/test-task")
def trigger_test_task(domain: str):
    test_task.delay(domain)
    return {"message": "Task submitted", "domain": domain}