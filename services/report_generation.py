"""
Report Generation Service for Daily Financial Report feature
"""

from datetime import datetime
from typing import Dict, List
from services.calculation_engine import CalculationEngine
from services.ai_insights import AIInsightGenerator


class ReportGenerationService:
    """Service for generating daily financial reports"""
    
    def __init__(self):
        self.calculation_engine = CalculationEngine()
        self.ai_generator = AIInsightGenerator()
    
    def generate_daily_report(self, driver_id: str, date_str: str) -> Dict:
        """
        Generate a comprehensive daily financial report
        
        Requirements: 4.2, 4.3, 4.4, 4.5, 4.6, 4.7
        """
        # Get trips for the day
        trips = self.calculation_engine.get_daily_trips(driver_id, date_str)
        
        # Calculate financial metrics
        total_earnings = self.calculation_engine.calculate_daily_earnings(driver_id, date_str)
        total_expenses = self.calculation_engine.calculate_daily_expenses(driver_id, date_str)
        net_profit = self.calculation_engine.calculate_net_profit(driver_id, date_str)
        expense_breakdown = self.calculation_engine.get_expense_breakdown(driver_id, date_str)
        performance_metrics = self.calculation_engine.calculate_performance_metrics(driver_id, date_str)
        
        # Generate AI insights
        ai_insights = self.ai_generator.generate_insights(
            driver_id=driver_id,
            date=date_str,
            trips=trips,
            total_earnings=total_earnings,
            total_expenses=total_expenses,
            expense_breakdown=expense_breakdown
        )
        
        # Compile report
        report = {
            "trips": trips,
            "financial_summary": {
                "total_earnings": round(total_earnings, 2),
                "total_expenses": round(total_expenses, 2),
                "net_profit": round(net_profit, 2),
                "expense_breakdown": {k: round(v, 2) for k, v in expense_breakdown.items()},
                "trips_completed": performance_metrics["trips_completed"],
                "average_earnings_per_trip": performance_metrics["average_earnings_per_trip"],
                "expense_ratio": performance_metrics["expense_ratio"]
            },
            "ai_insights": ai_insights
        }
        
        return report
