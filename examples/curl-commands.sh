#!/bin/bash

# AI Debt Payoff Planner - API Curl Commands
# Working curl examples for all API endpoints
# Server should be running on: http://localhost:8000

# =============================================================================
# Configuration
# =============================================================================

# Base URL for the API (change if running on different port)
BASE_URL="http://localhost:8000"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}===================================================${NC}"
echo -e "${BLUE}  AI Debt Payoff Planner - API Examples${NC}"
echo -e "${BLUE}===================================================${NC}"
echo ""

# =============================================================================
# Basic Health Endpoints
# =============================================================================

echo -e "${YELLOW}1. Basic Health Endpoints${NC}"
echo "----------------------------------------"

echo -e "${GREEN}Root endpoint:${NC}"
curl -X GET "${BASE_URL}/" | jq '.'
echo ""

echo -e "${GREEN}Health check:${NC}"
curl -X GET "${BASE_URL}/health" | jq '.'
echo ""

# =============================================================================
# Payoff Plan Calculation
# =============================================================================

echo -e "${YELLOW}2. Payoff Plan Calculation${NC}"
echo "----------------------------------------"

echo -e "${GREEN}Snowball strategy example:${NC}"
curl -X POST "${BASE_URL}/plan" \
  -H "Content-Type: application/json" \
  -d '{
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
  }' | jq '.summary'
echo ""

echo -e "${GREEN}Avalanche strategy example:${NC}"
curl -X POST "${BASE_URL}/plan" \
  -H "Content-Type: application/json" \
  -d '{
    "debts": [
      {
        "name": "Credit Card",
        "balance": 3000.00,
        "interest_rate": 24.99,
        "minimum_payment": 75.00,
        "due_date": 15
      },
      {
        "name": "Personal Loan",
        "balance": 8000.00,
        "interest_rate": 12.5,
        "minimum_payment": 150.00,
        "due_date": 1
      }
    ],
    "strategy": "avalanche",
    "extra_payment": 300.00
  }' | jq '.summary'
echo ""

echo -e "${GREEN}Compare strategies example:${NC}"
curl -X POST "${BASE_URL}/plan" \
  -H "Content-Type: application/json" \
  -d '{
    "debts": [
      {
        "name": "Credit Card A",
        "balance": 1500.00,
        "interest_rate": 19.99,
        "minimum_payment": 40.00,
        "due_date": 15
      },
      {
        "name": "Credit Card B",
        "balance": 3500.00,
        "interest_rate": 16.5,
        "minimum_payment": 70.00,
        "due_date": 10
      },
      {
        "name": "Auto Loan",
        "balance": 12000.00,
        "interest_rate": 4.2,
        "minimum_payment": 280.00,
        "due_date": 5
      }
    ],
    "strategy": "compare",
    "extra_payment": 400.00
  }' | jq '.'
echo ""

# =============================================================================
# Slip Detection Analysis
# =============================================================================

echo -e "${YELLOW}3. Budget Slip Detection${NC}"
echo "----------------------------------------"

echo -e "${GREEN}Budget sufficient (no slip):${NC}"
curl -X POST "${BASE_URL}/api/v1/slip/check" \
  -H "Content-Type: application/json" \
  -d '{
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
  }' | jq '.'
echo ""

echo -e "${GREEN}Budget insufficient (slip detected):${NC}"
curl -X POST "${BASE_URL}/api/v1/slip/check" \
  -H "Content-Type: application/json" \
  -d '{
    "monthly_budget": 200.00,
    "debts": [
      {
        "id": "debt_1",
        "name": "Credit Card",
        "balance": 3000.00,
        "minimum_payment": 100.00
      },
      {
        "id": "debt_2",
        "name": "Personal Loan",
        "balance": 8000.00,
        "minimum_payment": 180.00
      },
      {
        "id": "debt_3",
        "name": "Medical Bill",
        "balance": 2000.00,
        "minimum_payment": 50.00
      }
    ]
  }' | jq '.'
echo ""

echo -e "${GREEN}Slip detection health check:${NC}"
curl -X GET "${BASE_URL}/api/v1/slip/health" | jq '.'
echo ""

# =============================================================================
# Analytics and Event Tracking
# =============================================================================

echo -e "${YELLOW}4. Analytics and Event Tracking${NC}"
echo "----------------------------------------"

echo -e "${GREEN}Track single event:${NC}"
curl -X POST "${BASE_URL}/api/analytics/track" \
  -H "Content-Type: application/json" \
  -d '{
    "event": "plan_calculated",
    "properties": {
      "strategy": "snowball",
      "debt_count": 3,
      "total_debt": 15000.00,
      "extra_payment": 200.00
    },
    "user_id": "user_demo_123"
  }' | jq '.'
echo ""

