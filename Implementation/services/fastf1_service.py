"""
FastF1DataService — External API data fetching service.
Corresponds to the FastF1DataService <<service>> class in the Class Diagram.
Wraps the FastF1 library to fetch F1 session data.
"""

import fastf1
import streamlit as st
from typing import List, Optional
from models.entities import (
    Season, Race, Session, Driver, Team,
    LapTime, Position, TyreStint, TyreCompound
)
from datetime import timedelta

# Enable FastF1 cache
fastf1.Cache.enable_cache("f1_cache")

# Tyre compound color mapping
COMPOUND_COLORS = {
    "SOFT": "#FF3333",
    "MEDIUM": "#FFC300",
    "HARD": "#FFFFFF",
    "INTERMEDIATE": "#39B54A",
    "WET": "#0072C6",
    "UNKNOWN": "#888888",
}

COMPOUND_HARDNESS = {
    "SOFT": "soft",
    "MEDIUM": "medium",
    "HARD": "hard",
    "INTERMEDIATE": "intermediate",
    "WET": "wet",
    "UNKNOWN": "unknown",
}


class FastF1DataService:
    """Service class to fetch F1 data using the FastF1 library."""

    def fetchSeasons(self) -> List[int]:
        """Fetch available seasons. Returns list of years."""
        # FastF1 supports data from 2018 onwards reliably
        return list(range(2024, 2017, -1))

    @st.cache_data(ttl=3600, show_spinner=False)
    def fetchRaces(_self, year: int) -> List[Race]:
        """Fetch all races for a given season year."""
        try:
            schedule = fastf1.get_event_schedule(year)
            races = []
            for _, event in schedule.iterrows():
                if event["EventFormat"] == "testing":
                    continue
                race = Race(
                    name=str(event["EventName"]),
                    location=str(event["Location"]),
                    round=int(event["RoundNumber"]),
                    date=event["EventDate"].date() if hasattr(event["EventDate"], "date") else None,
                )
                races.append(race)
            return races
        except Exception as e:
            st.error(f"Error fetching races: {e}")
            return []

    def fetchSessions(self, year: int, race_name: str) -> List[str]:
        """Fetch available session types for a race."""
        return ["FP1", "FP2", "FP3", "Qualifying", "Race"]

    @st.cache_data(ttl=3600, show_spinner="Loading session data...")
    def loadSession(_self, year: int, race_name: str, session_type: str):
        """Load a FastF1 session object with lap and telemetry data."""
        try:
            session = fastf1.get_session(year, race_name, session_type)
            session.load(laps=True, telemetry=False, weather=False, messages=False)
            return session
        except Exception as e:
            st.error(f"Error loading session: {e}")
            return None

    def getDriversFromSession(self, ff1_session) -> List[Driver]:
        """Extract Driver entities from a loaded FastF1 session."""
        drivers = []
        if ff1_session is None:
            return drivers

        try:
            results = ff1_session.results
            if results is None or results.empty:
                # Fallback: get drivers from laps data
                laps = ff1_session.laps
                if laps is not None and not laps.empty:
                    for abbr in laps["Driver"].unique():
                        driver_laps = laps[laps["Driver"] == abbr]
                        team_name = str(driver_laps.iloc[0].get("Team", "Unknown"))
                        team_color = str(driver_laps.iloc[0].get("TeamColor", "888888"))
                        driver = Driver(
                            name=abbr,
                            abbreviation=str(abbr),
                            number=0,
                            team=Team(name=team_name, color=f"#{team_color}"),
                        )
                        drivers.append(driver)
                return drivers

            for _, row in results.iterrows():
                team_color = str(row.get("TeamColor", "888888"))
                if not team_color.startswith("#"):
                    team_color = f"#{team_color}"
                driver = Driver(
                    name=str(row.get("FullName", row.get("Abbreviation", "Unknown"))),
                    abbreviation=str(row.get("Abbreviation", "UNK")),
                    number=int(row.get("DriverNumber", 0)),
                    team=Team(
                        name=str(row.get("TeamName", "Unknown")),
                        color=team_color,
                    ),
                )
                drivers.append(driver)
        except Exception as e:
            st.warning(f"Could not extract full driver info: {e}")

        return drivers

    def getLapTimesForDriver(self, ff1_session, driver_abbr: str) -> List[LapTime]:
        """Fetch LapTime entities for a specific driver."""
        lap_times = []
        if ff1_session is None:
            return lap_times

        try:
            laps = ff1_session.laps.pick_driver(driver_abbr)
            for lap in laps.to_dict('records'):
                lt = lap.get("LapTime")
                s1 = lap.get("Sector1Time")
                s2 = lap.get("Sector2Time")
                s3 = lap.get("Sector3Time")

                lap_time = LapTime(
                    lapNumber=int(lap.get("LapNumber", 0)) if lap.get("LapNumber") is not None else 0,
                    time=lt if isinstance(lt, timedelta) else None,
                    sector1=s1 if isinstance(s1, timedelta) else None,
                    sector2=s2 if isinstance(s2, timedelta) else None,
                    sector3=s3 if isinstance(s3, timedelta) else None,
                )
                lap_times.append(lap_time)
        except Exception as e:
            st.warning(f"Error getting lap times for {driver_abbr}: {e}")

        return lap_times

    def getPositionsForDriver(self, ff1_session, driver_abbr: str) -> List[Position]:
        """Fetch Position entities for a specific driver."""
        positions = []
        if ff1_session is None:
            return positions

        try:
            laps = ff1_session.laps.pick_driver(driver_abbr)
            for lap in laps.to_dict('records'):
                pos = Position(
                    lapNumber=int(lap.get("LapNumber", 0)) if lap.get("LapNumber") is not None else 0,
                    position=int(lap.get("Position", 0)) if lap.get("Position") is not None else 0,
                )
                positions.append(pos)
        except Exception as e:
            st.warning(f"Error getting positions for {driver_abbr}: {e}")

        return positions

    def fetchStintData(self, ff1_session, driver_abbr: str) -> List[TyreStint]:
        """Fetch TyreStint entities for a specific driver."""
        stints = []
        if ff1_session is None:
            return stints

        try:
            laps = ff1_session.laps.pick_driver(driver_abbr)
            stint_groups = laps.groupby("Stint")

            for stint_num, stint_laps in stint_groups:
                compound_name = str(stint_laps.iloc[0].get("Compound", "UNKNOWN")).upper()
                compound = TyreCompound(
                    name=compound_name,
                    color=COMPOUND_COLORS.get(compound_name, "#888888"),
                    hardness=COMPOUND_HARDNESS.get(compound_name, "unknown"),
                )
                stint = TyreStint(
                    stintNumber=int(stint_num),
                    startLap=int(stint_laps["LapNumber"].min()),
                    endLap=int(stint_laps["LapNumber"].max()),
                    compound=compound,
                )
                stints.append(stint)
        except Exception as e:
            st.warning(f"Error getting stints for {driver_abbr}: {e}")

        return stints
