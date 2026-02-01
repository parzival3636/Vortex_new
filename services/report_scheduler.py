"""
Report Scheduler Service for Daily Financial Report feature
Handles automated report generation at 8 PM daily
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import logging
from typing import List
from db_chromadb import db
from services.report_generation import ReportGenerationService
import uuid

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ReportScheduler:
    """Scheduler for automated daily report generation"""
    
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.is_running = False
        self.report_service = ReportGenerationService()
    
    def start(self):
        """Start the scheduler"""
        if self.is_running:
            logger.warning("Scheduler is already running")
            return
        
        # Schedule report generation at 8 PM (20:00) every day
        self.scheduler.add_job(
            self._generate_daily_reports,
            CronTrigger(hour=20, minute=0),
            id='daily_report_generation',
            name='Daily Report Generation at 8 PM',
            replace_existing=True
        )
        
        self.scheduler.start()
        self.is_running = True
        logger.info("Report scheduler started. Reports will be generated daily at 8 PM")
    
    def stop(self):
        """Stop the scheduler"""
        if not self.is_running:
            logger.warning("Scheduler is not running")
            return
        
        self.scheduler.shutdown()
        self.is_running = False
        logger.info("Report scheduler stopped")
    
    def _generate_daily_reports(self):
        """Generate daily reports for all active drivers"""
        try:
            logger.info("Starting daily report generation...")
            
            # Get all drivers
            drivers = self._get_all_drivers()
            
            if not drivers:
                logger.info("No drivers found for report generation")
                return
            
            today = datetime.utcnow().strftime("%Y-%m-%d")
            
            for driver in drivers:
                try:
                    driver_id = driver.get('driver_id')
                    logger.info(f"Generating report for driver {driver_id}...")
                    
                    # Generate report
                    report = self.report_service.generate_daily_report(driver_id, today)
                    
                    # Store report in ChromaDB
                    report_id = str(uuid.uuid4())
                    import json
                    report_record = {
                        "report_id": report_id,
                        "driver_id": driver_id,
                        "date": today,
                        "generated_at": datetime.utcnow().isoformat(),
                        "trips": json.dumps(report['trips']),
                        "financial_summary": json.dumps(report['financial_summary']),
                        "ai_insights": json.dumps(report['ai_insights']),
                        "source": "automated_scheduler",
                        "version": 1
                    }
                    
                    db.reports.add(
                        ids=[report_id],
                        documents=[f"Report for {driver_id} on {today}"],
                        metadatas=[report_record]
                    )
                    
                    logger.info(f"Report generated successfully for driver {driver_id}: {report_id}")
                
                except Exception as e:
                    logger.error(f"Error generating report for driver {driver_id}: {str(e)}")
                    # Continue with next driver on error
                    continue
            
            logger.info("Daily report generation completed")
        
        except Exception as e:
            logger.error(f"Error in daily report generation: {str(e)}")
    
    def _get_all_drivers(self) -> List[dict]:
        """Get all active drivers from database"""
        try:
            result = db.drivers.get()
            
            if not result['ids']:
                return []
            
            return result['metadatas']
        
        except Exception as e:
            logger.error(f"Error retrieving drivers: {str(e)}")
            return []
    
    def force_run(self):
        """Force immediate execution of report generation"""
        try:
            logger.info("Force running daily report generation...")
            self._generate_daily_reports()
            logger.info("Force run completed")
        except Exception as e:
            logger.error(f"Error in force run: {str(e)}")
    
    def get_status(self) -> dict:
        """Get scheduler status"""
        return {
            "is_running": self.is_running,
            "next_run_time": str(self.scheduler.get_job('daily_report_generation').next_run_time) if self.is_running else None,
            "jobs": [
                {
                    "id": job.id,
                    "name": job.name,
                    "next_run_time": str(job.next_run_time)
                }
                for job in self.scheduler.get_jobs()
            ] if self.is_running else []
        }


# Global scheduler instance
report_scheduler = ReportScheduler()
