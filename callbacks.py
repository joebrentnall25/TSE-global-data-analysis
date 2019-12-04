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


# checks for "None"/null are required as callbacks will fire on page load
@app.callback(Output('output-data-upload', 'children'),
              [Input('show-file', 'n_clicks')],
              [State('session', 'data')])
def show_data(n_clicks, data_store):
    if n_clicks is None or data_store is None:
        raise PreventUpdate
    else:
        df = pd.read_json(data_store)
        return dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{'name': i, 'id': i} for i in df.columns])


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
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename')])
def update_chart_options(contents, filename):
    if contents is None:
        raise PreventUpdate
    else:
        df = parse_file_to_df(contents, filename)
        # Return as list of child elements
        return [
            html.H1("Chart creation options"),
            dcc.Dropdown(id='chart-dropdown',
        options=[{'label':i, 'value': i} for i in df.columns],
        value=df.columns[0]
        )]



@app.callback(Output('chart-output-area', 'children'),
              [Input('create-chart', 'n_clicks')],
              [State('session', 'data'), State('chart-dropdown', 'value')])
def create_chart(n_clicks, data_store, value):
    if n_clicks is None or data_store is None:
        raise PreventUpdate
    else:
        df = pd.read_json(data_store)
        data = df[value]
        fig = px.histogram(data, x=value, title='Histogram', labels={value: value}, opacity=0.8)
        return [
            dcc.Graph(
        id='user-histogram',
        figure=fig
    ),]
