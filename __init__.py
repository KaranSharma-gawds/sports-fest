import config as config
from flask_api import FlaskAPI
from routes import sports

app = FlaskAPI(__name__)


def run():
    app.register_blueprint(sports)
    app.run(host=config.HOST, port=config.PORT, debug=True, threaded=False, processes=1)

if __name__ == '__main__':
    run()