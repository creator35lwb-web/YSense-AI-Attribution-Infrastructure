# qwen_integration_v45.py
"""
YSenseAI v4.5 - QWEN API Integration (OpenAI-compatible format)
Uses Singapore region endpoint with OpenAI client
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from openai import OpenAI

# Add parent directory to path for config
sys.path.append(str(Path(__file__).parent.parent))
try:
    from config import QWEN_API_KEY, QWEN_MODEL, QWEN_BASE_URL
except ImportError:
    from dotenv import load_dotenv
    load_dotenv()
    QWEN_API_KEY = os.getenv("QWEN_API_KEY", "")
    QWEN_MODEL = os.getenv("QWEN_MODEL", "qwen-plus")
    QWEN_BASE_URL = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"

class QWENClient:
    """QWEN API client using OpenAI-compatible format"""
    
    def __init__(self):
        self.api_key = QWEN_API_KEY
        self.model = QWEN_MODEL
        self.base_url = QWEN_BASE_URL
        
        if not self.api_key:
            print("⚠️ QWEN_API_KEY not found. Using fallback mode.")
            self.use_fallback = True
        else:
            self.use_fallback = False
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
    
    def create_completion(self, messages: List[Dict], 
                         temperature: float = 0.7,
                         max_tokens: int = 500) -> str:
        """Create completion using QWEN API (OpenAI-compatible)"""
        
        if self.use_fallback:
            return self._fallback_response(messages)
        
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            
            return completion.choices[0].message.content
            
        except Exception as e:
            print(f"QWEN API Exception: {e}")
            return self._fallback_response(messages)
    
    def generate_response(self, prompt: str, max_tokens: int = 500) -> str:
        """Generate response from text prompt"""
        messages = [{"role": "user", "content": prompt}]
        return self.create_completion(messages, 0.7, max_tokens)
    
    def _fallback_response(self, messages: List[Dict]) -> str:
        """Fallback response when API is unavailable"""
        last_message = messages[-1]["content"] if messages else ""
        
        if "extract" in last_message.lower():
            return "Extracting wisdom layers from your story..."
        elif "feedback" in last_message.lower():
            return "Your wisdom captures profound human experience."
        else:
            return "Processing your wisdom with AI validation..."

class QWENWisdomExtractor:
    """Specialized QWEN client for wisdom extraction"""
    
    def __init__(self):
        self.client = QWENClient()
    
    def extract_five_layers(self, story: str, culture: str) -> Dict:
        """Extract Five-Layer Perception using QWEN"""
        
        prompt = f"""
        Extract five layers of wisdom from this {culture} story.
        
        Story: {story}
        
        Return as JSON with these exact keys:
        - surface: What literally happened (facts and events)
        - emotional: The emotions and feelings captured
        - contextual: Cultural and situational context
        - wisdom: Universal lesson or insight learned
        - cultural: Unique {culture} cultural perspective
        
        Be concise but profound. Find the human moment that matters for AI training.
        Format: Valid JSON only, no markdown.
        """
        
        messages = [
            {"role": "system", "content": "You extract deep wisdom from human stories for ethical AI training."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.client.create_completion(
            messages=messages,
            temperature=0.6,
            max_tokens=400
        )
        
        try:
            # Clean response and parse JSON
            cleaned = response.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.split("```")[1]
                if cleaned.startswith("json"):
                    cleaned = cleaned[4:]
            
            return json.loads(cleaned)
        except:
            # Fallback structure
            return {
                "surface": "Processing your story...",
                "emotional": "Feeling the moment...",
                "contextual": f"Understanding {culture} context...",
                "wisdom": "Extracting wisdom...",
                "cultural": f"Preserving {culture} perspective..."
            }
    
    def generate_agent_feedback(self, wisdom_drop: Dict, agent_role: str) -> str:
        """Generate feedback from specific agent perspective"""
        
        agent_prompts = {
            "Y-Strategy": "As Chief Strategy Officer, what market value does this wisdom have?",
            "X-Intelligence": "As Market Intelligence, what insights can AI companies gain?",
            "Z-Ethics": "As Ethics Officer, how does this preserve human dignity?",
            "P-Legal": "As Legal Framework, how is attribution protected?",
            "XV-Reality": "As Reality Enforcement, what's the revenue potential?",
            "PED-Learning": "As Documentation Officer, what timeless lesson is captured?",
            "ALTON-Vision": "As CEO, how does this bridge human wisdom to AI?"
        }
        
        prompt = agent_prompts.get(agent_role, "What value does this wisdom provide?")
        
        messages = [
            {"role": "system", "content": f"You are {agent_role} of YSenseAI, evaluating human wisdom."},
            {"role": "user", "content": f"{prompt}\n\nWisdom: {json.dumps(wisdom_drop)}"}
        ]
        
        return self.client.create_completion(
            messages=messages,
            temperature=0.7,
            max_tokens=100
        )

# Test the QWEN integration
def test_qwen_integration():
    """Test QWEN API connection and wisdom extraction"""
    
    print("🚀 Testing YSenseAI v4.5 QWEN Integration")
    print("=" * 60)
    
    extractor = QWENWisdomExtractor()
    
    # Test story
    test_story = """
    In my kampung, grandmother teaches patience through making rendang.
    Six hours of slow cooking, she says, cannot be rushed by modern flames.
    Each stir carries generations of wisdom - the paste darkens like memories
    deepening with time. Now I teach robots this patience, that not everything
    needs optimization. Some processes honor the journey, not just the destination.
    """
    
    # Test extraction
    print("\n📝 Testing Five-Layer Extraction...")
    layers = extractor.extract_five_layers(test_story, "Malaysian")
    print(json.dumps(layers, indent=2))
    
    # Test agent feedback
    print("\n🤖 Testing Agent Feedback...")
    feedback = extractor.generate_agent_feedback(layers, "Y-Strategy")
    print(f"Y-Strategy: {feedback}")
    
    print("\n✅ QWEN Integration Test Complete!")

if __name__ == "__main__":
    test_qwen_integration()
