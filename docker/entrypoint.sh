#!/bin/bash
# Script de inicialização otimizado para o Agente AI

set -e  # Encerra o script imediatamente em caso de erro

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

download_model() {
    local model_name=$1
    log "Baixando modelo $model_name..."
    if ! ollama pull $model_name; then
        log "❌ Falha ao baixar $model_name"
        return 1
    fi
    log "✅ Modelo $model_name baixado com sucesso"
}

# 1. Inicia o Ollama em segundo plano
log "Iniciando servidor Ollama..."
ollama serve > /var/log/ollama.log 2>&1 &

# 2. Espera inicialização com timeout
MAX_WAIT=30
ATTEMPT=0
log "Verificando saúde do Ollama..."

while [ $ATTEMPT -lt $MAX_WAIT ]; do
    if ollama list >/dev/null 2>&1; then
        log "Ollama pronto!"
        break
    fi
    sleep 1
    ATTEMPT=$((ATTEMPT+1))
done

if [ $ATTEMPT -eq $MAX_WAIT ]; then
    log "❌ Timeout: Ollama não respondeu após $MAX_WAIT segundos"
    exit 1
fi

# 3. Baixa modelos padrão (sempre baixa Llama3 estável)
MODEL_STABLE="llama3"  # Última versão estável
download_model $MODEL_STABLE

# 4. Modelos adicionais via variável de ambiente
if [ -n "$EXTRA_MODELS" ]; then
    IFS=',' read -ra MODELS <<< "$EXTRA_MODELS"
    for model in "${MODELS[@]}"; do
        download_model "$model"
    done
fi

# 5. Executa o aplicativo principal
log "Iniciando agente escritor..."
exec python /app/agente-escritor.py
