# F1 Insights & Strategy Explorer

**CSCI 6234 — Object-Oriented Design**  
*George Washington University | Spring 2026 | Group 23*

[![Python](https://img.shields.io/badge/Python-3.10+-3572A5.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![FastF1](https://img.shields.io/badge/FastF1-3.3+-E7471D.svg)](https://docs.fastf1.dev/)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive-3F4F75.svg?logo=plotly&logoColor=white)](https://plotly.com/)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-%E2%86%92%20Streamlit%20Cloud-FF4B4B.svg?logo=streamlit&logoColor=white)](https://teamooad23-hwm9sxennf9mk2poes7zga.streamlit.app)

> **[Launch Live Dashboard →](https://teamooad23-hwm9sxennf9mk2poes7zga.streamlit.app)**

An interactive, data-driven web application for analyzing Formula 1 race telemetry, tyre strategies, and session outcomes — built end-to-end using **Object-Oriented Analysis and Design (OOAD)** methodology following the **Rational Unified Process (RUP)**.

---

## Overview

The **F1 Insights & Strategy Explorer** gives fans, analysts, and engineers a clean interface to compare driver performance across any modern Formula 1 session. It pulls live timing data from the official F1 API (via `FastF1`) and renders dynamic, interactive visualizations using Plotly.

### What You Can Do

| Feature | Description |
|---|---|
| **Session Selection** | Load any Practice, Qualifying, or Race session from 2018 to present |
| **Head-to-Head Comparison** | Pick any two drivers on the grid and compare their full race data |
| **Lap Time Analysis** | Interactive pace chart with IQR-based outlier filtering and MM:SS.ms formatting |
| **Race Position Tracking** | Lap-by-lap position changes — spot overtakes and safety car impacts |
| **Tyre Strategy Breakdown** | Stint durations, compound selections, and pit stop timing visualized side-by-side |

---

## OOAD Phases

This repository documents the complete software lifecycle following the Rational Unified Process:

| Phase | Artifact | Location |
|---|---|---|
| **Requirements** | Use Case Diagrams, Use Case Specifications | `Requirements/` |
| **Analysis** | Domain Model, Robustness Diagrams | `Analysis/` |
| **Design** | Class Diagram, Sequence Diagrams | `Design/` |
| **Implementation** | Full Streamlit Application | `Implementation/` |

---

## Repository Structure

```text
Team_OOAD23/
├── UML/                         # Supporting UML diagrams
│   ├── ActivityDiagram.puml
│   ├── ComponentDiagram.puml
│   ├── StateDiagram.puml
│   └── CollaborationDiagram.puml
│
├── Requirements/                # Requirements phase
│   └── Use Case/                # Use Case Diagrams & Specifications
│
├── Analysis/                    # Analysis phase
│   ├── DomainModel/             # Core entity relationships
│   └── *.puml                   # 5x MVC Robustness Diagrams
│
├── Design/                      # Design phase
│   ├── ClassDiagram/            # Full architecture (Boundary, Controller, Entity, Service)
│   └── SequenceDiagram/         # Execution flows per use case
│
└── Implementation/              # Working application source code
    ├── app.py                   # Streamlit entry point
    ├── requirements.txt         # Python dependencies
    ├── models/                  # Domain entities (LapTime, TyreStint, Driver, etc.)
    ├── services/                # FastF1 data service & Plotly chart generator
    ├── controllers/             # Business logic controllers
    └── pages/                   # Streamlit boundary view pages
```

---

## Quick Start

```bash
# Clone the repository
git clone https://github.com/Abhics8/Team_OOAD23.git
cd Team_OOAD23/Implementation

# Install dependencies
pip install -r requirements.txt

# Launch the dashboard
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

### How to Use

1. **Select a Season** from the sidebar *(2018 → present)*
2. **Pick a Race** from the calendar
3. **Choose a Session** — FP1, FP2, FP3, Qualifying, or Race
4. Click **Load Session** to fetch lap data
5. **Select two drivers** to compare
6. Navigate to any of the three analysis pages using the sidebar

---

## Architecture

The implementation maps directly to the OOAD Class Diagram:

```
Boundary Classes  →  pages/             (Streamlit UI views)
Controller Classes →  controllers/      (Business logic & orchestration)
Service Classes    →  services/         (FastF1 data access, Plotly chart generation)
Entity Classes     →  models/entities.py (Domain dataclasses)
```

---

## Contributors

Designed and developed by **Group 23** for CSCI 6234 — Spring 2026:

- **Abhi Bhardwaj** — [@Abhics8](https://github.com/Abhics8)
- **Ankita Vilas Pimpalkar** — [@AnkitaVilasPimpalkar08](https://github.com/AnkitaVilasPimpalkar08)

---

*This is an academic project for CSCI 6234 at George Washington University. "Formula 1" and "F1" are registered trademarks of Formula One Licensing BV. Not affiliated with or endorsed by Formula 1.*
