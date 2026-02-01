from langchain_groq import ChatGroq
from config import settings
import os


_groq_llm_instance = None


def get_groq_llm():
    """Get Groq LLM instance configured from settings (singleton pattern)"""
    global _groq_llm_instance
    if _groq_llm_instance is None:
        _groq_llm_instance = ChatGroq(
            api_key=settings.groq_api_key,
            model=settings.groq_model,
            temperature=0.7
        )
    return _groq_llm_instance


# For backward compatibility with CrewAI agents
def create_agent(role: str, goal: str, backstory: str, tools: list = None, verbose: bool = True):
    """
    Simplified agent creation - returns LLM directly
    CrewAI agents are optional for this system
    
    Args:
        role: Agent's role description
        goal: Agent's goal
        backstory: Agent's backstory
        tools: List of tools available to the agent
        verbose: Whether to enable verbose output
        
    Returns:
        Groq LLM instance (lazy loaded)
    """
    # Return None for now - agents will be initialized when first used
    # This prevents initialization errors at import time
    return None
