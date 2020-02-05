from app import app
from app import server # Need for heroku procfile
from layouts import serve_layout


app.layout = serve_layout


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True)
