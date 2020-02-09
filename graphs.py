import plotly.graph_objects as go


GRAPH_TYPES = [
    'Histogram',
    'Overlaid Histogram',
    'Scatter plot',
    'Box plot'
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


def histogram(df, x_variable, colour_scheme):
    fig = go.Figure(data=go.Histogram(x=df[x_variable], histnorm='probability'))
    return fig


def overlaid_histogram(df, x_variable, y_variable, colour_scheme):
    fig = go.Figure(data=go.Histogram())
    return fig


def scatter_plot(df, x_variable, y_variable, colour_scheme):
    pass


def box_plot(df, x_variable, y_variable, colour_scheme):
    pass
