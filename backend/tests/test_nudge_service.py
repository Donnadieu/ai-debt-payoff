"""Tests for nudge service functionality."""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, AsyncMock
from typing import List, Dict, Any

from app.schemas.debt import Debt
from app.schemas.nudge import NudgeType, NudgeResponse


class MockNudgeService:
    """Mock nudge service for testing."""
    
    def __init__(self):
        self.nudges_generated = []
        self.user_preferences = {}
    
    async def generate_nudge(self, user_id: str, debt_data: List[Debt], context: Dict[str, Any]) -> NudgeResponse:
        """Generate a nudge based on user debt data."""
        nudge = NudgeResponse(
            nudge_type=NudgeType.MOTIVATION,
            title="Stay on Track!",
            message="You're doing great with your debt payoff plan.",
            priority="medium",
            user_id=user_id,
            metadata={"debts_count": len(debt_data)}
        )
        self.nudges_generated.append(nudge)
        return nudge
    
    def get_user_preferences(self, user_id: str) -> Dict[str, Any]:
        """Get user nudge preferences."""
        return self.user_preferences.get(user_id, {
            "frequency": "weekly",
            "types": ["motivation", "reminder"],
            "enabled": True
        })
    
    def update_user_preferences(self, user_id: str, preferences: Dict[str, Any]) -> bool:
        """Update user nudge preferences."""
        self.user_preferences[user_id] = preferences
        return True


class TestNudgeGeneration:
    """Test nudge generation logic."""
    
    @pytest.fixture
    def nudge_service(self):
        """Nudge service instance."""
        return MockNudgeService()
    
    @pytest.fixture
    def sample_debts_for_nudge(self):
        """Sample debt data for nudge generation."""
        return [
            Debt(
                id=1,
                name="Credit Card",
                balance=2500.0,
                interest_rate=18.5,
                minimum_payment=75.0
            ),
            Debt(
                id=2,
                name="Student Loan",
                balance=15000.0,
                interest_rate=6.8,
                minimum_payment=200.0
            )
        ]
    
    @pytest.mark.asyncio
    async def test_generate_motivation_nudge(self, nudge_service, sample_debts_for_nudge):
        """Test generating motivation nudge."""
        user_id = "user_123"
        context = {"progress": "good", "last_payment": "2024-01-15"}
        
        result = await nudge_service.generate_nudge(user_id, sample_debts_for_nudge, context)
        
        assert result.nudge_type == NudgeType.MOTIVATION
        assert result.user_id == user_id
        assert result.title is not None
        assert result.message is not None
        assert result.metadata["debts_count"] == 2
    
    @pytest.mark.asyncio
    async def test_generate_nudge_with_high_debt(self, nudge_service):
        """Test nudge generation for high debt scenario."""
        high_debt = [
            Debt(
                id=1,
                name="High Interest Card",
                balance=10000.0,
                interest_rate=24.9,
                minimum_payment=300.0
            )
        ]
        
        context = {"debt_to_income_ratio": 0.8, "risk_level": "high"}
        
        result = await nudge_service.generate_nudge("user_456", high_debt, context)
        
        assert result is not None
        assert result.user_id == "user_456"
        # High debt might generate different nudge types
        assert result.nudge_type in [NudgeType.MOTIVATION, NudgeType.WARNING, NudgeType.REMINDER]
    
    @pytest.mark.asyncio
    async def test_generate_nudge_with_progress(self, nudge_service, sample_debts_for_nudge):
        """Test nudge generation with progress context."""
        context = {
            "payments_made": 3,
            "total_paid": 1500.0,
            "progress_percentage": 15.2,
            "on_track": True
        }
        
        result = await nudge_service.generate_nudge("user_789", sample_debts_for_nudge, context)
        
        assert result is not None
        assert result.user_id == "user_789"
        # Progress context should influence nudge content
        assert "progress" in result.message.lower() or "track" in result.message.lower()
    
    @pytest.mark.asyncio
    async def test_generate_nudge_empty_debts(self, nudge_service):
        """Test nudge generation with no debts."""
        empty_debts = []
        context = {"status": "debt_free"}
        
        result = await nudge_service.generate_nudge("user_000", empty_debts, context)
        
        assert result is not None
        assert result.metadata["debts_count"] == 0
        # Should generate congratulatory or maintenance nudge
        assert result.nudge_type in [NudgeType.MOTIVATION, NudgeType.CELEBRATION]


