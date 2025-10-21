from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from .config import Config
from datetime import timedelta

# 1. Inicializa extensões sem app
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()

# 2. Configura o Flask-Login
login_manager.login_view = 'main.login'
login_manager.login_message = "Por favor, faça login para acessar."
login_manager.login_message_category = "warning"

def create_app(config_class=Config):
    """Application Factory: Cria e configura a instância do app Flask."""
    app = Flask(__name__)

    # 3. Carrega configurações
    app.config.from_object(config_class)
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=8)

    # 4. Conecta extensões ao app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    # 5. Importa e registra o Blueprint com as rotas
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # 6. Define como o Flask-Login carrega um usuário
    from .models import Usuario
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # 7. Retorna o app pronto
    return app
