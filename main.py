from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base, SessionLocal

# Models
from models.mess import MessSession
from models.holiday import Holiday
from models.expense import Expense
from models.loan import Loan
from models.mess_history import MessHistory

# Schemas
from schemas.mess import MessSessionCreate
from schemas.holiday import HolidayCreate
from schemas.expense import ExpenseCreate
from schemas.loan import LoanCreate
from schemas.mess_history import MessHistoryCreate

# CSV utils
from fastapi.responses import FileResponse
from utils.export_csv import export_expenses_csv, export_loans_csv

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Root
@app.get("/")
def home():
    return {"message": "Personal Ledger API Running"}


# =========================
# MESS SESSION
# =========================

@app.post("/mess-session")
def create_mess_session(data: MessSessionCreate, db: Session = Depends(get_db)):

    # FIXED (correct 30-day logic)
    end_date = data.start_date + timedelta(days=data.mess_days - 1)

    mess = MessSession(
        start_date=data.start_date,
        end_date=end_date,
        mess_days=data.mess_days
    )

    db.add(mess)
    db.commit()
    db.refresh(mess)

    return mess


@app.get("/mess-sessions")
def get_mess_sessions(db: Session = Depends(get_db)):
    return db.query(MessSession).all()

@app.post("/mess/finalize")
def finalize_mess(data: MessHistoryCreate, db: Session = Depends(get_db)):

    record = MessHistory(
        start_date=data.start_date,
        end_date=data.end_date,
        total_days=data.total_days,
        holiday_days=data.holiday_days,
        effective_days=data.effective_days,
        holidays=data.holidays
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record

@app.get("/mess/history")
def get_mess_history(db: Session = Depends(get_db)):
    return db.query(MessHistory).order_by(MessHistory.id.desc()).all()

# DELETE
@app.delete("/mess/{id}")
def delete_mess(id: int, db: Session = Depends(get_db)):
    mess = db.query(MessHistory).filter(MessHistory.id == id).first()

    if not mess:
        raise HTTPException(status_code=404, detail="Not found")

    db.delete(mess)
    db.commit()

    return {"message": "Deleted successfully"}

# UPDATE
@app.put("/mess/{id}")
def update_mess(id: int, payload: dict, db: Session = Depends(get_db)):
    mess = db.query(MessHistory).filter(MessHistory.id == id).first()

    if not mess:
        raise HTTPException(status_code=404, detail="Not found")

    for key, value in payload.items():
        setattr(mess, key, value)

    db.commit()
    db.refresh(mess)

    return mess


# =========================
# HOLIDAYS
# =========================

@app.post("/holiday")
def add_holiday(data: HolidayCreate, db: Session = Depends(get_db)):

    days = (data.end_date - data.start_date).days + 1

    holiday = Holiday(
        mess_id=data.mess_id,
        start_date=data.start_date,
        end_date=data.end_date,
        days=days
    )

    db.add(holiday)
    db.commit()
    db.refresh(holiday)

    return holiday


# ✅ IMPORTANT: Added missing endpoint
@app.get("/holidays/{mess_id}")
def get_holidays(mess_id: int, db: Session = Depends(get_db)):
    return db.query(Holiday).filter(Holiday.mess_id == mess_id).all()


# =========================
# EXPENSES
# =========================

@app.post("/expense")
def create_expense(data: ExpenseCreate, db: Session = Depends(get_db)):

    expense = Expense(
        amount=data.amount,
        description=data.description,
        date=data.date
    )

    db.add(expense)
    db.commit()
    db.refresh(expense)

    return expense


@app.get("/expenses")
def get_expenses(db: Session = Depends(get_db)):
    return db.query(Expense).all()


# =========================
# LOANS
# =========================

@app.post("/loan")
def create_loan(data: LoanCreate, db: Session = Depends(get_db)):

    new_loan = Loan(
        person_name=data.person_name,
        amount=data.amount,
        date=data.date,
        status=data.status,
        reason=data.reason
    )

    db.add(new_loan)
    db.commit()
    db.refresh(new_loan)

    return new_loan


@app.get("/loans")
def get_loans(db: Session = Depends(get_db)):
    return db.query(Loan).all()


# =========================
# EXPORT CSV
# =========================

@app.get("/export/expenses")
def export_expenses(db: Session = Depends(get_db)):

    file_path = export_expenses_csv(db)

    return FileResponse(
        file_path,
        media_type="text/csv",
        filename="expenses.csv"
    )


@app.get("/export/loans")
def export_loans(db: Session = Depends(get_db)):

    file_path = export_loans_csv(db)

    return FileResponse(
        file_path,
        media_type="text/csv",
        filename="loans.csv"
    )