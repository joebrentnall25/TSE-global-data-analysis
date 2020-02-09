from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import dash_table as dt
from dash.exceptions import PreventUpdate
import pandas as pd
from pandas.api.types import is_numeric_dtype
from app import app
from app import DATASETS_PATH
import os
from helpers import parse_file_to_df
from graphs import GRAPH_TYPES
import plotly.express as px


# List of avaliable plotly continuous colourscales
CONTINUOUS_COLOUR_SCALES = px.colors.named_colorscales()
QUALATATIVE_SWATCHES = px.colors.qualitative.swatches()


@app.callback(Output('file-list', 'children'),
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename'), State('file-list', 'children')])
def update_file_storage(contents, filename, curr_children):
    if contents is None:
        raise PreventUpdate

    if not os.path.exists(os.path.join(DATASETS_PATH, filename)):
        try:
            df = parse_file_to_df(contents, filename)
        except Exception:
            return [
                html.H3("Error: Unsupported filetype."),
                dcc.Dropdown(id='files', options=[{'label': filename, 'value':
                                                   filename} for filename in
                                                  os.listdir(DATASETS_PATH)])
            ]
        # Valid file? then save on to FS storage
        df.to_csv(os.path.join(DATASETS_PATH, filename), index=False)
        return [
            html.H3("Upload sucsessful"),
            dcc.Dropdown(id='files', options=[{'label': filename, 'value':
                                               filename}for filename in
                                              os.listdir(DATASETS_PATH)])
        ]
    else:
        return [
            html.H3("Error: filename already exists on disk."),
            dcc.Dropdown(id='files', options=[{'label': filename, 'value':
                                               filename} for filename in
                                              os.listdir(DATASETS_PATH)])
        ]


@app.callback(Output('choropleth-creation-area', 'children'),
              [Input('show-choropleth-opts', 'n_clicks')],
              [State('files', 'value')])
def populate_choropleth_menu(n_clicks, filename):
    if n_clicks is None:
        raise PreventUpdate

    df = pd.read_csv(os.path.join(DATASETS_PATH, filename), index_col=0)
    return [
        # Dropdown for x variable
        # TODO implement UI labeling
        dcc.Dropdown(id='x-variable-dropdown', options=[{'label': i, 'value': i}
                                                        for i in df.columns],
                            value=df.columns[0]),
        dcc.Dropdown(id='y-variable-dropdown', options=[{'label': i, 'value': i}
                                                        for i in df.columns],
                            value=df.columns[0]),
        # Dropdown for indicating where country information is located in df
        dcc.Dropdown(id='countries', options=[{'label': i, 'value': i}
                                                for i in df.columns],
                        value=df.columns[0]),
        # ISO ALPHA-3 or country names?
        dcc.RadioItems(id='location-radio',
            options=[
                {'label': 'ISO-3 (Default)', 'value': 'ISO-3'},
                {'label': 'Country Names', 'value': 'country names'},
            ],
            value='ISO-3'
        ),
        # Select colourscheme from list
        dcc.Dropdown(id='colour-dropdown',
                        options=[{'label': colourscheme, 'value': colourscheme}
                                 for colourscheme in CONTINUOUS_COLOUR_SCALES],
                        value=CONTINUOUS_COLOUR_SCALES[0]),
        # create map
        html.Button('Create Map', id='create-choropleth')
     ]


@app.callback(Output('graph-creation-area', 'children'),
              [Input('create-choropleth', 'n_clicks')],
              [State('files', 'value'), State('x-variable-dropdown', 'value'),
               State('y-variable-dropdown', 'value')])
def populate_graph_menu(n_clicks, filename, x_variable, y_variable):
    if n_clicks is None:
        raise PreventUpdate
    return [
        dcc.Dropdown(id='graph-type',
                     options=[{'label': graph_type, 'value': graph_type}
                              for graph_type in GRAPH_TYPES],
                     value=GRAPH_TYPES[0]),
        html.Button('Create graph', id='create-graph')
    ]



@app.callback(Output('stats', 'children'),
              [Input('create-choropleth', 'n_clicks')],
              [State('x-variable-dropdown', 'value'), State('y-variable-dropdown', 'value'),
               State('files', 'value')])
def update_summary_stats(n_clicks, x_variable, y_variable, filename):
    if n_clicks is None:
        raise PreventUpdate
    # read from FS as usual...
    df = pd.read_csv(os.path.join(DATASETS_PATH, filename))
    # check we're dealing with a quantative variable
    if is_numeric_dtype(df[x_variable]) and is_numeric_dtype(df[y_variable]):
        return [
            html.Ul(id='stats-list', children=[
                html.H3("Summary statistics for x variable: {}".format(x_variable)),
                html.Li("Minimum: {}".format(round(df[x_variable].min()), 2)),
                html.Li("Maximum: {}".format(round(df[x_variable].max()), 2)),
                html.Li("Mean: {}".format(round(df[x_variable].mean()), 2)),
                html.Li("Median: {}".format(round(df[x_variable].median()), 2)),
                html.Li("Standard Deviation: {}".format(round(df[x_variable].std()), 2)),
                html.Li("Variance: {}".format(round(df[x_variable].var()), 2)),
                html.Li("IQR: {}".format(round(df[x_variable].quantile(0.75) - df[x_variable].quantile(0.25)), 2)),

                html.H3("Summary statistics for y variable: {}".format(y_variable)),
                html.Li("Minimum: {}".format(round(df[y_variable].min()), 2)),
                html.Li("Maximum: {}".format(round(df[y_variable].max()), 2)),
                html.Li("Mean: {}".format(round(df[y_variable].mean()), 2)),
                html.Li("Median: {}".format(round(df[y_variable].median()), 2)),
                html.Li("Standard Deviation: {}".format(round(df[y_variable].std()), 2)),
                html.Li("Variance: {}".format(round(df[y_variable].var()), 2)),
                html.Li("IQR: {}".format(round(df[y_variable].quantile(0.75) - df[y_variable].quantile(0.75)), 2))
            ])]
    elif is_numeric_dtype(df[x_variable]):
        return [
            html.Ul(id='stats-list', children=[
                html.H3("Summary statistics for x variable: {}".format(x_variable)),
                html.Li("Minimum: {}".format(round(df[x_variable].min()), 2)),
                html.Li("Maximum: {}".format(round(df[x_variable].max()), 2)),
                html.Li("Mean: {}".format(round(df[x_variable].mean()), 2)),
                html.Li("Median: {}".format(round(df[x_variable].median()), 2)),
                html.Li("Standard Deviation: {}".format(round(df[x_variable].std()), 2)),
                html.Li("Variance: {}".format(round(df[x_variable].var()), 2)),
                html.Li("IQR: {}".format(round(df[x_variable].quantile(0.75) - df[x_variable].quantile(0.25)), 2))
            ])]
    elif is_numeric_dtype(df[y_variable]):
        return [
            html.Ul(id='stats-list', children=[
                html.H3("Summary statistics for y variable: {}".format(y_variable)),
                html.Li("Maximum: {}".format(round(df[y_variable].min()), 2)),
                html.Li("Maximum: {}".format(round(df[y_variable].max()), 2)),
                html.Li("Mean: {}".format(round(df[y_variable].mean()), 2)),
                html.Li("Median: {}".format(round(df[y_variable].median()), 2)),
                html.Li("Standard Deviation: {}".format(round(df[y_variable].std()), 2)),
                html.Li("Variance: {}".format(round(df[y_variable].var()), 2)),
                html.Li("IQR: {}".format(round(df[y_variable].quantile(0.75) - df[y_variable].quantile(0.25)), 2))
            ])]
    else:
        pass
        # TODO Error message or display count etc.


@app.callback(Output('country-data', 'children'),
              [Input('user-choropleth', 'clickData')],
              [State('location-radio', 'value'), State('countries', 'value'), State('files', 'value')])
def display_country_data(click, location_mode, countries, filename):
    # Extract the country code/name from the JSON response
    country_id = click['points'][0]['location']
    df = pd.read_csv(os.path.join(DATASETS_PATH, filename))
    country =  df[df[countries].str.contains(country_id, case=False)]
    return [
        html.H3("Country data for: {}".format(country_id)),
        dt.DataTable(
            id='country-table',
            columns=[{'name': i, 'id': i} for i in country.columns],
            data=country.to_dict('records'),
            fixed_columns={'headers': True, 'data': 1}
        )
    ]
