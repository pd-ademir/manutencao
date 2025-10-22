#!/bin/sh
# set -x: Imprime cada comando no log antes de executá-lo.
# set -e: Sai imediatamente se um comando falhar.
set -ex

echo "--- INICIANDO SCRIPT DE DEBUG ---"

echo "[DEBUG] 1. Imprimindo todas as variáveis de ambiente..."
printenv
echo "------------------------------------------------------"

echo "[DEBUG] 2. Definindo FLASK_APP..."
export FLASK_APP=app:create_app
echo "FLASK_APP definido como: $FLASK_APP"

echo "[DEBUG] 3. Tentando executar as migrações do banco de dados..."
# Executa o comando e força a exibição de qualquer erro.
flask db upgrade
echo "------------------------------------------------------"

echo "[DEBUG] 4. Se você está vendo esta mensagem, a migração foi bem-sucedida."
echo "Iniciando Gunicorn..."

# O comando final para iniciar o servidor web
exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --worker-tmp-dir /dev/shm --timeout 300 wsgi:app
