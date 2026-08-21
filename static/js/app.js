/* AI Productivity Assistant - JavaScript */

// ==================== STATE MANAGEMENT ====================
const appState = {
    currentSection: 'dashboard',
    loading: false,
    chatHistory: []
};

// ==================== INITIALIZATION ====================
document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
    initializeSidebar();
});

function initializeEventListeners() {
    // Sidebar Navigation
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const section = link.dataset.section;
            navigateToSection(section);
        });
    });

    // Dashboard Quick Buttons
    document.querySelectorAll('.quick-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const section = btn.dataset.section;
            navigateToSection(section);
        });
    });

    // Form Submissions
    document.getElementById('emailForm').addEventListener('submit', handleEmailSubmit);
    document.getElementById('meetingForm').addEventListener('submit', handleMeetingSubmit);
    document.getElementById('tasksForm').addEventListener('submit', handleTasksSubmit);
    document.getElementById('researchForm').addEventListener('submit', handleResearchSubmit);
    document.getElementById('chatForm').addEventListener('submit', handleChatSubmit);

    // Action Buttons
    document.getElementById('copyEmailBtn')?.addEventListener('click', copyToClipboard);
    document.getElementById('downloadEmailBtn')?.addEventListener('click', downloadEmail);
    document.getElementById('regenerateEmailBtn')?.addEventListener('click', () => {
        document.getElementById('emailForm').dispatchEvent(new Event('submit'));
    });

    // Sidebar Toggle (Mobile)
    document.getElementById('sidebarToggle')?.addEventListener('click', toggleSidebar);

    // Settings Button
    document.getElementById('settingsBtn')?.addEventListener('click', openSettings);
}

function initializeSidebar() {
    // Set active nav item
    updateActiveNavItem('dashboard');
}

// ==================== NAVIGATION ====================
function navigateToSection(section) {
    // Update state
    appState.currentSection = section;

    // Hide all sections
    document.querySelectorAll('.section').forEach(sec => {
        sec.classList.remove('active');
    });

    // Show selected section
    const sectionId = `${section}-section`;
    const sectionElement = document.getElementById(sectionId);
    if (sectionElement) {
        sectionElement.classList.add('active');
    }

    // Update page title
    const titles = {
        'dashboard': 'Dashboard',
        'email': 'Email Generator',
        'meeting': 'Meeting Summarizer',
        'tasks': 'Task Planner',
        'research': 'Research Assistant',
        'chatbot': 'AI Chatbot'
    };
    document.getElementById('pageTitle').textContent = titles[section] || 'Dashboard';

    // Update active nav item
    updateActiveNavItem(section);

    // Close mobile sidebar
    if (window.innerWidth < 768) {
        document.querySelector('.sidebar').classList.remove('active');
    }
}

function updateActiveNavItem(section) {
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });

    const activeLink = document.querySelector(`[data-section="${section}"]`);
    if (activeLink) {
        activeLink.closest('.nav-item').classList.add('active');
    }
}

function toggleSidebar() {
    document.querySelector('.sidebar').classList.toggle('active');
}

// ==================== EMAIL GENERATOR ====================
async function handleEmailSubmit(e) {
    e.preventDefault();

    const tone = document.getElementById('emailTone').value;
    const audience = document.getElementById('emailAudience').value;
    const topic = document.getElementById('emailTopic').value;
    const context = document.getElementById('emailContext').value;

    if (!tone || !audience || !topic) {
        showToast('Please fill in all required fields', 'error');
        return;
    }

    showLoading(true);

    try {
        const response = await fetch('/api/email/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                topic,
                tone,
                audience,
                context
            })
        });

        const data = await response.json();

        if (response.ok) {
            displayEmailResult(data.email);
            showToast('Email generated successfully!', 'success');
        } else {
            showToast(data.error || 'Failed to generate email', 'error');
        }
    } catch (error) {
        showToast('Error: ' + error.message, 'error');
        // Fallback demo response
        displayEmailResult(generateDemoEmail(tone, audience, topic));
    } finally {
        showLoading(false);
    }
}

