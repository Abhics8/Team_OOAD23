# 🏎️ F1 Insights & Strategy Explorer

**CSCI 6234 - Object-Oriented Design**  
*George Washington University | Spring 2026*

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B.svg)](https://streamlit.io/)
[![FastF1](https://img.shields.io/badge/FastF1-3.3+-orange.svg)](https://docs.fastf1.dev/)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive-brightgreen.svg)](https://plotly.com/)

An interactive, data-driven dashboard for analyzing Formula 1 race telemetry, strategies, and session outcomes. This project applies complete **Object-Oriented Analysis and Design (OOAD)** principles from conceptual requirements to a functional Python web application.

---

## Project Overview

The **F1 Insights & Strategy Explorer** provides fans, analysts, and engineers with an intuitive web application to compare drivers, track lap times, and dissect tyre strategies across any modern Formula 1 session. 

By leveraging the official F1 timing API (via `FastF1`), this project translates complex telemetry into readable, dynamic visualizations.

### Key Features
- **Global Session Integration:** Dynamically load any Practice, Qualifying, or Race session from 2018 to the present.
- **Head-to-Head Comparison:** Select any two drivers on the grid to analyze their comparative performance.
- **Pace Analysis:** Interactive lap-by-lap pace overlay charts.
- **Race Progression Tracking:** Visualize position changes and identify critical overtake moments.
- **Tyre Strategy Breakdown:** Analyze compound selections, stint durations, and pitstop execution.

---

## Repository Structure & Artifacts

This repository is structured sequentially through the four OOAD phases, strictly adhering to the **Rational Unified Process (RUP)**.

```text
Team_OOAD23/
├── UML/                    # General UML Architecture Diagrams
│   ├── ActivityDiagram.puml
│   ├── ComponentDiagram.puml
│   ├── StateDiagram.puml
│   └── CollaborationDiagram.puml
│
├── Requirements/           # Requirements Phase & Scope
│   └── Use Case/           # Use Case Diagrams & Specifications
│
├── Analysis/               # Analysis Phase Artifacts
│   ├── DomainModel/        # Core entity relationships and Domain Model
│   └── [Use Case].puml     # 5x MVC Robustness Diagrams
│
├── Design/                 # Formal Design & Implementation Blueprint
│   ├── ClassDiagram/       # Complete architecture mapping (Boundary, Controller, Entity, Service)
│   └── SequenceDiagram/    # Execution flows mapping UI to data services
│
└── Implementation/         # Source Code & Working Application
    ├── requirements.txt    # Python dependencies
    ├── app.py              # Streamlit gateway & Session Selection Views
    ├── models/             # Domain layer (TyreStint, LapTime, F1 Entities)
    ├── services/           # External and algorithmic services (FastF1 Data, Plotly Charts)
    ├── controllers/        # Strategy, Pace, and Session controllers
    └── pages/              # Modular UI Boundary views
```

---

## Quick Start & Live Application

We have translated our OOAD models into a fully working application dashboard. 

Navigate to the **[`/Implementation`](./Implementation)** directory to view the code, or run the app locally by following these steps:

```bash
# Clone the repository
git clone https://github.com/Abhics8/Team_OOAD23.git
cd Team_OOAD23/Implementation

# Install dependencies
pip install -r requirements.txt

# Run the interactive dashboard
streamlit run app.py
```
*The app will launch automatically in your browser at `http://localhost:8501`.*

---

## Contributors

This platform was designed and developed by **Group 23** for CSCI 6234 (Spring 2026):
- **Abhi Bhardwaj** ([@Abhics8](https://github.com/Abhics8))
- **Ankita Vilas Pimpalkar** ([@AnkitaVilasPimpalkar08](https://github.com/AnkitaVilasPimpalkar08))

---
*Disclaimer: This is an academic project. "Formula 1" and "F1" are trademarks of Formula One Licensing BV. This project is for educational purposes only and is not affiliated with Formula 1.*
