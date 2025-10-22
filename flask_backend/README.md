# Excess - AI Voice Support Line Backend

**🏆 1st Place Winner - Deutsche Bank Hackathon 2024**

This Flask backend powers **Excess**, an AI-powered voice support line that helps underrepresented communities discover verified local aid programs through simple, human-like interactions.

## 🎯 **Project Overview**

**Excess** addresses a critical problem: millions of people across the U.S. qualify for housing, food, and energy assistance, yet many never receive it because the information is confusing, scattered, or entirely offline.

### **Our Solution:**
- **🎙️ Voice-First Interface**: Makes aid discovery accessible to people without internet access or technology experience
- **🌍 Multilingual Support**: Serves diverse and rural communities in their native languages  
- **🗺️ Real-Time Visualization**: Web app shows nearby resources and assistance options
- **💰 Cost Effective**: Operates at ~60% lower cost than traditional human-operated support lines

### **How It Works:**
1. **Voice Input**: Users call the support line and speak naturally
2. **AI Processing**: Anthony (our AI agent) understands their needs in multiple languages
3. **Resource Matching**: System identifies relevant U.S. government and nonprofit programs
4. **Guided Assistance**: Provides step-by-step guidance and application links
5. **Visualization**: Web app shows nearby resources on an interactive map

## 🔧 **This Flask Backend**

This backend is the **brain** of the Excess voice system, handling:
- **Retell AI Integration**: Processes voice calls and SMS
- **Anthony Persona**: Multilingual AI agent for natural conversations
- **Resource Matching**: Connects users to LIHEAP, Housing, and Benefits programs
- **Conversation Management**: Tracks user needs and provides personalized assistance

## 🚀 **Key Features**

### **Anthony - The AI Agent**
- **🎙️ Voice-First Design**: Natural conversations without internet dependency
- **🌍 Multilingual Support**: 10 languages (English, Spanish, French, German, Hindi, Russian, Portuguese, Japanese, Italian, Dutch)
- **🧠 Smart Conversation Flow**: Collects user info step-by-step (need, location, name, age, income)
- **⚡ Real-Time Processing**: Instant responses through Retell AI integration
- **🚨 Urgent Situation Handling**: Empathetic responses for shutoffs/evictions

### **Technical Capabilities**
- **Retell AI Webhook Integration**: Handles voice call events seamlessly
- **U.S. Resource Matching**: Provides LIHEAP, Housing Resources, and Unclaimed Benefits Finder
- **Voice-Optimized Responses**: Natural speech formatting at 1.3x speed
- **Cost Efficiency**: ~60% lower operational costs than human support lines

## Endpoints

### Main Webhook Endpoint
- **POST** `/retell/webhook` - Primary webhook for Retell AI events
- **POST** `/retell/events` - Alternative webhook endpoint

### Utility Endpoints
- **GET** `/health` - Health check endpoint
- **POST** `/test-anthony` - Test Anthony persona conversation flow
- **POST** `/test-agent` - Test Anthony persona with a query

## Setup

1. **Install Dependencies**:
   ```bash
   cd flask_backend
   pip install -r requirements.txt
   ```
   
   **Note**: The Flask backend requires the same dependencies as your main project. If you get import errors, install the main project dependencies:
   ```bash
   # From the root directory
   pip install langchain langgraph langchain-groq langchain-community groq python-dotenv google-search-results wikipedia reportlab requests pydantic lxml streamlit
   ```

2. **Environment Variables**:
   The Flask backend uses the same `.env` file as your main project. Make sure your `.env` file in the **root directory** contains:
   ```
   GROQ_API_KEY=your_groq_api_key
   SERP_API_KEY=your_serp_api_key
   ```

3. **Run the Server**:
   ```bash
   # Option 1: Use the startup script
   ./start.sh
   
   # Option 2: Run directly
   python run_server.py
   
   # Option 3: Run with Flask directly
   python app.py
   ```

## Retell AI Configuration

Configure your Retell AI webhook to point to:
```
https://your-domain.com/retell/webhook
```

## How It Works

1. **Voice Input**: User speaks during a Retell AI call
2. **Transcription**: Retell AI sends transcribed text to the webhook
3. **Anthony Processing**: The Flask backend processes the text with Anthony persona
4. **Conversation Flow**: Anthony collects user info step-by-step (need, location, name, age, income)
5. **Resource Matching**: Anthony provides U.S. resources (LIHEAP, Housing, Benefits Finder)
6. **Voice Response**: The response is formatted for natural speech and sent back to Retell AI
7. **Voice Output**: Retell AI converts the response to speech for the user

## Anthony Persona Features

### Conversation Flow
1. **Greeting**: "Hi, I'm Anthony with Bridge—a free, confidential benefits line. What kind of help are you looking for today?"
2. **Need Detection**: Identifies if user needs energy, housing, food, money, or other help
3. **Location Collection**: "What state or ZIP code are you in?"
4. **Name Collection**: "What's your name? You can skip this if you prefer."
5. **Age Collection**: "What's your age?"
6. **Income Collection**: "What's your annual income in dollars?"
7. **Resource Provision**: Provides LIHEAP, Housing Resources, and Unclaimed Benefits Finder

