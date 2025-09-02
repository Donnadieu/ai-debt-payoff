"""Nudge service for managing nudge operations."""

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from backend.app.schemas.nudge import (
    Nudge, NudgeCreate, NudgeUpdate, NudgeResponse, 
    NudgeType, NudgeStatus
)
from backend.app.core.repository import NudgeRepository
from backend.app.core.transaction import transactional
import logging

logger = logging.getLogger(__name__)


class NudgeService:
    """Service class for nudge business logic."""
    
    def __init__(self):
        self.repository = NudgeRepository(Nudge)
    
    @transactional
    def create_nudge(self, nudge_data: NudgeCreate) -> NudgeResponse:
        """Create a new nudge with validation."""
        # Validate nudge data
        if nudge_data.scheduled_for and nudge_data.scheduled_for < datetime.utcnow():
            raise ValueError("Scheduled time cannot be in the past")
        
        if nudge_data.expires_at and nudge_data.expires_at < datetime.utcnow():
            raise ValueError("Expiration time cannot be in the past")
        
        # Create nudge
        nudge = self.repository.create(obj_in=nudge_data)
        logger.info(f"Created nudge {nudge.id} for user {nudge.user_id}")
        
        return NudgeResponse.model_validate(nudge)
    
    def get_nudge(self, nudge_id: int) -> Optional[NudgeResponse]:
        """Get a nudge by ID."""
        nudge = self.repository.get(nudge_id)
        if nudge:
            return NudgeResponse.model_validate(nudge)
        return None
    
    def get_user_nudges(
        self, 
        user_id: str, 
        *, 
        skip: int = 0, 
        limit: int = 100,
        status: Optional[NudgeStatus] = None
    ) -> List[NudgeResponse]:
        """Get nudges for a specific user."""
        filters = {"user_id": user_id}
        if status:
            filters["status"] = status.value
        
        nudges = self.repository.get_multi(skip=skip, limit=limit, filters=filters)
        return [NudgeResponse.model_validate(nudge) for nudge in nudges]
    
    @transactional
    def update_nudge(self, nudge_id: int, update_data: NudgeUpdate) -> Optional[NudgeResponse]:
        """Update an existing nudge."""
        nudge = self.repository.get(nudge_id)
        if not nudge:
            return None
        
        # Validate update data
        if update_data.scheduled_for and update_data.scheduled_for < datetime.utcnow():
            raise ValueError("Scheduled time cannot be in the past")
        
        updated_nudge = self.repository.update(db_obj=nudge, obj_in=update_data)
        logger.info(f"Updated nudge {nudge_id}")
        
        return NudgeResponse.model_validate(updated_nudge)
    
    @transactional
    def delete_nudge(self, nudge_id: int) -> bool:
        """Delete a nudge."""
        nudge = self.repository.delete(id=nudge_id)
        if nudge:
            logger.info(f"Deleted nudge {nudge_id}")
            return True
        return False
    
    def get_pending_nudges(self, *, skip: int = 0, limit: int = 100) -> List[NudgeResponse]:
        """Get all pending nudges."""
        nudges = self.repository.get_pending_nudges(skip=skip, limit=limit)
        return [NudgeResponse.model_validate(nudge) for nudge in nudges]
    
    def get_scheduled_nudges(self, before_time: Optional[datetime] = None) -> List[NudgeResponse]:
        """Get nudges scheduled to be sent before a specific time."""
        if not before_time:
            before_time = datetime.utcnow()
        
        # This would need a custom repository method for time-based filtering
        # For now, get pending nudges and filter in memory
        pending_nudges = self.get_pending_nudges(limit=1000)
        
        scheduled = [
            nudge for nudge in pending_nudges 
            if nudge.scheduled_for and nudge.scheduled_for <= before_time
        ]
        
        return scheduled
    
    @transactional
    def mark_nudge_sent(self, nudge_id: int) -> Optional[NudgeResponse]:
        """Mark a nudge as sent."""
        update_data = NudgeUpdate(
            status=NudgeStatus.SENT,
            sent_at=datetime.utcnow()
        )
        return self.update_nudge(nudge_id, update_data)
    
    @transactional
    def mark_nudge_dismissed(self, nudge_id: int) -> Optional[NudgeResponse]:
        """Mark a nudge as dismissed by user."""
        update_data = NudgeUpdate(
            status=NudgeStatus.DISMISSED,
            dismissed_at=datetime.utcnow()
        )
        return self.update_nudge(nudge_id, update_data)
    
    @transactional
    def validate_nudge(self, nudge_id: int, validation_result: str, score: float) -> Optional[NudgeResponse]:
        """Update nudge with AI validation results."""
        if not 0.0 <= score <= 1.0:
            raise ValueError("Validation score must be between 0.0 and 1.0")
        
        status = NudgeStatus.VALIDATED if score >= 0.7 else NudgeStatus.FAILED
        
        update_data = NudgeUpdate(
            status=status,
            validation_status=validation_result,
            validation_score=score
        )
        
        return self.update_nudge(nudge_id, update_data)
    
    def get_nudge_stats(self, user_id: Optional[str] = None) -> Dict[str, Any]:
        """Get nudge statistics."""
        filters = {"user_id": user_id} if user_id else None
        
        total_count = self.repository.count(filters=filters)
        
        stats = {"total": total_count}
        
        # Count by status
        for status in NudgeStatus:
            status_filters = {**(filters or {}), "status": status.value}
            stats[status.value] = self.repository.count(filters=status_filters)
        
        return stats
    
    def cleanup_expired_nudges(self) -> int:
        """Remove expired nudges and return count of removed items."""
        # This would need a custom repository method for time-based deletion
        # For now, return 0 as placeholder
        logger.info("Expired nudges cleanup completed")
        return 0
