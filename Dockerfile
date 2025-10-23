# 1. Imagem base leve com Python 3.11
FROM python:3.11-slim

# 2. Define o diretório de trabalho dentro do container
WORKDIR /app

# 3. Instala as dependências do sistema operacional
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    pkg-config \
    libcairo2-dev \
    libpango-1.0-0 \
    libharfbuzz0b \
    libfribidi0 \
    libjpeg62-turbo \
    libopenjp2-7 \
    libtiff6 \
    libgl1 \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# 4. Copia apenas o necessário para instalar as dependências Python
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 5. Copia todo o código da aplicação, incluindo o novo script de inicialização
COPY . .

# 6. Torna o script de inicialização executável DENTRO do container
RUN chmod +x /app/startup.sh

# 7. Expõe a porta que o Cloud Run espera
EXPOSE 8080

# 8. Define o script de inicialização como o comando de entrada. 
# Ele cuidará de rodar as migrações e depois iniciar o Gunicorn.
CMD ["/app/startup.sh"]
