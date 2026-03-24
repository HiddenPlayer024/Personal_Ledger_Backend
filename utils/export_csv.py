import pandas as pd
from sqlalchemy.orm import Session

from models.expense import Expense
from models.loan import Loan


def export_expenses_csv(db: Session):

    expenses = db.query(Expense).all()

    data = [
        {
            "id": e.id,
            "amount": e.amount,
            "description": e.description,
            "date": e.date
        }
        for e in expenses
    ]

    df = pd.DataFrame(data)

    file_path = "expenses.csv"

    df.to_csv(file_path, index=False)

    return file_path


def export_loans_csv(db: Session):

    loans = db.query(Loan).all()

    data = [
        {
            "id": l.id,
            "person_name": l.person_name,
            "amount": l.amount,
            "date": l.date,
            "status": l.status
        }
        for l in loans
    ]

    df = pd.DataFrame(data)

    file_path = "loans.csv"

    df.to_csv(file_path, index=False)

    return file_path