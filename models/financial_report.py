"""
Data models for Daily Financial Report feature
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict
from uuid import UUID


class Expense(BaseModel):
    """Expense record model"""
    expense_id: str = Field(..., description="Unique expense ID")
    driver_id: str = Field(..., description="Driver ID")
    amount: float = Field(..., gt=0, description="Expense amount (must be positive)")
    category: str = Field(..., description="Expense category: fuel, maintenance, toll, food, other")
    description: str = Field(..., min_length=1, description="Expense description")
    trip_id: Optional[str] = Field(None, description="Associated trip ID")
    timestamp: str = Field(..., description="ISO8601 timestamp when expense was recorded")
    created_at: str = Field(..., description="ISO8601 timestamp when record was created")
    
    class Config:
        json_schema_extra = {
            "example": {
                "expense_id": "550e8400-e29b-41d4-a716-446655440000",
                "driver_id": "driver-123",
                "amount": 500.00,
                "category": "fuel",
                "description": "Diesel fuel at pump",
                "trip_id": "trip-456",
                "timestamp": "2024-01-15T10:30:00Z",
                "created_at": "2024-01-15T10:30:01Z"
            }
        }


class ExpenseCreate(BaseModel):
    """Request model for creating an expense"""
    driver_id: str = Field(..., description="Driver ID")
    amount: float = Field(..., gt=0, description="Expense amount (must be positive)")
    category: str = Field(..., description="Expense category: fuel, maintenance, toll, food, other")
    description: str = Field(..., min_length=1, description="Expense description")
    trip_id: Optional[str] = Field(None, description="Associated trip ID (optional)")
    timestamp: Optional[str] = Field(None, description="ISO8601 timestamp (auto-generated if not provided)")


class ExpenseResponse(BaseModel):
    """Response model for expense data"""
    expense_id: str
    driver_id: str
    amount: float
    category: str
    description: str
    trip_id: Optional[str]
    timestamp: str
    created_at: str


class DailyExpenseSummary(BaseModel):
    """Daily expense summary"""
    date: str = Field(..., description="Date in YYYY-MM-DD format")
    total_expenses: float = Field(..., ge=0, description="Total expenses for the day")
    expense_breakdown: Dict[str, float] = Field(..., description="Breakdown by category")
    expenses: List[ExpenseResponse] = Field(..., description="List of all expenses")


class FinancialMetrics(BaseModel):
    """Financial metrics for a day"""
    total_earnings: float = Field(..., ge=0, description="Total earnings from trips")
    total_expenses: float = Field(..., ge=0, description="Total expenses")
    net_profit: float = Field(..., description="Net profit (earnings - expenses)")
    expense_breakdown: Dict[str, float] = Field(..., description="Breakdown by category")
    trips_completed: int = Field(..., ge=0, description="Number of trips completed")
    average_earnings_per_trip: float = Field(..., ge=0, description="Average earnings per trip")
    expense_ratio: float = Field(..., ge=0, le=1, description="Expense ratio (expenses/earnings)")


class TripDetail(BaseModel):
    """Trip detail for report"""
    trip_id: str = Field(..., description="Trip ID")
    origin: str = Field(..., description="Trip origin address")
    destination: str = Field(..., description="Trip destination address")
    load_details: str = Field(..., description="Load details")
    earnings: float = Field(..., ge=0, description="Trip earnings")


class AIInsights(BaseModel):
    """AI-generated insights"""
    summary: str = Field(..., description="Summary of daily performance")
    anomalies: List[str] = Field(..., description="List of detected anomalies")
    recommendations: List[str] = Field(..., description="List of recommendations")


class DailyReport(BaseModel):
    """Daily financial report"""
    report_id: str = Field(..., description="Unique report ID")
    driver_id: str = Field(..., description="Driver ID")
    date: str = Field(..., description="Report date in YYYY-MM-DD format")
    generated_at: str = Field(..., description="ISO8601 timestamp when report was generated")
    trips: List[TripDetail] = Field(..., description="List of trips completed")
    financial_summary: FinancialMetrics = Field(..., description="Financial metrics")
    ai_insights: AIInsights = Field(..., description="AI-generated insights")
    
    class Config:
        json_schema_extra = {
            "example": {
                "report_id": "report-123",
                "driver_id": "driver-456",
                "date": "2024-01-15",
                "generated_at": "2024-01-15T20:00:00Z",
                "trips": [
                    {
                        "trip_id": "trip-1",
                        "origin": "Mumbai",
                        "destination": "Pune",
                        "load_details": "Electronics",
                        "earnings": 2000.00
                    }
                ],
                "financial_summary": {
                    "total_earnings": 2000.00,
                    "total_expenses": 500.00,
                    "net_profit": 1500.00,
                    "expense_breakdown": {
                        "fuel": 300.00,
                        "maintenance": 100.00,
                        "toll": 100.00,
                        "food": 0.00,
                        "other": 0.00
                    },
                    "trips_completed": 1,
                    "average_earnings_per_trip": 2000.00,
                    "expense_ratio": 0.25
                },
                "ai_insights": {
                    "summary": "Good day with solid earnings",
                    "anomalies": [],
                    "recommendations": ["Consider fuel optimization"]
                }
            }
        }


class ReportGenerateRequest(BaseModel):
    """Request to generate a report"""
    driver_id: str = Field(..., description="Driver ID")
    date: Optional[str] = Field(None, description="Report date (YYYY-MM-DD, defaults to today)")


class ReportGenerateResponse(BaseModel):
    """Response for report generation"""
    report_id: str = Field(..., description="Generated report ID")
    status: str = Field(..., description="Generation status")
    message: Optional[str] = Field(None, description="Status message")
