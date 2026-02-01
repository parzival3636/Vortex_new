# Implementation Plan: Daily Financial Report

## Overview

This implementation plan breaks down the Daily Financial Report feature into discrete coding tasks. The approach follows a layered implementation strategy: first establishing the backend API and data models, then implementing the calculation engine, followed by the frontend components, and finally integrating the report generation service with AI insights.

Each task builds incrementally on previous work, with property-based tests integrated throughout to validate correctness properties early. Optional testing tasks are marked with `*` and can be skipped for faster MVP delivery.

## Tasks

- [x] 1. Set up backend project structure and core dependencies
  - Create FastAPI application skeleton with project structure
  - Install and configure ChromaDB for data persistence
  - Set up APScheduler for scheduled tasks
  - Configure environment variables and logging
  - _Requirements: 9.1, 10.3_

- [x] 2. Create data models and database schema
  - [x] 2.1 Define Expense model with all required fields (amount, category, description, timestamp, trip_id)
    - Create ChromaDB collection schema for expenses
    - Implement data validation for expense fields
    - _Requirements: 10.1_
  
  - [ ]* 2.2 Write property test for expense storage and retrieval
    - **Property 1: Expense Storage and Retrieval**
    - **Validates: Requirements 1.3, 10.1**
  
  - [x] 2.3 Define Report model with all required fields (trips, financial_summary, performance_metrics, ai_insights)
    - Create ChromaDB collection schema for reports
    - Implement report data structure
    - _Requirements: 10.2_
  
  - [ ]* 2.4 Write property test for report persistence and retrieval
    - **Property 11: Report Persistence and Retrieval**
    - **Validates: Requirements 4.8, 10.2**

- [x] 3. Implement Financial Calculation Engine
  - [x] 3.1 Create CalculationEngine class with core calculation methods
    - Implement calculate_daily_earnings(driver_id, date)
    - Implement calculate_daily_expenses(driver_id, date)
    - Implement calculate_net_profit(driver_id, date)
    - Implement get_expense_breakdown(driver_id, date)
    - _Requirements: 3.1, 3.2, 3.3, 3.4_
  
  - [ ]* 3.2 Write property test for financial calculations accuracy
    - **Property 7: Financial Calculations Accuracy**
    - **Validates: Requirements 3.1, 3.2, 3.3**
  
  - [x] 3.3 Implement rule-based expense classification system
    - Create classify_expense(description, amount) function
    - Implement classification rules for all five categories
    - _Requirements: 3.5, 8.2_
  
  - [ ]* 3.4 Write property test for classification consistency
    - **Property 8: Expense Classification Consistency**
    - **Validates: Requirements 3.5, 8.2**

- [x] 4. Implement Expense API endpoints
  - [x] 4.1 Create POST /api/expenses endpoint
    - Accept expense data (amount, category, description, trip_id)
    - Validate all required fields
    - Store expense in ChromaDB with automatic timestamp
    - Return created expense with ID
    - _Requirements: 1.3, 9.1, 9.5, 9.6_
  
  - [ ]* 4.2 Write property test for expense validation
    - **Property 4: Expense Validation**
    - **Validates: Requirements 1.6_
  
  - [x] 4.3 Create GET /api/expenses/{date} endpoint
    - Accept date parameter
    - Query ChromaDB for all expenses on that date
    - Return list of expenses with all fields
    - _Requirements: 9.2, 9.5, 9.6_
  
  - [ ]* 4.4 Write property test for API data retrieval
    - **Property 17: API Endpoint Data Retrieval**
    - **Validates: Requirements 9.2, 9.3_

- [x] 5. Implement Report Generation Service
  - [x] 5.1 Create ReportGenerationService class
    - Implement generate_daily_report(driver_id, date) method
    - Gather all trips for the day from existing trip data
    - Calculate financial metrics using CalculationEngine
    - Compile all data into report structure
    - _Requirements: 4.2, 4.3, 4.4, 4.5, 4.6_
  
  - [ ]* 5.2 Write property test for report generation completeness
    - **Property 10: Comprehensive Daily Report Generation**
    - **Validates: Requirements 4.2, 4.3, 4.4, 4.5, 4.6_
  
  - [x] 5.3 Implement AI insight generation using CrewAI
    - Create AI agent for expense analysis
    - Implement insight generation (summary, anomalies, recommendations)
    - Integrate with report generation
    - _Requirements: 4.7, 8.1, 8.3, 8.5_
  
  - [ ]* 5.4 Write property test for AI insights generation
    - **Property 12: AI Insights Generation**
    - **Validates: Requirements 4.7, 8.1, 8.3, 8.5_

