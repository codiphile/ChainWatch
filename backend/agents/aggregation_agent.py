from backend.agents.base import BaseAgent
from backend.models.schemas import AggregatedRisk


class AggregationAgent(BaseAgent):
    """Agent for aggregating risk scores from all sources."""

    # Weights for risk aggregation
    WEIGHTS = {
        "news": 0.4,
        "weather": 0.3,
        "port": 0.3,
    }

    # Risk level thresholds
    RISK_THRESHOLDS = {
        "Low": (0, 2.5),
        "Medium": (2.5, 3.5),
        "High": (3.5, 6),
    }

    def __init__(self):
        super().__init__(name="Risk Aggregation Agent")

    def _calculate_risk_level(self, score: float) -> str:
        """Map risk score to risk level category."""
        for level, (low, high) in self.RISK_THRESHOLDS.items():
            if low <= score < high:
                return level
        return "High"  # Default for edge cases

    async def run(
        self,
        region: str,
        news_severity: int = 1,
        weather_severity: int = 1,
        port_severity: int = 1,
    ) -> dict:
        """
        Aggregate risk scores from all agents.

        Args:
            region: Region being assessed
            news_severity: Severity from news agent (1-5)
            weather_severity: Severity from weather agent (1-5)
            port_severity: Severity from port agent (1-5)

        Returns:
            dict with AggregatedRisk fields
        """
        # Calculate weighted risk score
        risk_score = (
            self.WEIGHTS["news"] * news_severity
            + self.WEIGHTS["weather"] * weather_severity
            + self.WEIGHTS["port"] * port_severity
        )

        # Round to 1 decimal place
        risk_score = round(risk_score, 1)

        # Determine risk level
        risk_level = self._calculate_risk_level(risk_score)

        # Build breakdown for transparency
        breakdown = {
            "news": {
                "severity": news_severity,
                "weight": self.WEIGHTS["news"],
                "contribution": round(self.WEIGHTS["news"] * news_severity, 2),
            },
            "weather": {
                "severity": weather_severity,
                "weight": self.WEIGHTS["weather"],
                "contribution": round(self.WEIGHTS["weather"] * weather_severity, 2),
            },
            "port": {
                "severity": port_severity,
                "weight": self.WEIGHTS["port"],
                "contribution": round(self.WEIGHTS["port"] * port_severity, 2),
            },
        }

        return AggregatedRisk(
            risk_score=risk_score,
            risk_level=risk_level,
            breakdown=breakdown,
        ).model_dump()
