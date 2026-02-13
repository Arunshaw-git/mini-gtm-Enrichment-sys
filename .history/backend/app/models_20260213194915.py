import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from .database import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    domain = Column(String, nullable=False)

    industry = Column(String, nullable=True)
    company_size = Column(String, nullable=True)
    revenue_range = Column(String, nullable=True)

    status = Column(String, default="pending")  # pending | processing | done | failed

    created_at = Column(DateTime(timezone=True),
    from app.workers.celery_app import celery
from app.database import SessionLocal
from app.models import Company
from app.services.explorium import enrich_company


@celery.task(bind=True, max_retries=3)
def enrich_company_task(self, company_id: str):
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
        db.close(),
    server_default=func.now())