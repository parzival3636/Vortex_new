# Design Document: Daily Financial Report

## Overview

The Daily Financial Report system is a comprehensive financial tracking and reporting solution for truck logistics platforms. It consists of three main components:

1. **Driver Expense Tracking**: A frontend interface allowing drivers to record daily expenses with categorization
2. **Financial Calculation Engine**: Backend logic that computes earnings, expenses, and net profit metrics
3. **Automated Report Generation**: A scheduled service that generates comprehensive daily reports at 8 PM with AI-powered insights
4. **Owner Dashboard**: A frontend interface for viewing, analyzing, and downloading financial reports

The system integrates with existing trip data to calculate earnings, stores expenses in ChromaDB, and uses AI agents for intelligent expense analysis and insight generation.

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend Layer                            │
├─────────────────────────────────────────────────────────────────┤
│  Driver Dashboard          │         Owner Dashboard             │
│  - Record Spendage UI      │  - Report Viewing                   │
│  - Expense Summary         │  - Metrics Display                  │
│  - Category Selection      │  - Chart Visualization              │
│                            │  - PDF Download                     │
└──────────────┬─────────────┴──────────────┬──────────────────────┘
               │                            │
               └────────────┬───────────────┘
                            │
┌───────────────────────────▼──────────────────────────────────────┐
│                      API Layer (FastAPI)                         │
├─────────────────────────────────────────────────────────────────┤
│  POST /expenses              - Create expense                    │
│  GET /expenses/{date}        - Retrieve daily expenses           │
│  GET /reports/{date}         - Retrieve daily report             │
│  POST /reports/generate      - Trigger report generation         │
│  GET /reports/{date}/pdf     - Generate PDF download             │
└──────────────┬────────────────────────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────────────────────┐
│                    Business Logic Layer                          │
├─────────────────────────────────────────────────────────────────┤
│  Calculation Engine          │  Report Generation Service        │
│  - Earnings Calculator       │  - Daily Report Generator         │
│  - Expense Aggregator        │  - AI Insight Generator           │
│  - Net Profit Computer       │  - PDF Generator                  │
│  - Category Breakdown        │  - Scheduler (APScheduler)        │
└──────────────┬────────────────────────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────────────────────┐
│                      Data Layer                                  │
├─────────────────────────────────────────────────────────────────┤
│  ChromaDB Collections:                                           │
│  - expenses: Stores driver expense records                       │
│  - reports: Stores generated daily reports                       │
│  - trips: Existing trip data (read-only)                         │
└──────────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Expense Recording**: Driver submits expense → API validates → Stored in ChromaDB
2. **Daily Summary**: Frontend requests daily expenses → API queries ChromaDB → Returns aggregated data
3. **Report Generation**: Scheduler triggers at 8 PM → Calculation Engine computes metrics → AI Agent generates insights → Report stored in ChromaDB
4. **Report Viewing**: Owner requests report → API retrieves from ChromaDB → Frontend displays with visualizations
5. **PDF Download**: Owner requests PDF → PDF Generator creates document → Browser downloads file

## Components and Interfaces

### 1. Expense Recording Component

**Frontend (React)**:
- `ExpenseForm.jsx`: Modal/form for recording expenses
- `ExpenseSummary.jsx`: Display daily expense totals and breakdown
- `RecordSpendageButton.jsx`: Button to trigger expense recording

**Backend (FastAPI)**:
```python
POST /api/expenses
{
  "driver_id": string,
  "amount": float,
  "category": "fuel" | "maintenance" | "toll" | "food" | "other",
  "description": string,
  "trip_id": string (optional),
  "timestamp": ISO8601 datetime
}

Response: 201 Created
{
  "expense_id": string,
  "status": "created"
}
```

**Validation Rules**:
- Amount must be positive number
- Category must be one of five predefined values
- Description must be non-empty string
- Timestamp must be valid ISO8601 format

### 2. Financial Calculation Engine

**Core Functions**:

```python
class CalculationEngine:
  def calculate_daily_earnings(driver_id: str, date: str) -> float
    # Sum all completed trip earnings for the day
    
  def calculate_daily_expenses(driver_id: str, date: str) -> float
    # Sum all expense amounts for the day
    
  def calculate_net_profit(driver_id: str, date: str) -> float
    # earnings - expenses
    
  def get_expense_breakdown(driver_id: str, date: str) -> Dict[str, float]
    # Returns {category: total_amount} for each category
    
  def classify_expense(description: str, amount: float) -> str
    # Rule-based classification returning category
```

