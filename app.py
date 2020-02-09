import dash

app = dash.Dash(__name__)
# Neeeded for callbacks using dynamicly generated ui componenets
app.config.suppress_callback_exceptions = True

# relative path for dataset directory
DATASETS_PATH = './datasets/'
