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



@app.callback(Output('chart-output-area', 'children'),
              [Input('create-chart', 'n_clicks')],
              [State('session', 'data'), State('dropdown', 'value')])
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
                figure=fig),
        ]