# models/mess_history.py

from sqlalchemy import Column, Integer, Date, JSON
from database import Base

class MessHistory(Base):
    __tablename__ = "mess_history"

    id = Column(Integer, primary_key=True, index=True)

    start_date = Column(Date)
    end_date = Column(Date)

    total_days = Column(Integer)
    holiday_days = Column(Integer)
    effective_days = Column(Integer)

    holidays = Column(JSON)