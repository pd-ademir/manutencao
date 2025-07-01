import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'minha-chave-secreta-padrao'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///manutencao.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
