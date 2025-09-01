---
created: 2025-09-01T23:21:46Z
last_updated: 2025-09-01T23:21:46Z
version: 1.0
author: Claude Code PM System
---

# Project Style Guide

## Code Style Standards

### Python (Backend)
- **Formatter**: Black with 88-character line length
- **Linter**: flake8 with E203, W503 ignored
- **Import Order**: isort with black-compatible settings
- **Type Hints**: Required for all function signatures
- **Docstrings**: Google-style docstrings for all public functions

```python
# Example function style
def calculate_debt_payoff(
    principal: float,
    interest_rate: float,
    monthly_payment: float
) -> Dict[str, Union[int, float]]:
    """Calculate debt payoff timeline and total interest.
    
    Args:
        principal: Current debt balance
        interest_rate: Annual interest rate as decimal
        monthly_payment: Monthly payment amount
        
    Returns:
        Dictionary containing months_to_payoff and total_interest
    """
    # Implementation here
    pass
```

### TypeScript/JavaScript (Frontend)
- **Formatter**: Prettier with 2-space indentation
- **Linter**: ESLint with TypeScript and React rules
- **Naming**: camelCase for variables, PascalCase for components
- **File Extensions**: `.tsx` for React components, `.ts` for utilities
- **Import Style**: Absolute imports with path mapping

```typescript
// Example component style
interface DebtCardProps {
  debt: Debt;
  onEdit: (debt: Debt) => void;
  onDelete: (id: string) => void;
}

export const DebtCard: React.FC<DebtCardProps> = ({
  debt,
  onEdit,
  onDelete,
}) => {
  // Component implementation
  return <div>...</div>;
};
```

## File Naming Conventions

### Backend Files
- **Models**: `snake_case.py` (e.g., `debt_model.py`)
- **Services**: `snake_case_service.py` (e.g., `debt_calculation_service.py`)
- **Routes**: `snake_case_routes.py` (e.g., `debt_routes.py`)
- **Tests**: `test_snake_case.py` (e.g., `test_debt_service.py`)

### Frontend Files
- **Components**: `PascalCase.tsx` (e.g., `DebtCard.tsx`)
- **Pages**: `PascalCase.tsx` (e.g., `Dashboard.tsx`)
- **Hooks**: `useCamelCase.ts` (e.g., `useDebtCalculation.ts`)
- **Utils**: `camelCase.ts` (e.g., `formatCurrency.ts`)
- **Types**: `camelCase.types.ts` (e.g., `debt.types.ts`)

## Directory Structure Conventions

### Backend Structure
```
backend/
├── app/
│   ├── api/              # API route handlers
│   │   ├── v1/           # API version namespace
│   │   └── dependencies/ # Dependency injection
│   ├── core/             # Core configuration
│   ├── db/               # Database models and setup
│   ├── schemas/          # Pydantic request/response models
│   └── services/         # Business logic layer
├── tests/                # Test suites
└── alembic/              # Database migrations
```

### Frontend Structure
```
frontend/
├── src/
│   ├── components/       # Reusable UI components
│   │   ├── ui/           # Basic UI elements
│   │   └── forms/        # Form components
│   ├── pages/            # Route-level page components
│   ├── hooks/            # Custom React hooks
│   ├── services/         # API service layer
│   ├── types/            # TypeScript type definitions
│   ├── utils/            # Utility functions
│   └── assets/           # Static assets
└── public/               # Public static files
```

## Coding Conventions

### Variable Naming
- **Constants**: `UPPER_SNAKE_CASE`
- **Functions**: Descriptive verbs (`calculateInterest`, `formatCurrency`)
- **Classes**: Nouns in PascalCase (`DebtCalculator`, `PaymentSchedule`)
- **Boolean variables**: Prefixed with `is`, `has`, `can` (`isLoading`, `hasError`)

### Function Design
- **Single Responsibility**: Each function has one clear purpose
- **Pure Functions**: Prefer pure functions without side effects
- **Error Handling**: Explicit error handling with meaningful messages
- **Documentation**: Clear docstrings/comments for complex logic

### Component Design (React)
- **Functional Components**: Use function components with hooks
- **Props Interface**: Define TypeScript interfaces for all props
- **Default Props**: Use default parameters instead of defaultProps
- **Event Handlers**: Prefix with `handle` (`handleSubmit`, `handleChange`)

## API Design Standards

### REST Conventions
- **URLs**: Lowercase with hyphens (`/api/v1/debt-calculations`)
- **HTTP Methods**: Standard REST verbs (GET, POST, PUT, DELETE)
- **Status Codes**: Appropriate HTTP status codes
- **Response Format**: Consistent JSON structure

```python
# Example API response format
{
    "success": true,
    "data": {
        "id": "uuid",
        "name": "Credit Card",
        "balance": 5000.00
    },
    "message": "Debt created successfully",
    "timestamp": "2025-09-01T23:21:46Z"
}
```

### Error Handling
```python
# Example error response
{
    "success": false,
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Invalid interest rate",
        "details": {
            "field": "interest_rate",
            "value": -0.05,
            "constraint": "must_be_positive"
        }
    },
    "timestamp": "2025-09-01T23:21:46Z"
}
```

## Database Conventions

### Table Naming
- **Tables**: `snake_case` plural nouns (`debts`, `payment_schedules`)
- **Columns**: `snake_case` descriptive names (`created_at`, `interest_rate`)
- **Foreign Keys**: `{table}_id` format (`user_id`, `debt_id`)
- **Indexes**: `idx_{table}_{column}` format

### Model Design
- **Timestamps**: Include `created_at` and `updated_at` for all entities
- **Soft Deletes**: Use `deleted_at` timestamp instead of hard deletes
- **UUIDs**: Use UUID primary keys for external-facing entities
- **Constraints**: Appropriate database constraints and validations

## Testing Standards

### Test Organization
- **Unit Tests**: Test individual functions and methods
- **Integration Tests**: Test API endpoints and database interactions
- **Component Tests**: Test React components in isolation
- **E2E Tests**: Test complete user workflows

### Test Naming
```python
# Backend test naming
def test_calculate_debt_payoff_with_valid_inputs():
    """Test debt payoff calculation with valid input parameters."""
    pass

def test_calculate_debt_payoff_raises_error_with_negative_balance():
    """Test that negative balance raises appropriate error."""
    pass
```

```typescript
// Frontend test naming
describe('DebtCard Component', () => {
  it('renders debt information correctly', () => {
    // Test implementation
  });

  it('calls onEdit when edit button is clicked', () => {
    // Test implementation
  });
});
```

## Documentation Standards

### Code Comments
- **When**: Complex business logic, non-obvious algorithms, workarounds
- **Style**: Clear, concise explanations of "why" not "what"
- **Format**: Consistent comment style within each language

### API Documentation
- **OpenAPI**: Auto-generated Swagger documentation for all endpoints
- **Examples**: Include request/response examples
- **Error Codes**: Document all possible error responses
- **Authentication**: Clear authentication requirements

### README Files
- **Purpose**: Clear explanation of module/component purpose
- **Setup**: Step-by-step setup instructions
- **Usage**: Code examples and common use cases
- **Contributing**: Guidelines for code contributions

## Git Conventions

### Commit Messages
```
type(scope): short description

Longer description if needed

- Bullet points for multiple changes
- Reference issue numbers: Fixes #123
```

### Branch Naming
- **Features**: `feature/debt-calculator`
- **Bugs**: `bugfix/payment-calculation-error`
- **Releases**: `release/v1.0.0`
- **Hotfixes**: `hotfix/security-patch`

---
*Consistent style guidelines for maintainable, professional codebase*
