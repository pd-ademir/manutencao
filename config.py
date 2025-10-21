import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env (se ele existir)
load_dotenv()

# Determina o diretório base do projeto
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Classe de configuração principal. Define as configurações que são
    compartilhadas por todos os ambientes (produção, desenvolvimento, etc).
    """
    
    # CHAVE SECRETA (SECRET_KEY)
    # Essencial para a segurança das sessões e do CSRF.
    # O ideal é que em produção ela seja definida como uma variável de ambiente.
    # Se a variável de ambiente não for encontrada, uma chave aleatória e menos
    # segura é gerada para evitar que a aplicação quebre. Isso é útil para
    # ambientes de teste e desenvolvimento.
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
    
    # CONFIGURAÇÃO DO BANCO DE DADOS (SQLALCHEMY_DATABASE_URI)
    # Tenta carregar a URL do banco de dados a partir das variáveis de ambiente.
    # Se não encontrar, usa um banco de dados SQLite local como fallback.
    # ATENÇÃO: Usar SQLite em produção no Cloud Run não é recomendado pois o
    # sistema de arquivos é efêmero, mas serve para o deploy inicial funcionar.
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    
    # Desativa um recurso do SQLAlchemy que não usaremos e que consome recursos.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Outras configurações do seu app podem vir aqui...
