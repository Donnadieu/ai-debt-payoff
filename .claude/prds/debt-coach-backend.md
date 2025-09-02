---
name: debt-coach-backend
description: FastAPI backend MVP with payoff planning, nudge generation, and slip-risk detection
status: backlog
created: 2025-09-01T23:33:36Z
---

# PRD: Debt Coach Backend MVP

## Executive Summary

A production-ready FastAPI backend that implements three core debt management features: deterministic payoff planning with Snowball/Avalanche algorithms, AI-powered nudge generation with validation safeguards, and slip-risk detection with actionable recommendations. The system prioritizes reliability, performance, and safety over feature complexity.

## Problem Statement

**What problem are we solving?**
Users need reliable, fast debt payoff calculations and personalized guidance, but existing solutions either lack algorithmic rigor or provide unsafe AI-generated advice that could mislead users about their financial situation.

**Why is this important now?**
- Manual debt planning is error-prone and time-consuming
- Generic financial advice doesn't account for individual debt portfolios
- AI-generated financial advice often contains hallucinated numbers that can be financially harmful
- Users need immediate feedback on budget feasibility to prevent financial slip-ups

## User Stories

### Primary Personas

**Sarah - Young Professional**
- Needs: Quick debt payoff comparison between strategies
- Pain: Doesn't know if snowball or avalanche is better for her situation
- Journey: Inputs debts → Gets strategy comparison → Chooses optimal approach

**Mike - Budget-Conscious Family Man**
- Needs: Validation that his payment plan is feasible
- Pain: Worried about overcommitting and missing payments
- Journey: Plans payments → Gets slip-risk alert → Adjusts budget accordingly

**Lisa - Motivation Seeker**
- Needs: Encouraging, personalized guidance to stay on track
- Pain: Loses motivation without regular positive reinforcement
- Journey: Reviews progress → Gets personalized nudge → Feels motivated to continue

### Detailed User Journeys

1. **Payoff Planning Journey**
   - User inputs debt portfolio (name, balance, APR, minimum payment)
   - System calculates both snowball and avalanche strategies
   - User receives detailed timeline with total interest comparison
   - **Acceptance Criteria**: Results in <500ms for up to 10 debts

2. **Nudge Generation Journey**
   - System analyzes user's current debt situation
   - AI generates encouraging message using only verified facts
   - System validates all numeric claims against actual data
   - User receives safe, personalized motivation
   - **Acceptance Criteria**: No hallucinated numbers ever reach the user

3. **Slip Detection Journey**
   - User plans monthly payments
   - System detects if budget < minimum payments
   - User gets specific suggestion (e.g., "Apply $25 more")
   - **Acceptance Criteria**: Immediate feedback with actionable remedy

## Requirements

### Functional Requirements

**Core Features**
1. **Payoff Planner** (`POST /plan`)
   - Input: Debt portfolio + strategy choice + optional budget
   - Output: Complete payoff schedule with timeline and interest totals
   - Algorithms: Debt Snowball (smallest balance first) and Debt Avalanche (highest APR first)
   - Performance: <500ms for 10 debts on development hardware

2. **Nudge Generator** (`POST /nudge/generate`)
   - Input: User ID and debt plan data
   - Process: Generate AI prompt → Call LLM → Validate output → Return safe nudge
   - Fallback: Deterministic template if validation fails
   - Persistence: Store nudges in database with validation status

3. **Slip Risk Detector** (`POST /slip/check`)
   - Input: Debt portfolio and monthly budget
   - Logic: Detect if budget < sum(minimum payments)
   - Output: Shortfall amount + specific remedy suggestion
   - Rule: Suggest max($25, ceil(shortfall/25)*$25)

**User Interactions**
- RESTful API endpoints with JSON request/response
- Typed Pydantic models for all data structures
- Comprehensive error handling with meaningful messages
- Analytics event tracking at key interaction points

### Non-Functional Requirements

**Performance**
- Payoff calculations: <500ms for 10 debts
- API response times: <200ms for simple operations
- Database queries: Optimized for single-user operations
- Memory usage: Efficient for development/small production loads

**Security**
- Input validation on all endpoints
- SQL injection prevention via SQLModel/SQLAlchemy
- Safe LLM prompt construction (no injection attacks)
- Numeric validation to prevent financial misinformation

**Reliability**
- LLM validation with deterministic fallbacks
- Comprehensive unit test coverage (>90%)
- Error handling that never crashes the service
- Database transactions for data consistency

**Scalability**
- SQLite for development, easy PostgreSQL migration
- Background worker for LLM operations
- Configurable LLM integration (mock/real modes)
- Stateless API design for horizontal scaling

## Success Criteria

### Measurable Outcomes
- **Algorithm Accuracy**: 100% correct payoff calculations vs. manual verification
- **Safety**: 0% hallucinated numbers in production nudges
- **Performance**: 95% of payoff calculations complete in <500ms
- **Reliability**: 99.9% uptime for API endpoints
- **Test Coverage**: >90% code coverage with meaningful tests

### Key Metrics and KPIs
- API response times (P50, P95, P99)
- LLM validation success rate
- Slip detection accuracy rate
- Background worker job completion rate
- Analytics event capture rate

## Constraints & Assumptions

### Technical Constraints
- Python 3.10+ runtime environment
- Single-threaded development deployment
- SQLite database for MVP (PostgreSQL-ready)
- Mock LLM integration (OpenAI/Anthropic-ready)
- No authentication system (user_id parameter only)

### Timeline Constraints
- MVP delivery: 2-3 weeks
- Production-ready code quality from day one
- Comprehensive testing before any deployment
- Documentation complete with delivery

### Resource Constraints
- Single backend developer
- No dedicated DevOps support
- Development hardware performance baseline
- No external API costs during development

