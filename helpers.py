import base64
import io
import pandas as pd
from dash.exceptions import PreventUpdate
from app import app
import os


#TODO Remove? Local storage no longer needed.
"""@app.callback(Output('session', 'data'),
              [Input('show-file', 'n_clicks')],
              [State('files', 'value')])
def update_local_storage(n_clicks, filename):
    if n_clicks is None:
        raise PreventUpdate
    else:
        df = pd.read_csv(DATASETS_PATH, index_col=0)
        return df.to_json()
"""

def parse_file_to_df(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    if filename.endswith('.csv'):
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
    elif filename.endswith('xls'):
        df = pd.read_excel(io.BytesIO(decoded))
    else:
        raise TypeError
    return df
