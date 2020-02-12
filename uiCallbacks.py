from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import dash_table as dt
from dash.exceptions import PreventUpdate
import pandas as pd
from pandas.api.types import is_numeric_dtype
from app import app, DATASETS_PATH
import os
from helpers import parse_file_to_df
from graphs import CONTINUOUS_COLOUR_SCALES




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


@app.callback(Output('dashboard-creation-area', 'children'),
              [Input('show-dashboard-opts', 'n_clicks')],
              [State('files', 'value')])
def populate_dashboard_menu(n_clicks, filename):
    if n_clicks is None:
        raise PreventUpdate

    df = pd.read_csv(os.path.join(DATASETS_PATH, filename), index_col=0)
    return [
        # TODO implement UI labeling
        dcc.Dropdown(id='x-variable-dropdown', options=[{'label': i, 'value': i}
                                                        for i in df.columns],
                            placeholder='Select x variable'),
        dcc.Dropdown(id='y-variable-dropdown', options=[{'label': i, 'value': i}
                                                        for i in df.columns],
                            placeholder='Select y variable (optional)'),
        # Dropdown for indicating where country information is located in df
        dcc.Dropdown(id='countries', options=[{'label': i, 'value': i}
                                                for i in df.columns],
                        placeholder='Select countries column'),
        # ISO ALPHA-3 or country names?
        dcc.RadioItems(id='location-radio',
            options=[
                {'label': 'ISO-3 (Default)', 'value': 'ISO-3'},
                {'label': 'Country Names', 'value': 'Country Names'},
            ],
            value='ISO-3'
        ),
        # Select colourscheme from list
        dcc.Dropdown(id='colour-dropdown',
                        options=[{'label': colourscheme, 'value': colourscheme}
                                 for colourscheme in CONTINUOUS_COLOUR_SCALES],
                        value=CONTINUOUS_COLOUR_SCALES[0]),
        # create dashboard
        html.Button('Create Dashboard', id='create-dashboard')
     ]


@app.callback(Output('stats', 'children'),
              [Input('create-dashboard', 'n_clicks')],
              [State('x-variable-dropdown', 'value'), State('y-variable-dropdown', 'value'),
               State('files', 'value')])
def update_summary_stats(n_clicks, x_variable, y_variable, filename):
    if n_clicks is None:
        raise PreventUpdate

    #read from FS as usual...
    df = pd.read_csv(os.path.join(DATASETS_PATH, filename))
    # check we're dealing with two quantatative variables
    if is_numeric_dtype(df[x_variable]) and not y_variable == None and is_numeric_dtype(df[y_variable]):
        return [
            html.Ul(id='stats-list', children=[
                html.H6("Summary statistics for x variable: {}".format(x_variable)),
                html.Li("Minimum: {:0.2f}".format(df[x_variable].min())),
                html.Li("Maximum: {:0.2f}".format(df[x_variable].max())),
                html.Li("Mean: {:0.2f}".format(df[x_variable].mean())),
                html.Li("Median: {:0.2f}".format(df[x_variable].median())),
                html.Li("Standard Deviation: {:0.2f}".format(df[x_variable].std())),
                html.Li("Variance: {:0.2f}".format(df[x_variable].var())),
                html.Li("IQR: {:0.2f}".format(df[x_variable].quantile(0.75) - df[x_variable].quantile(0.25))),

                html.H6("Summary statistics for y variable: {}".format(y_variable)),
                html.Li("Minimum: {:0.2f}".format(df[y_variable].min())),
                html.Li("Maximum: {:0.2f}".format(df[y_variable].max())),
                html.Li("Mean: {:0.2f}".format(df[y_variable].mean())),
                html.Li("Median: {:0.2f}".format(df[y_variable].median())),
                html.Li("Standard Deviation: {:0.2f}".format(df[y_variable].std())),
                html.Li("Variance: {:0.2f}".format(df[y_variable].var())),
                html.Li("IQR: {:0.2f}".format(df[y_variable].quantile(0.75) - df[y_variable].quantile(0.25)))
            ])]
    elif is_numeric_dtype(df[x_variable]):
        return [
            html.Ul(id='stats-list', children=[
                html.H6("Summary statistics for x variable: {}".format(x_variable)),
                html.Li("Minimum: {:0.2f}".format(df[x_variable].min())),
                html.Li("Maximum: {:0.2f}".format(df[x_variable].max())),
                html.Li("Mean: {:0.2f}".format(df[x_variable].mean())),
                html.Li("Median: {:0.2f}".format(df[x_variable].median())),
                html.Li("Standard Deviation: {:0.2f}".format(df[x_variable].std())),
                html.Li("Variance: {:0.2f}".format(df[x_variable].var())),
                html.Li("IQR: {:0.2f}".format(df[x_variable].quantile(0.75) - df[x_variable].quantile(0.25)))
            ])]
    elif not y_variable == None and is_numeric_dtype(df[y_variable]):
        return [
            html.Ul(id='stats-list', children=[
                html.H6("Summary statistics for y variable: {}".format(y_variable)),
                html.Li("Maximum: {:0.2f}".format(df[y_variable].min())),
                html.Li("Maximum: {:0.2f}".format(df[y_variable].max())),
                html.Li("Mean: {:0.2f}".format(df[y_variable].mean())),
                html.Li("Median: {:0.2f}".format(df[y_variable].median())),
                html.Li("Standard Deviation: {:0.2f}".format(df[y_variable].std())),
                html.Li("Variance: {:0.2f}".format(df[y_variable].var())),
                html.Li("IQR: {:0.2f}".format(df[y_variable].quantile(0.75) - df[y_variable].quantile(0.25)))
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
