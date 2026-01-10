# 🎵 Melody Terminal Assistant

> **Assistente de IA local para terminal** que ajuda desenvolvedores iniciantes a esclarecer dúvidas sobre Linux e Python, tudo rodando offline na sua máquina! 🚀

Melody é uma IA inteligente que roda diretamente no terminal, usando **sistema híbrido** que detecta automaticamente se você quer conversar casualmente ou precisa de ajuda técnica. Ela busca informações em guias locais e responde com personalidade própria, sem depender de APIs externas.

---

## Características da Melody

- **IA Local** - Roda 100% offline usando Ollama
- **Sistema Híbrido Inteligente** - Detecta automaticamente modo casual vs técnico
- **Base de Conhecimento** - Guias de Linux e Python 3.12
- **Memória Persistente** - Lembra das conversas anteriores
- **Busca Inteligente por Triggers** - Só processa informação relevante
- **Modo Silencioso** - Terminal limpo, sem poluição visual
- **Rápida e Eficiente** - Otimizada para respostas diretas
- **Debug On-Demand** - Veja logs apenas quando necessário

---

## Requisitos do Sistema

### Requisitos Mínimos

| Componente | Especificação |
|-----------|---------------|
| **CPU** | Processador x86_64 dual-core (2+ núcleos) |
| **RAM** | 4 GB mínimo |
| **Armazenamento** | 5 GB livres |
| **OS** | Linux, macOS 11+, Windows 10/11 (com WSL2) |
| **Python** | 3.8 ou superior |

### Requisitos Recomendados

| Componente | Especificação |
|-----------|---------------|
| **RAM** | 8 GB ou mais |
| **Python** | 3.12 |
| **OS** | Ubuntu 20.04+, Zorin OS 17+|

---

## Instalação

### 1. Instalar Python 3 (se não tiver)

```bash
# Ubuntu/Debian/Zorin
sudo apt update
sudo apt install python3 python3-pip

# Fedora
sudo dnf install python3 python3-pip

# Arch
sudo pacman -S python python-pip

# Verificar instalação
python3 --version  # Deve ser >= 3.8
```

### 2. Instalar Ollama

```bash
# Linux
curl -fsSL https://ollama.com/install.sh | sh

#windows
instale no site oficial do ollama

# Verificar instalação
ollama --version
```

### 3. Baixar o Modelo Base

```bash

# OU baixe o Gemma 3:4b
ollama pull gemma3:4b
```

### 4. Clonar o Repositório

```bash
# Clone o projeto
git clone https://github.com/seu-usuario/melody-terminal.git
cd melody-terminal
```

### 5. Criar o Modelo Melody Personalizado

```bash
# Entre na pasta de modelfiles
cd modelfile

# Crie o modelo Melody baseado no Qwen
ollama create melody -f melody.modelfile

# Verifique se foi criado
ollama list
# Deve aparecer: melody:latest
```

### 6. Configurar Guias (Opcional)

Os guias já vêm no repositório, mas você pode adicionar mais:

```bash
# Navegue até a pasta guia
cd ../guia

# Adicione seus próprios guias em formato JSON ou TXT
# Exemplo: guia_docker.json, guia_git.txt
```

### 7. Executar a Melody

```bash
# Volte para a raiz do projeto
cd melody-assistent

# Execute!
python3 melody.py
```

---
# Documentação

## Como Usar?

### Iniciando a Melody

```bash
python3 melody.py
```

Você verá a tela inicial:

```
============================================================
🎵 MELODY - Assistente Linux Híbrida Inteligente
============================================================
Modelo: melody
Memória: 0 conversas
Triggers: 217
Modo silencioso: Ativado

Comandos:
  /sair ou /quit - Encerra
  /limpar - Limpa memória
  /recarregar - Recarrega guias
  /processos - Mostra log de processos
  /debug - Ativa/desativa modo debug
============================================================
```

### Exemplos de Uso

#### Modo Casual (Conversa Natural)

```
Você: olá melody!
Melody: E aí kuduu0! Tô aqui firme e forte, prontinha pra te ajudar! 
Bora resolver uns paranauês do Linux? 😄

Você: como você está?
Melody: Ótima! Rodando lisinha aqui no seu terminal. Precisa de ajuda com algo?
```

#### Modo Técnico (Assistência com Código)

```
Você: como criar uma pasta no terminal?
Melody: Fala kuduu0! Usa o mkdir aí, ó:
mkdir nome_da_pasta

Se quiser criar várias de uma vez usa mkdir -p pai/filho/neto, tranquilo? 🚀

Você: como ler arquivo json em python?
Melody: Saca só:

import json
with open('data.json', 'r') as f:
    dados = json.load(f)

Pronto! Assim você carrega o JSON numa boa. 🐍
```

### Comandos Disponíveis

| Comando | Descrição |
|---------|-----------|
| `/sair` ou `/quit` | Encerra o programa e mata processos |
| `/limpar` | Apaga o histórico de memória |
| `/recarregar` | Recarrega os arquivos guia da pasta |
| `/processos` | Mostra log detalhado de processos |
| `/debug` | Liga/desliga mensagens de debug |

---

## Estrutura do Projeto

