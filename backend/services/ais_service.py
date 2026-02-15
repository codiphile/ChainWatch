"""AIS Stream service for real-time vessel tracking data."""

import asyncio
import json
import websockets
from typing import Optional
from backend.config import get_settings


class AISStreamService:
    """Service for fetching real-time vessel data from AIS Stream API."""

    def __init__(self):
        self.settings = get_settings()
        self.ws_url = "wss://stream.aisstream.io/v0/stream"

    async def sample_port_vessels(
        self, 
        bounding_box: list[list[float]], 
        duration_seconds: int = 10
    ) -> dict:
        """
        Sample vessel data from a port area for a specified duration.

        Args:
            bounding_box: [[lat1, lon1], [lat2, lon2]] defining the area
            duration_seconds: How long to sample data (default 10 seconds)

        Returns:
            dict with vessel_count, avg_speed, navigational_statuses, etc.
        """
        if not self.settings.aisstream_api_key:
            raise ValueError("AIS Stream API key not configured")

        vessels = {}
        navigational_statuses = []
        speeds = []

        try:
            async with websockets.connect(self.ws_url) as websocket:
                # Subscribe to the port area
                subscribe_message = {
                    "APIKey": self.settings.aisstream_api_key,
                    "BoundingBoxes": [bounding_box],
                    "FilterMessageTypes": ["PositionReport"]
                }
                
                await websocket.send(json.dumps(subscribe_message))
                
                print(f"[AIS] Sampling {duration_seconds}s for bbox {bounding_box}")
                message_count = 0

                # Sample messages for the specified duration
                try:
                    async with asyncio.timeout(duration_seconds):
                        async for message_json in websocket:
                            message_count += 1
                            message = json.loads(message_json)
                            
                            # Debug: Log first few messages
                            if message_count <= 3:
                                print(f"[AIS] Message {message_count}: {message.get('MessageType', 'Unknown')}")
                            
                            # Handle different message types
                            if message.get("MessageType") == "PositionReport":
                                ais_msg = message.get("Message", {}).get("PositionReport", {})
                                
                                vessel_id = ais_msg.get("UserID")
                                if vessel_id:
                                    vessels[vessel_id] = {
                                        "mmsi": vessel_id,
                                        "latitude": ais_msg.get("Latitude"),
                                        "longitude": ais_msg.get("Longitude"),
                                        "sog": ais_msg.get("Sog", 0),  # Speed over ground
                                        "cog": ais_msg.get("Cog", 0),  # Course over ground
                                        "nav_status": ais_msg.get("NavigationalStatus", 0),
                                    }
                                    
                                    # Collect stats
                                    speed = ais_msg.get("Sog", 0)
                                    if speed is not None:
                                        speeds.append(speed)
                                    
                                    nav_status = ais_msg.get("NavigationalStatus")
                                    if nav_status is not None:
                                        navigational_statuses.append(nav_status)

                except asyncio.TimeoutError:
                    # Expected - we've sampled for the desired duration
                    print(f"[AIS] Timeout after {duration_seconds}s. Received {message_count} messages, found {len(vessels)} vessels")
                    pass

        except Exception as e:
            # Log error and return empty result
            print(f"AIS Stream error: {str(e)}")
            return {
                "vessel_count": 0,
                "avg_speed": 0,
                "stationary_count": 0,
                "moving_count": 0,
                "error": str(e)
            }

        # Calculate metrics
        vessel_count = len(vessels)
        avg_speed = sum(speeds) / len(speeds) if speeds else 0
        
        # Count stationary vs moving vessels
        # NavigationalStatus: 0=underway, 1=at anchor, 5=moored, etc.
        stationary_count = sum(1 for s in navigational_statuses if s in [1, 5])
        moving_count = sum(1 for s in navigational_statuses if s == 0)

        return {
            "vessel_count": vessel_count,
            "avg_speed": round(avg_speed, 2),
            "stationary_count": stationary_count,
            "moving_count": moving_count,
            "vessels": list(vessels.values())
        }

    async def get_port_congestion(self, region: str) -> Optional[dict]:
        """
        Get port congestion data for a specific region.

        Args:
            region: Region name (Shanghai, Rotterdam, Los Angeles)

        Returns:
            Vessel metrics for the port area, or None if error
        """
        region_config = self.settings.regions.get(region)
        if not region_config or "bbox" not in region_config:
            return None

        bounding_box = region_config["bbox"]
        
        try:
            metrics = await self.sample_port_vessels(bounding_box, duration_seconds=30)
            return metrics
        except Exception as e:
            print(f"Error fetching port congestion for {region}: {str(e)}")
            return None
