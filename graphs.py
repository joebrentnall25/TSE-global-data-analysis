import plotly.graph_objs as go
import plotly_express as px
import pandas as pd


# Lists of avaliable plotly continuous colourscales etc.
CONTINUOUS_COLOUR_SCALES = px.colors.named_colorscales()
QUALATATIVE_SWATCHES = px.colors.qualitative.swatches()


GRAPH_TYPES = [
    'Histogram',
    'Overlaid Histogram',
    'Box plot',
    'Scatter plot'
]


def choropleth(df, x_variable, location_mode, countries, colour_scheme):
    fig = go.Figure(data=go.Choropleth(
        locations=df[countries],  # Spatial coordinates
        z=df[x_variable].astype(float),  # Data to be color-coded
        locationmode=location_mode,  # set of locations match entries in `locations`
        colorscale=colour_scheme,
        text=df[countries],
    ))
    return fig


# TODO finish implementation of histogram fig
def histogram(df, x_variable, colour_scheme):
    fig = go.Figure(data=go.Histogram(
        x=df[x_variable],
        )
    )
    return fig


def overlaid_histogram(df, x1_variable, x2_variable, colour_scheme):
    pass


def scatter_plot(df, x_variable, y_variable, colour_scheme):
    pass


def box_plot(df, x_variable, colour_scheme):
    pass
