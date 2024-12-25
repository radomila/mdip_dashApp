"""
The about page contains a short description and source of the data used for this project.
"""


import dash
import dash_bootstrap_components as dbc
from dash import html

dash.register_page(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    path="/about",
)

url = "https://aijobs.net/salaries/download/"

# layout
layout = dbc.Container([
    html.Div([
        html.H2("About"),
        html.P("The dashboard visualizes salary levels and the job market situation in the"
               " fields of machine learning, data science, and artificial intelligence. "
               "It includes charts and interactive elements that allow dynamic data adjustments. "
               "This project was created as part of the MDIP course for the winter semester.",
               style={"width": "70%"}),
        html.Div([
            html.P("Data source:"),
            html.A(url)
        ], className="data-source")
    ], className="about-section")
])
