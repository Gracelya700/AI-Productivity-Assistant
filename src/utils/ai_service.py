"""
AI Service Interface
Handles all interactions with AI platforms (OpenAI, Google Gemini, etc.)
"""

import os
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import json

try:
    import openai
except ImportError:
    openai = None

try:
    import google.generativeai as genai
except ImportError:
    genai = None


class AIServiceInterface(ABC):
    """Abstract base class for AI service implementations"""
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate response from prompt"""
        pass
    
    @abstractmethod
    def validate_credentials(self) -> bool:
        """Validate API credentials"""
        pass


class OpenAIService(AIServiceInterface):
    """OpenAI ChatGPT Service Implementation"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4")
        self.temperature = float(os.getenv("OPENAI_TEMPERATURE", 0.7))
        
        if openai is None:
            raise ImportError("openai package not installed. Run: pip install openai")
        
        openai.api_key = self.api_key
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate response using OpenAI API"""
        try:
            temperature = kwargs.get("temperature", self.temperature)
            max_tokens = kwargs.get("max_tokens", 2000)
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful AI productivity assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    def validate_credentials(self) -> bool:
        """Validate OpenAI credentials"""
        try:
            openai.Model.list()
            return True
        except:
            return False


class GeminiService(AIServiceInterface):
    """Google Gemini Service Implementation"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-pro")
        
        if genai is None:
            raise ImportError("google-generativeai package not installed. Run: pip install google-generativeai")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate response using Google Gemini API"""
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")
    
    def validate_credentials(self) -> bool:
        """Validate Gemini credentials"""
        try:
            self.model.generate_content("Hello")
            return True
        except:
            return False


class AIServiceFactory:
    """Factory for creating AI service instances"""
    
    _services = {
        "openai": OpenAIService,
        "gemini": GeminiService,
    }
    
    @staticmethod
    def create_service(service_name: str = "openai", **kwargs) -> AIServiceInterface:
        """Create and return an AI service instance"""
        service_class = AIServiceFactory._services.get(service_name.lower())
        
        if service_class is None:
            raise ValueError(f"Unknown AI service: {service_name}")
        
        return service_class(**kwargs)
    
    @staticmethod
    def get_available_services() -> list:
        """Get list of available AI services"""
        return list(AIServiceFactory._services.keys())


class AIResponseValidator:
    """Validates and processes AI responses"""
    
    @staticmethod
    def validate_response(response: str, min_length: int = 1, max_length: Optional[int] = None) -> bool:
        """Validate AI response format and length"""
        if not response or len(response.strip()) < min_length:
            return False
        
        if max_length and len(response) > max_length:
            return False
        
        return True
    
    @staticmethod
    def parse_json_response(response: str) -> Dict[str, Any]:
        """Attempt to parse JSON from AI response"""
        try:
            # Try direct parsing first
            return json.loads(response)
        except json.JSONDecodeError:
            # Try to extract JSON from response text
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group())
                except:
                    pass
        
        return None
    
    @staticmethod
    def clean_response(response: str) -> str:
        """Clean and format AI response"""
        # Remove leading/trailing whitespace
        response = response.strip()
        
        # Remove markdown code blocks if present
        import re
        response = re.sub(r'```[\w]*\n?', '', response)
        
        return response
