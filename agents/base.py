from langchain_ollama import OllamaLLM
from crewai import Agent, Task, Crew
from config import settings
import os


def get_ollama_llm():
    """Get Ollama LLM instance configured from settings"""
    # Set a dummy OpenAI key to prevent CrewAI from complaining
    os.environ["OPENAI_API_KEY"] = "sk-dummy-key-not-used"
    
    return OllamaLLM(
        base_url=settings.ollama_base_url,
        model=settings.ollama_model,
        temperature=0.7
    )


def create_agent(role: str, goal: str, backstory: str, tools: list = None, verbose: bool = True) -> Agent:
    """
    Create a CrewAI agent with Ollama LLM
    
    Args:
        role: Agent's role description
        goal: Agent's goal
        backstory: Agent's backstory
        tools: List of tools available to the agent
        verbose: Whether to enable verbose output
        
    Returns:
        Configured Agent instance
    """
    llm = get_ollama_llm()
    
    return Agent(
        role=role,
        goal=goal,
        backstory=backstory,
        tools=tools or [],
        llm=llm,
        verbose=verbose,
        allow_delegation=False
    )
