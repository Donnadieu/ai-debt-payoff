"""Deterministic fallback nudges for failed LLM validations."""
import random
from typing import Dict, Any, List


class FallbackNudges:
    """Provides safe, deterministic nudge content when LLM validation fails."""
    
    def __init__(self):
        # Safe motivational templates without specific numbers
        self.general_nudges = [
            "You're making progress on your debt journey! Every payment brings you closer to financial freedom.",
            
            "Stay focused on your debt payoff goal. Consistency is the key to success.",
            
            "Your dedication to eliminating debt is building better financial habits for your future.",
            
            "Each payment you make is an investment in your financial independence. Keep going!",
            
            "Debt payoff requires discipline, but you're proving you have what it takes.",
            
            "Remember why you started this journey. Financial freedom is worth the effort.",
            
            "You're building momentum with each payment. Trust the process and stay committed.",
            
            "Every dollar toward debt is a step toward your financial goals. You've got this!"
        ]
        
        # Strategy-specific templates
        self.strategy_nudges = {
            'snowball': [
                "Focus on your smallest debt first - those quick wins will fuel your motivation!",
                "The snowball method builds momentum. Each paid-off debt makes the next one easier.",
                "You're building confidence with each debt you eliminate. Keep rolling that snowball!"
            ],
            'avalanche': [
                "Tackling high-interest debt first saves you money in the long run. Smart strategy!",
                "The avalanche method maximizes your savings. Every payment fights expensive interest.",
                "You're being strategic about interest costs. This approach will pay off big time!"
            ]
        }
        
        # Progress-based templates
        self.progress_nudges = {
            'early': [
                "Starting your debt payoff journey takes courage. You've taken the hardest step!",
                "The beginning is always the toughest part. You're building habits that will serve you well.",
                "Every expert was once a beginner. You're on the right path to financial freedom."
            ],
            'middle': [
                "You're in the thick of it now. This is where persistence pays off the most.",
                "The middle stretch tests your resolve. You're proving your commitment to your goals.",
                "Keep pushing through. You've come too far to give up now."
            ],
            'late': [
                "You're so close to the finish line! Don't let up now.",
                "The end is in sight. Your hard work is about to pay off in a big way.",
                "You've shown incredible discipline. Financial freedom is within reach!"
            ]
        }
        
        # Error fallback (when everything else fails)
        self.error_fallback = "Stay committed to your financial goals. Every step forward matters."
    
    def get_fallback_nudge(self, debt_plan: Dict[str, Any]) -> str:
        """
        Get appropriate fallback nudge based on debt plan context.
        
        Args:
            debt_plan: Debt plan data for context
            
        Returns:
            Safe, motivational nudge content
        """
        try:
            # Try strategy-specific nudge first
            strategy = debt_plan.get('strategy', '').lower()
            if strategy in self.strategy_nudges:
                strategy_options = self.strategy_nudges[strategy]
                return random.choice(strategy_options)
            
            # Try progress-based nudge
            progress_stage = self._determine_progress_stage(debt_plan)
            if progress_stage in self.progress_nudges:
                progress_options = self.progress_nudges[progress_stage]
                return random.choice(progress_options)
            
            # Fall back to general nudge
            return random.choice(self.general_nudges)
            
        except Exception:
            # Ultimate fallback
            return self.error_fallback
    
    def get_error_fallback(self) -> str:
        """Get the ultimate error fallback nudge."""
        return self.error_fallback
    
    def _determine_progress_stage(self, debt_plan: Dict[str, Any]) -> str:
        """Determine progress stage based on debt plan data."""
        try:
            total_months = debt_plan.get('total_months', 0)
            if total_months == 0:
                return 'early'
            
            # Rough categorization based on timeline
            if total_months <= 12:
                return 'late'  # Short timeline, probably close to done
            elif total_months <= 36:
                return 'middle'  # Medium timeline
            else:
                return 'early'  # Long timeline, just getting started
                
        except Exception:
            return 'early'  # Safe default
    
    def get_all_templates(self) -> Dict[str, List[str]]:
        """Get all available template categories for testing."""
        return {
            'general': self.general_nudges,
            'snowball': self.strategy_nudges['snowball'],
            'avalanche': self.strategy_nudges['avalanche'],
            'early': self.progress_nudges['early'],
            'middle': self.progress_nudges['middle'],
            'late': self.progress_nudges['late'],
            'error': [self.error_fallback]
        }
    
    def validate_all_templates(self) -> Dict[str, Any]:
        """Validate that all templates are safe (no numbers/amounts)."""
        from ..services.validation import NudgeValidator
        
        validator = NudgeValidator()
        results = []
        
        # Test all template categories
        all_templates = self.get_all_templates()
        
        for category, templates in all_templates.items():
            for template in templates:
                # Use empty debt plan since fallbacks shouldn't depend on specific data
                validation = validator.validate_nudge(template, {})
                results.append({
                    'category': category,
                    'template': template,
                    'is_valid': validation['is_valid'],
                    'errors': validation['errors']
                })
        
        # Summary
        total = len(results)
        valid = sum(1 for r in results if r['is_valid'])
        
        return {
            'total_templates': total,
            'valid_templates': valid,
            'invalid_templates': total - valid,
            'success_rate': (valid / total * 100) if total > 0 else 0,
            'results': results
        }
