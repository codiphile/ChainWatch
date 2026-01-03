import httpx
from typing import Optional
from backend.config import get_settings


class WeatherAPIClient:
    """Client for OpenWeatherMap API to fetch weather data."""

    BASE_URL = "https://api.openweathermap.org/data/2.5"

    def __init__(self):
        self.settings = get_settings()
        self.api_key = self.settings.openweather_api_key

    async def fetch_current_weather(self, lat: float, lon: float) -> dict:
        """
        Fetch current weather for given coordinates.

        Args:
            lat: Latitude
            lon: Longitude

        Returns:
            dict with weather data or error information
        """
        if not self.api_key:
            return {
                "status": "error",
                "message": "OPENWEATHER_API_KEY not configured",
                "data": None,
            }

        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": "metric",
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(f"{self.BASE_URL}/weather", params=params)
                response.raise_for_status()
                data = response.json()

                return {
                    "status": "ok",
                    "data": {
                        "temperature_c": data.get("main", {}).get("temp"),
                        "feels_like_c": data.get("main", {}).get("feels_like"),
                        "humidity_percent": data.get("main", {}).get("humidity"),
                        "wind_speed_ms": data.get("wind", {}).get("speed"),
                        "wind_speed_kmh": data.get("wind", {}).get("speed", 0) * 3.6,
                        "condition": data.get("weather", [{}])[0].get("main", "Unknown"),
                        "description": data.get("weather", [{}])[0].get("description", ""),
                        "visibility_m": data.get("visibility"),
                        "clouds_percent": data.get("clouds", {}).get("all"),
                        "rain_1h_mm": data.get("rain", {}).get("1h", 0),
                        "rain_3h_mm": data.get("rain", {}).get("3h", 0),
                    },
                }

        except httpx.HTTPStatusError as e:
            return {
                "status": "error",
                "message": f"HTTP error: {e.response.status_code}",
                "data": None,
            }
        except httpx.RequestError as e:
            return {
                "status": "error",
                "message": f"Request error: {str(e)}",
                "data": None,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Unexpected error: {str(e)}",
                "data": None,
            }

    async def fetch_forecast(self, lat: float, lon: float) -> dict:
        """
        Fetch 5-day weather forecast for given coordinates.

        Args:
            lat: Latitude
            lon: Longitude

        Returns:
            dict with forecast data or error information
        """
        if not self.api_key:
            return {
                "status": "error",
                "message": "OPENWEATHER_API_KEY not configured",
                "data": None,
            }

        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": "metric",
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(f"{self.BASE_URL}/forecast", params=params)
                response.raise_for_status()
                data = response.json()

                forecasts = []
                for item in data.get("list", [])[:8]:  # Next 24 hours (3-hour intervals)
                    forecasts.append(
                        {
                            "datetime": item.get("dt_txt"),
                            "temperature_c": item.get("main", {}).get("temp"),
                            "wind_speed_kmh": item.get("wind", {}).get("speed", 0) * 3.6,
                            "condition": item.get("weather", [{}])[0].get("main"),
                            "rain_3h_mm": item.get("rain", {}).get("3h", 0),
                        }
                    )

                return {
                    "status": "ok",
                    "data": forecasts,
                }

        except httpx.HTTPStatusError as e:
            return {
                "status": "error",
                "message": f"HTTP error: {e.response.status_code}",
                "data": None,
            }
        except httpx.RequestError as e:
            return {
                "status": "error",
                "message": f"Request error: {str(e)}",
                "data": None,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Unexpected error: {str(e)}",
                "data": None,
            }

    async def fetch_weather_for_region(self, region: str) -> dict:
        """
        Fetch weather data for a named region.

        Args:
            region: Region name (e.g., "Shanghai", "Rotterdam")

        Returns:
            dict with current weather and forecast
        """
        regions = self.settings.regions

        if region not in regions:
            return {
                "status": "error",
                "message": f"Unknown region: {region}",
                "current": None,
                "forecast": None,
            }

        coords = regions[region]
        lat, lon = coords["lat"], coords["lon"]

        current = await self.fetch_current_weather(lat, lon)
        forecast = await self.fetch_forecast(lat, lon)

        return {
            "status": "ok" if current["status"] == "ok" else "error",
            "current": current.get("data"),
            "forecast": forecast.get("data"),
        }