function displayEmailResult(email) {
    const resultDiv = document.getElementById('emailResult');
    const contentDiv = document.getElementById('emailContent');

    // Format email for display
    const formattedEmail = `
        <div class="email-display">
            <div class="email-section">
                <strong>Subject:</strong> ${extractEmailSubject(email)}
            </div>
            <div class="email-section">
                ${email.split('\n').map(line => line.trim() ? `<p>${escapeHtml(line)}</p>` : '').join('')}
            </div>
            <div class="email-disclaimer">
                <i class="fas fa-exclamation-circle"></i>
                <p><strong>Disclaimer:</strong> AI-generated content may require human review before sending.</p>
            </div>
        </div>
    `;

    contentDiv.innerHTML = formattedEmail;
    resultDiv.style.display = 'block';
}

function extractEmailSubject(email) {
    const match = email.match(/Subject:\s*(.+)/i);
    return match ? match[1] : 'Email';
}

function generateDemoEmail(tone, audience, topic) {
    return `Subject: ${topic}

Dear ${audience === 'client' ? 'Valued Client' : audience === 'manager' ? 'Manager' : 'Team'},

I hope this message finds you well. I'm writing to discuss ${topic}.

${tone === 'formal' ? 'I would like to formally address the key points regarding this matter.' : tone === 'informal' ? 'I wanted to touch base about this with you.' : 'I believe there are significant opportunities here that we should explore together.'}

Please let me know your thoughts at your earliest convenience.

Best regards,
${audience === 'client' ? 'Professional Team' : 'Your Colleague'}`;
}

function copyToClipboard() {
    const emailContent = document.getElementById('emailContent').innerText;
    navigator.clipboard.writeText(emailContent).then(() => {
        showToast('Email copied to clipboard!', 'success');
    });
}

function downloadEmail() {
    const emailContent = document.getElementById('emailContent').innerText;
    const element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(emailContent));
    element.setAttribute('download', 'email.txt');
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
    showToast('Email downloaded!', 'success');
}

// ==================== MEETING SUMMARIZER ====================
async function handleMeetingSubmit(e) {
    e.preventDefault();

    const notes = document.getElementById('meetingNotes').value;
    const title = document.getElementById('meetingTitle').value;
    const attendees = document.getElementById('meetingAttendees').value;

    if (!notes) {
        showToast('Please enter meeting notes', 'error');
        return;
    }

    showLoading(true);

    try {
        const response = await fetch('/api/meeting/summarize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                meeting_notes: notes,
                meeting_title: title,
                attendees: attendees.split(',').map(a => a.trim()).filter(a => a)
            })
        });

        const data = await response.json();

        if (response.ok) {
            displayMeetingResult(data);
            showToast('Meeting summarized successfully!', 'success');
        } else {
            showToast(data.error || 'Failed to summarize meeting', 'error');
        }
    } catch (error) {
        showToast('Error: ' + error.message, 'error');
        displayMeetingResult(generateDemoSummary());
    } finally {
        showLoading(false);
    }
}

function displayMeetingResult(summary) {
    const resultDiv = document.getElementById('meetingResult');

    document.getElementById('meetingSummary').textContent = summary.summary || 'Meeting discussed key topics and decisions.';

    document.getElementById('meetingKeyPoints').innerHTML = (summary.key_points || [])
        .map(point => `<li>${escapeHtml(point)}</li>`)
        .join('');

    document.getElementById('meetingActionItems').innerHTML = (summary.action_items || [])
        .map(item => `<li><strong>${escapeHtml(item.item || item)}</strong> - ${escapeHtml(item.owner || 'TBD')}</li>`)
        .join('');

    document.getElementById('meetingDeadlines').innerHTML = (summary.deadlines || [])
        .map(deadline => `<li>${escapeHtml(deadline)}</li>`)
        .join('');

    resultDiv.style.display = 'block';
}

