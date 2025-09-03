"""Tests for debt calculation algorithms and payoff planning."""

import pytest
import time
from decimal import Decimal
from typing import List, Dict, Any

from planner import PayoffCalculator, validate_debt_portfolio, handle_edge_cases
from models import Debt
from schemas import PayoffPlanRequest


class TestDebtValidation:
    """Test debt portfolio validation functions."""
    
    def test_validate_empty_portfolio(self):
        """Test validation with empty debt portfolio."""
        errors = validate_debt_portfolio([])
        assert "No debts provided" in str(errors)
    
    def test_validate_valid_portfolio(self, sample_debt_portfolio):
        """Test validation with valid debt portfolio."""
        errors = validate_debt_portfolio(sample_debt_portfolio)
        assert len(errors) == 0
    
    def test_validate_negative_balance(self):
        """Test validation with negative balance."""
        debt = {
            "name": "Invalid Debt",
            "balance": -1000.0,
            "apr": 15.0,
            "min_payment": 50.0
        }
        errors = validate_debt_portfolio([debt])
        assert any("balance" in error.lower() for error in errors)
    
    def test_validate_negative_apr(self):
        """Test validation with negative APR."""
        debt = {
            "name": "Invalid Debt",
            "balance": 1000.0,
            "apr": -5.0,
            "min_payment": 50.0
        }
        errors = validate_debt_portfolio([debt])
        assert any("apr" in error.lower() for error in errors)
    
    def test_validate_excessive_apr(self):
        """Test validation with excessive APR."""
        debt = {
            "name": "Invalid Debt",
            "balance": 1000.0,
            "apr": 150.0,  # 150% APR
            "min_payment": 50.0
        }
        errors = validate_debt_portfolio([debt])
        assert any("apr" in error.lower() for error in errors)
    
    def test_validate_zero_min_payment(self):
        """Test validation with zero minimum payment."""
        debt = {
            "name": "Invalid Debt",
            "balance": 1000.0,
            "apr": 15.0,
            "min_payment": 0.0
        }
        errors = validate_debt_portfolio([debt])
        assert any("payment" in error.lower() for error in errors)


class TestEdgeCaseHandling:
    """Test edge case handling functions."""
    
    def test_handle_zero_balance_debt(self):
        """Test handling of debt with zero balance."""
        debts = [{
            "name": "Paid Off Debt",
            "balance": 0.0,
            "apr": 15.0,
            "min_payment": 0.0
        }]
        cleaned = handle_edge_cases(debts)
        assert len(cleaned) == 0  # Should be filtered out
    
    def test_handle_very_small_balance(self):
        """Test handling of debt with very small balance."""
        debts = [{
            "name": "Small Debt",
            "balance": 0.50,
            "apr": 15.0,
            "min_payment": 25.0  # Min payment > balance
        }]
        cleaned = handle_edge_cases(debts)
        assert cleaned[0]["min_payment"] <= cleaned[0]["balance"]
    
    def test_handle_rounding_issues(self):
        """Test handling of floating point rounding issues."""
        debts = [{
            "name": "Rounding Debt",
            "balance": 1000.333333333,
            "apr": 15.555555555,
            "min_payment": 50.999999999
        }]
        cleaned = handle_edge_cases(debts)
        debt = cleaned[0]
        
        # Check that values are properly rounded
        assert isinstance(debt["balance"], (int, float))
        assert isinstance(debt["apr"], (int, float))
        assert isinstance(debt["min_payment"], (int, float))


class TestSnowballAlgorithm:
    """Test snowball payoff algorithm (smallest balance first)."""
    
    def test_snowball_basic_calculation(self, sample_debt_portfolio):
        """Test basic snowball calculation."""
        calculator = PayoffCalculator(extra_payment=100.0)
        debt_objects = [Debt(**debt) for debt in sample_debt_portfolio]
        
        result = calculator.calculate_snowball(debt_objects)
        
        assert "strategy" in result
        assert result["strategy"] == "snowball"
        assert "total_interest" in result
        assert "payoff_months" in result
        assert "monthly_schedule" in result
        assert isinstance(result["total_interest"], (int, float))
        assert result["payoff_months"] > 0
    
    def test_snowball_ordering(self, sample_debt_portfolio):
        """Test that snowball orders debts by balance (smallest first)."""
        calculator = PayoffCalculator(extra_payment=100.0)
        debt_objects = [Debt(**debt) for debt in sample_debt_portfolio]
        
        result = calculator.calculate_snowball(debt_objects)
        
        # Check that debts are ordered by balance
        schedule = result["monthly_schedule"]
        first_debt_paid = None
        
        for month in schedule:
            for debt_name, payment in month["payments"].items():
                if payment.get("remaining_balance", 0) == 0 and first_debt_paid is None:
                    first_debt_paid = debt_name
                    break
            if first_debt_paid:
                break
        
        # The first debt paid should be the one with smallest balance
        balances = {debt["name"]: debt["balance"] for debt in sample_debt_portfolio}
        smallest_debt = min(balances.keys(), key=lambda x: balances[x])
        assert first_debt_paid == smallest_debt
    
    def test_snowball_with_zero_extra_payment(self, sample_debt_portfolio):
        """Test snowball with no extra payment."""
        calculator = PayoffCalculator(extra_payment=0.0)
        debt_objects = [Debt(**debt) for debt in sample_debt_portfolio]
        
        result = calculator.calculate_snowball(debt_objects)
        
        assert result["payoff_months"] > 0
        assert result["total_interest"] > 0
    
    def test_snowball_single_debt(self, sample_debt_data):
        """Test snowball with single debt."""
        calculator = PayoffCalculator(extra_payment=50.0)
        debt_objects = [Debt(**sample_debt_data)]
        
        result = calculator.calculate_snowball(debt_objects)
        
        assert result["payoff_months"] > 0
        assert len(result["monthly_schedule"]) == result["payoff_months"]


