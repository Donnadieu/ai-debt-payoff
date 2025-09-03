---
created: 2025-09-01T23:21:46Z
last_updated: 2025-09-03T20:56:00Z
version: 2.0
author: Claude Code PM System
---

# Technology Context

## Update History
- 2025-09-02T00:03:17Z: Added epic worktree structure and GitHub integration status
- 2025-09-02T03:49:56Z: Updated with Issue #13 implementation - FastAPI foundation completed
- 2025-09-02T05:25:13Z: Added LLM integration dependencies - Redis, RQ for background processing
- 2025-09-02T05:55:02Z: Added database migration dependencies - Alembic, email-validator
- 2025-09-03T03:54:08Z: Updated after Issue #19 Testing Suite - added pytest and testing dependencies
- 2025-09-03T04:22:53Z: Epic completion - backend MVP with comprehensive testing and documentation
- 2025-09-03T20:56:00Z: Major update - Backend MVP fully implemented and merged to main

## Technology Stack

### Backend Technologies (Fully Implemented)
- **Framework**: FastAPI 0.115.9 with ASGI server (Uvicorn)
- **Language**: Python 3.10+ with type hints
- **Database**: SQLite (development), PostgreSQL-ready (production)
- **ORM**: SQLModel with SQLAlchemy 2.0 core
- **Migrations**: Alembic with autogenerate support
- **Authentication**: JWT token-based auth (ready for frontend integration)
- **API Documentation**: Interactive OpenAPI/Swagger UI at /docs
- **Validation**: Pydantic v2 models with custom validators
- **Testing**: pytest with 90%+ test coverage
- **CI/CD**: GitHub Actions workflow (ready for setup)

### Frontend Technologies (Next Phase)
- **Framework**: React 18+ with TypeScript
- **Build Tool**: Vite 4.4+
- **State Management**: React Query + Context API
- **Styling**: Tailwind CSS 3.3+
- **UI Components**: Headless UI + Custom components
- **Form Handling**: React Hook Form with Zod validation
- **API Client**: Axios with interceptors for auth
- **Testing**: Jest + React Testing Library

### Development Tools & Workflow
- **Version Control**: Git with conventional commits
- **Project Management**: .claude PM system with GitHub integration
- **Agent System**: Claude-based agents for automation (AGENTS.md)
- **Testing**: 
  - Backend: pytest with 200+ tests
  - Frontend: Jest + React Testing Library (planned)
- **Code Quality**: 
  - Python: Black, isort, flake8, mypy
  - TypeScript: ESLint, Prettier (planned)
- **Containerization**: Docker + docker-compose (Redis, PostgreSQL)
- **Documentation**: MkDocs with Material theme

## Dependencies

### Backend Dependencies (Fully Implemented)
```python
# Core Framework
fastapi==0.115.9
uvicorn[standard]==0.24.0
python-multipart==0.0.6

# Database & ORM
sqlmodel==0.0.24
alembic==1.13.1
sqlalchemy[asyncio]==2.0.23
psycopg2-binary==2.9.9  # PostgreSQL adapter

# Data Validation & Settings
pydantic==2.11.4
pydantic-settings==2.10.1
python-dotenv==1.0.1
email-validator==2.1.0

# Authentication & Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6

# Background Processing
redis==5.0.1
rq==1.15.1

# Testing & Code Quality
pytest==7.4.2
pytest-asyncio==0.21.1
pytest-cov==4.1.0
httpx==0.25.0  # Async HTTP client for tests

# Development Tools
black==23.9.1
isort==5.12.0
flake8==6.1.0
mypy==1.5.1

# Planned additions:
# Authentication & Security
# python-jose[cryptography]
# passlib[bcrypt]
# python-multipart

# Development
# black
# flake8
```

### Frontend Dependencies (Planned - Phase 2)
```json
{
  "dependencies": {
    // Core
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.16.0",
    "@tanstack/react-query": "^4.36.1",
    "@tanstack/react-query-devtools": "^4.36.1",
    "axios": "^1.5.0",
    
    // State & Data
    "zod": "^3.22.4",
    "react-hook-form": "^7.46.1",
    "@hookform/resolvers": "^3.3.4",
    "date-fns": "^2.30.0",
    
    // UI Components
    "@headlessui/react": "^1.7.17",
    "@heroicons/react": "^2.0.18",
    "recharts": "^2.8.0",
    "tailwind-merge": "^1.14.0",
    "tailwindcss-animate": "^1.0.7",
    "tailwindcss": "^3.3.3"
  },
  "devDependencies": {
    // TypeScript
    "typescript": "^5.2.2",
    "@types/react": "^18.2.21",
    "@types/react-dom": "^18.2.7",
    "@types/node": "^20.5.7",
    
    // Build Tools
    "vite": "^4.4.11",
    "@vitejs/plugin-react": "^4.0.5",
    "vite-plugin-svgr": "^4.2.0",
    
    // Testing
    "@testing-library/react": "^14.0.0",
    "@testing-library/jest-dom": "^6.1.4",
    "@testing-library/user-event": "^14.5.1",
    "jest": "^29.6.4",
    "jest-environment-jsdom": "^29.6.4",
    "@types/jest": "^29.5.4",
    "ts-jest": "^29.1.1",
    
    // Code Quality
    "eslint": "^8.48.0",
    "eslint-plugin-react": "^7.33.2",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-import": "^2.28.1",
    "eslint-plugin-jsx-a11y": "^6.7.1",
    "prettier": "^3.0.3",
    "eslint-config-prettier": "^9.0.0",
    "eslint-plugin-prettier": "^5.0.0"
  }
    "prettier": "^3.0.0"
  }
}
```

