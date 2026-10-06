# Agentic AI Customer Support System

React/Vite frontend, FastAPI API, Groq-powered FAQ with retrieval from local PDF/DOCX/TXT/Markdown knowledge files, and ticket creation backed by SQLAlchemy.

## Local development

1. Copy `.env.example` to `backend/.env` and add a Groq API key to `GROQ_API_KEY` (never commit that file).
2. Install Python dependencies from `backend/requirements.txt`.
3. Start the API from `backend/` with `uvicorn app.main:app --reload --port 8000`.
4. From `frontend/`, run `npm ci` then `npm run dev`.
5. Open `http://localhost:3000`. The API docs are at `http://localhost:8000/docs`.

Local development defaults to SQLite. Add approved business documents to `backend/knowledge_base/`; restart the API after changing them. The included NovaOne PDF is fictional sample material, not real business policy.

## Deploy the backend to Koyeb

The root `Dockerfile` builds the FastAPI backend. Connect the GitHub repository to Koyeb, create a Web Service from the repository, choose the Dockerfile build method, and use the repository root as the build context.

Configure the service with an HTTP port of `8000` and set these environment variables:

- `GROQ_API_KEY`: your Groq API key. Set it as a Koyeb secret; never commit it.
- `LLM_PROVIDER`: `groq`
- `FRONTEND_ORIGIN`: the exact origin of your Netlify site, without a trailing slash (for example, `https://your-site.netlify.app`).
- `DATABASE_URL`: optional for a demo; defaults to a local SQLite file.

Deploy the service, then check `https://<your-koyeb-service-domain>/health`. In Netlify, set `VITE_API_BASE_URL` to `https://<your-koyeb-service-domain>/api` and redeploy the frontend.

The default SQLite database is local to the running container and is not durable across redeployments or instance replacement. This is suitable only for a disposable demo; use an external PostgreSQL database if demo tickets and chat history must persist.

## Deploy the frontend to Netlify

The root `netlify.toml` configures Netlify with `frontend` as the base directory, `npm run build` as the build command, and `dist` as the publish directory. It also configures a single-page-app fallback and Node.js 22.12.0. For the backend deployment steps, see **Deploy the backend to Koyeb** above.

Without `VITE_API_BASE_URL`, the frontend defaults to `http://localhost:8000/api`, which only works for local development.

## GitHub safety

`.gitignore` excludes local `.env` files, SQLite databases, Python virtual environments, Node dependencies, and frontend build output. Before pushing, check `git status` and confirm no `.env` file or API key is staged. If a key has ever been committed or exposed, revoke it and generate a replacement before deploying.
