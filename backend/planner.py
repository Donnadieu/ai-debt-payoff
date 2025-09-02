"""Debt payoff calculation algorithms (Snowball and Avalanche strategies)."""

from typing import List, Dict, Any
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
import copy

from models import Debt


class PayoffCalculator:
    """Core debt payoff calculation engine."""
    
    def __init__(self, extra_payment: float = 0.0):
        """Initialize calculator with optional extra payment amount."""
        self.extra_payment = Decimal(str(extra_payment))
    
    def calculate_snowball(self, debts: List[Debt]) -> Dict[str, Any]:
        """
        Calculate debt payoff using Snowball method (smallest balance first).
        
        Args:
            debts: List of Debt objects
            
        Returns:
            Dict containing payoff schedule, total interest, and timeline
        """
        # Sort debts by balance (smallest first)
        sorted_debts = sorted(debts, key=lambda d: d.balance)
        return self._calculate_payoff_schedule(sorted_debts, "snowball")
    
    def calculate_avalanche(self, debts: List[Debt]) -> Dict[str, Any]:
        """
        Calculate debt payoff using Avalanche method (highest APR first).
        
        Args:
            debts: List of Debt objects
            
        Returns:
            Dict containing payoff schedule, total interest, and timeline
        """
        # Sort debts by interest rate (highest first)
        sorted_debts = sorted(debts, key=lambda d: d.interest_rate, reverse=True)
        return self._calculate_payoff_schedule(sorted_debts, "avalanche")
    
    def _calculate_payoff_schedule(self, sorted_debts: List[Debt], strategy: str) -> Dict[str, Any]:
        """
        Calculate complete payoff schedule for given debt order.
        
        Args:
            sorted_debts: Debts in payoff priority order
            strategy: Strategy name for tracking
            
        Returns:
            Complete payoff schedule with monthly breakdown
        """
        # Deep copy to avoid modifying original debts
        working_debts = []
        for debt in sorted_debts:
            working_debts.append({
                'id': debt.id,
                'name': debt.name,
                'balance': Decimal(str(debt.balance)),
                'interest_rate': Decimal(str(debt.interest_rate)),
                'minimum_payment': Decimal(str(debt.minimum_payment)),
                'due_date': debt.due_date
            })
        
        # Calculate total minimum payments
        total_minimum = sum(debt['minimum_payment'] for debt in working_debts)
        total_available = total_minimum + self.extra_payment
        
        schedule = []
        month = 1
        current_date = datetime.now().replace(day=1)
        total_interest_paid = Decimal('0')
        
        while any(debt['balance'] > 0 for debt in working_debts):
            month_data = {
                'month': month,
                'date': current_date.strftime('%Y-%m'),
                'payments': [],
                'total_payment': Decimal('0'),
                'total_interest': Decimal('0'),
                'remaining_balances': {}
            }
            
            # Calculate interest for all debts
            for debt in working_debts:
                if debt['balance'] > 0:
                    monthly_interest_rate = debt['interest_rate'] / Decimal('100') / Decimal('12')
                    interest_charge = debt['balance'] * monthly_interest_rate
                    debt['balance'] += interest_charge
                    month_data['total_interest'] += interest_charge
                    total_interest_paid += interest_charge
            
            # Allocate payments
            remaining_payment = total_available
            
            # Pay minimums on all debts first
            for debt in working_debts:
                if debt['balance'] > 0:
                    payment = min(debt['minimum_payment'], debt['balance'])
                    debt['balance'] -= payment
                    remaining_payment -= payment
                    
                    month_data['payments'].append({
                        'debt_id': debt['id'],
                        'debt_name': debt['name'],
                        'payment': float(payment),
                        'interest_portion': float(debt['balance'] * debt['interest_rate'] / Decimal('100') / Decimal('12')) if debt['balance'] > 0 else 0,
                        'principal_portion': float(payment)
                    })
                    month_data['total_payment'] += payment
            
            # Apply extra payment to priority debt
            if remaining_payment > 0:
                for debt in working_debts:
                    if debt['balance'] > 0:
                        extra_payment = min(remaining_payment, debt['balance'])
                        debt['balance'] -= extra_payment
                        
                        # Update the payment record
                        for payment_record in month_data['payments']:
                            if payment_record['debt_id'] == debt['id']:
                                payment_record['payment'] += float(extra_payment)
                                payment_record['principal_portion'] += float(extra_payment)
                                break
                        
                        month_data['total_payment'] += extra_payment
                        break
            
            # Record remaining balances
            for debt in working_debts:
                month_data['remaining_balances'][debt['name']] = float(debt['balance'])
            
            schedule.append(month_data)
            month += 1
            current_date += timedelta(days=32)
            current_date = current_date.replace(day=1)
            
            # Safety break to prevent infinite loops
            if month > 600:  # 50 years max
                break
        
        # Calculate summary statistics
        total_payments = sum(month['total_payment'] for month in schedule)
        payoff_timeline = {}
        
        for debt in sorted_debts:
            for month_idx, month_data in enumerate(schedule):
                if month_data['remaining_balances'][debt.name] == 0:
                    payoff_timeline[debt.name] = {
                        'month': month_idx + 1,
                        'date': month_data['date']
                    }
                    break
        
        return {
            'strategy': strategy,
            'total_months': len(schedule),
            'total_payments': float(total_payments),
            'total_interest': float(total_interest_paid),
            'payoff_timeline': payoff_timeline,
            'monthly_schedule': schedule,
            'summary': {
                'total_debt': float(sum(debt.balance for debt in sorted_debts)),
                'total_interest_saved': 0,  # Will be calculated by comparing strategies
                'completion_date': schedule[-1]['date'] if schedule else None
            }
        }
    
    def compare_strategies(self, debts: List[Debt]) -> Dict[str, Any]:
        """
        Compare Snowball vs Avalanche strategies.
        
        Args:
            debts: List of Debt objects
            
        Returns:
            Comparison of both strategies with recommendations
        """
        snowball_result = self.calculate_snowball(debts)
        avalanche_result = self.calculate_avalanche(debts)
        
        # Calculate interest savings
        interest_difference = snowball_result['total_interest'] - avalanche_result['total_interest']
        time_difference = snowball_result['total_months'] - avalanche_result['total_months']
        
        return {
            'snowball': snowball_result,
            'avalanche': avalanche_result,
            'comparison': {
                'avalanche_saves_interest': float(interest_difference),
                'avalanche_saves_months': time_difference,
                'recommended_strategy': 'avalanche' if interest_difference > 100 else 'snowball',
                'recommendation_reason': self._get_recommendation_reason(interest_difference, time_difference)
            }
        }
    
    def _get_recommendation_reason(self, interest_diff: float, time_diff: int) -> str:
        """Generate recommendation reasoning based on savings."""
        if interest_diff > 500:
            return f"Avalanche saves ${interest_diff:.2f} in interest over {time_diff} months"
        elif interest_diff > 100:
            return f"Avalanche saves ${interest_diff:.2f} in interest with similar timeline"
        elif time_diff < -3:
            return f"Snowball completes {abs(time_diff)} months faster for psychological wins"
        else:
            return "Both strategies are similar; choose based on personal preference"