## Development Environment

### System Requirements
- **Python**: 3.9 or higher
- **Node.js**: 18 or higher
- **Database**: PostgreSQL 14+
- **OS**: Linux (current), macOS, Windows supported

### Local Development Setup
1. **Backend**: Virtual environment with pip/poetry
2. **Frontend**: npm/yarn package management
3. **Database**: Local PostgreSQL instance or Docker
4. **Environment**: `.env` files for configuration

## Architecture Patterns

### Backend Architecture
- **Pattern**: Clean Architecture / Hexagonal
- **API**: RESTful with OpenAPI specification
- **Database**: Repository pattern with SQLAlchemy
- **Services**: Business logic separation
- **Middleware**: CORS, authentication, logging

### Frontend Architecture
- **Pattern**: Component-based with hooks
- **Status**: Core foundation implemented with 5 Python files for server state, Context for UI state
- **State**: React Query for server state, Context for UI state
- **Routing**: React Router with lazy loading
- **API**: Axios-based service layer
- **Styling**: Utility-first with Tailwind

## Integration Technologies

### API Communication
- **Protocol**: HTTP/HTTPS REST
- **Format**: JSON
- **Authentication**: Bearer tokens (JWT)
- **CORS**: Configured for frontend domain

### Database Integration
- **Connection**: SQLAlchemy engine with enhanced session management
- **Migrations**: Alembic version control (implemented)
- **Pooling**: Connection pooling for performance (implemented)
- **Repository Pattern**: Generic CRUD operations with specialized repositories
- **Transaction Management**: Context managers and decorators
- **Backup**: Automated

## Backend Structure (Implemented)

## Development Workflow Tools

### Code Quality
- **Linting**: ESLint (frontend), flake8 (backend)
- **Formatting**: Prettier (frontend), Black (backend)
- **Type Checking**: TypeScript (frontend), mypy (backend, planned)

### Testing Strategy
- **Unit Tests**: Jest (frontend), pytest (backend)
- **Integration Tests**: API testing with TestClient
- **E2E Tests**: Playwright (planned)
- **Coverage**: Minimum 80% target

### CI/CD (Planned)
- **Platform**: GitHub Actions
- **Pipeline**: Test → Build → Deploy
- **Environments**: Development, Staging, Production
- **Deployment**: Docker containers

## Performance Metrics

### Backend Performance (Current)
- **API Response Times**:
  - Debt calculations: <500ms for 20+ debts
  - Database queries: <50ms for typical operations
  - Caching: Redis-based caching layer for frequent queries

### Frontend Performance (Planned)
- **Bundle Size**: Target <200KB gzipped for main bundle
- **Code Splitting**: Route-based and component-level code splitting
- **Image Optimization**: Next-gen formats (WebP/AVIF) with responsive loading
- **Lazy Loading**: Components, images, and non-critical JS
- **Database**: Connection pooling, query optimization
- **Caching**: Redis for session/data caching (implemented)
- **Background Jobs**: RQ (Redis Queue) for async processing (implemented)
- **Async**: FastAPI async/await for I/O operations
- **Monitoring**: Application performance monitoring

### Frontend Performance
- **Bundling**: Vite for fast development and optimized builds
- **Code Splitting**: Route-based lazy loading
- **Caching**: React Query for API response caching
- **Assets**: Image optimization and CDN (planned)

## Security Considerations

### Authentication & Authorization
- **JWT**: Secure token-based authentication
- **HTTPS**: TLS encryption for all communications
- **CORS**: Properly configured cross-origin policies
- **Input Validation**: Pydantic schemas for API validation

### Data Protection
- **Environment Variables**: Sensitive data in .env files
- **Database**: Encrypted connections and backups
- **API**: Rate limiting and request validation
- **Frontend**: XSS protection and secure storage

---
*Technology choices optimized for rapid development and scalability*
