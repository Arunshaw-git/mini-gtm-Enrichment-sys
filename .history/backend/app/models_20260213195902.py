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

    status = Column(String, default="pending") 

    created_at = Column(DateTime(timezone=True),
    updated_at = Column(
    DateTime(timezone=True),
    server_default=func.now(),
    onupdate=func.now()),
    server_default=func.now())