# FloraFlux: Biodiversity Observation Tool
# A Shiny for Python web application for recording plant observations in ecological fieldwork.
# Features a modern, nature-inspired design with soft earth colors, gradients, and plant imagery.
# To run: shiny run --reload src/app.py

from shiny import App, ui, render, reactive, session
import pandas as pd
import folium
import os

# Custom CSS for nature-inspired design
custom_css = """
/* Global styles */
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #f5f5dc; /* Beige background */
    color: #2f4f2f; /* Dark green text */
}

/* Header banner */
.header-banner {
    background-image: url('https://images.unsplash.com/photo-1441974231531-c6227db76b6e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80');
    background-size: cover;
    background-position: center;
    height: 200px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    color: white;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    border-radius: 15px;
    margin-bottom: 20px;
    position: relative;
}

.header-banner::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 100, 0, 0.3); /* Dark green overlay */
    border-radius: 15px;
}

.header-banner h1, .header-banner p {
    position: relative;
    z-index: 1;
    margin: 0;
}

/* Card styling */
.card {
    background: linear-gradient(135deg, #e8f5e8 0%, #f0f8ff 100%); /* Light green to light blue gradient */
    border-radius: 15px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    padding: 20px;
    margin: 20px 0;
    border: 1px solid #d2b48c; /* Tan border */
}

/* Button styling */
.btn-primary {
    background: linear-gradient(135deg, #228b22 0%, #32cd32 100%); /* Green gradient */
    border: none;
    border-radius: 25px;
    padding: 10px 20px;
    color: white;
    font-weight: bold;
    transition: all 0.3s ease;
}

.btn-primary:hover {
    background: linear-gradient(135deg, #32cd32 0%, #228b22 100%);
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.btn-secondary {
    background: linear-gradient(135deg, #d2b48c 0%, #f5deb3 100%); /* Tan gradient */
    border: none;
    border-radius: 25px;
    padding: 10px 20px;
    color: #2f4f2f;
    font-weight: bold;
    transition: all 0.3s ease;
}

.btn-secondary:hover {
    background: linear-gradient(135deg, #f5deb3 0%, #d2b48c 100%);
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.btn-danger {
    background: linear-gradient(135deg, #dc143c 0%, #ff6347 100%); /* Red gradient */
    border: none;
    border-radius: 25px;
    padding: 10px 20px;
    color: white;
    font-weight: bold;
    transition: all 0.3s ease;
}

.btn-danger:hover {
    background: linear-gradient(135deg, #ff6347 0%, #dc143c 100%);
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.btn-info {
    background: linear-gradient(135deg, #4682b4 0%, #87ceeb 100%); /* Blue gradient */
    border: none;
    border-radius: 25px;
    padding: 10px 20px;
    color: white;
    font-weight: bold;
    transition: all 0.3s ease;
}

.btn-info:hover {
    background: linear-gradient(135deg, #87ceeb 0%, #4682b4 100%);
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

/* Table styling */
.table {
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.table th {
    background: linear-gradient(135deg, #228b22 0%, #32cd32 100%);
    color: white;
    border: none;
}

.table td {
    border: none;
    background-color: #f9f9f9;
}

/* Map container */
.map-container {
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

/* Plant image styling */
.plant-image {
    max-width: 100px;
    border-radius: 10px;
    margin: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* Footer */
.footer {
    text-align: center;
    margin-top: 40px;
    padding: 20px;
    background: linear-gradient(135deg, #228b22 0%, #32cd32 100%);
    color: white;
    border-radius: 15px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

/* Animation */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.card {
    animation: fadeIn 0.5s ease-in-out;
}
"""

# UI Layout
app_ui = ui.page_fluid(
    # Global header
    ui.tags.div(
        ui.tags.h1("FloraFlux 🌿", style="font-size: 3em; margin-bottom: 10px;"),
        ui.tags.p("Capture biodiversity in the field", style="font-size: 1.2em;"),
        class_="header-banner"
    ),

    # Custom CSS
    ui.tags.style(custom_css),

    # Navbar with tabs
    ui.navset_tab(
        ui.nav_panel(
            "🌱 New Observation",
            ui.div(
                ui.tags.h3("Record a New Plant Observation", style="color: #228b22; text-align: center;"),
                ui.input_text("observer", "Observer Name 🌿", placeholder="Enter your name"),
                ui.input_text("species", "Species Name 🌸", placeholder="e.g., Quercus alba"),
                ui.layout_column_wrap(
                    ui.input_numeric("lat", "Latitude 📍", value=0, min=-90, max=90),
                    ui.input_numeric("long", "Longitude 📍", value=0, min=-180, max=180),
                    width=1/2
                ),
                ui.input_file("images", "Upload Plant Images 📷", multiple=True, accept=[".jpg", ".jpeg", ".png"]),
                ui.input_text_area("notes", "Notes / Comments 📝", placeholder="Additional observations..."),
                ui.layout_column_wrap(
                    ui.input_action_button("submit", "Submit Observation ✅", class_="btn-primary"),
                    ui.input_action_button("clear", "Clear Form 🗑️", class_="btn-secondary"),
                    width=1/2
                ),
                # Decorative plant image
                ui.tags.img(src="https://images.unsplash.com/photo-1416879595882-3373a0480b5b?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80", 
                           alt="Decorative plant", class_="plant-image", style="float: right;"),
                class_="card"
            )
        ),
        ui.nav_panel(
            "📋 My Observations",
            ui.div(
                ui.tags.h3("Review Your Observations", style="color: #228b22; text-align: center;"),
                ui.output_table("obs_table"),
                ui.layout_column_wrap(
                    ui.input_select("delete_id", "Select Observation ID to Delete 🗑️", choices=[]),
                    ui.input_action_button("delete", "Delete Selected ❌", class_="btn-danger"),
                    width=1/2
                ),
                ui.download_button("download", "Download as CSV 📊", class_="btn-info"),
                class_="card"
            )
        ),
        ui.nav_panel(
            "🗺️ Map View",
            ui.div(
                ui.tags.h3("Observation Map", style="color: #228b22; text-align: center;"),
                ui.div(
                    ui.output_ui("map"),
                    class_="map-container"
                ),
                class_="card"
            )
        ),
        id="navbar"
    ),

    # Footer
    ui.tags.div(
        ui.tags.p("Built for ecological field research 🌍", style="margin: 0;"),
        class_="footer"
    )
)

