from sqlalchemy import Column, Integer, Float, String, Date
from database import Base

class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    person_name = Column(String)
    amount = Column(Float)
    date = Column(Date)
    status = Column(String)
    reason = Column(String)