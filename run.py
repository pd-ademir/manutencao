from app import create_app
from flask_login import LoginManager
from datetime import timedelta

# Cria a instância do app Flask
app = create_app()

# Configura o tempo de sessão
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)

# Configura o LoginManager (se ainda não estiver dentro do create_app)
login_manager = LoginManager()
login_manager.init_app(app)

# Define a rota padrão (opcional, para teste)
@app.route('/')
def index():
    return 'Aplicação Flask rodando no Google Cloud Run!'

# Não executa app.run() aqui, pois o Gunicorn vai iniciar o app
# O Gunicorn será chamado no Dockerfile com: gunicorn app:app
