from app.models import Company
from app.database import SessionLocal
from app.workers.tasks import enrich_company_task

db = SessionLocal()

company = Company(domain=domain)
db.add(company)
db.commit()
db.refresh(company)

enrich_company_task.delay(str(company.id))