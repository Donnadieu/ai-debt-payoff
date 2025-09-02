"""Unit tests for debt payoff calculation algorithms."""

import pytest
from decimal import Decimal
from datetime import datetime
import time

from planner import PayoffCalculator, validate_debt_portfolio, handle_edge_cases, PerformanceOptimizer
from models import Debt


class TestPayoffCalculator:
    """Test suite for PayoffCalculator class."""
    
    def setup_method(self):
        """Setup test data for each test method."""
        self.calculator = PayoffCalculator(extra_payment=100.0)
        
        # Sample debt data for testing
        self.test_debts = [
            Debt(
                id=1,
                name="Credit Card 1",
                balance=5000.0,
                interest_rate=18.0,
                minimum_payment=150.0,
                due_date=15
            ),
            Debt(
                id=2,
                name="Credit Card 2", 
                balance=2000.0,
                interest_rate=24.0,
                minimum_payment=60.0,
                due_date=20
            ),
            Debt(
                id=3,
                name="Personal Loan",
                balance=8000.0,
                interest_rate=12.0,
                minimum_payment=200.0,
                due_date=5
            )
        ]
    
    def test_snowball_algorithm(self):
        """Test Snowball algorithm (smallest balance first)."""
        result = self.calculator.calculate_snowball(self.test_debts)
        
        assert result['strategy'] == 'snowball'
        assert 'total_months' in result
        assert 'total_payments' in result
        assert 'total_interest' in result
        assert 'monthly_schedule' in result
        assert 'payoff_timeline' in result
        
        # Verify debts are paid off in balance order (smallest first)
        timeline = result['payoff_timeline']
        cc2_month = timeline['Credit Card 2']['month']  # $2000 balance
        cc1_month = timeline['Credit Card 1']['month']  # $5000 balance
        loan_month = timeline['Personal Loan']['month']  # $8000 balance
        
        assert cc2_month < cc1_month < loan_month
    
    def test_avalanche_algorithm(self):
        """Test Avalanche algorithm (highest APR first)."""
        result = self.calculator.calculate_avalanche(self.test_debts)
        
        assert result['strategy'] == 'avalanche'
        assert 'total_months' in result
        assert 'total_payments' in result
        assert 'total_interest' in result
        assert 'monthly_schedule' in result
        assert 'payoff_timeline' in result
        
        # Verify debts are paid off in interest rate order (highest first)
        timeline = result['payoff_timeline']
        cc2_month = timeline['Credit Card 2']['month']  # 24% APR
        cc1_month = timeline['Credit Card 1']['month']  # 18% APR
        loan_month = timeline['Personal Loan']['month']  # 12% APR
        
        assert cc2_month < cc1_month < loan_month
    
    def test_strategy_comparison(self):
        """Test strategy comparison functionality."""
        result = self.calculator.compare_strategies(self.test_debts)
        
        assert 'snowball' in result
        assert 'avalanche' in result
        assert 'comparison' in result
        
        comparison = result['comparison']
        assert 'avalanche_saves_interest' in comparison
        assert 'avalanche_saves_months' in comparison
        assert 'recommended_strategy' in comparison
        assert 'recommendation_reason' in comparison
        
        # Avalanche should typically save interest
        assert comparison['avalanche_saves_interest'] >= 0
    
    def test_performance_requirement(self):
        """Test that calculations meet <500ms performance requirement."""
        start_time = time.time()
        
        # Test with maximum 10 debts
        large_debt_list = []
        for i in range(10):
            large_debt_list.append(Debt(
                id=i+1,
                name=f"Debt {i+1}",
                balance=1000.0 + (i * 500),
                interest_rate=15.0 + i,
                minimum_payment=50.0 + (i * 10),
                due_date=15
            ))
        
        self.calculator.calculate_snowball(large_debt_list)
        self.calculator.calculate_avalanche(large_debt_list)
        
        end_time = time.time()
        calculation_time_ms = (end_time - start_time) * 1000
        
        assert calculation_time_ms < 500, f"Calculation took {calculation_time_ms}ms, exceeds 500ms requirement"
    
    def test_zero_extra_payment(self):
        """Test calculations with no extra payment."""
        calculator = PayoffCalculator(extra_payment=0.0)
        result = calculator.calculate_snowball(self.test_debts)
        
        assert result['total_months'] > 0
        assert result['total_payments'] > 0
        
        # Verify only minimum payments are made
        first_month = result['monthly_schedule'][0]
        expected_total = sum(debt.minimum_payment for debt in self.test_debts)
        assert abs(first_month['total_payment'] - expected_total) < 0.01