def validate_debt_portfolio(debts: List[Dict[str, Any]]) -> List[str]:
    """
    Validate debt portfolio for calculation requirements.
    
    Args:
        debts: List of debt dictionaries
        
    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []
    
    if not debts:
        errors.append("At least one debt is required")
        return errors


class PerformanceOptimizer:
    """Performance optimization utilities for debt calculations."""
    
    @staticmethod
    def optimize_calculation_precision(value: Decimal) -> Decimal:
        """Optimize decimal precision for performance while maintaining accuracy."""
        return value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    @staticmethod
    def batch_interest_calculation(debts: List[Dict[str, Any]]) -> List[Decimal]:
        """Batch calculate monthly interest for all debts for better performance."""
        monthly_rates = []
        for debt in debts:
            if debt['balance'] > 0:
                monthly_rate = debt['interest_rate'] / Decimal('100') / Decimal('12')
                monthly_rates.append(debt['balance'] * monthly_rate)
            else:
                monthly_rates.append(Decimal('0'))
        return monthly_rates
    
    @staticmethod
    def validate_performance_requirements(debts: List[Debt], max_time_ms: int = 500) -> bool:
        """
        Validate that calculation meets performance requirements.
        
        Args:
            debts: List of debts to test
            max_time_ms: Maximum allowed calculation time in milliseconds
            
        Returns:
            True if performance requirements met
        """
        import time
        
        if len(debts) > 10:
            return False
        
        calculator = PayoffCalculator()
        start_time = time.time()
        
        # Test both algorithms
        calculator.calculate_snowball(debts)
        calculator.calculate_avalanche(debts)
        
        end_time = time.time()
        calculation_time_ms = (end_time - start_time) * 1000
        
        return calculation_time_ms < max_time_ms


def handle_edge_cases(debts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Handle edge cases in debt data before calculation.
    
    Args:
        debts: Raw debt data
        
    Returns:
        Cleaned debt data ready for calculation
    """
    cleaned_debts = []
    
    for debt in debts:
        # Skip zero balance debts
        if debt.get('balance', 0) <= 0:
            continue
        
        # Ensure minimum payment doesn't exceed balance
        balance = Decimal(str(debt['balance']))
        min_payment = Decimal(str(debt['minimum_payment']))
        
        if min_payment > balance:
            debt['minimum_payment'] = float(balance)
        
        # Ensure interest rate is reasonable
        if debt.get('interest_rate', 0) > 100:
            debt['interest_rate'] = 100.0
        elif debt.get('interest_rate', 0) < 0:
            debt['interest_rate'] = 0.0
        
        # Ensure due date is valid
        if debt.get('due_date', 1) < 1 or debt.get('due_date', 1) > 31:
            debt['due_date'] = 1
        
        cleaned_debts.append(debt)
    
    return cleaned_debts


