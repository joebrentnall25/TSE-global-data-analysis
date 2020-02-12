import base64
import io
import pandas as pd
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from app import app
import os
import json
from datetime import datetime


#TODO implement user auth & accounts?
@app.callback(Output('session', 'data'),
              [Input('login-success-btn', 'children')],
              [State('username-field', 'value')])
def update_user_session(n_clicks, username):
    if n_clicks is None:
        raise PreventUpdate
    session_info = {"username": username, "login-time": str(datetime.now())}
    return json.loads(session_info)


def parse_file_to_df(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    if filename.endswith('.csv'):
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
    elif filename.endswith('xls'):
        df = pd.read_excel(io.BytesIO(decoded))
    else:
        raise ValueError
    return df
