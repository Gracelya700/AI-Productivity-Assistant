# Quick Start Guide - AI Workplace Productivity Assistant

## 🚀 Get Started in 3 Steps

### Step 1: Setup (First Time Only)

**On Mac/Linux:**
```bash
chmod +x start.sh
./start.sh
```

**On Windows:**
```bash
start.bat
```

### Step 2: Configure API Keys

1. Open `.env` file
2. Add your API keys:
   - **OpenAI API Key**: Get from https://platform.openai.com/api-keys
   - **Google API Key**: Get from https://makersuite.google.com/app/apikey

```bash
OPENAI_API_KEY=sk-your-key-here
GOOGLE_API_KEY=your-google-key-here
```

### Step 3: Start the Application

The startup script will automatically:
- Create a Python virtual environment
- Install all dependencies
- Start the Flask server on http://localhost:5000

## 📖 Using the Application

### Email Generator
1. Click "Email Generator" in sidebar
2. Select tone (Formal, Informal, Persuasive)
3. Select audience (Client, Manager, Team)
4. Enter email topic and context
5. Click "Generate Email"
6. Copy, download, or regenerate

### Meeting Summarizer
1. Click "Meeting Summarizer" in sidebar
2. Add meeting title and attendees (optional)
3. Paste meeting notes
4. Click "Summarize Meeting"
5. View extracted key points, action items, and deadlines

### Task Planner
1. Click "Task Planner" in sidebar
2. Select time frame (Daily or Weekly)
3. Enter working hours available
4. List your tasks (one per line)
5. Click "Generate Plan"
6. Get prioritized schedule and optimization tips

### Research Assistant
1. Click "Research Assistant" in sidebar
2. Select summary type and length
3. Paste article, report, or research content
4. Click "Analyze Content"
5. Get comprehensive analysis and insights

### AI Chatbot
1. Click "AI Chatbot" in sidebar
2. Type your question or request
3. Receive AI-powered assistance
4. Continue conversation naturally

## 🔑 API Keys

### Getting OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Sign up or log in
3. Click "Create new secret key"
4. Copy the key to `.env`

### Getting Google API Key
1. Go to https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key to `.env`

## 🛠️ Troubleshooting

### Port Already in Use
If port 5000 is already in use:
```bash
# Change port in .env
PORT=5001
```

### Missing Dependencies
```bash
# Reinstall all dependencies
pip install --upgrade -r requirements.txt
```

### API Key Issues
```bash
# Test OpenAI connection
python -c "import openai; openai.api_key='your-key'; print('OK')"
```

### Virtual Environment Issues
```bash
# Delete and recreate
rm -rf venv  # On Windows: rmdir /s venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 📊 Features Overview

| Feature | Description | Use Case |
|---------|-------------|----------|
| 📧 Email Generator | Create professional emails in different tones | Draft emails to clients, managers, or team |
| 📝 Meeting Summarizer | Extract key points and action items | Summarize meeting notes automatically |
| ✅ Task Planner | Prioritize and schedule tasks intelligently | Optimize daily/weekly workflows |
| 🔍 Research Assistant | Summarize and analyze content | Synthesize articles and reports |
| 💬 AI Chatbot | Ask anything about productivity | Get general assistance and advice |

## 📱 Supported Devices

✅ Desktop (Windows, Mac, Linux)
✅ Tablet
✅ Mobile (responsive design)

## 🔒 Privacy & Security

- All AI requests go directly to OpenAI/Google APIs
- No data is stored on our servers
- Your API keys stay in your `.env` file
- Recommended: Use read-only API keys with rate limits

## 📞 Support

- **Documentation**: See README.md
- **Issues**: Check GitHub issues
- **API Docs**: `/api/health` endpoint
- **Features**: All 5 core features included

## 🎓 Learning Resources

- Prompt Engineering: See `docs/prompt_engineering.md`
- Ethical AI: See `docs/ethical_ai.md`
- API Reference: See `docs/api_reference.md`

## 🚀 Next Steps

1. ✅ Install and run the app
2. ✅ Test all features
3. ✅ Customize prompts in `src/*/prompts.py`
4. ✅ Add your own features
5. ✅ Deploy to production

---

**Ready to boost productivity? Let's go!** 🎉

Need help? Check the full documentation in the `docs/` folder.
