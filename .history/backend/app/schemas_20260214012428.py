from pydantic import BaseModel
from typing import List

class DomainList(BaseModel):
    domains: List[str]