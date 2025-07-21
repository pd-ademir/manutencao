import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf import CSRFProtect

from .models import Usuario
from .extensions import db, migrate, login_manager
from .utils import format_km
from app.checklist import checklist_bp

csrf = CSRFProtect()

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    csrf.init_app(app)

    # Diretório base do projeto
    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_pneus_path = os.path.join(base_dir, '..', 'instance', 'pneus.sqlite3')

    # Configurações principais
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'  # banco principal
    app.config['SQLALCHEMY_BINDS'] = {
        'pneus': f'sqlite:///{os.path.abspath(db_pneus_path)}'  # banco de pneus
    }
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'sua-chave-super-secreta'

    # Inicializando extensões
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "main.login"
    csrf.init_app(app)

    # Registrando filtros e funções globais
    app.jinja_env.filters['format_km'] = format_km

    from .permissoes import tem_permissao
    app.jinja_env.globals['tem_permissao'] = tem_permissao

    # Registrando blueprints
    from .routes import main
    app.register_blueprint(main)
    app.register_blueprint(checklist_bp, url_prefix='/checklist')

    return app
