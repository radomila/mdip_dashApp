"""
Module containing helper functions
"""

import dash_bootstrap_components as dbc


def format_to_k(num):
    if num >= 1000:
        formatted = f"{num / 1000:.1f}".rstrip('0').rstrip('.')
        return f"{formatted}k"
    return str(num)


def create_graph_button(id: str):
    return dbc.Button("Show info", id=id, color="primary", className="info-button")


def get_info_text(info_type: str):
    """
    Funkce pro vrácení textu podle typu informace.

    :param info_type: Typ informace, podle kterého se vybere text.
    :return: Text, který odpovídá danému typu.
    """
    info_texts = {
        'remote_ratio': 'The number of employees working remotely over time from 2020 to 2024, either in a hybrid model or on-site, based on the remote ratio.',
        'sankey': 'A Sankey diagram showing the relationship between company size and experience level. The chart illustrates how many employees with a specific experience level work in a company of a particular size and number of employees.',
        'avg_salary': 'A bar chart displaying the average annual salary from 2020 to 2024 in USD. The data in the chart can be adjusted based on the selectors defined above the chart.',
        "avg_salary_choropleth": "The average annual salary in USD worldwide displayed using a choropleth map. The chart effectively compares average salaries across different countries through a color palette and the intensity of the colors."
    }

    return info_texts.get(info_type, info_texts[info_type])