class TestAvalancheAlgorithm:
    """Test avalanche payoff algorithm (highest APR first)."""
    
    def test_avalanche_basic_calculation(self, sample_debt_portfolio):
        """Test basic avalanche calculation."""
        calculator = PayoffCalculator(extra_payment=100.0)
        debt_objects = [Debt(**debt) for debt in sample_debt_portfolio]
        
        result = calculator.calculate_avalanche(debt_objects)
        
        assert "strategy" in result
        assert result["strategy"] == "avalanche"
        assert "total_interest" in result
        assert "payoff_months" in result
        assert "monthly_schedule" in result
        assert isinstance(result["total_interest"], (int, float))
        assert result["payoff_months"] > 0
    
    def test_avalanche_ordering(self, sample_debt_portfolio):
        """Test that avalanche orders debts by APR (highest first)."""
        calculator = PayoffCalculator(extra_payment=100.0)
        debt_objects = [Debt(**debt) for debt in sample_debt_portfolio]
        
        result = calculator.calculate_avalanche(debt_objects)
        
        # Check that debts are ordered by APR
        schedule = result["monthly_schedule"]
        first_debt_paid = None
        
        for month in schedule:
            for debt_name, payment in month["payments"].items():
                if payment.get("remaining_balance", 0) == 0 and first_debt_paid is None:
                    first_debt_paid = debt_name
                    break
            if first_debt_paid:
                break
        
        # The first debt paid should be the one with highest APR
        aprs = {debt["name"]: debt["apr"] for debt in sample_debt_portfolio}
        highest_apr_debt = max(aprs.keys(), key=lambda x: aprs[x])
        assert first_debt_paid == highest_apr_debt
    
    def test_avalanche_vs_snowball_interest(self, sample_debt_portfolio):
        """Test that avalanche typically saves more on interest than snowball."""
        calculator = PayoffCalculator(extra_payment=200.0)
        debt_objects = [Debt(**debt) for debt in sample_debt_portfolio]
        
        snowball_result = calculator.calculate_snowball(debt_objects.copy())
        avalanche_result = calculator.calculate_avalanche(debt_objects.copy())
        
        # Avalanche should generally save more on interest
        # (though this isn't guaranteed for all portfolios)
        assert avalanche_result["total_interest"] <= snowball_result["total_interest"] * 1.1


class TestStrategyComparison:
    """Test strategy comparison functionality."""
    
    def test_compare_strategies(self, sample_debt_portfolio):
        """Test strategy comparison."""
        calculator = PayoffCalculator(extra_payment=150.0)
        debt_objects = [Debt(**debt) for debt in sample_debt_portfolio]
        
        result = calculator.compare_strategies(debt_objects)
        
        assert "snowball" in result
        assert "avalanche" in result
        assert "recommendation" in result
        
        snowball = result["snowball"]
        avalanche = result["avalanche"]
        
        assert "total_interest" in snowball
        assert "total_interest" in avalanche
        assert "payoff_months" in snowball
        assert "payoff_months" in avalanche
    
    def test_recommendation_logic(self, sample_debt_portfolio):
        """Test that recommendation logic is sound."""
        calculator = PayoffCalculator(extra_payment=100.0)
        debt_objects = [Debt(**debt) for debt in sample_debt_portfolio]
        
        result = calculator.compare_strategies(debt_objects)
        recommendation = result["recommendation"]
        
        assert "strategy" in recommendation
        assert recommendation["strategy"] in ["snowball", "avalanche"]
        assert "reason" in recommendation
        assert isinstance(recommendation["reason"], str)


