import toml
import json
import os
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

SETTINGS_FILE = "config.toml"
LEGACY_SETTINGS_FILE = "settings.json"

class AppSettings(BaseModel):
    """应用全局配置"""
    base_url: str = Field("https://api.openai.com/v1", description="OpenAPI Base URL")
    api_key: str = Field("", description="API Key")
    model_name: str = Field("gpt-5", description="Model Name")
    language: str = Field("curl", description="Default Language")
    debug_mode: bool = Field(False, description="Enable Debug Mode to log node outputs")
    debug_log_path: str = Field("debug.log", description="Path to debug log file")

class SettingsManager:
    """配置及持久化管理器"""

    @staticmethod
    def load_settings() -> AppSettings:
        # Check for legacy JSON if TOML doesn't exist
        if not os.path.exists(SETTINGS_FILE):
             if os.path.exists(LEGACY_SETTINGS_FILE):
                 print(f"Migrating legacy settings from {LEGACY_SETTINGS_FILE} to {SETTINGS_FILE}")
                 try:
                     with open(LEGACY_SETTINGS_FILE, "r", encoding="utf-8") as f:
                         data = json.load(f)
                     settings = AppSettings(**data)
                     SettingsManager.save_settings(settings)
                     return settings
                 except Exception as e:
                     print(f"Error migrating settings: {e}")
             return AppSettings()
        
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = toml.load(f)
            return AppSettings(**data)
        except Exception as e:
            print(f"Error loading settings: {e}")
            return AppSettings()

    @staticmethod
    def save_settings(settings: AppSettings):
        try:
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                # model_dump() returns dict, suitable for toml.dump
                toml.dump(settings.model_dump(), f)
        except Exception as e:
            print(f"Error saving settings: {e}")
