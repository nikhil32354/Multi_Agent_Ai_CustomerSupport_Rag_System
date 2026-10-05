# Agentic AI Customer Support System

React/Vite frontend, FastAPI API, Groq-powered FAQ with retrieval from local PDF/DOCX/TXT/Markdown knowledge files, and ticket creation backed by SQLAlchemy.

## Local development

1. Copy `.env.example` to `backend/.env` and add a Groq API key to `GROQ_API_KEY` (never commit that file).
2. Install Python dependencies from `backend/requirements.txt`.
3. Start the API from `backend/` with `uvicorn app.main:app --reload --port 8000`.
4. From `frontend/`, run `npm ci` then `npm run dev`.
5. Open `http://localhost:3000`. The API docs are at `http://localhost:8000/docs`.

Local development defaults to SQLite. Add approved business documents to `backend/knowledge_base/`; restart the API after changing them. The included NovaOne PDF is fictional sample material, not real business policy.

## Deploy to Render

`render.yaml` describes a Render API web service, a static frontend, and a PostgreSQL database. Connect the GitHub repository to Render and create a Blueprint from this file.

1. In Render, create a **Blueprint Instance** for the connected repository and select `render.yaml`.
2. Set `GROQ_API_KEY` to a newly generated key when prompted. Do not place API keys in GitHub, this file, or `.env.example`.
3. Deploy the services. The static site is configured for the API name `agentic-support-api`; if Render assigns a different API URL, set the frontend build variable `VITE_API_BASE_URL` to `<API URL>/api` and redeploy the static site.
4. After the frontend URL is assigned, set the backend `FRONTEND_ORIGIN` environment variable to that exact `https://...onrender.com` origin, then redeploy the backend.
5. Check `<API URL>/health` and open the static site to test an FAQ and ticket creation.

The blueprint uses Render's free plans for a demo. Render free web services can sleep when idle; free Postgres expires after 30 days. **Do not use the free database for real customer data or production.** Before a real launch, select a paid persistent Postgres plan and review Render's current pricing and data-retention limits.

## GitHub safety

`.gitignore` excludes local `.env` files, SQLite databases, Python virtual environments, Node dependencies, and frontend build output. Before pushing, check `git status` and confirm no `.env` file or API key is staged. If a key has ever been committed or exposed, revoke it and generate a replacement before deploying.
