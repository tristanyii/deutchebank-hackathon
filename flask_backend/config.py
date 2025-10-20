"""
Configuration settings for the Flask backend
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

class Config:
    """Base configuration class"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    # Server settings
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    
    # Retell AI settings
    RETELL_WEBHOOK_SECRET = os.environ.get('RETELL_WEBHOOK_SECRET', '')
    RETELL_API_KEY = os.environ.get('RETELL_API_KEY', '')
    
    # Agent settings
    MAX_RESPONSE_LENGTH = int(os.environ.get('MAX_RESPONSE_LENGTH', 500))
    ENABLE_AGENT_LOGGING = os.environ.get('ENABLE_AGENT_LOGGING', 'True').lower() == 'true'
    
    # Voice settings
    VOICE_RESPONSE_PAUSE = os.environ.get('VOICE_RESPONSE_PAUSE', '. ')
    MAX_VOICE_SENTENCES = int(os.environ.get('MAX_VOICE_SENTENCES', 3))

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    ENABLE_AGENT_LOGGING = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    ENABLE_AGENT_LOGGING = False

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
