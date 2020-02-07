from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import dash_table as dt
from dash.exceptions import PreventUpdate
import pandas as pd
import numpy as np
import json
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
                                      for filename in os.listdir(DATASETS_PATH)],
                             value=None)
            ]
        else:
            return [
                html.H1("Error: File already exists on disk. Please change filename."),
                dcc.Dropdown(id='files',
                             options=[{'label': filename, 'value': filename}
                                      for filename in os.listdir(DATASETS_PATH)],
                             value=None)
            ]


@app.callback(Output('choropleth-creation-area', 'children'),
              [Input('show-choropleth-opts', 'n_clicks')],
              [State('files', 'value')])
def populate_choropleth_menu(n_clicks, filename):
    if filename is None or n_clicks is None:
        raise PreventUpdate
    else:
        df = pd.read_csv(os.path.join(DATASETS_PATH, filename))
        return [
            dcc.Dropdown(id='x-variable-dropdown', options=[{'label': i, 'value': i}
                                                 for i in df.columns],
                         value=df.columns[0]),
            # TODO add color radio code
            dcc.RadioItems(id='color-radio'),
            dcc.Dropdown(id='countries', options=[{'label': i, 'value': i}
                                                for i in df.columns],
                         value=df.columns[0]),
            dcc.RadioItems(id='location-radio',
                options=[
                    {'label': 'ISO-3', 'value': 'ISO-3'},
                    {'label': 'Country Names', 'value': 'Country Names'},
                ],
             value='ISO-3'
            ),
            html.Button('Create choropleth', id='create-choropleth')
        ]


@app.callback(Output('stats', 'children'),
              [Input('create-choropleth', 'n_clicks')],
              [State('session', 'data'), State('x-variable-dropdown', 'value')])
def update_summary_stats(n_clicks, data_store, x_variable):
    if n_clicks is None or data_store is None:
        raise PreventUpdate
    else:
        # read data frame from session store
        df = pd.read_json(data_store)
        # check if quantative or categorical variable
        if df[x_variable].dtype == np.float64 or df[x_variable].dtype == np.int64:
            return [
                html.Ul(id='stats-list', children=[
                    html.H3("Summary statistics: "),
                    html.Li("Mean: {}".format(round(df[x_variable].mean()), 2)),
                    html.Li("Median: {}".format(round(df[x_variable].median()), 2)),
                    html.Li("Standard Deviation: {}".format(round(df[x_variable].std()), 2)),
                    html.Li("Variance: {}".format(round(df[x_variable].var()), 2)),
                    html.Li("IQR: {}".format(round(df[x_variable].quantile(0.75) - df[x_variable].quantile(0.25)), 2))
                ])]
        else:
            pass
            # TODO implement categorical summary stats


@app.callback(Output('country-data', 'children'),
              [Input('user-choropleth', 'clickData')],
              [State('session', 'data'), State('location-radio', 'value')])
def display_country_data(click, data_store, location_mode):
    # Extract the country code/name from the JSON response
    country_name = click['points'][0]['location']
    df = pd.read_json(data_store)
    # location mode determines the col we match in
    if location_mode == 'ISO-3':
        country = df[df['Country Code'].str.contains(country_name, case=False)]
    else:
        country = df[df['Country Names'].str.contains(country_name, case=False)]

    return dt.DataTable(
        id='country-table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=country.to_dict('records'),
        fixed_columns={'headers': True, 'data': 1}
    )
