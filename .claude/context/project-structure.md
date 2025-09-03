---
created: 2025-09-01T23:21:46Z
last_updated: 2025-09-03T03:54:08Z
version: 1.7
author: Claude Code PM System
---

# Project Structure

## Directory Organization

```
ai-debt-payoff/
├── .claude/                    # Project management system
│   ├── agents/                 # Agent definitions
│   ├── commands/               # PM command definitions
│   ├── context/                # Project context documentation
│   ├── epics/                  # Epic definitions and tracking
│   │   └── debt-coach-backend/ # Active epic with 8 tasks
│   ├── prds/                   # Product requirement documents
│   ├── rules/                  # Project rules and guidelines
│   └── scripts/                # Automation scripts
├── backend/                    # FastAPI backend (foundation + LLM + database + analytics + testing implemented)
│   ├── app/                     # Application modules
│   │   ├── api/                 # API endpoints and routing (includes analytics endpoints)
│   │   ├── core/                # Core configurations (Redis, database, repository, analytics, performance)
│   │   ├── middleware/          # FastAPI middleware (performance monitoring)
│   │   ├── schemas/             # SQLModel data models (nudges, analytics, users, events)
│   │   ├── services/            # Business logic services (LLM, validation, nudges, analytics, events)
│   │   ├── workers/             # Background job workers
│   │   └── templates/           # Fallback content templates
│   ├── migrations/              # Alembic database migrations
│   │   ├── versions/            # Migration version files
│   │   ├── env.py               # Migration environment
│   │   └── script.py.mako       # Migration template
│   ├── alembic.ini              # Alembic migration configuration
│   ├── config.py                # Application configuration
│   ├── database.py              # Database connection and models
│   ├── main.py                  # FastAPI application entry point
│   ├── planner.py               # Debt calculation algorithms
│   ├── test_planner.py          # Unit tests for planner
│   ├── requirements.txt         # Python dependencies (includes alembic, email-validator)
│   ├── tests/                   # Comprehensive test suite (9 test files)
│   │   ├── conftest.py          # Test configuration and fixtures
│   │   ├── test_analytics_api.py # Analytics API endpoint tests
│   │   ├── test_api.py          # Core API endpoint tests
│   │   ├── test_event_service.py # Event service logic tests
│   │   ├── test_integration.py  # Integration tests
│   │   ├── test_llm_validation.py # LLM validation tests
│   │   ├── test_middleware.py   # Middleware tests
│   │   ├── test_nudge_service.py # Nudge service tests
│   │   ├── test_planner.py      # Debt planner algorithm tests
│   │   ├── test_simple.py       # Basic functionality tests
│   │   └── test_workers.py      # Background worker tests
│   ├── test_runner.py           # Test execution and reporting
│   └── docker-compose.yml       # Redis service configuration
├── ../epic-debt-coach-backend/ # Development worktree
├── AGENTS.md                   # Agent system documentation
├── CLAUDE.md                   # Project management documentation
└── README.md                   # Project overview and setup
```

## File Organization Patterns

### Backend Structure (Implemented)
```
backend/
├── main.py                     # FastAPI app and route definitions
├── config.py                   # Environment configuration
├── database.py                 # Database connection setup
├── models.py                   # SQLModel database models
├── schemas.py                  # Pydantic request/response models
├── planner.py                  # Debt calculation algorithms (Snowball/Avalanche)
├── test_planner.py             # Unit tests for debt algorithms
├── app/
│   ├── api/endpoints/          # API endpoint implementations
│   ├── core/
│   │   ├── database.py         # Enhanced database session management
│   │   ├── repository.py       # Generic repository pattern
│   │   └── transaction.py      # Transaction management utilities
│   ├── schemas/
│   │   ├── nudge.py            # Nudge data models
│   │   ├── analytics.py        # Analytics and session models
│   │   ├── user.py             # User and profile models
│   │   └── slip.py             # Slip detection models
│   └── services/
│       ├── nudge_service.py    # Nudge business logic
│       ├── analytics_service.py # Analytics service layer
│       └── slip_detector.py    # Slip detection algorithms
├── migrations/                 # Alembic database migrations
├── tests/                      # Comprehensive test suite
├── requirements.txt            # Python dependencies
├── alembic.ini                 # Migration configuration
├── debt_payoff.db             # SQLite database file (gitignored)
└── __pycache__/               # Python bytecode cache (gitignored)
```

