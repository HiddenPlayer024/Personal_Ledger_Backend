from pydantic import BaseModel
from datetime import date

class HolidayCreate(BaseModel):
    mess_id: int
    start_date: date
    end_date: date