---
created: 2025-09-01T23:21:46Z
last_updated: 2025-09-01T23:21:46Z
version: 1.0
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
│   ├── prds/                   # Product requirement documents
│   ├── rules/                  # Project rules and guidelines
│   └── scripts/                # Automation scripts
├── backend/                    # FastAPI backend (empty)
├── AGENTS.md                   # Agent system documentation
└── CLAUDE.md                   # Project management documentation
```

## File Organization Patterns

### Backend Structure (Planned)
```
backend/
├── app/
│   ├── api/                    # API route definitions
│   ├── core/                   # Core configuration
│   ├── db/                     # Database models and connections
│   ├── schemas/                # Pydantic schemas
│   └── services/               # Business logic
├── tests/                      # Test suites
├── requirements.txt            # Python dependencies
└── main.py                     # Application entry point
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
- **Status**: Directory exists but empty

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
- **Services**: Business logic separated from routes
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

---
*Structure reflects current state and planned architecture*
