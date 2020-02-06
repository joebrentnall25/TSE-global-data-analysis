from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
from dash.exceptions import PreventUpdate
import pandas as pd
import os
from pathlib import Path
from app import app
from helpers import parse_file_to_df


DATASETS_PATH = './datasets'


@app.callback(Output('file-list', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename')])
def update_file_list(contents, filename):
    if contents is None:
        raise PreventUpdate
    else:
        df = parse_file_to_df(contents, filename)
        my_file = Path(os.path.join(DATASETS_PATH, filename))
        if not my_file.is_file():
            df.to_csv(my_file)
            return [
                dcc.Dropdown(id='files',
                             options=[{'label': filename, 'value': filename}
                                      for filename in os.listdir(DATASETS_PATH)], value=None)
            ]
        else:
            return [
                html.H1("Error: File already exists on disk. Please change filename."),
                dcc.Dropdown(id='files',
                             options=[{'label': filename, 'value': filename}
                                      for filename in os.listdir(DATASETS_PATH)], value=None)
            ]


@app.callback(Output('chart-creation-area', 'children'),
              [Input('show-file', 'n_clicks')],
              [State('files', 'value')])
def populate_chart_menu(n_clicks, filename):
    if filename is None or n_clicks is None:
        raise PreventUpdate
    else:
        df = pd.read_csv(os.path.join(DATASETS_PATH, filename))
        return [
            dcc.Dropdown(id='dropdown', options=[{'label': i, 'value': i}
                                                 for i in df.columns], value=df.columns[0]),
            dcc.RadioItems(id='location-radio',
                options=[
                    {'label': 'ISO-3', 'value': 'ISO-3'},
                    {'label': 'Country Names', 'value': 'Country Names'},
                ],
             value='ISO-3'
            ),
            dcc.Dropdown(id='country', options=[{'label': i, 'value': i}
                                                for i in df.columns], value=df.columns[0]),
            html.Button('Create choropleth', id='create-chart')
        ]