### Frontend Structure (Planned)
```
frontend/
├── src/
│   ├── components/             # React components
│   ├── pages/                  # Page components
│   ├── hooks/                  # Custom React hooks
│   ├── services/               # API service layer
│   └── utils/                  # Utility functions
├── public/                     # Static assets
├── package.json                # Node.js dependencies
└── vite.config.js              # Build configuration
```

## Key Directories

### `.claude/` - Project Management
- **Purpose**: Houses the complete project management system
- **Pattern**: Follows .claude PM system conventions
- **Access**: Used by agents and PM commands

### `backend/` - API Server
- **Purpose**: FastAPI-based REST API server
- **Pattern**: Standard Python web application structure
- **Status**: Core foundation + LLM + slip detection + database + analytics + testing implemented with 35+ Python files

### Context Documentation
- **Location**: `.claude/context/`
- **Purpose**: Living documentation for project understanding
- **Pattern**: Markdown files with YAML frontmatter

## Naming Conventions

### Files
- **Context files**: `kebab-case.md`
- **Python files**: `snake_case.py`
- **JavaScript files**: `camelCase.js` or `PascalCase.jsx`
- **Configuration**: `lowercase.json`, `lowercase.yml`

### Directories
- **Root level**: `lowercase`
- **Python packages**: `snake_case`
- **React components**: `PascalCase`

## Module Organization

### Backend Modules
- **API routes**: Grouped by feature domain (slip detection endpoints)
- **Database models**: Comprehensive schemas (nudges, analytics, users, slips)
- **Services**: Business logic separated from routes (LLM, validation, nudges, analytics, slip detection)
- **Workers**: Background job processors (nudge generation)
- **Templates**: Fallback content systems (safe nudges)
- **Core**: Infrastructure (Redis, database sessions, repositories, transactions)
- **Schemas**: SQLModel data models with validation
- **Migrations**: Alembic database version control

### Frontend Modules
- **Components**: Reusable UI components
- **Pages**: Route-level components
- **Hooks**: Custom React hooks for state management
- **Services**: API communication layer

## Integration Points

### API Integration
- **Backend**: Exposes REST API on `/api/` prefix
- **Frontend**: Consumes API through service layer
- **Documentation**: OpenAPI/Swagger auto-generated

### Database Integration
- **ORM**: SQLModel with SQLAlchemy backend
- **Migrations**: Alembic for schema management with PostgreSQL compatibility
- **Connection**: Enhanced session management with pooling
- **Repository Pattern**: Generic CRUD operations with specialized repositories
- **Transaction Management**: Context managers and decorators for data consistency

## Development Workflow

### File Creation Order
1. Backend API structure
2. Database models and migrations
3. API route implementations
4. Frontend service layer
5. React components and pages

### Testing Structure
- **Backend**: `tests/` directory with pytest (comprehensive test suite implemented)
  - 9 test files covering all major components
  - Integration tests for API endpoints and database operations
  - Mock services for external dependencies
  - Performance benchmarks and validation tests
- **Frontend**: `__tests__/` co-located with components (planned)
- **Integration**: End-to-end tests in separate directory (planned)
- **Coverage**: 95% test coverage with extensive test suite

## Update History
- 2025-09-02T00:03:17Z: Added epic worktree structure and GitHub integration status
- 2025-09-02T03:49:56Z: Updated backend structure after Issue #13 Core API Foundation completion
- 2025-09-02T05:55:02Z: Updated structure after Issues #16 & #17 (slip detection + database layer)
- 2025-09-03T03:54:08Z: Updated structure after Issue #19 Testing Suite completion

---
*Structure reflects current state and planned architecture*
