from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import plotly_express as px
import pandas as pd
from app import app
from helpers import *


@app.callback(Output('choropleth-output-area', 'children'),
              [Input('create-chart', 'n_clicks')],
              [State('session', 'data'), State('x-variable-dropdown', 'value'),
              State('countries', 'value'), State('location-radio', 'value')])
def create_choropleth(n_clicks, data_store, x_variable, countries, location_mode):
    if n_clicks is None or data_store is None:
        raise PreventUpdate
    else:
        try:
            df = pd.read_json(data_store)
            fig = choropleth_chart(df, x_variable, location_mode, countries)
            return [
                dcc.Graph(
                    id='user-choropleth',
                    figure=fig
                )]
        except TypeError:
            return [
                html.H1("Error can not create choropleth from qualative variable.")
            ]


def choropleth_chart(df, x_variable, location_mode, countries):
    fig = go.Figure(data=go.Choropleth(
    locations=df[countries],  # Spatial coordinates
    z=df[x_variable].astype(float),  # Data to be color-coded
    locationmode=location_mode,  # set of locations match entries in `locations`
    colorscale='Reds',
    colorbar_title = 'X variable'
    ))
    return fig
