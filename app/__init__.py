import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from urllib.parse import quote_plus

from .models import Usuario
from .extensions import db, migrate, login_manager
from .utils import format_km
from .checklist import checklist_bp

csrf = CSRFProtect()

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'sua-chave-super-secreta')

    # Configurações padrões (servidor cloud)
    senha = 'Senhadobanco2025#'
    senha_encoded = quote_plus(senha)  # codifica '#'
    cloud_host = '34.39.255.52'
    user = 'Ornilio_neto'

    # Configurações locais
    local_host = 'localhost'
    local_user = 'root'           # ajuste conforme seu local
    local_senha = ''              # ajuste conforme seu local
    local_senha_encoded = quote_plus(local_senha)

    # Verifica se está rodando local ou no cloud
    ambiente = os.environ.get('AMBIENTE', 'cloud')  # use 'local' para rodar local

    if ambiente == 'local':
        host = local_host
        user = local_user
        senha_encoded = local_senha_encoded
    else:
        host = cloud_host

    # Monta URIs
    db_uri = os.environ.get('DATABASE_URL_MANUTENCAO') or f'mysql+pymysql://{user}:{senha_encoded}@{host}/manutencao'
    pneus_uri = os.environ.get('DATABASE_URL_PNEUS') or f'mysql+pymysql://{user}:{senha_encoded}@{host}/pneus'
    checklist_uri = os.environ.get('DATABASE_URL_CHECKLIST') or f'mysql+pymysql://{user}:{senha_encoded}@{host}/checklist'

    print(f"Ambiente: {ambiente}")
    print("Database URI usada:", db_uri)

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_BINDS'] = {
        'pneus': pneus_uri,
        'checklist': checklist_uri
    }

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
