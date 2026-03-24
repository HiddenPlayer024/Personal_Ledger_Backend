from sqlalchemy import Column, Integer, Date, ForeignKey
from database import Base

class Holiday(Base):
    __tablename__ = "holidays"

    id = Column(Integer, primary_key=True, index=True)
    mess_id = Column(Integer, ForeignKey("mess_sessions.id"))
    start_date = Column(Date)
    end_date = Column(Date)
    days = Column(Integer)