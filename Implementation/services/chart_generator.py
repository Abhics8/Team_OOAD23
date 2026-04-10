"""
ChartGenerator — Generates Plotly chart objects from entity data.
Corresponds to the ChartGenerator <<control>> class in the Class Diagram.
"""

import plotly.graph_objects as go
from typing import List
from models.entities import LapTime, Position, TyreStint, Chart


class ChartGenerator:
    """Generates interactive Plotly charts for F1 data visualization."""

    def generateLapTimeChart(
        self,
        d1_name: str,
        d1_color: str,
        d1Times: List[LapTime],
        d2_name: str,
        d2_color: str,
        d2Times: List[LapTime],
    ) -> go.Figure:
        """Generate a lap time comparison chart for two drivers."""
        fig = go.Figure()

        # Filter out laps with no time data and pit laps (outliers)
        d1_valid = [lt for lt in d1Times if lt.getTime() is not None]
        d2_valid = [lt for lt in d2Times if lt.getTime() is not None]

        if d1_valid:
            d1_seconds = [lt.getTime().total_seconds() for lt in d1_valid]
            median_d1 = sorted(d1_seconds)[len(d1_seconds) // 2]
            threshold = median_d1 * 1.1  # Filter outliers above 110% of median

            d1_filtered = [(lt, s) for lt, s in zip(d1_valid, d1_seconds) if s <= threshold]
            if d1_filtered:
                fig.add_trace(go.Scatter(
                    x=[lt.getLapNumber() for lt, _ in d1_filtered],
                    y=[s for _, s in d1_filtered],
                    mode="lines+markers",
                    name=d1_name,
                    line=dict(color=d1_color, width=2),
                    marker=dict(size=4),
                    hovertemplate="Lap %{x}<br>Time: %{y:.3f}s<extra>" + d1_name + "</extra>",
                ))

        if d2_valid:
            d2_seconds = [lt.getTime().total_seconds() for lt in d2_valid]
            median_d2 = sorted(d2_seconds)[len(d2_seconds) // 2]
            threshold = median_d2 * 1.1

            d2_filtered = [(lt, s) for lt, s in zip(d2_valid, d2_seconds) if s <= threshold]
            if d2_filtered:
                fig.add_trace(go.Scatter(
                    x=[lt.getLapNumber() for lt, _ in d2_filtered],
                    y=[s for _, s in d2_filtered],
                    mode="lines+markers",
                    name=d2_name,
                    line=dict(color=d2_color, width=2),
                    marker=dict(size=4),
                    hovertemplate="Lap %{x}<br>Time: %{y:.3f}s<extra>" + d2_name + "</extra>",
                ))

        fig.update_layout(
            title=dict(text="Lap Time Comparison", font=dict(size=22, color="white")),
            xaxis_title="Lap Number",
            yaxis_title="Lap Time (seconds)",
            template="plotly_dark",
            paper_bgcolor="#0E1117",
            plot_bgcolor="#1A1A2E",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(size=14),
            ),
            hovermode="x unified",
            height=500,
        )

        return fig

    def generatePositionChart(
        self,
        d1_name: str,
        d1_color: str,
        d1Pos: List[Position],
        d2_name: str,
        d2_color: str,
        d2Pos: List[Position],
        totalLaps: int,
    ) -> go.Figure:
        """Generate a position over laps chart for two drivers."""
        fig = go.Figure()

        if d1Pos:
            fig.add_trace(go.Scatter(
                x=[p.getLapNumber() for p in d1Pos],
                y=[p.getPosition() for p in d1Pos],
                mode="lines+markers",
                name=d1_name,
                line=dict(color=d1_color, width=3),
                marker=dict(size=5),
                hovertemplate="Lap %{x}<br>Position: P%{y}<extra>" + d1_name + "</extra>",
            ))

        if d2Pos:
            fig.add_trace(go.Scatter(
                x=[p.getLapNumber() for p in d2Pos],
                y=[p.getPosition() for p in d2Pos],
                mode="lines+markers",
                name=d2_name,
                line=dict(color=d2_color, width=3),
                marker=dict(size=5),
                hovertemplate="Lap %{x}<br>Position: P%{y}<extra>" + d2_name + "</extra>",
            ))

        fig.update_layout(
            title=dict(text="Position Over Laps", font=dict(size=22, color="white")),
            xaxis_title="Lap Number",
            yaxis_title="Position",
            yaxis=dict(autorange="reversed", dtick=1),  # P1 at top
            template="plotly_dark",
            paper_bgcolor="#0E1117",
            plot_bgcolor="#1A1A2E",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(size=14),
            ),
            hovermode="x unified",
            height=500,
        )

        return fig

    def generateTyreChart(
        self,
        d1_name: str,
        d1Stints: List[TyreStint],
        d2_name: str,
        d2Stints: List[TyreStint],
    ) -> go.Figure:
        """Generate a tyre strategy chart showing stint durations by compound."""
        fig = go.Figure()

        drivers_data = [
            (d1_name, d1Stints, 1),
            (d2_name, d2Stints, 0),
        ]

        for driver_name, stints, y_pos in drivers_data:
            for stint in stints:
                compound = stint.compound
                color = compound.getColor() if compound else "#888888"
                compound_name = compound.getName() if compound else "UNKNOWN"

                fig.add_trace(go.Bar(
                    x=[stint.getDuration()],
                    y=[driver_name],
                    base=[stint.getStartLap()],
                    orientation="h",
                    name=compound_name,
                    marker=dict(
                        color=color,
                        line=dict(color="white", width=1),
                        opacity=0.85,
                    ),
                    text=f"{compound_name}<br>Laps {stint.getStartLap()}-{stint.getEndLap()}",
                    textposition="inside",
                    textfont=dict(color="black" if compound_name in ["MEDIUM", "HARD"] else "white", size=11),
                    hovertemplate=(
                        f"<b>{driver_name}</b><br>"
                        f"Compound: {compound_name}<br>"
                        f"Laps: {stint.getStartLap()} - {stint.getEndLap()}<br>"
                        f"Duration: {stint.getDuration()} laps"
                        "<extra></extra>"
                    ),
                    showlegend=False,
                ))

        fig.update_layout(
            title=dict(text="Tyre Strategy Comparison", font=dict(size=22, color="white")),
            xaxis_title="Lap Number",
            yaxis_title="Driver",
            barmode="stack",
            template="plotly_dark",
            paper_bgcolor="#0E1117",
            plot_bgcolor="#1A1A2E",
            height=300,
            yaxis=dict(categoryorder="array", categoryarray=[d2_name, d1_name]),
        )

        return fig
