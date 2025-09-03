"""Debt schema definitions for the AI Debt Payoff Planner."""

from datetime import datetime
from decimal import Decimal
from typing import Optional
from sqlmodel import SQLModel, Field


class DebtBase(SQLModel):
    """Base debt model with common fields."""
    name: str = Field(max_length=100, description="Name of the debt")
    balance: float = Field(gt=0, description="Current balance amount")
    interest_rate: float = Field(ge=0, le=100, description="Annual interest rate as percentage")
    minimum_payment: float = Field(gt=0, description="Minimum monthly payment")
    due_date: Optional[int] = Field(default=None, ge=1, le=31, description="Monthly due date")


class DebtCreate(DebtBase):
    """Schema for creating a new debt."""
    pass


class DebtUpdate(SQLModel):
    """Schema for updating an existing debt."""
    name: Optional[str] = Field(default=None, max_length=100)
    balance: Optional[float] = Field(default=None, gt=0)
    interest_rate: Optional[float] = Field(default=None, ge=0, le=100)
    minimum_payment: Optional[float] = Field(default=None, gt=0)
    due_date: Optional[int] = Field(default=None, ge=1, le=31)


class Debt(DebtBase, table=True):
    """Database model for debt records."""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Legacy field mappings for backward compatibility
    @property
    def apr(self) -> float:
        """Legacy property for APR (maps to interest_rate)."""
        return self.interest_rate
    
    @apr.setter
    def apr(self, value: float):
        """Legacy setter for APR."""
        self.interest_rate = value
    
    @property
    def min_payment(self) -> float:
        """Legacy property for min_payment (maps to minimum_payment)."""
        return self.minimum_payment
    
    @min_payment.setter
    def min_payment(self, value: float):
        """Legacy setter for min_payment."""
        self.minimum_payment = value


class DebtResponse(DebtBase):
    """Response schema for debt data."""
    id: int
    created_at: datetime
    updated_at: datetime


class DebtSummary(SQLModel):
    """Summary statistics for debt portfolio."""
    total_balance: float
    total_minimum_payment: float
    average_interest_rate: float
    debt_count: int
    highest_interest_rate: float
    lowest_interest_rate: float