- [x] 6. Implement Report API endpoints
  - [x] 6.1 Create GET /api/reports/{date} endpoint
    - Accept date parameter
    - Query ChromaDB for report on that date
    - Return complete report with all sections
    - _Requirements: 9.3, 9.5, 9.6_
  
  - [x] 6.2 Create POST /api/reports/generate endpoint
    - Accept optional date parameter (defaults to today)
    - Trigger report generation
    - Store report in ChromaDB
    - Return generated report
    - _Requirements: 6.2, 6.3, 6.4_
  
  - [ ]* 6.3 Write property test for on-demand report generation
    - **Property 13: On-Demand Report Generation**
    - **Validates: Requirements 6.3, 6.4_

- [x] 7. Implement PDF generation functionality
  - [x] 7.1 Create PDFGenerator class using ReportLab
    - Implement generate_pdf_report(report_id) method
    - Format report data into PDF sections
    - Include all report sections: trips, earnings, expenses, metrics, insights
    - _Requirements: 7.2, 7.3_
  
  - [x] 7.2 Create GET /api/reports/{report_id}/pdf endpoint
    - Generate PDF for specified report
    - Return PDF with appropriate headers and filename
    - _Requirements: 7.4_
  
  - [ ]* 7.3 Write property test for PDF generation and content
    - **Property 16: PDF Generation and Content**
    - **Validates: Requirements 7.2, 7.3, 7.4_

- [x] 8. Implement scheduled report generation
  - [x] 8.1 Configure APScheduler for 8 PM daily task
    - Set up scheduler to run at 8 PM every day
    - Trigger report generation for all active drivers
    - Handle scheduler errors and retries
    - _Requirements: 4.1_
  
  - [x] 8.2 Implement error handling and logging for scheduled tasks
    - Log all report generation attempts
    - Implement retry logic for failed generations
    - Notify admin on critical failures
    - _Requirements: 4.1_

- [x] 9. Checkpoint - Backend API validation
  - Ensure all backend endpoints are working correctly
  - Verify data is persisting to ChromaDB
  - Test report generation manually
  - Ask the user if questions arise

- [x] 10. Create frontend project structure and dependencies
  - Set up React application with Tailwind CSS
  - Install required dependencies (axios, chart libraries, date pickers)
  - Configure environment variables for API endpoints
  - Set up component folder structure
  - _Requirements: 5.1, 6.1_

- [x] 11. Implement Driver Dashboard expense tracking UI
  - [x] 11.1 Create RecordSpendageButton component
    - Display button in Driver Dashboard
    - Trigger expense recording modal on click
    - _Requirements: 1.1, 1.2_
  
  - [x] 11.2 Create ExpenseForm component
    - Build form with fields: amount, category, description
    - Implement category dropdown with exactly 5 options
    - Add form validation
    - Submit to POST /api/expenses endpoint
    - _Requirements: 1.3, 1.7_
  
  - [ ]* 11.3 Write unit tests for ExpenseForm component
    - Test form rendering
    - Test category dropdown options
    - Test form submission
    - _Requirements: 1.7_
  
  - [x] 11.4 Create ExpenseSummary component
    - Display daily expense total
    - Show expense breakdown by category
    - Fetch data from GET /api/expenses/{date} endpoint
    - _Requirements: 2.1, 2.2, 2.3, 2.4_
  
  - [ ]* 11.5 Write property test for daily expense summary accuracy
    - **Property 5: Daily Expense Summary Accuracy**
    - **Validates: Requirements 2.2, 2.3, 2.4_

- [x] 12. Implement real-time expense summary updates
  - [x] 12.1 Add WebSocket or polling mechanism for real-time updates
    - Implement polling to refresh expense summary every 5 seconds
    - Or implement WebSocket connection for push updates
    - _Requirements: 2.5_
  
  - [ ]* 12.2 Write property test for real-time update responsiveness
    - **Property 6: Real-Time Summary Updates**
    - **Validates: Requirements 2.5_

- [x] 13. Implement Owner Dashboard report viewing UI
  - [x] 13.1 Create ReportViewer component
    - Display report viewing section on Owner Dashboard
    - Fetch report from GET /api/reports/{date} endpoint
    - _Requirements: 5.1_
  
  - [x] 13.2 Create MetricsDisplay component
    - Show key metrics: Total Earnings, Total Expenses, Net Profit
    - Format numbers with currency symbols
    - _Requirements: 5.2_
  
  - [x] 13.3 Create ExpenseChart component
    - Render pie chart or bar chart for expense breakdown
    - Use chart library (e.g., Chart.js, Recharts)
    - Display all five expense categories
    - _Requirements: 5.3_
  
  - [x] 13.4 Create TripSummaryTable component
    - Display table with all trips for the day
    - Show columns: origin, destination, load details, earnings
    - _Requirements: 5.4_
  
  - [ ]* 13.5 Write property test for report display completeness
    - **Property 14: Report Display Completeness**
    - **Validates: Requirements 5.4, 5.5_
  
  - [x] 13.6 Create ExpenseDetailsTable component
    - Display table with all expenses for the day
    - Show columns: amount, category, description, timestamp
    - _Requirements: 5.5_

