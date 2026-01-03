from datetime import datetime
from typing import Optional
from backend.models.schemas import SystemState


class StateStore:
    """In-memory state store for system outputs."""

    def __init__(self):
        self._state: Optional[SystemState] = None
        self._last_updated: Optional[datetime] = None

    def update(self, state: SystemState) -> None:
        """Update the current system state."""
        self._state = state
        self._last_updated = datetime.utcnow()

    def get(self) -> Optional[SystemState]:
        """Get the current system state."""
        return self._state

    def get_last_updated(self) -> Optional[datetime]:
        """Get the timestamp of the last update."""
        return self._last_updated

    def clear(self) -> None:
        """Clear the current state."""
        self._state = None
        self._last_updated = None


# Global state instance
state_store = StateStore()
