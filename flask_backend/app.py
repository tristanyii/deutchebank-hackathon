from flask import Flask, request, jsonify
import json
import logging
from datetime import datetime
import os
import sys
import re
from typing import Dict, List, Optional

# Add the parent directory to the path to import our agent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Untapped_Resource_Agent import ResourceAgent
from utils import format_resource_response, truncate_for_voice, extract_user_intent, log_conversation_turn

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the resource agent
try:
    resource_agent = ResourceAgent()
    logger.info("Resource agent initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize resource agent: {e}")
    resource_agent = None

# Anthony persona conversation management
class AnthonyPersona:
    def __init__(self):
        self.conversation_states = {}  # Track conversation state per call
        self.supported_languages = {
            'en': 'English', 'es': 'Spanish', 'fr': 'French', 'de': 'German',
            'hi': 'Hindi', 'ru': 'Russian', 'pt': 'Portuguese', 'ja': 'Japanese',
            'it': 'Italian', 'nl': 'Dutch'
        }
    
    def get_call_state(self, call_id: str) -> Dict:
        """Get or create conversation state for a call"""
        if call_id not in self.conversation_states:
            self.conversation_states[call_id] = {
                'step': 'greeting',
                'language': 'en',
                'user_info': {},
                'need_type': None,
                'conversation_history': []
            }
        return self.conversation_states[call_id]
    
    def detect_language(self, text: str) -> str:
        """Simple language detection based on common words"""
        text_lower = text.lower()
        
        # Spanish indicators
        if any(word in text_lower for word in ['hola', 'gracias', 'ayuda', 'necesito', 'por favor']):
            return 'es'
        # French indicators  
        elif any(word in text_lower for word in ['bonjour', 'merci', 'aide', 'besoin', 's\'il vous plaît']):
            return 'fr'
        # German indicators
        elif any(word in text_lower for word in ['hallo', 'danke', 'hilfe', 'brauche', 'bitte']):
            return 'de'
        # Hindi indicators
        elif any(word in text_lower for word in ['नमस्ते', 'धन्यवाद', 'मदद', 'ज़रूरत']):
            return 'hi'
        # Russian indicators
        elif any(word in text_lower for word in ['привет', 'спасибо', 'помощь', 'нужно']):
            return 'ru'
        # Portuguese indicators
        elif any(word in text_lower for word in ['olá', 'obrigado', 'ajuda', 'preciso', 'por favor']):
            return 'pt'
        # Japanese indicators
        elif any(word in text_lower for word in ['こんにちは', 'ありがとう', '助け', '必要']):
            return 'ja'
        # Italian indicators
        elif any(word in text_lower for word in ['ciao', 'grazie', 'aiuto', 'bisogno', 'per favore']):
            return 'it'
        # Dutch indicators
        elif any(word in text_lower for word in ['hallo', 'dank je', 'hulp', 'nodig', 'alsjeblieft']):
            return 'nl'
        
        return 'en'  # Default to English
    
    def get_greeting(self, language: str = 'en') -> str:
        """Get greeting in specified language"""
        greetings = {
            'en': "Hi, I'm Anthony with Bridge—a free, confidential benefits line. What kind of help are you looking for today? Energy, housing, food, money, or something else?",
            'es': "Hola, soy Anthony de Bridge—una línea gratuita y confidencial de beneficios. ¿Qué tipo de ayuda buscas hoy? ¿Energía, vivienda, comida, dinero, o algo más?",
            'fr': "Salut, je suis Anthony avec Bridge—une ligne d'assistance gratuite et confidentielle. Quel type d'aide cherchez-vous aujourd'hui? Énergie, logement, nourriture, argent, ou autre chose?",
            'de': "Hallo, ich bin Anthony von Bridge—eine kostenlose, vertrauliche Leistungslinie. Welche Art von Hilfe suchen Sie heute? Energie, Wohnen, Essen, Geld oder etwas anderes?",
            'hi': "नमस्ते, मैं एंथनी हूं ब्रिज के साथ—एक मुफ्त, गोपनीय लाभ लाइन। आज आपको किस तरह की मदद चाहिए? ऊर्जा, आवास, भोजन, पैसा, या कुछ और?",
            'ru': "Привет, я Энтони из Bridge—бесплатная, конфиденциальная линия помощи. Какую помощь вы ищете сегодня? Энергия, жилье, еда, деньги или что-то еще?",
            'pt': "Olá, sou Anthony da Bridge—uma linha gratuita e confidencial de benefícios. Que tipo de ajuda você está procurando hoje? Energia, habitação, comida, dinheiro, ou algo mais?",
            'ja': "こんにちは、私はブリッジのアンソニーです—無料の機密給付金ラインです。今日はどのような助けをお探しですか？エネルギー、住宅、食べ物、お金、またはその他？",
            'it': "Ciao, sono Anthony con Bridge—una linea di benefici gratuita e confidenziale. Che tipo di aiuto stai cercando oggi? Energia, alloggio, cibo, denaro, o qualcos'altro?",
            'nl': "Hallo, ik ben Anthony van Bridge—een gratis, vertrouwelijke voordelenlijn. Wat voor hulp zoekt u vandaag? Energie, huisvesting, voedsel, geld, of iets anders?"
        }
        return greetings.get(language, greetings['en'])
    
    def process_user_input(self, call_id: str, user_input: str) -> str:
        """Process user input and return appropriate response"""
        state = self.get_call_state(call_id)
        
        # Detect language if not already set
        if state['step'] == 'greeting':
            detected_lang = self.detect_language(user_input)
            state['language'] = detected_lang
            logger.info(f"Detected language: {detected_lang}")
        
        # Add to conversation history
        state['conversation_history'].append({
            'user': user_input,
            'timestamp': datetime.now().isoformat()
        })
        
        # Check for urgent situations
        if self.check_urgent_situation(user_input, state['language']):
            return self.handle_urgent_situation(state['language'])
        
        # Process based on conversation step
        if state['step'] == 'greeting':
            return self.handle_greeting_response(user_input, state)
        elif state['step'] == 'collecting_location':
            return self.handle_location_response(user_input, state)
        elif state['step'] == 'collecting_name':
            return self.handle_name_response(user_input, state)
        elif state['step'] == 'collecting_age':
            return self.handle_age_response(user_input, state)
        elif state['step'] == 'collecting_income':
            return self.handle_income_response(user_input, state)
        elif state['step'] == 'providing_resources':
            return self.handle_resource_followup(user_input, state)
        
        return self.get_greeting(state['language'])
    
    def check_urgent_situation(self, user_input: str, language: str) -> bool:
        """Check if user mentions urgent situation"""
        urgent_keywords = {
            'en': ['shutoff', 'eviction', 'today', 'emergency', 'urgent', 'immediately'],
            'es': ['corte', 'desalojo', 'hoy', 'emergencia', 'urgente', 'inmediatamente'],
            'fr': ['coupure', 'expulsion', 'aujourd\'hui', 'urgence', 'urgent', 'immédiatement'],
            'de': ['abgeschaltet', 'räumung', 'heute', 'notfall', 'dringend', 'sofort'],
            'hi': ['बंद', 'बेदखली', 'आज', 'आपातकाल', 'तत्काल', 'तुरंत'],
            'ru': ['отключение', 'выселение', 'сегодня', 'чрезвычайная ситуация', 'срочно', 'немедленно'],
            'pt': ['corte', 'despejo', 'hoje', 'emergência', 'urgente', 'imediatamente'],
            'ja': ['停止', '立ち退き', '今日', '緊急', '緊急', 'すぐに'],
            'it': ['interruzione', 'sfratto', 'oggi', 'emergenza', 'urgente', 'immediatamente'],
            'nl': ['afsluiting', 'ontruiming', 'vandaag', 'noodgeval', 'urgent', 'onmiddellijk']
        }
        
        keywords = urgent_keywords.get(language, urgent_keywords['en'])
        return any(keyword in user_input.lower() for keyword in keywords)
    
    def handle_urgent_situation(self, language: str) -> str:
        """Handle urgent situations with empathy"""
        responses = {
            'en': "I'm really sorry you're going through that. I can connect you to a local live assistance line right now.",
            'es': "Realmente lamento que estés pasando por eso. Puedo conectarte con una línea de asistencia local en vivo ahora mismo.",
            'fr': "Je suis vraiment désolé que vous traversiez cela. Je peux vous connecter à une ligne d'assistance locale en direct maintenant.",
            'de': "Es tut mir wirklich leid, dass Sie das durchmachen. Ich kann Sie jetzt mit einer lokalen Live-Hilfslinie verbinden.",
            'hi': "मुझे वास्तव में खेद है कि आप इससे गुजर रहे हैं। मैं आपको अभी एक स्थानीय लाइव सहायता लाइन से जोड़ सकता हूं।",
            'ru': "Мне очень жаль, что вы через это проходите. Я могу прямо сейчас подключить вас к местной линии живой помощи.",
            'pt': "Realmente sinto muito que você esteja passando por isso. Posso conectá-lo a uma linha de assistência local ao vivo agora mesmo.",
            'ja': "そのような状況に直面していることを本当に申し訳なく思います。今すぐ地元のライブアシスタンスラインに接続できます。",
            'it': "Mi dispiace davvero che tu stia passando questo. Posso collegarti a una linea di assistenza locale dal vivo proprio ora.",
            'nl': "Het spijt me echt dat je dit doormaakt. Ik kan je nu verbinden met een lokale live-assistentielijn."
        }
        return responses.get(language, responses['en'])
    
    def handle_greeting_response(self, user_input: str, state: Dict) -> str:
        """Handle response to initial greeting"""
        # Detect need type
        need_type = self.detect_need_type(user_input, state['language'])
        state['need_type'] = need_type
        state['step'] = 'collecting_location'
        
        # Acknowledge need and ask for location
        responses = {
            'en': f"Got it, you need help with {need_type}. What state or ZIP code are you in?",
            'es': f"Entendido, necesitas ayuda con {need_type}. ¿En qué estado o código postal estás?",
            'fr': f"Compris, vous avez besoin d'aide avec {need_type}. Dans quel état ou code postal êtes-vous?",
            'de': f"Verstanden, Sie brauchen Hilfe mit {need_type}. In welchem Bundesstaat oder Postleitzahl sind Sie?",
            'hi': f"समझ गया, आपको {need_type} के साथ मदद चाहिए। आप किस राज्य या ज़िप कोड में हैं?",
            'ru': f"Понял, вам нужна помощь с {need_type}. В каком штате или почтовом индексе вы находитесь?",
            'pt': f"Entendi, você precisa de ajuda com {need_type}. Em que estado ou código postal você está?",
            'ja': f"分かりました、{need_type}の助けが必要ですね。どの州または郵便番号にいますか？",
            'it': f"Capito, hai bisogno di aiuto con {need_type}. In che stato o codice postale sei?",
            'nl': f"Begrepen, je hebt hulp nodig met {need_type}. In welke staat of postcode ben je?"
        }
        return responses.get(state['language'], responses['en'])
    
    def detect_need_type(self, user_input: str, language: str) -> str:
        """Detect the type of help needed"""
        # Map keywords to need types
        need_mapping = {
            'energy': ['energy', 'electric', 'electricity', 'power', 'bill', 'heating', 'cooling', 'gas', 'utility'],
            'housing': ['housing', 'rent', 'rental', 'apartment', 'home', 'shelter', 'homeless'],
            'food': ['food', 'hungry', 'hunger', 'meal', 'nutrition', 'groceries', 'eat'],
            'money': ['money', 'cash', 'financial', 'income', 'benefits', 'assistance', 'aid'],
            'health': ['health', 'medical', 'doctor', 'healthcare', 'medicine', 'hospital'],
            'employment': ['job', 'work', 'employment', 'unemployed', 'career', 'training']
        }
        
        user_lower = user_input.lower()
        
        for need, keywords in need_mapping.items():
            if any(keyword in user_lower for keyword in keywords):
                return need
        
        return 'general'
    
    def handle_location_response(self, user_input: str, state: Dict) -> str:
        """Handle location response"""
        state['user_info']['location'] = user_input.strip()
        state['step'] = 'collecting_name'
        
        responses = {
            'en': "Thanks. What's your name? You can skip this if you prefer.",
            'es': "Gracias. ¿Cuál es tu nombre? Puedes omitir esto si prefieres.",
            'fr': "Merci. Quel est votre nom? Vous pouvez ignorer cela si vous préférez.",
            'de': "Danke. Wie ist Ihr Name? Sie können das überspringen, wenn Sie möchten.",
            'hi': "धन्यवाद। आपका नाम क्या है? आप चाहें तो इसे छोड़ सकते हैं।",
            'ru': "Спасибо. Как вас зовут? Вы можете пропустить это, если хотите.",
            'pt': "Obrigado. Qual é o seu nome? Você pode pular isso se preferir.",
            'ja': "ありがとう。お名前は何ですか？お好みでスキップできます。",
            'it': "Grazie. Qual è il tuo nome? Puoi saltare questo se preferisci.",
            'nl': "Bedankt. Wat is je naam? Je kunt dit overslaan als je wilt."
        }
        return responses.get(state['language'], responses['en'])
    
    def handle_name_response(self, user_input: str, state: Dict) -> str:
        """Handle name response"""
        if user_input.lower() not in ['skip', 'no', 'none', 'n/a', '']:
            state['user_info']['name'] = user_input.strip()
        
        state['step'] = 'collecting_age'
        
        responses = {
            'en': "What's your age?",
            'es': "¿Cuál es tu edad?",
            'fr': "Quel est votre âge?",
            'de': "Wie alt sind Sie?",
            'hi': "आपकी उम्र क्या है?",
            'ru': "Сколько вам лет?",
            'pt': "Qual é a sua idade?",
            'ja': "お年はいくつですか？",
            'it': "Quanti anni hai?",
            'nl': "Hoe oud ben je?"
        }
        return responses.get(state['language'], responses['en'])
    
    def handle_age_response(self, user_input: str, state: Dict) -> str:
        """Handle age response"""
        # Extract age from input
        age_match = re.search(r'\d+', user_input)
        if age_match:
            state['user_info']['age'] = int(age_match.group())
        
        state['step'] = 'collecting_income'
        
        responses = {
            'en': "What's your annual income in dollars?",
            'es': "¿Cuál es tu ingreso anual en dólares?",
            'fr': "Quel est votre revenu annuel en dollars?",
            'de': "Wie hoch ist Ihr Jahreseinkommen in Dollar?",
            'hi': "डॉलर में आपकी वार्षिक आय क्या है?",
            'ru': "Какой у вас годовой доход в долларах?",
            'pt': "Qual é a sua renda anual em dólares?",
            'ja': "ドルでの年間収入はいくらですか？",
            'it': "Qual è il tuo reddito annuo in dollari?",
            'nl': "Wat is je jaarlijkse inkomen in dollars?"
        }
        return responses.get(state['language'], responses['en'])
    
    def handle_income_response(self, user_input: str, state: Dict) -> str:
        """Handle income response and provide resources"""
        # Extract income from input
        income_match = re.search(r'\d+', user_input.replace(',', ''))
        if income_match:
            state['user_info']['income'] = int(income_match.group())
        
        state['step'] = 'providing_resources'
        
        # Generate resources based on need and location
        return self.generate_resources(state)
    
    def generate_resources(self, state: Dict) -> str:
        """Generate appropriate resources based on user profile"""
        need = state['need_type']
        location = state['user_info'].get('location', '')
        age = state['user_info'].get('age', 0)
        income = state['user_info'].get('income', 0)
        name = state['user_info'].get('name', '')
        language = state['language']
        
        # Build confirmation summary
        name_part = f", {name}" if name else ""
        summary = f"Thanks{name_part}. I have {location}, age {age}, and income ${income}. You said you need help with {need}. Let me share a few options near you."
        
        # Generate resources
        resources = []
        
        # Always include LIHEAP
        resources.append({
            'name': 'LIHEAP (Energy Bill Help)',
            'description': 'LIHEAP helps pay heating or cooling bills. Based on your ZIP and income, you may qualify. Apply through your state LIHEAP office—I can text the link.',
            'link': 'https://www.acf.hhs.gov/ocs/energy-assistance',
            'requirements': 'photo ID, proof of address, recent bill, income proof'
        })
        
        # Always include Housing Resources
        resources.append({
            'name': 'Housing Resources',
            'description': 'HUD helps people find rental and affordable housing in each state. You can search or apply on your state\'s HUD page.',
            'link': 'https://www.hud.gov/states'
        })
        
        # Always include Unclaimed Benefits Finder
        resources.append({
            'name': 'Unclaimed Benefits Finder',
            'description': 'This site checks for other programs—food, health, cash aid, or tax credits. It\'s quick and private.',
            'link': 'https://www.benefits.gov/benefit-finder'
        })
        
        # Format response
        response = summary + "\n\n"
        
        for i, resource in enumerate(resources, 1):
            response += f"{i}. {resource['name']} — {resource['description']}\n"
            if 'requirements' in resource:
                response += f"   Requirements: {resource['requirements']}\n"
            response += f"   Link: {resource['link']}\n\n"
        
        response += "Would you like me to text these links, or read them slowly?"
        
        return response
    
    def handle_resource_followup(self, user_input: str, state: Dict) -> str:
        """Handle follow-up questions about resources"""
        user_lower = user_input.lower()
        
        if any(word in user_lower for word in ['text', 'send', 'email', 'message']):
            return "May I send a text to this number? I'll send the links right away."
        elif any(word in user_lower for word in ['read', 'slow', 'repeat', 'again']):
            return "I'll read the URLs slowly. Here are the links: [reads URLs slowly] Would you like me to repeat any of them?"
        elif any(word in user_lower for word in ['person', 'human', 'speak', 'talk']):
            return "I can connect you to a local assistance line right now. Let me transfer you to speak with someone directly."
        else:
            return "Glad I could help today. You can call Bridge anytime for energy, housing, or benefit support. Take care."