**Classification Rules**:
- Fuel: Keywords like "gas", "fuel", "petrol", "diesel"
- Maintenance: Keywords like "repair", "maintenance", "service", "oil"
- Toll: Keywords like "toll", "highway", "fee"
- Food: Keywords like "food", "meal", "restaurant", "lunch", "dinner"
- Other: Default category for unclassified expenses

### 3. Report Generation Service

**Scheduled Task (APScheduler)**:
- Runs daily at 8 PM (20:00)
- Triggers `generate_daily_report()` for each active driver
- Stores report in ChromaDB

**Report Structure**:
```python
{
  "report_id": string,
  "driver_id": string,
  "date": string (YYYY-MM-DD),
  "generated_at": ISO8601 datetime,
  "trips": [
    {
      "trip_id": string,
      "origin": string,
      "destination": string,
      "load_details": string,
      "earnings": float
    }
  ],
  "financial_summary": {
    "total_earnings": float,
    "total_expenses": float,
    "net_profit": float,
    "expense_breakdown": {
      "fuel": float,
      "maintenance": float,
      "toll": float,
      "food": float,
      "other": float
    }
  },
  "performance_metrics": {
    "trips_completed": int,
    "average_earnings_per_trip": float,
    "expense_ratio": float (expenses/earnings)
  },
  "ai_insights": {
    "summary": string,
    "anomalies": [string],
    "recommendations": [string]
  }
}
```

**Backend Endpoint**:
```python
POST /api/reports/generate
{
  "driver_id": string,
  "date": string (optional, defaults to today)
}

Response: 200 OK
{
  "report_id": string,
  "status": "generated"
}
```

### 4. AI Insight Generation

**CrewAI Agent Configuration**:
- Role: Financial Analyst
- Goal: Analyze daily expenses and identify patterns
- Tools: Expense data access, calculation functions

**Insight Generation Process**:
1. Receive daily expense data and metrics
2. Analyze spending patterns by category
3. Identify anomalies (unusual amounts, categories)
4. Generate recommendations for cost optimization
5. Create summary narrative

### 5. PDF Generation Component

**Backend Function**:
```python
def generate_pdf_report(report_id: str) -> bytes
  # Uses ReportLab to create PDF
  # Includes all report sections with formatting
  # Returns PDF bytes for download
```

**PDF Sections**:
- Header with date and driver info
- Financial summary (key metrics)
- Trip details table
- Expense breakdown chart
- Expense details table
- AI insights and recommendations
- Footer with generation timestamp

**Backend Endpoint**:
```python
GET /api/reports/{report_id}/pdf

Response: 200 OK
Content-Type: application/pdf
Content-Disposition: attachment; filename="report_YYYY-MM-DD.pdf"
[PDF binary data]
```

### 6. Owner Dashboard Report Viewing

**Frontend Components**:
- `ReportViewer.jsx`: Main report display container
- `MetricsDisplay.jsx`: Shows Total Earnings, Total Expenses, Net Profit
- `ExpenseChart.jsx`: Pie/bar chart for expense breakdown
- `TripSummaryTable.jsx`: Table of trips with earnings
- `ExpenseDetailsTable.jsx`: Table of expenses with categories
- `AIInsightsPanel.jsx`: Display AI-generated insights
- `DateSelector.jsx`: Calendar/date picker for report selection
- `DownloadButton.jsx`: PDF download trigger

**Frontend State Management**:
- Selected date (default: today)
- Current report data
- Loading states
- Error handling

## Data Models

### Expense Model (ChromaDB)

```python
{
  "id": string (UUID),
  "driver_id": string,
  "amount": float,
  "category": string,
  "description": string,
  "trip_id": string (optional),
  "timestamp": ISO8601 datetime,
  "created_at": ISO8601 datetime,
  "metadata": {
    "source": "driver_dashboard",
    "version": 1
  }
}
```

### Report Model (ChromaDB)

```python
{
  "id": string (UUID),
  "driver_id": string,
  "date": string (YYYY-MM-DD),
  "generated_at": ISO8601 datetime,
  "trips": list,
  "financial_summary": dict,
  "performance_metrics": dict,
  "ai_insights": dict,
  "metadata": {
    "source": "automated_scheduler" | "manual_trigger",
    "version": 1
  }
}
```

### Trip Model (Existing, Read-Only)

```python
{
  "id": string (UUID),
  "driver_id": string,
  "origin": string,
  "destination": string,
  "load_details": string,
  "earnings": float,
  "completed_at": ISO8601 datetime,
  "status": "completed"
}
```

## Error Handling

