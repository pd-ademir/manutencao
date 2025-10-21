# 1. Imagem base leve com Python 3.11
FROM python:3.11-slim

# 2. Define o diretório de trabalho dentro do container
WORKDIR /app

# 3. Copia o arquivo de dependências e instala os pacotes
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 4. Copia o restante do código da aplicação
COPY . .

# 5. Expõe a porta 8080 (usada pelo Cloud Run)
EXPOSE 8080

# 6. Comando para iniciar o servidor com Gunicorn
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --worker-tmp-dir /dev/shm --timeout 300 app:app
