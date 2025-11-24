# 🌟 Asteria - Advanced AI Discord Bot

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Asteria** é um bot Discord de RP (Roleplay) avançado com IA local (Ollama), sistema de personalidade emocional complexo, memória de longo prazo (RAG/ChromaDB), e respostas automáticas em estilo narrativo literário.

## ✨ Características Principais

- 🤖 **IA Local**: Usa modelos Ollama (Hermes 3 8B, Qwen 2.5 3B/0.5B)
- 🧠 **Memória RAG**: Sistema de memória vetorial infinita com ChromaDB
- 🎭 **RP Automático**: Detecta e responde automaticamente a cenas de roleplay
- 💜 **Persona Avançada**: Sistema emocional multidimensional (valência, ativação, dominância)
- 🎯 **Smart Router**: Escolha automática de modelo baseada na complexidade
- 📋 **Sistema de Fichas**: Suporte a fichas de personagem para RP contextual
- ⚡ **Slash Commands**: Comandos modernos do Discord (`/ping`, `/perfil`, `/rp`, etc.)

## 🚀 Instalação

### Requisitos
- Python 3.10+
- Ollama instalado ([ollama.ai](https://ollama.ai))
- Token de bot Discord

### Passo 1: Clone o repositório
```bash
git clone https://github.com/SEU_USUARIO/Asteria.git
cd Asteria
```

### Passo 2: Crie ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### Passo 3: Instale dependências
```bash
pip install -r requirements.txt
```

### Passo 4: Configure modelos Ollama
```bash
ollama pull hermes3:8b
ollama pull qwen2.5:3b
ollama pull qwen2.5:0.5b
```

### Passo 5: Configure variáveis de ambiente
```bash
cp .env.example .env
# Edite .env e adicione seu DISCORD_BOT_TOKEN
```

### Passo 6: Execute o bot
```bash
python main.py
```

## 📋 Configuração

### Arquivo `.env`
```env
DISCORD_BOT_TOKEN=seu_token_aqui
CREATOR_ID=seu_id_discord
MODEL_HIGH=hermes3:8b
MODEL_MEDIUM=qwen2.5:3b
MODEL_LOW=qwen2.5:0.5b
```

## 🎮 Comandos

### Slash Commands
- `/ping` - Verifica latência do bot
- `/perfil` - Mostra estado emocional da Astéria
- `/pesquisar [termo]` - Pesquisa na web e comenta
- `/memorizar [fato]` - Adiciona fato à memória (Admin)
- `/rp [cena]` - Inicia cena de roleplay narrativo
- `/admin modelos` - Lista modelos configurados (Admin)
- `/admin desligar` - Desliga o bot (Admin)

### Interações Automáticas
- **Menção**: `@Astéria` - Responde com Smart Router
- **Reply**: Responder mensagem dela - Continua conversa
- **RP Automático**: Detecta formato RP (`_ _`, `**__L__**`, `—`) e responde automaticamente

## 🎭 Sistema de Roleplay

### Formatação Automática
O bot detecta e responde em estilo narrativo:

**Entrada:**
```
_ _
ㅤㅤㅤ      ' **__M__**ircea surge do salão...
— Bem-vindos.
_ _
```

**Saída:**
```
_ _
ㅤㅤㅤ      ' **__A__**stéria permaneceu em silêncio...
ㅤㅤㅤ      ' **__U__**m sorriso tocou seus lábios...
— Curiosa, realmente.
_ _
```

### Comentários OFF-RP
Use `//` no início para comentários fora do RP:
```
// Vou jantar, volto já
```
→ Astéria ignora completamente

## 📚 Sistema de Fichas de Personagem

### Ingerir Ficha
```bash
python scripts/ingest_character_sheet.py rp_sheets/asteria_base.txt
```

### Ingerir Lorebooks (histórias antigas)
```bash
python scripts/ingest_lorebook.py lorebooks/meu_rp.txt
```

## 🧠 Arquitetura

```
Asteria/
├── src/
│   ├── core/          # Bot principal, config, logger
│   ├── services/      # LLM, Memória RAG, Persona, Busca
│   └── cogs/          # Comandos (General, Admin)
├── rp_sheets/         # Fichas de personagem
├── lorebooks/         # Histórias/lore para memória
├── scripts/           # Scripts de ingestão
└── main.py           # Ponto de entrada
```

### Fluxo de RP
1. Usuário posta cena de RP
2. Bot detecta formato automaticamente
3. Salva na memória RAG (ChromaDB)
4. Busca contexto relevante (fichas, lore)
5. Gera resposta com Hermes 8B
6. Aplica formatação narrativa

## 🛠️ Desenvolvimento

### CLI para testes
```bash
python cli.py
```
Teste a IA diretamente sem Discord.

### Debug
```bash
python debug_bot.py
```
Verifica configuração de Intents.

## 📖 Documentação Adicional

- [GUIA_RP.md](GUIA_RP.md) - Guia completo de roleplay
- [SISTEMA_FICHAS.md](SISTEMA_FICHAS.md) - Sistema de fichas de personagem
- [walkthrough.md](.gemini/antigravity/brain/.../walkthrough.md) - Passo a passo detalhado

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:
1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/NovaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona NovaFeature'`)
4. Push para a branch (`git push origin feature/NovaFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja [LICENSE](LICENSE) para mais detalhes.

## 🙏 Agradecimentos

- [Ollama](https://ollama.ai) - IA local
- [ChromaDB](https://www.trychroma.com/) - Banco vetorial
- [Nextcord](https://nextcord.dev/) - Library Discord
- Comunidade de RP Discord

---

**Feito com 💜 por Yuzuki**
