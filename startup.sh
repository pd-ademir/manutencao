#!/bin/sh
# set -x: Imprime cada comando no log antes de executá-lo.
# set -e: Sai imediatamente se um comando falhar.
set -ex

echo "--- INICIANDO SCRIPT DE DIAGNÓSTICO ---"

echo "[DIAGNÓSTICO] Pulando 'flask db upgrade' intencionalmente para teste."

# echo "[DEBUG] Imprimindo variáveis de ambiente..."
# printenv

echo "[DIAGNÓSTICO] Iniciando Gunicorn diretamente..."

# Tenta iniciar o servidor web diretamente, sem migrações.
# O wsgi:app aponta para o arquivo wsgi.py, que chama a função create_app()
exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --worker-tmp-dir /dev/shm --timeout 300 wsgi:app
