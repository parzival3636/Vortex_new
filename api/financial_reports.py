"""
Financial Reports API endpoints for Daily Financial Report feature
"""

from fastapi import APIRouter, HTTPException, Query
from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, Field
import uuid
import json

from db_chromadb import db
from services.calculation_engine import CalculationEngine
from services.report_generation import ReportGenerationService

router = APIRouter(prefix="/api/v1/financial", tags=["financial"])

# ==================== MODELS ====================

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
    date: str
    total_expenses: float
    expense_breakdown: dict
    expenses: List[ExpenseResponse]


class FinancialMetrics(BaseModel):
    """Financial metrics for a day"""
    total_earnings: float
    total_expenses: float
    net_profit: float
    expense_breakdown: dict
    trips_completed: int
    average_earnings_per_trip: float
    expense_ratio: float


class TripDetail(BaseModel):
    """Trip detail for report"""
    trip_id: str
    origin: str
    destination: str
    load_details: str
    earnings: float


class AIInsights(BaseModel):
    """AI-generated insights"""
    summary: str
    anomalies: List[str]
    recommendations: List[str]


class DailyReport(BaseModel):
    """Daily financial report"""
    report_id: str
    driver_id: str
    date: str
    generated_at: str
    trips: List[TripDetail]
    financial_summary: FinancialMetrics
    ai_insights: AIInsights


class ReportGenerateRequest(BaseModel):
    """Request to generate a report"""
    driver_id: str = Field(..., description="Driver ID")
    date: Optional[str] = Field(None, description="Report date (YYYY-MM-DD, defaults to today)")


# ==================== VALIDATION ====================

VALID_CATEGORIES = {"fuel", "maintenance", "toll", "food", "other"}


def validate_expense_category(category: str) -> bool:
    """Validate expense category"""
    return category.lower() in VALID_CATEGORIES


def validate_expense_amount(amount: float) -> bool:
    """Validate expense amount"""
    return amount > 0


# ==================== ENDPOINTS ====================

