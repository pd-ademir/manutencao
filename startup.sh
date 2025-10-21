#!/bin/sh
# Para o script se um comando falhar
set -e

# Aponta o FLASK_APP para a "application factory", o que é o correto para o CLI do Flask.
export FLASK_APP=app:create_app

echo "Executando as migrações do banco de dados..."
# Este comando agora será executado no contexto correto.
flask db upgrade

echo "Migrações concluídas. Iniciando o servidor Gunicorn..."
# O Gunicorn continua usando o wsgi:app, que é o correto para ele.
exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --worker-tmp-dir /dev/shm --timeout 300 wsgi:app
