# schemas/mess_history.py

from pydantic import BaseModel
from datetime import date
from typing import List, Dict

class MessHistoryCreate(BaseModel):
    start_date: date
    end_date: date
    total_days: int
    holiday_days: int
    effective_days: int
    holidays: List[Dict]