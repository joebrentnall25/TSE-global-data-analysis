import dash_core_components as dcc
import dash_html_components as html
import uuid as uuid
import pandas as pd
import plotly.graph_objects as go
import plotly_express as px


def serve_layout():
    session_id = str(uuid.uuid4()) # Generate a random session ID for each user -> in case flask cache is needed
    return html.Div(id='root',
    children=[
        html.Div(session_id, id='session-id', style={'display': 'none'}), # hidden sess id div  
        dcc.Store(id='user-file-store', storage_type='session'), # User file store
        html.H1("Hello, World!")
])