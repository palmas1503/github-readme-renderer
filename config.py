"""
Application configuration module
Manages environment variables and application settings
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration"""
    
    # Flask settings
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    FLASK_DEBUG = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    PORT = int(os.getenv("PORT", 5000))
    
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    
    # Model Names
    GPT_MODEL = os.getenv("GPT_MODEL", "gpt-3.5-turbo")
    DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    
    # SSL Settings
    USE_SSL = os.getenv("USE_SSL", "False").lower() == "true"
    
    # API Endpoints
    OPENAI_ENDPOINT = "https://api.openai.com/v1/chat/completions"
    DEEPSEEK_ENDPOINT = "https://api.deepseek.com/chat/completions"
    
    # Timeouts
    API_TIMEOUT = 30.0
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def validate(cls):
        """Validate configuration"""
        if not cls.OPENAI_API_KEY and not cls.DEEPSEEK_API_KEY:
            raise ValueError(
                "At least one API key (OPENAI_API_KEY or DEEPSEEK_API_KEY) must be configured"
            )
        
        print(f"✓ Configuration loaded: {cls.FLASK_ENV} mode on port {cls.PORT}")


config = Config()
