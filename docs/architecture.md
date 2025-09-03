# System Architecture Overview

This document provides a comprehensive overview of the AI Debt Payoff Planner's system architecture, including components, data flow, and integration points.

## Table of Contents

1. [High-Level Architecture](#high-level-architecture)
2. [Core Components](#core-components)
3. [Data Flow](#data-flow)
4. [API Layer](#api-layer)
5. [Business Logic Layer](#business-logic-layer)
6. [Data Layer](#data-layer)
7. [External Integrations](#external-integrations)
8. [Background Processing](#background-processing)
9. [Monitoring & Analytics](#monitoring--analytics)
10. [Security Architecture](#security-architecture)
11. [Deployment Architecture](#deployment-architecture)

## High-Level Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Load Balancer   │    │   Monitoring    │
│   (Future)      │◄──►│   (Nginx/ALB)     │◄──►│   (Analytics)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                    ┌──────────────────────┐
                    │    FastAPI Server    │
                    │                      │
                    │  ┌────────────────┐  │
                    │  │  Middleware    │  │
                    │  │  - CORS        │  │
                    │  │  - Performance │  │
                    │  │  - Analytics   │  │
                    │  └────────────────┘  │
                    │                      │
                    │  ┌────────────────┐  │
                    │  │  API Routes    │  │
                    │  │  - Debt Mgmt   │  │
                    │  │  - Planning    │  │
                    │  │  - AI Coaching │  │
                    │  │  - Analytics   │  │
                    │  └────────────────┘  │
                    └──────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
┌──────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Database   │    │   Redis Cache    │    │  External APIs  │
│  (SQLite/    │    │   - Job Queue    │    │  - LLM Services │
│   PostgreSQL)│    │   - Session      │    │  - Webhooks     │
│              │    │   - Analytics    │    │                 │
└──────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                    ┌──────────────────────┐
                    │  Background Workers  │
                    │  - RQ Workers        │
                    │  - Async Processing  │
                    │  - Job Scheduling    │
                    └──────────────────────┘
```

## Core Components

### 1. FastAPI Application (`main.py`)
- **Purpose**: Main application entry point and configuration
- **Responsibilities**:
  - Application lifecycle management
  - Middleware setup and configuration
  - CORS policy enforcement
  - Route registration and API documentation
- **Key Features**:
  - Auto-generated OpenAPI documentation
  - Async request handling
  - Dependency injection system

### 2. Configuration Management (`config.py`)
- **Purpose**: Centralized application configuration
- **Features**:
  - Environment variable loading
  - Pydantic-based validation
  - Development/production profiles
  - Database URL management

### 3. Database Layer
- **ORM**: SQLModel (built on SQLAlchemy)
- **Development**: SQLite with file-based storage
- **Production**: PostgreSQL with connection pooling
- **Migrations**: Alembic for schema versioning

### 4. Background Processing
- **Queue System**: Redis-based with RQ (Redis Queue)
- **Workers**: Python-based async job processors
- **Use Cases**:
  - LLM API calls
  - Analytics aggregation
  - Email notifications (future)

## Data Flow

### 1. Request Processing Flow

```
Client Request
      │
      ▼
┌─────────────┐
│ Middleware  │ ──► CORS, Performance Tracking, Analytics
└─────────────┘
      │
      ▼
┌─────────────┐
│ Route       │ ──► Path matching, parameter extraction
│ Handler     │
└─────────────┘
      │
      ▼
┌─────────────┐
│ Validation  │ ──► Pydantic schema validation
└─────────────┘
      │
      ▼
┌─────────────┐
│ Business    │ ──► Core logic, calculations
│ Logic       │
└─────────────┘
      │
      ▼
┌─────────────┐
│ Data        │ ──► Database operations, caching
│ Access      │
└─────────────┘
      │
      ▼
┌─────────────┐
│ Response    │ ──► Serialization, status codes
│ Formation   │
└─────────────┘
      │
      ▼
Client Response
```

### 2. Debt Calculation Flow

```
Debt Input
    │
    ▼
┌─────────────────┐
│ Input           │ ──► Validation, normalization
│ Validation      │
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ Strategy        │ ──► Snowball, Avalanche, Compare
│ Selection       │
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ PayoffCalculator│ ──► Mathematical calculations
│ Engine          │     Interest projections
└─────────────────┘     Payment schedules
    │
    ▼
┌─────────────────┐
│ Results         │ ──► Timeline, savings, recommendations
│ Aggregation     │
└─────────────────┘
    │
    ▼
Formatted Response
```

### 3. AI Coaching Flow

```
Coaching Request
    │
    ▼
┌─────────────────┐
│ Context         │ ──► User progress, debt status
│ Gathering       │     Historical data
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ Prompt          │ ──► Template selection
│ Engineering     │     Context injection
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ LLM Integration │ ──► API call (queued)
│ (Async)         │     Response processing
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ Response        │ ──► Content validation
│ Validation      │     Safety filtering
└─────────────────┘
    │
    ▼
Coaching Response
```

## API Layer

### 1. Route Structure

```
/
├── /                    # Root endpoint (API info)
├── /health             # Health check
├── /docs               # OpenAPI documentation
├── /plan               # Debt payoff calculations
├── /nudge/generate     # AI coaching endpoints
├── /api/v1/
│   ├── /debts          # Debt CRUD operations
│   │   ├── /           # List/Create debts
│   │   └── /{id}       # Get/Update/Delete debt
│   ├── /slip/
│   │   └── /check      # Slip detection
│   └── /analytics/     # Analytics endpoints
│       ├── /events     # Event tracking
│       ├── /performance # Performance metrics
│       └── /dashboard  # Dashboard data
```

### 2. Request/Response Flow

- **Request Validation**: Pydantic models ensure data integrity
- **Authentication**: JWT-based (planned implementation)
- **Rate Limiting**: Redis-based request throttling (configurable)
- **Error Handling**: Structured HTTP exceptions with detailed messages
- **Response Formatting**: Consistent JSON structure across endpoints

### 3. Middleware Stack

1. **CORS Middleware**: Cross-origin request handling
2. **Performance Middleware**: Request timing and metrics
3. **Analytics Middleware**: Event tracking and user behavior
4. **Security Middleware**: Input sanitization and protection (future)

## Business Logic Layer

### 1. Core Services

#### Debt Planning Service (`planner.py`)
- **PayoffCalculator**: Mathematical engine for debt strategies
- **Strategy Algorithms**:
  - **Snowball**: Smallest balance first
  - **Avalanche**: Highest interest rate first
  - **Comparison**: Side-by-side analysis
- **Calculations**:
  - Payment schedules
  - Interest savings
  - Payoff timelines
  - Cash flow projections

#### AI Coaching Service (`app/services/nudge_service.py`)
- **Contextual Coaching**: Personalized messaging
- **Progress Tracking**: Achievement recognition
- **Motivation Engine**: Behavioral psychology principles
- **Content Generation**: LLM-powered message creation

#### Slip Detection Service (`app/services/slip_detector.py`)
- **Spending Analysis**: Budget deviation detection
- **Pattern Recognition**: Identifying concerning trends
- **Alert Generation**: Proactive notifications
- **Recovery Recommendations**: Actionable advice

### 2. Validation Services (`app/services/validation.py`)
- **Input Sanitization**: XSS and injection protection
- **Business Rule Enforcement**: Domain-specific validations
- **Data Consistency**: Cross-field validation
- **LLM Response Validation**: Content safety and accuracy

### 3. Analytics Services (`app/services/analytics_service.py`)
- **Event Tracking**: User interaction logging
- **Performance Monitoring**: System health metrics
- **Usage Analytics**: Feature adoption analysis
- **Custom Metrics**: Business KPI tracking

## Data Layer

### 1. Database Schema

#### Core Tables
- **debts**: User debt records
- **users**: User account information (planned)
- **payment_plans**: Generated payoff strategies
- **events**: Analytics and audit trail
- **nudges**: AI coaching history

#### Relationships
- One-to-Many: User → Debts
- One-to-Many: User → Payment Plans
- Many-to-Many: Plans → Strategies

### 2. Data Access Patterns

#### SQLModel Integration
```python
# Model Definition
class Debt(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    name: str
    balance: float
    interest_rate: float
    minimum_payment: float
    
# Query Operations
session.exec(select(Debt).where(Debt.balance > 0))
```

#### Connection Management
- **Development**: File-based SQLite
- **Production**: Connection pooling with PostgreSQL
- **Migrations**: Alembic schema evolution

### 3. Caching Strategy

#### Redis Integration
- **Session Storage**: User authentication state
- **Query Caching**: Expensive calculation results
- **Job Queue**: Background task management
- **Analytics Buffer**: Event aggregation before database write

## External Integrations

### 1. LLM Integration (`app/services/llm_client.py`)

#### Supported Providers
- **OpenAI**: GPT-3.5/GPT-4 models
- **Anthropic**: Claude models (planned)
- **Mock Mode**: Testing and development

#### Integration Features
- **Configurable Endpoints**: Environment-based provider selection
- **Prompt Engineering**: Template-based prompt construction
- **Response Validation**: Content safety and accuracy checking
- **Rate Limiting**: API quota management

### 2. Webhook Integration (Planned)
- **Payment Notifications**: Banking API callbacks
- **User Events**: External system integrations
- **Analytics Export**: Third-party analytics platforms

## Background Processing

### 1. Redis Queue (RQ) Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Request   │    │   Redis Queue   │    │   RQ Worker     │
│                 │    │                 │    │                 │
│  Enqueue Job    │───►│  Job Storage    │───►│  Process Job    │
│  Return Fast    │    │  Priority Mgmt  │    │  Execute Task   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

#### Job Types
- **LLM Processing**: AI coaching generation
- **Analytics Aggregation**: Metric calculations
- **Email Notifications**: Scheduled communications (planned)
- **Data Export**: Report generation (planned)

#### Worker Configuration
- **Concurrency**: Multiple worker processes
- **Error Handling**: Retry logic with exponential backoff
- **Monitoring**: Job status tracking and alerting

### 2. Async Processing Benefits

- **Improved Response Times**: Non-blocking API responses
- **Scalability**: Independent worker scaling
- **Reliability**: Job persistence and retry mechanisms
- **Monitoring**: Detailed job execution tracking

## Monitoring & Analytics

### 1. Performance Monitoring (`app/middleware/performance.py`)

#### Metrics Tracked
- **Request Latency**: Response time distribution
- **Throughput**: Requests per second
- **Error Rates**: HTTP error code tracking
- **Resource Usage**: Memory and CPU utilization

#### Implementation
```python
class PerformanceMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time
        
        # Track metrics
        self.record_metrics(request.url.path, duration, response.status_code)
        return response
```

### 2. Analytics Integration (`app/services/analytics_service.py`)

#### Event Types
- **User Interactions**: Button clicks, page views
- **Business Events**: Debt creation, plan generation
- **System Events**: Errors, performance issues
- **Custom Events**: Feature usage tracking

#### Analytics Dashboard
- **Real-time Metrics**: Live system health
- **Historical Trends**: Usage patterns over time
- **User Behavior**: Feature adoption analysis
- **Performance Insights**: Optimization opportunities

## Security Architecture

### 1. Current Security Measures

#### Input Validation
- **Pydantic Models**: Schema-based validation
- **SQL Injection Prevention**: ORM parameter binding
- **XSS Protection**: Output encoding
- **CORS Configuration**: Controlled cross-origin access

#### Data Protection
- **Environment Variables**: Sensitive data isolation
- **Database Security**: Connection encryption (production)
- **API Key Management**: Secure external service integration

### 2. Planned Security Enhancements

#### Authentication & Authorization
- **JWT Tokens**: Stateless authentication
- **Role-Based Access**: User permission management
- **Session Management**: Secure session handling

#### Additional Protections
- **Rate Limiting**: DDoS protection
- **Input Sanitization**: Advanced threat prevention
- **Audit Logging**: Security event tracking
- **Data Encryption**: At-rest and in-transit protection

## Deployment Architecture

### 1. Development Environment

```
┌─────────────────┐
│   Developer     │
│   Machine       │
│                 │
│ ┌─────────────┐ │
│ │  FastAPI    │ │
│ │  (uvicorn)  │ │
│ └─────────────┘ │
│                 │
│ ┌─────────────┐ │
│ │   SQLite    │ │
│ │   Database  │ │
│ └─────────────┘ │
│                 │
│ ┌─────────────┐ │
│ │   Redis     │ │
│ │   Server    │ │
│ └─────────────┘ │
└─────────────────┘
```

### 2. Production Environment

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Load          │    │   Application   │    │   Database      │
│   Balancer      │    │   Servers       │    │   Cluster       │
│   (Nginx/ALB)   │    │                 │    │                 │
│                 │    │ ┌─────────────┐ │    │ ┌─────────────┐ │
│  SSL            │───►│ │  FastAPI    │ │    │ │ PostgreSQL  │ │
│  Termination    │    │ │  Gunicorn   │ │◄──►│ │  Primary    │ │
│                 │    │ └─────────────┘ │    │ └─────────────┘ │
│  Health         │    │                 │    │                 │
│  Checks         │    │ ┌─────────────┐ │    │ ┌─────────────┐ │
│                 │    │ │  RQ Workers │ │    │ │  Read       │ │
│  Rate           │    │ │  Background │ │    │ │  Replicas   │ │
│  Limiting       │    │ └─────────────┘ │    │ └─────────────┘ │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Redis         │
                       │   Cluster       │
                       │                 │
                       │ ┌─────────────┐ │
                       │ │  Primary    │ │
                       │ │  Cache      │ │
                       │ └─────────────┘ │
                       │                 │
                       │ ┌─────────────┐ │
                       │ │  Queue      │ │
                       │ │  Storage    │ │
                       │ └─────────────┘ │
                       └─────────────────┘
```

### 3. Scaling Considerations

#### Horizontal Scaling
- **Stateless Application**: Easy multi-instance deployment
- **Load Balancing**: Traffic distribution across instances
- **Database Replication**: Read/write splitting
- **Worker Scaling**: Independent background processing scaling

#### Performance Optimization
- **Connection Pooling**: Database connection management
- **Query Optimization**: Efficient database operations
- **Caching Strategy**: Redis-based performance enhancement
- **CDN Integration**: Static asset delivery (future)

## Technology Stack Summary

### Core Technologies
- **Backend Framework**: FastAPI (Python 3.9+)
- **Database**: SQLModel + SQLAlchemy (SQLite/PostgreSQL)
- **Caching/Queue**: Redis + RQ
- **Migration Management**: Alembic
- **Configuration**: Pydantic Settings

### External Services
- **AI/LLM**: OpenAI API, Anthropic Claude (planned)
- **Monitoring**: Custom analytics + external providers (planned)
- **Deployment**: Docker, Kubernetes, or traditional VPS

### Development Tools
- **API Documentation**: FastAPI auto-generated OpenAPI
- **Testing**: pytest with comprehensive test suite
- **Code Quality**: Black formatting, flake8 linting
- **Type Checking**: mypy for static analysis

This architecture provides a solid foundation for the AI Debt Payoff Planner, with clear separation of concerns, scalability considerations, and extensibility for future enhancements.