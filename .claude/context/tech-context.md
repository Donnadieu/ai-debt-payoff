---
created: 2025-09-01T23:21:46Z
last_updated: 2025-09-03T18:32:44Z
version: 1.8
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
- 2025-09-03T18:32:44Z: Updated with Issue #25 completion - React Query and API integration layer implemented

## Technology Stack

### Backend Technologies
- **Framework**: FastAPI (implemented)
- **Language**: Python 3.10+
- **Database**: SQLite (implemented), PostgreSQL-ready
- **ORM**: SQLModel with SQLAlchemy backend
- **Migrations**: Alembic for database version control
- **Authentication**: JWT tokens
- **API Documentation**: OpenAPI/Swagger (auto-generated)

### Frontend Technologies
- **Framework**: React 19 (implemented)
- **Build Tool**: Vite 6.3.5 (implemented)
- **Language**: TypeScript (implemented)
- **State Management**: React Query + Context API (implemented)
- **Styling**: Tailwind CSS 4.1.12 (implemented)
- **UI Components**: Custom components (implemented)
- **HTTP Client**: Axios 1.11.0 (implemented)

### Development Tools
- **Version Control**: Git
- **Project Management**: .claude PM system
- **Agent System**: Claude-based agents for automation
- **Testing**: pytest (backend), Jest/React Testing Library (frontend)
- **Code Quality**: ESLint, Prettier, Black (Python)

## Dependencies

### Backend Dependencies (Implemented)
```python
# Core framework
fastapi==0.115.9
uvicorn[standard]==0.24.0

# Database
sqlmodel==0.0.24

# Configuration
python-dotenv==1.0.1
pydantic==2.11.4
pydantic-settings==2.10.1

# Background Processing (Issue #15)
redis==5.0.1
rq==1.15.1

# Database Migrations (Issue #17)
alembic==1.13.1
email-validator==2.1.0

# Testing (Issue #19 - Implemented)
pytest>=7.4.0
pytest-asyncio

# Planned additions:
# Authentication & Security
# python-jose[cryptography]
# passlib[bcrypt]
# python-multipart

# Development
# black
# flake8
```

### Frontend Dependencies (Implemented)
```json
{
  "dependencies": {
    "react": "^19.1.1",
    "react-dom": "^19.1.1",
    "@tanstack/react-query": "^5.85.9",
    "axios": "^1.11.0"
  },
  "devDependencies": {
    "@types/react": "^19.1.3",
    "@types/react-dom": "^19.1.0",
    "@vitejs/plugin-react": "^6.0.0",
    "typescript": "^5.8.10",
    "vite": "^6.3.5",
    "eslint": "^9.19.0",
    "prettier": "^3.5.1",
    "tailwindcss": "^4.1.12",
    "@tailwindcss/vite": "^4.1.12"
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
- **Status**: Core functionality implemented with React 19, Vite 6.3.5, Tailwind CSS 4.1.12
- **State**: React Query 5.85.9 for server state (implemented), Context for UI state
- **API Integration**: Complete service layer with axios 1.11.0, custom hooks for all endpoints
- **Authentication**: Token-based auth with refresh logic (implemented)
- **Routing**: React Router with lazy loading (planned)
- **Styling**: Utility-first with Tailwind (implemented)

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

## Performance Considerations

### Backend Performance
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
