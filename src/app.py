# FloraFlux: Biodiversity Observation Tool
# A Shiny for Python web application for recording plant observations in ecological fieldwork.
# To run: shiny run --reload src/app.py

from shiny import App, ui, render, reactive, session
import pandas as pd
import folium
import os

# UI Layout
app_ui = ui.page_navbar(
    ui.nav_panel("New Observation",
        ui.h3("Record a New Plant Observation"),
        ui.input_text("observer", "Observer Name", placeholder="Enter your name"),
        ui.input_text("species", "Species Name", placeholder="e.g., Quercus alba"),
        ui.input_numeric("lat", "Latitude", value=0, min=-90, max=90),
        ui.input_numeric("long", "Longitude", value=0, min=-180, max=180),
        ui.input_file("images", "Upload Plant Images", multiple=True, accept=[".jpg", ".jpeg", ".png"]),
        ui.input_text_area("notes", "Notes / Comments", placeholder="Additional observations..."),
        ui.layout_column_wrap(
            ui.input_action_button("submit", "Submit Observation", class_="btn-primary"),
            ui.input_action_button("clear", "Clear Form", class_="btn-secondary"),
            width=1/2
        )
    ),
    ui.nav_panel("My Observations",
        ui.h3("Review Your Observations"),
        ui.output_table("obs_table"),
        ui.input_select("delete_id", "Select Observation ID to Delete", choices=[]),
        ui.input_action_button("delete", "Delete Selected", class_="btn-danger"),
        ui.download_button("download", "Download as CSV", class_="btn-info")
    ),
    ui.nav_panel("Map View",
        ui.h3("Observation Map"),
        ui.output_ui("map")
    ),
    title="FloraFlux",
    id="navbar"
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