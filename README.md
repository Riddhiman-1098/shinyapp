# FloraFlux: Biodiversity Observation Tool

A Shiny for Python web application for recording plant observations in ecological fieldwork.

## Features

- **New Observation**: Record plant observations with metadata, location, images, and notes
- **My Observations**: Review and manage submitted observations in a table
- **Map View**: Visualize observations on an interactive map

## Requirements

- Python 3.8+
- Shiny for Python
- Folium
- Pandas

## Installation

Install dependencies:
```bash
pip install shiny folium pandas
```

## Running the App

From the project root:
```bash
shiny run --reload src/app.py
```

Open the provided URL in your browser to use the app.

## Usage

1. Navigate to "New Observation" tab to enter plant data
2. Submit observations and review them in "My Observations"
3. View locations on the map in "Map View"
4. Download observations as CSV for further analysis