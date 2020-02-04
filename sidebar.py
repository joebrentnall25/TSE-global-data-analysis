import dash_core_components as dcc
import dash_html_components as html
import uuid as uuid
import pandas as pd
import plotly.graph_objects as go
import os


DATASETS_PATH = './datasets/'

def serve_sidebar():
    return html.Div(id='side-bar', children=[
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
        html.Div(id='file-list',
                 children=[dcc.Dropdown(id='files', options=[{'label': filename, 'value': filename}
                                                             for filename in os.listdir(DATASETS_PATH)], value=None)]),
        html.Button('Populate menu', id='show-file'),
    ])