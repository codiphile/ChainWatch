from backend.agents.base import BaseAgent
from backend.services.news_api import NewsAPIClient
from backend.services.llm_service import LLMService
from backend.models.schemas import NewsRiskOutput


class NewsAgent(BaseAgent):
    """Agent for assessing supply chain risks from news sources."""

    def __init__(self):
        super().__init__(name="News Risk Agent")
        self.news_client = NewsAPIClient()
        self.llm_service = LLMService()

    async def run(self, region: str) -> dict:
        """
        Fetch and analyze news for supply chain risks.

        Args:
            region: Region to analyze (e.g., "Shanghai")

        Returns:
            dict with NewsRiskOutput fields
        """
        # Fetch supply chain related news for the region
        news_result = await self.news_client.fetch_supply_chain_news(region)

        if news_result["status"] != "ok" or not news_result.get("articles"):
            # Fallback response when no news available
            return NewsRiskOutput(
                event_type="none",
                severity=1,
                summary=f"No recent supply chain news found for {region}.",
                sources=[],
            ).model_dump()

        articles = news_result["articles"]

        # Use LLM to classify and assess risk
        classification = await self.llm_service.classify_news_risk(articles)

        # Extract source names
        sources = [article.get("source", "Unknown") for article in articles[:5]]

        return NewsRiskOutput(
            event_type=classification["event_type"],
            severity=classification["severity"],
            summary=classification["summary"],
            sources=sources,
        ).model_dump()
