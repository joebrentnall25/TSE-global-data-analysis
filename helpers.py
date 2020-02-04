import base64
import io
import pandas as pd
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from app import app


@app.callback(Output('session', 'data'),
              [Input('show-file', 'n_clicks')],
              [State('files', 'value')])
def update_local_storage(n_clicks, filename):
    if n_clicks is None:
        raise PreventUpdate
    else:
        df = pd.read_csv('./datasets/'+filename, index_col=0)
        return df.to_json()


def parse_file_to_df(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
    return df