# Server Logic
def server(input, output, session):
    # Reactive value to store observations
    observations = reactive.Value([])

    # Submit observation
    @reactive.Effect
    @reactive.event(input.submit)
    def submit_observation():
        # Basic validation
        if not input.observer().strip() or not input.species().strip():
            ui.notification_show("Please enter observer name and species.", type="error")
            return
        
        lat = input.lat()
        long = input.long()
        if not (-90 <= lat <= 90) or not (-180 <= long <= 180):
            ui.notification_show("Invalid coordinates. Latitude must be -90 to 90, Longitude -180 to 180.", type="error")
            return
        
        # Handle uploaded images (store filenames)
        images = input.images()
        filenames = [f['name'] for f in images] if images else []
        
        # Create observation dict
        obs_id = len(observations()) + 1
        obs = {
            'id': obs_id,
            'observer': input.observer(),
            'species': input.species(),
            'latitude': lat,
            'longitude': long,
            'notes': input.notes(),
            'images': ', '.join(filenames) if filenames else 'None'
        }
        
        # Add to observations
        observations.set(observations() + [obs])
        ui.notification_show(f"Observation #{obs_id} submitted successfully!", type="message")

    # Clear form
    @reactive.Effect
    @reactive.event(input.clear)
    def clear_form():
        ui.update_text("observer", value="")
        ui.update_text("species", value="")
        ui.update_numeric("lat", value=0)
        ui.update_numeric("long", value=0)
        ui.update_file("images", value=None)
        ui.update_text_area("notes", value="")

    # Update delete choices reactively
    @reactive.Effect
    def update_delete_choices():
        choices = [str(obs['id']) for obs in observations()]
        ui.update_select("delete_id", choices=choices)

    # Render observations table
    @render.table
    def obs_table():
        df = pd.DataFrame(observations())
        if df.empty:
            return pd.DataFrame(columns=['ID', 'Observer', 'Species', 'Latitude', 'Longitude', 'Notes', 'Images'])
        return df[['id', 'observer', 'species', 'latitude', 'longitude', 'notes', 'images']].rename(
            columns={'id': 'ID', 'observer': 'Observer', 'species': 'Species', 
                     'latitude': 'Latitude', 'longitude': 'Longitude', 'notes': 'Notes', 'images': 'Images'}
        )

    # Delete selected observation
    @reactive.Effect
    @reactive.event(input.delete)
    def delete_observation():
        if not input.delete_id():
            ui.notification_show("Please select an observation to delete.", type="warning")
            return
        id_to_delete = int(input.delete_id())
        new_obs = [obs for obs in observations() if obs['id'] != id_to_delete]
        observations.set(new_obs)
        ui.notification_show(f"Observation #{id_to_delete} deleted.", type="message")

    # Render map
    @render.ui
    def map():
        if not observations():
            return ui.HTML("<p>No observations to display on map.</p>")
        
        # Create folium map centered on average location
        lats = [obs['latitude'] for obs in observations()]
        longs = [obs['longitude'] for obs in observations()]
        center_lat = sum(lats) / len(lats)
        center_long = sum(longs) / len(longs)
        
        m = folium.Map(location=[center_lat, center_long], zoom_start=10)
        
        # Add markers
        for obs in observations():
            popup_text = f"<b>{obs['species']}</b><br>Observer: {obs['observer']}<br>Notes: {obs['notes']}"
            folium.Marker(
                [obs['latitude'], obs['longitude']], 
                popup=popup_text,
                tooltip=obs['species']
            ).add_to(m)
        
        return ui.HTML(m._repr_html_())

    # Download handler for CSV
    @session.download(filename="floraflux_observations.csv")
    def download():
        df = pd.DataFrame(observations())
        return df.to_csv(index=False)

# Create and run the app
app = App(app_ui, server)