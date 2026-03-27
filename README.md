# FloraFlux: Biodiversity Observation Tool 🌿

A modern, nature-inspired Shiny for Python web application for recording plant observations in ecological fieldwork. Features a clean, eco-friendly design with soft earth colors, gradients, and plant imagery.

## Features

- **🌱 New Observation**: Record plant observations with observer name, species, coordinates, images, and notes
- **📋 My Observations**: Review and manage submitted observations in a styled table with delete functionality
- **🗺️ Map View**: Visualize observations on an interactive Folium map with popups
- **📊 Data Export**: Download observations as CSV for further analysis

## Design Theme

- Soft earth colors: green, beige, brown, light blue
- Subtle gradients and rounded cards with shadows
- Plant/leaf/flower imagery and emojis for friendliness
- Header with forest background image
- Hover effects and fade-in animations
- Clean, calm, and intuitive layout

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

Open http://127.0.0.1:8000 in your browser to use the app.

## Usage

1. **New Observation Tab**: Enter plant data including observer name, species name, latitude/longitude, upload images, and add notes. Click "Submit Observation" to save.
2. **My Observations Tab**: View all submitted observations in a table. Select an ID to delete or download as CSV.
3. **Map View Tab**: See observation locations plotted on an interactive map with species popups.

## Data Structure

Each observation includes:
- ID (auto-generated)
- Observer name
- Species name
- Latitude/Longitude
- Notes
- Uploaded image filenames

## Built for Ecological Field Research 🌍

This app is designed to be a modern scientific tool that's visually engaging yet not overwhelming, perfect for biodiversity monitoring in the field.