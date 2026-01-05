# ChainWatch Application Architecture

## High-Level Architecture

```mermaid
graph TB
    subgraph "Frontend Layer (Next.js)"
        UI[Dashboard UI]
        Components[React Components]
        API_Client[API Client]
    end

    subgraph "API Layer (FastAPI)"
        Main[main.py]
        Endpoints[REST Endpoints]
        CORS[CORS Middleware]
    end

    subgraph "Orchestration Layer"
        Orchestrator[Orchestrator]
        State_Store[State Store]
    end

    subgraph "Agent Layer"
        News_Agent[News Agent]
        Weather_Agent[Weather Agent]
        Port_Agent[Port Agent]
        Aggregation_Agent[Aggregation Agent]
        Explanation_Agent[Explanation Agent]
    end

    subgraph "Service Layer"
        LLM_Service[LLM Service]
        News_API[News API]
        Weather_API[Weather API]
    end

    subgraph "External Services"
        OpenAI[OpenAI API]
        News_Source[External News Sources]
        Weather_Source[Weather Data Sources]
    end

    UI --> API_Client
    API_Client --> Endpoints
    Endpoints --> CORS
    CORS --> Main
    Main --> Orchestrator
    Orchestrator --> State_Store
    Orchestrator --> News_Agent
    Orchestrator --> Weather_Agent
    Orchestrator --> Port_Agent
    Orchestrator --> Aggregation_Agent
    Orchestrator --> Explanation_Agent
    News_Agent --> News_API
    News_API --> News_Source
    Weather_Agent --> Weather_API
    Weather_API --> Weather_Source
    News_Agent --> LLM_Service
    Weather_Agent --> LLM_Service
    Port_Agent --> LLM_Service
    Explanation_Agent --> LLM_Service
    LLM_Service --> OpenAI
    Main --> State_Store

    style UI fill:#e1f5ff
    style Main fill:#fff4e1
    style Orchestrator fill:#f0e1ff
    style News_Agent fill:#ffe1f0
    style Weather_Agent fill:#e1ffe1
    style Port_Agent fill:#fff0e1
    style Aggregation_Agent fill:#e1f0ff
    style Explanation_Agent fill:#f0ffe1
    style LLM_Service fill:#ffe1e1
```

## Detailed Data Flow

```mermaid
sequenceDiagram
    participant User as 👤 User
    participant UI as 🖥️ Frontend (Next.js)
    participant API as 🚀 FastAPI Backend
    participant Orch as 🎯 Orchestrator
    participant State as 💾 State Store
    participant Agents as 🤖 Agents
    participant LLM as 🧠 LLM Service
    participant ExtAPI as 🌐 External APIs

    User->>UI: Select Region & Click Analyze
    UI->>API: POST /analyze/{region}
    API->>Orch: analyze(region)

    Orch->>State: Initialize SystemState
    Orch->>Agents: NewsAgent.run(region)
    Agents->>ExtAPI: Fetch news articles
    ExtAPI-->>Agents: News data
    Agents->>LLM: classify_news_risk(articles)
    LLM-->>Agents: Risk classification
    Agents-->>Orch: News risk result

    Orch->>Agents: WeatherAgent.run(region)
    Agents->>ExtAPI: Fetch weather data
    ExtAPI-->>Agents: Weather data
    Agents-->>Orch: Weather risk result

    Orch->>Agents: PortAgent.run(region)
    Agents->>LLM: Analyze port conditions
    LLM-->>Agents: Port risk result
    Agents-->>Orch: Port risk result

    Orch->>Agents: AggregationAgent.run()
    Agents-->>Orch: Aggregated risk score

    Orch->>Agents: ExplanationAgent.run()
    Agents->>LLM: generate_explanation()
    LLM-->>Agents: Plain-text explanation
    Agents-->>Orch: Explanation

    Orch->>State: Update with all results
    State-->>Orch: Confirmation
    Orch-->>API: Complete SystemState
    API-->>UI: SystemState response
    UI->>User: Display risk dashboard

    Note over User,UI: User can now ask questions
    User->>UI: Ask question in chat
    UI->>API: POST /chat
    API->>State: Get current state
    State-->>API: SystemState
    API->>LLM: answer_chat_question()
    LLM-->>API: AI response
    API-->>UI: Chat response
    UI->>User: Display answer
```

