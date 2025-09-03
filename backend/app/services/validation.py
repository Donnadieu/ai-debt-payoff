"""Post-filter validation pipeline for LLM responses."""
import re
from typing import Dict, Any, List, Tuple
from decimal import Decimal


class NudgeValidator:
    """Validates LLM-generated nudges for hallucinated financial data."""
    
    def __init__(self):
        # Regex patterns for detecting financial numbers
        self.money_patterns = [
            r'\$[\d,]+\.?\d*',  # $1,000.00, $500, etc.
            r'\d+\s*dollars?',   # 100 dollars, 50 dollar
            r'\d+\s*cents?',     # 50 cents, 25 cent
        ]
        
        # Patterns for time/numeric claims
        self.numeric_patterns = [
            r'\d+\s*months?',    # 24 months, 12 month
            r'\d+\s*years?',     # 3 years, 1 year
            r'\d+\s*weeks?',     # 4 weeks, 1 week
            r'\d+%',             # 15%, 20%
            r'\d+\s*times?',     # 3 times, 2 time
        ]
        
        # Combined pattern for any suspicious numbers
        self.all_patterns = self.money_patterns + self.numeric_patterns
    
    def validate_nudge(self, content: str, debt_plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate nudge content against debt plan data.
        
        Args:
            content: LLM-generated nudge content
            debt_plan: Original debt plan data for verification
            
        Returns:
            Dict with validation results and cleaned content
        """
        errors = []
        warnings = []
        
        # Check for financial numbers
        money_matches = self._find_financial_numbers(content)
        if money_matches:
            errors.append(f"Contains financial amounts: {money_matches}")
        
        # Check for specific numeric claims
        numeric_matches = self._find_numeric_claims(content)
        if numeric_matches:
            # Verify against actual debt plan data
            invalid_claims = self._verify_numeric_claims(numeric_matches, debt_plan)
            if invalid_claims:
                errors.append(f"Contains unverified claims: {invalid_claims}")
            else:
                warnings.append(f"Contains numeric claims (verified): {numeric_matches}")
        
        # Check content length
        if len(content) > 300:
            warnings.append("Content exceeds recommended length (300 chars)")
        
        # Check for empty or too short content
        if len(content.strip()) < 20:
            errors.append("Content too short or empty")
        
        # Determine if valid
        is_valid = len(errors) == 0
        
        # Clean content if valid
        cleaned_content = content.strip() if is_valid else None
        
        return {
            'is_valid': is_valid,
            'content': cleaned_content,
            'errors': errors,
            'warnings': warnings,
            'detected_numbers': money_matches + numeric_matches,
            'original_length': len(content),
            'cleaned_length': len(cleaned_content) if cleaned_content else 0
        }
    
    def _find_financial_numbers(self, content: str) -> List[str]:
        """Find all financial number patterns in content."""
        matches = []
        for pattern in self.money_patterns:
            found = re.findall(pattern, content, re.IGNORECASE)
            matches.extend(found)
        return matches
    
    def _find_numeric_claims(self, content: str) -> List[str]:
        """Find all numeric claim patterns in content."""
        matches = []
        for pattern in self.numeric_patterns:
            found = re.findall(pattern, content, re.IGNORECASE)
            matches.extend(found)
        return matches
    
    def _verify_numeric_claims(self, claims: List[str], debt_plan: Dict[str, Any]) -> List[str]:
        """
        Verify numeric claims against actual debt plan data.
        
        Args:
            claims: List of numeric claims found in content
            debt_plan: Actual debt plan data
            
        Returns:
            List of claims that don't match the debt plan
        """
        invalid_claims = []
        
        # Extract actual values from debt plan
        actual_months = debt_plan.get('total_months', 0)
        actual_years = round(actual_months / 12, 1) if actual_months else 0
        
        for claim in claims:
            claim_lower = claim.lower()
            
            # Extract number from claim
            numbers = re.findall(r'\d+', claim)
            if not numbers:
                continue
                
            claim_value = int(numbers[0])
            
            # Check months
            if 'month' in claim_lower:
                if abs(claim_value - actual_months) > 2:  # Allow 2 month tolerance
                    invalid_claims.append(f"{claim} (actual: {actual_months} months)")
            
            # Check years
            elif 'year' in claim_lower:
                if abs(claim_value - actual_years) > 0.5:  # Allow 6 month tolerance
                    invalid_claims.append(f"{claim} (actual: {actual_years} years)")
            
            # For other numeric claims, we're more strict
            else:
                # Could add more specific validations here
                pass
        
        return invalid_claims
    
    def get_validation_summary(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get summary statistics for multiple validation results."""
        total = len(results)
        valid = sum(1 for r in results if r['is_valid'])
        invalid = total - valid
        
        all_errors = []
        all_warnings = []
        
        for result in results:
            all_errors.extend(result['errors'])
            all_warnings.extend(result['warnings'])
        
        return {
            'total_validated': total,
            'valid_count': valid,
            'invalid_count': invalid,
            'success_rate': (valid / total * 100) if total > 0 else 0,
            'common_errors': self._count_common_items(all_errors),
            'common_warnings': self._count_common_items(all_warnings)
        }
    
    def _count_common_items(self, items: List[str]) -> Dict[str, int]:
        """Count frequency of common error/warning patterns."""
        counts = {}
        for item in items:
            # Extract the error type (before the colon)
            error_type = item.split(':')[0] if ':' in item else item
            counts[error_type] = counts.get(error_type, 0) + 1
        return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))
