# AI Debt Payoff Planner API Documentation

Complete API reference for the AI Debt Payoff Planner backend service.

## Overview

The AI Debt Payoff Planner API provides endpoints for debt management, payoff strategy calculation, budget slip detection, and AI-powered coaching nudges. The API follows REST conventions and returns JSON responses.

**Base URL**: `http://localhost:8000`

**Interactive Documentation**:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Authentication

Currently, the API does not require authentication. In production, endpoints would be secured with appropriate authentication mechanisms.

## API Endpoints

### Health & Status

#### GET /
Root endpoint providing basic API information.

**Response**:
```json
{
  "message": "AI Debt Payoff Planner API",
  "version": "1.0.0",
  "docs": "/docs",
  "redoc": "/redoc"
}
```

#### GET /health
Health check endpoint for monitoring API availability.

**Response**:
```json
{
  "status": "healthy",
  "environment": "development"
}
```

---

### Payoff Planning

#### POST /plan
Calculate debt payoff plans using different strategies.

**Request Body**:
```json
{
  "debts": [
    {
      "name": "Credit Card",
      "balance": 2500.00,
      "interest_rate": 18.99,
      "minimum_payment": 50.00,
      "due_date": 15
    },
    {
      "name": "Student Loan",
      "balance": 5000.00,
      "interest_rate": 6.5,
      "minimum_payment": 100.00,
      "due_date": 1
    }
  ],
  "strategy": "snowball",
  "extra_payment": 200.00
}
```

**Parameters**:
- `debts` (array): List of debt objects (1-10 debts allowed)
  - `name` (string): Descriptive name for the debt
  - `balance` (number): Current outstanding balance
  - `interest_rate` (number): Annual interest rate (0-100%)
  - `minimum_payment` (number): Required minimum monthly payment
  - `due_date` (number): Day of month payment is due (1-31)
- `strategy` (string): Payoff strategy - "snowball", "avalanche", or "compare"
- `extra_payment` (number): Additional monthly payment amount (optional, default: 0)

**Strategies**:
- **Snowball**: Pays minimum on all debts, extra payment goes to smallest balance
- **Avalanche**: Pays minimum on all debts, extra payment goes to highest interest rate
- **Compare**: Returns both snowball and avalanche strategies with comparison

**Response Example** (Snowball Strategy):
```json
{
  "strategy": "snowball",
  "total_months": 24,
  "total_payments": 8171.83,
  "total_interest": 671.83,
  "payoff_timeline": {
    "Credit Card": {
      "month": 11,
      "date": "2026-07"
    },
    "Student Loan": {
      "month": 24,
      "date": "2027-08"
    }
  },
  "monthly_schedule": [
    {
      "month": 1,
      "date": "2025-09",
      "payments": [
        {
          "debt_name": "Credit Card",
          "payment": 250.0,
          "interest_portion": 39.40,
          "principal_portion": 210.60
        }
      ],
      "total_payment": 350.0,
      "remaining_balances": {
        "Credit Card": 2289.56,
        "Student Loan": 4927.08
      }
    }
  ],
  "summary": {
    "total_debt": 7500.0,
    "total_interest_saved": 0,
    "completion_date": "2027-08"
  }
}
```

**curl Example**:
```bash
curl -X POST "http://localhost:8000/plan" \
  -H "Content-Type: application/json" \
  -d '{
    "debts": [
      {
        "name": "Credit Card",
        "balance": 2500.00,
        "interest_rate": 18.99,
        "minimum_payment": 50.00,
        "due_date": 15
      }
    ],
    "strategy": "snowball",
    "extra_payment": 200.00
  }'
```

---

### Budget Slip Detection

#### POST /api/v1/slip/check
Analyze budget feasibility and detect potential payment slips.

**Request Body**:
```json
{
  "monthly_budget": 500.00,
  "debts": [
    {
      "id": "debt_1",
      "name": "Credit Card",
      "balance": 2500.00,
      "minimum_payment": 75.00
    },
    {
      "id": "debt_2",
      "name": "Student Loan",
      "balance": 15000.00,
      "minimum_payment": 150.00
    }
  ]
}
```

**Parameters**:
- `monthly_budget` (number): Available monthly budget amount
- `debts` (array): List of debt objects for analysis
  - `id` (string): Unique debt identifier
  - `name` (string): Debt name or description
  - `balance` (number): Current debt balance (optional)
  - `minimum_payment` (number): Required minimum monthly payment

