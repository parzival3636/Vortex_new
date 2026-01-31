# Deadheading Optimization System

AI-powered system to eliminate wasteful empty return trips for trucks using **local Ollama LLM** and CrewAI multi-agent orchestration.

## ✨ Features

- **3 Portals**: Owner Dashboard, Driver Portal, Vendor Portal
- **AI Agents**: Load Matcher, Route Optimizer, Financial Analyzer, Coordinator
- **Local LLM**: Uses Ollama (no OpenAI API key required!)
- **Embedded Database**: ChromaDB (no database server needed!)
- **Real Indian Data**: Actual cities, market yards, and GPS coordinates
- **Profitability Calculation**: Math engine for accurate cost/profit analysis
- **GPS Simulation**: Realistic truck movement tracking

## 🚀 Prerequisites

1. **Python 3.11+**
2. **Ollama** - [Installation Guide](OLLAMA_SETUP.md)

That's it! No database server, no Redis, no external APIs needed.

## ⚡ Quick Start

### 1. Install Ollama

Follow the [Ollama Setup Guide](OLLAMA_SETUP.md) to install and configure Ollama with the recommended model:

```bash
# Install Ollama (see OLLAMA_SETUP.md for platform-specific instructions)

# Pull the recommended model
ollama pull llama3.1:8b

# Verify it's working
ollama run llama3.1:8b "Hello!"
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

The default configuration works out of the box! Edit `.env` only if you want to customize:
```env
# ChromaDB (embedded database - no server needed!)
CHROMA_PERSIST_DIRECTORY=./chroma_data

# Ollama (local LLM)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b

# OpenAI (dummy key for CrewAI compatibility)
OPENAI_API_KEY=dummy-key-not-used
```

### 4. Seed the Database

```bash
python seed_chromadb.py
```

This creates sample data with real Indian cities and market yards.

### 5. Run the Automated Demo

```bash
python demo_automation.py
```

Watch the AI agents in action! The demo shows:
- Driver creates trip from Delhi to Jaipur
- GPS tracking simulation
- AI finds 5 profitable return loads
- Best opportunity: **₹16,886 profit** instead of driving empty!

### 6. Start the API Server

```bash
python main.py
```

The API will be available at http://localhost:8000

## 🧪 Testing

### Run All Tests
```bash
python test_system.py
```

### Individual Test Suites
```bash
python test_math_engine.py  # Math engine tests
python test_api.py          # API endpoint tests
python test_ollama.py       # Ollama integration tests
```

## 📚 API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **API Guide**: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

## 🎯 How It Works

### 1. Driver Creates Trip
Driver enters origin, destination, and outbound load details.

### 2. Mark as Deadheading
After delivery, driver marks the return journey as "no load" (deadheading).

### 3. AI Agent Workflow
- **Load Matcher Agent**: Finds vendor loads within 50km of the return route
- **Route Optimizer Agent**: Calculates distances and travel times
- **Financial Analyzer Agent**: Computes fuel costs, time costs, and net profit
- **Coordinator Agent**: Orchestrates all agents and ranks opportunities

### 4. Driver Receives Recommendations
Top 5 most profitable loads are presented with full calculation breakdown.

### 5. Accept & Navigate
Driver accepts a load and receives navigation to vendor pickup location.

## Project Structure

```
├── api/              # API endpoints (trips, loads, calculations)
├── agents/           # CrewAI agents (coordinator, load_matcher, route_optimizer, financial_analyzer)
├── models/           # Database and domain models
├── services/         # Business logic (math_engine)
├── tests/            # Test files
├── main.py           # FastAPI application
├── database.py       # Database configuration
├── config.py         # Settings management
└── requirements.txt  # Python dependencies
```

## Why Ollama?

- **No API costs**: Run everything locally
- **Privacy**: Your data never leaves your machine
- **Fast**: Local inference with GPU acceleration
- **Flexible**: Switch models easily (llama3.1, mistral, codellama, etc.)

## Troubleshooting

### Ollama not responding
```bash
curl http://localhost:11434/api/tags
```

If this fails, restart Ollama or check the [Ollama Setup Guide](OLLAMA_SETUP.md).

### Database connection errors
Ensure PostgreSQL is running and credentials in `.env` are correct.

### Redis connection errors
Ensure Redis is running: `redis-cli ping` should return `PONG`

## Next Steps

- Implement WebSocket notifications
- Build frontend portals (React/Vue)
- Add authentication
- Deploy with Docker
