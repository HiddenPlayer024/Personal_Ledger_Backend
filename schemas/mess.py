from pydantic import BaseModel
from datetime import date

class MessSessionCreate(BaseModel):
    start_date: date
    mess_days: int = 30