# Initialize Anthony persona
anthony = AnthonyPersona()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "agent_available": resource_agent is not None
    })

@app.route('/retell/webhook', methods=['POST'])
def retell_webhook():
    """
    Retell AI webhook endpoint for handling voice calls
    This endpoint receives events from Retell AI and processes them
    """
    try:
        # Get the raw request data
        data = request.get_json()
        
        if not data:
            logger.warning("No JSON data received in webhook")
            return jsonify({"error": "No data received"}), 400
        
        # Log the incoming event
        logger.info(f"Received Retell webhook: {json.dumps(data, indent=2)}")
        
        # Extract event type
        event_type = data.get('event')
        
        if event_type == 'call_started':
            return handle_call_started(data)
        elif event_type == 'call_ended':
            return handle_call_ended(data)
        elif event_type == 'call_analyzed':
            return handle_call_analyzed(data)
        elif event_type == 'conversation_turn':
            return handle_conversation_turn(data)
        else:
            logger.warning(f"Unknown event type: {event_type}")
            return jsonify({"message": "Event received but not processed"}), 200
            
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return jsonify({"error": "Internal server error"}), 500

def handle_call_started(data):
    """Handle call started event"""
    call_id = data.get('call', {}).get('call_id')
    logger.info(f"Call started: {call_id}")
    
    return jsonify({
        "message": "Call started event received",
        "call_id": call_id
    })

