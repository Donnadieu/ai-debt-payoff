# CLAUDE.md

> Think carefully and implement the most concise solution that changes as little code as possible.

## Project-Specific Instructions

### AI Debt Payoff Planner

This is a debt payoff planning application with FastAPI backend and React frontend.

**Architecture:**
- Backend: FastAPI with SQLAlchemy, Pydantic models
- Frontend: React with TypeScript, Tailwind CSS
- Database: PostgreSQL for production, SQLite for development
- Testing: pytest for backend, Jest/React Testing Library for frontend

**Development Guidelines:**
- Follow the epic structure in `.claude/epics/debt-payoff-planner/`
- Use sub-agents (file-analyzer, code-analyzer) for analysis tasks
- Always use real datetime in frontmatter (never hardcode timestamps)
- Implement atomic commits with clear issue references
- No partial implementations - complete features fully
- Include comprehensive tests for all functions
- Follow RESTful API patterns for backend endpoints

**Key Features:**
- Debt tracking and management
- Payment strategy calculations (snowball, avalanche)
- Progress visualization and reporting
- User authentication and data persistence

**Current Status:**
- Project structure established with `.claude/` management
- Backend directory exists but needs API foundation implementation
- Active task: Backend API Foundation (Task 001.md)

## Testing

Always run tests before committing:
- `npm test` or equivalent for your stack

## Code Style

Follow existing patterns in the codebase.
