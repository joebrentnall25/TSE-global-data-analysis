from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import plotly_express as px
import dash_table
import pandas as pd
from app import app
from helpers import *



@app.callback(Output('session', 'data'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename')])
def update_storage(contents, filename):
    if contents is None:
        raise PreventUpdate
    else:
        df = parse_file_to_df(contents, filename)
        return df.to_json()


@app.callback(Output('chart-creation-area', 'children'),
              [Input('show-file', 'n_clicks')],
              [State('session', 'data')])
def populate_chart_menu(n_clicks, data_store):
    if data_store is None or n_clicks is None:
        raise PreventUpdate
    else:
        df = pd.read_json(data_store)
        return [
            dcc.Dropdown(id='dropdown', options=[{'label': i, 'value': i } for i in df.columns], value=df.columns[0]),
            html.Button('Create chart', id='create-chart')
        ]
