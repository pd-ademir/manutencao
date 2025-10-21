#!/bin/sh
# Encerra o script se qualquer comando falhar
set -e

# Garante que o diretório raiz está no PYTHONPATH para evitar erros de import
export PYTHONPATH=/app

# Aponta o Flask para a Application Factory (create_app dentro de app/__init__.py)
export FLASK_APP=app:create_app

echo "🐍 [Startup] Executando as migrações do banco de dados..."
flask db upgrade || { echo "❌ Falha ao executar flask db upgrade"; exit 1; }

echo "✅ Migrações concluídas com sucesso."

echo "🚀 Iniciando o Gunicorn na porta $PORT..."
exec gunicorn --bind 0.0.0.0:$PORT \
  --workers 1 \
  --worker-tmp-dir /dev/shm \
  --timeout 300 \
  --log-level debug \
  wsgi:app
