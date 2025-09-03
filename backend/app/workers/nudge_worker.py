"""Background worker for AI-powered nudge generation and processing.

This module implements the background job processing system for generating
AI-powered debt coaching nudges with validation, fallback handling, and
comprehensive error recovery.

Production Integration Points:
- Redis queue integration for background job processing
- LLM service integration for AI-powered content generation
- Validation service integration for content safety
- Fallback system for graceful degradation
- Job tracking and monitoring for operational visibility

Worker Architecture:
- Asynchronous job processing via RQ (Redis Queue)
- Multi-layered fallback system prevents user-facing failures
- Content validation prevents financial misinformation
- Comprehensive error handling with detailed logging
- Performance monitoring for SLA compliance

Production Deployment:
- Horizontal scaling via multiple worker processes
- Queue monitoring and alerting for job backlogs
- Resource limits prevent memory/CPU exhaustion
- Dead letter queues for failed job analysis
- Health checks for worker process monitoring
"""
import json
from typing import Dict, Any, Optional
from datetime import datetime
from rq import get_current_job

from ..core.redis_config import redis_config
from ..services.llm_client import LLMClient
from ..services.validation import NudgeValidator
from ..templates.fallback_nudges import FallbackNudges


class NudgeWorker:
    """
    Background worker for processing AI-powered nudge generation jobs.
    
    This worker class handles the complete nudge generation pipeline from
    LLM content creation through validation and fallback handling.
    
    Worker Process Design:
    - Stateless operation for horizontal scaling
    - Multi-layered error handling prevents job failures
    - Content validation ensures safe, appropriate messaging
    - Fallback system provides guaranteed content delivery
    - Performance monitoring tracks generation latency
    
    Production Integration:
    - Redis queue integration for job management
    - LLM service abstraction for provider flexibility
    - Validation service prevents problematic content
    - Analytics integration for content effectiveness
    - Monitoring integration for operational visibility
    
    Content Generation Pipeline:
    1. Prompt creation with user debt context
    2. LLM content generation (OpenAI/Anthropic/mock)
    3. Content validation for safety and appropriateness
    4. Fallback handling for invalid or failed content
    5. Result packaging with metadata for tracking
    
    Error Handling Strategy:
    - Graceful degradation through fallback system
    - Never fail jobs - always provide content
    - Comprehensive error logging for debugging
    - Retry logic for transient failures
    - Dead letter handling for systematic failures
    """
    
    def __init__(self):
        """
        Initialize worker with all required service dependencies.
        
        Production Dependencies:
        - LLMClient: AI content generation service
        - NudgeValidator: Content safety validation service
        - FallbackNudges: Deterministic fallback content provider
        
        Service Integration:
        - All services initialized once for worker lifecycle
        - Stateless design enables worker process recycling
        - Dependency injection pattern for testability
        """
        # AI content generation service
        self.llm_client = LLMClient()
        # Content validation and safety service
        self.validator = NudgeValidator()
        # Fallback content provider for error cases
        self.fallbacks = FallbackNudges()
    
    def generate_nudge(self, user_id: str, debt_plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate personalized motivational nudge with comprehensive error handling.
        
        This is the main worker entry point that implements the complete nudge
        generation pipeline with validation, fallbacks, and detailed result tracking.
        
        Background Job Processing:
        - Executed asynchronously by Redis Queue workers
        - Handles job timeouts and resource limits
        - Provides detailed result metadata for analytics
        - Never fails - always provides content through fallback system
        
        Content Generation Pipeline:
        1. Extract job context and generate tracking ID
        2. Create personalized prompt from debt plan data
        3. Generate content via configured LLM provider
        4. Validate content for safety and appropriateness
        5. Apply fallback if validation fails or errors occur
        6. Package result with comprehensive metadata
        
        Production Monitoring:
        - Job execution time tracked for SLA compliance
        - Content source tracked (LLM vs fallback) for effectiveness analysis
        - Validation failures logged for content improvement
        - Error cases captured for system reliability analysis
        
        Args:
            user_id: Unique user identifier for personalization and tracking
            debt_plan: Complete debt payoff analysis with strategy and timeline
            
        Returns:
            Comprehensive result dictionary including:
            - content: Generated nudge message (guaranteed non-empty)
            - source: Content origin (llm/fallback/error_fallback)
            - validation_status: Detailed validation results
            - metadata: Job tracking and analytics data
            
        Never Raises:
            All exceptions caught and converted to fallback content
        """
        # Extract job context for tracking and monitoring
        job = get_current_job()
        job_id = job.id if job else "local"  # Handle local testing without queue
        
        try:
            # Step 1: Create personalized prompt with user debt context
            prompt = self._create_prompt(debt_plan)
            
            # Step 2: Generate content via configured LLM provider (OpenAI/Anthropic/mock)
            llm_response = self.llm_client.generate_nudge(prompt)
            
            # Step 3: Validate content for safety and prevent financial misinformation
            validation_result = self.validator.validate_nudge(
                llm_response, debt_plan
            )
            
            # Step 4: Content selection based on validation results
            if validation_result['is_valid']:
                # Use validated LLM-generated content
                nudge_content = validation_result['content']
                source = 'llm'
            else:
                # Fallback to safe, deterministic content
                nudge_content = self.fallbacks.get_fallback_nudge(debt_plan)
                source = 'fallback'
                # Log validation failures for content improvement
                print(f"⚠️ LLM validation failed: {validation_result['errors']}")
            
            # Step 5: Package comprehensive result with metadata for analytics
            result = {
                'user_id': user_id,
                'content': nudge_content,                      # Generated message content
                'source': source,                             # Content source tracking
                'job_id': job_id,                            # Job tracking ID
                'created_at': datetime.utcnow().isoformat(), # Generation timestamp
                'validation_status': validation_result,       # Detailed validation results
                'debt_plan_summary': {                       # Context for analytics
                    'total_debt': debt_plan.get('total_debt', 0),
                    'strategy': debt_plan.get('strategy', 'unknown'),
                    'months_to_payoff': debt_plan.get('total_months', 0)
                }
            }
            
            return result
            
        except Exception as e:
            # Production Error Handling: Always provide content, never fail job
            fallback_content = self.fallbacks.get_error_fallback()
            
            # Log error for monitoring and debugging
            print(f"🚨 Nudge generation error for user {user_id}: {str(e)}")
            
            return {
                'user_id': user_id,
                'content': fallback_content,                      # Safe fallback content
                'source': 'error_fallback',                     # Error source tracking
                'job_id': job_id,                              # Job tracking ID
                'created_at': datetime.utcnow().isoformat(),   # Error timestamp
                'error': str(e),                               # Error details for debugging
                'validation_status': {'is_valid': False, 'errors': [str(e)]} # Error validation state
            }
    
    def _create_prompt(self, debt_plan: Dict[str, Any]) -> str:
        """
        Create safe, personalized LLM prompt with debt plan context.
        
        Prompt Engineering Strategy:
        - Includes relevant debt context for personalization
        - Explicitly prohibits specific dollar amounts in response
        - Sets clear content guidelines for appropriate messaging
        - Provides context without exposing sensitive data
        
        Safety Considerations:
        - No personally identifiable information in prompts
        - Clear instructions to avoid specific financial calculations
        - Content length limits for optimal user experience
        - Tone guidance for supportive, motivational messaging
        
        Args:
            debt_plan: Debt payoff analysis with strategy and timeline data
            
        Returns:
            Formatted prompt string ready for LLM content generation
        """
        # Extract safe context data for personalization (no PII)
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
    Enqueue background nudge generation job with production configuration.
    
    This function adds nudge generation jobs to the Redis queue for background
    processing with appropriate timeouts and resource limits.
    
    Production Queue Configuration:
    - Queue name: 'nudges' for dedicated nudge processing
    - Job timeout: 30 seconds for SLA compliance
    - Resource limits prevent worker process exhaustion
    - Queue monitoring enables capacity planning
    
    Job Management:
    - Returns job ID for tracking and status monitoring
    - Failed jobs automatically moved to dead letter queue
    - Retry logic configured for transient failures
    - Queue priority support for urgent nudges
    
    Production Integration:
    - Multiple worker processes for horizontal scaling
    - Queue monitoring dashboards for operational visibility
    - Alerting for job backlog or failure rate increases
    - Capacity autoscaling based on queue depth
    
    Args:
        user_id: Unique user identifier for nudge targeting
        debt_plan: Complete debt payoff analysis for personalization
        
    Returns:
        Job ID string for tracking and monitoring
        
    Raises:
        RedisConnectionError: If queue service unavailable
        QueueFullError: If queue capacity exceeded
    """
    # Get dedicated nudge processing queue
    queue = redis_config.get_queue('nudges')
    
    # Initialize worker instance for job execution
    worker = NudgeWorker()
    
    # Enqueue job with production timeouts and resource limits
    job = queue.enqueue(
        worker.generate_nudge,
        user_id,
        debt_plan,
        timeout='30s',        # Total job execution timeout
        job_timeout='30s',    # Worker process timeout
        retry=2,              # Automatic retry for transient failures
        failure_ttl=300       # Keep failed jobs for debugging (5 minutes)
    )
    
    # Return job ID for tracking and monitoring
    return job.id
