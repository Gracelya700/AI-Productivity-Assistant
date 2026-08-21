"""
Flask Web Application - Main Server
Serves the AI Productivity Assistant web interface and API endpoints
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import logging
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, 
    static_folder='static',
    static_url_path='/static',
    template_folder='static')

# Enable CORS
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import feature modules
from src.email.generator import EmailGenerator
from src.meeting.summarizer import MeetingSummarizer
from src.tasks.planner import TaskPlanner
from src.research.assistant import ResearchAssistant
from src.chatbot.interface import SmartAssistant
from src.utils.config import get_config

# Initialize AI services
config = get_config()
ai_service_name = config.AI_SERVICE

try:
    email_generator = EmailGenerator(ai_service_name)
    meeting_summarizer = MeetingSummarizer(ai_service_name)
    task_planner = TaskPlanner(ai_service_name)
    research_assistant = ResearchAssistant(ai_service_name)
    smart_assistant = SmartAssistant(ai_service_name)
    logger.info(f"✓ AI services initialized with {ai_service_name}")
except Exception as e:
    logger.warning(f"⚠ AI services initialization failed: {e}")
    logger.info("Running in demo mode with mock responses")


# ==================== ROUTES ====================

@app.route('/')
def index():
    """Serve the main application"""
    return send_from_directory('static', 'index.html')


@app.route('/static/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory('static', path)


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'ai_service': config.AI_SERVICE,
        'environment': config.APP_ENV
    })


# ==================== EMAIL GENERATOR API ====================

@app.route('/api/email/generate', methods=['POST'])
def generate_email():
    """Generate a professional email"""
    try:
        data = request.json
        
        # Validate input
        required_fields = ['topic', 'tone', 'audience']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        topic = data.get('topic')
        tone = data.get('tone')
        audience = data.get('audience')
        context = data.get('context', '')
        
        # Validate tone and audience
        if tone not in ['formal', 'informal', 'persuasive']:
            return jsonify({'error': 'Invalid tone'}), 400
        
        if audience not in ['client', 'manager', 'team']:
            return jsonify({'error': 'Invalid audience'}), 400
        
        # Generate email
        logger.info(f"Generating email: topic={topic}, tone={tone}, audience={audience}")
        
        email = email_generator.generate(
            topic=topic,
            tone=tone,
            audience=audience,
            context=context if context else None
        )
        
        return jsonify({
            'email': email,
            'timestamp': datetime.now().isoformat(),
            'disclaimer': 'AI-generated content may require human review before sending.'
        })
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error generating email: {e}")
        return jsonify({'error': 'Failed to generate email'}), 500


@app.route('/api/email/templates', methods=['GET'])
def get_email_templates():
    """Get available email templates"""
    try:
        return jsonify({
            'tones': email_generator.get_available_tones(),
            'audiences': email_generator.get_available_audiences()
        })
    except Exception as e:
        logger.error(f"Error retrieving email templates: {e}")
        return jsonify({'error': 'Failed to retrieve templates'}), 500


# ==================== MEETING SUMMARIZER API ====================

@app.route('/api/meeting/summarize', methods=['POST'])
def summarize_meeting():
    """Summarize meeting notes"""
    try:
        data = request.json
        
        if 'meeting_notes' not in data:
            return jsonify({'error': 'Missing meeting_notes field'}), 400
        
        meeting_notes = data.get('meeting_notes')
        meeting_title = data.get('meeting_title', '')
        attendees = data.get('attendees', [])
        context = data.get('context', '')
        
        logger.info(f"Summarizing meeting: {meeting_title or 'Untitled'}")
        
        # Summarize meeting
        summary = meeting_summarizer.summarize(
            meeting_notes=meeting_notes,
            meeting_title=meeting_title if meeting_title else None,
            attendees=attendees if attendees else None,
            context=context if context else None
        )
        
        return jsonify({
            'summary': summary,
            'timestamp': datetime.now().isoformat(),
            'disclaimer': 'AI-generated summaries may require verification against original notes.'
        })
    
    except Exception as e:
        logger.error(f"Error summarizing meeting: {e}")
        return jsonify({'error': 'Failed to summarize meeting'}), 500


@app.route('/api/meeting/extract-actions', methods=['POST'])
def extract_action_items():
    """Extract action items from meeting notes"""
    try:
        data = request.json
        
        if 'meeting_notes' not in data:
            return jsonify({'error': 'Missing meeting_notes field'}), 400
        
        meeting_notes = data.get('meeting_notes')
        
        logger.info("Extracting action items from meeting")
        
        actions = meeting_summarizer.extract_action_items(meeting_notes)
        
        return jsonify({
            'action_items': actions,
            'count': len(actions),
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error extracting action items: {e}")
        return jsonify({'error': 'Failed to extract action items'}), 500


# ==================== TASK PLANNER API ====================

@app.route('/api/tasks/plan', methods=['POST'])
def create_task_plan():
    """Create a task plan"""
    try:
        data = request.json
        
        required_fields = ['tasks']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        tasks = data.get('tasks', [])
        time_frame = data.get('time_frame', 'daily')
        working_hours = data.get('working_hours', 8)
        context = data.get('context', '')
        
        if not isinstance(tasks, list) or len(tasks) == 0:
            return jsonify({'error': 'Tasks must be a non-empty list'}), 400
        
        logger.info(f"Planning tasks: {len(tasks)} tasks for {time_frame}")
        
        # Generate plan
        plan = task_planner.generate_plan(
            tasks=tasks,
            time_frame=time_frame,
            working_hours=working_hours,
            context=context if context else None
        )
        
        return jsonify({
            'plan': plan,
            'timestamp': datetime.now().isoformat(),
            'disclaimer': 'AI-generated plans should be adapted to your actual capacity and priorities.'
        })
    
    except Exception as e:
        logger.error(f"Error creating task plan: {e}")
        return jsonify({'error': 'Failed to create task plan'}), 500


@app.route('/api/tasks/prioritize', methods=['POST'])
def prioritize_tasks():
    """Prioritize tasks"""
    try:
        data = request.json
        
        if 'tasks' not in data:
            return jsonify({'error': 'Missing tasks field'}), 400
        
        tasks = data.get('tasks', [])
        criteria = data.get('criteria', '')
        
        logger.info(f"Prioritizing {len(tasks)} tasks")
        
        # Prioritize
        prioritized = task_planner.prioritize_tasks(
            tasks=tasks,
            criteria=criteria if criteria else None
        )
        
        return jsonify({
            'prioritized_tasks': prioritized,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error prioritizing tasks: {e}")
        return jsonify({'error': 'Failed to prioritize tasks'}), 500


# ==================== RESEARCH ASSISTANT API ====================

@app.route('/api/research/analyze', methods=['POST'])
def analyze_content():
    """Analyze research content"""
    try:
        data = request.json
        
        if 'content' not in data:
            return jsonify({'error': 'Missing content field'}), 400
        
        content = data.get('content')
        summary_type = data.get('summary_type', 'general')
        length = data.get('length', 'medium')
        
        logger.info(f"Analyzing content: type={summary_type}, length={length}")
        
        # Summarize content
        analysis = research_assistant.summarize_content(
            content=content,
            summary_type=summary_type,
            length=length
        )
        
        return jsonify({
            'analysis': analysis,
            'timestamp': datetime.now().isoformat(),
            'disclaimer': 'AI-generated summaries may miss nuances in the original content.'
        })
    
    except Exception as e:
        logger.error(f"Error analyzing content: {e}")
        return jsonify({'error': 'Failed to analyze content'}), 500


@app.route('/api/research/extract-insights', methods=['POST'])
def extract_insights():
    """Extract insights from content"""
    try:
        data = request.json
        
        if 'content' not in data:
            return jsonify({'error': 'Missing content field'}), 400
        
        content = data.get('content')
        focus_area = data.get('focus_area', '')
        
        logger.info("Extracting insights from content")
        
        # Extract insights
        insights = research_assistant.extract_insights(
            content=content,
            focus_area=focus_area if focus_area else None
        )
        
        return jsonify({
            'insights': insights,
            'count': len(insights),
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error extracting insights: {e}")
        return jsonify({'error': 'Failed to extract insights'}), 500


# ==================== CHATBOT API ====================

@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat with AI assistant"""
    try:
        data = request.json
        
        if 'message' not in data:
            return jsonify({'error': 'Missing message field'}), 400
        
        message = data.get('message')
        history = data.get('history', [])
        
        logger.info(f"Processing chat message: {message[:50]}...")
        
        # Process request
        response = smart_assistant.chatbot.chat(message)
        
        return jsonify({
            'response': response,
            'timestamp': datetime.now().isoformat(),
            'disclaimer': 'This is an AI-generated response. Please verify information before acting on it.'
        })
    
    except Exception as e:
        logger.error(f"Error processing chat: {e}")
        return jsonify({'error': 'Failed to process message'}), 500


