# Versão base otimizada
FROM python:3.10-slim

# 1. Configurações dinâmicas
ARG APP_USER=1000
ARG OLLAMA_DIR=/root/.ollama
ARG ARTICLES_DIR=/articles
ARG APP_DIR=/app
ARG OLLAMA_MODEL=llama  # Usará sempre a última versão estável

# 2. Variáveis de ambiente atualizáveis
ENV OLLAMA_HOST=127.0.0.1 \
    OLLAMA_MODELS=${OLLAMA_DIR}/models \
    ARTICLES_DIR=${ARTICLES_DIR} \
    OLLAMA_KEEP_ALIVE=5m \
    OLLAMA_MAX_LOADED_MODELS=3

# 3. Instalação do Ollama com auto-atualização
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    jq && \
    rm -rf /var/lib/apt/lists/* && \
    curl -fsSL https://ollama.com/install.sh | sh && \
    mkdir -p ${OLLAMA_DIR} && \
    chown -R ${APP_USER}:${APP_USER} ${OLLAMA_DIR}

# 4. Script para obter e instalar o modelo mais recente
COPY update_model.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/update_model.sh

# 5. Configuração do ambiente Python
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir \
    requests \
    openai \
    python-dotenv \
    deep-translator \
    semver  # Para controle de versões

# 6. Configuração da aplicação
WORKDIR ${APP_DIR}
COPY --chown=${APP_USER}:${APP_USER} src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=${APP_USER}:${APP_USER} src .

# 7. Diretórios persistentes
RUN mkdir -p ${ARTICLES_DIR} && \
    chown -R ${APP_USER}:${APP_USER} ${ARTICLES_DIR}

USER ${APP_USER}

# 8. Entrypoint atualizável
COPY --chown=${APP_USER}:${APP_USER} entrypoint.sh .
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
