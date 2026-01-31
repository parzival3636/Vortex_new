"""
Main FastAPI application for QR Verification System
Separate backend for vendor and receiver verification workflows
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

try:
    from verification_backend.api import qr_verification, receivers
except ImportError:
    from api import qr_verification, receivers

app = FastAPI(
    title="Load Verification System",
    description="QR-based verification system for load pickup and delivery with AI agents",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(qr_verification.router)
app.include_router(receivers.router)


@app.get("/")
def root():
    return {
        "service": "Load Verification System",
        "version": "1.0.0",
        "description": "QR-based verification with AI agents for pickup and delivery",
        "endpoints": {
            "qr_verification": "/api/v1/qr",
            "receivers": "/api/v1/receivers",
            "docs": "/docs"
        }
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "verification_backend",
        "ai_agents": {
            "verification_agent": "active",
            "notification_agent": "active"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
