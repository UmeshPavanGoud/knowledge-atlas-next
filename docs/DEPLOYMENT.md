# Deployment notes

## Local development

Run API on port 8000 and Vite on port 5173. The Vite development server proxies `/api` to `http://localhost:8000`.

## Docker Compose

`docker compose up --build` starts the API and frontend. SQLite is stored in a named Docker volume. This Compose file is a development/preview deployment, not a hardened public production deployment.

## Public deployment checklist

Before exposing this service publicly:

- Serve the frontend and API behind HTTPS.
- Configure exact CORS origins and an API reverse proxy.
- Use managed persistent storage and tested backup/restore.
- Add request limits, structured logs, health monitoring and dependency scanning.
- Add CI tests, type checking and a production static build.
- Decide a repository license and add proper attributions.
- Define a privacy policy before adding analytics, accounts or server-side progress.
- Review URLs and content terms before presenting the catalog as curated/verified.

## Secrets

The v1 project has no required API keys. Do not commit credentials, analytics keys or future AI-provider secrets.
