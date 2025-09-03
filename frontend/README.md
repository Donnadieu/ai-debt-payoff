# AI Debt Payoff Planner

A comprehensive debt payoff planning application with FastAPI backend and React TypeScript frontend.

## Quick Start Guide

### Prerequisites

- **Python 3.10+** with pip
- **Node.js 18+** with npm
- **Git** for version control

### Starting the Complete Application

#### 1. Backend Setup & Start

```bash
# Navigate to backend directory
cd backend/

# Install Python dependencies
pip install -r requirements.txt

# Start the FastAPI server
python3 -m uvicorn main:app --reload --port 8000
```

The backend will be available at: **http://localhost:8000**
- API Documentation: **http://localhost:8000/docs**
- Alternative docs: **http://localhost:8000/redoc**

#### 2. Frontend Setup & Start

```bash
# Navigate to frontend directory (in a new terminal)
cd frontend/

# Install Node.js dependencies
npm install

# Start the React development server
npm run dev
```

The frontend will be available at: **http://localhost:5173**

### Development Workflow

#### Backend Development
```bash
# Run tests
cd backend/
python -m pytest

# Check code formatting
black .
flake8 .

# Database migrations (when needed)
alembic upgrade head
```

#### Frontend Development
```bash
# Run tests
cd frontend/
npm test

# Type checking
npm run type-check

# Linting
npm run lint

# Build for production
npm run build
```

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/debts` | GET | List all debts |
| `/debts` | POST | Create new debt |
| `/debts/{id}` | PUT | Update debt |
| `/debts/{id}` | DELETE | Delete debt |
| `/calculate/snowball` | POST | Calculate snowball strategy |
| `/calculate/avalanche` | POST | Calculate avalanche strategy |
| `/analytics/events` | POST | Track user events |

### Project Structure

```
ai-debt-payoff/
├── backend/           # FastAPI backend
│   ├── main.py       # Application entry point
│   ├── models.py     # Database models
│   ├── planner.py    # Debt calculation logic
│   └── tests/        # Backend tests
├── frontend/         # React TypeScript frontend
│   ├── src/          # Source code
│   ├── public/       # Static assets
│   └── dist/         # Build output
└── docs/            # Documentation
```

### Technology Stack

**Backend:**
- FastAPI (Python web framework)
- SQLModel (Database ORM)
- SQLite (Development database)
- Pytest (Testing)

**Frontend:**
- React 18 with TypeScript
- Vite (Build tool)
- Tailwind CSS (Styling)
- React Query (State management)

### Troubleshooting

#### Port Already in Use
```bash
# Check what's using port 8000
lsof -i :8000

# Kill the process (replace PID)
kill -9 <PID>
```

#### Database Issues
```bash
# Reset database (development only)
cd backend/
rm debt_planner.db
python3 -m uvicorn main:app --reload --port 8000
```

#### Frontend Build Issues
```bash
# Clear node modules and reinstall
cd frontend/
rm -rf node_modules package-lock.json
npm install
```

### Contributing

1. Create feature branch from `main`
2. Make changes with tests
3. Run linting and tests
4. Submit pull request

### Environment Configuration

Copy `.env.example` to `.env` and configure:
```bash
# Backend environment
cp .env.example .env

# Frontend environment (if needed)
cd frontend/
cp .env.example .env.local
```
