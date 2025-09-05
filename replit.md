# AI Debt Payoff Planner - Replit Project

## Project Overview
This is a comprehensive AI-powered debt payoff planner API built with FastAPI and Python. The application helps users optimize their debt repayment strategies through intelligent analysis, AI coaching, and actionable insights.

## Current Setup Status
- ✅ **Backend**: FastAPI application running on port 5000
- ✅ **Database**: PostgreSQL database configured and connected with auto-created tables
- ✅ **Environment**: Development environment configured with .env file
- ✅ **Dependencies**: All Python packages installed via uv package manager
- ✅ **API Endpoints**: Core debt management and planning endpoints active and tested
- ✅ **Deployment**: Configured for autoscale deployment
- ✅ **Documentation**: OpenAPI/Swagger documentation accessible at /docs
- ✅ **Health Check**: API health endpoint responding correctly

## Project Architecture

### Backend Components
- **Framework**: FastAPI with Python 3.11
- **Database**: PostgreSQL with SQLModel ORM
- **AI Integration**: LLM client for coaching and nudge generation
- **Background Jobs**: Redis/RQ support (configured but optional in development)
- **Analytics**: Performance monitoring and user analytics

### Key Features
1. **Debt Management API** - Full CRUD operations for debt tracking
2. **Payoff Planning** - Calculate optimized payment strategies (snowball vs avalanche)
3. **AI Coaching** - Generate personalized coaching messages and nudges
4. **Slip Detection** - Monitor and detect deviations from debt payoff plans
5. **Analytics** - Track progress with detailed performance metrics

## API Endpoints
- `GET /` - API root information
- `GET /health` - Health check
- `GET /docs` - OpenAPI documentation
- `POST /plan` - Calculate payoff strategies
- `POST /api/v1/debts` - Create new debt
- `GET /api/v1/debts` - List all debts
- `POST /nudge/generate` - Generate AI coaching nudges
- `POST /api/v1/slip/check` - Check for spending slips

## Environment Configuration
The project uses environment variables for configuration:
- Database connection via `DATABASE_URL` (PostgreSQL)
- AI integration via `OPENAI_API_KEY` (currently mock for development)
- Optional Redis via `REDIS_URL`
- Debug mode enabled for development

## Recent Changes
- ✅ Fresh GitHub import successfully set up in Replit environment
- ✅ Installed Python 3.11 with uv package manager
- ✅ Installed all required dependencies from requirements.txt
- ✅ Created and configured PostgreSQL database with environment variables
- ✅ Set up .env file with database URL and OpenAI API key for development
- ✅ Database tables auto-created on startup (debt, nudge, analyticsevent)
- ✅ API server workflow configured and running on port 5000
- ✅ Configured autoscale deployment with proper run command
- ✅ Verified all endpoints working (/, /health, /docs)

## Development Notes
- Server runs on port 5000 (required for Replit)
- Database tables are auto-created on startup
- CORS configured to allow all origins for development
- Mock AI API key configured for development (replace with real key for production)

## Deployment Ready
The project is configured for production deployment with:
- Autoscale deployment target
- Production-ready FastAPI configuration
- Database persistence with PostgreSQL
- Environment variable configuration
- Health check endpoints