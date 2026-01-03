from backend.agents.base import BaseAgent
from backend.services.weather_api import WeatherAPIClient
from backend.models.schemas import WeatherRiskOutput


class WeatherAgent(BaseAgent):
    """Agent for assessing weather-related supply chain risks."""

    # Deterministic thresholds for weather severity
    RAINFALL_THRESHOLDS = [(80, 5), (50, 4), (30, 3), (10, 2)]  # (mm, severity)
    WIND_THRESHOLDS = [(80, 5), (60, 4), (40, 3), (25, 2)]  # (km/h, severity)
    TEMP_EXTREME_LOW = 0  # Celsius
    TEMP_EXTREME_HIGH = 40  # Celsius

    def __init__(self):
        super().__init__(name="Weather Risk Agent")
        self.weather_client = WeatherAPIClient()

    def _calculate_severity(
        self,
        temperature: float | None,
        wind_speed: float | None,
        rainfall: float | None,
    ) -> tuple[int, str]:
        """
        Calculate severity score based on deterministic thresholds.

        Returns:
            tuple of (severity_score, condition_description)
        """
        severities = []
        conditions = []

        # Check rainfall
        if rainfall is not None:
            for threshold, severity in self.RAINFALL_THRESHOLDS:
                if rainfall >= threshold:
                    severities.append(severity)
                    conditions.append(f"heavy rainfall ({rainfall:.0f}mm)")
                    break

        # Check wind speed
        if wind_speed is not None:
            for threshold, severity in self.WIND_THRESHOLDS:
                if wind_speed >= threshold:
                    severities.append(severity)
                    conditions.append(f"high winds ({wind_speed:.0f}km/h)")
                    break

        # Check temperature extremes
        if temperature is not None:
            if temperature <= self.TEMP_EXTREME_LOW:
                severities.append(4)
                conditions.append(f"freezing conditions ({temperature:.1f}C)")
            elif temperature >= self.TEMP_EXTREME_HIGH:
                severities.append(4)
                conditions.append(f"extreme heat ({temperature:.1f}C)")

        if not severities:
            return 1, "normal conditions"

        # Return maximum severity and combined conditions
        return max(severities), ", ".join(conditions)

    async def run(self, region: str) -> dict:
        """
        Fetch and analyze weather data for supply chain risks.

        Args:
            region: Region to analyze

        Returns:
            dict with WeatherRiskOutput fields
        """
        weather_result = await self.weather_client.fetch_weather_for_region(region)

        if weather_result["status"] != "ok" or not weather_result.get("current"):
            return WeatherRiskOutput(
                weather_condition="unknown",
                severity=1,
                details=f"Unable to fetch weather data for {region}.",
                temperature_c=None,
                wind_speed_kmh=None,
                rainfall_mm=None,
            ).model_dump()

        current = weather_result["current"]

        temperature = current.get("temperature_c")
        wind_speed = current.get("wind_speed_kmh")
        rainfall = current.get("rain_1h_mm", 0) or current.get("rain_3h_mm", 0) or 0

        # Check forecast for upcoming severe weather
        forecast = weather_result.get("forecast", [])
        max_forecast_rainfall = 0
        max_forecast_wind = 0

        for fc in forecast or []:
            max_forecast_rainfall = max(max_forecast_rainfall, fc.get("rain_3h_mm", 0) or 0)
            max_forecast_wind = max(max_forecast_wind, fc.get("wind_speed_kmh", 0) or 0)

        # Use worst case between current and forecast
        effective_rainfall = max(rainfall, max_forecast_rainfall)
        effective_wind = max(wind_speed or 0, max_forecast_wind)

        severity, condition = self._calculate_severity(
            temperature, effective_wind, effective_rainfall
        )

        # Build details string
        details_parts = []
        if temperature is not None:
            details_parts.append(f"Temperature: {temperature:.1f}C")
        if wind_speed is not None:
            details_parts.append(f"Wind: {wind_speed:.1f}km/h")
        if effective_rainfall > 0:
            details_parts.append(f"Rainfall: {effective_rainfall:.1f}mm")

        weather_desc = current.get("description", current.get("condition", "unknown"))
        details = f"{weather_desc.capitalize()}. {', '.join(details_parts)}"

        return WeatherRiskOutput(
            weather_condition=condition if severity > 1 else weather_desc,
            severity=severity,
            details=details,
            temperature_c=temperature,
            wind_speed_kmh=wind_speed,
            rainfall_mm=effective_rainfall,
        ).model_dump()
