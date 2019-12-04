import dash_core_components as dcc
import dash_html_components as html
import uuid as uuid
import pandas as pd
import plotly.graph_objects as go

def serve_layout():
    session_id = str(uuid.uuid4())
    return html.Div([
        html.Div(session_id, id='session-id'), # hidden id div
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            # Allow multiple files to be uploaded
            multiple=False
        ),
        dcc.Store(id='session', storage_type='session'),
        html.Button('show-file', id='show-file'),
        html.Div(id='output-data-upload'),
        html.Div(id='chart-creation-area'),
        html.Button('Create chart', id='create-chart'),
        html.Div(id='chart-output-area')
])
