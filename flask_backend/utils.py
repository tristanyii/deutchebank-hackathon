"""
Utility functions for the Flask backend
"""

import re
import logging
from typing import str

logger = logging.getLogger(__name__)

def clean_text_for_voice(text: str) -> str:
    """
    Clean and format text for natural voice output
    """
    if not text:
        return "I'm sorry, I couldn't find any specific resources for your request."
    
    # Remove markdown formatting
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Remove bold
    text = re.sub(r'\*(.*?)\*', r'\1', text)     # Remove italic
    text = re.sub(r'`(.*?)`', r'\1', text)       # Remove code formatting
    
    # Replace line breaks with natural pauses
    text = re.sub(r'\n+', '. ', text)
    text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
    
    # Clean up punctuation
    text = re.sub(r'\.\s*\.', '.', text)  # Remove double periods
    text = re.sub(r'\s+([.!?])', r'\1', text)  # Remove spaces before punctuation
    
    return text.strip()

def format_resource_response(response: str) -> str:
    """
    Format the agent's response specifically for voice output
    """
    if not response:
        return "I'm sorry, I couldn't find any specific resources for your request."
    
    # Clean the text
    voice_response = clean_text_for_voice(response)
    
    # Add natural speech patterns
    if voice_response.startswith('Government and Community Resources'):
        voice_response = "Here are some government and community resources that might help you. " + voice_response[35:]
    elif voice_response.startswith('Available Nonprofit and Community Resources'):
        voice_response = "Here are some nonprofit and community resources available. " + voice_response[44:]
    elif voice_response.startswith('**'):
        # Remove any remaining markdown and add natural intro
        voice_response = "Here's what I found for you. " + voice_response
    
    return voice_response

def truncate_for_voice(text: str, max_length: int = 500, max_sentences: int = 3) -> str:
    """
    Truncate text to be appropriate for voice output
    """
    if len(text) <= max_length:
        return text
    
    # Try to break at sentence boundaries
    sentences = text.split('. ')
    if len(sentences) > max_sentences:
        truncated = '. '.join(sentences[:max_sentences])
        if len(truncated) < len(text):
            truncated += ". Would you like me to provide more specific information about any of these resources?"
        return truncated
    
    # If still too long, truncate at word boundary
    words = text.split()
    truncated_words = []
    current_length = 0
    
    for word in words:
        if current_length + len(word) + 1 > max_length:
            break
        truncated_words.append(word)
        current_length += len(word) + 1
    
    if truncated_words:
        truncated = ' '.join(truncated_words)
        if len(truncated) < len(text):
            truncated += "... Would you like me to provide more details?"
        return truncated
    
    return text[:max_length] + "..."

def extract_user_intent(text: str) -> dict:
    """
    Extract user intent from the transcribed text
    """
    text_lower = text.lower()
    
    intent = {
        'category': 'general',
        'urgency': 'normal',
        'specific_need': None
    }
    
    # Category detection
    if any(word in text_lower for word in ['housing', 'rent', 'apartment', 'home']):
        intent['category'] = 'housing'
    elif any(word in text_lower for word in ['food', 'hungry', 'meal', 'nutrition']):
        intent['category'] = 'food'
    elif any(word in text_lower for word in ['health', 'medical', 'doctor', 'healthcare']):
        intent['category'] = 'healthcare'
    elif any(word in text_lower for word in ['job', 'work', 'employment', 'unemployed']):
        intent['category'] = 'employment'
    elif any(word in text_lower for word in ['money', 'financial', 'bills', 'debt']):
        intent['category'] = 'financial'
    
    # Urgency detection
    if any(word in text_lower for word in ['urgent', 'emergency', 'immediately', 'asap', 'right now']):
        intent['urgency'] = 'high'
    elif any(word in text_lower for word in ['soon', 'quickly', 'fast']):
        intent['urgency'] = 'medium'
    
    return intent

def log_conversation_turn(call_id: str, user_input: str, agent_response: str, voice_response: str):
    """
    Log conversation turn for debugging and analytics
    """
    logger.info(f"Conversation Turn - Call ID: {call_id}")
    logger.info(f"User Input: {user_input}")
    logger.info(f"Agent Response: {agent_response[:200]}...")
    logger.info(f"Voice Response: {voice_response[:200]}...")
    logger.info("-" * 50)
