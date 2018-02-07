import config as config
from flask_api import FlaskAPI
from flask import render_template
from my_routes import initialise_routes
from routes import sports

app = FlaskAPI(__name__)


def run():
    initialise_routes(app)
    app.register_blueprint(sports)
    app.run(host=config.HOST, port=config.PORT, debug=True, threaded=False, processes=1)

@app.route('/', methods=['GET'])
def indexRoute():
    return render_template('index.html')

if __name__ == '__main__':
    run()