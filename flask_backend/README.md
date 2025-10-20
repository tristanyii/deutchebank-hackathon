# Flask Backend for Retell AI Integration - Anthony Persona

This Flask backend integrates with Retell AI to provide a voice-first U.S. benefits hotline using the Anthony persona for Sharing Excess.

## Features

- **Anthony Persona**: Multilingual, voice-first U.S. benefits assistant
- **Retell AI Webhook Integration**: Handles voice call events from Retell AI
- **Dynamic Conversation Flow**: Collects user info step-by-step (need, location, name, age, income)
- **Multilingual Support**: Detects and responds in 10 languages (English, Spanish, French, German, Hindi, Russian, Portuguese, Japanese, Italian, Dutch)
- **U.S. Resource Matching**: Provides LIHEAP, Housing Resources, and Unclaimed Benefits Finder
- **Voice-Optimized Responses**: Natural speech formatting at 1.3x speed
- **Urgent Situation Handling**: Empathetic responses for shutoffs/evictions

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

2. **Environment Variables**:
   Make sure your `.env` file in the parent directory contains:
   ```
   GROQ_API_KEY=your_groq_api_key
   SERP_API_KEY=your_serp_api_key
   ```

3. **Run the Server**:
   ```bash
   python run_server.py
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

Test Anthony persona conversation flow:
```bash
# Test full conversation flow
curl -X POST http://localhost:5000/test-anthony \
  -H "Content-Type: application/json" \
  -d '{"call_id": "test-123", "user_input": "Hi, I need help with housing"}'

# Test individual responses
curl -X POST http://localhost:5000/test-agent \
  -H "Content-Type: application/json" \
  -d '{"query": "I need help with energy bills", "call_id": "test-456"}'
```

## U.S. Resources Provided

Anthony always provides these three core resources:

1. **LIHEAP (Energy Bill Help)**
   - Helps pay heating or cooling bills
   - Based on ZIP and income eligibility
   - Link: https://www.acf.hhs.gov/ocs/energy-assistance
   - Requirements: photo ID, proof of address, recent bill, income proof

2. **Housing Resources**
   - HUD helps find rental and affordable housing
   - State-specific housing programs
   - Link: https://www.hud.gov/states

3. **Unclaimed Benefits Finder**
   - Checks for food, health, cash aid, tax credits
   - Quick and private screening
   - Link: https://www.benefits.gov/benefit-finder

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
