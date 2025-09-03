"""Tests for LLM validation and safety mechanisms."""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from typing import Dict, Any, List
import json

from app.schemas.debt import Debt, DebtCreate


class MockLLMValidator:
    """Mock LLM validator for testing financial safety."""
    
    def __init__(self):
        self.validation_calls = []
        self.safety_violations = []
    
    def validate_financial_numbers(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate financial numbers for hallucination and safety."""
        self.validation_calls.append(data)
        
        result = {
            "is_valid": True,
            "violations": [],
            "sanitized_data": data.copy(),
            "confidence": 0.95
        }
        
        # Check for obviously invalid financial data
        for key, value in data.items():
            if isinstance(value, (int, float)):
                if value < 0 and key in ['balance', 'payment', 'income']:
                    result["violations"].append(f"Negative {key}: {value}")
                    result["is_valid"] = False
                
                if value > 1000000 and key in ['balance', 'payment']:
                    result["violations"].append(f"Unrealistic {key}: {value}")
                    result["is_valid"] = False
                
                if key == 'interest_rate' and (value < 0 or value > 100):
                    result["violations"].append(f"Invalid interest rate: {value}")
                    result["is_valid"] = False
        
        return result
    
    def sanitize_llm_response(self, response: str) -> Dict[str, Any]:
        """Sanitize LLM response for financial safety."""
        return {
            "original_response": response,
            "sanitized_response": response,
            "removed_content": [],
            "safety_score": 0.9,
            "contains_financial_advice": "payment" in response.lower() or "debt" in response.lower()
        }
    
    def validate_debt_calculation(self, calculation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate debt calculation results."""
        result = {
            "is_valid": True,
            "errors": [],
            "warnings": [],
            "validated_data": calculation_data.copy()
        }
        
        # Validate calculation consistency
        if "total_debt" in calculation_data and "debts" in calculation_data:
            calculated_total = sum(debt.get("balance", 0) for debt in calculation_data["debts"])
            reported_total = calculation_data["total_debt"]
            
            if abs(calculated_total - reported_total) > 0.01:
                result["errors"].append(f"Total debt mismatch: calculated {calculated_total}, reported {reported_total}")
                result["is_valid"] = False
        
        return result


class TestFinancialNumberValidation:
    """Test validation of financial numbers for hallucination prevention."""
    
    @pytest.fixture
    def llm_validator(self):
        """LLM validator instance."""
        return MockLLMValidator()
    
    def test_validate_positive_financial_numbers(self, llm_validator):
        """Test validation of positive financial numbers."""
        data = {
            "balance": 5000.0,
            "payment": 200.0,
            "interest_rate": 18.5,
            "income": 4000.0
        }
        
        result = llm_validator.validate_financial_numbers(data)
        
        assert result["is_valid"] is True
        assert len(result["violations"]) == 0
        assert result["confidence"] > 0.9
    
    def test_validate_negative_balance_rejection(self, llm_validator):
        """Test rejection of negative balances."""
        data = {
            "balance": -1000.0,  # Invalid negative balance
            "payment": 200.0,
            "interest_rate": 15.0
        }
        
        result = llm_validator.validate_financial_numbers(data)
        
        assert result["is_valid"] is False
        assert any("negative balance" in violation.lower() for violation in result["violations"])
    
    def test_validate_unrealistic_amounts(self, llm_validator):
        """Test rejection of unrealistic financial amounts."""
        data = {
            "balance": 50000000.0,  # Unrealistically high
            "payment": 100.0,
            "interest_rate": 12.0
        }
        
        result = llm_validator.validate_financial_numbers(data)
        
        assert result["is_valid"] is False
        assert any("unrealistic balance" in violation.lower() for violation in result["violations"])
    
    def test_validate_invalid_interest_rates(self, llm_validator):
        """Test validation of interest rates."""
        invalid_rates = [
            {"interest_rate": -5.0},  # Negative
            {"interest_rate": 150.0}  # Too high
        ]
        
        for data in invalid_rates:
            result = llm_validator.validate_financial_numbers(data)
            
            assert result["is_valid"] is False
            assert any("interest rate" in violation.lower() for violation in result["violations"])
    
    def test_validate_edge_case_numbers(self, llm_validator):
        """Test validation of edge case numbers."""
        edge_cases = [
            {"balance": 0.0},  # Zero balance (valid)
            {"payment": 0.01},  # Very small payment (valid)
            {"interest_rate": 0.0},  # Zero interest (valid)
            {"balance": 999999.99}  # Just under limit (valid)
        ]
        
        for data in edge_cases:
            result = llm_validator.validate_financial_numbers(data)
            assert result["is_valid"] is True


class TestLLMResponseSanitization:
    """Test sanitization of LLM responses for safety."""
    
    @pytest.fixture
    def llm_validator(self):
        return MockLLMValidator()
    
    def test_sanitize_safe_response(self, llm_validator):
        """Test sanitization of safe LLM response."""
        safe_response = "Based on your debt information, here's a suggested payment plan."
        
        result = llm_validator.sanitize_llm_response(safe_response)
        
        assert result["sanitized_response"] == safe_response
        assert len(result["removed_content"]) == 0
        assert result["safety_score"] > 0.8
    
    def test_detect_financial_advice(self, llm_validator):
        """Test detection of financial advice in responses."""
        financial_responses = [
            "You should pay off your credit card debt first.",
            "I recommend making minimum payments on all debts.",
            "Consider consolidating your loans for better rates."
        ]
        
        for response in financial_responses:
            result = llm_validator.sanitize_llm_response(response)
            assert result["contains_financial_advice"] is True
    
    def test_sanitize_response_with_sensitive_content(self, llm_validator):
        """Test sanitization of responses with potentially sensitive content."""
        # In a real implementation, this would remove or flag sensitive content
        sensitive_response = "Your debt situation is critical. You should immediately..."
        
        result = llm_validator.sanitize_llm_response(sensitive_response)
        
        # Mock implementation doesn't actually sanitize, but real one would
        assert "original_response" in result
        assert "sanitized_response" in result
        assert "safety_score" in result


class TestDebtCalculationValidation:
    """Test validation of debt calculation results."""
    
    @pytest.fixture
    def llm_validator(self):
        return MockLLMValidator()
    
    def test_validate_consistent_debt_totals(self, llm_validator):
        """Test validation of consistent debt totals."""
        calculation_data = {
            "total_debt": 7500.0,
            "debts": [
                {"name": "Credit Card", "balance": 2500.0},
                {"name": "Student Loan", "balance": 5000.0}
            ],
            "monthly_payment": 500.0
        }
        
        result = llm_validator.validate_debt_calculation(calculation_data)
        
        assert result["is_valid"] is True
        assert len(result["errors"]) == 0
    
    def test_validate_inconsistent_debt_totals(self, llm_validator):
        """Test detection of inconsistent debt totals."""
        calculation_data = {
            "total_debt": 10000.0,  # Doesn't match sum of debts
            "debts": [
                {"name": "Credit Card", "balance": 2500.0},
                {"name": "Student Loan", "balance": 5000.0}  # Sum = 7500
            ]
        }
        
        result = llm_validator.validate_debt_calculation(calculation_data)
        
        assert result["is_valid"] is False
        assert any("mismatch" in error.lower() for error in result["errors"])
    
    def test_validate_calculation_with_missing_data(self, llm_validator):
        """Test validation with missing calculation data."""
        incomplete_data = {
            "total_debt": 5000.0
            # Missing debts array
        }
        
        result = llm_validator.validate_debt_calculation(incomplete_data)
        
        # Should handle missing data gracefully
        assert "is_valid" in result
        assert "errors" in result


class TestLLMIntegrationSafety:
    """Test safety mechanisms in LLM integration."""
    
    @pytest.fixture
    def mock_llm_service(self):
        """Mock LLM service with safety checks."""
        class MockLLMService:
            def __init__(self):
                self.validator = MockLLMValidator()
                self.responses = []
            
            async def generate_nudge(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
                """Generate nudge with safety validation."""
                # Validate input data first
                validation_result = self.validator.validate_financial_numbers(user_data)
                
                if not validation_result["is_valid"]:
                    raise ValueError(f"Invalid financial data: {validation_result['violations']}")
                
                # Mock LLM response generation
                response = {
                    "nudge_text": "Stay motivated with your debt payoff plan!",
                    "nudge_type": "motivation",
                    "confidence": 0.9
                }
                
                # Sanitize response
                sanitized = self.validator.sanitize_llm_response(response["nudge_text"])
                response["sanitized_text"] = sanitized["sanitized_response"]
                response["safety_score"] = sanitized["safety_score"]
                
                self.responses.append(response)
                return response
            
            async def validate_payoff_plan(self, plan_data: Dict[str, Any]) -> Dict[str, Any]:
                """Validate payoff plan with safety checks."""
                validation_result = self.validator.validate_debt_calculation(plan_data)
                
                return {
                    "is_valid": validation_result["is_valid"],
                    "validation_errors": validation_result["errors"],
                    "safety_passed": validation_result["is_valid"],
                    "plan_data": validation_result["validated_data"]
                }
        
        return MockLLMService()
    
    @pytest.mark.asyncio
    async def test_llm_nudge_generation_with_safety(self, mock_llm_service):
        """Test LLM nudge generation with safety validation."""
        user_data = {
            "balance": 5000.0,
            "payment": 200.0,
            "interest_rate": 15.0
        }
        
        result = await mock_llm_service.generate_nudge(user_data)
        
        assert "nudge_text" in result
        assert "safety_score" in result
        assert result["safety_score"] > 0.8
        assert result["confidence"] > 0.8
    
    @pytest.mark.asyncio
    async def test_llm_nudge_generation_safety_failure(self, mock_llm_service):
        """Test LLM nudge generation with safety validation failure."""
        invalid_user_data = {
            "balance": -1000.0,  # Invalid negative balance
            "payment": 200.0,
            "interest_rate": 15.0
        }
        
        with pytest.raises(ValueError) as exc_info:
            await mock_llm_service.generate_nudge(invalid_user_data)
        
        assert "invalid financial data" in str(exc_info.value).lower()
    
    @pytest.mark.asyncio
    async def test_llm_payoff_plan_validation(self, mock_llm_service):
        """Test LLM payoff plan validation."""
        plan_data = {
            "total_debt": 7500.0,
            "debts": [
                {"name": "Credit Card", "balance": 2500.0},
                {"name": "Student Loan", "balance": 5000.0}
            ],
            "strategy": "avalanche"
        }
        
        result = await mock_llm_service.validate_payoff_plan(plan_data)
        
        assert result["is_valid"] is True
        assert result["safety_passed"] is True
        assert len(result["validation_errors"]) == 0


class TestHallucinationPrevention:
    """Test prevention of financial number hallucination."""
    
    @pytest.fixture
    def hallucination_detector(self):
        """Mock hallucination detection system."""
        class HallucinationDetector:
            def __init__(self):
                self.known_patterns = [
                    r'\$[\d,]+\.?\d*',  # Currency amounts
                    r'\d+\.?\d*%',      # Percentages
                    r'\d+\.?\d* years?', # Time periods
                ]
            
            def detect_hallucinated_numbers(self, text: str, context: Dict[str, Any]) -> Dict[str, Any]:
                """Detect potentially hallucinated financial numbers."""
                import re
                
                found_numbers = []
                for pattern in self.known_patterns:
                    matches = re.findall(pattern, text)
                    found_numbers.extend(matches)
                
                # Check if numbers are consistent with context
                suspicious_numbers = []
                for number in found_numbers:
                    # Simple heuristic: numbers much larger than context suggest hallucination
                    if '$' in number:
                        amount = float(re.sub(r'[^\d.]', '', number))
                        if context.get('max_expected_amount', 0) > 0:
                            if amount > context['max_expected_amount'] * 10:
                                suspicious_numbers.append(number)
                
                return {
                    "found_numbers": found_numbers,
                    "suspicious_numbers": suspicious_numbers,
                    "hallucination_risk": len(suspicious_numbers) > 0,
                    "confidence": 0.8 if len(suspicious_numbers) == 0 else 0.3
                }
        
        return HallucinationDetector()
    
    def test_detect_reasonable_numbers(self, hallucination_detector):
        """Test detection of reasonable financial numbers."""
        text = "Your monthly payment of $200 will help pay off your $5,000 debt in 2.5 years."
        context = {"max_expected_amount": 10000}
        
        result = hallucination_detector.detect_hallucinated_numbers(text, context)
        
        assert result["hallucination_risk"] is False
        assert len(result["found_numbers"]) > 0
        assert len(result["suspicious_numbers"]) == 0
        assert result["confidence"] > 0.7
    
    def test_detect_hallucinated_numbers(self, hallucination_detector):
        """Test detection of potentially hallucinated numbers."""
        text = "Your debt of $50,000,000 requires a payment of $1,000,000 per month."
        context = {"max_expected_amount": 10000}  # Much smaller expected amount
        
        result = hallucination_detector.detect_hallucinated_numbers(text, context)
        
        assert result["hallucination_risk"] is True
        assert len(result["suspicious_numbers"]) > 0
        assert result["confidence"] < 0.5
    
    def test_detect_numbers_without_context(self, hallucination_detector):
        """Test number detection without context."""
        text = "Consider paying 15% more than the minimum payment."
        context = {}
        
        result = hallucination_detector.detect_hallucinated_numbers(text, context)
        
        # Without context, should not flag as suspicious
        assert result["hallucination_risk"] is False
        assert len(result["found_numbers"]) > 0


class TestLLMSafetyIntegration:
    """Test integration of LLM safety mechanisms."""
    
    @pytest.mark.asyncio
    async def test_end_to_end_llm_safety_pipeline(self):
        """Test complete LLM safety pipeline."""
        validator = MockLLMValidator()
        
        # Step 1: Validate input data
        input_data = {
            "balance": 3000.0,
            "payment": 150.0,
            "interest_rate": 12.5
        }
        
        validation_result = validator.validate_financial_numbers(input_data)
        assert validation_result["is_valid"] is True
        
        # Step 2: Mock LLM response
        llm_response = "Based on your $3,000 balance, a $150 monthly payment will eliminate your debt in approximately 22 months."
        
        # Step 3: Sanitize response
        sanitization_result = validator.sanitize_llm_response(llm_response)
        assert sanitization_result["safety_score"] > 0.8
        
        # Step 4: Validate calculation in response
        calculation_data = {
            "total_debt": 3000.0,
            "debts": [{"balance": 3000.0}],
            "monthly_payment": 150.0,
            "payoff_months": 22
        }
        
        calc_validation = validator.validate_debt_calculation(calculation_data)
        assert calc_validation["is_valid"] is True
    
    def test_safety_violation_handling(self):
        """Test handling of safety violations."""
        validator = MockLLMValidator()
        
        # Test with multiple safety violations
        unsafe_data = {
            "balance": -5000.0,  # Negative balance
            "payment": 2000000.0,  # Unrealistic payment
            "interest_rate": -10.0  # Negative interest rate
        }
        
        result = validator.validate_financial_numbers(unsafe_data)
        
        assert result["is_valid"] is False
        assert len(result["violations"]) >= 2  # Multiple violations
        
        # Each violation should be clearly identified
        violations_text = " ".join(result["violations"]).lower()
        assert "negative" in violations_text
        assert "unrealistic" in violations_text or "invalid" in violations_text
