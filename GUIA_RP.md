# 🎭 Guia de Roleplay - Asteria Bot

## Sistema de Memória Automática

### Como Funciona
A Astéria detecta **automaticamente** mensagens de RP no Discord e as salva na memória de longo prazo.

**Detecção Automática:**
- Qualquer mensagem que comece e termine com `_ _`
- Mensagens com espaçamento especial `ㅤㅤㅤ`
- Mensagens com formatação `**__L__**etter`

Quando detectado, a mensagem é salva instantaneamente no ChromaDB com metadados (autor, canal, timestamp).

### O que é RAG (Retrieval-Augmented Generation)?
**RAG** = A Astéria busca automaticamente memórias relevantes e as usa como "conhecimento de fundo" ao responder.

**Como ela usa a memória:**
✅ **SIM:** "Mircea é o regente, então vou responder com respeito à hierarquia"
✅ **SIM:** "Ancalagon tem duas cabeças, vou mencionar isso na minha descrição"
❌ **NÃO:** Copiar descrições antigas palavra por palavra
❌ **NÃO:** Reciclar diálogos antigos

## Comandos de RP

### `/rp cena: [sua ação]`
**Modo Roleplay Narrativo**

Força a Astéria a responder em estilo literário épico, usando:
- Modelo **Hermes 8B** (o mais pesado e criativo)
- Formatação Discord exata (espaçamento, `**__L__**`, travessões `—`)
- Busca automática de contexto na memória

**Exemplo:**
```
/rp cena: Astéria adentra o salão, seus olhos brilhando
```

**Resposta esperada:**
```
_ _
ㅤㅤㅤ      ' **__A__** figura esbelta de Astéria materializou-se no limiar do salão, como se tivesse sido tecida pelas próprias sombras...

— Saudações, nobres presentes.
_ _
```

### `/memorizar fato: [texto]`
**(Apenas para o criador)**

Adiciona manualmente um fato importante à memória permanente.

**Exemplo:**
```
/memorizar fato: O Reino de Vhaltor foi destruído em 1523
```

### `/perfil`
Mostra o estado emocional atual da Astéria (Valência, Ativação, Dominância, etc.)

## Otimizações Implementadas

### 1. Limite de Memórias Recuperadas
- Busca apenas as **3 memórias mais relevantes**
- Cada memória truncada em **300 caracteres** (evita sobrecarga de contexto)

### 2. ChromaDB (Banco Vetorial)
- **Espaço:** Texto é incrivelmente leve (anos de RP = poucos MBs)
- **Velocidade:** Busca semântica em milissegundos, mesmo com milhões de entradas
- **Persistente:** Dados salvos em `/home/yuzuki/Projeto/Asteria/data/memory/`

### 3. Arquivos `.txt` são Descartáveis
- Use `lorebooks/*.txt` para **ingestão inicial** com o script
- Depois de rodar `python scripts/ingest_lorebook.py`, pode deletar ou arquivar o `.txt`
- Os dados reais estão no ChromaDB

## Ingestão Manual de Lorebooks

Se você tiver arquivos grandes de RP para adicionar:

1. **Coloque o arquivo em** `lorebooks/meu_rp.txt`
2. **Rode o script:**
   ```bash
   python scripts/ingest_lorebook.py lorebooks/meu_rp.txt
   ```
3. **Pronto!** A memória foi alimentada.

## Fluxo Completo de RP

1. **Você ou seus amigos** postam ações de RP no Discord
2. **Astéria detecta** automaticamente (formato `_ _`)
3. **Salva na memória** com autor, canal e timestamp
4. **Quando alguém usa** `/rp` ou menciona ela:
   - Ela busca as 3 memórias mais relevantes
   - Usa como contexto de mundo
   - **Cria uma resposta nova e original**

## Anti-Anti-RP (Garantia de Criatividade)

**Problema:** IAs podem copiar textos da memória (quebra a imersão)

**Solução Implementada:**
- Instruções explícitas: "Use memória como contexto, NÃO copie"
- Truncamento de memórias (evita textos longos que incentivam cópia)
- Aviso no prompt: "⚠️ Crie respostas NOVAS e ORIGINAIS"

## Dicas de Uso

### Para Melhor Imersão:
- Use `/rp` para cenas importantes (qualidade máxima)
- Mencione personagens conhecidos (Mircea, Ancalagon) - ela vai reconhecer via RAG
- Seja descritivo nas ações para receber respostas igualmente ricas

### Para Gerenciar Memória:
- Todo RP formatado é salvo automaticamente (você não precisa fazer nada)
- Use `/memorizar` apenas para fatos cruciais (ex: regras de mundo, eventos chave)
- A memória nunca "fica pesada" - ChromaDB é otimizado para escala

## Troubleshooting

**"Ela está copiando descrições antigas!"**
- Reporte para o criador ajustar o peso da instrução anti-cópia
- Verifique se o Modelo High (Hermes 8B) está ativo (`/admin modelos`)

**"Ela não lembra de algo que foi dito há 2 dias!"**
- Verifique se a mensagem foi salva (deve ter log `📚 RP salvo automaticamente`)
- Inspecione o banco: Total de memórias aparece quando o bot inicia

**"O bot está lento ao responder em RP!"**
- Normal: Hermes 8B é o modelo mais pesado (alta qualidade = mais tempo)
- Tempo esperado: 10-30 segundos dependendo do tamanho da resposta
