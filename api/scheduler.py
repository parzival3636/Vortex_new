"""
Auto-Scheduler API Endpoints
Control and monitor the AI-powered auto-scheduler
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Dict

from services.auto_scheduler import auto_scheduler

router = APIRouter(prefix="/api/v1/scheduler", tags=["scheduler"])


class SchedulerStatus(BaseModel):
    """Scheduler status response"""
    running: bool
    interval_seconds: int
    total_runs: int
    total_matches: int
    total_assignments: int
    last_run_time: str = None
    last_run_matches: int


@router.post("/start")
def start_scheduler():
    """
    Start the auto-scheduler
    
    The scheduler will run every 2 minutes to:
    1. Find active trips (deadheading drivers)
    2. Get available loads
    3. Use Math Engine to calculate profitability
    4. Use AI Agents to find optimal matches
    5. Auto-assign best load to each driver
    """
    try:
        auto_scheduler.start()
        return {
            "message": "Auto-scheduler started",
            "interval_seconds": auto_scheduler.interval_seconds,
            "status": "running"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start scheduler: {str(e)}"
        )


@router.post("/stop")
def stop_scheduler():
    """Stop the auto-scheduler"""
    try:
        auto_scheduler.stop()
        return {
            "message": "Auto-scheduler stopped",
            "status": "stopped"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to stop scheduler: {str(e)}"
        )


@router.get("/status")
def get_scheduler_status():
    """Get current scheduler status and statistics"""
    stats = auto_scheduler.get_stats()
    
    return {
        "running": stats['running'],
        "interval_seconds": stats['interval_seconds'],
        "total_runs": stats['total_runs'],
        "total_matches": stats['total_matches'],
        "total_assignments": stats['total_assignments'],
        "last_run_time": stats['last_run_time'] or "",
        "last_run_matches": stats['last_run_matches']
    }


@router.post("/force-run")
def force_scheduler_run():
    """
    Force an immediate scheduling cycle (for testing)
    
    This will run the scheduler immediately without waiting for the interval.
    Useful for testing and demonstrations.
    """
    try:
        auto_scheduler.force_run()
        return {
            "message": "Scheduling cycle completed",
            "stats": auto_scheduler.get_stats()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to run scheduler: {str(e)}"
        )


@router.get("/stats")
def get_scheduler_stats():
    """Get detailed scheduler statistics"""
    return auto_scheduler.get_stats()
