from pydantic import BaseModel
from datetime import date

class ExpenseCreate(BaseModel):
    amount: float
    description: str
    date: date