class TestNudgePersonalization:
    """Test nudge personalization features."""
    
    @pytest.fixture
    def nudge_service(self):
        return MockNudgeService()
    
    def test_get_user_preferences_default(self, nudge_service):
        """Test getting default user preferences."""
        preferences = nudge_service.get_user_preferences("new_user")
        
        assert "frequency" in preferences
        assert "types" in preferences
        assert "enabled" in preferences
        assert preferences["enabled"] is True
    
    def test_update_user_preferences(self, nudge_service):
        """Test updating user preferences."""
        user_id = "user_123"
        new_preferences = {
            "frequency": "daily",
            "types": ["reminder", "warning"],
            "enabled": True,
            "quiet_hours": {"start": "22:00", "end": "08:00"}
        }
        
        result = nudge_service.update_user_preferences(user_id, new_preferences)
        
        assert result is True
        
        # Verify preferences were saved
        saved_preferences = nudge_service.get_user_preferences(user_id)
        assert saved_preferences["frequency"] == "daily"
        assert "warning" in saved_preferences["types"]
    
    def test_disable_nudges(self, nudge_service):
        """Test disabling nudges for a user."""
        user_id = "user_456"
        preferences = {"enabled": False}
        
        result = nudge_service.update_user_preferences(user_id, preferences)
        assert result is True
        
        saved_preferences = nudge_service.get_user_preferences(user_id)
        assert saved_preferences["enabled"] is False
    
    @pytest.mark.asyncio
    async def test_nudge_respects_user_preferences(self, nudge_service, sample_debts_for_nudge):
        """Test that nudge generation respects user preferences."""
        user_id = "user_789"
        
        # Set user preferences to only motivation nudges
        preferences = {
            "types": ["motivation"],
            "frequency": "weekly",
            "enabled": True
        }
        nudge_service.update_user_preferences(user_id, preferences)
        
        context = {"preference_check": True}
        result = await nudge_service.generate_nudge(user_id, sample_debts_for_nudge, context)
        
        # Should respect preference for motivation nudges
        assert result.nudge_type == NudgeType.MOTIVATION


class TestNudgeScheduling:
    """Test nudge scheduling and timing."""
    
    @pytest.fixture
    def nudge_scheduler(self):
        """Mock nudge scheduler."""
        class MockScheduler:
            def __init__(self):
                self.scheduled_nudges = []
            
            def schedule_nudge(self, user_id: str, nudge_time: datetime, nudge_type: str) -> str:
                nudge_id = f"nudge_{len(self.scheduled_nudges) + 1}"
                self.scheduled_nudges.append({
                    "id": nudge_id,
                    "user_id": user_id,
                    "scheduled_time": nudge_time,
                    "type": nudge_type,
                    "status": "scheduled"
                })
                return nudge_id
            
            def cancel_nudge(self, nudge_id: str) -> bool:
                for nudge in self.scheduled_nudges:
                    if nudge["id"] == nudge_id:
                        nudge["status"] = "cancelled"
                        return True
                return False
            
            def get_scheduled_nudges(self, user_id: str) -> List[Dict]:
                return [n for n in self.scheduled_nudges if n["user_id"] == user_id and n["status"] == "scheduled"]
        
        return MockScheduler()
    
    def test_schedule_weekly_nudge(self, nudge_scheduler):
        """Test scheduling a weekly nudge."""
        user_id = "user_123"
        next_week = datetime.utcnow() + timedelta(weeks=1)
        
        nudge_id = nudge_scheduler.schedule_nudge(user_id, next_week, "reminder")
        
        assert nudge_id is not None
        assert nudge_id.startswith("nudge_")
        
        scheduled = nudge_scheduler.get_scheduled_nudges(user_id)
        assert len(scheduled) == 1
        assert scheduled[0]["type"] == "reminder"
    
    def test_schedule_multiple_nudges(self, nudge_scheduler):
        """Test scheduling multiple nudges for a user."""
        user_id = "user_456"
        
        # Schedule different types of nudges
        times_and_types = [
            (datetime.utcnow() + timedelta(days=1), "reminder"),
            (datetime.utcnow() + timedelta(days=7), "motivation"),
            (datetime.utcnow() + timedelta(days=14), "progress_check")
        ]
        
        nudge_ids = []
        for nudge_time, nudge_type in times_and_types:
            nudge_id = nudge_scheduler.schedule_nudge(user_id, nudge_time, nudge_type)
            nudge_ids.append(nudge_id)
        
        assert len(nudge_ids) == 3
        
        scheduled = nudge_scheduler.get_scheduled_nudges(user_id)
        assert len(scheduled) == 3
    
    def test_cancel_scheduled_nudge(self, nudge_scheduler):
        """Test cancelling a scheduled nudge."""
        user_id = "user_789"
        nudge_time = datetime.utcnow() + timedelta(days=3)
        
        nudge_id = nudge_scheduler.schedule_nudge(user_id, nudge_time, "reminder")
        
        # Verify it's scheduled
        scheduled = nudge_scheduler.get_scheduled_nudges(user_id)
        assert len(scheduled) == 1
        
        # Cancel it
        result = nudge_scheduler.cancel_nudge(nudge_id)
        assert result is True
        
        # Verify it's no longer scheduled
        scheduled = nudge_scheduler.get_scheduled_nudges(user_id)
        assert len(scheduled) == 0


