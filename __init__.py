import config as config
from flask_api import FlaskAPI
from my_routes import initialise_routes

app = FlaskAPI(__name__)


def run():
    initialise_routes(app)
    app.run(host=config.HOST, port=config.PORT, debug=True, threaded=False, processes=1)

if __name__ == '__main__':
    run()