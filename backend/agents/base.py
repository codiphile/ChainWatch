from abc import ABC, abstractmethod
from typing import Any


class BaseAgent(ABC):
    """Abstract base class for all risk assessment agents."""

    def __init__(self, name: str):
        """
        Initialize the agent.

        Args:
            name: Human-readable name for the agent
        """
        self.name = name

    @abstractmethod
    async def run(self, region: str) -> dict[str, Any]:
        """
        Execute the agent's risk assessment for a given region.

        Args:
            region: The region to assess (e.g., "Shanghai", "Rotterdam")

        Returns:
            dict containing the agent's risk assessment output
        """
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}')"
