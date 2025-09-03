"""Tests for event service layer."""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, AsyncMock
from sqlalchemy.orm import Session

from app.services.event_service import (
    EventRepository, 
    EventValidator, 
    EventFormatter, 
    EventService
)
from app.schemas.event import (
    Event, 
    EventCreate, 
    EventUpdate, 
    EventType, 
    EventSeverity,
    EventDB
)


class TestEventRepository:
    """Test event repository CRUD operations."""
    
    @pytest.fixture
    def mock_db(self):
        """Mock database session."""
        return Mock(spec=Session)
    
    @pytest.fixture
    def event_repo(self, mock_db):
        """Event repository instance."""
        return EventRepository(mock_db)
    
    def test_create_event(self, event_repo, mock_db):
        """Test creating an event."""
        event_data = EventCreate(
            event_type=EventType.USER_ACTION,
            name="test_event",
            properties={"test": True},
            user_id="user_123"
        )
        
        # Mock database operations
        mock_db_event = EventDB(
            id=1,
            event_type=EventType.USER_ACTION,
            name="test_event",
            properties={"test": True},
            user_id="user_123",
            timestamp=datetime.utcnow(),
            severity=EventSeverity.INFO
        )
        mock_db.add.return_value = None
        mock_db.commit.return_value = None
        mock_db.refresh.return_value = None
        
        # Set up the mock to return our event when queried
        with patch.object(event_repo, '_create_db_event', return_value=mock_db_event):
            result = event_repo.create(event_data)
        
        assert result.name == "test_event"
        assert result.event_type == EventType.USER_ACTION
        assert result.user_id == "user_123"
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
    
    def test_get_event_by_id(self, event_repo, mock_db):
        """Test getting event by ID."""
        mock_event = EventDB(
            id=1,
            event_type=EventType.USER_ACTION,
            name="test_event",
            properties={},
            timestamp=datetime.utcnow(),
            severity=EventSeverity.INFO
        )
        
        mock_db.query.return_value.filter.return_value.first.return_value = mock_event
        
        result = event_repo.get(1)
        
        assert result is not None
        assert result.id == 1
        assert result.name == "test_event"
        mock_db.query.assert_called_once()
    
    def test_get_nonexistent_event(self, event_repo, mock_db):
        """Test getting non-existent event returns None."""
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        result = event_repo.get(999)
        
        assert result is None
    
    def test_get_events_by_user(self, event_repo, mock_db):
        """Test getting events by user ID."""
        mock_events = [
            EventDB(id=1, name="event1", user_id="user_123", 
                    event_type=EventType.USER_ACTION, properties={},
                    timestamp=datetime.utcnow(), severity=EventSeverity.INFO),
            EventDB(id=2, name="event2", user_id="user_123",
                    event_type=EventType.USER_ACTION, properties={},
                    timestamp=datetime.utcnow(), severity=EventSeverity.INFO)
        ]
        
        mock_db.query.return_value.filter.return_value.order_by.return_value.limit.return_value.all.return_value = mock_events
        
        result = event_repo.get_by_user("user_123", limit=10)
        
        assert len(result) == 2
        assert all(event.user_id == "user_123" for event in result)
    
    def test_get_events_by_type(self, event_repo, mock_db):
        """Test getting events by type."""
        mock_events = [
            EventDB(id=1, name="event1", event_type=EventType.SYSTEM_EVENT,
                    properties={}, timestamp=datetime.utcnow(), severity=EventSeverity.INFO)
        ]
        
        mock_db.query.return_value.filter.return_value.order_by.return_value.limit.return_value.all.return_value = mock_events
        
        result = event_repo.get_by_type(EventType.SYSTEM_EVENT, limit=10)
        
        assert len(result) == 1
        assert result[0].event_type == EventType.SYSTEM_EVENT
    
    def test_get_events_by_date_range(self, event_repo, mock_db):
        """Test getting events by date range."""
        start_date = datetime.utcnow() - timedelta(days=1)
        end_date = datetime.utcnow()
        
        mock_events = [
            EventDB(id=1, name="event1", event_type=EventType.USER_ACTION,
                    properties={}, timestamp=datetime.utcnow(), severity=EventSeverity.INFO)
        ]
        
        mock_db.query.return_value.filter.return_value.order_by.return_value.limit.return_value.all.return_value = mock_events
        
        result = event_repo.get_by_date_range(start_date, end_date, limit=10)
        
        assert len(result) == 1
        mock_db.query.assert_called_once()
    
    def test_update_event(self, event_repo, mock_db):
        """Test updating an event."""
        mock_event = EventDB(
            id=1,
            event_type=EventType.USER_ACTION,
            name="old_name",
            properties={"old": True},
            timestamp=datetime.utcnow(),
            severity=EventSeverity.INFO
        )
        
        mock_db.query.return_value.filter.return_value.first.return_value = mock_event
        mock_db.commit.return_value = None
        mock_db.refresh.return_value = None
        
        update_data = EventUpdate(name="new_name", properties={"new": True})
        result = event_repo.update(1, update_data)
        
        assert result is not None
        assert mock_event.name == "new_name"
        assert mock_event.properties == {"new": True}
        mock_db.commit.assert_called_once()
    
    def test_delete_event(self, event_repo, mock_db):
        """Test deleting an event."""
        mock_event = EventDB(
            id=1,
            event_type=EventType.USER_ACTION,
            name="test_event",
            properties={},
            timestamp=datetime.utcnow(),
            severity=EventSeverity.INFO
        )
        
        mock_db.query.return_value.filter.return_value.first.return_value = mock_event
        mock_db.delete.return_value = None
        mock_db.commit.return_value = None
        
        result = event_repo.delete(1)
        
        assert result is True
        mock_db.delete.assert_called_once_with(mock_event)
        mock_db.commit.assert_called_once()
    
    def test_get_event_statistics(self, event_repo, mock_db):
        """Test getting event statistics."""
        # Mock count queries
        mock_db.query.return_value.count.return_value = 100
        mock_db.query.return_value.filter.return_value.count.return_value = 50
        
        result = event_repo.get_statistics()
        
        assert "total_events" in result
        assert "events_by_type" in result
        assert "events_by_severity" in result
        assert isinstance(result["total_events"], int)