### Multilingual Support
- **Automatic Detection**: Detects language from user speech
- **10 Languages**: English, Spanish, French, German, Hindi, Russian, Portuguese, Japanese, Italian, Dutch
- **Consistent Experience**: Maintains same conversation flow in all languages

### Voice Optimization
- **1.3x Speed**: Natural, brisk pace for voice calls
- **Short Turns**: 1-2 sentences per response
- **Barge-in Support**: Allows user interruption
- **Natural Pauses**: Easy to follow conversation flow

## Testing

### **Quick Test**
```bash
# Run the integration test suite
cd flask_backend
python test_integration.py
```

### **Manual Testing**
```bash
# Test full conversation flow
curl -X POST http://localhost:5000/test-anthony \
  -H "Content-Type: application/json" \
  -d '{"call_id": "test-123", "user_input": "Hi, I need help with housing"}'

# Test individual responses
curl -X POST http://localhost:5000/test-agent \
  -H "Content-Type: application/json" \
  -d '{"query": "I need help with energy bills", "call_id": "test-456"}'

# Test health check
curl http://localhost:5000/health
```

### **Troubleshooting**
If you get import errors:
1. Make sure you're in the `flask_backend` directory
2. Install dependencies from the root directory: `pip install -r ../requirements.txt`
3. Check that your `.env` file is in the root directory with valid API keys
4. Try running: `python -c "from app import app; print('Import successful')"`

## 🏛️ **U.S. Resources Provided**

Anthony always provides these three core resources to ensure comprehensive assistance:

### **1. LIHEAP (Energy Bill Help)**
- **Purpose**: Helps pay heating or cooling bills
- **Eligibility**: Based on ZIP code and income
- **Link**: https://www.acf.hhs.gov/ocs/energy-assistance
- **Requirements**: photo ID, proof of address, recent bill, income proof

### **2. Housing Resources**
- **Purpose**: HUD helps find rental and affordable housing
- **Coverage**: State-specific housing programs
- **Link**: https://www.hud.gov/states

### **3. Unclaimed Benefits Finder**
- **Purpose**: Checks for food, health, cash aid, tax credits
- **Process**: Quick and private screening
- **Link**: https://www.benefits.gov/benefit-finder

## 🎯 **Impact & Results**

- **🏆 1st Place**: Deutsche Bank Hackathon 2024
- **💰 Cost Reduction**: ~60% lower operational costs than human support lines
- **🌍 Accessibility**: Serves communities without internet access
- **📞 Voice-First**: Natural conversation interface for all users
- **🔍 Comprehensive**: Covers energy, housing, food, and financial assistance

## Response Formatting

The backend automatically formats responses for voice by:
- Natural speech patterns at 1.3x speed
- Short, clear turns (1-2 sentences)
- Multilingual support with consistent flow
- Empathetic handling of urgent situations

## Error Handling

- Graceful handling of agent unavailability
- Fallback responses for processing errors
- Comprehensive logging for debugging

## Common Issues & Solutions

### **Import Errors**
```
ModuleNotFoundError: No module named 'langchain'
```
**Solution**: Install dependencies from root directory
```bash
cd /Users/tristanyi/deutchebank-hackathon
pip install -r requirements.txt
```

### **Environment Variables Not Found**
```
ValueError: GROQ_API_KEY and SERP_API_KEY are required in .env file
```
**Solution**: Ensure `.env` file is in the root directory with valid API keys

### **Port Already in Use**
```
OSError: [Errno 48] Address already in use
```
**Solution**: Kill existing process or use different port
```bash
lsof -ti:5000 | xargs kill -9
# Or set different port: PORT=5001 python run_server.py
```

### **Path Issues**
```
ImportError: cannot import name 'ResourceAgent'
```
**Solution**: Run from flask_backend directory
```bash
cd flask_backend
python run_server.py
```

## File Structure
```
flask_backend/
├── app.py                 # Main Flask application with Anthony persona
├── utils.py              # Utility functions for voice formatting
├── config.py             # Configuration settings
├── requirements.txt      # Flask-specific dependencies
├── run_server.py         # Server runner script
├── deploy.py            # Deployment helper script
├── test_integration.py   # Integration testing script
├── start.sh             # Easy startup script
└── README.md            # This documentation
```

## 🛠️ **Dependencies**
The Flask backend requires these packages (installed from root directory):
- `flask` - Web framework
- `requests` - HTTP requests
- `python-dotenv` - Environment variables
- `langchain` - AI agent framework
- `langgraph` - Agent orchestration
- `langchain-groq` - Groq LLM integration
- `langchain-community` - Community tools
- `groq` - Groq API client
- `google-search-results` - Search functionality
- `wikipedia` - Wikipedia integration
- `reportlab` - PDF generation
- `pydantic` - Data validation
- `lxml` - XML processing

## 👥 **Team**
**Excess** was created by the winning team at Deutsche Bank Hackathon 2024:
- **Uttam Dev Sapkota**
- **Anna Benbow** 
- **Tahia Islam**
- **Rama Yakkala**

**Mentors**: Meghna Gaddam and Anil Pandya

## 🎉 **Recognition**
- **🏆 1st Place Winner** - Deutsche Bank Hackathon 2024
- **💡 Innovation Award** - AI-powered accessibility solution
- **🌍 Social Impact** - Serving underrepresented communities