@router.post("/expenses", response_model=ExpenseResponse, status_code=201)
async def create_expense(expense: ExpenseCreate):
    """
    Create a new expense record
    
    Requirements: 1.3, 9.1, 9.5, 9.6
    """
    # Validate category
    if not validate_expense_category(expense.category):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid category. Must be one of: {', '.join(VALID_CATEGORIES)}"
        )
    
    # Validate amount
    if not validate_expense_amount(expense.amount):
        raise HTTPException(
            status_code=400,
            detail="Amount must be a positive number"
        )
    
    # Validate description
    if not expense.description or not expense.description.strip():
        raise HTTPException(
            status_code=400,
            detail="Description cannot be empty"
        )
    
    # Generate timestamp if not provided
    timestamp = expense.timestamp or datetime.utcnow().isoformat()
    
    # Create expense record
    expense_id = str(uuid.uuid4())
    expense_record = {
        "expense_id": expense_id,
        "driver_id": expense.driver_id,
        "amount": expense.amount,
        "category": expense.category.lower(),
        "description": expense.description.strip(),
        "trip_id": expense.trip_id or "",
        "timestamp": timestamp,
        "created_at": datetime.utcnow().isoformat(),
        "source": "driver_dashboard",
        "version": 1
    }
    
    # Store in ChromaDB
    try:
        print(f"DEBUG: Attempting to store expense {expense_id}")
        print(f"DEBUG: Expense record: {expense_record}")
        db.expenses.add(
            ids=[expense_id],
            documents=[f"{expense.category}: {expense.description}"],
            metadatas=[expense_record]
        )
        print(f"DEBUG: Successfully stored expense {expense_id}")
    except Exception as e:
        print(f"ERROR: Database error storing expense: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )
    
    return ExpenseResponse(
        expense_id=expense_id,
        driver_id=expense.driver_id,
        amount=expense.amount,
        category=expense.category.lower(),
        description=expense.description,
        trip_id=expense.trip_id,
        timestamp=timestamp,
        created_at=expense_record["created_at"]
    )


@router.get("/expenses/{date}", response_model=DailyExpenseSummary)
async def get_daily_expenses(
    date: str,
    driver_id: Optional[str] = Query(None, description="Filter by driver ID")
):
    """
    Get daily expenses for a specific date
    
    Requirements: 9.2, 9.5, 9.6
    """
    try:
        # Query all expenses
        result = db.expenses.get()
        
        if not result['ids']:
            return DailyExpenseSummary(
                date=date,
                total_expenses=0.0,
                expense_breakdown={cat: 0.0 for cat in VALID_CATEGORIES},
                expenses=[]
            )
        
        # Filter by date and driver
        expenses_list = []
        for metadata in result['metadatas']:
            expense_date = metadata['timestamp'][:10]  # Extract YYYY-MM-DD
            
            if expense_date == date:
                if driver_id is None or metadata['driver_id'] == driver_id:
                    expenses_list.append(metadata)
        
        # Calculate totals and breakdown
        total_expenses = sum(e['amount'] for e in expenses_list)
        expense_breakdown = {cat: 0.0 for cat in VALID_CATEGORIES}
        
        for expense in expenses_list:
            category = expense['category']
            if category in expense_breakdown:
                expense_breakdown[category] += expense['amount']
        
        # Convert to response format
        expenses_response = [
            ExpenseResponse(
                expense_id=e['expense_id'],
                driver_id=e['driver_id'],
                amount=e['amount'],
                category=e['category'],
                description=e['description'],
                trip_id=e.get('trip_id') or None,
                timestamp=e['timestamp'],
                created_at=e['created_at']
            )
            for e in expenses_list
        ]
        
        return DailyExpenseSummary(
            date=date,
            total_expenses=total_expenses,
            expense_breakdown=expense_breakdown,
            expenses=expenses_response
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving expenses: {str(e)}"
        )


@router.post("/reports/generate", response_model=DailyReport, status_code=201)
async def generate_report(request: ReportGenerateRequest):
    """
    Generate a daily financial report
    
    Requirements: 6.2, 6.3, 6.4
    """
    try:
        # Use provided date or default to today
        report_date = request.date or datetime.utcnow().strftime("%Y-%m-%d")
        
        # Generate report using service
        report_service = ReportGenerationService()
        report = report_service.generate_daily_report(request.driver_id, report_date)
        
        # Store in ChromaDB
        report_id = str(uuid.uuid4())
        report_record = {
            "report_id": report_id,
            "driver_id": request.driver_id,
            "date": report_date,
            "generated_at": datetime.utcnow().isoformat(),
            "trips": json.dumps(report['trips']),
            "financial_summary": json.dumps(report['financial_summary']),
            "ai_insights": json.dumps(report['ai_insights']),
            "source": "manual_trigger",
            "version": 1
        }
        
        db.reports.add(
            ids=[report_id],
            documents=[f"Report for {request.driver_id} on {report_date}"],
            metadatas=[report_record]
        )
        
        return DailyReport(
            report_id=report_id,
            driver_id=request.driver_id,
            date=report_date,
            generated_at=report_record["generated_at"],
            trips=[TripDetail(**trip) for trip in report['trips']],
            financial_summary=FinancialMetrics(**report['financial_summary']),
            ai_insights=AIInsights(**report['ai_insights'])
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating report: {str(e)}"
        )


@router.get("/reports/{date}", response_model=DailyReport)
async def get_daily_report(
    date: str,
    driver_id: Optional[str] = Query(None, description="Filter by driver ID")
):
    """
    Get daily report for a specific date
    
    Requirements: 9.3, 9.5, 9.6
    """
    try:
        # Query reports
        result = db.reports.get()
        
        if not result['ids']:
            raise HTTPException(
                status_code=404,
                detail=f"No report found for date {date}"
            )
        
        # Find matching report
        for metadata in result['metadatas']:
            if metadata['date'] == date:
                if driver_id is None or metadata['driver_id'] == driver_id:
                    return DailyReport(
                        report_id=metadata['report_id'],
                        driver_id=metadata['driver_id'],
                        date=metadata['date'],
                        generated_at=metadata['generated_at'],
                        trips=[TripDetail(**trip) for trip in json.loads(metadata['trips'])],
                        financial_summary=FinancialMetrics(**json.loads(metadata['financial_summary'])),
                        ai_insights=AIInsights(**json.loads(metadata['ai_insights']))
                    )
        
        raise HTTPException(
            status_code=404,
            detail=f"No report found for date {date}"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving report: {str(e)}"
        )


@router.get("/reports/{report_id}/pdf")
async def get_report_pdf(report_id: str):
    """
    Get PDF version of a report
    
    Requirements: 7.4
    """
    try:
        from services.pdf_generator import PDFGenerator
        
        # Get report from database
        result = db.reports.get(ids=[report_id])
        
        if not result['ids']:
            raise HTTPException(
                status_code=404,
                detail=f"Report not found: {report_id}"
            )
        
        report_data = result['metadatas'][0]
        
        # Generate PDF
        pdf_generator = PDFGenerator()
        pdf_bytes = pdf_generator.generate_pdf_report(report_data)
        
        # Return PDF with appropriate headers
        from fastapi.responses import FileResponse
        import io
        
        return FileResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=report_{report_data['date']}.pdf"
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating PDF: {str(e)}"
        )
