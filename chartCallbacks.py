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
              [State('session', 'data'), State('dropdown', 'value'), 
              State('country', 'value'), State('location-radio', 'value')])
def create_choropleth(n_clicks, data_store, variable, country, location_mode):
    if n_clicks is None or data_store is None:
        raise PreventUpdate
    else:
        df = pd.read_json(data_store)
        fig = go.Figure(data=go.Choropleth(
        locations=df[country], # Spatial coordinates
        z = df[variable].astype(float), # Data to be color-coded
        locationmode = location_mode, # set of locations match entries in `locations`
        colorscale = 'Reds',
        colorbar_title = variable
        ))
        return [
            dcc.Graph(
                id='user-choropleth',
                figure=fig),
        ]