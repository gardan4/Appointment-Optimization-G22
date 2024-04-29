from dash import html, dcc, callback, Input, Output, State
import dash_mantine_components as dmc
import dash


layout = html.Div([
    dmc.Paper(
        children=[
            dmc.Title("Register"),
            dmc.TextInput(label="Name", id="name-input", placeholder="Enter your name"),
            dmc.TextInput(label="City", id="city-input", placeholder="Enter your city"),
            dmc.Button("Register", id="register-button"),
            html.Div(id="registration-output")
        ],
    )
])

dash.register_page(
    __name__,
    path='/register',
    # redirect_from=['/'],
    title='Register',
    layout=layout,
)





