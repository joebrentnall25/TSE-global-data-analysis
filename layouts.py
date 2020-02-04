import dash_core_components as dcc
import dash_html_components as html
import uuid as uuid
import pandas as pd
import plotly.graph_objects as go
from body import serve_body


def serve_layout():
    session_id = str(uuid.uuid4())
    return html.Div(id='root', children=[
        dcc.Store(id='session', storage_type='local'),
        html.Div(session_id, id='session-id'), # hidden id div
        serve_body()
])
