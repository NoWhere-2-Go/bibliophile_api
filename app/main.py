from fastapi import FastAPI

import app.models  # noqa: F401 - imports all model classes for SQLAlchemy metadata registration
from app.api.router import api_router
from app.middleware.request_context import RequestContextMiddleware
from app.middleware.request_logging import RequestLoggingMiddleware


def create_app() -> FastAPI:
    app = FastAPI(title="Bibliophile API")
    app.include_router(api_router)
    return app


app = create_app()

app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(RequestContextMiddleware)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