**Validation Errors**:
- Invalid expense amount: Return 400 with message "Amount must be positive"
- Invalid category: Return 400 with message "Category must be one of: fuel, maintenance, toll, food, other"
- Missing required fields: Return 400 with message "Missing required field: {field_name}"

**Processing Errors**:
- Database connection failure: Return 500 with message "Database error"
- Report generation failure: Log error, retry after 5 minutes, notify admin
- PDF generation failure: Return 500 with message "PDF generation failed"

**Data Errors**:
- No expenses found for date: Return empty expense list
- No report found for date: Return 404 with message "Report not found for date"
- No trips found for date: Include empty trips array in report

## Correctness Properties

A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.


### Property Reflection and Consolidation

After analyzing all acceptance criteria, I've identified the following redundancies and consolidations:

- Properties 3.1, 3.2, 3.3 (earnings, expenses, net profit calculations) are interdependent and can be consolidated into one comprehensive calculation property
- Properties 4.2, 4.3, 4.4, 4.5, 4.6 (report content) can be consolidated into one comprehensive report generation property
- Properties 5.4, 5.5 (table displays) can be consolidated into one comprehensive display property
- Properties 7.2, 7.3 (PDF generation and content) can be consolidated into one comprehensive PDF property
- Properties 9.2, 9.3 (API GET endpoints) can be consolidated into one comprehensive API retrieval property
- Properties 10.1, 10.2 (data persistence) can be consolidated into one comprehensive persistence property

### Correctness Properties

**Property 1: Expense Storage and Retrieval**

*For any* valid expense record with all required fields (amount, category, description, timestamp), when the expense is submitted to the system, it SHALL be stored in ChromaDB and retrievable with all fields intact.

**Validates: Requirements 1.3, 10.1**

**Property 2: Expense-Trip Association**

*For any* active trip and any expense recorded during that trip, the expense record SHALL contain the trip_id and be retrievable through the trip's expense collection.

**Validates: Requirements 1.4**

**Property 3: Automatic Timestamp Capture**

*For any* expense record created, the timestamp field SHALL be automatically populated with the current time and SHALL be within 1 second of the actual creation time.

**Validates: Requirements 1.5**

**Property 4: Expense Validation**

*For any* expense submission with missing required fields or invalid values (negative amount, invalid category), the system SHALL reject the submission and return a validation error without creating a record.

**Validates: Requirements 1.6**

**Property 5: Daily Expense Summary Accuracy**

*For any* set of expenses recorded on a given day, the displayed daily expense total SHALL equal the sum of all expense amounts for that day, and the category breakdown SHALL show correct totals for each category.

**Validates: Requirements 2.2, 2.3, 2.4**

**Property 6: Real-Time Summary Updates**

*For any* new expense added to the system, the daily expense summary display SHALL update within 2 seconds to reflect the new total and category breakdown.

**Validates: Requirements 2.5**

**Property 7: Financial Calculations Accuracy**

*For any* set of completed trips and recorded expenses on a given day, the system SHALL calculate daily earnings as the sum of trip earnings, daily expenses as the sum of expense amounts, and net profit as earnings minus expenses, with all calculations matching the expected mathematical results.

**Validates: Requirements 3.1, 3.2, 3.3**

**Property 8: Expense Classification Consistency**

*For any* expense description and amount, the rule-based classification system SHALL consistently assign the same category every time the same description is classified, and SHALL classify expenses into exactly one of the five categories: fuel, maintenance, toll, food, or other.

**Validates: Requirements 3.5, 8.2**

**Property 9: Earnings Update on Trip Completion**

*For any* completed trip with a specified earnings amount, the daily earnings total SHALL increase by exactly that amount immediately upon trip completion.

**Validates: Requirements 3.6**

**Property 10: Comprehensive Daily Report Generation**

*For any* day with completed trips and recorded expenses, the generated daily report SHALL include all trips with complete details (origin, destination, load details, earnings), total earnings matching the sum of trip earnings, expense breakdown by category matching actual expenses, net profit calculation as earnings minus expenses, and driver performance metrics (trips_completed, average_earnings_per_trip, expense_ratio).

**Validates: Requirements 4.2, 4.3, 4.4, 4.5, 4.6**

**Property 11: Report Persistence and Retrieval**

*For any* generated daily report, the report SHALL be stored in ChromaDB and be retrievable by report_id, driver_id, and date, with all report data intact and unchanged.

**Validates: Requirements 4.8, 10.2**

**Property 12: AI Insights Generation**

*For any* daily report generated, the ai_insights field SHALL be populated with analysis including a summary, identified anomalies, and recommendations for cost optimization.

**Validates: Requirements 4.7, 8.1, 8.3, 8.5**