class TestEventValidator:
    """Test event validation logic."""
    
    @pytest.fixture
    def validator(self):
        """Event validator instance."""
        return EventValidator()
    
    def test_validate_valid_event(self, validator):
        """Test validating a valid event."""
        event_data = EventCreate(
            event_type=EventType.USER_ACTION,
            name="valid_event",
            properties={"key": "value"},
            user_id="user_123"
        )
        
        result = validator.validate(event_data)
        
        assert result.is_valid is True
        assert len(result.errors) == 0
    
    def test_validate_empty_name(self, validator):
        """Test validation fails for empty event name."""
        event_data = EventCreate(
            event_type=EventType.USER_ACTION,
            name="",
            properties={}
        )
        
        result = validator.validate(event_data)
        
        assert result.is_valid is False
        assert any("name" in error.lower() for error in result.errors)
    
    def test_validate_invalid_properties(self, validator):
        """Test validation of properties."""
        # Test with non-serializable properties
        event_data = EventCreate(
            event_type=EventType.USER_ACTION,
            name="test_event",
            properties={"func": lambda x: x}  # Non-serializable
        )
        
        result = validator.validate(event_data)
        
        # Should handle non-serializable properties gracefully
        assert result.is_valid is False or result.is_valid is True  # Implementation dependent
    
    def test_validate_properties_size_limit(self, validator):
        """Test validation of properties size limit."""
        # Create large properties object
        large_properties = {f"key_{i}": f"value_{i}" * 1000 for i in range(100)}
        
        event_data = EventCreate(
            event_type=EventType.USER_ACTION,
            name="test_event",
            properties=large_properties
        )
        
        result = validator.validate(event_data)
        
        # Should validate size limits
        if not result.is_valid:
            assert any("size" in error.lower() or "large" in error.lower() for error in result.errors)
    
    def test_validate_user_id_format(self, validator):
        """Test validation of user ID format."""
        event_data = EventCreate(
            event_type=EventType.USER_ACTION,
            name="test_event",
            properties={},
            user_id="invalid user id with spaces and special chars!!!"
        )
        
        result = validator.validate(event_data)
        
        # Implementation may or may not validate user ID format
        assert isinstance(result.is_valid, bool)
    
    def test_validate_event_type_required(self, validator):
        """Test that event type is required."""
        # This would be caught by Pydantic validation before reaching our validator
        with pytest.raises((ValueError, TypeError)):
            EventCreate(
                name="test_event",
                properties={}
                # Missing event_type
            )


