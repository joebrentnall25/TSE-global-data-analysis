import dash_core_components as dcc
import dash_html_components as html


def serve_choropleth():
    return html.Div(id='body', children=[
        html.Div(id='choropleth-output-area'),
    ])


def serve_charts_data():
    return html.Div(id='charts-data', children=[
        html.Div(id='charts'),
        html.Div(id='stats'),
        html.Div(id='country-data')
    ])


# TODO add data table div?
def serve_data_table():
    pass
