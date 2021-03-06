import config as config
from flask_api import FlaskAPI
from flask import render_template
from my_routes import initialise_routes
from flask_cors import CORS
from routes import sports


app = FlaskAPI(__name__)
CORS(app)

def run():
    initialise_routes(app)
    app.register_blueprint(sports)
    app.config.update(SECRET_KEY='dilrubajanemangaanddekejachutmarwakeja')
    app.run(host=config.HOST, port=config.PORT, debug=True, threaded=False, processes=1)

@app.route('/', methods=['GET'])
def indexRoute():
    return render_template('index.html')

if __name__ == '__main__':
    run()