from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application configuration settings"""
    
    # ChromaDB (embedded, no setup needed!)
    chroma_persist_directory: str = "./chroma_data"
    
    # Redis (optional)
    redis_url: str = "redis://localhost:6379/0"
    
    # Ollama (Local LLM)
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.1:8b"
    
    # Application
    app_env: str = "development"
    debug: bool = True
    log_level: str = "INFO"
    
    # Math Engine Constants
    default_fuel_consumption_rate: float = 0.35
    default_fuel_price: float = 1.50
    default_driver_hourly_rate: float = 25.0
    average_truck_speed: float = 60.0
    max_route_deviation_km: float = 500.0  # Increased to 500km for better matching
    distance_accuracy_tolerance: float = 0.05
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"


settings = Settings()
