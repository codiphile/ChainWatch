import httpx
from typing import Optional
from backend.config import get_settings


class NewsAPIClient:
    """Client for NewsAPI.org to fetch news headlines."""

    BASE_URL = "https://newsapi.org/v2"

    def __init__(self):
        self.settings = get_settings()
        self.api_key = self.settings.news_api_key

    async def fetch_headlines(
        self,
        query: str,
        language: str = "en",
        page_size: int = 10,
    ) -> dict:
        """
        Fetch news headlines related to a query.

        Args:
            query: Search query (e.g., "Shanghai port disruption")
            language: Language code (default: en)
            page_size: Number of articles to fetch (default: 10)

        Returns:
            dict with articles or error information
        """
        if not self.api_key:
            return {
                "status": "error",
                "message": "NEWS_API_KEY not configured",
                "articles": [],
            }

        params = {
            "q": query,
            "language": language,
            "pageSize": page_size,
            "sortBy": "publishedAt",
            "apiKey": self.api_key,
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(f"{self.BASE_URL}/everything", params=params)
                response.raise_for_status()
                data = response.json()

                return {
                    "status": "ok",
                    "total_results": data.get("totalResults", 0),
                    "articles": [
                        {
                            "title": article.get("title", ""),
                            "description": article.get("description", ""),
                            "source": article.get("source", {}).get("name", "Unknown"),
                            "published_at": article.get("publishedAt", ""),
                            "url": article.get("url", ""),
                        }
                        for article in data.get("articles", [])
                    ],
                }

        except httpx.HTTPStatusError as e:
            return {
                "status": "error",
                "message": f"HTTP error: {e.response.status_code}",
                "articles": [],
            }
        except httpx.RequestError as e:
            return {
                "status": "error",
                "message": f"Request error: {str(e)}",
                "articles": [],
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Unexpected error: {str(e)}",
                "articles": [],
            }

    async def fetch_supply_chain_news(self, region: str) -> dict:
        """
        Fetch supply chain related news for a specific region.

        Args:
            region: Region name (e.g., "Shanghai", "Rotterdam")

        Returns:
            dict with relevant news articles
        """
        supply_chain_keywords = [
            "port disruption",
            "shipping delay",
            "supply chain",
            "logistics",
            "dock strike",
            "cargo",
            "container",
            "freight",
        ]

        query = f"{region} ({' OR '.join(supply_chain_keywords)})"
        return await self.fetch_headlines(query)
