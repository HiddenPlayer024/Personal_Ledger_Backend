from sqlalchemy import Column, Integer, Date
from database import Base

class MessSession(Base):
    __tablename__ = "mess_sessions"

    id = Column(Integer, primary_key=True, index=True)
    start_date = Column(Date)
    end_date = Column(Date)
    mess_days = Column(Integer)