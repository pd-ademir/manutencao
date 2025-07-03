from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from .models import Usuario
from .extensions import db, migrate, login_manager
from .utils import format_km
from app.checklist import checklist_bp



@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

def create_app():
    app = Flask(__name__)

    # Configurações principais
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'sua-chave-super-secreta'

    # Inicializando extensões
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "main.login"

    # Registrando filtros e funções globais
    from .utils import format_km
    app.jinja_env.filters['format_km'] = format_km

    from .permissoes import tem_permissao
    app.jinja_env.globals['tem_permissao'] = tem_permissao

    # Registrando blueprints
    from .routes import main
    app.register_blueprint(main)
    app.register_blueprint(checklist_bp, url_prefix='/checklist')

    return app


