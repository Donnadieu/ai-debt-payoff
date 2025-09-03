# AI Debt Payoff Planner

A comprehensive web application that helps individuals optimize their debt repayment strategies through intelligent analysis, AI coaching, and actionable insights.

## 🎯 Overview

The AI Debt Payoff Planner empowers users to make informed decisions about debt management by comparing different payoff strategies (debt snowball vs. avalanche), providing AI-powered coaching nudges, detecting spending slips, and tracking progress with detailed analytics.

## ✨ Features

### Core Functionality ✅
- **Multi-Debt Tracking** - Manage unlimited debts with detailed information
- **Strategy Comparison** - Compare debt snowball vs. avalanche methods with detailed calculations
- **AI Coaching** - Intelligent nudges and personalized coaching messages
- **Slip Detection** - Monitor and detect deviations from debt payoff plans
- **Analytics & Monitoring** - Track progress with detailed performance metrics
- **Background Processing** - Asynchronous task processing with Redis and RQ

### API Endpoints
- **Debt Management** - Full CRUD operations for debt tracking
- **Payoff Planning** - `/plan` - Calculate optimized payment strategies
- **Slip Detection** - `/api/v1/slip/check` - Monitor spending deviations
- **Coaching Nudges** - `/nudge/generate` - AI-powered coaching messages
- **Analytics** - `/api/v1/analytics/*` - Performance and progress tracking

## 🏗️ Architecture

### Backend
- **Framework**: FastAPI with Python 3.9+
- **Database**: SQLite (development) / PostgreSQL (production)
- **ORM**: SQLModel with Alembic migrations
- **Background Jobs**: Redis + RQ for async processing
- **Authentication**: JWT-based user sessions (planned)
- **API**: RESTful with auto-generated OpenAPI documentation at `/docs`

### AI Integration
- **LLM Client**: Configurable AI service integration
- **Coaching Engine**: Contextual nudge generation
- **Validation Service**: AI-powered debt plan validation

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- Redis server (for background workers)
- PostgreSQL 14+ (for production) or SQLite (for development)

### 1. Clone and Setup Backend

```bash
# Clone the repository
git clone https://github.com/Donnadieu/ai-debt-payoff.git
cd ai-debt-payoff

# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings
# DATABASE_URL, REDIS_URL, LLM_API_KEY, etc.
```

### 3. Database Setup

```bash
# Initialize database (SQLite for development)
alembic upgrade head

# For production PostgreSQL:
# 1. Create database: createdb debt_payoff_db
# 2. Update DATABASE_URL in .env
# 3. Run migrations: alembic upgrade head
```

### 4. Start Services

```bash
# Terminal 1: Start Redis (required for background workers)
redis-server

# Terminal 2: Start RQ Worker
python -m rq worker --url redis://localhost:6379

# Terminal 3: Start FastAPI server
python -m uvicorn main:app --reload --port 8000
```

### 5. Verify Installation

```bash
# Check API health
curl http://localhost:8000/health

# View API documentation
open http://localhost:8000/docs
```

## 🔧 API Usage Examples

### Calculate Debt Payoff Plan

```bash
curl -X POST "http://localhost:8000/plan" \
  -H "Content-Type: application/json" \
  -d '{
    "debts": [
      {
        "name": "Credit Card 1",
        "balance": 5000,
        "interest_rate": 18.5,
        "minimum_payment": 120
      },
      {
        "name": "Student Loan",
        "balance": 15000,
        "interest_rate": 6.5,
        "minimum_payment": 200
      }
    ],
    "extra_payment": 300,
    "strategy": "compare"
  }'
```

### Generate AI Coaching Nudge

```bash
curl -X POST "http://localhost:8000/nudge/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "user_context": {
      "current_debts": 20000,
      "monthly_payment": 500,
      "progress_percentage": 25
    },
    "nudge_type": "motivational"
  }'
```

### Check for Spending Slip

```bash
curl -X POST "http://localhost:8000/api/v1/slip/check" \
  -H "Content-Type: application/json" \
  -d '{
    "recent_transactions": [
      {"amount": 150, "category": "dining", "date": "2024-01-15"},
      {"amount": 300, "category": "shopping", "date": "2024-01-16"}
    ],
    "budget_limits": {
      "dining": 100,
      "shopping": 200
    }
  }'
```

## 📁 Project Structure

```
ai-debt-payoff/
├── .claude/                    # Project management system
│   ├── context/                # Project documentation
│   ├── epics/                  # Epic definitions and tracking
│   └── prds/                   # Product requirements
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── api/                # API routes and endpoints
│   │   │   ├── endpoints/      # Individual endpoint modules
│   │   │   └── analytics.py    # Analytics router
│   │   ├── core/               # Core configuration
│   │   ├── middleware/         # Custom middleware
│   │   ├── schemas/            # Pydantic request/response schemas
│   │   ├── services/           # Business logic services
│   │   │   ├── analytics_service.py
│   │   │   ├── event_service.py
│   │   │   ├── llm_client.py
│   │   │   ├── nudge_service.py
│   │   │   ├── slip_detector.py
│   │   │   └── validation.py
│   │   └── workers/            # Background job workers
│   ├── migrations/             # Alembic database migrations
│   ├── tests/                  # Comprehensive test suite
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Application configuration
│   ├── database.py             # Database connection setup
│   ├── models.py               # SQLModel database models
│   ├── schemas.py              # Pydantic schemas
│   ├── planner.py              # Debt payoff calculation engine
│   └── requirements.txt        # Python dependencies
├── docs/                       # Detailed documentation
│   ├── setup.md                # Setup instructions
│   └── architecture.md         # System architecture
└── README.md                   # This file
```

