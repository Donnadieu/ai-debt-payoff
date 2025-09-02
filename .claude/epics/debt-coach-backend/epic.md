---
name: debt-coach-backend
status: in-progress
created: 2025-09-01T23:36:27Z
progress: 13%
prd: .claude/prds/debt-coach-backend.md
github: https://github.com/Donnadieu/ai-debt-payoff/issues/12
---

# Epic: Debt Coach Backend MVP

## Overview

Production-ready FastAPI backend implementing three core debt management features: deterministic payoff planning algorithms (Snowball/Avalanche), AI-powered nudge generation with strict validation safeguards, and slip-risk detection with actionable recommendations. The system prioritizes safety, performance (<500ms for 10 debts), and reliability over feature complexity.

## Architecture Decisions

### Core Technology Stack
- **FastAPI**: High-performance async web framework with auto-generated OpenAPI docs
- **SQLModel/SQLAlchemy**: Type-safe ORM with PostgreSQL migration path
- **Pydantic**: Comprehensive data validation and serialization
- **RQ + Redis**: Background job processing for LLM operations
- **pytest**: Comprehensive testing framework

### Key Design Patterns
- **Repository Pattern**: Clean separation between business logic and data access
- **Service Layer**: Encapsulated business logic for debt calculations and validation
- **Background Workers**: Async LLM processing to maintain API responsiveness
- **Validation Pipeline**: Multi-stage LLM output validation with deterministic fallbacks
- **Analytics Events**: Comprehensive tracking without external dependencies

### Safety-First Approach
- **Numeric Validation**: Zero tolerance for hallucinated financial numbers
- **Deterministic Fallbacks**: Template-based responses when LLM validation fails
- **Input Sanitization**: Comprehensive validation on all API endpoints
- **Error Boundaries**: Graceful degradation without service crashes

## Technical Approach

### Backend Services

**Core API Endpoints**
1. `POST /plan` - Debt payoff calculation engine
   - Implements both Snowball (smallest balance first) and Avalanche (highest APR first) algorithms
   - Returns complete payoff schedule with timeline and interest projections
   - Performance target: <500ms for 10 debts

2. `POST /nudge/generate` - AI-powered motivation system
   - Background worker generates safe LLM prompts using verified debt data
   - Multi-stage validation pipeline prevents numeric hallucinations
   - Deterministic fallback templates for failed validations
   - Persistence layer for nudge tracking and analytics

3. `POST /slip/check` - Budget feasibility detector
   - Detects when monthly_budget < sum(minimum_payments)
   - Calculates specific shortfall amounts
   - Provides actionable remediation suggestions using rule: max($25, ceil(shortfall/25)*$25)

**Data Models and Schema**
- **Debt**: name, balance, apr, min_payment with validation constraints
- **PayoffPlan**: complete schedule with per-month and per-debt projections
- **Nudge**: LLM-generated content with validation status and metadata
- **Analytics Event**: structured event tracking for user behavior analysis

**Business Logic Components**
- **PayoffCalculator**: Core algorithms for debt payoff strategies
- **LLMValidator**: Post-processing pipeline for safe AI content generation
- **SlipDetector**: Budget feasibility analysis and recommendation engine
- **AnalyticsTracker**: Event collection and console logging

### Infrastructure

**Database Strategy**
- SQLite for development with zero-config setup
- PostgreSQL-ready schema design for production scaling
- Alembic migrations for schema version control
- Connection pooling and transaction management

**Background Processing**
- RQ (Redis Queue) for LLM job processing
- Threaded worker alternative for development environments
- Configurable worker concurrency and retry policies
- Job status tracking and error handling

**Configuration Management**
- Environment-based configuration via .env files
- Feature flags for LLM integration (mock/real modes)
- Database connection string management
- Worker and queue configuration

## Implementation Strategy

### Development Phases

**Phase 1: Core Foundation (Week 1)**
- FastAPI application setup with basic routing
- SQLModel database models and migrations
- Debt payoff algorithms (Snowball/Avalanche)
- Basic API endpoints with Pydantic validation

**Phase 2: LLM Integration (Week 2)**
- Mock LLM client with configurable responses
- Background worker setup with RQ/Redis
- LLM prompt generation and validation pipeline
- Nudge persistence and retrieval

