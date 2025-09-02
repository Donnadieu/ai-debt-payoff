---
created: 2025-09-01T23:21:46Z
last_updated: 2025-09-02T05:25:13Z
version: 1.4
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
├── backend/                    # FastAPI backend (foundation + LLM integration implemented)
│   ├── app/                     # Application modules
│   │   ├── core/                # Core configurations (Redis)
│   │   ├── services/            # Business logic services (LLM, validation)
│   │   ├── workers/             # Background job workers
│   │   └── templates/           # Fallback content templates
│   ├── config.py                # Application configuration
│   ├── database.py              # Database connection and models
│   ├── main.py                  # FastAPI application entry point
│   ├── planner.py               # Debt calculation algorithms
│   ├── test_planner.py          # Unit tests for planner
│   ├── requirements.txt         # Python dependencies
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
├── requirements.txt            # Python dependencies
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
- **Status**: Core foundation + LLM integration implemented with 11 Python files

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
- **API routes**: Grouped by feature domain
- **Database models**: One model per file
- **Services**: Business logic separated from routes (LLM client, validation pipeline)
- **Workers**: Background job processors (nudge generation)
- **Templates**: Fallback content systems (safe nudges)
- **Core**: Infrastructure configurations (Redis, database)
- **Schemas**: Request/response validation

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
- **ORM**: SQLAlchemy for Python backend
- **Migrations**: Alembic for schema management
- **Connection**: Environment-based configuration

## Development Workflow

### File Creation Order
1. Backend API structure
2. Database models and migrations
3. API route implementations
4. Frontend service layer
5. React components and pages

### Testing Structure
- **Backend**: `tests/` directory with pytest
- **Frontend**: `__tests__/` co-located with components
- **Integration**: End-to-end tests in separate directory

## Update History
- 2025-09-02T00:03:17Z: Added epic worktree structure and GitHub integration status
- 2025-09-02T03:49:56Z: Updated backend structure after Issue #13 Core API Foundation completion

---
*Structure reflects current state and planned architecture*
