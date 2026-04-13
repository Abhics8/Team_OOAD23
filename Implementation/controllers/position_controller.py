"""
PositionController — Controls position over laps logic.
Corresponds to the PositionController <<control>> class in the Class Diagram.
"""

import plotly.graph_objects as go
from models.entities import Driver, Session
from services.fastf1_service import FastF1DataService
from services.chart_generator import ChartGenerator


class PositionController:
    """Controller for loading and visualizing position data over laps."""

    def __init__(self):
        self.dataService = FastF1DataService()
        self.chartGenerator = ChartGenerator()

    def loadPositionData(
        self, ff1_session, driver1: Driver, driver2: Driver
    ) -> go.Figure:
        """Load positions for both drivers and generate position chart."""
        d1_pos = self.dataService.getPositionsForDriver(
            ff1_session, driver1.getAbbreviation()
        )
        d2_pos = self.dataService.getPositionsForDriver(
            ff1_session, driver2.getAbbreviation()
        )

        # Get total laps from session
        try:
            totalLaps = int(ff1_session.laps["LapNumber"].max())
        except Exception:
            totalLaps = 0

        d1_color = driver1.team.getColor() if driver1.team else "#FF0000"
        d2_color = driver2.team.getColor() if driver2.team else "#0000FF"

        return self.chartGenerator.generatePositionChart(
            d1_name=driver1.getAbbreviation(),
            d1_color=d1_color,
            d1Pos=d1_pos,
            d2_name=driver2.getAbbreviation(),
            d2_color=d2_color,
            d2Pos=d2_pos,
            totalLaps=totalLaps,
        )
