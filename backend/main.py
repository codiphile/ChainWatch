from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from backend.orchestrator import Orchestrator
from backend.state import state_store
from backend.config import get_settings
from backend.models.schemas import SystemState, ChatRequest, ChatResponse
from backend.services.llm_service import LLMService


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    print("ChainWatch API starting up...")
    yield
    # Shutdown
    print("ChainWatch API shutting down...")


app = FastAPI(
    title="ChainWatch API",
    description="AI-Based Supply Chain Risk Monitoring System",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
orchestrator = Orchestrator()
llm_service = LLMService()
settings = get_settings()


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "chainwatch-api"}


@app.get("/regions")
async def get_regions():
    """Get list of available regions for analysis."""
    return {
        "regions": orchestrator.get_available_regions(),
        "details": settings.regions,
    }


@app.post("/analyze/{region}", response_model=SystemState)
async def analyze_region(region: str):
    """
    Run full risk analysis for a region.

    Args:
        region: Region name (Shanghai, Rotterdam, Los Angeles)

    Returns:
        Complete system state with all risk assessments
    """
    if region not in settings.regions:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid region: {region}. Valid options: {list(settings.regions.keys())}",
        )

    result = await orchestrator.analyze(region)

    if result.status == "error":
        raise HTTPException(status_code=500, detail=result.error_message)

    return result


@app.get("/state", response_model=SystemState | None)
async def get_current_state():
    """Get the current system state from the last analysis."""
    state = state_store.get()
    if not state:
        return None
    return state


@app.get("/state/summary")
async def get_state_summary():
    """Get a summary of the current state."""
    state = state_store.get()
    if not state:
        return {"status": "no_data", "message": "No analysis has been run yet."}

    return {
        "status": "ok",
        "region": state.region,
        "risk_level": state.aggregated_risk.get("risk_level") if state.aggregated_risk else None,
        "risk_score": state.aggregated_risk.get("risk_score") if state.aggregated_risk else None,
        "last_updated": state_store.get_last_updated(),
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint for asking questions about the current risk assessment.

    Args:
        request: ChatRequest with user message

    Returns:
        AI-generated response based on current system state
    """
    state = state_store.get()

    if not state:
        return ChatResponse(
            response="No risk assessment data is available. Please run an analysis first by selecting a region.",
            based_on_data=False,
        )

    # Convert state to dict for LLM
    state_dict = state.model_dump() if state else None

    response = await llm_service.answer_chat_question(
        question=request.message,
        system_state=state_dict,
    )

    return ChatResponse(response=response, based_on_data=True)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
