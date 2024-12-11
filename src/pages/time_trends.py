import dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import dcc, html, callback

dash.register_page(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    path="/time-trends",
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

# Layout aplikace
layout = dbc.Container([
    html.Div([
        dcc.Checklist(
            id="remote-ratio-items",
            options=[
                {"label": label, "value": label} for label in remote_ratio_labels.values()
            ],
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
    ])
])

# Callback pro aktualizaci grafu
@dash.callback(
    Output("remote-ratio-graph", "figure"),
    Input("remote-ratio-items", "value")
)
def update_graph(selected_ratios):
    if not selected_ratios:
        return px.line(title="No data selected")

    filtered_data = remote_ratio_counts[remote_ratio_counts['label'].isin(selected_ratios)]

    fig = px.line(
        filtered_data,
        x="work_year",
        y="count",
        color="label",
        title="Number of Employees Working Remotely by Remote Ratio",
        labels={
            "work_year": "Year",
            "count": "Number of Employees",
            "label": "Remote Ratio"
        },
        markers=True
    )

    fig.update_layout(
        xaxis=dict(
            tickmode="array",
            tickvals=filtered_data["work_year"].unique(),
            ticktext=[str(year) for year in filtered_data["work_year"].unique()],
        )
    )
    return fig