"""
LapTimeController — Controls lap time comparison logic.
Corresponds to the LapTimeController <<control>> class in the Class Diagram.
"""

import plotly.graph_objects as go
from models.entities import Driver
from services.fastf1_service import FastF1DataService
from services.chart_generator import ChartGenerator


class LapTimeController:
    """Controller for loading and comparing lap time data."""

    def __init__(self):
        self.dataService = FastF1DataService()
        self.chartGenerator = ChartGenerator()

    def loadLapTimeComparison(
        self, ff1_session, driver1: Driver, driver2: Driver
    ) -> go.Figure:
        """Load lap times for both drivers and generate comparison chart."""
        d1_times = self.dataService.getLapTimesForDriver(
            ff1_session, driver1.getAbbreviation()
        )
        d2_times = self.dataService.getLapTimesForDriver(
            ff1_session, driver2.getAbbreviation()
        )

        d1_color = driver1.team.getColor() if driver1.team else "#FF0000"
        d2_color = driver2.team.getColor() if driver2.team else "#0000FF"

        return self.chartGenerator.generateLapTimeChart(
            d1_name=driver1.getAbbreviation(),
            d1_color=d1_color,
            d1Times=d1_times,
            d2_name=driver2.getAbbreviation(),
            d2_color=d2_color,
            d2Times=d2_times,
        )
