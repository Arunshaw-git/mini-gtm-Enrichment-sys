# app/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import csv
from io import StringIO
from typing import List
from uuid import UUID

from .database import SessionLocal, engine
from . import models
from app.models import Company
from app.workers.tasks import enrich_company_task

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Company Enrichment API")

# Health Check

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a CSV")

    content = await file.read()
    csv_file = StringIO(content.decode("utf-8"))
    reader = csv.DictReader(csv_file)

    domains_added: List[str] = []
    db = SessionLocal()

    for row in reader:
        domain = row.get("domain")
        if not domain:
            continue

        # Check if company exists
        existing = db.query(Company).filter(Company.domain == domain).first()
        if existing:
            continue

        # Add to DB
        company = Company(domain=domain)
        db.add(company)
        db.commit()
        db.refresh(company)

        # Trigger Celery task
        enrich_company_task.delay(str(company.id))
        domains_added.append(domain)

    db.close()
    return {"message": "Tasks submitted", "domains": domains_added}



# Trigger single enrichment task
@app.post("/trigger-task")
def trigger_task(domain: str):
    db = SessionLocal()
    company = db.query(Company).filter(Company.domain == domain).first()

    if not company:
        company = Company(domain=domain)
        db.add(company)
        db.commit()
        db.refresh(company)

    enrich_company_task.delay(str(company.id))
    db.close()
    return {"message": "Task submitted", "domain": domain}


#
# List all companies
# ------------------------
@app.get("/companies")
def list_companies(status: str = None):
    db = SessionLocal()
    query = db.query(Company)
    if status:
        query = query.filter(Company.status == status)
    companies = query.all()
    db.close()

    results = [
        {
            "id": str(c.id),
            "domain": c.domain,
            "industry": c.industry,
            "company_size": c.company_size,
            "revenue_range": c.revenue_range,
            "status": c.status,
            "created_at": c.created_at,
            "updated_at": getattr(c, "updated_at", None),
        }
        for c in companies
    ]
    return results


# ------------------------
# Get single company
# ------------------------
@app.get("/company/{company_id}")
def get_company(company_id: UUID):
    db = SessionLocal()
    company = db.query(Company).filter(Company.id == company_id).first()
    db.close()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    return {
        "id": str(company.id),
        "domain": company.domain,
        "industry": company.industry,
        "company_size": company.company_size,
        "revenue_range": company.revenue_range,
        "status": company.status,
        "created_at": company.created_at,
        "updated_at": getattr(company, "updated_at", None),
    }


# ------------------------
# Retry a failed task
# ------------------------
@app.post("/retry-task/{company_id}")
def retry_task(company_id: UUID):
    db = SessionLocal()
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        db.close()
        raise HTTPException(status_code=404, detail="Company not found")

    if company.status != "failed":
        db.close()
        return {"message": "Company task not in failed state"}

    company.status = "pending"
    db.commit()
    db.close()

    enrich_company_task.delay(str(company.id))
    return {"message": "Retry task submitted", "domain": company.domain}

