"""
Test Groq Integration
Run this to verify Groq is working correctly
"""

from langchain_groq import ChatGroq
from config import settings

print("\n" + "="*60)
print("GROQ INTEGRATION TEST")
print("="*60)
print(f"API Key: {settings.groq_api_key[:20]}...")
print(f"Model: {settings.groq_model}")
print("="*60)

try:
    print("\nInitializing Groq LLM...")
    llm = ChatGroq(
        api_key=settings.groq_api_key,
        model=settings.groq_model,
        temperature=0.7
    )
    print("✅ Groq LLM initialized successfully!")
    
    print("\nTesting text generation...")
    response = llm.invoke("What is 2+2? Answer in one short sentence.")
    print(f"✅ Response: {response.content}")
    
    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED!")
    print("="*60)
    
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
    print("\nTroubleshooting:")
    print("1. Check if GROQ_API_KEY is set in .env")
    print("2. Verify API key is valid")
    print("3. Check internet connection")
