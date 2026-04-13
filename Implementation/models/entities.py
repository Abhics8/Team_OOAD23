"""
Entity classes for the F1 Insights & Strategy Explorer.
These classes correspond to the entity classes defined in the Class Diagram
and Domain Model of the OOAD design.
"""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import date, timedelta


@dataclass
class TyreCompound:
    """Represents a tyre compound type used in F1 races."""
    name: str          # e.g., "SOFT", "MEDIUM", "HARD"
    color: str         # hex color for visualization
    hardness: str      # "soft", "medium", "hard", "intermediate", "wet"

    def getName(self) -> str:
        return self.name

    def getColor(self) -> str:
        return self.color

    def getHardness(self) -> str:
        return self.hardness


@dataclass
class TyreStint:
    """Represents a single tyre stint during a race."""
    stintNumber: int
    startLap: int
    endLap: int
    compound: Optional[TyreCompound] = None

    def getStintNumber(self) -> int:
        return self.stintNumber

    def getStartLap(self) -> int:
        return self.startLap

    def getEndLap(self) -> int:
        return self.endLap

    def getDuration(self) -> int:
        return self.endLap - self.startLap + 1


@dataclass
class LapTime:
    """Represents lap time data for a single lap."""
    lapNumber: int
    time: Optional[timedelta] = None
    sector1: Optional[timedelta] = None
    sector2: Optional[timedelta] = None
    sector3: Optional[timedelta] = None

    def getLapNumber(self) -> int:
        return self.lapNumber

    def getTime(self) -> Optional[timedelta]:
        return self.time

    def getSector1(self) -> Optional[timedelta]:
        return self.sector1

    def getSector2(self) -> Optional[timedelta]:
        return self.sector2

    def getSector3(self) -> Optional[timedelta]:
        return self.sector3


@dataclass
class Position:
    """Represents a driver's position at a specific lap."""
    lapNumber: int
    position: int

    def getLapNumber(self) -> int:
        return self.lapNumber

    def getPosition(self) -> int:
        return self.position


@dataclass
class Team:
    """Represents an F1 constructor/team."""
    name: str
    color: str  # team color for visualization

    def getName(self) -> str:
        return self.name

    def getColor(self) -> str:
        return self.color


@dataclass
class Driver:
    """Represents an F1 driver."""
    name: str
    abbreviation: str
    number: int
    team: Optional[Team] = None
    _lapTimes: List[LapTime] = field(default_factory=list)
    _positions: List[Position] = field(default_factory=list)
    _tyreStints: List[TyreStint] = field(default_factory=list)

    def getName(self) -> str:
        return self.name

    def getAbbreviation(self) -> str:
        return self.abbreviation

    def getNumber(self) -> int:
        return self.number

    def getLapTimes(self) -> List[LapTime]:
        return self._lapTimes

    def getPositions(self) -> List[Position]:
        return self._positions

    def getTyreStints(self) -> List[TyreStint]:
        return self._tyreStints


@dataclass
class Session:
    """Represents an F1 session (Practice, Qualifying, Race)."""
    type: str        # "FP1", "FP2", "FP3", "Q", "R"
    date: Optional[date] = None
    totalLaps: int = 0
    _drivers: List[Driver] = field(default_factory=list)

    def getType(self) -> str:
        return self.type

    def getDate(self) -> Optional[date]:
        return self.date

    def getTotalLaps(self) -> int:
        return self.totalLaps

    def getDrivers(self) -> List[Driver]:
        return self._drivers

    def getLaps(self) -> List[LapTime]:
        all_laps = []
        for driver in self._drivers:
            all_laps.extend(driver.getLapTimes())
        return all_laps


@dataclass
class Race:
    """Represents an F1 race weekend."""
    name: str
    location: str
    round: int
    date: Optional[date] = None
    _sessions: List[Session] = field(default_factory=list)

    def getName(self) -> str:
        return self.name

    def getLocation(self) -> str:
        return self.location

    def getRound(self) -> int:
        return self.round

    def getDate(self) -> Optional[date]:
        return self.date

    def getSessions(self) -> List[Session]:
        return self._sessions


@dataclass
class Season:
    """Represents an F1 season/year."""
    year: int
    name: str
    _races: List[Race] = field(default_factory=list)

    def getYear(self) -> int:
        return self.year

    def getName(self) -> str:
        return self.name

    def getRaces(self) -> List[Race]:
        return self._races


@dataclass
class Chart:
    """Represents a chart visualization configuration."""
    title: str
    xAxisLabel: str
    yAxisLabel: str
    series: list = field(default_factory=list)

    def getTitle(self) -> str:
        return self.title

    def getXAxisLabel(self) -> str:
        return self.xAxisLabel

    def getYAxisLabel(self) -> str:
        return self.yAxisLabel

    def render(self):
        """Render is handled by ChartGenerator with Plotly."""
        pass
