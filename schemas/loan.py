from pydantic import BaseModel
from datetime import date

class LoanCreate(BaseModel):
    person_name: str
    amount: float
    date: date
    status: str
    reason: str