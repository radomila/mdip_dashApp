import dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import dcc, html

dash.register_page(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    path="/salaries",
)

df = pd.read_csv("data/salaries.csv")

experience_levels = [{"label": i, "value": i} for i in df["experience_level"].unique()]
employment_types = [{"label": i, "value": i} for i in df["employment_type"].unique()]
company_sizes = [{"label": i, "value": i} for i in df["company_size"].unique()]
job_titles = df["job_title"].unique()

layout = dbc.Container([
    html.Div([
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    options=experience_levels,
                    placeholder="Select an experience level",
                    className="dropdown-item",
                    id="experience-dropdown"
                ),
                dcc.Dropdown(
                    options=employment_types,
                    placeholder="Select an employment type",
                    className="dropdown-item",
                    id="employment-dropdown"
                ),
            ]),
            dbc.Col([
                dcc.Dropdown(
                    options=company_sizes,
                    placeholder="Select a company size",
                    className="dropdown-item",
                    id="company-dropdown"
                ),
            ]),
        ], className="dropdown-container"),
        dcc.Loading(
            id="loading-graph",
            type="default",
            children=dcc.Graph(id="salary-graph")
        )
    ])
])

# Callback funkce pro aktualizaci grafu
@dash.callback(
    Output("salary-graph", "figure"),
    [
        Input("experience-dropdown", "value"),
        Input("employment-dropdown", "value"),
        Input("company-dropdown", "value")
    ]
)

def update_graph(experience_levels, employment_types, company_sizes):
    filtered_df = df.copy()

    if experience_levels:
        filtered_df = filtered_df[filtered_df["experience_level"] == experience_levels]
    if employment_types:
        filtered_df = filtered_df[filtered_df["employment_type"] == employment_types]
    if company_sizes:
        filtered_df = filtered_df[filtered_df["company_size"] == company_sizes]

    average_salary_per_year = filtered_df.groupby("work_year")["salary_in_usd"].mean().reset_index()

    fig = px.bar(
        average_salary_per_year,
        x="work_year",
        y="salary_in_usd",
        title="Average annual salary in AI, ML and Data Science from 2020 to 2024 worldwide",
        labels={
            "work_year": "Year",
            "salary_in_usd": "Average salary in USD"
        },
    )

    fig.update_layout(
        xaxis=dict(
            tickmode="array",
            tickvals=filtered_df["work_year"].unique(),
            ticktext=[str(year) for year in filtered_df["work_year"].unique()],
        )
    )

    return fig