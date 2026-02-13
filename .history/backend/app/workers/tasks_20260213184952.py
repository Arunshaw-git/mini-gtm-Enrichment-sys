from app.workers.celery_app import celery
from app.database import SessionLocal
from app.models import Company
from app.services.explorium import enrich_company


@celery.task(bind=True, max_retries=3)
def enrich_company_task(company_id: str):
    db = SessionLocal()

    try:
        company = db.query(Company).filter(Company.id == company_id).first()

        if not company:
            return

        company.status = "processing"
        db.commit()

        data = enrich_company(company.domain)

        company.industry = data.get("industry")
        company.company_size = data.get("company_size")
        company.revenue_range = data.get("revenue_range")
        company.status = "completed"

        db.commit()

    except Exception as e:
        company.status = "failed"
        db.commit()
        raise self.retry(exc=e, countdown=5)

    finally:
        db.close()