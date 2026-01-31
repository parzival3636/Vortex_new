"""
Test Ollama Integration
Run this to verify Ollama is working correctly
"""

import requests
import json
from langchain_community.llms import Ollama
from config import settings


def test_ollama_direct():
    """Test Ollama API directly"""
    print("\n" + "="*60)
    print("TEST 1: Ollama Direct API")
    print("="*60)
    
    try:
        # Check if Ollama is running
        response = requests.get(f"{settings.ollama_base_url}/api/tags")
        
        if response.status_code == 200:
            models = response.json().get("models", [])
            print(f"✅ Ollama is running at {settings.ollama_base_url}")
            print(f"✅ Available models: {len(models)}")
            for model in models:
                print(f"   - {model['name']}")
            return True
        else:
            print(f"❌ Ollama returned status code: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to Ollama at {settings.ollama_base_url}")
        print("   Make sure Ollama is running: ollama serve")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_ollama_model():
    """Test if the configured model exists"""
    print("\n" + "="*60)
    print("TEST 2: Check Model Availability")
    print("="*60)
    
    try:
        response = requests.get(f"{settings.ollama_base_url}/api/tags")
        models = response.json().get("models", [])
        model_names = [m["name"] for m in models]
        
        if settings.ollama_model in model_names:
            print(f"✅ Model '{settings.ollama_model}' is available")
            return True
        else:
            print(f"❌ Model '{settings.ollama_model}' not found")
            print(f"   Available models: {', '.join(model_names)}")
            print(f"   Run: ollama pull {settings.ollama_model}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_ollama_generation():
    """Test Ollama text generation"""
    print("\n" + "="*60)
    print("TEST 3: Ollama Text Generation")
    print("="*60)
    
    try:
        payload = {
            "model": settings.ollama_model,
            "prompt": "What is 2+2? Answer in one sentence.",
            "stream": False
        }
        
        print(f"Sending prompt to {settings.ollama_model}...")
        response = requests.post(
            f"{settings.ollama_base_url}/api/generate",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            answer = result.get("response", "")
            print(f"✅ Response received:")
            print(f"   {answer[:200]}...")
            return True
        else:
            print(f"❌ Generation failed with status: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out (model might be loading)")
        print("   Try again in a few seconds")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_langchain_ollama():
    """Test Ollama through LangChain"""
    print("\n" + "="*60)
    print("TEST 4: LangChain Ollama Integration")
    print("="*60)
    
    try:
        llm = Ollama(
            base_url=settings.ollama_base_url,
            model=settings.ollama_model,
            temperature=0.7
        )
        
        print("Invoking LLM through LangChain...")
        response = llm.invoke("What is the capital of France? Answer in one word.")
        
        print(f"✅ LangChain integration working")
        print(f"   Response: {response[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_agent_tools():
    """Test if agent tools can be created"""
    print("\n" + "="*60)
    print("TEST 5: Agent Tools Creation")
    print("="*60)
    
    try:
        from agents.load_matcher import calculate_route_deviation_tool
        
        # Test the tool
        deviation = calculate_route_deviation_tool(
            driver_lat=28.6139,
            driver_lng=77.2090,
            driver_dest_lat=28.7041,
            driver_dest_lng=77.1025,
            vendor_lat=28.6517,
            vendor_lng=77.2219
        )
        
        print(f"✅ Agent tools working")
        print(f"   Route deviation calculated: {deviation} km")
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_agent_creation():
    """Test if agents can be created"""
    print("\n" + "="*60)
    print("TEST 6: Agent Creation")
    print("="*60)
    
    try:
        from agents.load_matcher import load_matcher_agent
        
        print(f"✅ Load Matcher Agent created successfully")
        print(f"   Role: {load_matcher_agent.agent.role}")
        return True
        
    except Exception as e:
        print(f"❌ Error creating agent: {str(e)}")
        print("   This might be due to Ollama not running or model not available")
        return False


def run_all_tests():
    """Run all Ollama tests"""
    print("\n" + "="*60)
    print("OLLAMA INTEGRATION TESTS")
    print("="*60)
    print(f"Ollama URL: {settings.ollama_base_url}")
    print(f"Model: {settings.ollama_model}")
    print("="*60)
    
    tests = [
        ("Ollama Direct API", test_ollama_direct),
        ("Model Availability", test_ollama_model),
        ("Text Generation", test_ollama_generation),
        ("LangChain Integration", test_langchain_ollama),
        ("Agent Tools", test_agent_tools),
        ("Agent Creation", test_agent_creation),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ EXCEPTION in {name}: {str(e)}\n")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    for name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {name}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\nTotal: {passed}/{total} tests passed")
    print("="*60)
    
    if passed < total:
        print("\n⚠️  TROUBLESHOOTING TIPS:")
        print("1. Make sure Ollama is running: ollama serve")
        print("2. Check if model is installed: ollama list")
        print(f"3. Pull model if missing: ollama pull {settings.ollama_model}")
        print("4. Verify Ollama URL in .env file")
        print("5. Restart Ollama service if needed")
    else:
        print("\n🎉 All tests passed! Ollama is working correctly!")
    
    print("="*60 + "\n")


if __name__ == "__main__":
    run_all_tests()
