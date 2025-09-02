---
created: 2025-09-01T23:21:46Z
last_updated: 2025-09-02T03:49:56Z
version: 1.1
author: Claude Code PM System
---

# Technology Context

## Update History
- 2025-09-02T00:03:17Z: Added epic worktree structure and GitHub integration status
- 2025-09-02T03:49:56Z: Updated with Issue #13 implementation - FastAPI foundation completed

## Technology Stack

### Backend Technologies
- **Framework**: FastAPI (implemented)
- **Language**: Python 3.10+
- **Database**: SQLite (implemented), PostgreSQL-ready
- **ORM**: SQLModel with SQLAlchemy backend
- **Authentication**: JWT tokens
- **API Documentation**: OpenAPI/Swagger (auto-generated)

### Frontend Technologies
- **Framework**: React 18+ (planned)
- **Build Tool**: Vite
- **Language**: TypeScript
- **State Management**: React Query + Context API
- **Styling**: Tailwind CSS
- **UI Components**: Custom components

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

# Planned additions:
# Authentication & Security
# python-jose[cryptography]
# passlib[bcrypt]
# python-multipart

# Development
# pytest>=7.4.0
# pytest-asyncio
# black
# flake8
```

### Frontend Dependencies (Planned)
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.8.0",
    "@tanstack/react-query": "^4.29.0",
    "axios": "^1.4.0",
    "tailwindcss": "^3.3.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@vitejs/plugin-react": "^4.0.0",
    "typescript": "^5.0.0",
    "vite": "^4.4.0",
    "eslint": "^8.45.0",
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
- **Connection**: SQLAlchemy async engine
- **Migrations**: Alembic version control
- **Pooling**: Connection pooling for performance
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
- **Caching**: Redis for session/data caching (planned)
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
