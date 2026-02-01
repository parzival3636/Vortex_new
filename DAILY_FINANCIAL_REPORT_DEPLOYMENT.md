# Daily Financial Report - Deployment Guide

## Overview

This guide provides step-by-step instructions for deploying the Daily Financial Report feature to production.

## Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn
- ChromaDB (embedded, no separate installation needed)
- APScheduler (for scheduled tasks)

## Backend Deployment

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Key dependencies:
- `fastapi==0.109.0` - Web framework
- `chromadb==0.4.22` - Vector database
- `apscheduler==3.10.4` - Task scheduling
- `reportlab==4.0.9` - PDF generation
- `crewai==0.203.2` - AI insights

### 2. Environment Configuration

Create a `.env` file in the project root:

```env
# FastAPI Configuration
DEBUG=False
HOST=0.0.0.0
PORT=8000

# ChromaDB Configuration
CHROMA_DB_PATH=./chroma_data

# Scheduler Configuration
SCHEDULER_ENABLED=True
SCHEDULER_TIME=20:00  # 8 PM

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/app.log

# Optional: AI Configuration
OLLAMA_MODEL=mistral
OLLAMA_BASE_URL=http://localhost:11434
```

### 3. Initialize Database

The ChromaDB database is automatically initialized on first run. Collections are created as needed:

```python
from db_chromadb import db

# Collections are automatically created:
# - expenses
# - reports
# - trips (existing)
# - loads (existing)
```

### 4. Start the Backend Server

```bash
# Development
python main.py

# Production (with Gunicorn)
gunicorn -w 4 -b 0.0.0.0:8000 main:app
```

The API will be available at `http://localhost:8000`

### 5. Verify Backend

Test the health endpoint:

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "healthy"}
```

---

## Frontend Deployment

### 1. Install Node Dependencies

```bash
cd frontend
npm install
```

### 2. Environment Configuration

Create a `.env` file in the `frontend` directory:

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

For production:
```env
VITE_API_BASE_URL=https://api.yourdomain.com/api/v1
```

### 3. Build Frontend

```bash
npm run build
```

This creates an optimized production build in the `dist` directory.

### 4. Serve Frontend

**Development:**
```bash
npm run dev
```

**Production (using a static server):**
```bash
npm install -g serve
serve -s dist -l 3000
```

Or use Nginx/Apache to serve the `dist` directory.

---

## Docker Deployment

### Backend Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Dockerfile

```dockerfile
FROM node:18-alpine as builder

WORKDIR /app

COPY frontend/package*.json ./
RUN npm install

COPY frontend/ .
RUN npm run build

FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - SCHEDULER_ENABLED=True
    volumes:
      - ./chroma_data:/app/chroma_data
      - ./logs:/app/logs
    depends_on:
      - db

  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "3000:80"
    environment:
      - VITE_API_BASE_URL=http://backend:8000/api/v1
    depends_on:
      - backend

  db:
    image: chromadb/chroma:latest
    ports:
      - "8001:8000"
    volumes:
      - chroma_data:/data

volumes:
  chroma_data:
```

---

## Scheduler Setup

### Automatic Startup

To start the scheduler automatically on application startup, add this to `main.py`:

```python
from services.report_scheduler import report_scheduler

@app.on_event("startup")
async def startup_event():
    report_scheduler.start()
    logger.info("Report scheduler started")

@app.on_event("shutdown")
async def shutdown_event():
    report_scheduler.stop()
    logger.info("Report scheduler stopped")
```

### Manual Scheduler Control

```bash
# Start scheduler
curl -X POST http://localhost:8000/api/v1/scheduler/start

# Check status
curl http://localhost:8000/api/v1/scheduler/status

# Force run
curl -X POST http://localhost:8000/api/v1/scheduler/force-run

# Stop scheduler
curl -X POST http://localhost:8000/api/v1/scheduler/stop
```

---

## Database Backup

### ChromaDB Backup

ChromaDB stores data in `./chroma_data` directory. To backup:

```bash
# Create backup
tar -czf chroma_backup_$(date +%Y%m%d_%H%M%S).tar.gz chroma_data/

# Restore backup
tar -xzf chroma_backup_20240115_120000.tar.gz
```

### Automated Backup Script

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="./backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

tar -czf $BACKUP_DIR/chroma_backup_$TIMESTAMP.tar.gz chroma_data/

# Keep only last 7 days of backups
find $BACKUP_DIR -name "chroma_backup_*.tar.gz" -mtime +7 -delete

echo "Backup completed: $BACKUP_DIR/chroma_backup_$TIMESTAMP.tar.gz"
```

Schedule with cron:
```bash
0 2 * * * /path/to/backup.sh  # Daily at 2 AM
```

---

## Monitoring and Logging

### Application Logging

