from flask_login import LoginManager, current_user
from flask_admin import Admin, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView

from settings import create_app

flask_app = create_app()
celery_app = flask_app.extensions["celery"]

login_manager = LoginManager()
login_manager.init_app(flask_app)


class Controler(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self):
        return 'you are not authorized'


admin = Admin(flask_app, name='My App', template_mode='bootstrap3')






