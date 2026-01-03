import random
from backend.agents.base import BaseAgent
from backend.models.schemas import PortRiskOutput
from backend.config import get_settings


class PortAgent(BaseAgent):
    """Agent for assessing port congestion risks using mock/static data."""

    # Static port congestion data for demo
    # In production, this would come from AIS data, port APIs, etc.
    MOCK_PORT_DATA = {
        "Shanghai": {
            "base_congestion": "moderate",
            "base_severity": 3,
            "vessel_queue_range": (15, 35),
            "avg_delay_range": (24, 72),
            "description": "Shanghai Port experiencing typical congestion levels",
        },
        "Rotterdam": {
            "base_congestion": "low",
            "base_severity": 2,
            "vessel_queue_range": (5, 15),
            "avg_delay_range": (6, 24),
            "description": "Port of Rotterdam operating efficiently",
        },
        "Los Angeles": {
            "base_congestion": "high",
            "base_severity": 4,
            "vessel_queue_range": (25, 50),
            "avg_delay_range": (48, 120),
            "description": "Port of Los Angeles experiencing elevated congestion",
        },
    }

    def __init__(self):
        super().__init__(name="Port Risk Agent")
        self.settings = get_settings()

    def _get_congestion_level(self, severity: int) -> str:
        """Map severity to congestion level."""
        if severity <= 1:
            return "low"
        elif severity <= 2:
            return "low"
        elif severity <= 3:
            return "moderate"
        elif severity <= 4:
            return "high"
        else:
            return "critical"

    async def run(self, region: str) -> dict:
        """
        Assess port congestion risk for a region.

        Args:
            region: Region to analyze

        Returns:
            dict with PortRiskOutput fields
        """
        port_data = self.MOCK_PORT_DATA.get(region)

        if not port_data:
            # Unknown region - return neutral assessment
            return PortRiskOutput(
                congestion_level="low",
                severity=1,
                details=f"No port data available for {region}.",
                vessel_queue=None,
                avg_delay_hours=None,
            ).model_dump()

        # Simulate some variability for demo purposes
        # In production, this would be real-time data
        severity = port_data["base_severity"]

        # Add small random variation for demo realism (+/- 1)
        severity_variation = random.choice([-1, 0, 0, 0, 1])
        severity = max(1, min(5, severity + severity_variation))

        vessel_queue = random.randint(*port_data["vessel_queue_range"])
        avg_delay = random.uniform(*port_data["avg_delay_range"])

        # Adjust severity based on simulated conditions
        if vessel_queue > 40:
            severity = max(severity, 4)
        if avg_delay > 96:
            severity = max(severity, 4)

        congestion_level = self._get_congestion_level(severity)

        # Build detailed description
        details = (
            f"{port_data['description']}. "
            f"Vessel queue: {vessel_queue} ships. "
            f"Average delay: {avg_delay:.0f} hours."
        )

        if severity >= 4:
            details += " Significant delays expected for incoming cargo."
        elif severity >= 3:
            details += " Some delays possible for cargo operations."

        return PortRiskOutput(
            congestion_level=congestion_level,
            severity=severity,
            details=details,
            vessel_queue=vessel_queue,
            avg_delay_hours=round(avg_delay, 1),
        ).model_dump()
