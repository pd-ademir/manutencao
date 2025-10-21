#!/bin/sh
# Para o script se um comando falhar
set -e

# Garante que o Flask saiba qual aplicação usar
export FLASK_APP=wsgi:app

echo "Aguardando o banco de dados iniciar (se aplicável)..."
# Em um cenário real com Postgres/MySQL, adicionaríamos um 'wait-for-it.sh' aqui

echo "Executando as migrações do banco de dados..."
flask db upgrade

echo "Migrações concluídas. Iniciando o servidor Gunicorn..."
# Inicia o servidor Gunicorn, substituindo o processo do shell
exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --worker-tmp-dir /dev/shm --timeout 300 wsgi:app