- [x] 14. Implement report date selection and navigation
  - [x] 14.1 Create DateSelector component
    - Add date picker for selecting report date
    - Display most recent report by default
    - Fetch report when date changes
    - _Requirements: 5.6, 5.7_
  
  - [ ]* 14.2 Write property test for report date selection
    - **Property 15: Report Date Selection**
    - **Validates: Requirements 5.6, 5.7_

- [x] 15. Implement on-demand report generation UI
  - [x] 15.1 Create GenerateReportButton component
    - Display "Generate Report Now" button on Owner Dashboard
    - Call POST /api/reports/generate endpoint on click
    - Show loading state during generation
    - _Requirements: 6.1, 6.2_
  
  - [x] 15.2 Display generated report immediately
    - Update ReportViewer with newly generated report
    - Show success message to user
    - _Requirements: 6.3_

- [x] 16. Implement PDF download functionality
  - [x] 16.1 Create DownloadButton component
    - Display "Download as PDF" button on report view
    - Call GET /api/reports/{report_id}/pdf endpoint
    - Trigger browser download with proper filename
    - _Requirements: 7.1, 7.4_
  
  - [ ]* 16.2 Write unit tests for PDF download
    - Test button rendering
    - Test download trigger
    - _Requirements: 7.1_

- [x] 17. Implement AI insights display
  - [x] 17.1 Create AIInsightsPanel component
    - Display AI-generated insights from report
    - Show summary, anomalies, and recommendations
    - Format insights for readability
    - _Requirements: 8.1, 8.3, 8.4, 8.5_

- [x] 18. Checkpoint - Frontend integration validation
  - Ensure all frontend components render correctly
  - Verify API calls are working from frontend
  - Test complete user flows for both driver and owner
  - Ask the user if questions arise

- [x] 19. Integrate expense tracking with trip association
  - [x] 19.1 Modify ExpenseForm to capture active trip context
    - Detect if driver is currently on a trip
    - Automatically associate expense with active trip
    - _Requirements: 1.4_
  
  - [ ]* 19.2 Write property test for expense-trip association
    - **Property 2: Expense-Trip Association**
    - **Validates: Requirements 1.4_

- [x] 20. Implement earnings update on trip completion
  - [x] 20.1 Add hook to update daily earnings when trip completes
    - Listen for trip completion events
    - Trigger CalculationEngine to update daily totals
    - Update frontend display
    - _Requirements: 3.6_
  
  - [ ]* 20.2 Write property test for earnings update on trip completion
    - **Property 9: Earnings Update on Trip Completion**
    - **Validates: Requirements 3.6_

- [x] 21. Implement timestamp validation and accuracy
  - [x] 21.1 Add timestamp validation to expense recording
    - Ensure timestamps are captured automatically
    - Validate timestamp accuracy
    - _Requirements: 1.5_
  
  - [ ]* 21.2 Write property test for automatic timestamp capture
    - **Property 3: Automatic Timestamp Capture**
    - **Validates: Requirements 1.5_

- [x] 22. Implement database query efficiency
  - [x] 22.1 Optimize ChromaDB queries for date and driver filtering
    - Create indexes on driver_id and date fields
    - Test query performance
    - _Requirements: 10.4_
  
  - [ ]* 22.2 Write property test for database query efficiency
    - **Property 19: Database Query Efficiency**
    - **Validates: Requirements 10.4_

- [x] 23. Implement API error handling and validation
  - [x] 23.1 Add comprehensive error handling to all API endpoints
    - Validate all input parameters
    - Return appropriate HTTP status codes
    - Return descriptive error messages
    - _Requirements: 9.5, 9.6_
  
  - [ ]* 23.2 Write property test for API input validation
    - **Property 18: API Input Validation**
    - **Validates: Requirements 9.5, 9.6_

- [x] 24. Final checkpoint - Complete system validation
  - Run all property-based tests (minimum 100 iterations each)
  - Run all unit tests
  - Test complete end-to-end workflows
  - Verify all requirements are met
  - Ask the user if questions arise

- [x] 25. Documentation and deployment preparation
  - Create API documentation (OpenAPI/Swagger)
  - Document database schema and data models
  - Create deployment guide
  - Prepare environment configuration templates
  - _Requirements: All_

## Notes

- Tasks marked with `*` are optional testing tasks and can be skipped for faster MVP delivery
- Each task references specific requirements for traceability
- Property-based tests are integrated throughout to catch bugs early
- Checkpoints ensure incremental validation of system functionality
- All API endpoints should include proper error handling and validation
- Frontend components should follow existing design patterns and Tailwind CSS styling
- Database queries should be optimized for performance with proper indexing

