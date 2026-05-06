"""FastAPI application entry point; registers routes and exposes the health check endpoint."""

from fastapi import FastAPI
from app.routes import recommendations

app = FastAPI(title="AgriPulse AI - Crop Recommendations", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(recommendations.router, prefix="/api")
