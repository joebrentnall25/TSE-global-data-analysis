import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from app import app
from app import server # Need for heroku procfile
from layouts import serve_layout
import uiCallbacks
import chartCallbacks
from flask_caching import Cache


app.layout = serve_layout


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True)
