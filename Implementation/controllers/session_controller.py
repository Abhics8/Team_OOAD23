"""
SessionController — Controls session selection logic.
Corresponds to the SessionController <<control>> class in the Class Diagram.
"""

from typing import List, Optional
from models.entities import Season, Race, Session
from services.fastf1_service import FastF1DataService


class SessionController:
    """Controller for managing season, race, and session selection."""

    def __init__(self):
        self.dataService = FastF1DataService()
        self._activeSession = None
        self._ff1Session = None

    def loadAvailableSeasons(self) -> List[int]:
        """Load available F1 seasons."""
        return self.dataService.fetchSeasons()

    def loadRaces(self, year: int) -> List[Race]:
        """Load races for a given season year."""
        return self.dataService.fetchRaces(year)

    def loadSessions(self, year: int, race_name: str) -> List[str]:
        """Load available session types for a race."""
        return self.dataService.fetchSessions(year, race_name)

    def setActiveSession(self, year: int, race_name: str, session_type: str):
        """Set the active session by loading it via FastF1."""
        self._ff1Session = self.dataService.loadSession(year, race_name, session_type)
        return self._ff1Session

    def getActiveSession(self):
        """Return the currently loaded FastF1 session object."""
        return self._ff1Session
