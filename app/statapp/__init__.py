from flask_login import LoginManager

from statapp.app import application
from statapp.index import index_bp
from statapp.user import user_bp, User
from statapp.events import events_bp
from statapp.operators import operators_bp
from statapp.feedback import feedback_bp
from statapp.stats import stats_bp

# Login manager
login_manager = LoginManager()
login_manager.init_app(application)
login_manager.login_view = "user.login"

@login_manager.user_loader
def load_user(user_id) -> User:
    user = User.user_setup("id", user_id)
    if user:
        return user
    return None

application.register_blueprint(index_bp, url_prefix="/")
application.register_blueprint(user_bp, url_prefix="/user")
application.register_blueprint(events_bp, url_prefix="/event")
application.register_blueprint(operators_bp, url_prefix="/operator")
application.register_blueprint(feedback_bp, url_prefix="/feedback")
application.register_blueprint(stats_bp, url_prefix="/stats")
