import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'minha-chave-secreta-padrao'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance', 'db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
