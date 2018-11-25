from flask import Flask, render_template
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config
from flask_login import LoginManager

basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()

def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    # apply the blueprints to the app
    from requester import views
    app.register_blueprint(views.bp)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    login_manager = LoginManager()
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @login_manager.unauthorized_handler
    def unauthorized():
        message = {
            'message': "You need to login",
            'error': True
        }
        return render_template('auth/login.html', message=message)


    return app