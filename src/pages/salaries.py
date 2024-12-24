import dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import dcc, html
import pycountry
from src.utils import format_to_k, create_graph_button, get_info_text

dash.register_page(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    path="/",
)

# Data loading
df = pd.read_csv("data/salaries.csv")

average_salary_per_country = df.groupby("company_location")["salary_in_usd"].mean()
min_average_salary_per_country = format_to_k(average_salary_per_country.min())
max_average_salary_per_country = format_to_k(average_salary_per_country.max())
average_salary = format_to_k(df["salary_in_usd"].sum() / df['salary_in_usd'].count())

choropleth_df = average_salary_per_country.reset_index()
choropleth_df.columns = ["company_location", "avg_salary"]

min_salary_location = choropleth_df.loc[choropleth_df["avg_salary"] == choropleth_df["avg_salary"].min(), "company_location"].iloc[0]
min_salary_location_fullname = pycountry.countries.get(alpha_2=min_salary_location).official_name

max_salary_location = choropleth_df.loc[choropleth_df["avg_salary"] == choropleth_df["avg_salary"].max(), "company_location"].iloc[0]
max_salary_location_fullname = pycountry.countries.get(alpha_2=max_salary_location).official_name

# Function for converting country codes to ISO-3
def convert_to_iso3(country_code):
    try:
        return pycountry.countries.lookup(country_code).alpha_3
    except LookupError:
        return None


choropleth_df["company_location"] = choropleth_df["company_location"].apply(convert_to_iso3)
choropleth_df = choropleth_df.dropna(subset=["company_location"])

fig = px.choropleth(
    choropleth_df,
    locations="company_location",
    color="avg_salary",
    locationmode="ISO-3",
    color_continuous_scale="blues",
    title="Average Salary by Country in USD"
)

fig.update_layout(
    title_font=dict(
        size=13,
    )
)

experience_levels = [{"label": i, "value": i} for i in df["experience_level"].unique()]
employment_types = [{"label": i, "value": i} for i in df["employment_type"].unique()]
company_sizes = [{"label": i, "value": i} for i in df["company_size"].unique()]
job_titles = df["job_title"].unique()

# Layout
layout = dbc.Container([
    dbc.Row([
        dbc.Col(dbc.Card(
            dbc.CardBody([
                html.P("Average Salary", className="card-title"),
                html.H4(f"$ {average_salary}", className="average-salary"),
                html.P("Average salary across all countries", className="card-country-name")
            ], className="card-body")
        )),
        dbc.Col(dbc.Card(
            dbc.CardBody([
                html.P("The Highest Salary", className="card-title"),
                html.H4(f"$ {max_average_salary_per_country}", className="highest-salary"),
                html.P(f"{max_salary_location_fullname}", className="card-country-name")
            ], className="card-body")
        )),
        dbc.Col(dbc.Card(
            dbc.CardBody([
                html.P("The Lowest Salary", className="card-title"),
                html.H4(f"$ {min_average_salary_per_country}", className="lowest-salary"),
                html.P(f"{min_salary_location_fullname}", className="card-country-name")
            ], className="card-body")
        ))
    ], className="cards-section"),
    dbc.Row([
        dbc.Col([
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
            ),
        ], width=6),
        dbc.Col([
            dcc.Graph(
                figure=fig,
                id="choropleth-graph"
            ),
        ], width=6),
    ], className="graphs-container"),
    dbc.Row([
        dbc.Col([
            create_graph_button("show-info-button"),
            html.Div(id="info-text", style={'display': 'none'})
        ], width=6),
        dbc.Col([
            create_graph_button("show-info-button-choropleth"),
            html.Div(id="info-text-choropleth", style={'display': 'none'})
        ], width=6)
    ])
])

@dash.callback(
    [Output("info-text-choropleth", "children"),
     Output("info-text-choropleth", "style"),
     Output("show-info-button-choropleth", "children")],
    Input("show-info-button-choropleth", "n_clicks")
)


def display_text_choropleth(n_clicks):
    if n_clicks is None:
        n_clicks = 0

    if n_clicks % 2 == 1:
        return get_info_text("avg_salary_choropleth"), {'display': 'block'}, "Hide Info"
    else:
        return "", {'display': 'none'}, "Show Info"


@dash.callback(
    [Output("info-text", "children"),
     Output("info-text", "style"),
     Output("show-info-button", "children")],
    Input("show-info-button", "n_clicks")
)


def display_text(n_clicks):
    if n_clicks is None:
        n_clicks = 0

    if n_clicks % 2 == 1:
        return get_info_text("avg_salary"), {'display': 'block'}, "Hide Info"
    else:
        return "", {'display': 'none'}, "Show Info"


# Callback function for graph showing average salary in USD per year from 2020-2024
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

    fig.update_traces(
        marker_color="#1f77b4"
    )

    fig.update_layout(
        xaxis=dict(
            tickmode="array",
            tickvals=filtered_df["work_year"].unique(),
            ticktext=[str(year) for year in filtered_df["work_year"].unique()],
            title_font=dict(
                size=13,
            )
        ),
        yaxis=dict(
            rangemode="tozero",
            title_font=dict(
                size=13,
            )
        ),
        title_font=dict(
            size=13,
        )
    )

    return fig