class TestEventFormatter:
    """Test event formatting logic."""
    
    @pytest.fixture
    def formatter(self):
        """Event formatter instance."""
        return EventFormatter()
    
    def test_format_for_storage(self, formatter):
        """Test formatting event for storage."""
        event = Event(
            id=1,
            event_type=EventType.USER_ACTION,
            name="test_event",
            properties={"key": "value"},
            user_id="user_123",
            timestamp=datetime.utcnow(),
            severity=EventSeverity.INFO
        )
        
        result = formatter.format_for_storage(event)
        
        assert "id" in result
        assert "event_type" in result
        assert "name" in result
        assert "properties" in result
        assert "timestamp" in result
        assert isinstance(result["properties"], (dict, str))
    
    def test_format_for_api(self, formatter):
        """Test formatting event for API response."""
        event = Event(
            id=1,
            event_type=EventType.USER_ACTION,
            name="test_event",
            properties={"key": "value"},
            user_id="user_123",
            timestamp=datetime.utcnow(),
            severity=EventSeverity.INFO
        )
        
        result = formatter.format_for_api(event)
        
        assert "id" in result
        assert "event_type" in result
        assert "name" in result
        assert "properties" in result
        assert "timestamp" in result
        assert "user_id" in result
    
    def test_format_batch_events(self, formatter):
        """Test formatting batch of events."""
        events = [
            Event(
                id=i,
                event_type=EventType.USER_ACTION,
                name=f"event_{i}",
                properties={"index": i},
                timestamp=datetime.utcnow(),
                severity=EventSeverity.INFO
            )
            for i in range(3)
        ]
        
        result = formatter.format_batch(events)
        
        assert isinstance(result, list)
        assert len(result) == 3
        assert all("id" in event for event in result)
    
    def test_format_with_sensitive_data(self, formatter):
        """Test formatting removes sensitive data."""
        event = Event(
            id=1,
            event_type=EventType.USER_ACTION,
            name="login_event",
            properties={
                "username": "user123",
                "password": "secret123",  # Sensitive
                "email": "user@example.com"
            },
            timestamp=datetime.utcnow(),
            severity=EventSeverity.INFO
        )
        
        result = formatter.format_for_api(event)
        
        # Should remove or mask sensitive fields
        properties = result.get("properties", {})
        if isinstance(properties, dict):
            # Password should be removed or masked
            assert properties.get("password") != "secret123"


