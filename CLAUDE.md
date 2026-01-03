# ChainWatch - AI-Based Supply Chain Risk Monitoring System

## Overview

ChainWatch is an agentic MVP for supply chain risk monitoring. It uses orchestrated AI agents, LLMs for classification and explanation, and live external data sources to provide real-time risk assessments.

**Key Principle:** No ML model training. Intelligence comes from LLMs (GPT-4o-mini), deterministic rules, and live data.

## Architecture

```
User Interface (Next.js Dashboard)
            |
            v
    FastAPI Backend
            |
            v
      Orchestrator
            |
  +---------+---------+
  |         |         |
  v         v         v
News    Weather    Port
Agent    Agent    Agent
  |         |         |
  +---------+---------+
            |
            v
  Aggregation Agent
            |
            v
  Explanation Agent
            |
            v
    System State
```

## Tech Stack

- **Backend:** FastAPI (Python 3.11+)
- **Frontend:** Next.js 14 + TypeScript + Tailwind CSS + Framer Motion
- **LLM:** OpenAI GPT-4o-mini
- **News API:** NewsAPI.org
- **Weather API:** OpenWeatherMap
- **HTTP Client:** httpx (async)
- **Validation:** Pydantic v2

## Project Structure

```
chainWatch/
├── backend/
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Environment configuration
│   ├── state.py             # In-memory state store
│   ├── orchestrator/
│   │   └── orchestrator.py  # Central orchestrator
│   ├── agents/
│   │   ├── base.py          # Abstract base agent
│   │   ├── news_agent.py    # News risk assessment
│   │   ├── weather_agent.py # Weather risk assessment
│   │   ├── port_agent.py    # Port congestion assessment
│   │   ├── aggregation_agent.py # Risk aggregation
│   │   └── explanation_agent.py # LLM explanation
│   ├── services/
│   │   ├── news_api.py      # NewsAPI.org client
│   │   ├── weather_api.py   # OpenWeatherMap client
│   │   └── llm_service.py   # OpenAI integration
│   └── models/
│       └── schemas.py       # Pydantic models
├── frontend-next/
│   ├── app/
│   │   ├── layout.tsx       # Root layout
│   │   ├── page.tsx         # Main dashboard
│   │   └── globals.css      # Global styles
│   ├── components/
│   │   ├── Header.tsx       # Dashboard header
│   │   ├── RegionSelector.tsx
│   │   ├── AnalyzeButton.tsx
│   │   ├── RiskMeter.tsx    # Main risk display
│   │   ├── RiskCard.tsx     # Individual risk cards
│   │   ├── ChatBot.tsx      # AI chat interface
│   │   ├── EmptyState.tsx
│   │   └── BackgroundEffects.tsx
│   ├── lib/
│   │   ├── api.ts           # Backend API client
│   │   ├── types.ts         # TypeScript types
│   │   └── utils.ts         # Utilities
│   ├── package.json
│   └── tailwind.config.js
├── .env.example             # Environment template
├── requirements.txt         # Python dependencies
└── CLAUDE.md               # This file
```

## Setup

### 1. Install Backend Dependencies

```bash
cd chainWatch
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your API keys:
- `OPENAI_API_KEY` - From platform.openai.com
- `NEWS_API_KEY` - From newsapi.org
- `OPENWEATHER_API_KEY` - From openweathermap.org

### 3. Run Backend

```bash
cd chainWatch
uvicorn backend.main:app --reload --port 8000
```

### 4. Install & Run Next.js Frontend

```bash
cd chainWatch/frontend-next
npm install
npm run dev
```

Open http://localhost:3000 in your browser.

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/regions` | GET | List available regions |
| `/analyze/{region}` | POST | Run full risk analysis |
| `/state` | GET | Get current system state |
| `/state/summary` | GET | Get state summary |
| `/chat` | POST | Chat with the system |

## Agents

### News Risk Agent
- Fetches supply chain news via NewsAPI
- Uses GPT-4o-mini to classify event type and severity
- Event types: strike, conflict, disaster, pandemic, policy, weather, infrastructure, none

### Weather Risk Agent
- Fetches weather data via OpenWeatherMap
- Applies deterministic thresholds (no LLM)
- Thresholds:
  - Rainfall: >30mm=3, >50mm=4, >80mm=5
  - Wind: >40km/h=3, >60km/h=4, >80km/h=5
  - Temperature: <0C or >40C = severity 3-4

### Port Risk Agent
- Uses mock/static data for demo stability
- Simulates vessel queue and delay metrics
- Demo data for: Shanghai, Rotterdam, Los Angeles

### Risk Aggregation Agent
- Formula: `0.4*news + 0.3*weather + 0.3*port`
- Risk levels: Low (<2.5), Medium (2.5-3.5), High (>3.5)

### Explanation Agent
- Uses GPT-4o-mini to generate plain-language explanations
- References only system-generated facts

## Demo Regions

| Region | Coordinates | Port |
|--------|-------------|------|
| Shanghai | 31.2304, 121.4737 | Shanghai Port |
| Rotterdam | 51.9225, 4.4792 | Port of Rotterdam |
| Los Angeles | 33.7405, -118.2760 | Port of Los Angeles |

## Frontend Features

### Design Aesthetic: "Orbital Command Center"
- Dark theme with deep navy/slate base
- Dynamic ambient glow that shifts based on risk level (green/amber/red)
- Glassmorphism panels with risk-tinted edges
- Radar/sonar-inspired animations
- Orbitron display font + JetBrains Mono for data

### Components
- **Header** - Logo, system status, risk badge
- **Region Selector** - Dropdown with cyber styling
- **Analyze Button** - Triggers full pipeline analysis
- **Risk Meter** - Main score display with breakdown
- **Risk Cards** - News, Weather, Port details
- **ChatBot** - Floating AI assistant panel

## Demo Script

1. Open the dashboard at http://localhost:3000
2. Select "Shanghai" from the region dropdown
3. Click "Analyze Region"
4. Watch the ambient glow change based on risk level
5. Review the risk breakdown cards
6. Read the AI-generated explanation
7. Click the chat bubble to ask questions:
   - "Why is this region high risk?"
   - "What are the weather conditions?"
   - "Are there port delays?"

## Troubleshooting

### API Key Errors
Ensure all API keys are set in `.env` file.

### Connection Errors
1. Verify backend is running on port 8000
2. Frontend expects API at `http://localhost:8000`
3. Check CORS settings if needed

### No News Results
NewsAPI free tier has limitations. The system gracefully handles this with fallback responses.

### Frontend Build Issues
```bash
cd frontend-next
rm -rf node_modules .next
npm install
npm run dev
```

## Future Extensions

- [ ] Event dependency graphs
- [ ] Time-to-impact estimation
- [ ] Scenario simulation
- [ ] ML-based risk calibration
- [ ] Persistent data storage (PostgreSQL)
- [ ] Real port data integration (AIS, port APIs)
- [ ] Multi-user support with authentication
