---
framework: pytest
test_command: pytest
created: 2025-09-03T03:37:15Z
---

# Testing Configuration

## Framework
- Type: pytest
- Version: 8.3.5
- Config File: backend/tests/conftest.py

## Test Structure
- Test Directory: backend/tests
- Test Files: 12 files found
- Naming Pattern: test_*.py

## Commands
- Run All Tests: `cd backend && python3 -m pytest tests/ -v`
- Run Specific Test: `cd backend && python3 -m pytest tests/{test_file} -v`
- Run with Debugging: `cd backend && python3 -m pytest tests/ -v --tb=long -s`

## Environment
- Required ENV vars: PYTHONPATH=backend
- Test Database: SQLite in-memory
- Test Servers: Mock services

## Test Runner Agent Configuration
- Use verbose output for debugging
- Run tests sequentially (no parallel)
- Capture full stack traces
- No mocking - use real implementations
- Wait for each test to complete
