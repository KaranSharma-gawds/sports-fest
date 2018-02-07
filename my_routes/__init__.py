from flask import Blueprint
from flask_login import LoginManager

login_manager = LoginManager()
institute = Blueprint('institute', __name__)
login = Blueprint('login', __name__)
people = Blueprint('people', __name__)
sports_fest = Blueprint('sports_fest', __name__)
events = Blueprint('events', __name__)
event_result = Blueprint('event_result', __name__)
upload_route = Blueprint('upload_route', __name__)

from . import institution
from . import user
from . import person
from . import fest
from . import event
from . import result
from . import upload

def initialise_routes(app):
    login_manager.init_app(app)
    app.register_blueprint(institute, url_prefix='/api/institute')
    app.register_blueprint(login, url_prefix='/api/user')
    app.register_blueprint(people, url_prefix='/api/people')
    app.register_blueprint(sports_fest, url_prefix='/api/fest')
    app.register_blueprint(events, url_prefix='/api/event')
    app.register_blueprint(event_result, url_prefix='/api/result')
    app.register_blueprint(upload_route, url_prefix='/api/upload')
