"""
Email Generator Module
Generates professional emails with various tones and for different audiences
"""

from typing import Optional, Dict
from src.utils.ai_service import AIServiceFactory, AIResponseValidator


class EmailGenerator:
    """Generate professional emails using AI"""
    
    # Tone templates
    TONE_TEMPLATES = {
        "formal": "Use a formal, professional tone. Be concise and direct.",
        "informal": "Use a casual, friendly tone. Be approachable.",
        "persuasive": "Use a persuasive, convincing tone. Highlight benefits and call to action.",
    }
    
    # Audience templates
    AUDIENCE_TEMPLATES = {
        "client": "This is for an external client. Maintain professionalism and clarity.",
        "manager": "This is for your manager/supervisor. Be respectful and results-focused.",
        "team": "This is for your team members. Be collaborative and supportive.",
    }
    
    def __init__(self, ai_service_name: str = "openai"):
        """Initialize email generator with specified AI service"""
        self.ai_service = AIServiceFactory.create_service(ai_service_name)
        self.validator = AIResponseValidator()
    
    def generate(
        self,
        topic: str,
        tone: str = "formal",
        audience: str = "client",
        context: Optional[str] = None,
        additional_requirements: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Generate a professional email
        
        Args:
            topic: The main topic of the email
            tone: Email tone (formal, informal, persuasive)
            audience: Target audience (client, manager, team)
            context: Additional context or background information
            additional_requirements: Any specific requirements or constraints
            **kwargs: Additional parameters to pass to AI service
        
        Returns:
            Generated email text
        """
        
        # Validate tone and audience
        if tone not in self.TONE_TEMPLATES:
            raise ValueError(f"Invalid tone. Choose from: {list(self.TONE_TEMPLATES.keys())}")
        
        if audience not in self.AUDIENCE_TEMPLATES:
            raise ValueError(f"Invalid audience. Choose from: {list(self.AUDIENCE_TEMPLATES.keys())}")
        
        # Build the prompt
        prompt = self._build_email_prompt(
            topic=topic,
            tone=tone,
            audience=audience,
            context=context,
            additional_requirements=additional_requirements
        )
        
        # Generate email
        response = self.ai_service.generate(prompt, **kwargs)
        
        # Validate and clean response
        if self.validator.validate_response(response):
            return self.validator.clean_response(response)
        else:
            raise Exception("Generated email did not meet validation requirements")
    
    def _build_email_prompt(
        self,
        topic: str,
        tone: str,
        audience: str,
        context: Optional[str] = None,
        additional_requirements: Optional[str] = None
    ) -> str:
        """Build the prompt for email generation"""
        
        tone_instruction = self.TONE_TEMPLATES[tone]
        audience_instruction = self.AUDIENCE_TEMPLATES[audience]
        
        prompt = f"""You are a professional email writing assistant. Generate a professional email based on the following specifications:

Topic: {topic}
Tone: {tone} - {tone_instruction}
Audience: {audience} - {audience_instruction}

{f"Context: {context}" if context else ""}

Requirements:
- Include a clear subject line
- Start with an appropriate greeting
- Keep the body concise and well-structured
- End with a professional sign-off
- Make the email engaging and easy to read

{f"Additional Requirements: {additional_requirements}" if additional_requirements else ""}

Please generate the email now:
"""
        return prompt
    
    def generate_batch(
        self,
        emails: list,
        **kwargs
    ) -> list:
        """
        Generate multiple emails
        
        Args:
            emails: List of email specifications (each should have topic, tone, audience)
            **kwargs: Additional parameters to pass to AI service
        
        Returns:
            List of generated emails
        """
        results = []
        
        for email_spec in emails:
            try:
                generated = self.generate(**email_spec, **kwargs)
                results.append({
                    "status": "success",
                    "email": generated,
                    "spec": email_spec
                })
            except Exception as e:
                results.append({
                    "status": "error",
                    "error": str(e),
                    "spec": email_spec
                })
        
        return results
    
    def get_available_tones(self) -> list:
        """Get list of available email tones"""
        return list(self.TONE_TEMPLATES.keys())
    
    def get_available_audiences(self) -> list:
        """Get list of available audiences"""
        return list(self.AUDIENCE_TEMPLATES.keys())


class EmailTemplateBuilder:
    """Build email templates with placeholders"""
    
    def __init__(self):
        self.templates = {}
    
    def create_template(self, name: str, template: str) -> None:
        """Create a reusable email template"""
        self.templates[name] = template
    
    def get_template(self, name: str) -> Optional[str]:
        """Get a saved template by name"""
        return self.templates.get(name)
    
    def fill_template(self, template_name: str, **placeholders) -> str:
        """Fill template with values"""
        template = self.get_template(template_name)
        if not template:
            raise ValueError(f"Template '{template_name}' not found")
        
        result = template
        for key, value in placeholders.items():
            result = result.replace(f"{{{{{key}}}}}", str(value))
        
        return result
