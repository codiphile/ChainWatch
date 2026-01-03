from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


class NewsRiskOutput(BaseModel):
    """Output schema for the News Risk Agent."""

    event_type: str = Field(
        description="Type of disruption event (strike, conflict, disaster, pandemic, policy, none)"
    )
    severity: int = Field(ge=1, le=5, description="Severity score from 1 (low) to 5 (critical)")
    summary: str = Field(description="Brief summary of the news findings")
    sources: list[str] = Field(default_factory=list, description="List of news source titles")


class WeatherRiskOutput(BaseModel):
    """Output schema for the Weather Risk Agent."""

    weather_condition: str = Field(description="Current weather condition description")
    severity: int = Field(ge=1, le=5, description="Severity score from 1 (low) to 5 (critical)")
    details: str = Field(description="Detailed weather information including metrics")
    temperature_c: Optional[float] = Field(default=None, description="Temperature in Celsius")
    wind_speed_kmh: Optional[float] = Field(default=None, description="Wind speed in km/h")
    rainfall_mm: Optional[float] = Field(default=None, description="Rainfall in mm")


class PortRiskOutput(BaseModel):
    """Output schema for the Port Risk Agent."""

    congestion_level: Literal["low", "moderate", "high", "critical"] = Field(
        description="Port congestion level"
    )
    severity: int = Field(ge=1, le=5, description="Severity score from 1 (low) to 5 (critical)")
    details: str = Field(description="Details about port congestion and delays")
    vessel_queue: Optional[int] = Field(default=None, description="Number of vessels waiting")
    avg_delay_hours: Optional[float] = Field(default=None, description="Average delay in hours")


class AggregatedRisk(BaseModel):
    """Output schema for the Risk Aggregation Agent."""

    risk_score: float = Field(ge=1.0, le=5.0, description="Weighted risk score")
    risk_level: Literal["Low", "Medium", "High"] = Field(description="Risk level category")
    breakdown: dict = Field(
        default_factory=dict,
        description="Breakdown of individual risk components with weights",
    )


class SystemState(BaseModel):
    """Complete system state containing all agent outputs."""

    region: str = Field(description="Region being analyzed")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    news_risk: Optional[NewsRiskOutput] = None
    weather_risk: Optional[WeatherRiskOutput] = None
    port_risk: Optional[PortRiskOutput] = None
    aggregated_risk: Optional[AggregatedRisk] = None
    explanation: Optional[str] = None
    status: Literal["pending", "processing", "completed", "error"] = "pending"
    error_message: Optional[str] = None


class ChatRequest(BaseModel):
    """Request schema for chatbot endpoint."""

    message: str = Field(description="User's chat message")
    region: Optional[str] = Field(default=None, description="Optional region context")


class ChatResponse(BaseModel):
    """Response schema for chatbot endpoint."""

    response: str = Field(description="AI-generated response")
    based_on_data: bool = Field(
        default=True, description="Whether response is based on available system data"
    )