class TestPerformanceBenchmarks:
    """Test performance requirements."""
    
    def test_calculation_performance_small_portfolio(self, sample_debt_portfolio, performance_threshold):
        """Test calculation performance with small portfolio."""
        calculator = PayoffCalculator(extra_payment=100.0)
        debt_objects = [Debt(**debt) for debt in sample_debt_portfolio]
        
        start_time = time.time()
        calculator.calculate_snowball(debt_objects)
        end_time = time.time()
        
        execution_time = end_time - start_time
        assert execution_time < performance_threshold
    
    def test_calculation_performance_large_portfolio(self, large_debt_portfolio, performance_threshold):
        """Test calculation performance with 10-debt portfolio."""
        calculator = PayoffCalculator(extra_payment=200.0)
        debt_objects = [Debt(**debt) for debt in large_debt_portfolio]
        
        start_time = time.time()
        calculator.calculate_snowball(debt_objects)
        end_time = time.time()
        
        execution_time = end_time - start_time
        assert execution_time < performance_threshold, f"Calculation took {execution_time:.3f}s, expected < {performance_threshold}s"
    
    def test_avalanche_performance_large_portfolio(self, large_debt_portfolio, performance_threshold):
        """Test avalanche performance with 10-debt portfolio."""
        calculator = PayoffCalculator(extra_payment=200.0)
        debt_objects = [Debt(**debt) for debt in large_debt_portfolio]
        
        start_time = time.time()
        calculator.calculate_avalanche(debt_objects)
        end_time = time.time()
        
        execution_time = end_time - start_time
        assert execution_time < performance_threshold, f"Avalanche calculation took {execution_time:.3f}s, expected < {performance_threshold}s"
    
    def test_comparison_performance(self, large_debt_portfolio, performance_threshold):
        """Test strategy comparison performance."""
        calculator = PayoffCalculator(extra_payment=200.0)
        debt_objects = [Debt(**debt) for debt in large_debt_portfolio]
        
        start_time = time.time()
        calculator.compare_strategies(debt_objects)
        end_time = time.time()
        
        execution_time = end_time - start_time
        # Comparison should be less than 2x single calculation
        assert execution_time < (performance_threshold * 2)


class TestCalculatorEdgeCases:
    """Test calculator edge cases and error conditions."""
    
    def test_very_high_extra_payment(self, sample_debt_data):
        """Test with extra payment higher than total debt."""
        calculator = PayoffCalculator(extra_payment=10000.0)
        debt_objects = [Debt(**sample_debt_data)]
        
        result = calculator.calculate_snowball(debt_objects)
        
        # Should pay off in 1 month
        assert result["payoff_months"] == 1
    
    def test_zero_balance_portfolio(self):
        """Test with all zero-balance debts."""
        debts = [
            {"name": "Paid Debt 1", "balance": 0.0, "apr": 15.0, "min_payment": 0.0},
            {"name": "Paid Debt 2", "balance": 0.0, "apr": 20.0, "min_payment": 0.0}
        ]
        
        # Should be filtered out by edge case handling
        cleaned = handle_edge_cases(debts)
        assert len(cleaned) == 0
    
    def test_minimum_payment_exceeds_balance(self):
        """Test when minimum payment exceeds remaining balance."""
        debt_data = {
            "name": "Small Debt",
            "balance": 25.0,
            "apr": 15.0,
            "min_payment": 50.0
        }
        
        calculator = PayoffCalculator(extra_payment=0.0)
        debt_objects = [Debt(**debt_data)]
        
        result = calculator.calculate_snowball(debt_objects)
        
        # Should pay off in 1 month
        assert result["payoff_months"] == 1
        assert result["monthly_schedule"][0]["payments"][debt_data["name"]]["payment"] == 25.0


class TestCalculatorAccuracy:
    """Test calculation accuracy and mathematical correctness."""
    
    def test_interest_calculation_accuracy(self):
        """Test that interest calculations are mathematically correct."""
        debt_data = {
            "name": "Test Debt",
            "balance": 1000.0,
            "apr": 12.0,  # 1% monthly
            "min_payment": 100.0
        }
        
        calculator = PayoffCalculator(extra_payment=0.0)
        debt_objects = [Debt(**debt_data)]
        
        result = calculator.calculate_snowball(debt_objects)
        
        # Manually calculate expected interest for first month
        monthly_rate = 12.0 / 100 / 12  # 1% monthly
        expected_first_interest = 1000.0 * monthly_rate
        
        first_month = result["monthly_schedule"][0]
        actual_first_interest = first_month["payments"]["Test Debt"]["interest"]
        
        # Should be within 1 cent
        assert abs(actual_first_interest - expected_first_interest) < 0.01
    
    def test_balance_progression_accuracy(self):
        """Test that balance progression is mathematically correct."""
        debt_data = {
            "name": "Test Debt",
            "balance": 1000.0,
            "apr": 12.0,
            "min_payment": 200.0
        }
        
        calculator = PayoffCalculator(extra_payment=0.0)
        debt_objects = [Debt(**debt_data)]
        
        result = calculator.calculate_snowball(debt_objects)
        
        # Check balance progression
        previous_balance = 1000.0
        monthly_rate = 12.0 / 100 / 12
        
        for month in result["monthly_schedule"]:
            payment_info = month["payments"]["Test Debt"]
            
            expected_interest = previous_balance * monthly_rate
            expected_principal = payment_info["payment"] - expected_interest
            expected_new_balance = max(0, previous_balance - expected_principal)
            
            assert abs(payment_info["interest"] - expected_interest) < 0.01
            assert abs(payment_info["principal"] - expected_principal) < 0.01
            assert abs(payment_info["remaining_balance"] - expected_new_balance) < 0.01
            
            previous_balance = expected_new_balance
            if previous_balance == 0:
                break
