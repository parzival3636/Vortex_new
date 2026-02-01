from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from api import trips, loads, calculate, vendors, demo, scheduler, financial_reports, report_scheduler, allocations

app = FastAPI(
    title="Deadheading Optimization System",
    description="AI-powered system to eliminate empty return trips for trucks using Groq LLM",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(trips.router)
app.include_router(loads.router)
app.include_router(calculate.router)
app.include_router(vendors.router)
app.include_router(demo.router)
app.include_router(scheduler.router)
app.include_router(financial_reports.router)
app.include_router(report_scheduler.router)
app.include_router(allocations.router)


@app.get("/")
async def root():
    return {
        "message": "Deadheading Optimization System API",
        "version": "1.0.0",
        "status": "running",
        "llm": f"Groq ({settings.groq_model})"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
