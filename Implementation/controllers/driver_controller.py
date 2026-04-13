"""
DriverController — Controls driver selection logic.
Corresponds to the DriverController <<control>> class in the Class Diagram.
"""

from typing import List, Tuple, Optional
from models.entities import Driver
from services.fastf1_service import FastF1DataService


class DriverController:
    """Controller for managing driver selection and validation."""

    def __init__(self):
        self.dataService = FastF1DataService()

    def getAvailableDrivers(self, ff1_session) -> List[Driver]:
        """Get list of available drivers from the active session."""
        return self.dataService.getDriversFromSession(ff1_session)

    def validateSelection(self, d1: Optional[Driver], d2: Optional[Driver]) -> Tuple[bool, str]:
        """Validate that two different drivers are selected."""
        if d1 is None or d2 is None:
            return False, "Please select two drivers."
        if d1.getAbbreviation() == d2.getAbbreviation():
            return False, "Please select two different drivers."
        return True, "Selection valid."
