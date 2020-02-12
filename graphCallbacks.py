from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import pandas as pd
from pandas.api.types import is_string_dtype, is_numeric_dtype
from app import app, DATASETS_PATH
import os
from graphs import choropleth, histogram, GRAPH_TYPES
import re


# Callback to create the choropleth from user dataset
@app.callback(Output('choropleth-output-area', 'children'),
              [Input('create-dashboard', 'n_clicks')],
              [State('x-variable-dropdown', 'value'), State('countries', 'value'),
               State('location-radio', 'value'), State('files', 'value'),
               State('colour-dropdown', 'value')])
def create_choropleth(n_clicks,
                      x_variable,
                      countries,
                      location_mode,
                      filename,
                      colour_scheme):
    if n_clicks is None:
        raise PreventUpdate

    df = pd.read_csv(os.path.join(DATASETS_PATH, filename))
    """ We have 3 edge cases to handle with user input.
    1) Column provided as the x variable is not a numeric datatype
    2) column provided for country information is not a string datatype
    3) If ISO-3 location mode is selected, contents of the countries column fail to match regex
    """
    if not is_numeric_dtype(df[x_variable]):
        return [
            html.H3("Error: Can not create choropleth from non-quantative variable.")
        ]
    if not is_string_dtype(df[countries]):
        return[
            html.H3("Error: Locations for plotting must be a string type.")
        ]
    if location_mode == 'ISO-3':
        ISO_3 = re.compile('^[A-Z]{3}$')
        for country in df[countries]:
            if not ISO_3.match(country):
                return [
                    html.H3("Error: Entry {} in countries column does not comply with ISO Alpha-3".format(country))
                ]

    fig = choropleth(df, x_variable, location_mode, countries, colour_scheme)

    """fig.update_layout(
        autosize=True,
        margin=go.layout.Margin(
            l=10, r=10, b=25, t=25,
            pad=2
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title=x_variable,
        title_x=0.5,
        font=dict(
            family="Courier New, monospace",
            size=12,
            color="#ffffff"
        )
    )"""
    return dcc.Graph(id='user-choropleth', figure=fig)


@app.callback(Output('graph-creation-area', 'children'),
                  [Input('create-dashboard', 'n_clicks')],
                  [State('files', 'value'), State('x-variable-dropdown', 'value'),
                  State('y-variable-dropdown', 'value')])
def populate_graph_menu(n_clicks, filename, x_variable, y_variable):
    if n_clicks is None:
        raise PreventUpdate
    df = pd.read_csv(os.path.join(DATASETS_PATH, filename))
    fig = histogram(df, x_variable, 'ex')
    return [
            dcc.Dropdown(id='graph-type',
                     options=[{'label': graph_type, 'value': graph_type}
                                for graph_type in GRAPH_TYPES],
                    value=GRAPH_TYPES[0]),
            html.Button('Create graph', id='create-graph'),
            html.Div(id='graph-output-area', children=[
                dcc.Graph(id='user-graph', figure=fig)
        ])]


@app.callback(Output('graph-output-area', 'children'),
             [Input('create-graph', 'n_clicks')],
             [State('graph-type', 'value'),
            State('x-variable-dropdown', 'value'), State('y-variable-dropdown', 'value'),
            State('files', 'value'), State('colour-dropdown', 'value')])
def create_graph(n_clicks, graph_type, x_variable, y_variable, filename, colour_scheme):
    if n_clicks is None:
        raise PreventUpdate

    df = pd.read_csv(os.path.join(DATASETS_PATH, filename))

    if graph_type == 'Histogram':
        fig = histogram(df, x_variable, colour_scheme)
        return [
            dcc.Graph(id='user-graph', figure=fig)
        ]
