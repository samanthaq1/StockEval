# Deployment Guide: GitHub Pages + Render

## Overview
- **Frontend**: React/Vite app hosted on GitHub Pages at `https://samanthaq1.github.io/StockEval/`
- **Backend**: FastAPI mock API hosted on Render's free tier

## Step 1: Deploy Backend to Render

### 1.1 Sign up at Render
- Go to [render.com](https://render.com)
- Sign up with GitHub (easiest — gives direct repo integration)

### 1.2 Create a new Web Service
- Click **"New +"** → **"Web Service"**
- Connect your GitHub account and select the **StockEval** repo
- Render will detect it's a Python project

### 1.3 Configure the service
Fill in the following fields:
- **Name**: `stockeval-backend` (or any name)
- **Environment**: `Python 3`
- **Build command**: 
  ```
  pip install -r backend/requirements.txt
  ```
- **Start command**: 
  ```
  uvicorn main:app --host 0.0.0.0 --port $PORT
  ```
- **Root directory**: `backend` (optional, but helps Render locate `requirements.txt`)

### 1.4 Set environment variables
- Scroll to **"Environment"** section
- Click **"Add Environment Variable"**
- Add:
  - **Key**: `FRONTEND_ORIGIN`
  - **Value**: `https://samanthaq1.github.io/StockEval`

### 1.5 Deploy
- Click **"Create Web Service"**
- Render will build and deploy (takes ~2–3 min)
- Once live, you'll get a URL like: `https://stockeval-backend-xxxx.onrender.com`
- Copy this URL; you'll need it next

## Step 2: Update Frontend with Backend URL

### 2.1 Update the API endpoint in frontend code
Edit `frontend/src/App.tsx` and replace the backend URL:

```typescript
// OLD:
const res = await fetch('http://127.0.0.1:8000/api/allocate', {

// NEW (use Render URL):
const res = await fetch('https://stockeval-backend-xxxx.onrender.com/api/allocate', {
```

Replace `stockeval-backend-xxxx.onrender.com` with your actual Render service URL.

### 2.2 Push to GitHub
```powershell
git add .
git commit -m "Update backend URL for Render deployment"
git push origin main
```

The GitHub Actions workflow will automatically build and deploy the frontend to GitHub Pages.

## Step 3: Verify deployment

1. Wait for GitHub Actions to complete (check the **Actions** tab)
2. Visit your live frontend: `https://samanthaq1.github.io/StockEval/`
3. Open the browser console (F12) for errors
4. Submit the allocation form
5. You should see mock allocations returned from the Render backend

## Troubleshooting

### CORS errors in browser console
- **Symptom**: `Access to XMLHttpRequest... has been blocked by CORS policy`
- **Fix**: Verify the `FRONTEND_ORIGIN` environment variable on Render matches your Pages URL exactly
  - Render dashboard → your web service → **Environment** tab
  - Check the value is `https://samanthaq1.github.io/StockEval` (no trailing slash)
  - Redeploy: click **"Redeploy latest commit"**

### Backend returns 503 or times out
- **Symptom**: Render service unavailable
- **Cause**: Free tier auto-sleeps after 15 min of inactivity; first request takes ~50ms to wake up
- **Fix**: This is normal. Just wait a few seconds and try again. If it persists, check Render logs:
  - Render dashboard → your service → **Logs** tab
  - Look for Python/startup errors

### Backend URL not found
- **Symptom**: 404 on `/api/allocate`
- **Fix**: Make sure the start command is correct and includes `--host 0.0.0.0`

## Optional: Use environment variables in frontend (advanced)

To avoid hardcoding the backend URL in the frontend, you can use a `.env` file during build:

1. Create `frontend/.env.production`:
   ```
   VITE_API_URL=https://stockeval-backend-xxxx.onrender.com
   ```

2. Update `frontend/src/App.tsx`:
   ```typescript
   const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'
   const res = await fetch(`${API_URL}/api/allocate`, {
   ```

3. Update GitHub Actions to pass the URL as a build variable (requires storing it as a GitHub secret or Actions variable).

For now, hardcoding the URL is fine for a prototype.

## Next: Add real features

Once the deployment is working, you can:
- Add real price data fetching (yfinance, IEX Cloud)
- Build a portfolio dashboard
- Add user authentication
- Connect to a database (PostgreSQL on Render's free tier or MongoDB Atlas)
- Deploy a Python analytics service for backtests and simulations