class PerformanceOptimizer:
    """Performance optimization utilities for debt calculations."""
    
    @staticmethod
    def optimize_calculation_precision(value: Decimal) -> Decimal:
        """Optimize decimal precision for performance while maintaining accuracy."""
        return value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    @staticmethod
    def batch_interest_calculation(debts: List[Dict[str, Any]]) -> List[Decimal]:
        """Batch calculate monthly interest for all debts for better performance."""
        monthly_rates = []
        for debt in debts:
            if debt['balance'] > 0:
                monthly_rate = debt['interest_rate'] / Decimal('100') / Decimal('12')
                monthly_rates.append(debt['balance'] * monthly_rate)
            else:
                monthly_rates.append(Decimal('0'))
        return monthly_rates
    
    @staticmethod
    def validate_performance_requirements(debts: List[Debt], max_time_ms: int = 500) -> bool:
        """
        Validate that calculation meets performance requirements.
        
        Args:
            debts: List of debts to test
            max_time_ms: Maximum allowed calculation time in milliseconds
            
        Returns:
            True if performance requirements met
        """
        import time
        
        if len(debts) > 10:
            return False
        
        calculator = PayoffCalculator()
        start_time = time.time()
        
        # Test both algorithms
        calculator.calculate_snowball(debts)
        calculator.calculate_avalanche(debts)
        
        end_time = time.time()
        calculation_time_ms = (end_time - start_time) * 1000
        
        return calculation_time_ms < max_time_ms


def handle_edge_cases(debts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Handle edge cases in debt data before calculation.
    
    Args:
        debts: Raw debt data
        
    Returns:
        Cleaned debt data ready for calculation
    """
    cleaned_debts = []
    
    for debt in debts:
        # Skip zero balance debts
        if debt.get('balance', 0) <= 0:
            continue
        
        # Ensure minimum payment doesn't exceed balance
        balance = Decimal(str(debt['balance']))
        min_payment = Decimal(str(debt['minimum_payment']))
        
        if min_payment > balance:
            debt['minimum_payment'] = float(balance)
        
        # Ensure interest rate is reasonable
        if debt.get('interest_rate', 0) > 100:
            debt['interest_rate'] = 100.0
        elif debt.get('interest_rate', 0) < 0:
            debt['interest_rate'] = 0.0
        
        # Ensure due date is valid
        if debt.get('due_date', 1) < 1 or debt.get('due_date', 1) > 31:
            debt['due_date'] = 1
        
        cleaned_debts.append(debt)
    
    return cleaned_debts