**Response Example** (Budget Sufficient):
```json
{
  "is_feasible": true,
  "has_slip": false,
  "monthly_budget": 500.00,
  "total_minimum_payments": 225.00,
  "surplus": 275.00,
  "shortfall": 0.0,
  "suggestion_amount": 0.0,
  "suggestion_text": null,
  "message": "Budget is sufficient for all minimum payments"
}
```

**Response Example** (Budget Insufficient):
```json
{
  "is_feasible": false,
  "has_slip": true,
  "monthly_budget": 200.00,
  "total_minimum_payments": 330.00,
  "surplus": 0.0,
  "shortfall": 130.00,
  "suggestion_amount": 150.00,
  "suggestion_text": "Apply $150",
  "message": "Budget shortfall of $130.00. Consider applying $150 additional monthly budget."
}
```

**curl Example**:
```bash
curl -X POST "http://localhost:8000/api/v1/slip/check" \
  -H "Content-Type: application/json" \
  -d '{
    "monthly_budget": 300.00,
    "debts": [
      {
        "id": "debt_1",
        "name": "Credit Card",
        "minimum_payment": 100.00
      }
    ]
  }'
```

#### GET /api/v1/slip/health
Health check endpoint for slip detection service.

**Response**:
```json
{
  "status": "healthy",
  "service": "slip_detection",
  "timestamp": "2025-09-03T04:00:00.000Z"
}
```

---

### AI Nudge Generation

#### POST /nudge/generate
Generate AI-powered motivational nudges based on debt payoff plans.

**Request Body**:
```json
{
  "user_id": "user_123",
  "debt_plan": {
    "strategy": "snowball",
    "total_debt": 7500.00,
    "total_months": 24,
    "monthly_payment": 350.00,
    "total_interest": 671.83
  }
}
```

**Parameters**:
- `user_id` (string): User identifier (1-50 characters)
- `debt_plan` (object): Debt payoff plan data for context
  - `strategy` (string): Payoff strategy being used
  - `total_debt` (number): Total debt amount
  - `total_months` (number): Expected months to payoff
  - `monthly_payment` (number): Monthly payment amount (optional)
  - `total_interest` (number): Total interest to be paid (optional)

**Response Example**:
```json
{
  "success": true,
  "job_id": null,
  "nudge": {
    "title": "Stay Motivated!",
    "message": "Focus on your smallest debt first - those quick wins will fuel your motivation!",
    "nudge_type": "motivation",
    "priority": 3,
    "user_id": "user_123"
  },
  "source": "fallback",
  "message": "Nudge generated successfully"
}
```

**Response Fields**:
- `success` (boolean): Whether nudge generation succeeded
- `job_id` (string): Job identifier for async processing (if applicable)
- `nudge` (object): Generated nudge content
  - `title` (string): Nudge title/headline
  - `message` (string): Main motivational message
  - `nudge_type` (string): Type of nudge (motivation, reminder, etc.)
  - `priority` (number): Priority level (1-5)
  - `user_id` (string): User identifier
- `source` (string): Content source - "llm", "fallback", or "error_fallback"
- `message` (string): Response status message

**curl Example**:
```bash
curl -X POST "http://localhost:8000/nudge/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "demo_user",
    "debt_plan": {
      "strategy": "avalanche",
      "total_debt": 12000.00,
      "total_months": 36
    }
  }'
```

---

### Analytics & Event Tracking

#### POST /api/analytics/track
Track individual analytics events.

**Request Body**:
```json
{
  "event": "plan_calculated",
  "properties": {
    "strategy": "snowball",
    "debt_count": 3,
    "total_debt": 15000.00
  },
  "user_id": "user_123"
}
```

**Parameters**:
- `event` (string): Event name
- `properties` (object): Event properties and metadata
- `user_id` (string): User identifier (optional)

**Response**:
```json
{
  "success": true,
  "message": "Event tracked successfully",
  "event_id": null
}
```

#### POST /api/analytics/batch-track
Track multiple analytics events in a single request.

**Request Body**:
```json
[
  {
    "event": "slip_detected",
    "properties": {
      "shortfall": 150.00,
      "debt_count": 2
    },
    "user_id": "user_456"
  },
  {
    "event": "page_view",
    "properties": {
      "page": "dashboard"
    },
    "user_id": "user_456"
  }
]
```

