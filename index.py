import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from app import app
from layouts import serve_layout
import uiCallbacks
import graphCallbacks

app.layout = serve_layout
# Access underlying flask server object
# Need for gunicorn or any other prod server
application = app.server


if __name__ == '__main__':
    app.run_server(host='0.0.0.0')
