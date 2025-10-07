"""
LLM Integration for Dynamic Persona Generator
This shows how to integrate with actual LLM APIs like OpenAI, Anthropic, etc.
"""

import os
import json
from typing import Dict, List, Optional
import requests

class LLMIntegration:
    def __init__(self, provider: str = "openai", api_key: Optional[str] = None):
        self.provider = provider
        self.api_key = api_key or os.getenv(f"{provider.upper()}_API_KEY")
        
        if not self.api_key:
            raise ValueError(f"API key not found. Set {provider.upper()}_API_KEY environment variable")
    
    def generate_persona_response(self, persona_traits: Dict, chat_personality: str, 
                                 message: str, conversation_history: List[Dict] = None) -> str:
        """Generate persona response using LLM"""
        
        if self.provider == "openai":
            return self._openai_response(persona_traits, chat_personality, message, conversation_history)
        elif self.provider == "anthropic":
            return self._anthropic_response(persona_traits, chat_personality, message, conversation_history)
        elif self.provider == "google":
            return self._google_response(persona_traits, chat_personality, message, conversation_history)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def _openai_response(self, persona_traits: Dict, chat_personality: str, 
                        message: str, conversation_history: List[Dict] = None) -> str:
        """Generate response using OpenAI API"""
        
        # Build system prompt
        system_prompt = f"""You are a persona in a market research study. Here are your characteristics:

{json.dumps(persona_traits, indent=2)}

Your personality: {chat_personality}

Respond naturally as this persona would, using casual language and expressing your genuine concerns and interests. Keep responses conversational and authentic to your persona."""

        # Build conversation messages
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history
        if conversation_history:
            for msg in conversation_history[-10:]:  # Keep last 10 messages
                messages.append({
                    "role": "user" if msg["role"] == "user" else "assistant",
                    "content": msg["message"]
                })
        
        # Add current message
        messages.append({"role": "user", "content": message})
        
        # Call OpenAI API
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-3.5-turbo",
                "messages": messages,
                "max_tokens": 150,
                "temperature": 0.8
            },
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            raise Exception(f"OpenAI API error: {response.status_code} - {response.text}")
    
    def _anthropic_response(self, persona_traits: Dict, chat_personality: str, 
                           message: str, conversation_history: List[Dict] = None) -> str:
        """Generate response using Anthropic Claude API"""
        
        # Build prompt
        prompt = f"""You are a persona in a market research study. Here are your characteristics:

{json.dumps(persona_traits, indent=2)}

Your personality: {chat_personality}

Respond naturally as this persona would, using casual language and expressing your genuine concerns and interests. Keep responses conversational and authentic to your persona.

User message: {message}

Response:"""

        # Call Anthropic API
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": self.api_key,
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01"
            },
            json={
                "model": "claude-3-haiku-20240307",
                "max_tokens": 150,
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()["content"][0]["text"]
        else:
            raise Exception(f"Anthropic API error: {response.status_code} - {response.text}")
    
    def _google_response(self, persona_traits: Dict, chat_personality: str, 
                        message: str, conversation_history: List[Dict] = None) -> str:
        """Generate response using Google Gemini API"""
        
        # Build prompt
        prompt = f"""You are a persona in a market research study. Here are your characteristics:

{json.dumps(persona_traits, indent=2)}

Your personality: {chat_personality}

Respond naturally as this persona would, using casual language and expressing your genuine concerns and interests. Keep responses conversational and authentic to your persona.

User message: {message}

Response:"""

        # Call Google Gemini API
        response = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={self.api_key}",
            headers={"Content-Type": "application/json"},
            json={
                "contents": [{
                    "parts": [{"text": prompt}]
                }],
                "generationConfig": {
                    "maxOutputTokens": 150,
                    "temperature": 0.8
                }
            },
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        else:
            raise Exception(f"Google API error: {response.status_code} - {response.text}")

# Example usage
if __name__ == "__main__":
    # Example persona traits
    persona_traits = {
        "age_group": "21 years old",
        "tech_savviness": "Medium",
        "price_sensitivity": "High",
        "brand_awareness": "Low",
        "privacy_consciousness": "Medium",
        "city_tier": "Tier-2",
        "income_level": "Mid",
        "preferred_media": "YouTube",
        "device_count": "3.0 devices",
        "emi_usage_likelihood": "44.4%"
    }
    
    chat_personality = "You are a 21-year-old from a Tier-2 city with mid income. You're moderately tech-savvy and adopt technology when it makes sense. You're very price-conscious and always look for deals and EMI options. Respond naturally as this persona would, using casual language and expressing your genuine concerns and interests."
    
    # Test with different providers (you'll need API keys)
    try:
        # OpenAI
        llm = LLMIntegration("openai")
        response = llm.generate_persona_response(
            persona_traits, 
            chat_personality, 
            "What do you think about Bose headphones?",
            []
        )
        print(f"OpenAI Response: {response}")
    except Exception as e:
        print(f"OpenAI Error: {e}")
    
    try:
        # Anthropic
        llm = LLMIntegration("anthropic")
        response = llm.generate_persona_response(
            persona_traits, 
            chat_personality, 
            "What do you think about Bose headphones?",
            []
        )
        print(f"Anthropic Response: {response}")
    except Exception as e:
        print(f"Anthropic Error: {e}")
