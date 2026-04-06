"""
bi-finance-intelligence — showcase_code.py
Key pipeline components for reference.
"""

# 1. Multi-source data ingestion
from sqlalchemy import create_engine, Column, Float, String, DateTime
from sqlalchemy.orm import declarative_base, Session
from datetime import datetime

Base = declarative_base()

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(String, primary_key=True)
    source = Column(String)          # erp | bank | stripe | paypal
    amount = Column(Float)
    currency = Column(String)
    date = Column(DateTime)
    category = Column(String)
    reconciled = Column(String, default="pending")

def get_engine(db_path="/data/finance.db"):
    return create_engine(f"sqlite:///{db_path}")

# 2. Reconciliation engine
def reconcile(session: Session) -> dict:
    pending = session.query(Transaction).filter_by(reconciled="pending").all()
    errors = 0
    for txn in pending:
        # Cross-reference logic (simplified)
        duplicate = session.query(Transaction).filter(
            Transaction.id != txn.id,
            Transaction.amount == txn.amount,
            Transaction.date == txn.date
        ).first()
        if duplicate:
            errors += 1
            txn.reconciled = "error"
        else:
            txn.reconciled = "ok"
    session.commit()
    return {"processed": len(pending), "errors": errors}

# 3. Cash flow forecast (linear extrapolation)
import pandas as pd

def forecast_cashflow(monthly_data: list[dict], months_ahead: int = 3) -> list[dict]:
    df = pd.DataFrame(monthly_data)
    df["date"] = pd.to_datetime(df["month"])
    df = df.sort_values("date")
    avg_net = df["net"].tail(6).mean()
    last_balance = df["balance"].iloc[-1]
    forecast = []
    for i in range(1, months_ahead + 1):
        last_balance += avg_net
        forecast.append({"month": f"M+{i}", "projected_balance": round(last_balance, 2)})
    return forecast

# 4. FastAPI endpoint
from fastapi import FastAPI
app = FastAPI()

@app.get("/api/kpis")
def get_kpis():
    engine = get_engine()
    with Session(engine) as session:
        total = session.query(Transaction).count()
        total_inflow = sum(t.amount for t in session.query(Transaction).filter(Transaction.amount > 0))
        return {"transactions": total, "total_inflow": round(total_inflow, 2)}