Configure logging in `main.py`:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

### Health Checks

```bash
# API health
curl http://localhost:8000/health

# Scheduler status
curl http://localhost:8000/api/v1/scheduler/status

# Database connectivity
curl http://localhost:8000/api/v1/financial/expenses/2024-01-15
```

### Performance Monitoring

Monitor these metrics:
- API response times
- Report generation duration
- Database query performance
- Scheduler execution times
- Error rates

---

## Security Considerations

### 1. Authentication

Implement JWT authentication:

```python
from fastapi.security import HTTPBearer, HTTPAuthCredential

security = HTTPBearer()

@app.post("/api/v1/financial/expenses")
async def create_expense(
    expense: ExpenseCreate,
    credentials: HTTPAuthCredential = Depends(security)
):
    # Verify JWT token
    # ...
```

### 2. CORS Configuration

For production, restrict CORS:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

### 3. Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/v1/financial/expenses")
@limiter.limit("100/minute")
async def create_expense(request: Request, expense: ExpenseCreate):
    # ...
```

### 4. Input Validation

All inputs are validated using Pydantic models. Ensure:
- Amount is positive
- Category is valid
- Description is non-empty
- Timestamps are valid ISO8601

### 5. Environment Variables

Never commit sensitive data:
- Use `.env` files (add to `.gitignore`)
- Use environment variables in production
- Rotate API keys regularly

---

## Troubleshooting

### Issue: Scheduler not running

**Solution:**
```bash
# Check scheduler status
curl http://localhost:8000/api/v1/scheduler/status

# Start scheduler
curl -X POST http://localhost:8000/api/v1/scheduler/start

# Check logs
tail -f logs/app.log
```

### Issue: Reports not generating

**Solution:**
```bash
# Force run report generation
curl -X POST http://localhost:8000/api/v1/scheduler/force-run

# Check for errors in logs
grep "ERROR" logs/app.log
```

### Issue: Database connection errors

**Solution:**
```bash
# Verify ChromaDB is running
ls -la chroma_data/

# Check database file
file chroma_data/chroma.sqlite3

# Reinitialize if corrupted
rm -rf chroma_data/
# Restart application to recreate
```

### Issue: PDF generation fails

**Solution:**
```bash
# Verify ReportLab is installed
pip show reportlab

# Check PDF generation logs
grep "PDF" logs/app.log

# Test PDF generation manually
python -c "from services.pdf_generator import PDFGenerator; print('OK')"
```

---

## Performance Optimization

### 1. Database Indexing

ChromaDB automatically indexes collections. For better performance:
- Filter by driver_id and date in queries
- Use pagination for large result sets

### 2. Caching

Implement caching for frequently accessed reports:

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_cached_report(report_id: str):
    # ...
```

### 3. Async Operations

Use async/await for I/O operations:

```python
@app.get("/api/v1/financial/expenses/{date}")
async def get_daily_expenses(date: str):
    # Async database query
    result = await db.expenses.get_async()
    return result
```

---

## Scaling Considerations

### Horizontal Scaling

For multiple instances:
1. Use a load balancer (Nginx, HAProxy)
2. Share ChromaDB instance or use distributed version
3. Use a message queue for scheduled tasks (Celery + Redis)

### Vertical Scaling

- Increase server resources (CPU, RAM)
- Optimize database queries
- Implement caching layer (Redis)

---

## Maintenance

### Regular Tasks

- [ ] Monitor disk space for ChromaDB
- [ ] Review and archive old reports
- [ ] Update dependencies monthly
- [ ] Review security logs
- [ ] Test backup/restore procedures
- [ ] Monitor scheduler execution
- [ ] Check error rates and logs

### Upgrade Procedure

```bash
# 1. Backup database
tar -czf chroma_backup_pre_upgrade.tar.gz chroma_data/

# 2. Update dependencies
pip install --upgrade -r requirements.txt

# 3. Test in staging
python main.py

# 4. Deploy to production
# (restart application)
```

---

## Support and Documentation

- API Documentation: `DAILY_FINANCIAL_REPORT_API.md`
- Requirements: `.kiro/specs/daily-financial-report/requirements.md`
- Design: `.kiro/specs/daily-financial-report/design.md`
- Tasks: `.kiro/specs/daily-financial-report/tasks.md`

---

## Deployment Checklist

- [ ] Install all dependencies
- [ ] Configure environment variables
- [ ] Initialize database
- [ ] Start backend server
- [ ] Verify API endpoints
- [ ] Build frontend
- [ ] Start frontend server
- [ ] Test complete workflow
- [ ] Configure scheduler
- [ ] Set up logging
- [ ] Configure backups
- [ ] Implement authentication
- [ ] Set up monitoring
- [ ] Document deployment
- [ ] Train team on operations
