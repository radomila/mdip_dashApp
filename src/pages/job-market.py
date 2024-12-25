"""
The job market page represents the situation on the job market in artificial intelligence, machine learning and data science.

This page contains:

1. Line chart showing the development of a different work modes, such as hybrid, onsite and remote work mode. Checkbox above the graph enables to show a different combinations.
2. Sankey diagram showing the relationship between employment type and company size. Checkbox above the graph enables to show data for a specific year.

Button below each graph shows information about what the graph expresses.
"""


import dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html
from src.utils import create_graph_button, get_info_text

dash.register_page(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    path="/job-market",
)

df = pd.read_csv("data/salaries.csv")

remote_ratio_labels = {
    0: "Onsite",
    50: "Hybrid",
    100: "Remote"
}

remote_ratio_counts = (
    df.groupby(['work_year', 'remote_ratio'])
    .size()
    .reset_index(name='count')
    .assign(label=lambda x: x['remote_ratio'].map(remote_ratio_labels))
)

df_filtered = df.groupby(['work_year', 'company_size', 'experience_level']).size().reset_index(name='count')

work_years = [{"label": str(year), "value": year} for year in sorted(df["work_year"].unique(), reverse=True)]

# layout
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dcc.Checklist(
                id="remote-ratio-items",
                options=[{"label": label, "value": label} for label in remote_ratio_labels.values()],
                value=["Onsite"],
                className="checklist-container",
                labelStyle={
                    "display": "flex",
                    "align-items": "center",
                    "font-size": "16px",
                    "gap": "10px",
                    "paddingTop": "5px"
                },
            ),
            dcc.Loading(
                id="loading-graph",
                type="default",
                children=dcc.Graph(id="remote-ratio-graph")
            )
        ], width=6),
        dbc.Col([
            dbc.Col([
                dcc.Dropdown(
                    id="work-years-dropdown",
                    options=work_years,
                    value=2020,
                    placeholder="Select a work year",
                    className="dropdown-item"
                )
            ], width=6),
            dcc.Loading(
                id="loading-sankey",
                type="default",
                children=dcc.Graph(id="sankey-diagram")
            )
        ], width=6),
        dbc.Row([
            dbc.Col([
                create_graph_button("show-info-button-remote-ratio"),
                html.Div(id="info-text-remote-ratio", style={'display': 'none'})
            ], width=6),
            dbc.Col([
                create_graph_button("show-info-button-sankey"),
                html.Div(id="info-text-sankey", style={'display': 'none'})
            ], width=6)
        ])
    ], className="graphs-container")
])


@dash.callback(
    [Output("info-text-sankey", "children"),
     Output("info-text-sankey", "style"),
     Output("show-info-button-sankey", "children")],
    Input("show-info-button-sankey", "n_clicks")
)
def display_text_sankey(n_clicks):
    """Displays and hides the information about the graph

    Args:
        n_clicks (integer or None): The number of times the button has been clicked.

    Returns:
        tuple: A tuple containing:
        - str: The information text to display (or an empty string if hidden).
        - dict: The CSS style dict controlling visibility (`{'display': 'block'}` or `{'display': 'none'}`).
        - str: The button text, either "Show Info" or "Hide Info".
        """
    if n_clicks is None:
        n_clicks = 0

    if n_clicks % 2 == 1:
        return get_info_text("sankey"), {'display': 'block'}, "Hide Info"
    else:
        return "", {'display': 'none'}, "Show Info"


@dash.callback(
    [Output("info-text-remote-ratio", "children"),
     Output("info-text-remote-ratio", "style"),
     Output("show-info-button-remote-ratio", "children")],
    Input("show-info-button-remote-ratio", "n_clicks")
)
def display_text_remote_ratio(n_clicks):
    """Displays and hides the information about the graph

    Args:
        n_clicks (integer or None): The number of times the button has been clicked.

    Returns:
        tuple: A tuple containing:
        - str: The information text to display (or an empty string if hidden).
        - dict: The CSS style dict controlling visibility (`{'display': 'block'}` or `{'display': 'none'}`).
        - str: The button text, either "Show Info" or "Hide Info".
    """
    if n_clicks is None:
        n_clicks = 0

    if n_clicks % 2 == 1:
        return get_info_text("remote_ratio"), {'display': 'block'}, "Hide Info"
    else:
        return "", {'display': 'none'}, "Show Info"


@dash.callback(
    Output("sankey-diagram", "figure"),
    Input("work-years-dropdown", "value")
)
def update_sankey_graph(selected_work_year):
    """Updates the Sankey diagram based on the selected work year.

    Args:
        selected_work_year (int or None): The selected year from the dropdown menu.
                                          If None, no year is selected.

    Returns:
        plotly.graph_objects.Figure: A Sankey diagram showing the flow between company size
                                     and experience level for the selected year. If no year
                                     is selected, a blank figure with a placeholder title
                                     is returned.
        """
    if not selected_work_year:
        return go.Figure().update_layout(title="No data selected")

    filtered_data = df_filtered[df_filtered["work_year"] == selected_work_year].copy()

    filtered_data.loc[:, 'company_size_label'] = filtered_data['company_size'].map({'S': 'Small', 'M': 'Medium', 'L': 'Large'})

    company_sizes = filtered_data['company_size_label'].unique()
    experience_levels = filtered_data['experience_level'].unique()

    all_nodes = list(company_sizes) + list(experience_levels)

    source_indices = filtered_data['company_size_label'].apply(lambda x: all_nodes.index(x))
    target_indices = filtered_data['experience_level'].apply(lambda x: all_nodes.index(x))

    sankey_figure = go.Figure(go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            label=all_nodes,
            color=["#1f77b4", "#D967B5", "#FF7F46", "#5DADE2", "#F8839E", "#FFA366", "#AE86DB"]

        ),
        link=dict(
            source=source_indices,
            target=target_indices,
            value=filtered_data['count'],
        )
    ))

    sankey_figure.update_layout(title=f"Company Size vs Experience Level Flow for {selected_work_year}")
    return sankey_figure


@dash.callback(
    Output("remote-ratio-graph", "figure"),
    Input("remote-ratio-items", "value")
)
def update_graph(selected_ratios):
    """Updates the line chart showing remote work trends based on selected work modes.

    Args:
        selected_ratios (list of str): List of selected work modes (e.g., "Onsite",
                                       "Hybrid", "Remote") from the checklist.
                                       If empty, no data is selected.

    Returns:
        plotly.express.Figure: A line chart showing the number of employees working
                               in each selected work mode over time. If no modes
                               are selected, a blank chart with a placeholder title
                               is returned.
        """
    if not selected_ratios:
        return px.line(title="No data selected")

    filtered_data = remote_ratio_counts[remote_ratio_counts['label'].isin(selected_ratios)]

    color_map = {
        "Onsite": "#1f77b4",
        "Hybrid": "#D967B5",
        "Remote": "#ff7f0e"
    }

    fig = px.line(
        filtered_data,
        x="work_year",
        y="count",
        color="label",
        title="Number of Employees Working Remotely by Remote Ratio",
        labels={
            "work_year": "Year",
            "count": "Number of Employees",
            "label": "Work Mode"
        },
        markers=True,
        color_discrete_map=color_map
    )

    fig.update_layout(
        xaxis=dict(
            tickmode="array",
            tickvals=filtered_data["work_year"].unique(),
            ticktext=[str(year) for year in filtered_data["work_year"].unique()],
        ),
        yaxis=dict(
            rangemode="tozero"
        )
    )
    return fig
