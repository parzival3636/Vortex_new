# Quick Start Guide - Two Options

## 🚀 Option 1: Run WITHOUT Database (Fastest)

**Perfect for hackathon demo and testing Math Engine!**

### Step 1: Start the Server
```bash
python main.py
```

### Step 2: Test Immediately
Open browser: **http://localhost:8000/docs**

### Step 3: Test Profitability Calculator
Click on `POST /api/v1/calculate/profitability` and use this:

```json
{
  "driver_current": {"lat": 28.6139, "lng": 77.2090, "address": "Delhi"},
  "driver_destination": {"lat": 28.7041, "lng": 77.1025, "address": "Rohini"},
  "vendor_pickup": {"lat": 28.6517, "lng": 77.2219, "address": "CP"},
  "vendor_destination": {"lat": 28.6900, "lng": 77.1500, "address": "Pitampura"},
  "vendor_offering": 5000
}
```

**✅ This works immediately - no database needed!**

---

## 🗄️ Option 2: Run WITH Database (Full Features)

**Needed for: trips, loads, drivers, vendors, full workflow**

### Step 1: Install PostgreSQL

#### Windows:
1. Download from: https://www.postgresql.org/download/windows/
2. Run installer (use default settings)
3. Remember the password you set for `postgres` user

#### Mac:
```bash
brew install postgresql
brew services start postgresql
```

#### Linux:
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

### Step 2: Create Database

Open terminal/command prompt:

```bash
# Windows (use psql from Start Menu or CMD)
psql -U postgres

# Mac/Linux
psql postgres

# Then in psql:
CREATE DATABASE deadheading_db;
\q
```

### Step 3: Update .env File

Update your `.env` with correct database credentials:

```env
# Replace 'user' and 'password' with your PostgreSQL credentials
DATABASE_URL=postgresql+asyncpg://postgres:your_password@localhost:5432/deadheading_db
```

### Step 4: Run Database Migrations

```bash
# This creates all tables
alembic upgrade head
```

### Step 5: Add Sample Data

Run the seed script (I'll create this for you):

```bash
python seed_database.py
```

### Step 6: Start Server

```bash
python main.py
```

Now you can use ALL endpoints!

---

## 🎯 What Works Without Database

✅ **Math Engine APIs:**
- `POST /api/v1/calculate/profitability` - Calculate load profitability
- `GET /health` - Health check
- `GET /` - API info

❌ **Requires Database:**
- Trip management (create, get, update trips)
- Load management (create, get, update loads)
- AI load matching (needs loads from database)
- Driver/Vendor/Owner management

---

## 💡 Recommendation for Hackathon

**Start with Option 1 (No Database):**
1. Demo the Math Engine calculations
2. Show profitability analysis
3. Explain the AI agent architecture

**Then add Option 2 if time permits:**
1. Set up database
2. Show full workflow
3. Demo AI load matching

---

## 🆘 Troubleshooting

### "Can't connect to database"
- You're trying to use database endpoints without setup
- Either set up PostgreSQL OR use only Math Engine endpoints

### "Database doesn't exist"
- Run: `createdb deadheading_db` (Mac/Linux)
- Or use psql to create it (Windows)

### "Wrong password"
- Update DATABASE_URL in .env with correct password
- Default user is usually `postgres`
