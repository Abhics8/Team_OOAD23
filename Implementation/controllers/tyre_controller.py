"""
TyreStrategyController — Controls tyre stint logic.
Corresponds to the TyreStrategyController <<control>> class in the Class Diagram.
"""

import plotly.graph_objects as go
from models.entities import Driver
from services.fastf1_service import FastF1DataService
from services.chart_generator import ChartGenerator


class TyreStrategyController:
    """Controller for loading and visualizing tyre strategy data."""

    def __init__(self):
        self.dataService = FastF1DataService()
        self.chartGenerator = ChartGenerator()

    def loadTyreStints(
        self, ff1_session, driver1: Driver, driver2: Driver
    ) -> go.Figure:
        """Load tyre stint data for both drivers and generate strategy chart."""
        d1_stints = self.dataService.fetchStintData(
            ff1_session, driver1.getAbbreviation()
        )
        d2_stints = self.dataService.fetchStintData(
            ff1_session, driver2.getAbbreviation()
        )

        return self.chartGenerator.generateTyreChart(
            d1_name=driver1.getAbbreviation(),
            d1Stints=d1_stints,
            d2_name=driver2.getAbbreviation(),
            d2Stints=d2_stints,
        )