## Component Architecture

```mermaid
graph TB
    subgraph "Frontend Components"
        Dashboard[Dashboard Page]
        Header[Header Component]
        RegionSelector[Region Selector]
        AnalyzeButton[Analyze Button]
        RiskMeter[Risk Meter]
        RiskCards[Risk Cards]
        ChatBot[Chat Bot]
        EmptyState[Empty State]
        BackgroundEffects[Background Effects]
    end

    subgraph "API Endpoints"
        Health[GET /health]
        Regions[GET /regions]
        Analyze[POST /analyze/{region}]
        GetState[GET /state]
        StateSummary[GET /state/summary]
        Chat[POST /chat]
    end

    subgraph "Backend Modules"
        Config[config.py]
        State[state.py]
        Schemas[models/schemas.py]
    end

    Dashboard --> Header
    Dashboard --> RegionSelector
    Dashboard --> AnalyzeButton
    Dashboard --> RiskMeter
    Dashboard --> RiskCards
    Dashboard --> ChatBot
    Dashboard --> EmptyState
    Dashboard --> BackgroundEffects

    AnalyzeButton --> Analyze
    RegionSelector --> Regions
    RiskMeter --> GetState
    RiskCards --> GetState
    ChatBot --> Chat

    Analyze --> Config
    GetState --> State
    Chat --> State
    Analyze --> Schemas
    GetState --> Schemas
    Chat --> Schemas

    style Dashboard fill:#e3f2fd
    style Analyze fill:#fff3e0
    style Chat fill:#f3e5f5
```

## Agent Architecture

```mermaid
classDiagram
    class BaseAgent {
        <<abstract>>
        +str name
        +__init__(name: str)
        +run(region: str) dict
    }

    class NewsAgent {
        +run(region: str) dict
        -fetch_news(region: str) list
    }

    class WeatherAgent {
        +run(region: str) dict
        -fetch_weather(region: str) dict
    }

    class PortAgent {
        +run(region: str) dict
        -analyze_port_conditions(region: str) dict
    }

    class AggregationAgent {
        +run(region, news_severity, weather_severity, port_severity) dict
        -calculate_aggregated_risk() dict
    }

    class ExplanationAgent {
        +run(region, news_risk, weather_risk, port_risk, aggregated_risk) str
    }

    BaseAgent <|-- NewsAgent
    BaseAgent <|-- WeatherAgent
    BaseAgent <|-- PortAgent
    BaseAgent <|-- AggregationAgent
    BaseAgent <|-- ExplanationAgent

    class Orchestrator {
        -NewsAgent news_agent
        -WeatherAgent weather_agent
        -PortAgent port_agent
        -AggregationAgent aggregation_agent
        -ExplanationAgent explanation_agent
        +analyze(region: str) SystemState
        +get_available_regions() list
    }

    Orchestrator --> NewsAgent
    Orchestrator --> WeatherAgent
    Orchestrator --> PortAgent
    Orchestrator --> AggregationAgent
    Orchestrator --> ExplanationAgent
```

## Service Architecture

```mermaid
graph TB
    subgraph "LLM Service"
        LLM[LLMService]
        Classify[classify_news_risk]
        Generate[generate_explanation]
        Answer[answer_chat_question]
    end

    subgraph "External APIs"
        NewsAPI[News API Service]
        WeatherAPI[Weather API Service]
    end

    subgraph "OpenAI Integration"
        Client[AsyncOpenAI Client]
        Model[GPT-4o-mini]
    end

    Classify --> LLM
    Generate --> LLM
    Answer --> LLM
    LLM --> Client
    Client --> Model

    NewsAgent[News Agent] --> Classify
    WeatherAgent[Weather Agent] --> NewsAPI
    PortAgent[Port Agent] --> Generate
    ExplanationAgent[Explanation Agent] --> Generate
    ChatEndpoint[Chat Endpoint] --> Answer

    style LLM fill:#ffebee
    style Model fill:#e8f5e9
```

## State Management Flow