def handle_call_ended(data):
    """Handle call ended event"""
    call_id = data.get('call', {}).get('call_id')
    logger.info(f"Call ended: {call_id}")
    
    return jsonify({
        "message": "Call ended event received",
        "call_id": call_id
    })

def handle_call_analyzed(data):
    """Handle call analyzed event"""
    call_id = data.get('call', {}).get('call_id')
    logger.info(f"Call analyzed: {call_id}")
    
    return jsonify({
        "message": "Call analyzed event received",
        "call_id": call_id
    })

def handle_conversation_turn(data):
    """Handle conversation turn - this is where we process user input and generate responses"""
    try:
        # Extract user input from the conversation turn
        user_input = data.get('transcript', '')
        call_id = data.get('call', {}).get('call_id', 'unknown')
        
        logger.info(f"Processing conversation turn for call {call_id}: {user_input}")
        
        if not user_input.strip():
            return jsonify({
                "response": "I didn't catch that. Could you please repeat what you said?",
                "end_call": False
            })
        
        # Process with Anthony persona
        try:
            # Get Anthony's response based on conversation state
            anthony_response = anthony.process_user_input(call_id, user_input)
            
            # Log the conversation turn
            logger.info(f"Anthony response: {anthony_response}")
            
            return jsonify({
                "response": anthony_response,
                "end_call": False
            })
            
        except Exception as e:
            logger.error(f"Error processing with Anthony persona: {e}")
            return jsonify({
                "response": "I'm sorry, I'm having trouble processing your request right now. Could you please try again?",
                "end_call": False
            })
            
    except Exception as e:
        logger.error(f"Error in conversation turn handler: {e}")
        return jsonify({
            "response": "I'm sorry, something went wrong. Could you please repeat your question?",
            "end_call": False
        })

