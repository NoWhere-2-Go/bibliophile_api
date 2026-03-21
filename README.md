# Bibliophile API

Minimal FastAPI service with PostgreSQL connectivity.

## 1) Install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2) Configure local database connection

Copy `.env.example` to `.env` and set values for your local PostgreSQL server.

```bash
cp .env.example .env
```

If your local server uses different credentials/database, edit `.env`.

## 3) Run the API

```bash
uvicorn main:app --reload
```

## 4) Verify endpoints

Open `test_main.http` in your IDE and run:
- `GET /`
- `GET /hello/User`
- `GET /health/db`

Expected DB success response:

```json
{"status":"ok","database":"reachable"}
```

If DB is unreachable, `/health/db` returns HTTP 503 with error detail.

