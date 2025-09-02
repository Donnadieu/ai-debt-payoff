"""Mock LLM client with real API integration points."""
import os
import random
from typing import Dict, Any, Optional
from datetime import datetime


class LLMClient:
    """Mock LLM client with configurable responses and real API hooks."""
    
    def __init__(self):
        self.mode = os.getenv('LLM_MODE', 'mock')  # 'mock' or 'openai' or 'anthropic'
        self.api_key = os.getenv('OPENAI_API_KEY') or os.getenv('ANTHROPIC_API_KEY')
        
        # Mock response templates for testing
        self.mock_responses = [
            "You're making great progress on your debt journey! Every payment brings you closer to financial freedom. Stay focused on your goal and remember that consistency is key to success.",
            
            "Your dedication to paying off debt is admirable! Each month you're building better financial habits. Keep up the momentum - you've got this!",
            
            "Debt payoff takes discipline, but you're proving you have what it takes. Every dollar you put toward debt is an investment in your future self. Stay strong!",
            
            # Intentionally problematic responses for validation testing
            "You owe $50000 and should pay $2000 monthly to be debt-free in 25 months!",  # Contains specific numbers
            "Your $1500 payment will save you $5000 in interest over 3 years.",  # Hallucinated calculations
        ]
    
    def generate_nudge(self, prompt: str) -> str:
        """
        Generate nudge content using configured LLM provider.
        
        Args:
            prompt: Formatted prompt with debt context
            
        Returns:
            Generated nudge content
        """
        if self.mode == 'mock':
            return self._mock_generate(prompt)
        elif self.mode == 'openai':
            return self._openai_generate(prompt)
        elif self.mode == 'anthropic':
            return self._anthropic_generate(prompt)
        else:
            raise ValueError(f"Unknown LLM mode: {self.mode}")
    
    def _mock_generate(self, prompt: str) -> str:
        """Generate mock response for testing."""
        # Simulate API delay
        import time
        time.sleep(0.1)
        
        # Return random response (including problematic ones for testing)
        response = random.choice(self.mock_responses)
        
        # Log for debugging
        print(f"🤖 Mock LLM Response: {response[:50]}...")
        
        return response
    
    def _openai_generate(self, prompt: str) -> str:
        """Generate using OpenAI API (production integration point)."""
        if not self.api_key:
            raise ValueError("OpenAI API key not configured")
        
        # TODO: Implement OpenAI integration
        # import openai
        # openai.api_key = self.api_key
        # 
        # response = openai.ChatCompletion.create(
        #     model="gpt-3.5-turbo",
        #     messages=[{"role": "user", "content": prompt}],
        #     max_tokens=200,
        #     temperature=0.7
        # )
        # 
        # return response.choices[0].message.content.strip()
        
        raise NotImplementedError("OpenAI integration not yet implemented")
    
    def _anthropic_generate(self, prompt: str) -> str:
        """Generate using Anthropic API (production integration point)."""
        if not self.api_key:
            raise ValueError("Anthropic API key not configured")
        
        # TODO: Implement Anthropic integration
        # import anthropic
        # 
        # client = anthropic.Anthropic(api_key=self.api_key)
        # 
        # response = client.messages.create(
        #     model="claude-3-haiku-20240307",
        #     max_tokens=200,
        #     messages=[{"role": "user", "content": prompt}]
        # )
        # 
        # return response.content[0].text.strip()
        
        raise NotImplementedError("Anthropic integration not yet implemented")
    
    def health_check(self) -> Dict[str, Any]:
        """Check LLM client health and configuration."""
        return {
            'mode': self.mode,
            'api_key_configured': bool(self.api_key),
            'timestamp': datetime.utcnow().isoformat(),
            'status': 'healthy' if self.mode == 'mock' else 'needs_api_key'
        }
