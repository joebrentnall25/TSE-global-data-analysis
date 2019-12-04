import dash

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__)
server = app.server
# Neeeded for callbacks using dynamicly generated ui componenets
app.config.suppress_callback_exceptions = True
