import dash_core_components as dcc
import dash_html_components as html
import uuid as uuid
import pandas as pd
import plotly.graph_objects as go
from header import serve_header
from body import serve_body
from sidebar import serve_sidebar


def serve_layout():
#    session_id = uuid()
    return html.Div(id='root', children=[
        dcc.Store(id='session', storage_type='local'),
        serve_header(),
        html.Span(id='main-span', children=[
            serve_sidebar(),
            serve_body()
        ])
])