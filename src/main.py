"""The main file defines the root structure of the app."""

import dash
from dash import Dash, html
import dash_bootstrap_components as dbc

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])

# navbar
navbar = html.Div([
    dbc.Nav([
        dbc.NavLink([
            html.I(className="fa-solid fa-sack-dollar"),
            "Salaries"
        ], href="/", className="navbar-link"),
        dbc.NavLink([
            html.I(className="fa-solid fa-chart-line"),
            "Job Market"
        ], href="/job-market", className="navbar-link"),
        dbc.NavLink([
            html.I(className="fa-solid fa-house"),
            "About"
        ], href="/about", className="navbar-link"),
    ],
        vertical=True,
        pills=True
    ),
    ],
    className="navbar"
)

# layout
app.layout = html.Div(
    children=[
        navbar,  
        html.Div(
            dash.page_container,
            style={
                "marginLeft": "220px",
                "padding": "2em",
                "backgroundColor": "var(--light-grey)",
                "minHeight": "100vh",
            },
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)