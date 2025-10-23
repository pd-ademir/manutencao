import os

class Config:
    """
    Configurações para a aplicação Flask com múltiplos bancos MySQL.
    As credenciais e URIs são configuradas para conectar aos bancos na nuvem.
    """

    SECRET_KEY = os.environ.get('SECRET_KEY', 'uma-chave-secreta-padrao')  # Mantenha a variável de ambiente em produção
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-chave-secreta-padrao')

    # Configuração para banco principal "manutencao"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL_MANUTENCAO') or \
        'mysql+pymysql://ornilio:@Machado2025@136.113.79.172/manutencao'

    # Configurações para os outros bancos "pneus" e "checklist" via binds
    SQLALCHEMY_BINDS = {
        'pneus': os.environ.get('DATABASE_URL_PNEUS') or 'mysql+pymysql://ornilio:@Machado2025@136.113.79.172/pneus',
        'checklist': os.environ.get('DATABASE_URL_CHECKLIST') or 'mysql+pymysql://ornilio:@Machado2025@136.113.79.172/checklist'
    }

    SQLALCHEMY_TRACK_MODIFICATIONS = False

        # Pooling de conexões para melhorar desempenho
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_POOL_TIMEOUT = 30
    SQLALCHEMY_POOL_RECYCLE = 1800
    SQLALCHEMY_MAX_OVERFLOW = 20

