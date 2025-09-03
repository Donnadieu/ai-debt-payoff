"""
Slip Detection API Endpoint - Budget feasibility analysis endpoint.
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
import logging
from datetime import datetime

from app.schemas.slip import SlipCheckRequest, SlipCheckResponse, SlipAnalyticsEvent
from app.services.slip_detector import SlipDetector

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize slip detector
slip_detector = SlipDetector()


@router.post("/check", response_model=SlipCheckResponse)
async def check_slip(request: SlipCheckRequest) -> SlipCheckResponse:
    """
    Analyze budget feasibility and detect potential slips.
    
    Compares monthly budget against minimum debt payments and provides
    remediation suggestions when budget is insufficient.
    """
    try:
        # Convert request data for analysis
        debts_data = []
        for debt in request.debts:
            debts_data.append({
                'id': debt.id,
                'name': debt.name,
                'minimum_payment': debt.minimum_payment,
                'balance': debt.balance
            })
        
        # Perform slip analysis
        analysis_result = slip_detector.analyze_budget_feasibility(
            monthly_budget=request.monthly_budget,
            debts=debts_data
        )
        
        # Create analytics event
        analytics_event = SlipAnalyticsEvent(
            has_slip=analysis_result['has_slip'],
            shortfall_amount=analysis_result['shortfall'],
            suggestion_amount=analysis_result['suggestion_amount'],
            debt_count=len(request.debts),
            timestamp=datetime.utcnow().isoformat() + 'Z'
        )
        
        # Log analytics event (in production, this would be sent to analytics service)
        logger.info(f"Slip detection event: {analytics_event.dict()}")
        
        # Return response
        return SlipCheckResponse(**analysis_result)
        
    except Exception as e:
        logger.error(f"Error in slip detection: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal error during slip analysis: {str(e)}"
        )


@router.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint for slip detection service."""
    return {
        "status": "healthy",
        "service": "slip_detection",
        "timestamp": datetime.utcnow().isoformat() + 'Z'
    }
