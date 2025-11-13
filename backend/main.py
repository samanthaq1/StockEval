from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import os

# Import database and models
from database import engine, get_db, Base
from models import User, Account, Portfolio, Allocation, Holding, Transaction, Ticker, Dividend
from schemas import (
    UserCreate, UserResponse, PortfolioCreate, PortfolioResponse, 
    AllocationItem, HoldingCreate, HoldingResponse, AccountCreate, 
    AccountResponse, TransactionCreate, TransactionResponse
)

# Create all tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="StockEval API")

# Configure CORS: allow local dev and optionally GitHub Pages frontend
FRONTEND_ORIGIN = os.environ.get("FRONTEND_ORIGIN")
allowed = ["http://localhost:5173", "http://127.0.0.1:5173"]
if FRONTEND_ORIGIN:
    allowed.append(FRONTEND_ORIGIN)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============= Legacy allocation endpoint (mock) =============

class AllocationRequest(BaseModel):
    amount: float
    risk: str


class AllocationResponse(BaseModel):
    requested: AllocationRequest
    allocations: List[AllocationItem]
    created_at: datetime


@app.post("/api/allocate", response_model=AllocationResponse)
def allocate(req: AllocationRequest):
    """Legacy mock allocation endpoint for frontend compatibility."""
    amt = float(req.amount)
    risk = req.risk.lower()

    if risk == "conservative":
        weights = [
            ("BND", 0.6),
            ("VOO", 0.2),
            ("VXUS", 0.2),
        ]
    elif risk == "aggressive":
        weights = [
            ("QQQ", 0.5),
            ("VOO", 0.3),
            ("EEM", 0.2),
        ]
    else:  # balanced
        weights = [
            ("VOO", 0.4),
            ("BND", 0.3),
            ("VXUS", 0.2),
            ("QQQ", 0.1),
        ]

    allocations = []
    for ticker, pct in weights:
        allocations.append(AllocationItem(ticker=ticker, percent=round(pct * 100, 2), amount=round(amt * pct, 2)))

    return AllocationResponse(requested=req, allocations=allocations, created_at=datetime.utcnow())


# ============= User endpoints =============

@app.post("/api/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user."""
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(email=user.email, username=user.username)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/api/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get a user by ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# ============= Account endpoints =============

@app.post("/api/users/{user_id}/accounts", response_model=AccountResponse)
def create_account(user_id: int, account: AccountCreate, db: Session = Depends(get_db)):
    """Create a new account for a user."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    new_account = Account(user_id=user_id, **account.dict())
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return new_account


@app.get("/api/users/{user_id}/accounts", response_model=List[AccountResponse])
def list_accounts(user_id: int, db: Session = Depends(get_db)):
    """List all accounts for a user."""
    accounts = db.query(Account).filter(Account.user_id == user_id).all()
    return accounts


@app.get("/api/accounts/{account_id}", response_model=AccountResponse)
def get_account(account_id: int, db: Session = Depends(get_db)):
    """Get an account by ID."""
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


# ============= Portfolio endpoints =============

@app.post("/api/users/{user_id}/portfolios", response_model=PortfolioResponse)
def create_portfolio(user_id: int, portfolio: PortfolioCreate, db: Session = Depends(get_db)):
    """Create a new portfolio for a user."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    new_portfolio = Portfolio(user_id=user_id, **portfolio.dict())
    db.add(new_portfolio)
    db.commit()
    db.refresh(new_portfolio)
    return new_portfolio


@app.get("/api/portfolios/{portfolio_id}", response_model=PortfolioResponse)
def get_portfolio(portfolio_id: int, db: Session = Depends(get_db)):
    """Get a portfolio by ID with its allocations."""
    portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return portfolio


# ============= Holdings endpoints =============

@app.post("/api/accounts/{account_id}/holdings", response_model=HoldingResponse)
def add_holding(account_id: int, holding: HoldingCreate, db: Session = Depends(get_db)):
    """Add a holding to an account."""
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    new_holding = Holding(account_id=account_id, **holding.dict())
    db.add(new_holding)
    db.commit()
    db.refresh(new_holding)
    return new_holding


@app.get("/api/accounts/{account_id}/holdings", response_model=List[HoldingResponse])
def list_holdings(account_id: int, db: Session = Depends(get_db)):
    """List all holdings in an account."""
    holdings = db.query(Holding).filter(Holding.account_id == account_id).all()
    return holdings


# ============= Transaction endpoints =============

@app.post("/api/accounts/{account_id}/transactions", response_model=TransactionResponse)
def add_transaction(account_id: int, transaction: TransactionCreate, db: Session = Depends(get_db)):
    """Add a transaction to an account."""
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    # Calculate total amount
    amount = float(transaction.shares * transaction.price)
    new_transaction = Transaction(
        account_id=account_id,
        amount=amount,
        **transaction.dict()
    )
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction


@app.get("/api/accounts/{account_id}/transactions", response_model=List[TransactionResponse])
def list_transactions(account_id: int, db: Session = Depends(get_db)):
    """List all transactions for an account."""
    transactions = db.query(Transaction).filter(Transaction.account_id == account_id).all()
    return transactions


# ============= Health check =============

@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok"}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