# This function has been moved to utils.py and is now imported

@app.route('/retell/events', methods=['POST'])
def retell_events():
    """
    Alternative endpoint for Retell AI events
    Some configurations might use this endpoint
    """
    return retell_webhook()

@app.route('/test-agent', methods=['POST'])
def test_agent():
    """
    Test endpoint to verify Anthony persona is working
    """
    try:
        data = request.get_json()
        query = data.get('query', '')
        call_id = data.get('call_id', 'test-call-123')
        
        if not query:
            return jsonify({"error": "No query provided"}), 400
        
        # Test Anthony persona
        anthony_response = anthony.process_user_input(call_id, query)
        
        # Get current conversation state
        state = anthony.get_call_state(call_id)
        
        return jsonify({
            "query": query,
            "anthony_response": anthony_response,
            "conversation_state": state,
            "call_id": call_id
        })
        
    except Exception as e:
        logger.error(f"Error in test endpoint: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/test-anthony', methods=['POST'])
def test_anthony():
    """
    Test endpoint specifically for Anthony persona conversation flow
    """
    try:
        data = request.get_json()
        call_id = data.get('call_id', 'test-call-123')
        user_input = data.get('user_input', '')
        
        if not user_input:
            return jsonify({"error": "No user input provided"}), 400
        
        # Process with Anthony
        anthony_response = anthony.process_user_input(call_id, user_input)
        state = anthony.get_call_state(call_id)
        
        return jsonify({
            "user_input": user_input,
            "anthony_response": anthony_response,
            "conversation_step": state['step'],
            "user_info": state['user_info'],
            "language": state['language'],
            "need_type": state['need_type']
        })
        
    except Exception as e:
        logger.error(f"Error in Anthony test endpoint: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run the Flask app
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting Flask app on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
