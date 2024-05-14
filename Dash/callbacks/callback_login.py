from Dash.index import app
import dash
from dash.dependencies import Input, Output, State
import os


# Function to check if user is registered
def is_user_registered(name):
    users_file = './Data/users.txt'
    if os.path.exists(users_file):
        with open(users_file, 'r') as file:
            for line in file:
                registered_name, registered_location = line.strip().split(',', 1)
                if registered_name == name:
                    return [registered_name, registered_location]
    return [False, False]


@app.callback(
    [Output('session-store', 'data'), Output('url', 'pathname', allow_duplicate=True)],
    [Input('login-button', 'n_clicks')],
    [State('login-name-input', 'value')],
    prevent_initial_call=True
)
def login(n_clicks, name):
    if n_clicks:
        user_data = is_user_registered(name)
        if name and user_data[0] == name:
            # Log the user in by setting the session data and redirecting
            return {'username': user_data[0], 'location': user_data[1]}, '/plan_appointment'
        else:
            # Clear any existing session data and force stay on the login page
            return {}, '/login'
    return {}, '/login'

