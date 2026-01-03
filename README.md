# ChainWatch

**AI-Powered Supply Chain Risk Monitoring System**

ChainWatch is an agentic MVP that monitors supply chain risks using orchestrated AI agents, LLMs for intelligent classification, and live external data sources. It provides real-time risk assessments for major global ports.

![Risk Levels](https://img.shields.io/badge/Risk%20Levels-Low%20%7C%20Medium%20%7C%20High-brightgreen)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Next.js](https://img.shields.io/badge/Next.js-14-black)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Features

- **Multi-Agent Architecture** - Orchestrated agents for news, weather, and port analysis
- **AI-Powered Classification** - GPT-4o-mini for news event classification and explanations
- **Real-Time Data** - Live weather and news feeds from external APIs
- **Dynamic Risk Scoring** - Weighted aggregation with transparent breakdowns
- **Interactive Dashboard** - Sleek Next.js frontend with ambient risk-based theming
- **AI Chatbot** - Ask questions about the current risk assessment

## Demo Regions

| Region | Port | Coordinates |
|--------|------|-------------|
| Shanghai | Shanghai Port | 31.2304, 121.4737 |
| Rotterdam | Port of Rotterdam | 51.9225, 4.4792 |
| Los Angeles | Port of LA | 33.7405, -118.2760 |

---

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- API Keys:
  - [OpenAI](https://platform.openai.com) - For AI classification
  - [NewsAPI](https://newsapi.org) - For news data
  - [OpenWeatherMap](https://openweathermap.org/api) - For weather data

### 1. Clone & Setup Backend

```bash
# Clone the repository
git clone <repository-url>
cd chainWatch

# Create Python virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env
```

Edit `.env` with your API keys:

```env
OPENAI_API_KEY=sk-your-openai-key
NEWS_API_KEY=your-newsapi-key
OPENWEATHER_API_KEY=your-openweather-key
```

### 3. Start Backend Server

```bash
# From project root
uvicorn backend.main:app --reload --port 8000
```

Backend will be available at `http://localhost:8000`

### 4. Setup & Start Frontend

```bash
# Open new terminal
cd frontend-next

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at `http://localhost:3000`

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Next.js Dashboard                     │
│         (Region Selection, Risk Display, Chat)          │
└─────────────────────────┬───────────────────────────────┘
                          │ HTTP/REST
┌─────────────────────────▼───────────────────────────────┐
│                    FastAPI Backend                       │
│                     /analyze/{region}                    │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────┐
│                     Orchestrator                         │
│            (Coordinates all agents sequentially)         │
└───────┬─────────────────┼─────────────────┬─────────────┘
        │                 │                 │
        ▼                 ▼                 ▼
┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│  News Agent   │ │ Weather Agent │ │  Port Agent   │
│   (LLM + API) │ │  (Rules + API)│ │  (Mock Data)  │
└───────────────┘ └───────────────┘ └───────────────┘
        │                 │                 │
        └─────────────────┼─────────────────┘
                          ▼
              ┌───────────────────────┐
              │  Aggregation Agent    │
              │  (Weighted Formula)   │
              └───────────┬───────────┘
                          ▼
              ┌───────────────────────┐
              │  Explanation Agent    │
              │  (LLM Summary)        │
              └───────────────────────┘
```

## Risk Calculation

Risk scores are calculated using transparent weighted aggregation:

```
Risk Score = 0.4 × News + 0.3 × Weather + 0.3 × Port
```

| Risk Level | Score Range | Color |
|------------|-------------|-------|
| Low | < 2.5 | Green |
| Medium | 2.5 - 3.5 | Amber |
| High | > 3.5 | Red |

---

## API Reference

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/regions` | List available regions |
| POST | `/analyze/{region}` | Run full risk analysis |
| GET | `/state` | Get current system state |
| GET | `/state/summary` | Get state summary |
| POST | `/chat` | Chat with AI about risks |

### Example: Analyze Region

```bash
curl -X POST http://localhost:8000/analyze/Shanghai
```

Response:
```json
{
  "region": "Shanghai",
  "timestamp": "2024-01-15T10:30:00Z",
  "news_risk": {
    "event_type": "strike",
    "severity": 3,
    "summary": "Minor labor disputes reported..."
  },
  "weather_risk": {
    "weather_condition": "clear sky",
    "severity": 1,
    "temperature_c": 12.5
  },
  "port_risk": {
    "congestion_level": "moderate",
    "severity": 3,
    "vessel_queue": 25
  },
  "aggregated_risk": {
    "risk_score": 2.4,
    "risk_level": "Low"
  },
  "explanation": "Shanghai is currently at low risk..."
}
```

---

## Project Structure

```
chainWatch/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration management
│   ├── state.py             # In-memory state store
│   ├── orchestrator/
│   │   └── orchestrator.py  # Agent coordination
│   ├── agents/
│   │   ├── news_agent.py    # News risk assessment
│   │   ├── weather_agent.py # Weather risk assessment
│   │   ├── port_agent.py    # Port congestion assessment
│   │   ├── aggregation_agent.py
│   │   └── explanation_agent.py
│   ├── services/
│   │   ├── news_api.py      # NewsAPI client
│   │   ├── weather_api.py   # OpenWeatherMap client
│   │   └── llm_service.py   # OpenAI integration
│   └── models/
│       └── schemas.py       # Pydantic models
├── frontend-next/
│   ├── app/                 # Next.js app router
│   ├── components/          # React components
│   └── lib/                 # API client & utilities
├── .env.example             # Environment template
├── requirements.txt         # Python dependencies
├── CLAUDE.md               # Developer documentation
└── README.md               # This file
```

---

## Development

### Running Tests

```bash
# Backend tests (when implemented)
pytest

# Frontend linting
cd frontend-next && npm run lint
```

### Building for Production

```bash
# Backend
uvicorn backend.main:app --host 0.0.0.0 --port 8000

# Frontend
cd frontend-next
npm run build
npm start
```

---

## Troubleshooting

### Backend won't start

1. Ensure virtual environment is activated
2. Check all dependencies are installed: `pip install -r requirements.txt`
3. Verify `.env` file exists with valid API keys

### Frontend connection errors

1. Ensure backend is running on port 8000
2. Check browser console for CORS errors
3. Verify `NEXT_PUBLIC_API_URL` if customized

### No news results

NewsAPI free tier limits requests. The system handles this gracefully with fallback responses.

### API rate limits

- NewsAPI: 100 requests/day (free tier)
- OpenWeatherMap: 1000 requests/day (free tier)
- OpenAI: Based on your plan

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- [OpenAI](https://openai.com) - GPT-4o-mini for AI classification
- [NewsAPI](https://newsapi.org) - News data provider
- [OpenWeatherMap](https://openweathermap.org) - Weather data provider
- [Vercel](https://vercel.com) - Next.js framework

---

<p align="center">
  <strong>ChainWatch</strong> - Built with AI-powered intelligence
</p>