function generateDemoSummary() {
    return {
        summary: 'Team discussed project progress, reviewed budget allocations, and set priorities for Q4.',
        key_points: [
            'Project is on track for Q4 launch',
            'Budget approved for marketing campaign',
            'New team member onboarding scheduled'
        ],
        action_items: [
            { item: 'Finalize launch plan', owner: 'Alice', deadline: 'EOW' },
            { item: 'Prepare marketing materials', owner: 'Bob', deadline: 'Next week' },
            { item: 'Set up onboarding schedule', owner: 'Carol', deadline: 'Tomorrow' }
        ],
        deadlines: [
            'Launch plan - End of week',
            'Marketing materials - Next week',
            'Onboarding setup - Tomorrow'
        ]
    };
}

// ==================== TASK PLANNER ====================
async function handleTasksSubmit(e) {
    e.preventDefault();

    const tasks = document.getElementById('taskList').value.split('\n')
        .map(t => t.trim())
        .filter(t => t);
    const timeframe = document.getElementById('taskTimeframe').value;
    const hours = parseInt(document.getElementById('taskHours').value);
    const context = document.getElementById('taskContext').value;

    if (tasks.length === 0) {
        showToast('Please enter at least one task', 'error');
        return;
    }

    showLoading(true);

    try {
        const response = await fetch('/api/tasks/plan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                tasks,
                time_frame: timeframe,
                working_hours: hours,
                context
            })
        });

        const data = await response.json();

        if (response.ok) {
            displayTasksResult(data);
            showToast('Task plan generated successfully!', 'success');
        } else {
            showToast(data.error || 'Failed to generate plan', 'error');
        }
    } catch (error) {
        showToast('Error: ' + error.message, 'error');
        displayTasksResult(generateDemoPlan(tasks));
    } finally {
        showLoading(false);
    }
}

function displayTasksResult(plan) {
    const resultDiv = document.getElementById('tasksResult');

    document.getElementById('planOverview').textContent = plan.plan_overview || 'Your tasks have been prioritized and scheduled for optimal productivity.';

    const tasksHtml = (plan.scheduled_tasks || [])
        .map((task, idx) => `
            <div class="task-item">
                <div class="task-info">
                    <h5>#${task.order || idx + 1}: ${escapeHtml(task.task)}</h5>
                    <p>Priority: <strong>${task.priority}</strong> | Time: ${task.estimated_hours || '?'} hrs</p>
                    <p>${escapeHtml(task.rationale || '')}</p>
                </div>
                <div class="task-time">
                    ${task.time_slot || 'TBD'}
                </div>
            </div>
        `)
        .join('');

    document.getElementById('scheduledTasks').innerHTML = tasksHtml;

    document.getElementById('optimizationTips').innerHTML = (plan.time_optimization || [])
        .map(tip => `<li>${escapeHtml(tip)}</li>`)
        .join('');

    resultDiv.style.display = 'block';
}

function generateDemoPlan(tasks) {
    return {
        plan_overview: `Your ${tasks.length} tasks have been prioritized and scheduled for optimal productivity.`,
        scheduled_tasks: tasks.map((task, idx) => ({
            order: idx + 1,
            task,
            priority: idx === 0 ? 'critical' : idx === 1 ? 'high' : 'medium',
            estimated_hours: 1 + idx,
            time_slot: idx === 0 ? 'Morning' : idx === 1 ? 'Afternoon' : 'Evening',
            rationale: 'Scheduled based on urgency and complexity'
        })),
        time_optimization: [
            'Start with high-priority tasks during peak energy hours',
            'Group similar tasks to reduce context switching',
            'Take breaks between complex tasks'
        ]
    };
}