### Assumptions
- Users provide accurate debt information
- Monthly budgets are realistic estimates
- LLM responses are generally coherent JSON
- SQLite performance sufficient for single-user testing
- Background workers can handle LLM latency

## Out of Scope

**Explicitly NOT Building**
- User authentication and authorization system
- Frontend web interface or mobile app
- Real-time notifications or email systems
- Integration with banking APIs or financial institutions
- Multi-user support or user management
- Payment processing or financial transactions
- Credit score monitoring or reporting
- Advanced analytics dashboard or reporting
- Deployment infrastructure or CI/CD pipelines
- Rate limiting or API quotas
- Caching layers or performance optimization beyond requirements

## Dependencies

### External Dependencies
- **FastAPI**: Web framework and API documentation
- **SQLModel/SQLAlchemy**: Database ORM and migrations
- **Pydantic**: Data validation and serialization
- **RQ or threading**: Background job processing
- **pytest**: Testing framework
- **uvicorn**: ASGI server for development

### Internal Dependencies
- **Analytics System**: Stub implementation logging to console
- **LLM Client**: Mock implementation with real integration points
- **Database Schema**: SQLite with PostgreSQL migration path
- **Configuration System**: Environment-based settings

### Future Integration Points
- **Real LLM APIs**: OpenAI, Anthropic, or local models
- **Authentication Service**: JWT or session-based auth
- **Production Database**: PostgreSQL with connection pooling
- **Message Queue**: Redis/RabbitMQ for production workers
- **Monitoring**: Application performance monitoring
- **Deployment**: Docker containers and orchestration

## Implementation Details

### API Specification

**POST /plan**
```json
Request: {
  "debts": [{"name": "Credit Card", "balance": 5000, "apr": 0.24, "min_payment": 100}],
  "strategy": "snowball|avalanche",
  "monthly_budget": 500
}

Response: {
  "payoff_date": "2026-03-15",
  "months_to_payoff": 18,
  "total_interest": 1250.50,
  "per_month_totals": [500, 500, 450],
  "per_debt_schedule": [{"name": "Credit Card", "months_to_payoff": 18, "final_balance": 0}],
  "suggestion": {"shortfall_amount": 25}
}
```

**POST /nudge/generate?user_id=123**
```json
Response: {
  "nudge": "You're making great progress! Focus on your Credit Card with $5000 remaining.",
  "cta": "Make Extra Payment",
  "validated": true,
  "fallback": false
}
```

**POST /slip/check**
```json
Request: {same as /plan}
Response: {
  "shortfall": 25,
  "suggestion": {"amount": 25, "label": "Apply $25"}
}
```

### LLM Integration Specification

**Prompt Template**
```
SYSTEM: You are a short, encouraging, educational debt coach. You MUST NOT invent numbers or dates. Use only the exact numeric facts provided.

USER: Facts:
- total_remaining: {{TOTAL}}
- monthly_budget: {{BUDGET}}
- strategy: {{STRATEGY}}
- top_debt: {{TOP_NAME}} (balance: {{TOP_BAL}}, apr: {{TOP_APR}}, payoff_in_months: {{TOP_MONTHS}})
- suggested_extra: {{EXTRA}}

Instruction: Return a single JSON object exactly: {"nudge":"<text>", "cta":"<label>"}. The nudge may include at most one numeric token and that number must exactly match one of the provided numeric facts. If you cannot produce a safe nudge, return {"nudge":"FALLBACK","cta":"FALLBACK"}.
```

**Post-Filter Validation**
1. Parse JSON response from LLM
2. Extract all numeric tokens using regex
3. Verify each number exists in allowed set (TOTAL, BUDGET, TOP_BAL, TOP_MONTHS, EXTRA)
4. Format numbers consistently for comparison
5. Reject and use fallback if any number fails validation

### Analytics Events
- `add_debt`: When debt is added to calculation
- `view_plan`: When payoff plan is generated
- `nudge_generated`: When LLM generates nudge
- `nudge_validated`: When nudge passes validation
- `nudge_rejected`: When nudge fails validation
- `nudge_sent`: When validated nudge is returned to user
- `slip_alert_fired`: When slip risk is detected
- `slip_action_confirmed`: When user acknowledges slip suggestion

### File Structure
```
backend/
├── main.py              # FastAPI app and route definitions
├── models.py            # SQLModel database models
├── planner.py           # Debt payoff algorithms
├── nudge_worker.py      # LLM integration and validation
├── analytics.py         # Event tracking stub
├── llm_client.py        # Mock LLM client with real integration points
├── config.py            # Environment configuration
├── requirements.txt     # Python dependencies
├── .env.example         # Configuration template
├── README.md            # Setup and usage instructions
└── tests/
    ├── test_planner.py      # Algorithm unit tests
    ├── test_nudge.py        # LLM validation tests
    ├── test_slip.py         # Slip detection tests
    └── test_api.py          # API endpoint tests
```

## Quality Assurance

### Testing Requirements
- **Unit Tests**: All algorithms and business logic
- **Integration Tests**: API endpoints with database
- **Validation Tests**: LLM post-filter with mock hallucinations
- **Performance Tests**: 10-debt payoff calculation timing
- **Error Handling Tests**: Invalid inputs and edge cases

### Code Quality Standards
- Type hints for all function signatures
- Pydantic models for all API data
- Comprehensive docstrings for public functions
- Error handling with meaningful messages
- Configuration via environment variables

### Documentation Requirements
- README with exact setup commands
- Sample curl commands for all endpoints
- Code comments explaining business logic
- Integration points clearly marked
- Acceptance criteria in main files

---

*This PRD defines a focused, production-ready MVP that prioritizes safety and reliability in financial calculations while providing a foundation for future AI-powered features.*
