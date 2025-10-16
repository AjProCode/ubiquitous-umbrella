"""Configuration management"""

import os
from typing import Any, Optional
from pathlib import Path
from dotenv import load_dotenv


class Config:
    """Application configuration"""
    
    def __init__(self, env_file: Optional[str] = None):
        """
        Initialize configuration
        
        Args:
            env_file: Path to .env file (uses .env in root if not specified)
        """
        if env_file:
            load_dotenv(env_file)
        else:
            load_dotenv()
        
        self.openai_api_key = os.getenv('OPENAI_API_KEY', '')
        self.database_url = os.getenv('DATABASE_URL', 'sqlite:///products.db')
        self.enable_notifications = os.getenv('ENABLE_NOTIFICATIONS', 'true').lower() == 'true'
        self.notification_lead_time_days = int(os.getenv('NOTIFICATION_LEAD_TIME_DAYS', '7'))
        self.manufacturing_log_path = os.getenv('MANUFACTURING_LOG_PATH', './data/manufacturing_logs')
        self.verification_strict_mode = os.getenv('VERIFICATION_STRICT_MODE', 'true').lower() == 'true'
        self.medicine_interaction_check = os.getenv('MEDICINE_INTERACTION_CHECK', 'true').lower() == 'true'
        self.dosage_tracking = os.getenv('DOSAGE_TRACKING', 'true').lower() == 'true'
        self.enable_recipe_suggestions = os.getenv('ENABLE_RECIPE_SUGGESTIONS', 'true').lower() == 'true'
        self.recipe_complexity = os.getenv('RECIPE_COMPLEXITY', 'medium')
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return getattr(self, key, default)
    
    def set(self, key: str, value: Any):
        """Set configuration value"""
        setattr(self, key, value)
    
    def __repr__(self) -> str:
        """String representation"""
        config_items = {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
        # Hide sensitive data
        if 'openai_api_key' in config_items and config_items['openai_api_key']:
            config_items['openai_api_key'] = '***hidden***'
        return f"Config({config_items})"
