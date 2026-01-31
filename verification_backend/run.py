"""
Simple runner script for verification backend
Run this from the verification_backend directory
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now import and run
from verification_backend.main_verification import app

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting QR Verification Backend...")
    print("📍 Server: http://localhost:8001")
    print("📚 API Docs: http://localhost:8001/docs")
    print("❤️  Health: http://localhost:8001/health")
    print("\nPress CTRL+C to stop\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8001)