**Property 13: On-Demand Report Generation**

*For any* manual report generation request, the system SHALL generate a report for the specified date (or current day if not specified) and store it in the database, making it immediately available for retrieval and display.

**Validates: Requirements 6.3, 6.4**

**Property 14: Report Display Completeness**

*For any* retrieved daily report, the Owner Dashboard SHALL display all report data including trip summary table with all trips and their earnings, expense details table with all expenses and categories, key metrics (Total Earnings, Total Expenses, Net Profit), and AI insights.

**Validates: Requirements 5.4, 5.5**

**Property 15: Report Date Selection**

*For any* date selected by the owner, the system SHALL retrieve and display the report for that specific date, and SHALL display the most recent available report by default when no date is selected.

**Validates: Requirements 5.6, 5.7**

**Property 16: PDF Generation and Content**

*For any* daily report, when PDF generation is requested, the system SHALL create a valid PDF document containing all report sections (trips, earnings, expenses, metrics, insights), with a filename containing the report date, and make it available for download.

**Validates: Requirements 7.2, 7.3, 7.4**

**Property 17: API Endpoint Data Retrieval**

*For any* API request to retrieve expenses or reports by date and driver, the system SHALL return all matching records with complete data intact, and SHALL return an empty collection if no records exist for the specified criteria.

**Validates: Requirements 9.2, 9.3**

**Property 18: API Input Validation**

*For any* API request with invalid or missing parameters, the system SHALL validate the input and return a 400 Bad Request status with a descriptive error message, without processing the request.

**Validates: Requirements 9.5, 9.6**

**Property 19: Database Query Efficiency**

*For any* query to retrieve expenses or reports by date and driver_id, the database SHALL return results efficiently and support filtering by both date and driver_id independently or in combination.

**Validates: Requirements 10.4**

## Testing Strategy

### Dual Testing Approach

This feature requires both unit testing and property-based testing for comprehensive coverage:

**Unit Tests** (Specific Examples and Edge Cases):
- Test the "Record Spendage" button rendering and click behavior
- Test expense form validation with various invalid inputs
- Test category dropdown displays exactly 5 options
- Test PDF download button rendering and click behavior
- Test report date selector functionality
- Test API endpoint existence and basic response structure
- Test edge cases: zero expenses, single trip, multiple expenses in same category

**Property-Based Tests** (Universal Properties):
- Property 1: Expense storage and retrieval round-trip
- Property 2: Expense-trip association consistency
- Property 3: Timestamp accuracy
- Property 4: Validation rejection of invalid data
- Property 5: Daily summary calculation accuracy
- Property 6: Real-time update responsiveness
- Property 7: Financial calculations correctness
- Property 8: Classification consistency
- Property 9: Earnings update on trip completion
- Property 10: Report generation completeness
- Property 11: Report persistence and retrieval
- Property 12: AI insights generation
- Property 13: On-demand report generation
- Property 14: Report display completeness
- Property 15: Report date selection
- Property 16: PDF generation and content
- Property 17: API data retrieval
- Property 18: API input validation
- Property 19: Database query efficiency

### Property-Based Testing Configuration

**Testing Framework**: Hypothesis (Python) for backend, fast-check (JavaScript) for frontend

**Test Configuration**:
- Minimum 100 iterations per property test
- Each test tagged with feature name and property number
- Tag format: `Feature: daily-financial-report, Property {number}: {property_text}`

**Example Test Structure**:
```python
# Feature: daily-financial-report, Property 1: Expense Storage and Retrieval
@given(
    amount=st.floats(min_value=0.01, max_value=10000),
    category=st.sampled_from(['fuel', 'maintenance', 'toll', 'food', 'other']),
    description=st.text(min_size=1, max_size=200)
)
def test_expense_storage_and_retrieval(amount, category, description):
    # Create expense
    expense = create_expense(amount, category, description)
    
    # Store in ChromaDB
    stored_id = store_expense(expense)
    
    # Retrieve from ChromaDB
    retrieved = retrieve_expense(stored_id)
    
    # Verify all fields match
    assert retrieved.amount == amount
    assert retrieved.category == category
    assert retrieved.description == description
```

### Testing Priorities

1. **High Priority** (Core Functionality):
   - Property 1: Expense storage
   - Property 7: Financial calculations
   - Property 10: Report generation
   - Property 11: Report persistence

2. **Medium Priority** (User-Facing Features):
   - Property 5: Summary accuracy
   - Property 14: Report display
   - Property 16: PDF generation

3. **Low Priority** (Edge Cases and Optimization):
   - Property 3: Timestamp accuracy
   - Property 19: Database efficiency

