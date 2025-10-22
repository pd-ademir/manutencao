#!/bin/sh
set -e

# Define a variável de ambiente para o CLI do Flask funcionar corretamente
export FLASK_APP=app:create_app

echo "Executando migrações do banco de dados..."
flask db upgrade

echo "Migrações concluídas. Iniciando o servidor Gunicorn..."
exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --worker-tmp-dir /dev/shm --timeout 300 wsgi:app
