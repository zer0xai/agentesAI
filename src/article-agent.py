"""
Script Didático: Gerador de Artigos com Ollama
Autor: Zer0X
Data: 2025
"""

import requests
import json
import os
import socket
from datetime import datetime
from time import sleep

def verificar_porta_ollama():
    """
    Verifica se a porta do Ollama (11434) está em uso.
    Retorna True se o Ollama parece estar rodando, False caso contrário.
    """
    try:
        # Cria um socket temporário para testar a porta
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("127.0.0.1", 11434))
        return False  # Porta está livre
    except OSError:
        return True  # Porta está ocupada (Ollama provavelmente rodando)

def matar_processo_ollama():
    """
    Tenta encerrar o processo Ollama de forma segura.
    Funciona no Windows, Linux e MacOS.
    """
    print("🔄 Tentando encerrar o Ollama...")
    
    try:
        if os.name == 'posix':  # Linux ou Mac
            os.system("pkill -f ollama")
        else:  # Windows
            os.system("taskkill /f /im ollama.exe")
        
        sleep(2)  # Dá tempo para o processo encerrar
        print("✅ Ollama encerrado com sucesso!")
    except Exception as e:
        print(f"❌ Não foi possível encerrar o Ollama: {e}")

def iniciar_ollama_se_necessario():
    """
    Garante que o Ollama está rodando antes de gerar artigos.
    Retorna True se estiver tudo ok, False em caso de erro.
    """
    if verificar_porta_ollama():
        print("✅ Ollama já está rodando!")
        return True
    
    print("🔴 Ollama não está ativo. Iniciando...")
    
    try:
        if os.name == 'posix':  # Linux ou Mac
            os.system("ollama serve &")  # & roda em segundo plano
        else:  # Windows
            os.startfile("ollama.exe")
        
        sleep(5)  # Dá tempo para iniciar
        return True
    except Exception as e:
        print(f"❌ Falha ao iniciar Ollama: {e}")
        return False

def gerar_artigo(prompt):
    """
    Gera um artigo usando o Ollama local.
    Retorna o conteúdo gerado ou uma mensagem de erro.
    """
    if not iniciar_ollama_se_necessario():
        return "[ERRO] Ollama não está disponível."
    
    try:
        print("🔄 Gerando artigo...")
        
        resposta = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": f"Escreva um artigo completo sobre: {prompt}",
                "stream": False,
                "options": {"temperature": 0.7}
            },
            timeout=30
        )
        
        resposta.raise_for_status()  # Verifica erros HTTP
        conteudo = resposta.json().get("response", "").strip()
        
        if not conteudo:
            return "[ERRO] Ollama respondeu com conteúdo vazio."
            
        return conteudo
        
    except requests.exceptions.Timeout:
        matar_processo_ollama()
        return "[ERRO] Ollama não respondeu. Tente novamente."
    except Exception as e:
        return f"[ERRO] Problema ao gerar artigo: {str(e)}"

def salvar_artigo(prompt, conteudo):
    """
    Salva o artigo nos formatos JSON e TXT.
    Retorna True se salvou com sucesso, False caso contrário.
    """
    if not conteudo or conteudo.startswith("[ERRO]"):
        print("❌ Artigo não salvo - conteúdo inválido.")
        return False
    
    try:
        # Cria um nome único para os arquivos
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_base = f"artigo_{timestamp}"
        
        # Salva em JSON (estruturado)
        with open(f"{nome_base}.json", "w", encoding="utf-8") as f:
            json.dump({
                "prompt": prompt,
                "conteudo": conteudo,
                "modelo": "llama3",
                "data": timestamp
            }, f, indent=2, ensure_ascii=False)
        
        # Salva em TXT (texto puro)
        with open(f"{nome_base}.txt", "w", encoding="utf-8") as f:
            f.write(f"Tema: {prompt}\n\n")
            f.write(conteudo)
        
        print(f"📄 Artigo salvo como:")
        print(f"  - {nome_base}.json")
        print(f"  - {nome_base}.txt")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao salvar arquivos: {str(e)}")
        return False

def main():
    """Função principal que orquestra tudo."""
    print("\n" + "="*50)
    print("GERADOR DE ARTIGOS DIDÁTICO".center(50))
    print("="*50 + "\n")
    
    # Pede o tema ao usuário
    try:
        prompt = input("? Sobre o que você quer o artigo? ").strip()
    except EOFError:
        prompt = "artigo padrão"
    
    if not prompt:
        print("❌ Por favor, digite um tema válido.")
        return
    
    # Gera o artigo
    artigo = gerar_artigo(prompt)
    
    print("\n" + "="*50)
    print("RESULTADO".center(50))
    print("="*50 + "\n")
    
    print(artigo)
    
    # Salva se não for mensagem de erro
    if not artigo.startswith("[ERRO]"):
        salvar_artigo(prompt, artigo)

if __name__ == "__main__":
    main()
