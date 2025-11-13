"""
Database initialization script.
Run this once to create all tables:
    python init_db.py
"""
from database import engine, Base
from models import User, Account, Portfolio, Allocation, Holding, Transaction, Ticker, PriceSeries, Dividend


def init_db():
    """Create all tables in the database."""
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


if __name__ == "__main__":
    init_db()
