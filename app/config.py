import os

# Determina o diretório base do projeto
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Classe de configuração principal. As configurações são lidas
    DIRETAMENTE das variáveis de ambiente injetadas pelo Cloud Run.
    """
    
    # CHAVE SECRETA (SECRET_KEY)
    # Em produção, a aplicação irá falhar se esta variável não for definida,
    # o que é um comportamento seguro.
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # CONFIGURAÇÃO DO BANCO DE DADOS (SQLALCHEMY_DATABASE_URI)
    # No ambiente Cloud Run, vamos usar um diretório temporário e seguro para o SQLite.
    # /dev/shm é um diretório em memória, ideal para um banco de dados temporário.
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or \
        'sqlite:////dev/shm/app.db'
    
    # Desativa um recurso do SQLAlchemy que não usaremos e que consome recursos.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT Secret Key
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
