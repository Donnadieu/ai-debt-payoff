# Detailed Setup Instructions

This guide provides comprehensive setup instructions for the AI Debt Payoff Planner backend API.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [System Requirements](#system-requirements)
3. [Installation Steps](#installation-steps)
4. [Environment Configuration](#environment-configuration)
5. [Database Setup](#database-setup)
6. [Redis and Background Workers](#redis-and-background-workers)
7. [Development Setup](#development-setup)
8. [Production Setup](#production-setup)
9. [Troubleshooting](#troubleshooting)
10. [Verification](#verification)

## Prerequisites

### Required Software

1. **Python 3.9+**
   ```bash
   # Check Python version
   python --version
   # or
   python3 --version
   ```

2. **pip (Python Package Manager)**
   ```bash
   # Check pip version
   pip --version
   ```

3. **Redis Server**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install redis-server
   
   # macOS with Homebrew
   brew install redis
   
   # Windows - Download from https://redis.io/download
   ```

4. **PostgreSQL** (for production)
   ```bash
   # Ubuntu/Debian
   sudo apt-get install postgresql postgresql-contrib
   
   # macOS with Homebrew
   brew install postgresql
   
   # Windows - Download from https://www.postgresql.org/download/
   ```

5. **Git**
   ```bash
   # Check git version
   git --version
   ```

### Optional Tools

- **curl** - for API testing
- **Postman** or **Insomnia** - for API testing GUI
- **Docker** - for containerized development
- **VS Code** or **PyCharm** - recommended IDEs

## System Requirements

### Minimum Requirements
- **RAM**: 2GB available memory
- **Storage**: 1GB free disk space
- **CPU**: 1 core
- **Network**: Internet connection for dependencies

### Recommended Requirements
- **RAM**: 4GB available memory
- **Storage**: 5GB free disk space
- **CPU**: 2+ cores
- **Network**: Stable broadband connection

## Installation Steps

### 1. Clone the Repository

```bash
# Clone from GitHub
git clone https://github.com/Donnadieu/ai-debt-payoff.git

# Navigate to project directory
cd ai-debt-payoff

# Check project structure
ls -la
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Verify you're in the correct directory
pwd
# Should show: /path/to/ai-debt-payoff/backend
```

### 3. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Verify activation (should show venv path)
which python
```

### 4. Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt

# Verify installation
pip list
```

## Environment Configuration

### 1. Create Environment File

```bash
# Copy template
cp ../.env.example .env

# Edit with your preferred editor
nano .env
# or
vim .env
# or
code .env
```

### 2. Required Configuration

Edit the `.env` file with these minimum required settings:

```bash
# Database (SQLite for development)
DATABASE_URL=sqlite:///./debt_payoff.db

# Redis (required for background workers)
REDIS_URL=redis://localhost:6379/0

# API Settings
ENVIRONMENT=development
DEBUG=true

# LLM Integration (required for nudges)
LLM_API_KEY=your_actual_api_key_here
LLM_MODEL=gpt-3.5-turbo

# Analytics
ENABLE_ANALYTICS=true
ENABLE_PERFORMANCE_MONITORING=true
```

### 3. AI Integration Setup

Choose your AI provider and update the configuration:

#### OpenAI (Recommended)
```bash
LLM_API_KEY=sk-your-openai-api-key
LLM_MODEL=gpt-3.5-turbo
LLM_BASE_URL=https://api.openai.com/v1
```

#### Anthropic (Alternative)
```bash
LLM_API_KEY=your-anthropic-key
LLM_MODEL=claude-3-sonnet
LLM_BASE_URL=https://api.anthropic.com/v1
```

## Database Setup

### Development (SQLite)

SQLite is used by default and requires no additional setup:

```bash
# Initialize database
alembic upgrade head

# Verify database creation
ls -la *.db
# Should show: debt_payoff.db
```

### Production (PostgreSQL)

For production deployment, use PostgreSQL:

```bash
# 1. Create database
sudo -u postgres createdb debt_payoff_production

# 2. Create user (optional)
sudo -u postgres createuser --interactive debt_user

# 3. Grant permissions
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE debt_payoff_production TO debt_user;"

# 4. Update .env file
DATABASE_URL=postgresql://debt_user:password@localhost:5432/debt_payoff_production

# 5. Run migrations
alembic upgrade head
```

### Migration Management

```bash
# Check current migration status
alembic current

# Create new migration (after model changes)
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# View migration history
alembic history --verbose
```

## Redis and Background Workers

### 1. Start Redis Server

```bash
# Start Redis (varies by system)
# Ubuntu/Debian
sudo systemctl start redis-server
sudo systemctl enable redis-server

# macOS with Homebrew
brew services start redis

# Manual start
redis-server

# Test Redis connection
redis-cli ping
# Should return: PONG
```

### 2. Verify Redis Configuration

```bash
# Check Redis status
redis-cli info server

# Test basic operations
redis-cli set test "hello"
redis-cli get test
redis-cli del test
```

### 3. Start Background Workers

```bash
# Start worker (keep this terminal open)
python -m rq worker --url redis://localhost:6379

# For multiple workers (in separate terminals)
python -m rq worker high --url redis://localhost:6379
python -m rq worker default --url redis://localhost:6379
python -m rq worker low --url redis://localhost:6379
```

## Development Setup

### 1. Start All Services

You'll need 3 terminal windows/tabs:

**Terminal 1: Redis Server**
```bash
redis-server
```

**Terminal 2: RQ Worker**
```bash
cd backend
source venv/bin/activate
python -m rq worker --url redis://localhost:6379
```

**Terminal 3: FastAPI Server**
```bash
cd backend
source venv/bin/activate
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Development Tools

```bash
# Format code
black .

# Check code style
flake8 .

# Type checking
mypy .

# Run tests
python -m pytest

# Run tests with coverage
python -m pytest --cov=. --cov-report=html
```

### 3. Debug Mode

For debugging, use these settings in your `.env`:

```bash
DEBUG=true
LOG_LEVEL=DEBUG
RELOAD=true
```

## Production Setup

### 1. Environment Configuration

```bash
# Create production .env
cp .env.example .env.production

# Update production settings
ENVIRONMENT=production
DEBUG=false
DATABASE_URL=postgresql://username:password@host:port/database
REDIS_URL=redis://redis-host:6379/0
SECRET_KEY=your-super-secure-secret-key
CORS_ORIGINS=["https://yourdomain.com"]
```

### 2. Process Management

Use a process manager like Supervisor or systemd:

**Supervisor Configuration (`/etc/supervisor/conf.d/debt-payoff.conf`):**
```ini
[program:debt-payoff-api]
command=/path/to/venv/bin/gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
directory=/path/to/ai-debt-payoff/backend
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/debt-payoff-api.log

[program:debt-payoff-worker]
command=/path/to/venv/bin/python -m rq worker --url redis://localhost:6379
directory=/path/to/ai-debt-payoff/backend
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/debt-payoff-worker.log
```

### 3. Reverse Proxy (Nginx)

**Nginx Configuration (`/etc/nginx/sites-available/debt-payoff`):**
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Troubleshooting

### Common Issues

#### 1. Virtual Environment Issues
```bash
# If activation fails
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 2. Database Connection Errors
```bash
# Check database URL format
echo $DATABASE_URL

# Test SQLite permissions
touch debt_payoff.db
ls -la debt_payoff.db

# Test PostgreSQL connection
psql $DATABASE_URL -c "SELECT version();"
```

#### 3. Redis Connection Issues
```bash
# Check if Redis is running
redis-cli ping

# Check Redis logs
sudo journalctl -u redis-server

# Test Redis URL
redis-cli -u $REDIS_URL ping
```

#### 4. Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Use different port
uvicorn main:app --port 8001
```

#### 5. Import Errors
```bash
# Verify you're in the correct directory
pwd

# Check Python path
python -c "import sys; print(sys.path)"

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Debugging Steps

1. **Check Environment**
   ```bash
   python --version
   which python
   pip list
   ```

2. **Verify Configuration**
   ```bash
   python -c "from config import settings; print(settings.database_url)"
   ```

3. **Test Components**
   ```bash
   # Test database
   alembic current
   
   # Test Redis
   redis-cli ping
   
   # Test API
   curl http://localhost:8000/health
   ```

4. **Check Logs**
   ```bash
   # API logs (if running with uvicorn)
   tail -f /var/log/debt-payoff-api.log
   
   # Worker logs
   tail -f /var/log/debt-payoff-worker.log
   ```

## Verification

### 1. Basic Health Check

```bash
# Start the server and test
curl http://localhost:8000/health

# Expected response:
{
  "status": "healthy",
  "environment": "development"
}
```

### 2. API Documentation

Visit: http://localhost:8000/docs

You should see the FastAPI auto-generated documentation with all endpoints.

### 3. Test API Endpoints

```bash
# Test debt creation
curl -X POST "http://localhost:8000/api/v1/debts" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Credit Card",
    "balance": 1000,
    "interest_rate": 15.0,
    "minimum_payment": 50
  }'

# Test payoff calculation
curl -X POST "http://localhost:8000/plan" \
  -H "Content-Type: application/json" \
  -d '{
    "debts": [{
      "name": "Test Debt",
      "balance": 5000,
      "interest_rate": 18.0,
      "minimum_payment": 100
    }],
    "extra_payment": 200,
    "strategy": "avalanche"
  }'
```

### 4. Test Background Workers

```bash
# Check RQ dashboard (install rq-dashboard first)
pip install rq-dashboard
rq-dashboard --redis-url redis://localhost:6379
# Visit: http://localhost:9181
```

### 5. Run Test Suite

```bash
# Run all tests
python -m pytest -v

# Expected: All tests should pass
# If tests fail, check the error messages and fix accordingly
```

## Next Steps

After successful setup:

1. **Explore API Documentation**: Visit http://localhost:8000/docs
2. **Run Tests**: Execute `python -m pytest` to ensure everything works
3. **Configure AI Integration**: Add your LLM API key for full functionality
4. **Set Up Monitoring**: Enable analytics and performance monitoring
5. **Create Sample Data**: Add some test debts to experiment with

For development workflow and API usage examples, see the main [README.md](../README.md) file.