// ==================== RESEARCH ASSISTANT ====================
async function handleResearchSubmit(e) {
    e.preventDefault();

    const content = document.getElementById('researchContent').value;
    const type = document.getElementById('researchType').value;
    const length = document.getElementById('researchLength').value;

    if (!content) {
        showToast('Please enter content to analyze', 'error');
        return;
    }

    showLoading(true);

    try {
        const response = await fetch('/api/research/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                content,
                summary_type: type,
                length
            })
        });

        const data = await response.json();

        if (response.ok) {
            displayResearchResult(data);
            showToast('Content analyzed successfully!', 'success');
        } else {
            showToast(data.error || 'Failed to analyze content', 'error');
        }
    } catch (error) {
        showToast('Error: ' + error.message, 'error');
        displayResearchResult(generateDemoAnalysis());
    } finally {
        showLoading(false);
    }
}

function displayResearchResult(analysis) {
    const resultDiv = document.getElementById('researchResult');

    document.getElementById('analysisSummary').textContent = analysis.summary || 'Content analysis completed.';

    document.getElementById('analysisKeyPoints').innerHTML = (analysis.key_points || [])
        .map(point => `<li>${escapeHtml(point)}</li>`)
        .join('');

    document.getElementById('analysisInsights').innerHTML = (analysis.main_ideas || analysis.important_details || [])
        .map(insight => `<li>${escapeHtml(insight)}</li>`)
        .join('');

    document.getElementById('analysisImplications').textContent = analysis.implications || 'See key insights for practical applications.';

    resultDiv.style.display = 'block';
}

function generateDemoAnalysis() {
    return {
        summary: 'This content discusses important workplace concepts with practical applications for professionals.',
        key_points: [
            'Main point 1 from the content',
            'Key finding relevant to your work',
            'Important consideration to remember'
        ],
        main_ideas: [
            'Central theme: Productivity and automation',
            'Supporting idea: AI improves efficiency',
            'Application: Tools should be user-friendly'
        ],
        implications: 'These insights suggest that investing in automation tools can significantly improve team productivity.'
    };
}

// ==================== AI CHATBOT ====================
async function handleChatSubmit(e) {
    e.preventDefault();

    const input = document.getElementById('chatInput');
    const message = input.value.trim();

    if (!message) return;

    // Add user message to chat
    addChatMessage('user', message);
    input.value = '';
    input.focus();

    showLoading(true);

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message,
                history: appState.chatHistory
            })
        });

        const data = await response.json();

        if (response.ok) {
            addChatMessage('assistant', data.response);
            appState.chatHistory.push({ role: 'user', content: message });
            appState.chatHistory.push({ role: 'assistant', content: data.response });
        } else {
            addChatMessage('assistant', 'Sorry, I encountered an error. Please try again.');
        }
    } catch (error) {
        // Fallback demo response
        const demoResponses = [
            'I can help you with email generation, meeting summarization, task planning, research analysis, and general productivity advice.',
            'For email generation, I can create professional emails in different tones and for different audiences.',
            'I can summarize meeting notes and extract key points, decisions, and action items.',
            'Let me know what specific task you need help with!'
        ];
        const response = demoResponses[Math.floor(Math.random() * demoResponses.length)];
        addChatMessage('assistant', response);
    } finally {
        showLoading(false);
    }
}

function addChatMessage(role, content) {
    const messagesDiv = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}-message`;

    const avatar = role === 'user' ? '👤' : '🤖';
    const avatarClass = role === 'user' ? 'user' : 'assistant';

    messageDiv.innerHTML = `
        <div class="message-avatar">
            ${role === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-brain"></i>'}
        </div>
        <div class="message-content">
            <p>${escapeHtml(content)}</p>
        </div>
    `;

    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// ==================== UI UTILITIES ====================
function showLoading(show) {
    const modal = document.getElementById('loadingModal');
    if (show) {
        modal.classList.add('active');
        appState.loading = true;
    } else {
        modal.classList.remove('active');
        appState.loading = false;
    }
}

function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast show ${type}`;

    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function openSettings() {
    showToast('Settings page coming soon!', 'info');
}

// ==================== RESPONSIVE HANDLING ====================
window.addEventListener('resize', () => {
    if (window.innerWidth >= 768) {
        document.querySelector('.sidebar').classList.remove('active');
    }
});

// ==================== EXPORT ====================
window.appState = appState;
window.navigateToSection = navigateToSection;
