---
created: 2025-09-01T23:21:46Z
last_updated: 2025-09-03T18:32:44Z
version: 2.1
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
│   ├── epics/
│   │   ├── front-end-core-funcionality/ # Active frontend core functionality epic (20% complete)
│   │   │   ├── 25-analysis.md   # Issue #25 analysis (authentication system)
│   │   │   └── updates/25/      # Stream progress tracking
│   │   └── archived/           # Completed epics
│   │       └── debt-coach-backend/ # Completed backend MVP epic
│   ├── prds/                   # Product requirement documents
│   ├── rules/                  # Project rules and guidelines
│   └── scripts/                # Automation scripts
├── backend/                    # FastAPI backend (foundation + LLM + database + analytics + testing implemented)
├── frontend/                   # React TypeScript frontend (foundation established)
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
├── docs/                       # Complete project documentation
│   ├── api.md                  # API endpoint documentation
│   ├── architecture.md         # System architecture guide
│   └── setup.md               # Detailed setup instructions
├── examples/                   # Working API examples
│   └── curl-commands.sh        # Executable curl examples for all endpoints
├── .env.example                # Environment configuration template
├── AGENTS.md                   # Agent system documentation
├── CLAUDE.md                   # Project management documentation
└── README.md                   # Complete project overview with setup guides
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

### Frontend Structure (Foundation + Component Library Implemented)
```
frontend/
├── src/                        # Source code directory
│   ├── assets/                 # Static assets (React logo, etc.)
│   ├── components/             # Complete UI component library (15+ components)
│   │   ├── Alert/              # Alert component with TypeScript types
│   │   ├── Button/             # Button component with variants
│   │   ├── Card/               # Card layout components
│   │   ├── FormField/          # Form field wrapper component
│   │   ├── Input/              # Input component with validation states
│   │   ├── Loading/            # Loading components (Spinner, Skeleton)
│   │   ├── Modal/              # Modal component with TypeScript fixes
│   │   └── Navigation/         # Navigation components (Header, Sidebar, Breadcrumbs)
│   ├── hooks/                  # Custom React hooks
│   │   ├── api/                # API integration hooks (React Query)
│   │   │   ├── index.ts        # Hook exports
│   │   │   ├── useAnalytics.ts # Analytics API hooks
│   │   │   ├── useCoaching.ts  # Coaching/nudge API hooks
│   │   │   ├── useDebts.ts     # Debt management API hooks
│   │   │   └── useStrategies.ts # Strategy calculation hooks
│   │   └── useAuth.ts          # Authentication hook
│   ├── App.css                 # Main application styles
│   ├── App.tsx                 # Root React component
│   ├── index.css               # Tailwind CSS imports and base styles
│   ├── main.tsx                # React application entry point
│   ├── providers/             # React context providers
│   │   └── QueryProvider.tsx  # React Query provider setup
│   ├── services/              # API service layer (complete)
│   │   └── api/               # API service implementations
│   │       ├── analyticsService.ts # Analytics API methods
│   │       ├── auth.ts        # Authentication service
│   │       ├── client.ts      # HTTP client configuration
│   │       ├── coachingService.ts # Coaching/nudge API methods
│   │       ├── debtService.ts # Debt management API methods
│   │       ├── index.ts       # Service exports
│   │       └── strategyService.ts # Strategy calculation API methods
│   ├── types/                 # TypeScript type definitions
│   │   └── api/               # API response types (complete)
│   │       ├── analytics.ts   # Analytics type definitions
│   │       ├── coaching.ts    # Coaching/nudge type definitions
│   │       ├── debt.ts        # Debt management type definitions
│   │       └── strategy.ts    # Strategy calculation type definitions
│   └── vite-env.d.ts          # Vite environment types
├── public/                     # Public static assets
├── .env.example                # Environment variables template
├── .env.local                  # Local development environment
├── eslint.config.js            # Modern ESLint 9+ configuration
├── .prettierrc                 # Prettier formatting configuration
├── .prettierignore             # Prettier ignore patterns
├── .gitignore                  # Git ignore patterns
├── package.json                # React 19 + TypeScript + Vite dependencies
├── postcss.config.js           # PostCSS configuration for Tailwind
├── tailwind.config.js          # Tailwind CSS 4.1.12 with custom theme
├── tsconfig.app.json           # TypeScript app configuration
├── tsconfig.json               # Base TypeScript configuration
├── tsconfig.node.json          # Node.js TypeScript configuration
├── vite.config.ts              # Vite 6.3.5 build system configuration
└── index.html                  # HTML entry point
```

**Technology Stack Implemented:**
- **React**: 19.1.1 with TypeScript
- **Build System**: Vite 6.3.5 with hot reload (port 3000)
- **Styling**: Tailwind CSS 4.1.12 with custom debt management theme
- **Code Quality**: ESLint 9+ with Prettier integration
- **TypeScript**: Strict mode configuration
- **API Integration**: React Query 5.85.9 + Axios 1.11.0 (complete)
- **Authentication**: Token-based auth with refresh logic
- **Development**: Complete development server and build pipeline

**Status**: Foundation + Component Library + API Integration complete, ready for routing and UI implementation

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
- **Components**: Complete UI component library (15+ components implemented)
  - Alert, Button, Card, FormField, Input, Loading (Spinner/Skeleton)
  - Modal, Navigation (Header/Sidebar/Breadcrumbs)
  - All components with TypeScript types and Tailwind styling
- **Pages**: Route-level components (planned)
- **Hooks**: Custom React hooks for state management (API integration implemented)
  - API hooks with React Query integration (useDebts, useStrategies, useAnalytics, useCoaching)
  - Authentication hook (useAuth) with token management
- **Services**: API communication layer (complete)
  - Service layer with full CRUD operations for all backend endpoints
  - HTTP client with authentication middleware and error handling
- **Types**: Complete TypeScript definitions for all API responses
- **Providers**: React Query provider setup for data management

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
  - 10 test files covering all major components (229+ test functions)
  - Integration tests for API endpoints and database operations
  - Mock services for external dependencies (LLM, Redis)
  - Performance benchmarks and validation tests
  - Test runner with optimized execution and logging
- **Frontend**: `__tests__/` co-located with components (planned)
- **Integration**: End-to-end tests in separate directory (planned)
- **Coverage**: 95% test coverage with extensive test suite

## Update History
- 2025-09-02T00:03:17Z: Added epic worktree structure and GitHub integration status
- 2025-09-02T03:49:56Z: Updated backend structure after Issue #13 Core API Foundation completion
- 2025-09-02T05:55:02Z: Updated structure after Issues #16 & #17 (slip detection + database layer)
- 2025-09-03T03:54:08Z: Updated structure after Issue #19 Testing Suite completion
- 2025-09-03T04:22:53Z: Epic completion - backend MVP with docs/, examples/ and comprehensive backend structure
- 2025-09-03T12:46:10Z: Updated epics structure - backend epic archived, frontend epic (front-end-core-funcionality) activated with tasks 22-32
- 2025-09-03T13:13:15Z: Added complete frontend directory structure - React 19 + TypeScript foundation with Vite 6.3.5, Tailwind CSS 4.1.12, ESLint/Prettier
- 2025-09-03T17:46:12Z: Updated frontend structure with complete UI component library - 15+ components with TypeScript fixes, Issue #25 analysis and stream tracking added
- 2025-09-03T18:32:44Z: Updated frontend structure with complete API integration layer - React Query hooks, service layer, TypeScript types, and authentication system implemented

---
*Structure reflects current state and planned architecture*
