"""Main FastAPI application for AI Debt Payoff Planner."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config import settings
from database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    create_db_and_tables()
    yield
    # Shutdown


# Create FastAPI app
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description=settings.api_description,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "AI Debt Payoff Planner API",
        "version": settings.api_version,
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "environment": settings.environment}


# Debt management endpoints (placeholder)
@app.get("/api/v1/debts")
async def get_debts():
    """Get all debts."""
    return {"debts": []}


@app.post("/api/v1/debts")
async def create_debt():
    """Create a new debt."""
    return {"message": "Debt creation endpoint - to be implemented"}


@app.get("/api/v1/debts/{debt_id}")
async def get_debt(debt_id: int):
    """Get a specific debt."""
    return {"debt_id": debt_id, "message": "Debt retrieval endpoint - to be implemented"}


@app.put("/api/v1/debts/{debt_id}")
async def update_debt(debt_id: int):
    """Update a specific debt."""
    return {"debt_id": debt_id, "message": "Debt update endpoint - to be implemented"}


@app.delete("/api/v1/debts/{debt_id}")
async def delete_debt(debt_id: int):
    """Delete a specific debt."""
    return {"debt_id": debt_id, "message": "Debt deletion endpoint - to be implemented"}


# Nudge/coaching endpoints (placeholder)
@app.get("/api/v1/nudges")
async def get_nudges():
    """Get AI coaching nudges."""
    return {"nudges": []}


@app.post("/api/v1/nudges")
async def create_nudge():
    """Create a new nudge."""
    return {"message": "Nudge creation endpoint - to be implemented"}


# Analytics endpoints (placeholder)
@app.get("/api/v1/analytics/progress")
async def get_progress_analytics():
    """Get debt payoff progress analytics."""
    return {"analytics": {}, "message": "Analytics endpoint - to be implemented"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
