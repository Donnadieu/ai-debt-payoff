"""
Slip Detection Logic - Budget feasibility analysis and remediation suggestions.

Implements the core algorithm for detecting when monthly budget is insufficient
for minimum debt payments and provides actionable remediation suggestions.
"""

import math
from typing import List, Dict, Any, Optional
from decimal import Decimal, ROUND_HALF_UP


class SlipDetector:
    """Detects budget slips and provides remediation suggestions."""
    
    def __init__(self):
        self.minimum_suggestion = Decimal('25.00')
        self.suggestion_increment = Decimal('25.00')
    
    def analyze_budget_feasibility(
        self, 
        monthly_budget: Decimal, 
        debts: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Analyze if monthly budget can cover minimum debt payments.
        
        Args:
            monthly_budget: Available monthly budget amount
            debts: List of debt dictionaries with minimum_payment fields
            
        Returns:
            Dictionary containing analysis results and suggestions
        """
        # Handle edge cases
        if monthly_budget <= 0:
            return self._create_zero_budget_response()
        
        if not debts:
            return self._create_no_debts_response(monthly_budget)
        
        # Calculate total minimum payments
        total_minimum_payments = self._calculate_total_minimum_payments(debts)
        
        # Check for slip condition
        if monthly_budget >= total_minimum_payments:
            return self._create_feasible_response(monthly_budget, total_minimum_payments)
        
        # Calculate shortfall and suggestion
        shortfall = total_minimum_payments - monthly_budget
        suggestion_amount = self._calculate_remediation_suggestion(shortfall)
        
        return self._create_slip_response(
            monthly_budget, 
            total_minimum_payments, 
            shortfall, 
            suggestion_amount
        )
    
    def _calculate_total_minimum_payments(self, debts: List[Dict[str, Any]]) -> Decimal:
        """Calculate sum of all minimum payments."""
        total = Decimal('0.00')
        for debt in debts:
            min_payment = debt.get('minimum_payment', 0)
            if isinstance(min_payment, (int, float)):
                min_payment = Decimal(str(min_payment))
            elif isinstance(min_payment, str):
                min_payment = Decimal(min_payment)
            total += min_payment
        return total
    
    def _calculate_remediation_suggestion(self, shortfall: Decimal) -> Decimal:
        """
        Calculate remediation suggestion using the rule:
        max($25, ceil(shortfall/25)*$25)
        """
        if shortfall <= 0:
            return Decimal('0.00')
        
        # Calculate ceil(shortfall/25) * 25
        multiplier = math.ceil(float(shortfall / self.suggestion_increment))
        calculated_amount = Decimal(str(multiplier)) * self.suggestion_increment
        
        # Return max($25, calculated_amount)
        return max(self.minimum_suggestion, calculated_amount)
    
    def _create_feasible_response(
        self, 
        budget: Decimal, 
        total_payments: Decimal
    ) -> Dict[str, Any]:
        """Create response for feasible budget scenario."""
        return {
            'is_feasible': True,
            'has_slip': False,
            'monthly_budget': float(budget),
            'total_minimum_payments': float(total_payments),
            'surplus': float(budget - total_payments),
            'shortfall': 0.0,
            'suggestion_amount': 0.0,
            'suggestion_text': None,
            'message': 'Budget is sufficient for all minimum payments'
        }
    
    def _create_slip_response(
        self, 
        budget: Decimal, 
        total_payments: Decimal, 
        shortfall: Decimal, 
        suggestion: Decimal
    ) -> Dict[str, Any]:
        """Create response for budget slip scenario."""
        return {
            'is_feasible': False,
            'has_slip': True,
            'monthly_budget': float(budget),
            'total_minimum_payments': float(total_payments),
            'surplus': 0.0,
            'shortfall': float(shortfall),
            'suggestion_amount': float(suggestion),
            'suggestion_text': f'Apply ${suggestion:.0f}',
            'message': f'Budget shortfall of ${shortfall:.2f}. Consider applying ${suggestion:.0f} additional monthly budget.'
        }
    
    def _create_zero_budget_response(self) -> Dict[str, Any]:
        """Create response for zero or negative budget."""
        return {
            'is_feasible': False,
            'has_slip': True,
            'monthly_budget': 0.0,
            'total_minimum_payments': 0.0,
            'surplus': 0.0,
            'shortfall': 0.0,
            'suggestion_amount': float(self.minimum_suggestion),
            'suggestion_text': f'Apply ${self.minimum_suggestion:.0f}',
            'message': 'No budget available. Consider establishing a minimum monthly budget.'
        }
    
    def _create_no_debts_response(self, budget: Decimal) -> Dict[str, Any]:
        """Create response for no debts scenario."""
        return {
            'is_feasible': True,
            'has_slip': False,
            'monthly_budget': float(budget),
            'total_minimum_payments': 0.0,
            'surplus': float(budget),
            'shortfall': 0.0,
            'suggestion_amount': 0.0,
            'suggestion_text': None,
            'message': 'No debts to analyze'
        }
