import dash_core_components as dcc
import dash_html_components as html
import os
from app import DATASETS_PATH


# return sidebar for choropleth creation
def serve_sidebar():
    return html.Div(id='sidebar', children=[
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files to upload')
            ]),
            # Do NOT Allow SIMULTANEOUS uploads by the user
            multiple=False
        ),
        # List all .csv or .xls files hosted on the server
        html.Div(id='file-list',
                 children=[dcc.Dropdown(id='files',
                                        options=[{'label': filename,
                                                  'value': filename}
                                                             for filename in
                                                             os.listdir(DATASETS_PATH)], value='./proper.csv')]),
        html.Button('Populate menu', id='show-choropleth-opts'),
        html.Div(id='choropleth-creation-area')
    ])
