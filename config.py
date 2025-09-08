import os

# 'basedir' agora aponta para a raiz do projeto (a pasta 'manutencao'),
# subindo um nível a partir do diretório do arquivo de configuração (que está em 'app').
basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Garante que a pasta 'instance' exista na raiz do projeto.
# Se não existir, este comando a criará.
instance_path = os.path.join(basedir, 'instance')
os.makedirs(instance_path, exist_ok=True)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'minha-chave-secreta-padrao'
    
    # Esta URI agora funcionará tanto no seu Windows quanto no servidor Linux,
    # pois sempre apontará para a pasta 'instance' na raiz do projeto.
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(instance_path, 'db.sqlite3')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
