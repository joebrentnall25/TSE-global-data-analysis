import dash_core_components as dcc
import dash_html_components as html
import uuid as uuid
import pandas as pd
import plotly.graph_objects as go
import plotly_express as px

# Starting header for the application goes here

def serve_header():
    return html.H1(id='test', children="Hello, World!")