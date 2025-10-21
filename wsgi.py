# Este arquivo é o ponto de entrada para o servidor Gunicorn.

from app import create_app

# A função create_app() é chamada a partir do __init__.py do pacote 'app'
app = create_app()
