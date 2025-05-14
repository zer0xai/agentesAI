#!/bin/bash

# Verifica se o Ollama está respondendo
while ! ollama list >/dev/null 2>&1; do
    echo "Aguardando Ollama ficar disponível..."
    sleep 5
done

# Obtém a última versão estável do modelo
LATEST_MODEL=$(curl -s https://registry.ollama.ai/v2/library/${OLLAMA_MODEL:-llama}/tags/list | jq -r '.tags[]' | grep -v "latest" | sort -V | tail -n1)

echo "Usando modelo ${OLLAMA_MODEL}:${LATEST_MODEL}"

# Puxa a versão mais recente
ollama pull ${OLLAMA_MODEL}:${LATEST_MODEL} || exit 1

# Atualiza o alias 'latest'
ollama tag ${OLLAMA_MODEL}:${LATEST_MODEL} ${OLLAMA_MODEL}:latest
