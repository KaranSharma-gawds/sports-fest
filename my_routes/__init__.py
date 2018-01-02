from flask import Blueprint
from flask_login import LoginManager

login_manager = LoginManager()
institute = Blueprint('institute', __name__)
login = Blueprint('login', __name)
from . import institution

def initialise_routes(app):
    login_manager.init_app(app)
    app.register_blueprint(institute, url_prefix='/institute')
    app.register_blueprint(login, url_prefix='/user')
