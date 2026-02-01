"""
Report Scheduler API endpoints
"""

from fastapi import APIRouter, HTTPException
from services.report_scheduler import report_scheduler

router = APIRouter(prefix="/api/v1/report-scheduler", tags=["report-scheduler"])


@router.post("/start")
async def start_scheduler():
    """
    Start the daily report scheduler
    
    Requirements: 4.1
    """
    try:
        report_scheduler.start()
        return {
            "status": "started",
            "message": "Report scheduler started. Reports will be generated daily at 8 PM"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error starting scheduler: {str(e)}"
        )


@router.post("/stop")
async def stop_scheduler():
    """
    Stop the daily report scheduler
    """
    try:
        report_scheduler.stop()
        return {
            "status": "stopped",
            "message": "Report scheduler stopped"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error stopping scheduler: {str(e)}"
        )


@router.get("/status")
async def get_scheduler_status():
    """
    Get scheduler status
    """
    try:
        status = report_scheduler.get_status()
        return status
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting scheduler status: {str(e)}"
        )


@router.post("/force-run")
async def force_run_scheduler():
    """
    Force immediate execution of report generation
    """
    try:
        report_scheduler.force_run()
        return {
            "status": "completed",
            "message": "Report generation completed"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error running reports: {str(e)}"
        )
