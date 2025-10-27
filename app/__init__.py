import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from urllib.parse import quote_plus
from dotenv import load_dotenv

from .models import Usuario
from .extensions import db, migrate, login_manager
from .utils import format_km
from .checklist import checklist_bp

# Carrega variáveis do .env (se existir)
load_dotenv()

csrf = CSRFProtect()

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'sua-chave-super-secreta')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-chave-secreta-padrao')

    # Verifica se está rodando local ou no cloud
    ambiente = os.environ.get('AMBIENTE', 'cloud')  # padrão é 'cloud'

    if ambiente == 'local':
        user = os.environ.get('LOCAL_DB_USER', 'root')
        senha = os.environ.get('LOCAL_DB_PASSWORD', '')
        host = os.environ.get('LOCAL_DB_HOST', 'localhost')
    else:
        user = os.environ.get('CLOUD_DB_USER', 'Ornilio_neto')
        senha = os.environ.get('CLOUD_DB_PASSWORD', 'Senhadobanco2025#')
        host = os.environ.get('CLOUD_DB_HOST', '34.39.255.52')

    senha_encoded = quote_plus(senha)

    # Monta URIs
    db_uri = f'mysql+pymysql://{user}:{senha_encoded}@{host}/manutencao'
    pneus_uri = f'mysql+pymysql://{user}:{senha_encoded}@{host}/pneus'
    checklist_uri = f'mysql+pymysql://{user}:{senha_encoded}@{host}/checklist'

    print(f"Ambiente: {ambiente}")
    print("Database URI usada:", db_uri)

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_BINDS'] = {
        'pneus': pneus_uri,
        'checklist': checklist_uri
    }

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Pooling para performance
    app.config['SQLALCHEMY_POOL_SIZE'] = 10
    app.config['SQLALCHEMY_POOL_TIMEOUT'] = 30
    app.config['SQLALCHEMY_POOL_RECYCLE'] = 1800
    app.config['SQLALCHEMY_MAX_OVERFLOW'] = 20

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "main.login"
    csrf.init_app(app)

    app.jinja_env.filters['format_km'] = format_km

    from .permissoes import tem_permissao
    app.jinja_env.globals['tem_permissao'] = tem_permissao

    from .routes import main
    app.register_blueprint(main)
    app.register_blueprint(checklist_bp, url_prefix='/checklist')

    return app
