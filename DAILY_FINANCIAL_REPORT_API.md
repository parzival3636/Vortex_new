# Daily Financial Report API Documentation

## Overview

The Daily Financial Report API provides endpoints for managing driver expenses, generating financial reports, and accessing AI-powered insights. The system automatically generates daily reports at 8 PM and supports on-demand report generation.

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

Currently, the API does not require authentication. In production, implement JWT or OAuth2 authentication.

## Endpoints

### Expenses

#### Create Expense
**POST** `/financial/expenses`

Create a new expense record.

**Request Body:**
```json
{
  "driver_id": "string",
  "amount": 500.00,
  "category": "fuel",
  "description": "Diesel fuel at pump",
  "trip_id": "optional-trip-id",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

**Response (201 Created):**
```json
{
  "expense_id": "550e8400-e29b-41d4-a716-446655440000",
  "driver_id": "driver-123",
  "amount": 500.00,
  "category": "fuel",
  "description": "Diesel fuel at pump",
  "trip_id": "trip-456",
  "timestamp": "2024-01-15T10:30:00Z",
  "created_at": "2024-01-15T10:30:01Z"
}
```

**Error Responses:**
- `400 Bad Request`: Invalid category, negative amount, or missing required fields
- `500 Internal Server Error`: Database error

**Validation Rules:**
- Amount must be positive
- Category must be one of: fuel, maintenance, toll, food, other
- Description must be non-empty

---

#### Get Daily Expenses
**GET** `/financial/expenses/{date}`

Retrieve all expenses for a specific date.

**Query Parameters:**
- `driver_id` (optional): Filter by driver ID

**Response (200 OK):**
```json
{
  "date": "2024-01-15",
  "total_expenses": 1500.00,
  "expense_breakdown": {
    "fuel": 800.00,
    "maintenance": 300.00,
    "toll": 200.00,
    "food": 200.00,
    "other": 0.00
  },
  "expenses": [
    {
      "expense_id": "550e8400-e29b-41d4-a716-446655440000",
      "driver_id": "driver-123",
      "amount": 500.00,
      "category": "fuel",
      "description": "Diesel fuel at pump",
      "trip_id": "trip-456",
      "timestamp": "2024-01-15T10:30:00Z",
      "created_at": "2024-01-15T10:30:01Z"
    }
  ]
}
```

**Error Responses:**
- `500 Internal Server Error`: Database error

---

### Reports

#### Generate Report
**POST** `/financial/reports/generate`

Generate a daily financial report.

**Request Body:**
```json
{
  "driver_id": "driver-123",
  "date": "2024-01-15"
}
```

**Response (201 Created):**
```json
{
  "report_id": "report-123",
  "driver_id": "driver-123",
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
```

**Error Responses:**
- `500 Internal Server Error`: Report generation error

---

#### Get Daily Report
**GET** `/financial/reports/{date}`

Retrieve a daily report for a specific date.

**Query Parameters:**
- `driver_id` (optional): Filter by driver ID

**Response (200 OK):**
```json
{
  "report_id": "report-123",
  "driver_id": "driver-123",
  "date": "2024-01-15",
  "generated_at": "2024-01-15T20:00:00Z",
  "trips": [...],
  "financial_summary": {...},
  "ai_insights": {...}
}
```

**Error Responses:**
- `404 Not Found`: No report found for the specified date
- `500 Internal Server Error`: Database error

---

#### Download Report as PDF
**GET** `/financial/reports/{report_id}/pdf`

Download a report as PDF.

**Response (200 OK):**
- Content-Type: `application/pdf`
- Content-Disposition: `attachment; filename=report_YYYY-MM-DD.pdf`
- Body: PDF binary data

**Error Responses:**
- `404 Not Found`: Report not found
- `500 Internal Server Error`: PDF generation error

---

### Scheduler

#### Start Scheduler
**POST** `/scheduler/start`

Start the daily report scheduler (8 PM daily).

**Response (200 OK):**
```json
{
  "status": "started",
  "message": "Report scheduler started. Reports will be generated daily at 8 PM"
}
```

---

#### Stop Scheduler
**POST** `/scheduler/stop`

Stop the daily report scheduler.

**Response (200 OK):**
```json
{
  "status": "stopped",
  "message": "Report scheduler stopped"
}
```

---

#### Get Scheduler Status
**GET** `/scheduler/status`

Get the current status of the scheduler.

**Response (200 OK):**
```json
{
  "is_running": true,
  "next_run_time": "2024-01-15T20:00:00",
  "jobs": [
    {
      "id": "daily_report_generation",
      "name": "Daily Report Generation at 8 PM",
      "next_run_time": "2024-01-15T20:00:00"
    }
  ]
}
```

---

#### Force Run Scheduler
**POST** `/scheduler/force-run`

Force immediate execution of report generation.

**Response (200 OK):**
```json
{
  "status": "completed",
  "message": "Report generation completed"
}
```

---

## Data Models

### Expense
```json
{
  "expense_id": "string (UUID)",
  "driver_id": "string",
  "amount": "float (> 0)",
  "category": "string (fuel|maintenance|toll|food|other)",
  "description": "string (non-empty)",
  "trip_id": "string (optional)",
  "timestamp": "string (ISO8601)",
  "created_at": "string (ISO8601)"
}
```

### Report
```json
{
  "report_id": "string (UUID)",
  "driver_id": "string",
  "date": "string (YYYY-MM-DD)",
  "generated_at": "string (ISO8601)",
  "trips": "array of TripDetail",
  "financial_summary": "FinancialMetrics",
  "ai_insights": "AIInsights"
}
```

### FinancialMetrics
```json
{
  "total_earnings": "float (>= 0)",
  "total_expenses": "float (>= 0)",
  "net_profit": "float",
  "expense_breakdown": {
    "fuel": "float",
    "maintenance": "float",
    "toll": "float",
    "food": "float",
    "other": "float"
  },
  "trips_completed": "integer (>= 0)",
  "average_earnings_per_trip": "float (>= 0)",
  "expense_ratio": "float (0-1)"
}
```

### AIInsights
```json
{
  "summary": "string",
  "anomalies": "array of string",
  "recommendations": "array of string"
}
```

---

## Error Handling

All error responses follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common HTTP Status Codes

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid input or validation error
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

---

## Expense Categories

The system supports exactly five expense categories:

1. **fuel** - Diesel, petrol, gasoline, fuel pump expenses
2. **maintenance** - Repairs, service, oil changes, spare parts
3. **toll** - Highway tolls, road fees, taxes
4. **food** - Meals, restaurants, snacks
5. **other** - Any other expenses

---

## Classification Rules

Expenses are automatically classified based on keywords in the description:

- **Fuel**: "gas", "fuel", "petrol", "diesel", "gasoline", "pump"
- **Maintenance**: "repair", "maintenance", "service", "oil", "mechanic", "spare", "parts"
- **Toll**: "toll", "highway", "fee", "tax", "road"
- **Food**: "food", "meal", "restaurant", "lunch", "dinner", "breakfast", "snack", "eat"
- **Other**: Default category for unclassified expenses

---

## Scheduled Report Generation

Reports are automatically generated daily at **8 PM (20:00 UTC)** for all active drivers.

### Automatic Report Contents

Each automatically generated report includes:

1. **Trips**: All completed trips for the day
2. **Financial Summary**: Earnings, expenses, net profit, and metrics
3. **AI Insights**: Summary, anomalies, and recommendations

### Manual Report Generation

Reports can also be generated on-demand using the `/financial/reports/generate` endpoint.

---

## Real-Time Updates

The frontend implements polling (every 5 seconds) to display real-time expense updates on the Driver Dashboard.

---

## Database Schema

### Expenses Collection (ChromaDB)

```
Collection: expenses
Fields:
  - expense_id (string, primary key)
  - driver_id (string)
  - amount (float)
  - category (string)
  - description (string)
  - trip_id (string, optional)
  - timestamp (string, ISO8601)
  - created_at (string, ISO8601)
  - metadata (object)
```

### Reports Collection (ChromaDB)

```
Collection: reports
Fields:
  - report_id (string, primary key)
  - driver_id (string)
  - date (string, YYYY-MM-DD)
  - generated_at (string, ISO8601)
  - trips (array)
  - financial_summary (object)
  - ai_insights (object)
  - metadata (object)
```

---

## Example Usage

### Create an Expense

```bash
curl -X POST http://localhost:8000/api/v1/financial/expenses \
  -H "Content-Type: application/json" \
  -d '{
    "driver_id": "driver-123",
    "amount": 500.00,
    "category": "fuel",
    "description": "Diesel fuel at pump",
    "trip_id": "trip-456"
  }'
