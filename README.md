oc---

# 📝 Content Automation Ecosystem / Ecossistema de Automação de Conteúdo  
*AI-powered article writing, translation, and video editing — all containerized with Docker!*  
*Escrita de artigos, tradução e edição de vídeo via IA — tudo containerizado com Docker!*  

---

## 🌐 **Language / Idioma**  
- [English](#-quick-start) (Default)  
- [Português](#-começo-rápido)  

---

## 🚀 **Quick Start**  
### **Prerequisites / Pré-requisitos**  
- Docker ([Install guide](https://docs.docker.com/get-docker/))  
- Docker Compose (included with Docker Desktop)  
- API keys (OpenAI, etc.) — see [`.env.example`](#-environment-variables--variáveis-de-ambiente)  

### **1. Clone and configure**  
```bash
git clone https://github.com/seu-usuario/ecossistema-conteudo.git
cd ecossistema-conteudo
cp .env.example .env  # Add your API keys here!
```

### **2. Start containers**  
```bash
docker-compose up -d
```

### **3. Run the article agent**  
```bash
docker-compose exec agent python article-agent.py --prompt "Explain AI in 3 lines"
```
*(For interactive mode: `docker-compose exec -it agent python article-agent.py`)*  

---

## 🐳 **Key Commands / Comandos Principais**  

### **Containers**  
| Command / Comando | Description / Descrição |  
|-------------------|------------------------|  
| `dc-up` | Start all services |  
| `dc-down` | Stop and remove containers |  
| `dc-rebuild` | Rebuild images and restart |  

### **Ollama (Llama3)**  
```bash
ollama-pull llama3  # Download model  
ollama-run llama3 "Your prompt"  # Generate text  
```

### **Debugging / Depuração**  
```bash
dc-bash agent  # Enter container shell  
dc-logs agent  # Check logs  
```

---

## 📂 **Project Structure / Estrutura**  
```bash
.
├── agent/
│   ├── article-agent.py  # Main Python script
│   ├── Dockerfile
├── ollama/               # LLM service
├── docker-compose.yml
└── .env.example
```

---

## ❓ **FAQ (English)**  
### **How to edit code without rebuilding?**  
Files are synced via Docker volumes — edit `article-agent.py` locally!  

### **Adding new services?**  
1. Create a folder (e.g., `translator/`)  
2. Add its `Dockerfile`  
3. Update `docker-compose.yml`  

---

## ❓ **FAQ (Português)**  
### **Como editar sem rebuild?**  
Arquivos estão sincronizados via volumes — edite `article-agent.py` direto no seu OS!  

### **Adicionar novos serviços?**  
1. Crie uma pasta (ex.: `translator/`)  
2. Adicione um `Dockerfile`  
3. Atualize o `docker-compose.yml`  

---

## 🔧 **Troubleshooting / Solução de Problemas**  

### **English**  
- **"Port in use"**: Run `dc-down` then `dc-up`  
- **"Module not found"**: Use `dc-rebuild`  
- **Ollama errors**: Check logs with `dc-logs ollama`  

### **Português**  
- **"Porta em uso"**: Execute `dc-down` e depois `dc-up`  
- **"Módulo não encontrado"**: Use `dc-rebuild`  
- **Erros no Ollama**: Verifique com `dc-logs ollama`  

---

## 💡 **Aliases (Add to `~/.bashrc`)**  
```bash
# English comments above each alias / Comentários em português abaixo
alias dc-up='docker-compose up -d'        # Inicia containers
alias dc-down='docker-compose down'       # Para containers
alias ollama-run='docker-compose exec ollama ollama run'  # Roda modelos
```

---

### **License / Licença**  
MIT © [Your Name]  

--- 

### **Notes for Your Course / Notas para Seu Curso**  
- For YouTube: Include a **video demo** of `docker-compose up` and running `article-agent.py`.  
- Para o YouTube: Adicione um **vídeo** mostrando `docker-compose up` e o `article-agent.py` em ação.  

--- 