**Response**:
```json
{
  "success": true,
  "message": "Successfully tracked 2 events",
  "tracked_count": 2
}
```

#### GET /api/analytics/stats
Get analytics system statistics.

**Response**:
```json
{
  "buffer_size": 15,
  "last_flush": 1725339600.0,
  "enabled_services": ["console", "file"],
  "config": {
    "enabled": true,
    "buffer_size": 100,
    "flush_interval": 30.0
  }
}
```

#### GET /api/analytics/performance
Get performance monitoring statistics.

**Response**:
```json
{
  "timestamp": "2025-09-03T04:00:00.000Z",
  "system_metrics": {
    "memory_usage": 45.2,
    "cpu_usage": 12.1
  },
  "operation_stats": {
    "plan_calculation": {
      "avg_time": 0.125,
      "call_count": 45
    }
  },
  "total_metrics_collected": 150,
  "thresholds": {
    "response_time": 1.0,
    "memory_usage": 80.0
  }
}
```

#### GET /api/analytics/health
Health check for analytics system.

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2025-09-03T04:00:00.000Z",
  "analytics": {
    "enabled": true,
    "buffer_size": 15,
    "services_count": 2
  },
  "system_health": {
    "status": "healthy",
    "checks_passed": 3
  }
}
```

**curl Examples**:
```bash
# Track single event
curl -X POST "http://localhost:8000/api/analytics/track" \
  -H "Content-Type: application/json" \
  -d '{
    "event": "plan_calculated",
    "properties": {"strategy": "snowball"},
    "user_id": "demo_user"
  }'

# Get analytics stats
curl -X GET "http://localhost:8000/api/analytics/stats"
```

---

### Debt Management (CRUD)

#### GET /api/v1/debts
Get all debt records.

**Response**:
```json
{
  "debts": []
}
```

#### POST /api/v1/debts
Create a new debt record.

**Request Body**:
```json
{
  "name": "Credit Card",
  "balance": 1250.75,
  "interest_rate": 18.5,
  "minimum_payment": 35.00
}
```

**Response**:
```json
{
  "success": true,
  "message": "Debt created successfully",
  "debt": {
    "name": "Credit Card",
    "balance": 1250.75,
    "interest_rate": 18.5,
    "minimum_payment": 35.00
  }
}
```

#### GET /api/v1/debts/{debt_id}
Get a specific debt by ID.

**Response**:
```json
{
  "debt_id": 1,
  "message": "Debt retrieval endpoint - to be implemented"
}
```

#### PUT /api/v1/debts/{debt_id}
Update a specific debt by ID.

#### DELETE /api/v1/debts/{debt_id}
Delete a specific debt by ID.

---

## Error Responses

The API returns standard HTTP status codes and JSON error responses:

**400 Bad Request**:
```json
{
  "detail": "Invalid strategy. Use 'snowball', 'avalanche', or 'compare'"
}
```

**422 Unprocessable Entity**:
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "debts"],
      "msg": "Field required"
    }
  ]
}
```

**500 Internal Server Error**:
```json
{
  "detail": "Internal error during slip analysis: Database connection failed"
}
```

## Rate Limits

Currently, no rate limiting is implemented. In production, appropriate rate limits would be configured based on endpoint and user.

## Data Validation

All endpoints include comprehensive input validation:

- **Numbers**: Must be non-negative where applicable
- **Interest Rates**: Must be between 0-100%
- **Debt Names**: Must be 1-100 characters
- **Arrays**: Debt lists limited to 1-10 items
- **Dates**: Due dates must be 1-31

## Content Safety

The nudge generation endpoint includes content validation:

- Financial figures are validated against hallucinations
- Generic motivational language is preferred over specific numbers
- Fallback templates ensure consistent quality
- All generated content is reviewed for appropriateness

## Complete Working Examples

For complete working curl command examples, see: `/examples/curl-commands.sh`

This script includes:
- All endpoint examples with realistic data
- Error handling scenarios
- Batch operations
- Health check commands
- Performance monitoring examples

Run the script after starting the server:
```bash
chmod +x examples/curl-commands.sh
./examples/curl-commands.sh
```

## Development

**Start Development Server**:
```bash
cd backend
python -m uvicorn main:app --reload --port 8000
```

**View Interactive Documentation**:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

**API Schema**:
- OpenAPI JSON: http://localhost:8000/openapi.json