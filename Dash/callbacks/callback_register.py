from Dash.index import app
import dash
from dash.dependencies import Input, Output, State
import os


# Function to register user
def register_user(name, city):
    # Path to the user data file
    users_file = 'users.txt'

    # Check if file exists, if not, create it
    if not os.path.exists(users_file):
        open(users_file, 'a').close()

    # Add user data to the file
    with open(users_file, 'a') as file:
        file.write(f"{name},{city}\n")


@app.callback(
    Output("registration-output", "children"),
    [Input("register-button", "n_clicks")],
    [State("name-input", "value"), State("city-input", "value")],
    prevent_initial_call=True
)
def on_register_click(n_clicks, name, city):
    if name and city:
        register_user(name, city)
        return f"User {name} from {city} registered successfully!"
    return "Please enter both name and city."
