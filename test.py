# Basic Shiny for Python App
# This app demonstrates core Shiny functionality with a simple UI and reactive server logic.
# To run this app, open a terminal and use: shiny run --reload app.py

from shiny import App, ui, render

# Define the UI (User Interface)
# The UI describes what the app looks like and what inputs/outputs it has.
app_ui = ui.page_fluid(
    # Title panel at the top
    ui.panel_title("My Shiny App"),
    
    # Text input for the user's name
    ui.input_text("name", "Enter your name:", ""),
    
    # Slider input for choosing a number between 1 and 100
    ui.input_slider("number", "Choose a number:", min=1, max=100, value=50),
    
    # Output text area that will display the reactive message
    ui.output_text("message")
)

# Define the server logic
# The server function contains the instructions for how to build the app.
# It takes three arguments: input, output, and session.
def server(input, output, session):
    # This is a reactive expression that updates whenever the inputs change
    @render.text
    def message():
        # Get the current value of the name input
        name = input.name()
        # Get the current value of the number input
        num = input.number()
        # Return a formatted message combining the inputs
        return f"Hello {name}, your number is {num}"

# Create the Shiny app by combining the UI and server
app = App(app_ui, server)