```

### Get Daily Expenses

```bash
curl http://localhost:8000/api/v1/financial/expenses/2024-01-15?driver_id=driver-123
```

### Generate Report

```bash
curl -X POST http://localhost:8000/api/v1/financial/reports/generate \
  -H "Content-Type: application/json" \
  -d '{
    "driver_id": "driver-123",
    "date": "2024-01-15"
  }'
```

### Get Daily Report

```bash
curl http://localhost:8000/api/v1/financial/reports/2024-01-15?driver_id=driver-123
```

### Download PDF

```bash
curl http://localhost:8000/api/v1/financial/reports/report-123/pdf \
  -o report_2024-01-15.pdf
```

---

## Deployment Checklist

- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Configure environment variables in `.env`
- [ ] Initialize ChromaDB collections
- [ ] Start the FastAPI server: `python main.py`
- [ ] Start the frontend development server: `npm run dev` (in frontend directory)
- [ ] Test all API endpoints
- [ ] Configure scheduler to start on application startup
- [ ] Set up logging and monitoring
- [ ] Configure CORS for production
- [ ] Implement authentication (JWT/OAuth2)
- [ ] Set up database backups
- [ ] Configure error tracking (Sentry, etc.)

---

## Support

For issues or questions, please refer to the specification documents:
- Requirements: `.kiro/specs/daily-financial-report/requirements.md`
- Design: `.kiro/specs/daily-financial-report/design.md`
- Tasks: `.kiro/specs/daily-financial-report/tasks.md`
