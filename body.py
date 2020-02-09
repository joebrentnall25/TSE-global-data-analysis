import dash_core_components as dcc
import dash_html_components as html
# Layout generation functions for main body



def serve_choropleth():
    return html.Div(id='body', children=[
        html.Div(id='choropleth-output-area'),
    ])


def serve_graphs_data():
    return html.Div(id='graphs-stats-container', children=[
        html.Div(id='graphs', children=[
            html.Div(id='graph-creation-area'),
            html.Div(id='graph-output-area')
        ]),
        html.Div(id='stats'),
        html.Div(id='country-data')
    ])