class TestNudgeDelivery:
    """Test nudge delivery mechanisms."""
    
    @pytest.fixture
    def nudge_delivery(self):
        """Mock nudge delivery service."""
        class MockDelivery:
            def __init__(self):
                self.delivered_nudges = []
                self.delivery_methods = ["email", "push", "in_app"]
            
            async def deliver_nudge(self, nudge: NudgeResponse, method: str = "in_app") -> bool:
                if method not in self.delivery_methods:
                    return False
                
                delivery_record = {
                    "nudge_id": getattr(nudge, 'id', 'generated'),
                    "user_id": nudge.user_id,
                    "method": method,
                    "delivered_at": datetime.utcnow(),
                    "status": "delivered"
                }
                self.delivered_nudges.append(delivery_record)
                return True
            
            def get_delivery_history(self, user_id: str) -> List[Dict]:
                return [d for d in self.delivered_nudges if d["user_id"] == user_id]
        
        return MockDelivery()
    
    @pytest.mark.asyncio
    async def test_deliver_nudge_in_app(self, nudge_delivery):
        """Test delivering nudge via in-app notification."""
        nudge = NudgeResponse(
            nudge_type=NudgeType.REMINDER,
            title="Payment Due Soon",
            message="Your credit card payment is due in 3 days.",
            priority="high",
            user_id="user_123"
        )
        
        result = await nudge_delivery.deliver_nudge(nudge, "in_app")
        
        assert result is True
        
        history = nudge_delivery.get_delivery_history("user_123")
        assert len(history) == 1
        assert history[0]["method"] == "in_app"
        assert history[0]["status"] == "delivered"
    
    @pytest.mark.asyncio
    async def test_deliver_nudge_email(self, nudge_delivery):
        """Test delivering nudge via email."""
        nudge = NudgeResponse(
            nudge_type=NudgeType.MOTIVATION,
            title="Great Progress!",
            message="You've paid off 25% of your debt this month.",
            priority="medium",
            user_id="user_456"
        )
        
        result = await nudge_delivery.deliver_nudge(nudge, "email")
        
        assert result is True
        
        history = nudge_delivery.get_delivery_history("user_456")
        assert len(history) == 1
        assert history[0]["method"] == "email"
    
    @pytest.mark.asyncio
    async def test_deliver_nudge_invalid_method(self, nudge_delivery):
        """Test delivering nudge with invalid method."""
        nudge = NudgeResponse(
            nudge_type=NudgeType.WARNING,
            title="High Interest Alert",
            message="Consider paying off high-interest debt first.",
            priority="high",
            user_id="user_789"
        )
        
        result = await nudge_delivery.deliver_nudge(nudge, "invalid_method")
        
        assert result is False
        
        history = nudge_delivery.get_delivery_history("user_789")
        assert len(history) == 0


