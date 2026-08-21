"""
Test Configuration and Fixtures
"""

import pytest
import os
from dotenv import load_dotenv

# Load test environment variables
load_dotenv(".env.example")

@pytest.fixture(scope="session")
def api_keys():
    """Provide API keys for testing"""
    return {
        "openai": os.getenv("OPENAI_API_KEY", "test-key"),
        "google": os.getenv("GOOGLE_API_KEY", "test-key")
    }

@pytest.fixture
def sample_email_topic():
    """Provide sample email topic"""
    return "Q3 Performance Review Discussion"

@pytest.fixture
def sample_meeting_notes():
    """Provide sample meeting notes"""
    return """
    Date: August 21, 2026
    Attendees: Alice, Bob, Carol, David
    
    Agenda:
    1. Project Status
    2. Budget Review
    3. Team Updates
    
    Discussion:
    - Project is on track for Q4 launch
    - Budget approved for marketing campaign
    - New hire starting next week
    
    Decisions Made:
    - Launch date confirmed: October 1st
    - Marketing budget increased by 10%
    - Onboarding team assigned
    
    Action Items:
    - Alice: Finalize launch plan by end of week
    - Bob: Prepare marketing materials
    - Carol: Set up onboarding schedule
    - David: Review budget allocations
    """

@pytest.fixture
def sample_tasks():
    """Provide sample tasks for planning"""
    return [
        "Complete project proposal",
        "Review team performance reports",
        "Schedule client meeting",
        "Update documentation",
        "Fix critical bugs in production"
    ]

@pytest.fixture
def sample_research_content():
    """Provide sample content for research analysis"""
    return """
    Artificial Intelligence in the Workplace: Benefits and Challenges
    
    Introduction:
    AI is transforming how organizations operate, from automation to decision-making.
    
    Key Benefits:
    1. Increased efficiency and productivity
    2. Cost reduction through automation
    3. Better data-driven decision making
    4. Improved customer experience
    
    Challenges:
    1. Employee displacement concerns
    2. Data privacy and security risks
    3. High implementation costs
    4. Need for workforce retraining
    
    Conclusion:
    Organizations must carefully plan AI adoption to maximize benefits while mitigating risks.
    """

@pytest.fixture(autouse=True)
def reset_environment():
    """Reset environment between tests"""
    yield
    # Cleanup after test
    pass
