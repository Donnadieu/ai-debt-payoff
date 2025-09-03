"""Main FastAPI application for AI Debt Payoff Planner."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

import schemas
from schemas import PayoffPlanRequest
from database import create_db_and_tables
from planner import PayoffCalculator, validate_debt_portfolio, handle_edge_cases
from models import Debt
from config import settings
from app.api.endpoints import slip
from app.api import analytics
from app.middleware.performance import setup_middleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    create_db_and_tables()
    yield
    # Shutdown


# Create FastAPI app with enhanced OpenAPI metadata
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description=settings.api_description,
    lifespan=lifespan,
    openapi_tags=[
        {
            "name": "payoff-planning",
            "description": "Debt payoff plan calculation and strategy comparison"
        },
        {
            "name": "slip-detection", 
            "description": "Budget feasibility analysis and slip detection"
        },
        {
            "name": "nudges",
            "description": "AI-powered motivational nudges and coaching"
        },
        {
            "name": "analytics",
            "description": "Event tracking and performance monitoring"
        },
        {
            "name": "debt-management",
            "description": "CRUD operations for debt tracking"
        },
        {
            "name": "health",
            "description": "API health and status endpoints"
        }
    ],
    contact={
        "name": "AI Debt Payoff Planner API",
        "url": "https://github.com/your-org/ai-debt-payoff",
        "email": "support@example.com"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    }
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup analytics and performance monitoring middleware
setup_middleware(app, enable_performance=True, enable_analytics=True)


@app.get("/", tags=["health"])
async def root():
    """
    API Root endpoint.
    
    Returns basic API information including version and documentation links.
    """
    return {
        "message": "AI Debt Payoff Planner API",
        "version": settings.api_version,
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", tags=["health"])
async def health_check():
    """
    Health check endpoint.
    
    Returns the current status of the API and environment information.
    Use this endpoint to verify the API is running and responsive.
    """
    return {"status": "healthy", "environment": settings.environment}


# Debt management endpoints (placeholder)
@app.get("/api/v1/debts", tags=["debt-management"])
async def get_debts():
    """
    Get all debts.
    
    Returns a list of all debt records for the current user.
    """
    return {"debts": []}


@app.post("/api/v1/debts", tags=["debt-management"])
async def create_debt(debt_data: dict):
    """
    Create a new debt.
    
    Adds a new debt record with validation for required fields and reasonable limits.
    
    **Required Fields:**
    - name: Descriptive name for the debt
    - balance: Current outstanding balance
    - interest_rate: Annual interest rate (0-100%)
    - minimum_payment: Required minimum monthly payment
    """
    # Basic validation that debt has required fields
    required_fields = ["name", "balance", "interest_rate", "minimum_payment"]
    for field in required_fields:
        if field not in debt_data:
            raise HTTPException(status_code=422, detail=f"Missing required field: {field}")
    
    # Validate field values
    if not debt_data.get("name") or debt_data["name"].strip() == "":
        raise HTTPException(status_code=422, detail="Debt name cannot be empty")
    
    if debt_data.get("balance", 0) < 0:
        raise HTTPException(status_code=422, detail="Debt balance cannot be negative")
    
    if debt_data.get("interest_rate", 0) < 0 or debt_data.get("interest_rate", 0) > 100:
        raise HTTPException(status_code=422, detail="Interest rate must be between 0 and 100")
    
    return {
        "success": True,
        "message": "Debt created successfully",
        "debt": debt_data
    }


@app.post("/plan", tags=["payoff-planning"])
async def calculate_payoff_plan(request: PayoffPlanRequest):
    """
    Calculate debt payoff plan using specified strategy.
    
    Generates a complete debt payoff timeline using either the snowball method 
    (smallest balance first), avalanche method (highest interest rate first), 
    or comparison of both strategies.
    
    **Strategies:**
    - **Snowball**: Pay minimums on all debts, extra payment goes to smallest balance
    - **Avalanche**: Pay minimums on all debts, extra payment goes to highest interest rate
    - **Compare**: Returns both strategies with detailed comparison
    
    **Features:**
    - Monthly payment schedule
    - Total interest calculation
    - Payoff timeline projections
    - Strategy comparison and recommendations
    """
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


@app.get("/api/v1/debts/{debt_id}", tags=["debt-management"])
async def get_debt(debt_id: int):
    """
    Get a specific debt by ID.
    
    Retrieves detailed information for a single debt record.
    """
    return {"debt_id": debt_id, "message": "Debt retrieval endpoint - to be implemented"}


@app.put("/api/v1/debts/{debt_id}", tags=["debt-management"])
async def update_debt(debt_id: int):
    """
    Update a specific debt by ID.
    
    Updates an existing debt record with new balance, payment amount, or other details.
    """
    return {"debt_id": debt_id, "message": "Debt update endpoint - to be implemented"}


@app.delete("/api/v1/debts/{debt_id}", tags=["debt-management"])
async def delete_debt(debt_id: int):
    """
    Delete a specific debt by ID.
    
    Permanently removes a debt record from the system.
    """
    return {"debt_id": debt_id, "message": "Debt deletion endpoint - to be implemented"}


# Nudge/coaching endpoints
@app.get("/api/v1/nudges", tags=["nudges"])
async def get_nudges():
    """
    Get AI coaching nudges.
    
    Returns a list of nudges/coaching messages for the current user.
    """
    return {"nudges": []}


@app.post("/api/v1/nudges", tags=["nudges"])
async def create_nudge():
    """
    Create a new nudge.
    
    Manually create a nudge/coaching message. This is typically used for
    scheduled or system-generated nudges.
    """
    return {"message": "Nudge creation endpoint - to be implemented"}


class NudgeGenerateRequest(BaseModel):
    """Request model for nudge generation."""
    user_id: str = Field(..., min_length=1, max_length=50, description="User identifier")
    debt_plan: Dict[str, Any] = Field(..., description="Debt payoff plan data for context")
    
    class Config:
        schema_extra = {
            "example": {
                "user_id": "user_123",
                "debt_plan": {
                    "strategy": "snowball",
                    "total_debt": 7500.00,
                    "total_months": 24,
                    "monthly_payment": 350.00,
                    "total_interest": 671.83
                }
            }
        }


class NudgeGenerateResponse(BaseModel):
    """Response model for nudge generation."""
    success: bool
    job_id: Optional[str] = None
    nudge: Optional[Dict[str, Any]] = None
    source: Optional[str] = None
    message: str
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "job_id": "abc123",
                "nudge": {
                    "title": "Stay Motivated!",
                    "message": "You're making excellent progress with your debt payoff plan. Stay focused on your goals and remember that every payment brings you closer to financial freedom!",
                    "nudge_type": "motivation",
                    "priority": 3,
                    "user_id": "user_123"
                },
                "source": "llm",
                "message": "Nudge generated successfully"
            }
        }


@app.post("/nudge/generate", response_model=NudgeGenerateResponse, tags=["nudges"])
async def generate_nudge(request: NudgeGenerateRequest):
    """
    Generate an AI-powered motivational nudge based on user's debt payoff plan.
    
    This endpoint generates personalized motivational content to help users stay
    committed to their debt payoff goals. The nudge is created using AI analysis
    of the user's debt plan and financial progress.
    
    **Process:**
    1. Validates the debt plan data for completeness
    2. Generates AI-powered motivational content using LLM
    3. Validates generated content for accuracy and safety
    4. Falls back to template-based nudges if AI validation fails
    5. Returns formatted nudge content ready for display
    
    **Content Safety:**
    - All financial figures are validated against hallucinations
    - Generic motivational language is preferred over specific numbers
    - Fallback templates ensure consistent quality
    
    Args:
        request: Nudge generation request with user ID and debt plan
    
    Returns:
        Generated nudge content with metadata and generation details
    
    Raises:
        HTTPException: If user_id is invalid or debt_plan is malformed
    """
    try:
        # Import here to avoid circular dependencies
        from app.workers.nudge_worker import NudgeWorker
        
        # Initialize worker and generate nudge synchronously for API response
        # In production, this could be made async with job queuing
        worker = NudgeWorker()
        
        # Validate debt plan has required fields
        required_fields = ['strategy', 'total_debt', 'total_months']
        missing_fields = [field for field in required_fields if field not in request.debt_plan]
        
        if missing_fields:
            raise HTTPException(
                status_code=422, 
                detail=f"Missing required debt plan fields: {', '.join(missing_fields)}"
            )
        
        # Generate nudge content
        result = worker.generate_nudge(request.user_id, request.debt_plan)
        
        # Format response - handle string or dict content
        content = result.get('content', '')
        if isinstance(content, str):
            # Convert string content to structured nudge
            nudge = {
                "title": "Stay Motivated!",
                "message": content,
                "nudge_type": "motivation",
                "priority": 3,
                "user_id": request.user_id
            }
        else:
            # Content is already a dict
            nudge = content
        
        return NudgeGenerateResponse(
            success=True,
            job_id=result.get('job_id'),
            nudge=nudge,
            source=result.get('source', 'unknown'),
            message="Nudge generated successfully"
        )
        
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        # Always provide fallback response
        from app.templates.fallback_nudges import FallbackNudges
        fallbacks = FallbackNudges()
        fallback_content = fallbacks.get_error_fallback()
        
        # Format fallback as structured nudge
        fallback_nudge = {
            "title": "Keep Going!",
            "message": fallback_content,
            "nudge_type": "motivation",
            "priority": 3,
            "user_id": request.user_id
        }
        
        return NudgeGenerateResponse(
            success=True,  # Still successful - we have fallback content
            nudge=fallback_nudge,
            source="error_fallback",
            message=f"Generated fallback nudge due to error: {str(e)}"
        )


# Slip detection endpoints
app.include_router(slip.router, prefix="/api/v1/slip", tags=["slip-detection"])

# Analytics endpoints
app.include_router(analytics.router, tags=["analytics"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=5000,
        reload=settings.debug
    )
