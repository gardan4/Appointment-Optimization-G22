import dash
from Dash.index import app
import dash_mantine_components as dmc
from dash import html, dcc, Input, Output, State, ctx
import dash_bootstrap_components as dbc
from Dash.callbacks import callback_register
from Dash.callbacks import callback_login

# app.config['SECRET_KEY'] = 'your_secret_key'

header = dmc.Header(
    fixed=True,
    height=75,
    children=[
        dmc.Group(
            position="apart",
            children=[
                dmc.Text("Your App Name", color="white", size="xl"),
                html.Div(
                    id='navigation-links',
                    children=[
                        dmc.Anchor("Register", href="/register", color="white",
                                   style={'padding': '0px 20px', 'margin': 'right'}),
                        dmc.Anchor("Login", href="/login", color="white",
                                   style={'padding': '0px 20px', 'margin': 'right'}),
                    ],
                    style={"display": "flex"}
                )
            ],
        )
    ],
    style={"backgroundColor": '#1e1e1e'},
)

# Add dcc.Store to hold the user's logged-in state
app.layout = html.Div([
    dcc.Store(id='session-store', storage_type='session'),
    dcc.Location(id='url', refresh=True),
    dmc.MantineProvider(
        theme={"colorScheme": "dark"},
        children=[
            dmc.Container(
                children=[
                    header,
                    dmc.Container(dash.page_container, fluid=True)
                ],
                fluid=True,
            )
        ]
    )
])


# Callback to dynamically render navigation links based on login status
@app.callback(
    Output('navigation-links', 'children'),
    Input('session-store', 'data'),
)
def update_navigation_links(session_data):
    print(session_data)
    if session_data and 'username' in session_data:
        # User is logged in, show all links including Logout
        return [
            dmc.Anchor("Plan Appointment", href="/plan_appointment", color="white", className='nav-list-items'),
            dmc.Anchor("Planned Appointments", href="/planned_appointments", color="white", className='nav-list-items'),
            dmc.Anchor(href="#", children=[
                dmc.Button("Logout", id="logout-button", n_clicks=0, style={
                    "background": "none",
                    "border": "none",
                    "color": "white",
                    "padding": "0",
                    "margin": "0",
                    "cursor": "pointer"
                }),
            ], style={"textDecoration": "none", "color": "white"}, className='nav-list-items')

        ]
    else:
        # User is not logged in, only show the Register and Login links
        return [
            dmc.Anchor("Register", href="/register", color="white", className='nav-list-items'),
            dmc.Anchor("Login", href="/login", color="white", className='nav-list-items'),
        ]


# Update the callback for logout process
# Callback for the logout process
@app.callback(
    [Output('session-store', 'data', allow_duplicate=True), Output('url', 'pathname')],
    [Input('logout-button', 'n_clicks')],
    prevent_initial_call=True
)
def logout_user(n_clicks):
    if n_clicks:
        # Clear the session data and redirect to the login page
        return {}, '/login'
    return dash.no_update, dash.no_update



# You'll need to add a check on the plan_appointment and planned_appointments pages
# to redirect the user to the login page if they are not logged in. Here's a placeholder example:
@app.callback(
    Output('page-content', 'children'),
    [Input('session-store', 'data')],
    prevent_initial_call=True,
)
def protect_pages(session_data):
    if not (session_data and 'username' in session_data):
        # Redirect to login page
        return dcc.Location(href='/login', id='login-redirect')
    # Otherwise, allow access to the page content
    return html.Div(id='page-content')

# Remember to add similar protection to all pages that require authentication

