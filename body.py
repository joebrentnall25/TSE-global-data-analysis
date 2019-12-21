
import dash_core_components as dcc
import dash_html_components as html
import uuid as uuid
import pandas as pd 
import plotly.graph_objects as go 

def serve_body():
    return html.Div([
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
        html.Button('Populate menu', id='show-file'),
        html.Div(id='chart-creation-area'),
        html.Div(id='chart-output-area')
    ])