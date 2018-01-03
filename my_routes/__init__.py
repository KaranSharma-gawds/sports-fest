from flask import Blueprint
from flask_login import LoginManager

login_manager = LoginManager()
institute = Blueprint('institute', __name__)
login = Blueprint('login', __name__)
people = Blueprint('people', __name__)
sports_fest = Blueprint('sports_fest', __name__)
events = Blueprint('events', __name__)

from . import institution
from . import user
from . import person
from . import fest
from . import event
def initialise_routes(app):
    login_manager.init_app(app)
    app.register_blueprint(institute, url_prefix='/institute')
    app.register_blueprint(login, url_prefix='/user')
    app.register_blueprint(people, url_prefix='/people')
    app.register_blueprint(sports_fest, url_prefix='/fest')
    app.register_blueprint(events)
