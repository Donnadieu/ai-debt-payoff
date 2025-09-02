"""Background worker for LLM nudge generation."""
import json
from typing import Dict, Any, Optional
from datetime import datetime
from rq import get_current_job

from ..core.redis_config import redis_config
from ..services.llm_client import LLMClient
from ..services.validation import NudgeValidator
from ..templates.fallback_nudges import FallbackNudges


class NudgeWorker:
    """Background worker for processing nudge generation jobs."""
    
    def __init__(self):
        self.llm_client = LLMClient()
        self.validator = NudgeValidator()
        self.fallbacks = FallbackNudges()
    
    def generate_nudge(self, user_id: str, debt_plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate motivational nudge for user's debt payoff plan.
        
        Args:
            user_id: User identifier
            debt_plan: Complete debt payoff plan data
            
        Returns:
            Dict with nudge content, validation status, and metadata
        """
        job = get_current_job()
        job_id = job.id if job else "local"
        
        try:
            # Generate LLM prompt with debt plan data
            prompt = self._create_prompt(debt_plan)
            
            # Get LLM response (mock or real)
            llm_response = self.llm_client.generate_nudge(prompt)
            
            # Validate response for hallucinated numbers
            validation_result = self.validator.validate_nudge(
                llm_response, debt_plan
            )
            
            if validation_result['is_valid']:
                # Use validated LLM content
                nudge_content = validation_result['content']
                source = 'llm'
            else:
                # Use deterministic fallback
                nudge_content = self.fallbacks.get_fallback_nudge(debt_plan)
                source = 'fallback'
                print(f"⚠️ LLM validation failed: {validation_result['errors']}")
            
            # Create result with metadata
            result = {
                'user_id': user_id,
                'content': nudge_content,
                'source': source,
                'job_id': job_id,
                'created_at': datetime.utcnow().isoformat(),
                'validation_status': validation_result,
                'debt_plan_summary': {
                    'total_debt': debt_plan.get('total_debt', 0),
                    'strategy': debt_plan.get('strategy', 'unknown'),
                    'months_to_payoff': debt_plan.get('total_months', 0)
                }
            }
            
            return result
            
        except Exception as e:
            # Always provide fallback on any error
            fallback_content = self.fallbacks.get_error_fallback()
            
            return {
                'user_id': user_id,
                'content': fallback_content,
                'source': 'error_fallback',
                'job_id': job_id,
                'created_at': datetime.utcnow().isoformat(),
                'error': str(e),
                'validation_status': {'is_valid': False, 'errors': [str(e)]}
            }
    
    def _create_prompt(self, debt_plan: Dict[str, Any]) -> str:
        """Create safe LLM prompt with debt plan data."""
        # Extract safe numeric values for prompt
        total_debt = debt_plan.get('total_debt', 0)
        monthly_payment = debt_plan.get('monthly_payment', 0)
        months_to_payoff = debt_plan.get('total_months', 0)
        strategy = debt_plan.get('strategy', 'debt payoff')
        
        prompt = f"""Generate a motivational nudge for someone paying off debt.

Context:
- Total debt: ${total_debt:,.2f}
- Monthly payment: ${monthly_payment:,.2f}
- Time to payoff: {months_to_payoff} months
- Strategy: {strategy}

Requirements:
- Be encouraging and supportive
- Focus on progress and motivation
- Keep under 200 words
- Do NOT mention specific dollar amounts or numbers
- Use general terms like "your debt" or "monthly payment"

Generate a motivational message:"""
        
        return prompt


def enqueue_nudge_generation(user_id: str, debt_plan: Dict[str, Any]) -> str:
    """
    Enqueue nudge generation job.
    
    Args:
        user_id: User identifier
        debt_plan: Complete debt payoff plan
        
    Returns:
        Job ID for tracking
    """
    queue = redis_config.get_queue('nudges')
    worker = NudgeWorker()
    
    job = queue.enqueue(
        worker.generate_nudge,
        user_id,
        debt_plan,
        timeout='30s',
        job_timeout='30s'
    )
    
    return job.id
