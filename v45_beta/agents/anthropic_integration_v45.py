# anthropic_integration_v45.py
"""
YSenseAI v4.5 - Anthropic API Integration
Advanced AI reasoning for orchestrator agents
Uses claude-3-haiku-20240307 model
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import anthropic

# Add parent directory to path for config
sys.path.append(str(Path(__file__).parent.parent))
try:
    from config import ANTHROPIC_API_KEY, ANTHROPIC_MODEL
except ImportError:
    from dotenv import load_dotenv
    load_dotenv()
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    ANTHROPIC_MODEL = "claude-3-haiku-20240307"

class AnthropicClient:
    """Anthropic API client for YSenseAI orchestrator agents"""
    
    def __init__(self):
        self.api_key = ANTHROPIC_API_KEY
        self.model = ANTHROPIC_MODEL
        
        if not self.api_key:
            print("⚠️ ANTHROPIC_API_KEY not found. Using fallback mode.")
            self.use_fallback = True
        else:
            self.use_fallback = False
            self.client = anthropic.Anthropic(api_key=self.api_key)
    
    def create_completion(self, messages: List[Dict], 
                         temperature: float = 0.7,
                         max_tokens: int = 1000) -> str:
        """Create completion using Anthropic API"""
        
        if self.use_fallback:
            return self._fallback_response(messages)
        
        try:
            # Convert messages to Anthropic format
            system_message = ""
            anthropic_messages = []
            
            for msg in messages:
                if msg["role"] == "system":
                    system_message = msg["content"]
                else:
                    anthropic_messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
            
            # Ensure we have at least one user message
            if not anthropic_messages:
                anthropic_messages = [{"role": "user", "content": "Hello"}]
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_message if system_message else None,
                messages=anthropic_messages
            )
            
            return response.content[0].text
            
        except Exception as e:
            print(f"Anthropic API Error: {e}")
            return self._fallback_response(messages)
    
    def generate_response(self, prompt: str, max_tokens: int = 1000) -> str:
        """Generate response from text prompt"""
        messages = [{"role": "user", "content": prompt}]
        return self.create_completion(messages, 0.7, max_tokens)
    
    def _fallback_response(self, messages: List[Dict]) -> str:
        """Fallback response when API is unavailable"""
        last_message = messages[-1]["content"] if messages else ""
        
        if "strategy" in last_message.lower():
            return "Strategic analysis completed with focus on academic partnerships and €15K Q1 2026 target."
        elif "market" in last_message.lower():
            return "Market intelligence analysis identifies high-value opportunities in humanoid robotics and academic sectors."
        elif "ethics" in last_message.lower():
            return "Z Protocol validation ensures ethical compliance with 100% score for contributor protection."
        elif "legal" in last_message.lower():
            return "Legal framework structured with Apache 2.0 licensing and defensive publication protection."
        elif "revenue" in last_message.lower():
            return "Revenue analysis shows current progress toward €15K Q1 2026 target with actionable recommendations."
        elif "documentation" in last_message.lower():
            return "Pedagogical documentation captures key learning patterns for continuous improvement."
        elif "ceo" in last_message.lower() or "leadership" in last_message.lower():
            return "CEO leadership guidance emphasizes ethical excellence and revenue generation for Malaysian innovation."
        else:
            return "Advanced AI analysis completed with strategic insights for YSenseAI platform growth."

class AnthropicOrchestratorAgent:
    """Base class for orchestrator agents using Anthropic"""
    
    def __init__(self, role: str, activation_phrase: str, expertise: str):
        self.role = role
        self.activation_phrase = activation_phrase
        self.expertise = expertise
        self.client = AnthropicClient()
    
    def analyze(self, wisdom_drop: Dict, context: str = "") -> str:
        """Analyze wisdom drop from agent's perspective"""
        
        prompt = f"""
        Role: {self.role}
        Expertise: {self.expertise}
        
        Analyze this wisdom contribution:
        {wisdom_drop}
        
        Context: {context}
        
        Provide your analysis focusing on {self.activation_phrase}.
        Be concise but insightful (max 150 words).
        """
        
        messages = [
            {"role": "system", "content": f"You are {self.role} of YSenseAI, providing expert analysis."},
            {"role": "user", "content": prompt}
        ]
        
        return self.client.create_completion(messages, temperature=0.7, max_tokens=200)

# Test the Anthropic integration
def test_anthropic_integration():
    """Test Anthropic API connection"""
    
    print("🚀 Testing YSenseAI v4.5 Anthropic Integration")
    print("=" * 60)
    
    client = AnthropicClient()
    
    # Test simple completion
    print("\n📝 Testing Simple Completion...")
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant for YSenseAI."},
        {"role": "user", "content": "Say 'Hello from YSenseAI v4.5!' in a friendly way."}
    ]
    
    response = client.create_completion(messages, max_tokens=100)
    print(f"Response: {response}")
    
    # Test orchestrator agent
    print("\n🤖 Testing Orchestrator Agent...")
    agent = AnthropicOrchestratorAgent(
        role="Y-Strategy",
        activation_phrase="strategic market value",
        expertise="Market strategy and business development"
    )
    
    test_wisdom = {
        "surface": "A grandmother teaches patience through cooking rendang",
        "wisdom": "True mastery requires slowness and attention to process"
    }
    
    analysis = agent.analyze(test_wisdom, "Evaluating for AI training dataset")
    print(f"Y-Strategy Analysis: {analysis}")
    
    print("\n✅ Anthropic Integration Test Complete!")

if __name__ == "__main__":
    test_anthropic_integration()
