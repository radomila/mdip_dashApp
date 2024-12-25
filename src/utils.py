"""
Module containing helper functions
"""

import dash_bootstrap_components as dbc


def format_to_k(num):
    """Formats a number to a string with 'k' suffix for thousands.

        Args:
            num (int or float): The number to format.

        Returns:
            str: A formatted string with 'k' if the number is 1000 or greater.
                 Otherwise, the number is returned as a string.
    """
    if num >= 1000:
        formatted = f"{num / 1000:.1f}".rstrip('0').rstrip('.')
        return f"{formatted}k"
    return str(num)


def create_graph_button(id: str):
    """Creates a reusable Dash Bootstrap button for toggling graph information.

        Args:
            id (str): The ID to assign to the button.

        Returns:
            dbc.Button: A Dash Bootstrap Button component with the specified ID.
    """
    return dbc.Button("Show info", id=id, color="primary", className="info-button")


def get_info_text(info_type: str):
    """Returns information text based on the specified type.

    Args:
        info_type (str): The type of information to retrieve. It should be one of
                         the predefined keys in `info_texts`.

    Returns:
        str: The corresponding information text. If the `info_type` does not exist,
             the function returns a fallback default text (in this case, raises a KeyError).
    """
    info_texts = {
        'remote_ratio': (
            'The number of employees working remotely over time from 2020 to 2024, '
            'either in a hybrid model or on-site, based on the remote ratio.'
        ),
        'sankey': (
            'A Sankey diagram showing the relationship between company size and experience level. '
            'The chart illustrates how many employees with a specific experience level work in a company of '
            'a particular size and number of employees.'
        ),
        'avg_salary': (
            'A bar chart displaying the average annual salary from 2020 to 2024 in USD. '
            'The data in the chart can be adjusted based on the selectors defined above the chart.'
        ),
        "avg_salary_choropleth": (
            "The average annual salary in USD worldwide displayed using a choropleth map. "
            "The chart effectively compares average salaries across different countries through a color palette "
            "and the intensity of the colors."
        )
    }

    return info_texts.get(info_type, info_texts[info_type])
