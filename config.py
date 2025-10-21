import os

basedir = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.join(basedir, 'instance')
os.makedirs(instance_path, exist_ok=True)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'minha-chave-secreta-padrao'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(instance_path, 'db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
