from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager #* Importa login
from .config import Config
from .auth import auth
from .models import UserModel

login_manager = LoginManager()
login_manager.login_view = 'auth.login' #* asigna app

def create_app():
    """Created app flask in the app folder file __init__

    Returns:
        class flask: application
    """
    app = Flask(__name__)
    bootstrap = Bootstrap(app)
    app.config.from_object(Config)
    login_manager.init_app(app) #* envio la app al login
    app.register_blueprint(auth) #! aqui defines que se va al login siempre
    return app

@login_manager.user_loader
def load_user(username):
    return UserModel.query(username)