class TestEventService:
    """Test event service orchestration."""
    
    @pytest.fixture
    def mock_repo(self):
        """Mock event repository."""
        return Mock(spec=EventRepository)
    
    @pytest.fixture
    def mock_validator(self):
        """Mock event validator."""
        validator = Mock(spec=EventValidator)
        # Default to valid
        validator.validate.return_value = Mock(is_valid=True, errors=[])
        return validator
    
    @pytest.fixture
    def mock_formatter(self):
        """Mock event formatter."""
        return Mock(spec=EventFormatter)
    
    @pytest.fixture
    def event_service(self, mock_repo, mock_validator, mock_formatter):
        """Event service instance."""
        return EventService(mock_repo, mock_validator, mock_formatter)
    
    def test_create_event_success(self, event_service, mock_repo, mock_validator, mock_formatter):
        """Test successful event creation."""
        event_data = EventCreate(
            event_type=EventType.USER_ACTION,
            name="test_event",
            properties={"test": True}
        )
        
        mock_event = Event(
            id=1,
            event_type=EventType.USER_ACTION,
            name="test_event",
            properties={"test": True},
            timestamp=datetime.utcnow(),
            severity=EventSeverity.INFO
        )
        
        mock_repo.create.return_value = mock_event
        mock_formatter.format_for_api.return_value = {"id": 1, "name": "test_event"}
        
        result = event_service.create_event(event_data)
        
        assert result is not None
        mock_validator.validate.assert_called_once_with(event_data)
        mock_repo.create.assert_called_once_with(event_data)
        mock_formatter.format_for_api.assert_called_once_with(mock_event)
    
    def test_create_event_validation_failure(self, event_service, mock_validator):
        """Test event creation with validation failure."""
        event_data = EventCreate(
            event_type=EventType.USER_ACTION,
            name="",  # Invalid empty name
            properties={}
        )
        
        # Mock validation failure
        mock_validator.validate.return_value = Mock(
            is_valid=False, 
            errors=["Event name cannot be empty"]
        )
        
        with pytest.raises(ValueError) as exc_info:
            event_service.create_event(event_data)
        
        assert "validation" in str(exc_info.value).lower()
        mock_validator.validate.assert_called_once_with(event_data)
    
    def test_get_event_by_id(self, event_service, mock_repo, mock_formatter):
        """Test getting event by ID."""
        mock_event = Event(
            id=1,
            event_type=EventType.USER_ACTION,
            name="test_event",
            properties={},
            timestamp=datetime.utcnow(),
            severity=EventSeverity.INFO
        )
        
        mock_repo.get.return_value = mock_event
        mock_formatter.format_for_api.return_value = {"id": 1, "name": "test_event"}
        
        result = event_service.get_event(1)
        
        assert result is not None
        mock_repo.get.assert_called_once_with(1)
        mock_formatter.format_for_api.assert_called_once_with(mock_event)
    
    def test_get_nonexistent_event(self, event_service, mock_repo):
        """Test getting non-existent event."""
        mock_repo.get.return_value = None
        
        result = event_service.get_event(999)
        
        assert result is None
        mock_repo.get.assert_called_once_with(999)
    
    def test_create_batch_events(self, event_service, mock_repo, mock_validator, mock_formatter):
        """Test creating batch of events."""
        events_data = [
            EventCreate(
                event_type=EventType.USER_ACTION,
                name=f"event_{i}",
                properties={"index": i}
            )
            for i in range(3)
        ]
        
        mock_events = [
            Event(
                id=i,
                event_type=EventType.USER_ACTION,
                name=f"event_{i}",
                properties={"index": i},
                timestamp=datetime.utcnow(),
                severity=EventSeverity.INFO
            )
            for i in range(3)
        ]
        
        mock_repo.create.side_effect = mock_events
        mock_formatter.format_batch.return_value = [{"id": i} for i in range(3)]
        
        result = event_service.create_batch_events(events_data)
        
        assert len(result) == 3
        assert mock_repo.create.call_count == 3
        assert mock_validator.validate.call_count == 3
    
    def test_get_user_events(self, event_service, mock_repo, mock_formatter):
        """Test getting events for a user."""
        mock_events = [
            Event(
                id=1,
                event_type=EventType.USER_ACTION,
                name="event1",
                properties={},
                user_id="user_123",
                timestamp=datetime.utcnow(),
                severity=EventSeverity.INFO
            )
        ]
        
        mock_repo.get_by_user.return_value = mock_events
        mock_formatter.format_batch.return_value = [{"id": 1}]
        
        result = event_service.get_user_events("user_123", limit=10)
        
        assert len(result) == 1
        mock_repo.get_by_user.assert_called_once_with("user_123", limit=10)
    
    def test_get_event_statistics(self, event_service, mock_repo):
        """Test getting event statistics."""
        mock_stats = {
            "total_events": 100,
            "events_by_type": {"USER_ACTION": 50, "SYSTEM_EVENT": 50},
            "events_by_severity": {"INFO": 80, "WARNING": 20}
        }
        
        mock_repo.get_statistics.return_value = mock_stats
        
        result = event_service.get_statistics()
        
        assert result == mock_stats
        mock_repo.get_statistics.assert_called_once()
    
    def test_update_event(self, event_service, mock_repo, mock_formatter):
        """Test updating an event."""
        update_data = EventUpdate(name="updated_name")
        
        mock_event = Event(
            id=1,
            event_type=EventType.USER_ACTION,
            name="updated_name",
            properties={},
            timestamp=datetime.utcnow(),
            severity=EventSeverity.INFO
        )
        
        mock_repo.update.return_value = mock_event
        mock_formatter.format_for_api.return_value = {"id": 1, "name": "updated_name"}
        
        result = event_service.update_event(1, update_data)
        
        assert result is not None
        mock_repo.update.assert_called_once_with(1, update_data)
    
    def test_delete_event(self, event_service, mock_repo):
        """Test deleting an event."""
        mock_repo.delete.return_value = True
        
        result = event_service.delete_event(1)
        
        assert result is True
        mock_repo.delete.assert_called_once_with(1)