## 🛠️ Development

### Running Tests

```bash
# Run all tests
cd backend
python -m pytest

# Run specific test file
python -m pytest tests/test_planner.py -v

# Run with coverage
python -m pytest --cov=. --cov-report=html
```

### Code Style

```bash
# Format code
black .

# Check linting
flake8 .

# Type checking
mypy .
```

### Database Management

```bash
# Create new migration
alembic revision --autogenerate -m "Add new table"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## 🔒 Environment Variables

Required environment variables (see `.env.example` for complete list):

```bash
# Database
DATABASE_URL=sqlite:///./debt_payoff.db

# Redis (for background workers)
REDIS_URL=redis://localhost:6379

# API Configuration
API_TITLE="AI Debt Payoff Planner API"
ENVIRONMENT=development
DEBUG=true

# AI Integration
LLM_API_KEY=your_llm_api_key_here
LLM_MODEL=gpt-3.5-turbo

# Analytics
ENABLE_ANALYTICS=true
ENABLE_PERFORMANCE_MONITORING=true

# CORS
CORS_ORIGINS=["http://localhost:3000"]
```

## 📊 Current Status

**Project Phase**: Backend MVP Complete ✅  
**Backend**: Full API implementation with AI integration  
**Frontend**: Not yet started  
**Database**: Schema implemented with migrations  

### Recent Updates
- ✅ Core API foundation with debt management
- ✅ Debt calculation engine (snowball/avalanche strategies)
- ✅ LLM integration system with AI coaching
- ✅ Slip detection logic and monitoring
- ✅ Database and persistence layer with SQLModel
- ✅ Analytics and performance monitoring
- ✅ Background worker system with Redis/RQ
- ✅ Comprehensive test suite

### Available API Endpoints

| Endpoint | Method | Description | Status |
|----------|--------|-------------|---------|
| `/` | GET | API root information | ✅ |
| `/health` | GET | Health check | ✅ |
| `/docs` | GET | OpenAPI documentation | ✅ |
| `/plan` | POST | Calculate payoff strategies | ✅ |
| `/api/v1/debts` | GET/POST | Debt management | ✅ |
| `/api/v1/debts/{id}` | GET/PUT/DELETE | Individual debt operations | ✅ |
| `/nudge/generate` | POST | AI coaching nudges | ✅ |
| `/api/v1/slip/check` | POST | Slip detection | ✅ |
| `/api/v1/analytics/*` | GET | Analytics endpoints | ✅ |

## 🚀 Deployment

### Production Requirements

1. **Database**: PostgreSQL 14+
2. **Cache/Queue**: Redis 6+
3. **Python**: 3.9+ with virtual environment
4. **Process Manager**: Supervisor or systemd for worker processes
5. **Reverse Proxy**: Nginx or similar
6. **Environment**: Production-grade `.env` configuration

### Production Setup

```bash
# 1. Database setup
createdb debt_payoff_production
export DATABASE_URL="postgresql://user:password@localhost/debt_payoff_production"

# 2. Install and configure
pip install -r requirements.txt
alembic upgrade head

# 3. Start services
# - Redis server
# - RQ workers (multiple instances)
# - FastAPI with Gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 🧪 Testing

The project includes comprehensive tests covering:

- **Unit Tests**: Individual component testing
- **Integration Tests**: API endpoint testing
- **Service Tests**: Business logic validation
- **Analytics Tests**: Monitoring and metrics
- **End-to-End**: Full workflow testing

Run specific test suites:

```bash
# API tests
python -m pytest tests/test_api.py

# Planner logic tests
python -m pytest tests/test_planner.py

# LLM integration tests
python -m pytest tests/test_llm_validation.py

# Analytics tests
python -m pytest tests/test_analytics_api.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes with tests
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

### Development Guidelines
- Follow existing code style and patterns
- Write comprehensive tests for new functionality
- Update documentation for API changes
- Use the `.claude` PM system for task tracking
- Ensure all tests pass before submitting PR

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with FastAPI, SQLModel, and modern Python tools
- AI integration capabilities for enhanced user experience
- Designed for scalability and production deployment
- Comprehensive testing and monitoring included

## 📞 Support

- **API Documentation**: http://localhost:8000/docs (when running locally)
- **GitHub Issues**: For bug reports and feature requests
- **Health Check**: http://localhost:8000/health

---

**Start your journey to debt freedom today!** 🎉