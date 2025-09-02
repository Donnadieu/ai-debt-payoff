"""Main FastAPI application for AI Debt Payoff Planner."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

import schemas
from schemas import PayoffPlanRequest
from database import create_db_and_tables
from planner import PayoffCalculator, validate_debt_portfolio, handle_edge_cases
from models import Debt
from config import settings


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


@app.post("/plan")
async def calculate_payoff_plan(request: PayoffPlanRequest):
    """Calculate debt payoff plan using specified strategy."""
    try:
        # Validate and clean debt data
        debt_dicts = [debt.dict() for debt in request.debts]
        validation_errors = validate_debt_portfolio(debt_dicts)
        
        if validation_errors:
            raise HTTPException(status_code=400, detail={"errors": validation_errors})
        
        # Handle edge cases
        cleaned_debts = handle_edge_cases(debt_dicts)
        
        # Convert to Debt objects for calculation
        debt_objects = []
        for debt_data in cleaned_debts:
            debt_objects.append(Debt(**debt_data))
        
        # Initialize calculator with extra payment
        calculator = PayoffCalculator(extra_payment=request.extra_payment)
        
        # Calculate based on strategy
        if request.strategy == "snowball":
            result = calculator.calculate_snowball(debt_objects)
        elif request.strategy == "avalanche":
            result = calculator.calculate_avalanche(debt_objects)
        elif request.strategy == "compare":
            result = calculator.compare_strategies(debt_objects)
        else:
            raise HTTPException(status_code=400, detail="Invalid strategy. Use 'snowball', 'avalanche', or 'compare'")
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")


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
