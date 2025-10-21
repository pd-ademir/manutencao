from flask import Flask
from flask_login import LoginManager
from config import Config
from datetime import timedelta

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)

    login_manager.init_app(app)

    @app.route('/')
    def index():
        return 'Aplicação Flask rodando no Google Cloud Run!'

    return app
