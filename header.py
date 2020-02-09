import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go


def serve_header():
    return html.Div(id='header', children=[
        html.H1("GDAT - Global Data Analysis Tool")
    ])
