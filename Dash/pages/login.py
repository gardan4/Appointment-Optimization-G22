from dash import html, dcc, callback, Input, Output, State
import dash_mantine_components as dmc
import dash

layout = html.Div([
    dmc.Paper(
        children=[
            dmc.Title("Login"),
            dmc.TextInput(label="Name", id="login-name-input", placeholder="Enter your name"),
            dmc.Button("Login", id="login-button"),
            html.Div(id="login-output")
        ],
    )
])

dash.register_page(
    __name__,
    path='/login',
    # redirect_from=['/'],
    title='Login',
    layout=layout,
)