```mermaid
stateDiagram-v2
    [*] --> Idle: Application Start

    Idle --> Processing: User clicks Analyze
    Processing --> NewsAnalysis: Orchestrator starts
    NewsAnalysis --> WeatherAnalysis: NewsAgent completes
    WeatherAnalysis --> PortAnalysis: WeatherAgent completes
    PortAnalysis --> Aggregation: PortAgent completes
    Aggregation --> Explanation: AggregationAgent completes
    Explanation --> Completed: ExplanationAgent completes

    Completed --> Idle: Ready for new analysis
    Processing --> Error: Exception occurs
    Error --> Idle: Error handled

    state Processing {
        [*] --> NewsAnalysis
        NewsAnalysis --> WeatherAnalysis
        WeatherAnalysis --> PortAnalysis
        PortAnalysis --> Aggregation
        Aggregation --> Explanation
        Explanation --> [*]
    }

    Completed --> ChatReady: User opens chat
    ChatReady --> ChatActive: User asks question
    ChatActive --> ChatReady: Answer provided
    ChatReady --> Idle: Chat closed
```

## Technology Stack

```mermaid
graph LR
    subgraph "Frontend"
        Next[Next.js 14]
        React[React 18]
        TypeScript[TypeScript]
        Tailwind[Tailwind CSS]
        Framer[Framer Motion]
        Lucide[Lucide Icons]
    end

    subgraph "Backend"
        FastAPI[FastAPI]
        Python[Python 3.11+]
        Uvicorn[Uvicorn Server]
        Pydantic[Pydantic]
        OpenAI[OpenAI SDK]
    end

    subgraph "External Services"
        OpenAI_API[OpenAI API]
        News[News API]
        Weather[Weather API]
    end

    Next --> React
    React --> TypeScript
    TypeScript --> Tailwind
    Tailwind --> Framer
    Framer --> Lucide

    FastAPI --> Python
    Python --> Uvicorn
    Uvicorn --> Pydantic
    Pydantic --> OpenAI

    OpenAI --> OpenAI_API
    News --> News_API
    Weather --> Weather_API

    style Next fill:#0070f3
    style FastAPI fill:#009688
    style OpenAI_API fill:#412991
```

## Risk Assessment Pipeline

```mermaid
graph TB
    Start[User Initiates Analysis] --> Select[Select Region]
    Select --> Validate[Validate Region]
    Validate -->|Invalid| Error[Return Error]
    Validate -->|Valid| News[Fetch News Articles]
    News --> Classify[LLM Classifies Risk]
    Classify --> Weather[Fetch Weather Data]
    Weather --> WeatherRisk[Assess Weather Risk]
    WeatherRisk --> Port[Analyze Port Conditions]
    Port --> PortRisk[Assess Port Risk]
    PortRisk --> Aggregate[Combine Risk Scores]
    Aggregate --> Calculate[Calculate Overall Risk]
    Calculate --> Explain[Generate Explanation]
    Explain --> Store[Store in State]
    Store --> Return[Return to Frontend]
    Return --> Display[Display Dashboard]

    style Start fill:#e3f2fd
    style Display fill:#c8e6c9
    style Error fill:#ffcdd2
```

## API Request/Response Flow

```mermaid
graph TB
    subgraph "Frontend Request"
        Req[HTTP Request]
        Headers[Headers]
        Body[Request Body]
    end

    subgraph "Backend Processing"
        Auth[Authentication]
        Validation[Input Validation]
        BusinessLogic[Business Logic]
        Database[State Store]
    end

    subgraph "Frontend Response"
        Resp[HTTP Response]
        Data[Response Data]
        Error[Error Handling]
    end

    Req --> Headers
    Req --> Body
    Headers --> Auth
    Body --> Validation
    Auth --> BusinessLogic
    Validation --> BusinessLogic
    BusinessLogic --> Database
    Database --> BusinessLogic
    BusinessLogic --> Resp
    Resp --> Data
    Resp --> Error

    style Req fill:#e1f5fe
    style BusinessLogic fill:#fff3e0
    style Resp fill:#e8f5e9
```

## Key Architecture Patterns

1. **Orchestrator Pattern**: Central coordinator manages multiple specialized agents
2. **Agent Pattern**: Each risk type has a dedicated agent with single responsibility
3. **Service Layer**: External API integrations abstracted into service classes
4. **State Management**: Global state store for sharing analysis results
5. **RESTful API**: Clean separation between frontend and backend
6. **Component-Based UI**: Modular React components for maintainability
7. **Async/Await**: Non-blocking operations for better performance
8. **Dependency Injection**: Services injected into agents and orchestrator
