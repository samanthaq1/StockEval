# Backend Setup & Database Integration Guide

## Overview
The backend now uses SQLAlchemy ORM with PostgreSQL (or SQLite for local dev). All database tables are automatically created on startup.

## Local Setup with SQLite (quick test)

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python init_db.py
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

The database file will be created at `backend/test.db`. No database setup needed!

## PostgreSQL on Render (production)

1. **Create PostgreSQL on Render** (following DEPLOY.md steps 1–2)
2. **Set `DATABASE_URL` environment variable** on your Render web service
3. **Deploy** — tables will auto-create on startup

## API Endpoints

### Users
- `POST /api/users` — Create user
  ```json
  { "email": "user@example.com", "username": "john" }
  ```
- `GET /api/users/{user_id}` — Get user

### Accounts
- `POST /api/users/{user_id}/accounts` — Create brokerage account
  ```json
  { "broker": "Fidelity", "account_type": "brokerage", "color_tag": "blue" }
  ```
- `GET /api/users/{user_id}/accounts` — List user accounts
- `GET /api/accounts/{account_id}` — Get account details

### Holdings
- `POST /api/accounts/{account_id}/holdings` — Add a stock holding
  ```json
  { "ticker": "AAPL", "shares": 10.5, "avg_price": 150.25 }
  ```
- `GET /api/accounts/{account_id}/holdings` — List holdings

### Transactions
- `POST /api/accounts/{account_id}/transactions` — Record a buy/sell
  ```json
  {
    "ticker": "AAPL",
    "type": "buy",
    "date": "2024-01-15T10:00:00",
    "shares": 5,
    "price": 150.25,
    "fees": 0
  }
  ```
- `GET /api/accounts/{account_id}/transactions` — List transactions

### Portfolios
- `POST /api/users/{user_id}/portfolios` — Create portfolio plan
  ```json
  {
    "name": "My Balanced Portfolio",
    "risk_level": "balanced",
    "total_amount": 10000
  }
  ```
- `GET /api/portfolios/{portfolio_id}` — Get portfolio with allocations

## Example workflow (testing locally)

```bash
# 1. Create a user
curl -X POST http://127.0.0.1:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{"email":"sam@example.com","username":"sam"}'
# Response: { "id": 1, "email": "sam@example.com", ... }

# 2. Create an account for user 1
curl -X POST http://127.0.0.1:8000/api/users/1/accounts \
  -H "Content-Type: application/json" \
  -d '{"broker":"Fidelity","account_type":"brokerage","color_tag":"blue"}'
# Response: { "id": 1, "broker": "Fidelity", ... }

# 3. Add a holding
curl -X POST http://127.0.0.1:8000/api/accounts/1/holdings \
  -H "Content-Type: application/json" \
  -d '{"ticker":"AAPL","shares":10.5,"avg_price":150.25}'

# 4. Check holdings
curl http://127.0.0.1:8000/api/accounts/1/holdings
```

## Database Schema (auto-created)

Tables:
- `users` — User accounts
- `accounts` — Brokerage accounts (Fidelity, Schwab, etc.)
- `portfolios` — Allocation plans
- `allocations` — Individual allocations within a portfolio
- `holdings` — Current stock positions
- `transactions` — Buy/sell/dividend history
- `tickers` — Stock metadata (sector, rating, dividend yield)
- `price_series` — Historical price data
- `dividends` — Dividend payment history

## Adding Data Later

Once you have a few portfolios and holdings saved, you can:
- Build analytics endpoints to compute returns, allocations, dividend yield
- Add price fetching (yfinance, IEX) to populate `price_series`
- Create a dashboard to visualize holdings across accounts
- Export holdings as CSV

## Troubleshooting

**ImportError: cannot import name 'BaseModel' from 'pydantic'**
→ Run `pip install -r requirements.txt` to ensure all dependencies are installed.

**ModuleNotFoundError: No module named 'sqlalchemy'**
→ Ensure you're in the virtual environment: `.\.venv\Scripts\Activate.ps1`

**Database locked (SQLite only)**
→ SQLite doesn't handle concurrent writes well. For production, use PostgreSQL.