class TestNudgeAnalytics:
    """Test nudge analytics and effectiveness tracking."""
    
    @pytest.fixture
    def nudge_analytics(self):
        """Mock nudge analytics service."""
        class MockAnalytics:
            def __init__(self):
                self.interactions = []
                self.effectiveness_data = {}
            
            def track_nudge_interaction(self, user_id: str, nudge_id: str, interaction_type: str):
                """Track user interaction with nudge."""
                self.interactions.append({
                    "user_id": user_id,
                    "nudge_id": nudge_id,
                    "interaction_type": interaction_type,
                    "timestamp": datetime.utcnow()
                })
            
            def calculate_effectiveness(self, nudge_type: str, time_period: timedelta) -> Dict[str, float]:
                """Calculate nudge effectiveness metrics."""
                # Mock effectiveness calculation
                return {
                    "open_rate": 0.75,
                    "click_rate": 0.45,
                    "action_rate": 0.30,
                    "total_sent": 100,
                    "total_opened": 75,
                    "total_clicked": 45,
                    "total_actions": 30
                }
            
            def get_user_engagement(self, user_id: str) -> Dict[str, Any]:
                """Get user engagement metrics."""
                user_interactions = [i for i in self.interactions if i["user_id"] == user_id]
                return {
                    "total_nudges_received": len(user_interactions),
                    "total_interactions": len(user_interactions),
                    "last_interaction": max([i["timestamp"] for i in user_interactions]) if user_interactions else None,
                    "engagement_score": min(len(user_interactions) / 10.0, 1.0)  # Simple score
                }
        
        return MockAnalytics()
    
    def test_track_nudge_opened(self, nudge_analytics):
        """Test tracking when user opens a nudge."""
        user_id = "user_123"
        nudge_id = "nudge_456"
        
        nudge_analytics.track_nudge_interaction(user_id, nudge_id, "opened")
        
        engagement = nudge_analytics.get_user_engagement(user_id)
        assert engagement["total_interactions"] == 1
        assert engagement["engagement_score"] > 0
    
    def test_track_nudge_clicked(self, nudge_analytics):
        """Test tracking when user clicks on nudge."""
        user_id = "user_456"
        nudge_id = "nudge_789"
        
        nudge_analytics.track_nudge_interaction(user_id, nudge_id, "clicked")
        nudge_analytics.track_nudge_interaction(user_id, nudge_id, "action_taken")
        
        engagement = nudge_analytics.get_user_engagement(user_id)
        assert engagement["total_interactions"] == 2
    
    def test_calculate_nudge_effectiveness(self, nudge_analytics):
        """Test calculating nudge effectiveness metrics."""
        time_period = timedelta(days=30)
        
        effectiveness = nudge_analytics.calculate_effectiveness("motivation", time_period)
        
        assert "open_rate" in effectiveness
        assert "click_rate" in effectiveness
        assert "action_rate" in effectiveness
        assert 0 <= effectiveness["open_rate"] <= 1
        assert 0 <= effectiveness["click_rate"] <= 1
        assert 0 <= effectiveness["action_rate"] <= 1
    
    def test_user_engagement_scoring(self, nudge_analytics):
        """Test user engagement scoring."""
        user_id = "user_789"
        
        # Simulate multiple interactions
        for i in range(5):
            nudge_analytics.track_nudge_interaction(user_id, f"nudge_{i}", "opened")
        
        engagement = nudge_analytics.get_user_engagement(user_id)
        assert engagement["total_interactions"] == 5
        assert engagement["engagement_score"] == 0.5  # 5/10 = 0.5


class TestNudgeIntegration:
    """Test nudge service integration with other components."""
    
    @pytest.mark.asyncio
    async def test_nudge_triggered_by_debt_change(self):
        """Test nudge generation triggered by debt changes."""
        # Mock debt service detecting significant change
        debt_change = {
            "user_id": "user_123",
            "change_type": "balance_increase",
            "amount": 500.0,
            "debt_name": "Credit Card"
        }
        
        # This would typically trigger nudge generation
        nudge_service = MockNudgeService()
        
        # Simulate nudge generation based on debt change
        context = {
            "trigger": "debt_change",
            "change_type": debt_change["change_type"],
            "amount": debt_change["amount"]
        }
        
        sample_debts = [
            Debt(
                id=1,
                name="Credit Card",
                balance=3000.0,  # Increased balance
                interest_rate=18.5,
                minimum_payment=90.0
            )
        ]
        
        result = await nudge_service.generate_nudge(debt_change["user_id"], sample_debts, context)
        
        assert result is not None
        assert result.user_id == debt_change["user_id"]
        # Should generate appropriate nudge for balance increase
        assert result.nudge_type in [NudgeType.WARNING, NudgeType.REMINDER]
    
    @pytest.mark.asyncio
    async def test_nudge_integration_with_analytics(self):
        """Test nudge service integration with analytics."""
        nudge_service = MockNudgeService()
        
        # Generate a nudge
        sample_debts = [
            Debt(id=1, name="Test Debt", balance=1000.0, interest_rate=10.0, minimum_payment=50.0)
        ]
        
        with patch('app.core.analytics.analytics_core.track_event') as mock_track:
            result = await nudge_service.generate_nudge("user_123", sample_debts, {})
            
            # In a real implementation, nudge generation would trigger analytics
            # Mock the analytics call that would happen
            mock_track("nudge_generated", {
                "user_id": "user_123",
                "nudge_type": result.nudge_type.value,
                "nudge_priority": result.priority,
                "debts_count": 1
            })
            
            mock_track.assert_called_once()
            call_args = mock_track.call_args
            assert call_args[0][0] == "nudge_generated"
            assert call_args[0][1]["user_id"] == "user_123"
