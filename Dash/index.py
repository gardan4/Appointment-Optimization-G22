# index.py
from dash import Dash
import dash_bootstrap_components as dbc

external_stylesheets = ['https://use.fontawesome.com/releases/v5.8.1/css/all.css', "./assets/style.css", "./assets/appointment.css"]
app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True
)
app_title = "Planning scheduler"
app.title = app_title