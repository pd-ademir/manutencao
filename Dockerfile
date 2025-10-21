# 1. Imagem base leve com Python 3.11
FROM python:3.11-slim

# 2. Define o diretório de trabalho dentro do container
WORKDIR /app

# 3. Instala dependências do sistema operacional (Debian/Linux)
# Essencial para bibliotecas como WeasyPrint, OpenCV, Pillow, etc.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpango1.0-0 \
    libharfbuzz0b \
    libfribidi0 \
    libjpeg62-turbo \
    libopenjp2-7 \
    libtiff5 \
    libgl1-mesa-glx \
    # Limpa o cache do apt para manter a imagem final menor
    && rm -rf /var/lib/apt/lists/*

# 4. Copia o arquivo de dependências e instala os pacotes Python
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 5. Copia o restante do código da aplicação para o container
COPY . .

# 6. Expõe a porta que o Cloud Run espera
EXPOSE 8080

# 7. Comando para iniciar o servidor com Gunicorn (sem alterações)
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --worker-tmp-dir /dev/shm --timeout 300 wsgi:app
