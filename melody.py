#!/usr/bin/env python3
"""
Terminal AI Assistant com Memória e Modo Híbrido Inteligente
Detecta automaticamente entre conversa casual e busca técnica
"""

import json
import os
import subprocess
import re
from datetime import datetime
from pathlib import Path

class MelodyTerminal:
    def __init__(self):
        # Sistema de log silencioso - DEVE VIR PRIMEIRO!
        self.modo_silencioso = True
        self.log_processos = []
        
        # Configurações básicas
        self.guia_dir = Path("guia")
        self.memoria_file = Path("memoria.json")
        self.modelo = "melody"
        
        # Carrega dados (agora pode usar self.log())
        self.memoria = self.carregar_memoria()
        self.guias_completos = self.carregar_guias()
        self.indice_triggers = self.construir_indice_triggers()
        
        # Palavras-chave técnicas que indicam busca no guia
        self.keywords_tecnicas = {
            # Linux/Terminal
            'comando', 'comandos', 'como', 'criar', 'deletar', 'remover', 'listar',
            'copiar', 'mover', 'ver', 'mostrar', 'instalar', 'desinstalar',
            'executar', 'rodar', 'arquivo', 'pasta', 'diretório', 'permissão',
            'terminal', 'linux', 'script', 'processo', 'memória', 'disco',
            'rede', 'ip', 'ping', 'wget', 'curl', 'grep', 'find', 'chmod',
            'chown', 'sudo', 'apt', 'system', 'service',
            # Python
            'python', 'python3', 'py', 'código', 'codigo', 'programar', 'programa',
            'função', 'funcao', 'class', 'classe', 'def', 'import', 'importar',
            'lista', 'list', 'dicionário', 'dicionario', 'dict', 'string', 'int',
            'float', 'tuple', 'tupla', 'set', 'for', 'while', 'if', 'elif', 'else',
            'try', 'except', 'raise', 'lambda', 'map', 'filter', 'comprehension',
            'async', 'await', 'generator', 'yield', 'decorator', 'property',
            'json', 'csv', 'arquivo', 'ler', 'escrever', 'abrir', 'open',
            'print', 'input', 'variavel', 'tipo', 'type', 'conversão', 'converter',
            'loop', 'iteração', 'iterar', 'format', 'formatação', 'formatar',
            'erro', 'exception', 'error', 'debug', 'método', 'metodo', 'atributo',
            'herança', 'heranca', 'polimorfismo', 'encapsulamento', 'oop',
            'módulo', 'modulo', 'biblioteca', 'package', 'pip', 'instalar'
        }
        
    def log(self, mensagem, tipo="info"):
        """Adiciona mensagem ao log e mostra apenas se não estiver silencioso"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = {
            "timestamp": timestamp,
            "tipo": tipo,
            "mensagem": mensagem
        }
        self.log_processos.append(log_entry)
        
        # Limita log a últimas 50 entradas
        if len(self.log_processos) > 50:
            self.log_processos = self.log_processos[-50:]
        
        # Mostra apenas se não estiver silencioso
        if not self.modo_silencioso:
            emoji = {
                "info": "ℹ️",
                "sucesso": "✅",
                "erro": "❌",
                "aviso": "⚠️",
                "busca": "🔍",
                "ia": "🎵"
            }.get(tipo, "•")
            print(f"{emoji} {mensagem}")
    
    def mostrar_processos(self):
        """Mostra histórico de processos/logs"""
        print("\n" + "=" * 60)
        print("📊 HISTÓRICO DE PROCESSOS")
        print("=" * 60)
        
        if not self.log_processos:
            print("Nenhum processo registrado ainda.")
        else:
            for entry in self.log_processos[-20:]:  # Mostra últimos 20
                print(f"[{entry['timestamp']}] {entry['mensagem']}")
        
        print("=" * 60 + "\n")
    
    def carregar_memoria(self):
        """Carrega histórico de conversas anteriores"""
        if self.memoria_file.exists():
            try:
                with open(self.memoria_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {"conversas": []}
        return {"conversas": []}
    
    def salvar_memoria(self):
        """Salva a memória no arquivo JSON"""
        with open(self.memoria_file, 'w', encoding='utf-8') as f:
            json.dump(self.memoria, f, ensure_ascii=False, indent=2)
    
    def carregar_guias(self):
        """Carrega todos os arquivos guia da pasta"""
        guias = []
        
        if not self.guia_dir.exists():
            print(f"⚠️  Pasta '{self.guia_dir}' não encontrada. Criando...")
            self.guia_dir.mkdir(exist_ok=True)
            return guias
        
        # Carrega arquivos .json
        for arquivo in self.guia_dir.glob("*.json"):
            try:
                with open(arquivo, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                    guias.append({
                        "nome": arquivo.name,
                        "tipo": "json",
                        "conteudo": dados
                    })
            except Exception as e:
                print(f"⚠️  Erro ao carregar {arquivo.name}: {e}")
        
        # Carrega arquivos .txt
        for arquivo in self.guia_dir.glob("*.txt"):
            try:
                with open(arquivo, 'r', encoding='utf-8') as f:
                    conteudo = f.read()
                    guias.append({
                        "nome": arquivo.name,
                        "tipo": "txt",
                        "conteudo": conteudo
                    })
            except Exception as e:
                print(f"⚠️  Erro ao carregar {arquivo.name}: {e}")
        
        if guias:
            self.log(f"Carregados {len(guias)} arquivo(s) guia", "sucesso")
        else:
            self.log(f"Nenhum arquivo guia encontrado em '{self.guia_dir}'", "aviso")
            
        return guias
    
    def construir_indice_triggers(self):
        """Constrói índice de triggers para busca rápida"""
        indice = {}
        
        for guia in self.guias_completos:
            if guia["tipo"] == "json":
                self._indexar_json(guia["conteudo"], guia["nome"], indice)
            elif guia["tipo"] == "txt":
                self._indexar_txt(guia["conteudo"], guia["nome"], indice)
        
        self.log(f"Índice criado com {len(indice)} triggers", "sucesso")
        return indice
    
    def _indexar_json(self, dados, nome_arquivo, indice):
        """Indexa arquivo JSON recursivamente"""
        
        if isinstance(dados, dict):
            if "categorias" in dados:
                for cat_nome, categoria in dados["categorias"].items():
                    if "comandos" in categoria:
                        for cmd_nome, comando in categoria["comandos"].items():
                            triggers = [
                                cmd_nome.lower(),
                                categoria.get("descricao", "").lower(),
                                comando.get("descricao", "").lower()
                            ]
                            
                            if "exemplos" in comando:
                                for ex in comando["exemplos"]:
                                    triggers.extend(ex.lower().split())
                            
                            triggers = [t.strip() for t in triggers if t.strip()]
                            
                            for trigger in triggers:
                                if trigger not in indice:
                                    indice[trigger] = []
                                indice[trigger].append({
                                    "arquivo": nome_arquivo,
                                    "categoria": cat_nome,
                                    "comando": cmd_nome,
                                    "conteudo": comando
                                })
    
    def _indexar_txt(self, conteudo, nome_arquivo, indice):
        """Indexa arquivo TXT por linhas"""
        linhas = conteudo.split('\n')
        for i, linha in enumerate(linhas):
            if linha.strip():
                palavras = linha.lower().split()
                for palavra in palavras:
                    palavra = palavra.strip(".,!?:")
                    if len(palavra) > 3:
                        if palavra not in indice:
                            indice[palavra] = []
                        indice[palavra].append({
                            "arquivo": nome_arquivo,
                            "linha": i + 1,
                            "conteudo": linha.strip()
                        })
    
    def detectar_modo(self, pergunta):
        """Detecta se é pergunta técnica ou conversa casual"""
        pergunta_lower = pergunta.lower()
        
        # Saudações e conversas casuais
        saudacoes = ['olá', 'oi', 'ola', 'hey', 'e aí', 'eai', 'como vai', 'tudo bem', 'beleza']
        for saudacao in saudacoes:
            if pergunta_lower.strip().startswith(saudacao) and len(pergunta.split()) <= 4:
                return 'casual'
        
        # Conta quantas palavras técnicas tem
        palavras = pergunta_lower.split()
        palavras_tecnicas_encontradas = sum(1 for p in palavras if p in self.keywords_tecnicas)
        
        # Se tem 2+ palavras técnicas, é técnico
        if palavras_tecnicas_encontradas >= 2:
            return 'tecnico'
        
        # Se tem palavras como "como" + palavra técnica
        if 'como' in palavras and palavras_tecnicas_encontradas >= 1:
            return 'tecnico'
        
        # Se tem "?" e alguma palavra técnica, provavelmente é técnico
        if '?' in pergunta and palavras_tecnicas_encontradas >= 1:
            return 'tecnico'
        
        # Caso contrário, é casual
        return 'casual'
    
    def buscar_contexto_minimo(self, pergunta):
        """Busca APENAS o comando mais relevante (1 resultado)"""
        self.log("Analisando pergunta...", "busca")
        pergunta_lower = pergunta.lower()
        
        stopwords = {'o', 'a', 'de', 'da', 'do', 'para', 'com', 'como', 'que', 'um', 'uma', 'em', 'no', 'na'}
        palavras = [p.strip(".,!?") for p in pergunta_lower.split() if p not in stopwords]
        
        self.log(f"Palavras-chave: {', '.join(palavras[:5])}", "busca")
        
        # Busca o melhor resultado
        melhor_resultado = None
        max_score = 0
        
        for palavra in palavras:
            if palavra in self.indice_triggers:
                for item in self.indice_triggers[palavra]:
                    score = 1
                    if "comando" in item:
                        score += 3
                        if item["comando"].lower() in pergunta_lower:
                            score += 5
                    
                    if score > max_score:
                        max_score = score
                        melhor_resultado = item
        
        if not melhor_resultado:
            self.log("Nenhuma referência específica encontrada", "aviso")
            return None
        
        self.log(f"Referência encontrada: {melhor_resultado.get('comando', 'N/A')}", "sucesso")
        
        # Formata apenas 1 resultado compacto
        if "comando" in melhor_resultado:
            cmd = melhor_resultado["conteudo"]
            resultado_texto = f"📌 {melhor_resultado['comando']}: {cmd.get('descricao', '')}"
            
            if "exemplos" in cmd and cmd["exemplos"]:
                resultado_texto += f"\nEx: {cmd['exemplos'][0]}"
            
            return resultado_texto
        
        return None
    
    def construir_prompt(self, pergunta_usuario, modo):
        """Constrói prompt baseado no modo detectado"""
        prompt_partes = []
        
        if modo == 'casual':
            self.log("Modo: Conversa Casual", "ia")
            
            if self.memoria["conversas"]:
                conversas_recentes = self.memoria["conversas"][-2:]
                for conv in conversas_recentes:
                    prompt_partes.append(f"Usuário: {conv['pergunta']}")
                    prompt_partes.append(f"Você: {conv['resposta'][:80]}...\n")
            
            prompt_partes.append(f"Pergunta: {pergunta_usuario}")
            
        else:
            self.log("Modo: Assistência Técnica", "ia")
            
            contexto = self.buscar_contexto_minimo(pergunta_usuario)
            if contexto:
                prompt_partes.append("=== REFERÊNCIA RÁPIDA ===")
                prompt_partes.append(contexto)
                prompt_partes.append("=== FIM ===\n")
            
            prompt_partes.append(f"Pergunta: {pergunta_usuario}")
        
        return "\n".join(prompt_partes)
    
    def perguntar_melody(self, pergunta, modo):
        """Envia pergunta pro Ollama SEM timeout (IA livre)"""
        self.log("Preparando contexto...", "ia")
        prompt = self.construir_prompt(pergunta, modo)
        
        self.log(f"Enviando para Melody ({len(prompt)} caracteres)", "ia")
        
        processo = None
        try:
            self.log("Melody está pensando...", "ia")
            processo = subprocess.Popen(
                ['ollama', 'run', self.modelo, prompt],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # SEM TIMEOUT - deixa ela pensar o quanto quiser
            stdout, stderr = processo.communicate()
            
            if processo.returncode == 0:
                self.log("Resposta recebida!", "sucesso")
                return stdout.strip()
            else:
                self.log(f"Erro no Ollama: {stderr}", "erro")
                return f"❌ Erro ao executar Ollama: {stderr}"
                
        except FileNotFoundError:
            self.log("Ollama não encontrado", "erro")
            return "❌ Ollama não encontrado."
        except KeyboardInterrupt:
            self.log("Interrompido pelo usuário (Ctrl+C)", "aviso")
            if processo:
                processo.kill()
            return "❌ Resposta cancelada pelo usuário."
        except Exception as e:
            self.log(f"Erro inesperado: {e}", "erro")
            if processo:
                try:
                    processo.kill()
                except:
                    pass
            return f"❌ Erro: {e}"
    
    def adicionar_a_memoria(self, pergunta, resposta):
        """Adiciona interação à memória"""
        interacao = {
            "timestamp": datetime.now().isoformat(),
            "pergunta": pergunta,
            "resposta": resposta
        }
        self.memoria["conversas"].append(interacao)
        
        # Limita memória a 50 conversas
        if len(self.memoria["conversas"]) > 50:
            self.memoria["conversas"] = self.memoria["conversas"][-50:]
        
        self.salvar_memoria()
    
    def iniciar_chat(self):
        """Loop principal do chat"""
        print("=" * 60)
        print("🎵 MELODY - Assistente Linux Híbrida Inteligente")
        print("=" * 60)
        print(f"Modelo: {self.modelo}")
        print(f"Memória: {len(self.memoria['conversas'])} conversas")
        print(f"Triggers: {len(self.indice_triggers)}")
        print(f"Modo silencioso: {'Ativado' if self.modo_silencioso else 'Desativado'}")
        print("\nComandos:")
        print("  /sair ou /quit - Encerra")
        print("  /limpar - Limpa memória")
        print("  /recarregar - Recarrega guias")
        print("  /processos - Mostra log de processos")
        print("  /debug - Ativa/desativa modo debug")
        print("=" * 60)
        print()
        
        while True:
            try:
                pergunta = input("Você: ").strip()
                
                if not pergunta:
                    continue
                
                if pergunta.lower() in ['/sair', '/quit', '/exit']:
                    print("\n🛑 Encerrando Melody...")
                    self.log("Comando de saída recebido", "info")
                    
                    # Mata todos os processos do Ollama relacionados ao modelo
                    try:
                        self.log("Finalizando processos do Ollama...", "info")
                        # Mata processo do modelo melody especificamente
                        subprocess.run(['pkill', '-9', '-f', f'ollama.*{self.modelo}'], 
                                     stderr=subprocess.DEVNULL, timeout=2)
                        # Mata servidor ollama se estiver rodando
                        subprocess.run(['pkill', '-9', 'ollama'], 
                                     stderr=subprocess.DEVNULL, timeout=2)
                        self.log("Processos finalizados com sucesso", "sucesso")
                    except Exception as e:
                        self.log(f"Aviso ao finalizar processos: {e}", "aviso")
                    
                    print("👋 Até logo!")
                    break
                
                if pergunta.lower() == '/limpar':
                    self.memoria = {"conversas": []}
                    self.salvar_memoria()
                    print("🗑️  Memória limpa!\n")
                    continue
                
                if pergunta.lower() == '/recarregar':
                    self.guias_completos = self.carregar_guias()
                    self.indice_triggers = self.construir_indice_triggers()
                    print("🔄 Guias recarregados!\n")
                    continue
                
                if pergunta.lower() == '/processos':
                    self.mostrar_processos()
                    continue
                
                if pergunta.lower() == '/debug':
                    self.modo_silencioso = not self.modo_silencioso
                    status = "desativado" if self.modo_silencioso else "ativado"
                    print(f"🔧 Modo debug {status}!\n")
                    continue
                
                # Detecta modo e processa
                if not self.modo_silencioso:
                    print("\n" + "=" * 60)
                modo = self.detectar_modo(pergunta)
                resposta = self.perguntar_melody(pergunta, modo)
                if not self.modo_silencioso:
                    print("=" * 60)
                
                print(f"\nMelody: {resposta}\n")
                
                self.adicionar_a_memoria(pergunta, resposta)
                
                if not self.modo_silencioso:
                    print("-" * 60 + "\n")
                
            except KeyboardInterrupt:
                print("\n\n🛑 Encerrando Melody...")
                self.log("Interrupção por Ctrl+C", "aviso")
                
                # Mata processos do Ollama
                try:
                    subprocess.run(['pkill', '-9', '-f', f'ollama.*{self.modelo}'], 
                                 stderr=subprocess.DEVNULL, timeout=2)
                    subprocess.run(['pkill', '-9', 'ollama'], 
                                 stderr=subprocess.DEVNULL, timeout=2)
                    self.log("Processos finalizados", "sucesso")
                except:
                    pass
                
                print("👋 Até logo!")
                break
            except Exception as e:
                print(f"\n❌ Erro: {e}\n")

def main():
    """Função principal"""
    melody = None
    try:
        melody = MelodyTerminal()
        melody.iniciar_chat()
    except Exception as e:
        print(f"❌ Erro fatal: {e}")
        return 1
    finally:
        # Garante que processos são mortos ao sair
        if melody:
            try:
                subprocess.run(['pkill', '-9', '-f', f'ollama.*{melody.modelo}'], 
                             stderr=subprocess.DEVNULL, timeout=2)
                subprocess.run(['pkill', '-9', 'ollama'], 
                             stderr=subprocess.DEVNULL, timeout=2)
            except:
                pass
    return 0

if __name__ == "__main__":
    exit(main())