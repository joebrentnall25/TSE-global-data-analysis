import dash_core_components as dcc
import dash_html_components as html
import os


DATASETS_PATH = './datasets/'


# return sidebar for choropleth creation + summary stats
def serve_sidebar():
    return html.Div(id='side-bar', children=[
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files to upload')
            ]),
            # Allow multiple files to be uploaded
            multiple=True
        ),
        # List all .csv files hosted on the server
        html.Div(id='file-list',
                 children=[dcc.Dropdown(id='files',
                                        options=[{'label': filename,
                                                  'value': filename}
                                                             for filename in
                                                             os.listdir(DATASETS_PATH)], value=None)]),
        html.Button('Populate menu', id='show-choropleth-opts'),
        html.Div(id='choropleth-creation-area')
    ])
