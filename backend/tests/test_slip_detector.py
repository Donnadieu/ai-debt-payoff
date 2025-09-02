"""
Unit tests for SlipDetector - Core algorithm testing.
"""

import pytest
from decimal import Decimal
from app.services.slip_detector import SlipDetector


class TestSlipDetector:
    """Test suite for SlipDetector class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.detector = SlipDetector()
        
        # Standard test debts
        self.test_debts = [
            {
                'id': 'debt_1',
                'name': 'Credit Card A',
                'minimum_payment': Decimal('150.00'),
                'balance': Decimal('5000.00')
            },
            {
                'id': 'debt_2',
                'name': 'Student Loan',
                'minimum_payment': Decimal('300.00'),
                'balance': Decimal('25000.00')
            }
        ]
    
    def test_feasible_budget_scenario(self):
        """Test scenario where budget covers all minimum payments."""
        budget = Decimal('500.00')  # Total minimums = 450.00
        
        result = self.detector.analyze_budget_feasibility(budget, self.test_debts)
        
        assert result['is_feasible'] is True
        assert result['has_slip'] is False
        assert result['monthly_budget'] == 500.00
        assert result['total_minimum_payments'] == 450.00
        assert result['surplus'] == 50.00
        assert result['shortfall'] == 0.0
        assert result['suggestion_amount'] == 0.0
        assert result['suggestion_text'] is None
        assert 'sufficient' in result['message'].lower()
    
    def test_slip_scenario_basic(self):
        """Test basic slip scenario with shortfall."""
        budget = Decimal('400.00')  # Total minimums = 450.00, shortfall = 50.00
        
        result = self.detector.analyze_budget_feasibility(budget, self.test_debts)
        
        assert result['is_feasible'] is False
        assert result['has_slip'] is True
        assert result['monthly_budget'] == 400.00
        assert result['total_minimum_payments'] == 450.00
        assert result['surplus'] == 0.0
        assert result['shortfall'] == 50.00
        assert result['suggestion_amount'] == 50.00  # ceil(50/25)*25 = 50
        assert result['suggestion_text'] == 'Apply $50'
        assert 'shortfall' in result['message'].lower()
    
    def test_remediation_suggestion_algorithm(self):
        """Test the remediation suggestion calculation rule."""
        test_cases = [
            # (shortfall, expected_suggestion)
            (Decimal('10.00'), Decimal('25.00')),   # max(25, ceil(10/25)*25) = max(25, 25) = 25
            (Decimal('25.00'), Decimal('25.00')),   # max(25, ceil(25/25)*25) = max(25, 25) = 25
            (Decimal('26.00'), Decimal('50.00')),   # max(25, ceil(26/25)*25) = max(25, 50) = 50
            (Decimal('50.00'), Decimal('50.00')),   # max(25, ceil(50/25)*25) = max(25, 50) = 50
            (Decimal('51.00'), Decimal('75.00')),   # max(25, ceil(51/25)*25) = max(25, 75) = 75
            (Decimal('100.00'), Decimal('100.00')), # max(25, ceil(100/25)*25) = max(25, 100) = 100
            (Decimal('125.50'), Decimal('150.00')), # max(25, ceil(125.5/25)*25) = max(25, 150) = 150
        ]
        
        for shortfall, expected in test_cases:
            result = self.detector._calculate_remediation_suggestion(shortfall)
            assert result == expected, f"Shortfall {shortfall} should suggest {expected}, got {result}"
    
    def test_zero_budget_edge_case(self):
        """Test edge case with zero budget."""
        budget = Decimal('0.00')
        
        result = self.detector.analyze_budget_feasibility(budget, self.test_debts)
        
        assert result['is_feasible'] is False
        assert result['has_slip'] is True
        assert result['monthly_budget'] == 0.0
        assert result['suggestion_amount'] == 25.0
        assert result['suggestion_text'] == 'Apply $25'
        assert 'no budget' in result['message'].lower()
    
    def test_negative_budget_edge_case(self):
        """Test edge case with negative budget."""
        budget = Decimal('-100.00')
        
        result = self.detector.analyze_budget_feasibility(budget, self.test_debts)
        
        assert result['is_feasible'] is False
        assert result['has_slip'] is True
        assert result['monthly_budget'] == 0.0
        assert result['suggestion_amount'] == 25.0
    
    def test_no_debts_edge_case(self):
        """Test edge case with no debts."""
        budget = Decimal('1000.00')
        
        result = self.detector.analyze_budget_feasibility(budget, [])
        
        assert result['is_feasible'] is True
        assert result['has_slip'] is False
        assert result['monthly_budget'] == 1000.00
        assert result['total_minimum_payments'] == 0.0
        assert result['surplus'] == 1000.00
        assert result['shortfall'] == 0.0
        assert result['suggestion_amount'] == 0.0
        assert 'no debts' in result['message'].lower()
    
    def test_single_debt_scenarios(self):
        """Test scenarios with single debt."""
        single_debt = [{'minimum_payment': Decimal('200.00'), 'name': 'Single Debt'}]
        
        # Feasible case
        result = self.detector.analyze_budget_feasibility(Decimal('250.00'), single_debt)
        assert result['is_feasible'] is True
        assert result['surplus'] == 50.00
        
        # Slip case
        result = self.detector.analyze_budget_feasibility(Decimal('150.00'), single_debt)
        assert result['is_feasible'] is False
        assert result['shortfall'] == 50.00
        assert result['suggestion_amount'] == 50.00
    
    def test_exact_budget_match(self):
        """Test scenario where budget exactly matches minimum payments."""
        budget = Decimal('450.00')  # Exactly matches total minimums
        
        result = self.detector.analyze_budget_feasibility(budget, self.test_debts)
        
        assert result['is_feasible'] is True
        assert result['has_slip'] is False
        assert result['surplus'] == 0.0
        assert result['shortfall'] == 0.0
    
    def test_large_shortfall_scenario(self):
        """Test scenario with large shortfall."""
        budget = Decimal('100.00')  # Total minimums = 450.00, shortfall = 350.00
        
        result = self.detector.analyze_budget_feasibility(budget, self.test_debts)
        
        assert result['shortfall'] == 350.00
        # ceil(350/25)*25 = ceil(14)*25 = 14*25 = 350
        assert result['suggestion_amount'] == 350.00
        assert result['suggestion_text'] == 'Apply $350'
    
    def test_mixed_debt_types(self):
        """Test with various debt payment amounts."""
        mixed_debts = [
            {'minimum_payment': Decimal('25.00'), 'name': 'Small Debt'},
            {'minimum_payment': Decimal('500.00'), 'name': 'Large Debt'},
            {'minimum_payment': Decimal('75.50'), 'name': 'Odd Amount'},
        ]
        
        budget = Decimal('500.00')  # Total = 600.50, shortfall = 100.50
        result = self.detector.analyze_budget_feasibility(budget, mixed_debts)
        
        assert result['total_minimum_payments'] == 600.50
        assert result['shortfall'] == 100.50
        # ceil(100.5/25)*25 = ceil(4.02)*25 = 5*25 = 125
        assert result['suggestion_amount'] == 125.00
    
    def test_string_and_numeric_inputs(self):
        """Test handling of different input types for minimum payments."""
        mixed_input_debts = [
            {'minimum_payment': '150.00', 'name': 'String Input'},
            {'minimum_payment': 300, 'name': 'Int Input'},
            {'minimum_payment': 75.50, 'name': 'Float Input'},
        ]
        
        budget = Decimal('400.00')
        result = self.detector.analyze_budget_feasibility(budget, mixed_input_debts)
        
        assert result['total_minimum_payments'] == 525.50
        assert result['shortfall'] == 125.50
    
    def test_performance_requirement(self):
        """Test that calculation completes quickly (< 50ms requirement)."""
        import time
        
        # Create larger debt portfolio
        large_debt_portfolio = []
        for i in range(100):
            large_debt_portfolio.append({
                'minimum_payment': Decimal('50.00'),
                'name': f'Debt {i}'
            })
        
        start_time = time.time()
        result = self.detector.analyze_budget_feasibility(Decimal('1000.00'), large_debt_portfolio)
        end_time = time.time()
        
        calculation_time = (end_time - start_time) * 1000  # Convert to milliseconds
        assert calculation_time < 50, f"Calculation took {calculation_time}ms, should be < 50ms"
        assert result['total_minimum_payments'] == 5000.00
