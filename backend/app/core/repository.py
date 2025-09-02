"""Generic repository pattern for database operations."""

from typing import Generic, TypeVar, Type, Optional, List, Dict, Any
from sqlmodel import SQLModel, Session, select, func
from backend.app.core.database import get_db_session

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=SQLModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=SQLModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Base repository class with common CRUD operations."""
    
    def __init__(self, model: Type[ModelType]):
        self.model = model
    
    def create(self, *, obj_in: CreateSchemaType) -> ModelType:
        """Create a new record."""
        with get_db_session() as session:
            obj_data = obj_in.model_dump()
            db_obj = self.model(**obj_data)
            session.add(db_obj)
            session.commit()
            session.refresh(db_obj)
            return db_obj
    
    def get(self, id: int) -> Optional[ModelType]:
        """Get a record by ID."""
        with get_db_session() as session:
            return session.get(self.model, id)
    
    def get_multi(
        self, 
        *, 
        skip: int = 0, 
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[ModelType]:
        """Get multiple records with pagination and filtering."""
        with get_db_session() as session:
            query = select(self.model)
            
            # Apply filters if provided
            if filters:
                for field, value in filters.items():
                    if hasattr(self.model, field):
                        query = query.where(getattr(self.model, field) == value)
            
            query = query.offset(skip).limit(limit)
            return session.exec(query).all()
    
    def update(self, *, db_obj: ModelType, obj_in: UpdateSchemaType) -> ModelType:
        """Update an existing record."""
        with get_db_session() as session:
            obj_data = obj_in.model_dump(exclude_unset=True)
            for field, value in obj_data.items():
                setattr(db_obj, field, value)
            
            session.add(db_obj)
            session.commit()
            session.refresh(db_obj)
            return db_obj
    
    def delete(self, *, id: int) -> ModelType:
        """Delete a record by ID."""
        with get_db_session() as session:
            obj = session.get(self.model, id)
            if obj:
                session.delete(obj)
                session.commit()
            return obj
    
    def count(self, *, filters: Optional[Dict[str, Any]] = None) -> int:
        """Count records with optional filtering."""
        with get_db_session() as session:
            query = select(func.count()).select_from(self.model)
            
            # Apply filters if provided
            if filters:
                for field, value in filters.items():
                    if hasattr(self.model, field):
                        query = query.where(getattr(self.model, field) == value)
            
            return session.exec(query).one()
    
    def exists(self, *, filters: Dict[str, Any]) -> bool:
        """Check if a record exists with given filters."""
        with get_db_session() as session:
            query = select(self.model)
            
            for field, value in filters.items():
                if hasattr(self.model, field):
                    query = query.where(getattr(self.model, field) == value)
            
            result = session.exec(query.limit(1)).first()
            return result is not None


class NudgeRepository(BaseRepository):
    """Repository for nudge operations."""
    
    def get_by_user_id(self, user_id: str, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Get nudges for a specific user."""
        return self.get_multi(skip=skip, limit=limit, filters={"user_id": user_id})
    
    def get_pending_nudges(self, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Get all pending nudges."""
        return self.get_multi(skip=skip, limit=limit, filters={"status": "pending"})
    
    def get_by_type(self, nudge_type: str, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Get nudges by type."""
        return self.get_multi(skip=skip, limit=limit, filters={"nudge_type": nudge_type})


class AnalyticsRepository(BaseRepository):
    """Repository for analytics operations."""
    
    def get_by_user_id(self, user_id: str, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Get analytics events for a specific user."""
        return self.get_multi(skip=skip, limit=limit, filters={"user_id": user_id})
    
    def get_by_event_type(self, event_type: str, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Get events by type."""
        return self.get_multi(skip=skip, limit=limit, filters={"event_type": event_type})
    
    def get_unprocessed_events(self, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Get unprocessed analytics events."""
        return self.get_multi(skip=skip, limit=limit, filters={"processed": False})


class UserRepository(BaseRepository):
    """Repository for user operations."""
    
    def get_by_user_id(self, user_id: str) -> Optional[ModelType]:
        """Get user by external user ID."""
        with get_db_session() as session:
            query = select(self.model).where(self.model.user_id == user_id)
            return session.exec(query).first()
    
    def get_by_email(self, email: str) -> Optional[ModelType]:
        """Get user by email."""
        with get_db_session() as session:
            query = select(self.model).where(self.model.email == email)
            return session.exec(query).first()
    
    def get_active_users(self, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Get active users."""
        return self.get_multi(skip=skip, limit=limit, filters={"is_active": True})