```bash
melody-terminal/
│
├── guia/                          # Guias de conhecimento
│   ├── guia_documentacao_python3_12.json
│   └── guia_linux_comandos_terminal.json
│
├── modelfile/                     # Arquivos de configuração do modelo
│   └── melody.modelfile          # Personalização da Melody
│
├── .gitattributes
├── .gitignore
├── LICENSE
│
├── melody.py                      # Script principal (EXECUTE ESTE)
├── memoria.json                   # Histórico de conversas (gerado automaticamente)
└── README.md                      # Você está aqui! 📍
```

---

## Como Funciona?

### Sistema Híbrido Inteligente

A Melody usa um **detector automático de modo** que analisa sua pergunta:

#### 🔧 Modo Técnico
Ativado quando detecta palavras como: `como`, `criar`, `deletar`, `python`, `código`, `função`, etc.

- Busca **apenas** a informação mais relevante nos guias
- Envia contexto mínimo para resposta rápida
- Mantém personalidade da IA

#### 💬 Modo Casual
Ativado em conversas normais: `olá`, `como vai?`, `você está aí?`

- **Sem busca** nos guias
- IA pura com personalidade total
- Conversação natural

### Sistema de gatilho

Cada guia é indexado por **palavras-chave** (triggers):

```json
{
  "comando": "mkdir",
  "triggers": ["criar", "pasta", "diretório", "mkdir"],
  "descrição": "Cria diretórios"
}
```

Quando você pergunta *"como criar uma pasta?"*, a Melody:
1. Identifica triggers: `criar`, `pasta`
2. Busca **apenas** o comando `mkdir` no índice
3. Envia contexto mínimo (5-10 linhas) para a IA
4. Responde rápido com personalidade própria

---

## Adicionando Novos Guias

### Formato JSON

Crie um arquivo na pasta `guia/`:

```json
{
  "titulo": "Guia de Docker",
  "categorias": {
    "containers": {
      "descricao": "Gerenciamento de containers",
      "comandos": {
        "docker_run": {
          "descricao": "Executa um container",
          "exemplos": [
            "docker run -it ubuntu bash - inicia container Ubuntu",
            "docker run -d nginx - executa nginx em background"
          ]
        }
      }
    }
  },
  "dicas_gerais": [
    "Use docker ps para listar containers ativos",
    "docker-compose simplifica gerenciamento de múltiplos containers"
  ]
}
```

### Formato TXT (Simples)

Crie um arquivo `.txt` na pasta `guia/`:

```txt
Git - Sistema de Controle de Versão

git init - Inicializa repositório
git add . - Adiciona todos os arquivos
git commit -m "mensagem" - Cria commit
git push origin main - Envia para repositório remoto

Dica: Use git status para ver mudanças
```

### Recarregar Guias

Depois de adicionar novos guias:

```
Você: /recarregar
🔄 Guias recarregados!
```

---

## Personalização

### Modificar o Modelfile

Edite `modelfile/melody.modelfile` para mudar comportamento:

```modelfile
FROM gemma3:4b

# Ajuste a temperatura (0.5 = mais focada, 1.0 = mais criativa)
PARAMETER temperature 0.7

# Ajuste o contexto (menor = mais rápido)
PARAMETER num_ctx 2048

# Limite de tokens de resposta
PARAMETER num_predict 400

SYSTEM """
Seu nome é Melody IA...
[Personalize aqui]
"""
```

Recrie o modelo:

```bash
cd modelfile
ollama create melody -f melody.modelfile
```

### Adicionar Triggers de Palavras-chave

Edite `melody.py` e adicione palavras em `self.keywords_tecnicas`:

```python
self.keywords_tecnicas = {
    # ... existentes ...
    'docker', 'container', 'kubernetes', 'k8s',  # Novos triggers
}
```

---

## Troubleshooting

### Problema: `Ollama não encontrado`

**Solução:**
```bash
# Verifique se o Ollama está no PATH
which ollama

# Se não estiver, adicione ao PATH:
export PATH=$PATH:/usr/local/bin
```

### Problema: `Modelo melody não encontrado`

**Solução:**
```bash
# Liste os modelos instalados
ollama list

# Se não aparecer 'melody', crie novamente:
cd modelfile
ollama create melody -f melody.modelfile
```

### Problema: `Melody demora muito para responder`

**Soluções:**

1. Reduza o contexto no modelfile:
```modelfile
PARAMETER num_ctx 1024  # Era 2048
PARAMETER num_predict 300  # Era 400
```

2. Use modelo menor:
```bash
ollama pull qwen2.5:1.5b  # Mais leve
```

3. Ative modo debug para ver onde trava:
```
Você: /debug
```

### Problema: `Processo fica rodando após /exit`

**Solução:**
```bash
# Mate manualmente
pkill -9 ollama
```

Ou reinicie o script - o código já tem proteção contra isso.

### Problema: `Erro de memória insuficiente`

**Solução:**

Use modelo menor ou ajuste swap:

```bash
# Criar swap de 4GB (temporário)
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

---

## 🤝 Contribuindo

Contribuições são bem-vindas! 

### Como Contribuir

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

### Ideias de Contribuição

- Novos guias (Docker, Git, JavaScript, etc.)
- Traduções para outros idiomas
- Melhorias na interface do terminal

---

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [license para mais detalhes.

---

## Autor

Criado por **kuduu0**

- GitHub: [kaduu0](https://github.com/Kaduu0)

---

## Agradecimentos

- [Ollama](https://ollama.com/) - Por possibilitar IA local
- Comunidade Open Source 

---

<div align="center">

⭐ Se este projeto te ajudou, considere dar uma estrela!

</div>