@app.route('/api/chat/intent', methods=['POST'])
def detect_intent():
    """Detect user intent from message"""
    try:
        data = request.json
        
        if 'message' not in data:
            return jsonify({'error': 'Missing message field'}), 400
        
        message = data.get('message')
        
        logger.info(f"Detecting intent: {message[:50]}...")
        
        # Detect intent
        intent_result = smart_assistant.process_request(message)
        
        return jsonify({
            'intent_type': intent_result.get('type'),
            'confidence': 0.9,  # Placeholder
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error detecting intent: {e}")
        return jsonify({'error': 'Failed to detect intent'}), 500


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    logger.error(f"Server error: {error}")
    return jsonify({'error': 'Internal server error'}), 500


@app.errorhandler(400)
def bad_request(error):
    """Handle 400 errors"""
    return jsonify({'error': 'Bad request'}), 400


# ==================== STARTUP ====================

if __name__ == '__main__':
    logger.info("=" * 50)
    logger.info("AI Productivity Assistant Starting...")
    logger.info("=" * 50)
    logger.info(f"Environment: {config.APP_ENV}")
    logger.info(f"AI Service: {config.AI_SERVICE}")
    logger.info(f"Debug Mode: {config.DEBUG}")
    logger.info(f"Server: http://{config.HOST}:{config.PORT}")
    logger.info("=" * 50)
    
    # Run development server
    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG,
        use_reloader=True
    )
