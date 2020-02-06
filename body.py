import dash_core_components as dcc
import dash_html_components as html
import uuid as uuid
import pandas as pd
import plotly.graph_objects as go
import os

DATASETS_PATH = './datasets/'


def serve_body():
    return html.Div(id='body', children=[
        html.Div(id='chart-output-area')
    ])