**Phase 3: Testing & Polish (Week 3)**
- Comprehensive unit and integration tests
- Performance optimization and benchmarking
- Documentation and deployment guides
- Analytics integration and monitoring

### Risk Mitigation
- **LLM Reliability**: Strict validation with deterministic fallbacks
- **Performance**: Algorithm optimization and caching strategies
- **Data Safety**: Comprehensive input validation and error handling
- **Scalability**: Stateless design with horizontal scaling readiness

### Testing Approach
- **Unit Tests**: Algorithm correctness, validation logic, slip detection
- **Integration Tests**: API endpoints with database interactions
- **Performance Tests**: 10-debt calculation timing benchmarks
- **Safety Tests**: LLM validation with mock hallucinated responses

## Task Breakdown Preview

High-level task categories for implementation:

- [ ] **Core API Foundation**: FastAPI setup, models, basic endpoints (5-8 hours)
- [ ] **Debt Calculation Engine**: Snowball/Avalanche algorithms with tests (6-8 hours)
- [ ] **LLM Integration System**: Background workers, validation pipeline, mock client (8-10 hours)
- [ ] **Slip Detection Logic**: Budget analysis and recommendation engine (3-4 hours)
- [ ] **Database & Persistence**: SQLModel setup, migrations, data layer (4-5 hours)
- [ ] **Analytics & Monitoring**: Event tracking, logging, performance metrics (3-4 hours)
- [ ] **Testing Suite**: Unit tests, integration tests, performance benchmarks (6-8 hours)
- [ ] **Documentation & Deployment**: README, API docs, setup guides (3-4 hours)

## Dependencies

### External Dependencies
- **Redis**: Required for background job processing (can use Docker for development)
- **Python 3.10+**: Runtime environment with type hint support
- **Development Tools**: pytest, uvicorn, development database

### Internal Dependencies
- **Project Context**: Leverages existing .claude PM system and documentation
- **Configuration**: Environment-based settings for different deployment modes
- **Analytics Stub**: Console logging implementation ready for external service integration

### Integration Points
- **LLM APIs**: OpenAI/Anthropic integration points clearly marked in code
- **Production Database**: PostgreSQL migration path with connection pooling
- **Monitoring**: Application performance monitoring hooks
- **Authentication**: User ID parameter ready for JWT/session integration

## Success Criteria (Technical)

### Performance Benchmarks
- Debt payoff calculations complete in <500ms for 10 debts
- API response times <200ms for simple operations
- Background worker job completion rate >99%
- Database query optimization for single-user workloads

### Quality Gates
- >90% code coverage with meaningful tests
- 100% algorithm accuracy vs. manual verification
- 0% hallucinated numbers in LLM validation pipeline
- All API endpoints return proper HTTP status codes and error messages

### Acceptance Criteria
- All three core endpoints functional with sample data
- LLM validation prevents numeric hallucinations in test scenarios
- Slip detection accurately identifies budget shortfalls
- Complete test suite passes with performance benchmarks met
- README provides exact commands for local development setup

## Estimated Effort

### Overall Timeline
- **Total Effort**: 38-51 hours (approximately 2-3 weeks for single developer)
- **Critical Path**: LLM integration and validation pipeline (most complex component)
- **MVP Delivery**: 2-3 weeks with production-ready code quality

### Resource Requirements
- **Single Backend Developer**: Full-stack Python/FastAPI experience
- **Development Environment**: Local machine with Docker for Redis
- **Testing Infrastructure**: Automated test suite with CI/CD readiness

### Risk Buffer
- **LLM Integration Complexity**: Additional time for validation pipeline edge cases
- **Performance Optimization**: Potential algorithm tuning for large debt portfolios
- **Documentation**: Comprehensive README and API documentation requirements

## Tasks Created
- [ ] #13 - Core API Foundation (parallel: true)
- [ ] #14 - Debt Calculation Engine (parallel: true)
- [ ] #15 - LLM Integration System (parallel: false)
- [ ] #16 - Slip Detection Logic (parallel: true)
- [ ] #17 - Database & Persistence (parallel: true)
- [ ] #18 - Analytics & Monitoring (parallel: true)
- [ ] #19 - Testing Suite (parallel: false)
- [ ] #20 - Documentation & Deployment (parallel: false)

Total tasks: 8
Parallel tasks: 5
Sequential tasks: 3
