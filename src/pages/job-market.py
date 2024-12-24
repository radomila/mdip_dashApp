import dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc

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

# Layout aplikace
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
                    value=2024,
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
    ], className="graphs-container")
])


@dash.callback(
    Output("sankey-diagram", "figure"),
    Input("work-years-dropdown", "value")
)
def update_sankey_graph(selected_work_year):
    if not selected_work_year:
        return go.Figure().update_layout(title="No data selected")

    filtered_data = df_filtered[df_filtered["work_year"] == selected_work_year]

    filtered_data['company_size_label'] = filtered_data['company_size'].map({'S': 'Small', 'M': 'Medium', 'L': 'Large'})

    company_sizes = filtered_data['company_size_label'].unique()
    experience_levels = filtered_data['experience_level'].unique()

    all_nodes = list(company_sizes) + list(experience_levels)

    source_indices = filtered_data['company_size_label'].apply(lambda x: all_nodes.index(x))
    target_indices = filtered_data['experience_level'].apply(lambda x: all_nodes.index(x))

    sankey_figure = go.Figure(go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=all_nodes,
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
    if not selected_ratios:
        return px.line(title="No data selected")

    filtered_data = remote_ratio_counts[remote_ratio_counts['label'].isin(selected_ratios)]

    color_map = {
        "Onsite": "#1f77b4",
        "Hybrid": "#2ca02c",
        "Remote": "#e57373"
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
            "label": "Remote Ratio"
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