class TestValidation:
    """Test suite for debt portfolio validation."""
    
    def test_validate_debt_portfolio_valid(self):
        """Test validation with valid debt data."""
        valid_debts = [
            {
                'name': 'Credit Card',
                'balance': 1000.0,
                'interest_rate': 18.0,
                'minimum_payment': 50.0
            }
        ]
        
        errors = validate_debt_portfolio(valid_debts)
        assert len(errors) == 0
    
    def test_validate_debt_portfolio_empty(self):
        """Test validation with empty debt list."""
        errors = validate_debt_portfolio([])
        assert "At least one debt is required" in errors
    
    def test_validate_debt_portfolio_too_many(self):
        """Test validation with too many debts."""
        too_many_debts = []
        for i in range(11):
            too_many_debts.append({
                'name': f'Debt {i}',
                'balance': 1000.0,
                'interest_rate': 15.0,
                'minimum_payment': 50.0
            })
        
        errors = validate_debt_portfolio(too_many_debts)
        assert any("Maximum 10 debts" in error for error in errors)
    
    def test_validate_debt_portfolio_negative_values(self):
        """Test validation with negative values."""
        invalid_debts = [
            {
                'name': 'Bad Debt',
                'balance': -100.0,
                'interest_rate': -5.0,
                'minimum_payment': -25.0
            }
        ]
        
        errors = validate_debt_portfolio(invalid_debts)
        assert any("Balance cannot be negative" in error for error in errors)
        assert any("Interest rate must be between 0-100%" in error for error in errors)
        assert any("Minimum payment cannot be negative" in error for error in errors)


class TestEdgeCases:
    """Test suite for edge case handling."""
    
    def test_handle_zero_balance_debts(self):
        """Test that zero balance debts are filtered out."""
        debts_with_zero = [
            {'name': 'Active Debt', 'balance': 1000.0, 'interest_rate': 15.0, 'minimum_payment': 50.0},
            {'name': 'Paid Off', 'balance': 0.0, 'interest_rate': 18.0, 'minimum_payment': 0.0}
        ]
        
        cleaned = handle_edge_cases(debts_with_zero)
        assert len(cleaned) == 1
        assert cleaned[0]['name'] == 'Active Debt'
    
    def test_handle_minimum_payment_exceeds_balance(self):
        """Test correction when minimum payment exceeds balance."""
        debts = [
            {'name': 'Small Debt', 'balance': 50.0, 'interest_rate': 15.0, 'minimum_payment': 100.0}
        ]
        
        cleaned = handle_edge_cases(debts)
        assert cleaned[0]['minimum_payment'] == 50.0  # Should be corrected to balance
    
    def test_handle_invalid_interest_rates(self):
        """Test correction of invalid interest rates."""
        debts = [
            {'name': 'High Rate', 'balance': 1000.0, 'interest_rate': 150.0, 'minimum_payment': 50.0},
            {'name': 'Negative Rate', 'balance': 1000.0, 'interest_rate': -5.0, 'minimum_payment': 50.0}
        ]
        
        cleaned = handle_edge_cases(debts)
        assert cleaned[0]['interest_rate'] == 100.0  # Capped at 100%
        assert cleaned[1]['interest_rate'] == 0.0    # Corrected to 0%


class TestPerformanceOptimizer:
    """Test suite for performance optimization utilities."""
    
    def test_optimize_calculation_precision(self):
        """Test decimal precision optimization."""
        value = Decimal('123.456789')
        optimized = PerformanceOptimizer.optimize_calculation_precision(value)
        assert optimized == Decimal('123.46')
    
    def test_batch_interest_calculation(self):
        """Test batch interest calculation for performance."""
        debts = [
            {'balance': Decimal('1000'), 'interest_rate': Decimal('18')},
            {'balance': Decimal('2000'), 'interest_rate': Decimal('24')}
        ]
        
        monthly_interests = PerformanceOptimizer.batch_interest_calculation(debts)
        
        # 18% annual = 1.5% monthly, 24% annual = 2% monthly
        expected_1 = Decimal('1000') * Decimal('0.015')  # $15
        expected_2 = Decimal('2000') * Decimal('0.02')   # $40
        
        assert abs(monthly_interests[0] - expected_1) < Decimal('0.01')
        assert abs(monthly_interests[1] - expected_2) < Decimal('0.01')
    
    def test_validate_performance_requirements(self):
        """Test performance validation with sample debts."""
        test_debts = [
            Debt(id=1, name="Test", balance=1000.0, interest_rate=15.0, minimum_payment=50.0, due_date=15)
        ]
        
        # Should pass performance requirements
        assert PerformanceOptimizer.validate_performance_requirements(test_debts, 500)
        
        # Should fail with too many debts
        too_many_debts = [test_debts[0]] * 11
        assert not PerformanceOptimizer.validate_performance_requirements(too_many_debts, 500)


if __name__ == "__main__":
    # Run basic smoke tests
    calculator = PayoffCalculator(extra_payment=100.0)
    
    sample_debts = [
        Debt(id=1, name="CC1", balance=1000.0, interest_rate=18.0, minimum_payment=50.0, due_date=15),
        Debt(id=2, name="CC2", balance=2000.0, interest_rate=24.0, minimum_payment=75.0, due_date=20)
    ]
    
    print("Testing Snowball algorithm...")
    snowball = calculator.calculate_snowball(sample_debts)
    print(f"Snowball: {snowball['total_months']} months, ${snowball['total_interest']:.2f} interest")
    
    print("Testing Avalanche algorithm...")
    avalanche = calculator.calculate_avalanche(sample_debts)
    print(f"Avalanche: {avalanche['total_months']} months, ${avalanche['total_interest']:.2f} interest")
    
    print("Testing strategy comparison...")
    comparison = calculator.compare_strategies(sample_debts)
    print(f"Recommended: {comparison['comparison']['recommended_strategy']}")
    print(f"Reason: {comparison['comparison']['recommendation_reason']}")
    
    print("✅ All smoke tests passed!")
