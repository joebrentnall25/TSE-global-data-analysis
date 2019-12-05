import dash_core_components as dcc
import dash_html_components as html
import uuid as uuid
import pandas as pd
import plotly.graph_objects as go
import plotly_express as px
from header import serve_header
from body import serve_body


def serve_layout():
    session_id = str(uuid.uuid4())
    return html.Div(id='root',
    children=[
        html.Div(session_id, id='session-id'), # Show Session ID for debugging purposes
        dcc.Store(id='user-file-store', storage_type='session'), # User file store
        serve_header(),
        serve_body()
])