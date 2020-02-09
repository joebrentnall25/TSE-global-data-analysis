import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
from header import serve_header
from body import serve_choropleth
from body import serve_graphs_data
from sidebar import serve_sidebar


# Serve page layout
def serve_layout():
    return html.Div(id='root', children=[
        dcc.Store(id='session', storage_type='local'),
        serve_header(),
        html.Span(id='main-span', children=[
            serve_sidebar(),
            serve_choropleth(),
        ]),
        serve_graphs_data()
    ])
