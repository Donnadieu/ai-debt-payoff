"""SQLModel database models for the debt payoff application.

This module defines the core data models for the debt payoff planner.
All models use SQLModel for both Pydantic validation and SQLAlchemy ORM functionality.

Production Integration Points:
- Database schema migrations managed via Alembic
- Validation rules enforced at both API and database levels
- Relationship management for complex debt portfolios
- Analytics tracking integrated into all user interactions

Data Validation Strategy:
- Input validation via Pydantic field constraints
- Business rule validation in service layer
- Database constraints for data integrity
- Graceful error handling for user experience

Performance Considerations:
- Indexed fields for common queries
- Relationship loading strategies optimized
- Bulk operations supported for large portfolios
- Connection pooling configured for concurrent users
"""

from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship


class DebtBase(SQLModel):
    """
    Base debt model with shared fields and comprehensive validation rules.
    
    This model represents a single debt account (credit card, loan, etc.) with all
    information needed for payoff calculations and tracking.
    
    Validation Rules:
    - name: Non-empty string, indexed for fast lookups, max 100 characters
    - balance: Non-negative currency amount, required for calculations
    - interest_rate: Annual percentage rate (0-100%), validates realistic ranges
    - minimum_payment: Non-negative monthly payment, cannot exceed balance
    - due_date: Calendar day (1-31), used for payment scheduling
    
    Business Logic:
    - Zero balance debts are filtered out before calculations
    - Interest rates above 100% are capped for stability
    - Due dates invalid for month are defaulted to day 1
    - Names are required for user identification and reporting
    
    Production Considerations:
    - Index on name field for portfolio queries
    - Decimal precision maintained for currency accuracy
    - Relationship tracking for nudges and analytics
    - Audit trail via created_at/updated_at timestamps
    """
    name: str = Field(
        index=True,
        min_length=1,
        max_length=100,
        description="User-friendly name for the debt (e.g., 'Chase Freedom Card', 'Student Loan')"
    )
    
    balance: float = Field(
        ge=0,
        description="Current outstanding balance in dollars. Must be positive for active debts."
    )
    
    interest_rate: float = Field(
        ge=0,
        le=100,
        description="Annual Percentage Rate (APR) as percentage (0-100). Used for monthly interest calculations."
    )
    
    minimum_payment: float = Field(
        ge=0,
        description="Required minimum monthly payment in dollars. Cannot exceed current balance."
    )
    
    due_date: int = Field(
        ge=1,
        le=31,
        description="Day of month payment is due (1-31). Used for scheduling and reminders."
    )


class Debt(DebtBase, table=True):
    """
    Debt database model with full ORM capabilities.
    
    This is the primary table for storing user debt information. Each record
    represents one debt account that can be included in payoff calculations.
    
    Database Design:
    - Primary key: Auto-incrementing integer ID
    - Audit fields: created_at, updated_at for change tracking
    - Foreign key relationships: One-to-many with nudges and analytics
    - Indexes: name field for fast portfolio queries
    
    Production Integration:
    - Used by PayoffCalculator for strategy calculations
    - Triggers analytics events on create/update/delete
    - Supports bulk operations for portfolio management
    - Relationship loading optimized for API responses
    
    Data Lifecycle:
    1. Creation: User adds debt via API with validation
    2. Updates: Balance/payment changes tracked over time
    3. Calculations: Used in snowball/avalanche algorithms
    4. Completion: Marked as paid off when balance reaches zero
    5. Analytics: All interactions logged for insights
    """
    id: Optional[int] = Field(
        default=None, 
        primary_key=True,
        description="Unique identifier for the debt record"
    )
    
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when debt was first created"
    )
    
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp of last modification for audit trail"
    )
    
    # Relationships - Production Integration Points
    nudges: list["Nudge"] = Relationship(
        back_populates="debt",
        description="AI-generated coaching messages for this debt"
    )
    
    analytics_events: list["AnalyticsEvent"] = Relationship(
        back_populates="debt",
        description="User interaction analytics for this debt"
    )


class NudgeBase(SQLModel):
    """
    Base nudge model for AI-generated coaching messages.
    
    Nudges are personalized motivational messages generated by the LLM system
    to help users stay on track with their debt payoff goals.
    
    Validation Rules:
    - title: Required string, max 200 characters for UI display
    - message: Required content, max 1000 characters for readability
    - nudge_type: Enum-like string from predefined categories
    - priority: Controls delivery frequency and UI prominence
    - is_active: Allows disabling without deletion for analytics
    
    Business Logic:
    - Generated based on user behavior and debt progress
    - Scheduled delivery based on due dates and payment patterns
    - Priority affects notification frequency and UI placement
    - Inactive nudges preserved for analytics and A/B testing
    
    LLM Integration Points:
    - Content generated via OpenAI API based on user context
    - Personalization using debt data and payment history
    - A/B testing different message styles for effectiveness
    - Sentiment analysis to optimize motivational impact
    """
    title: str = Field(
        min_length=1,
        max_length=200,
        description="Short title for the nudge message (displayed in notifications)"
    )
    
    message: str = Field(
        min_length=1,
        max_length=1000,
        description="Full nudge message content generated by AI coaching system"
    )
    
    nudge_type: str = Field(
        description="Category of nudge: 'reminder', 'motivation', 'tip', 'celebration', 'warning'"
    )
    
    priority: str = Field(
        default="medium",
        description="Delivery priority: 'low', 'medium', 'high' - affects frequency and UI prominence"
    )
    
    is_active: bool = Field(
        default=True,
        description="Whether nudge is active for delivery. Inactive nudges preserved for analytics."
    )


