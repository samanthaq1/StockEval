from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class UserCreate(BaseModel):
    email: str
    username: str


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    created_at: datetime

    class Config:
        from_attributes = True


class PortfolioCreate(BaseModel):
    name: str
    risk_level: str  # "conservative", "balanced", "aggressive"
    total_amount: float


class AllocationItem(BaseModel):
    ticker: str
    percent: float
    amount: float


class PortfolioResponse(BaseModel):
    id: int
    name: str
    risk_level: str
    total_amount: float
    allocations: List[AllocationItem] = []
    created_at: datetime

    class Config:
        from_attributes = True


class HoldingCreate(BaseModel):
    ticker: str
    shares: float
    avg_price: float


class HoldingResponse(BaseModel):
    id: int
    ticker: str
    shares: float
    avg_price: float
    currency: str

    class Config:
        from_attributes = True


class AccountCreate(BaseModel):
    broker: str
    account_type: str
    color_tag: str


class AccountResponse(BaseModel):
    id: int
    broker: str
    account_type: str
    color_tag: str
    holdings: List[HoldingResponse] = []
    created_at: datetime

    class Config:
        from_attributes = True


class TransactionCreate(BaseModel):
    ticker: str
    type: str  # "buy", "sell", "dividend"
    date: datetime
    shares: float
    price: float
    fees: float = 0


class TransactionResponse(BaseModel):
    id: int
    ticker: str
    type: str
    date: datetime
    shares: float
    price: float
    amount: float
    fees: float

    class Config:
        from_attributes = True
