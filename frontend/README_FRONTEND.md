# Frontend (React + TypeScript) — quick start

This folder contains a minimal Vite + React + TypeScript scaffold with a small allocation form and a Plotly sample chart.


Run locally (PowerShell):

```powershell
cd frontend
npm install
npm run dev
```

Open the URL printed by Vite (usually `http://localhost:5173`).

Deploy to GitHub Pages (automated)
- This repo includes a GitHub Actions workflow at `.github/workflows/deploy-frontend.yml` that builds the frontend and publishes `frontend/dist` to GitHub Pages when you push to `main`.
- Vite `base` is set to `/StockEval/` in `vite.config.ts`, so the Pages URL will be `https://<github-username>.github.io/StockEval/`.

If you prefer a different Pages path or a user site (e.g. `https://<github-username>.github.io/`), adjust `frontend/vite.config.ts` `base` accordingly before building and deploying.

Notes:
- This is a lightweight prototype. Extend by adding API calls to your backend to fetch real price data, allocation suggestions, and user portfolios.
- To build production bundle: `npm run build` and serve the `dist/` folder.