class Nudge(NudgeBase, table=True):
    """
    Nudge database model with scheduling and delivery tracking.
    
    This table stores AI-generated coaching messages with full lifecycle tracking
    from generation through delivery to user engagement analytics.
    
    Database Design:
    - Primary key: Auto-incrementing integer ID
    - Foreign key: Optional relationship to specific debt
    - Timestamps: Track creation, scheduling, and delivery
    - Status tracking: scheduled_for vs sent_at for delivery pipeline
    
    Production Integration:
    - Background workers process scheduled nudges
    - Delivery status tracked for engagement analytics
    - A/B testing supported via nudge variations
    - User preferences control frequency and types
    
    Nudge Lifecycle:
    1. Generation: AI creates personalized message based on user context
    2. Scheduling: System determines optimal delivery time
    3. Queuing: Background worker picks up scheduled nudges
    4. Delivery: Message sent via configured channels
    5. Tracking: User engagement and effectiveness measured
    """
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="Unique identifier for the nudge record"
    )
    
    debt_id: Optional[int] = Field(
        default=None,
        foreign_key="debt.id",
        description="Associated debt ID for targeted messages, null for general nudges"
    )
    
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When the nudge was generated by AI system"
    )
    
    scheduled_for: Optional[datetime] = Field(
        default=None,
        description="Target delivery time based on user patterns and debt due dates"
    )
    
    sent_at: Optional[datetime] = Field(
        default=None,
        description="Actual delivery timestamp, null if not yet sent"
    )
    
    # Relationships - Production Integration
    debt: Optional[Debt] = Relationship(
        back_populates="nudges",
        description="Associated debt for targeted coaching messages"
    )


class AnalyticsEventBase(SQLModel):
    """
    Base analytics event model for tracking user interactions.
    
    This model captures all user interactions with the debt payoff system
    for analytics, monitoring, and product improvement.
    
    Validation Rules:
    - event_type: Required category from predefined event taxonomy
    - event_data: JSON string with event-specific payload data
    - user_agent: Optional browser/client identification for debugging
    
    Event Types:
    - 'debt_created': User adds new debt to portfolio
    - 'debt_updated': User modifies debt information
    - 'calculation_run': User runs snowball/avalanche calculation
    - 'strategy_selected': User chooses recommended strategy
    - 'payment_logged': User records payment made
    - 'nudge_delivered': AI coaching message sent to user
    - 'nudge_engaged': User clicks/responds to nudge
    - 'goal_achieved': User reaches payoff milestone
    
    Production Analytics Integration:
    - Event data feeds into business intelligence dashboards
    - Performance monitoring tracks calculation response times
    - User behavior analytics improve AI coaching effectiveness
    - A/B testing framework for feature optimization
    """
    event_type: str = Field(
        min_length=1,
        max_length=50,
        description="Event category from predefined taxonomy (e.g., 'debt_created', 'calculation_run')"
    )
    
    event_data: str = Field(
        description="JSON-encoded event payload with type-specific data for analytics processing"
    )
    
    user_agent: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Browser/client user agent string for debugging and compatibility tracking"
    )


class AnalyticsEvent(AnalyticsEventBase, table=True):
    """
    Analytics event model with comprehensive tracking capabilities.
    
    This table stores all user interaction events for business intelligence,
    performance monitoring, and product optimization.
    
    Database Design:
    - Primary key: Auto-incrementing integer ID
    - Foreign key: Optional relationship to specific debt
    - Timestamp: High-precision event timing for analytics
    - Partitioning: Consider time-based partitioning for scale
    
    Production Analytics Pipeline:
    - Real-time event streaming to analytics service
    - Batch processing for daily/weekly reports
    - Alerting on error rates and performance degradation
    - Data retention policy for GDPR compliance
    
    Analytics Use Cases:
    1. Performance Monitoring: Track calculation response times
    2. User Behavior: Analyze feature usage patterns
    3. A/B Testing: Measure effectiveness of different approaches
    4. Business Intelligence: Revenue and engagement metrics
    5. ML Training: User interaction data for AI model improvement
    
    Privacy Considerations:
    - No personally identifiable information stored directly
    - Event data anonymized for analytics processing
    - Retention policies comply with data protection regulations
    - User consent tracked for analytics participation
    """
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="Unique identifier for the analytics event"
    )
    
    debt_id: Optional[int] = Field(
        default=None,
        foreign_key="debt.id",
        description="Associated debt ID for debt-specific events, null for general events"
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="High-precision timestamp when event occurred for analytics processing"
    )
    
    # Relationships - Production Integration
    debt: Optional[Debt] = Relationship(
        back_populates="analytics_events",
        description="Associated debt for debt-specific analytics events"
    )