echo -e "${GREEN}Track multiple events:${NC}"
curl -X POST "${BASE_URL}/api/analytics/batch-track" \
  -H "Content-Type: application/json" \
  -d '[
    {
      "event": "slip_detected",
      "properties": {
        "shortfall": 150.00,
        "debt_count": 2
      },
      "user_id": "user_demo_456"
    },
    {
      "event": "page_view",
      "properties": {
        "page": "dashboard",
        "source": "direct"
      },
      "user_id": "user_demo_456"
    }
  ]' | jq '.'
echo ""

echo -e "${GREEN}Get analytics statistics:${NC}"
curl -X GET "${BASE_URL}/api/analytics/stats" | jq '.'
echo ""

echo -e "${GREEN}Get performance statistics:${NC}"
curl -X GET "${BASE_URL}/api/analytics/performance" | jq '.'
echo ""

echo -e "${GREEN}Analytics health check:${NC}"
curl -X GET "${BASE_URL}/api/analytics/health" | jq '.'
echo ""

# =============================================================================
# AI Nudge Generation
# =============================================================================

echo -e "${YELLOW}5. AI Nudge Generation${NC}"
echo "----------------------------------------"

echo -e "${GREEN}Generate motivational nudge:${NC}"
curl -X POST "${BASE_URL}/nudge/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "demo_user_123",
    "debt_plan": {
      "strategy": "snowball",
      "total_debt": 7500.00,
      "total_months": 24,
      "monthly_payment": 350.00,
      "total_interest": 671.83
    }
  }' | jq '.'
echo ""

echo -e "${GREEN}Generate nudge for avalanche strategy:${NC}"
curl -X POST "${BASE_URL}/nudge/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "demo_user_456",
    "debt_plan": {
      "strategy": "avalanche",
      "total_debt": 12000.00,
      "total_months": 36,
      "monthly_payment": 450.00,
      "total_interest": 3200.00
    }
  }' | jq '.'
echo ""

# =============================================================================
# Debt Management (Basic CRUD)
# =============================================================================

echo -e "${YELLOW}6. Debt Management (Basic CRUD)${NC}"
echo "----------------------------------------"

echo -e "${GREEN}Get all debts:${NC}"
curl -X GET "${BASE_URL}/api/v1/debts" | jq '.'
echo ""

echo -e "${GREEN}Create a debt:${NC}"
curl -X POST "${BASE_URL}/api/v1/debts" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Demo Credit Card",
    "balance": 1250.75,
    "interest_rate": 18.5,
    "minimum_payment": 35.00
  }' | jq '.'
echo ""

# =============================================================================
# Testing Error Scenarios
# =============================================================================

echo -e "${YELLOW}7. Error Handling Examples${NC}"
echo "----------------------------------------"

echo -e "${GREEN}Invalid payoff strategy:${NC}"
curl -X POST "${BASE_URL}/plan" \
  -H "Content-Type: application/json" \
  -d '{
    "debts": [
      {
        "name": "Test Debt",
        "balance": 1000.00,
        "interest_rate": 15.0,
        "minimum_payment": 25.00,
        "due_date": 15
      }
    ],
    "strategy": "invalid_strategy",
    "extra_payment": 100.00
  }' | jq '.'
echo ""

echo -e "${GREEN}Missing required debt fields:${NC}"
curl -X POST "${BASE_URL}/api/v1/debts" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Incomplete Debt",
    "balance": 1000.00
  }' | jq '.'
echo ""

echo -e "${GREEN}Invalid budget slip request:${NC}"
curl -X POST "${BASE_URL}/api/v1/slip/check" \
  -H "Content-Type: application/json" \
  -d '{
    "monthly_budget": -100.00,
    "debts": []
  }' | jq '.'
echo ""

# =============================================================================
# Documentation and Swagger UI
# =============================================================================

echo -e "${YELLOW}8. API Documentation${NC}"
echo "----------------------------------------"

echo -e "${GREEN}Interactive API documentation is available at:${NC}"
echo -e "${BLUE}${BASE_URL}/docs${NC} (Swagger UI)"
echo -e "${BLUE}${BASE_URL}/redoc${NC} (ReDoc)"
echo ""

echo -e "${YELLOW}9. OpenAPI Schema${NC}"
echo "----------------------------------------"

echo -e "${GREEN}Get OpenAPI JSON schema:${NC}"
curl -X GET "${BASE_URL}/openapi.json" | jq '.info'
echo ""

echo -e "${BLUE}===================================================${NC}"
echo -e "${BLUE}  All API Examples Complete!${NC}"
echo -e "${BLUE}===================================================${NC}"
echo -e "${GREEN}For interactive testing, visit: ${BASE_URL}/docs${NC}"
echo ""

# Note: This script requires 'jq' for pretty JSON formatting
# Install with: sudo apt-get install jq (Ubuntu/Debian) or brew install jq (macOS)