"""User data models and schemas."""

from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum
from sqlmodel import SQLModel, Field, Column, JSON
from pydantic import validator, EmailStr


class UserStatus(str, Enum):
    """User account status."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING = "pending"


class UserPreferences(SQLModel):
    """User preferences model."""
    notifications_enabled: bool = Field(default=True)
    email_notifications: bool = Field(default=True)
    nudge_frequency: str = Field(default="daily")  # daily, weekly, custom
    preferred_payment_day: Optional[int] = Field(default=None, ge=1, le=31)
    timezone: str = Field(default="UTC")
    currency: str = Field(default="USD")


class UserBase(SQLModel):
    """Base user model with common fields."""
    email: EmailStr = Field(unique=True, index=True, description="User email address")
    full_name: Optional[str] = Field(default=None, max_length=100)
    is_active: bool = Field(default=True)
    preferences: Optional[UserPreferences] = Field(default=None, sa_column=Column(JSON))


class User(UserBase, table=True):
    """User database model."""
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(unique=True, index=True, description="External user identifier")
    status: UserStatus = Field(default=UserStatus.ACTIVE, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = Field(default=None, index=True)
    login_count: int = Field(default=0)
    
    @validator('updated_at', pre=True, always=True)
    def set_updated_at(cls, v):
        return datetime.utcnow()


class UserCreate(UserBase):
    """Schema for creating a new user."""
    user_id: str = Field(description="External user identifier")


class UserUpdate(SQLModel):
    """Schema for updating a user."""
    email: Optional[EmailStr] = Field(default=None)
    full_name: Optional[str] = Field(default=None, max_length=100)
    is_active: Optional[bool] = Field(default=None)
    status: Optional[UserStatus] = Field(default=None)
    preferences: Optional[UserPreferences] = Field(default=None)


class UserResponse(UserBase):
    """Schema for user API responses."""
    id: int
    user_id: str
    status: UserStatus
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime]
    login_count: int


class UserProfileBase(SQLModel):
    """Base user profile model."""
    user_id: str = Field(foreign_key="users.user_id", index=True)
    total_debt: Optional[float] = Field(default=None, ge=0)
    monthly_income: Optional[float] = Field(default=None, ge=0)
    monthly_expenses: Optional[float] = Field(default=None, ge=0)
    debt_payoff_goal: Optional[datetime] = Field(default=None)
    preferred_strategy: Optional[str] = Field(default=None)
    profile_data: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))


class UserProfile(UserProfileBase, table=True):
    """User profile database model."""
    __tablename__ = "user_profiles"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    @validator('updated_at', pre=True, always=True)
    def set_updated_at(cls, v):
        return datetime.utcnow()


class UserProfileCreate(UserProfileBase):
    """Schema for creating user profiles."""
    pass


class UserProfileUpdate(SQLModel):
    """Schema for updating user profiles."""
    total_debt: Optional[float] = Field(default=None, ge=0)
    monthly_income: Optional[float] = Field(default=None, ge=0)
    monthly_expenses: Optional[float] = Field(default=None, ge=0)
    debt_payoff_goal: Optional[datetime] = Field(default=None)
    preferred_strategy: Optional[str] = Field(default=None)
    profile_data: Optional[Dict[str, Any]] = Field(default=None)


class UserProfileResponse(UserProfileBase):
    """Schema for user profile API responses."""
    id: int
    created_at: datetime
    updated_at: datetime
