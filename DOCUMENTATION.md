# ChainWatch Documentation

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Getting Started](#getting-started)
4. [Configuration](#configuration)
5. [API Reference](#api-reference)
6. [Components](#components)
7. [Development Guide](#development-guide)
8. [Deployment](#deployment)
9. [Troubleshooting](#troubleshooting)
10. [Contributing](#contributing)

---

## Overview

### What is ChainWatch?

ChainWatch is an AI-powered supply chain risk monitoring system that uses orchestrated AI agents to assess risks for major global ports. The system combines:

-   **Multi-Agent Architecture**: Specialized agents for news, weather, and port analysis
-   **LLM-Powered Intelligence**: GPT-4o-mini for intelligent classification and explanation generation
-   **Real-Time Data**: Live weather and news feeds from external APIs
-   **Interactive Dashboard**: Modern Next.js frontend with dynamic risk-based theming
-   **AI Chatbot**: Natural language interface for querying risk assessments

### Key Features

| Feature                  | Description                                                        |
| ------------------------ | ------------------------------------------------------------------ |
| **Multi-Agent System**   | Orchestrated agents work together to assess different risk factors |
| **Real-Time Analysis**   | Live data from news and weather APIs                               |
| **Dynamic Risk Scoring** | Weighted aggregation with transparent breakdowns                   |
| **Interactive UI**       | Responsive dashboard with ambient theming                          |
| **AI Chatbot**           | Ask questions about current risk assessments                       |
| **State Management**     | In-memory state store for real-time updates                        |

### Supported Regions

| Region      | Port              | Coordinates        | Key Features                   |
| ----------- | ----------------- | ------------------ | ------------------------------ |
| Shanghai    | Shanghai Port     | 31.2304, 121.4737  | World's busiest container port |
| Rotterdam   | Port of Rotterdam | 51.9225, 4.4792    | Europe's largest port          |
| Los Angeles | Port of LA        | 33.7405, -118.2760 | US West Coast gateway          |

---

## Architecture

### System Overview

ChainWatch follows a multi-layered architecture:

```
┌─────────────────────────────────────────────────────────┐
│                   Frontend Layer                        │
│              (Next.js 14 + React 18)                     │
│  Dashboard, Risk Visualization, Chat Interface          │
└─────────────────────────┬───────────────────────────────┘
                          │ HTTP/REST API
┌─────────────────────────▼───────────────────────────────┐
│                    API Layer                             │
│                   (FastAPI)                              │
│  Endpoints, CORS, Request/Response Handling            │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────┐
│                Orchestration Layer                      │
│                  Orchestrator                           │
│  Coordinates agents, manages state, handles errors     │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────┐
│                   Agent Layer                            │
│  NewsAgent, WeatherAgent, PortAgent,                    │
│  AggregationAgent, ExplanationAgent                     │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────┐
│                   Service Layer                          │
│  LLMService, NewsAPI, WeatherAPI                        │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────┐
│                External Services                         │
│  OpenAI API, NewsAPI, OpenWeatherMap                    │
└─────────────────────────────────────────────────────────┘
```

### Data Flow

1. **User Interaction**: User selects region and initiates analysis
2. **API Request**: Frontend sends POST request to `/analyze/{region}`
3. **Orchestration**: Orchestrator coordinates sequential agent execution
4. **Data Collection**: Agents fetch data from external APIs
5. **AI Processing**: LLM classifies risks and generates explanations
6. **Aggregation**: Risk scores combined using weighted formula
7. **State Update**: Results stored in global state store
8. **Response**: Complete system state returned to frontend
9. **Visualization**: Dashboard displays risk assessment

### Risk Calculation Formula

```
Risk Score = (0.4 × News Severity) + (0.3 × Weather Severity) + (0.3 × Port Severity)
```

**Risk Levels:**

| Risk Level | Score Range | Color | Action Required             |
| ---------- | ----------- | ----- | --------------------------- |
| Low        | < 2.5       | Green | Normal operations           |
| Medium     | 2.5 - 3.5   | Amber | Monitor closely             |
| High       | > 3.5       | Red   | Take precautionary measures |

---

## Getting Started

### Prerequisites

-   **Python**: 3.11 or higher
-   **Node.js**: 18 or higher
-   **npm**: 9 or higher
-   **API Keys**:
    -   [OpenAI API Key](https://platform.openai.com/api-keys)
    -   [NewsAPI Key](https://newsapi.org/register)
    -   [OpenWeatherMap API Key](https://openweathermap.org/api)

### Installation Steps

#### 1. Clone the Repository

```bash
git clone <repository-url>
cd chainWatch
```

#### 2. Backend Setup

```bash
# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

#### 3. Environment Configuration

```bash
# Copy environment template
cp .env.example .env
```

Edit `.env` file with your API keys:

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here

# NewsAPI Configuration
NEWS_API_KEY=your-newsapi-key-here

# OpenWeatherMap Configuration
OPENWEATHER_API_KEY=your-openweather-api-key-here

# Backend URL (optional, defaults to localhost:8000)
BACKEND_URL=http://localhost:8000
```

#### 4. Start Backend Server

```bash
# From project root directory
uvicorn backend.main:app --reload --port 8000
```

Backend will be available at `http://localhost:8000`

Verify it's running:

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{
	"status": "healthy",
	"service": "chainwatch-api"
}
```

#### 5. Frontend Setup

Open a new terminal:

```bash
# Navigate to frontend directory
cd frontend-next

# Install Node.js dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at `http://localhost:3000`

#### 6. Access the Application

Open your browser and navigate to `http://localhost:3000`

You should see the ChainWatch dashboard with:

-   Region selector
-   Analyze button
-   Risk meter (initially empty)
-   Chat interface

### Quick Test

1. Select a region (e.g., "Shanghai")
2. Click "Analyze Region"
3. Wait for the analysis to complete
4. View the risk assessment dashboard
5. Try asking a question in the chat

---

## Configuration

### Backend Configuration

Configuration is managed through [`backend/config.py`](backend/config.py:1) using Pydantic Settings.

#### Environment Variables

| Variable              | Required | Default                 | Description                    |
| --------------------- | -------- | ----------------------- | ------------------------------ |
| `OPENAI_API_KEY`      | Yes      | -                       | OpenAI API key for GPT-4o-mini |
| `NEWS_API_KEY`        | Yes      | -                       | NewsAPI key for news data      |
| `OPENWEATHER_API_KEY` | Yes      | -                       | OpenWeatherMap API key         |
| `BACKEND_URL`         | No       | `http://localhost:8000` | Backend API URL                |

#### Region Configuration

Regions are configured in [`backend/config.py`](backend/config.py:14):

```python
regions: dict = {
    "Shanghai": {
        "lat": 31.2304,
        "lon": 121.4737,
        "port": "Shanghai Port"
    },
    "Rotterdam": {
        "lat": 51.9225,
        "lon": 4.4792,
        "port": "Port of Rotterdam"
    },
    "Los Angeles": {
        "lat": 33.7405,
        "lon": -118.2760,
        "port": "Port of Los Angeles"
    }
}
```

To add a new region, add an entry to this dictionary.

### Frontend Configuration

Frontend configuration is in [`frontend-next/.env.local.example`](frontend-next/.env.local.example:1):

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Copy this to `.env.local` and modify if your backend is on a different URL.

---

## API Reference

### Base URL

```
http://localhost:8000
```

### Authentication

Currently, no authentication is required. In production, implement API keys or OAuth.

### Endpoints

#### 1. Health Check

**GET** `/health`

Check if the API is running.

**Response:**

```json
{
	"status": "healthy",
	"service": "chainwatch-api"
}
```

---

#### 2. Get Available Regions

**GET** `/regions`

Get list of available regions for analysis.

**Response:**

```json
{
	"regions": ["Shanghai", "Rotterdam", "Los Angeles"],
	"details": {
		"Shanghai": {
			"lat": 31.2304,
			"lon": 121.4737,
			"port": "Shanghai Port"
		},
		"Rotterdam": {
			"lat": 51.9225,
			"lon": 4.4792,
			"port": "Port of Rotterdam"
		},
		"Los Angeles": {
			"lat": 33.7405,
			"lon": -118.276,
			"port": "Port of Los Angeles"
		}
	}
}
```

---

#### 3. Analyze Region

**POST** `/analyze/{region}`

Run full risk analysis for a specific region.

**Parameters:**

-   `region` (path parameter): Region name (e.g., "Shanghai", "Rotterdam", "Los Angeles")

**Response (200 OK):**

```json
{
	"region": "Shanghai",
	"timestamp": "2024-01-15T10:30:00.123456",
	"news_risk": {
		"event_type": "strike",
		"severity": 3,
		"summary": "Minor labor disputes reported at Shanghai Port...",
		"sources": [
			"Port strike delays shipments",
			"Union negotiations ongoing"
		]
	},
	"weather_risk": {
		"weather_condition": "clear sky",
		"severity": 1,
		"details": "Clear conditions with light winds. Temperature: 12.5°C, Wind: 15 km/h",
		"temperature_c": 12.5,
		"wind_speed_kmh": 15.0,
		"rainfall_mm": 0.0
	},
	"port_risk": {
		"congestion_level": "moderate",
		"severity": 3,
		"details": "Moderate congestion with 25 vessels waiting. Average delay: 12 hours",
		"vessel_queue": 25,
		"avg_delay_hours": 12.0
	},
	"aggregated_risk": {
		"risk_score": 2.4,
		"risk_level": "Low",
		"breakdown": {
			"news": 3,
			"weather": 1,
			"port": 3,
			"weights": {
				"news": 0.4,
				"weather": 0.3,
				"port": 0.3
			}
		}
	},
	"explanation": "Shanghai is currently at low risk. Weather conditions are favorable with clear skies, though there are moderate port delays and minor labor disputes. Operations can proceed normally with routine monitoring.",
	"status": "completed",
	"error_message": null
}
```

**Error Response (400 Bad Request):**

```json
{
	"detail": "Invalid region: UnknownRegion. Valid options: ['Shanghai', 'Rotterdam', 'Los Angeles']"
}
```

**Error Response (500 Internal Server Error):**

```json
{
	"detail": "Error message from backend"
}
```

---

#### 4. Get Current State

**GET** `/state`

Get the current system state from the last analysis.

**Response (200 OK):**

```json
{
  "region": "Shanghai",
  "timestamp": "2024-01-15T10:30:00.123456",
  "news_risk": { ... },
  "weather_risk": { ... },
  "port_risk": { ... },
  "aggregated_risk": { ... },
  "explanation": "...",
  "status": "completed"
}
```

**Response (200 OK - No Data):**

```json
null
```

---

#### 5. Get State Summary

**GET** `/state/summary`

Get a summary of the current state.

**Response (200 OK):**

```json
{
	"status": "ok",
	"region": "Shanghai",
	"risk_level": "Low",
	"risk_score": 2.4,
	"last_updated": "2024-01-15T10:30:00.123456"
}
```

**Response (200 OK - No Data):**

```json
{
	"status": "no_data",
	"message": "No analysis has been run yet."
}
```

---

#### 6. Chat with AI

**POST** `/chat`

Ask a question about the current risk assessment.

**Request Body:**

```json
{
	"message": "What is the current weather risk level?",
	"region": "Shanghai"
}
```

**Response (200 OK):**

```json
{
	"response": "The current weather risk level is 1/5 (Low). Weather conditions are clear with light winds at 15 km/h and temperature of 12.5°C.",
	"based_on_data": true
}
```

**Response (200 OK - No Data):**

```json
{
	"response": "No risk assessment data is available. Please run an analysis first by selecting a region.",
	"based_on_data": false
}
```

---

### API Rate Limits

| Service        | Free Tier Limit   | Current Usage   |
| -------------- | ----------------- | --------------- |
| NewsAPI        | 100 requests/day  | ~1 per analysis |
| OpenWeatherMap | 1000 requests/day | ~1 per analysis |
| OpenAI         | Based on plan     | ~3 per analysis |

---

## Components

### Backend Components

#### 1. Main Application ([`backend/main.py`](backend/main.py:1))

FastAPI application with REST endpoints.

**Key Functions:**

-   `health_check()` - Health check endpoint
-   `get_regions()` - List available regions
-   `analyze_region()` - Run full risk analysis
-   `get_current_state()` - Get current system state
-   `get_state_summary()` - Get state summary
-   `chat()` - Chat with AI about risks

**Middleware:**

-   CORS enabled for frontend communication

---

#### 2. Orchestrator ([`backend/orchestrator/orchestrator.py`](backend/orchestrator/orchestrator.py:1))

Central coordinator that manages all risk assessment agents.

**Key Methods:**

-   `analyze(region)` - Run full risk analysis pipeline
-   `get_available_regions()` - Get list of available regions

**Execution Order:**

1. News Risk Agent
2. Weather Risk Agent
3. Port Risk Agent
4. Risk Aggregation Agent
5. Explanation Agent

---

#### 3. Agents ([`backend/agents/`](backend/agents/))

Specialized agents for different risk assessments.

##### BaseAgent ([`backend/agents/base.py`](backend/agents/base.py:1))

Abstract base class for all agents.

**Methods:**

-   `run(region)` - Execute agent's risk assessment

##### NewsAgent ([`backend/agents/news_agent.py`](backend/agents/news_agent.py:1))

Analyzes news articles for supply chain disruption risks.

**Process:**

1. Fetches news articles from NewsAPI
2. Sends articles to LLM for classification
3. Returns event type, severity, and summary

**Event Types:**

-   strike
-   conflict
-   disaster
-   pandemic
-   policy
-   weather
-   infrastructure
-   none

##### WeatherAgent ([`backend/agents/weather_agent.py`](backend/agents/weather_agent.py:1))

Assesses weather-related risks for a region.

**Process:**

1. Fetches current weather from OpenWeatherMap
2. Analyzes weather conditions
3. Returns severity score and details

**Weather Conditions:**

-   Clear sky
-   Cloudy
-   Rain
-   Storm
-   Snow
-   etc.

##### PortAgent ([`backend/agents/port_agent.py`](backend/agents/port_agent.py:1))

Analyzes port congestion and operational risks.

**Process:**

1. Fetches port data (currently simulated)
2. Analyzes congestion level
3. Returns severity score and queue information

**Congestion Levels:**

-   low
-   moderate
-   high
-   critical

##### AggregationAgent ([`backend/agents/aggregation_agent.py`](backend/agents/aggregation_agent.py:1))

Combines individual risk scores into an overall risk assessment.

**Formula:**

```
Risk Score = (0.4 × News) + (0.3 × Weather) + (0.3 × Port)
```

**Returns:**

-   Overall risk score (1-5)
-   Risk level (Low/Medium/High)
-   Breakdown of individual components

##### ExplanationAgent ([`backend/agents/explanation_agent.py`](backend/agents/explanation_agent.py:1))

Generates plain-language explanation of the risk assessment.

**Process:**

1. Collects all risk data
2. Sends to LLM for explanation generation
3. Returns clear, stakeholder-friendly summary

---

#### 4. Services ([`backend/services/`](backend/services/))

External API integrations.

##### LLMService ([`backend/services/llm_service.py`](backend/services/llm_service.py:1))

OpenAI integration for AI-powered analysis.

**Methods:**

-   `classify_news_risk(news_articles)` - Classify news for supply chain risk
-   `generate_explanation(...)` - Generate plain-language explanation
-   `answer_chat_question(question, system_state)` - Answer user questions

**Model:** GPT-4o-mini

##### NewsAPI ([`backend/services/news_api.py`](backend/services/news_api.py:1))

NewsAPI client for fetching news articles.

**Methods:**

-   `get_news(query, language, page_size)` - Fetch news articles

##### WeatherAPI ([`backend/services/weather_api.py`](backend/services/weather_api.py:1))

OpenWeatherMap client for weather data.

**Methods:**

-   `get_weather(lat, lon)` - Fetch current weather

---

#### 5. Models ([`backend/models/schemas.py`](backend/models/schemas.py:1))

Pydantic models for data validation.

**Key Models:**

-   `NewsRiskOutput` - News risk assessment output
-   `WeatherRiskOutput` - Weather risk assessment output
-   `PortRiskOutput` - Port risk assessment output
-   `AggregatedRisk` - Aggregated risk output
-   `SystemState` - Complete system state
-   `ChatRequest` - Chat request schema
-   `ChatResponse` - Chat response schema

---

#### 6. State Store ([`backend/state.py`](backend/state.py:1))

In-memory state store for system outputs.

**Methods:**

-   `update(state)` - Update current state
-   `get()` - Get current state
-   `get_last_updated()` - Get last update timestamp
-   `clear()` - Clear current state

---

### Frontend Components

#### 1. Dashboard ([`frontend-next/app/page.tsx`](frontend-next/app/page.tsx:1))

Main dashboard component.

**Features:**

-   Region selection
-   Analysis triggering
-   Risk display
-   Chat interface
-   Error handling

---

#### 2. Components ([`frontend-next/components/`](frontend-next/components/))

| Component               | Description                                  |
| ----------------------- | -------------------------------------------- |
| `Header.tsx`            | Application header with risk level indicator |
| `RegionSelector.tsx`    | Dropdown for region selection                |
| `AnalyzeButton.tsx`     | Button to trigger analysis                   |
| `RiskMeter.tsx`         | Visual risk meter with gauge                 |
| `RiskCard.tsx`          | Individual risk cards (News, Weather, Port)  |
| `ChatBot.tsx`           | AI chatbot interface                         |
| `EmptyState.tsx`        | Placeholder when no data available           |
| `BackgroundEffects.tsx` | Ambient background effects based on risk     |

---

#### 3. API Client ([`frontend-next/lib/api.ts`](frontend-next/lib/api.ts))

API client for backend communication.

**Functions:**

-   `getRegions()` - Fetch available regions
-   `analyzeRegion(region)` - Run analysis
-   `getCurrentState()` - Get current state
-   `chat(message)` - Send chat message

---

#### 4. Types ([`frontend-next/lib/types.ts`](frontend-next/lib/types.ts))

TypeScript type definitions.

**Key Types:**

-   `SystemState` - Complete system state
-   `RiskLevel` - Risk level type
-   `NewsRisk`, `WeatherRisk`, `PortRisk` - Individual risk types

---

## Development Guide

### Backend Development

#### Project Structure

```
backend/
├── main.py              # FastAPI application
├── config.py            # Configuration
├── state.py             # State management
├── orchestrator/
│   └── orchestrator.py  # Agent coordination
├── agents/
│   ├── base.py          # Base agent class
│   ├── news_agent.py    # News risk agent
│   ├── weather_agent.py # Weather risk agent
│   ├── port_agent.py    # Port risk agent
│   ├── aggregation_agent.py
│   └── explanation_agent.py
├── services/
│   ├── llm_service.py   # LLM integration
│   ├── news_api.py      # NewsAPI client
│   └── weather_api.py   # Weather API client
└── models/
    └── schemas.py       # Pydantic models
```

#### Adding a New Agent

1. Create new agent file in `backend/agents/`
2. Inherit from `BaseAgent`
3. Implement `run(region)` method
4. Register in `Orchestrator.__init__()`
5. Add to analysis pipeline in `Orchestrator.analyze()`

Example:

```python
from backend.agents.base import BaseAgent

class CustomAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Custom Agent")

    async def run(self, region: str) -> dict:
        # Your implementation
        return {
            "severity": 1,
            "details": "Custom analysis result"
        }
```

#### Adding a New Region

Edit [`backend/config.py`](backend/config.py:14):

```python
regions: dict = {
    "Shanghai": {...},
    "Rotterdam": {...},
    "Los Angeles": {...},
    "NewRegion": {
        "lat": 0.0,
        "lon": 0.0,
        "port": "New Port"
    }
}
```

#### Testing

Run backend tests (when implemented):

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=backend --cov-report=html
```

---

### Frontend Development

#### Project Structure

```
frontend-next/
├── app/
│   ├── layout.tsx        # Root layout
│   ├── page.tsx          # Dashboard page
│   └── globals.css       # Global styles
├── components/
│   ├── Header.tsx
│   ├── RegionSelector.tsx
│   ├── AnalyzeButton.tsx
│   ├── RiskMeter.tsx
│   ├── RiskCard.tsx
│   ├── ChatBot.tsx
│   ├── EmptyState.tsx
│   └── BackgroundEffects.tsx
├── lib/
│   ├── api.ts            # API client
│   └── types.ts          # TypeScript types
└── package.json
```

#### Adding a New Component

1. Create component file in `frontend-next/components/`
2. Export from `frontend-next/components/index.ts`
3. Import and use in page or other components

Example:

```typescript
// components/NewComponent.tsx
export function NewComponent() {
	return <div className="new-component">{/* Component content */}</div>;
}

// components/index.ts
export { NewComponent } from "./NewComponent";
```

#### Styling

The project uses Tailwind CSS. Add styles using utility classes:

```typescript
<div className="bg-white rounded-lg shadow-md p-4">{/* Content */}</div>
```

Custom styles are in `app/globals.css`.

#### Development

Start development server:

```bash
cd frontend-next
npm run dev
```

Build for production:

```bash
npm run build
```

Run production build:

```bash
npm start
```

Lint code:

```bash
npm run lint
```

---

## Deployment

### Backend Deployment

#### Using Docker

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -t chainwatch-backend .
docker run -p 8000:8000 --env-file .env chainwatch-backend
```

#### Using Cloud Services

**AWS (Elastic Beanstalk):**

```bash
eb init
eb create production
```

**Google Cloud (App Engine):**

```bash
gcloud app deploy
```

**Heroku:**

```bash
heroku create chainwatch-backend
git push heroku main
```

### Frontend Deployment

#### Vercel (Recommended)

1. Connect repository to Vercel
2. Configure environment variables
3. Deploy automatically on push

#### Netlify

```bash
npm run build
netlify deploy --prod
```

#### Docker

Create `Dockerfile`:

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
```

Build and run:

```bash
docker build -t chainwatch-frontend .
docker run -p 3000:3000 chainwatch-frontend
```

### Environment Variables for Production

Set these environment variables in your hosting platform:

**Backend:**

-   `OPENAI_API_KEY`
-   `NEWS_API_KEY`
-   `OPENWEATHER_API_KEY`
-   `BACKEND_URL` (production URL)

**Frontend:**

-   `NEXT_PUBLIC_API_URL` (production backend URL)

---

## Troubleshooting

### Common Issues

#### Backend won't start

**Symptoms:** Error when running `uvicorn backend.main:app`

**Solutions:**

1. Ensure virtual environment is activated
2. Check all dependencies are installed:
    ```bash
    pip install -r requirements.txt
    ```
3. Verify `.env` file exists with valid API keys
4. Check Python version (3.11+ required):
    ```bash
    python --version
    ```

#### Frontend connection errors

**Symptoms:** Frontend can't connect to backend

**Solutions:**

1. Ensure backend is running on port 8000
2. Check browser console for CORS errors
3. Verify `NEXT_PUBLIC_API_URL` in frontend
4. Check backend logs for errors

#### No news results

**Symptoms:** News risk shows "No relevant news found"

**Solutions:**

1. Check NewsAPI key is valid
2. Verify API quota not exceeded (100 requests/day free tier)
3. Try a different region
4. Check NewsAPI status page

#### API rate limits exceeded

**Symptoms:** API returns rate limit errors

**Solutions:**

1. Check API usage:
    - NewsAPI: 100 requests/day (free tier)
    - OpenWeatherMap: 1000 requests/day (free tier)
    - OpenAI: Based on your plan
2. Upgrade to paid tier if needed
3. Implement caching to reduce API calls

#### LLM errors

**Symptoms:** LLM service returns errors

**Solutions:**

1. Verify OpenAI API key is valid
2. Check OpenAI account has credits
3. Verify model name (gpt-4o-mini)
4. Check OpenAI status page

#### Weather data not updating

**Symptoms:** Weather data is stale or incorrect

**Solutions:**

1. Check OpenWeatherMap API key
2. Verify coordinates are correct
3. Check OpenWeatherMap status page
4. Try a different region

#### Frontend build errors

**Symptoms:** `npm run build` fails

**Solutions:**

1. Clear cache:
    ```bash
    rm -rf .next node_modules
    npm install
    ```
2. Check Node.js version (18+ required):
    ```bash
    node --version
    ```
3. Check for TypeScript errors:
    ```bash
    npm run lint
    ```

### Debugging

#### Backend Debugging

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Use Python debugger:

```python
import pdb; pdb.set_trace()
```

#### Frontend Debugging

Check browser console for errors:

-   Press F12
-   Go to Console tab
-   Look for red error messages

Use React DevTools:

-   Install React DevTools extension
-   Inspect component state and props

### Getting Help

1. Check this documentation
2. Review error messages carefully
3. Check API status pages:
    - [OpenAI Status](https://status.openai.com)
    - [NewsAPI Status](https://newsapi.org/docs)
    - [OpenWeatherMap Status](https://openweathermap.org/status)
4. Search existing issues on GitHub
5. Open a new issue with:
    - Error message
    - Steps to reproduce
    - Environment details (OS, Python/Node versions)

---

## Contributing

### Contribution Guidelines

We welcome contributions! Please follow these guidelines:

#### Code Style

**Python:**

-   Follow PEP 8 style guide
-   Use type hints where appropriate
-   Write docstrings for functions and classes
-   Maximum line length: 88 characters (Black default)

**TypeScript:**

-   Use ESLint and Prettier
-   Follow existing code style
-   Use TypeScript strict mode
-   Add JSDoc comments for complex functions

#### Commit Messages

Use conventional commits:

```
feat: add new agent for custom risk assessment
fix: resolve weather API connection issue
docs: update API documentation
style: format code with black
refactor: simplify orchestrator logic
test: add unit tests for news agent
chore: update dependencies
```

#### Pull Request Process

1. Fork the repository
2. Create a feature branch:
    ```bash
    git checkout -b feature/amazing-feature
    ```
3. Make your changes
4. Write tests for new functionality
5. Update documentation
6. Commit your changes:
    ```bash
    git commit -m 'feat: add amazing feature'
    ```
7. Push to branch:
    ```bash
    git push origin feature/amazing-feature
    ```
8. Open a Pull Request
9. Respond to code review feedback

#### Testing Requirements

-   All tests must pass
-   New features must include tests
-   Maintain test coverage above 80%

#### Documentation Requirements

-   Update README for user-facing changes
-   Update API documentation for API changes
-   Add inline comments for complex logic
-   Update this documentation for architectural changes

### Development Workflow

1. **Setup**: Follow the Getting Started guide
2. **Develop**: Make changes in your feature branch
3. **Test**: Run tests locally
4. **Document**: Update relevant documentation
5. **Submit**: Open a pull request
6. **Review**: Respond to feedback
7. **Merge**: Once approved, your PR will be merged

### Reporting Issues

When reporting bugs, please include:

-   **Description**: Clear description of the issue
-   **Steps to Reproduce**: Detailed steps to reproduce the issue
-   **Expected Behavior**: What you expected to happen
-   **Actual Behavior**: What actually happened
-   **Environment**:
    -   OS and version
    -   Python version
    -   Node.js version
    -   Browser (if frontend issue)
-   **Logs**: Relevant error messages or logs
-   **Screenshots**: If applicable

### Feature Requests

We welcome feature requests! Please include:

-   **Description**: Clear description of the feature
-   **Use Case**: Why this feature would be useful
-   **Proposed Solution**: How you envision the feature working
-   **Alternatives**: Any alternative solutions considered

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

-   [OpenAI](https://openai.com) - GPT-4o-mini for AI classification
-   [NewsAPI](https://newsapi.org) - News data provider
-   [OpenWeatherMap](https://openweathermap.org) - Weather data provider
-   [Vercel](https://vercel.com) - Next.js framework
-   [FastAPI](https://fastapi.tiangolo.com) - Modern Python web framework
-   [Tailwind CSS](https://tailwindcss.com) - Utility-first CSS framework

---

## Support

For questions, issues, or contributions:

-   **Documentation**: This file and [`README.md`](README.md:1)
-   **Architecture**: See [`architecture.md`](architecture.md:1)
-   **Issues**: [GitHub Issues](https://github.com/your-repo/chainWatch/issues)
-   **Discussions**: [GitHub Discussions](https://github.com/your-repo/chainWatch/discussions)

---

**ChainWatch** - Built with AI-powered intelligence for supply chain risk monitoring.
