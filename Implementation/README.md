# 🏎️ F1 Insights & Strategy Explorer — Implementation

An interactive dashboard for analyzing Formula 1 race data, built as the implementation phase of the OOAD project (CSCI 6234 - Group 23).

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit%20Cloud-FF4B4B?logo=streamlit)](https://teamooad23-hwm9sxennf9mk2poes7zga.streamlit.app)
**[Launch Live Dashboard →](https://teamooad23-hwm9sxennf9mk2poes7zga.streamlit.app)**

## 📸 Features

- **Session Selection** — Choose Season → Race → Session with cascading dropdowns
- **Driver Comparison** — Select up to 2 drivers to compare side-by-side
- **Lap Time Analysis** — Interactive lap-by-lap pace comparison chart
- **Position Tracking** — Position changes over laps with overtake visualization
- **Tyre Strategy** — Stint duration comparison with compound color coding

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend/UI | Streamlit |
| Data Source | FastF1 (Python F1 Data Library) |
| Charts | Plotly |
| Language | Python 3.10+ |

## 📐 Architecture (from Class Diagram)

```
Boundary Classes (Views)     →  Streamlit Pages
Controller Classes           →  controllers/ package
Service Classes              →  services/ package
Entity Classes               →  models/entities.py
```

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- pip

### Installation

```bash
cd Implementation
pip install -r requirements.txt
```

### Running Locally

```bash
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`.

## 📁 Project Structure

```
Implementation/
├── app.py                          # Main entry point (Session + Driver Selection)
├── requirements.txt                # Python dependencies
├── .streamlit/config.toml          # Streamlit theme config
├── models/
│   └── entities.py                 # Entity classes (Season, Race, Driver, etc.)
├── services/
│   ├── fastf1_service.py           # FastF1DataService
│   └── chart_generator.py          # ChartGenerator
├── controllers/
│   ├── session_controller.py       # SessionController
│   ├── driver_controller.py        # DriverController
│   ├── laptime_controller.py       # LapTimeController
│   ├── position_controller.py      # PositionController
│   └── tyre_controller.py          # TyreStrategyController
└── pages/
    ├── 1_Lap_Time_Comparison.py    # LapTimeComparisonView
    ├── 2_Position_Over_Laps.py     # PositionTrackingView
    └── 3_Tyre_Strategy.py          # TyreStintView
```

## 👥 Team — Group OOAD23

- Abhi Bhardwaj
- Ankita Vilas Pimpalkar

## 📄 License

This project is part of CSCI 6234 coursework at George Washington University.
