from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class User(Base):
    """User account information."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    username = Column(String(100), unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    portfolios = relationship("Portfolio", back_populates="user", cascade="all, delete-orphan")
    accounts = relationship("Account", back_populates="user", cascade="all, delete-orphan")


class Account(Base):
    """Brokerage account information."""
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    broker = Column(String(100))  # e.g., "Fidelity", "Charles Schwab"
    account_type = Column(String(50))  # e.g., "brokerage", "401k", "IRA"
    color_tag = Column(String(20))  # e.g., "blue", "red", "green" for UI display
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="accounts")
    holdings = relationship("Holding", back_populates="account", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="account", cascade="all, delete-orphan")


class Portfolio(Base):
    """Portfolio / allocation plan."""
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String(255))
    risk_level = Column(String(50))  # "conservative", "balanced", "aggressive"
    total_amount = Column(Numeric(15, 2))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="portfolios")
    allocations = relationship("Allocation", back_populates="portfolio", cascade="all, delete-orphan")


class Allocation(Base):
    """Suggested allocation for a portfolio."""
    __tablename__ = "allocations"

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"))
    ticker = Column(String(10), index=True)
    percent = Column(Float)  # e.g., 0.4 for 40%
    amount = Column(Numeric(15, 2))
    created_at = Column(DateTime, default=datetime.utcnow)

    portfolio = relationship("Portfolio", back_populates="allocations")


class Holding(Base):
    """Stock holding in an account."""
    __tablename__ = "holdings"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    ticker = Column(String(10), index=True)
    shares = Column(Numeric(15, 4))
    avg_price = Column(Numeric(15, 2))
    currency = Column(String(10), default="USD")
    created_at = Column(DateTime, default=datetime.utcnow)

    account = relationship("Account", back_populates="holdings")


class Transaction(Base):
    """Buy/sell transaction."""
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    ticker = Column(String(10), index=True)
    type = Column(String(10))  # "buy", "sell", "dividend"
    date = Column(DateTime, index=True)
    shares = Column(Numeric(15, 4))
    price = Column(Numeric(15, 2))
    amount = Column(Numeric(15, 2))  # total (shares * price)
    fees = Column(Numeric(15, 2), default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    account = relationship("Account", back_populates="transactions")


class Ticker(Base):
    """Stock ticker metadata."""
    __tablename__ = "tickers"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(10), unique=True, index=True)
    name = Column(String(255))
    sector = Column(String(100))
    market_cap = Column(Numeric(20, 2), nullable=True)
    custom_rating = Column(Float, nullable=True)  # your own 1-5 rating
    div_yield = Column(Float, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class PriceSeries(Base):
    """Historical price data."""
    __tablename__ = "price_series"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(10), ForeignKey("tickers.ticker"), index=True)
    date = Column(DateTime, index=True)
    close_price = Column(Numeric(15, 2))
    volume = Column(Integer, nullable=True)

    __table_args__ = (
        # Composite unique constraint
        {"mysql_charset": "utf8mb4"},
    )


class Dividend(Base):
    """Dividend payment history."""
    __tablename__ = "dividends"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(10), ForeignKey("tickers.ticker"), index=True)
    ex_date = Column(DateTime)
    pay_date = Column(DateTime)
    amount = Column(Numeric(15, 4))
    currency = Column(String(10), default="USD")
    created_at = Column(DateTime, default=datetime.utcnow)
