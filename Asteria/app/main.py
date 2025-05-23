import os
import asyncio
import nextcord as discord
from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup
import ollama
from typing import Optional

# Função de pesquisa e resumo
def pesquisar_web(termo: str) -> str:
    try:
        with DDGS() as ddgs:
            resultados = list(ddgs.text(termo, region='pt-br', safesearch='moderate', max_results=3))

        if not resultados:
            return "Nenhum resultado encontrado."

        respostas = []
        headers = {"User-Agent": "Mozilla/5.0"}

        for resultado in resultados:
            url = resultado.get("href")
            if url:
                try:
                    response = requests.get(url, headers=headers, timeout=10)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.text, 'html.parser')
                    texto_visivel = ' '.join(soup.stripped_strings)
                    resumo = texto_visivel[:500] + "..." if len(texto_visivel) > 500 else texto_visivel
                    respostas.append(f"🔗 {url}\n📄 {resumo}")
                except requests.RequestException as e:
                    respostas.append(f"🔗 {url}\n❗ Erro ao acessar o conteúdo: {e}")
        return "\n\n".join(respostas)

    except Exception as e:
        return f"Erro ao realizar a pesquisa: {e}"

# Geração do comentário humanizado via Llama3
def gerar_comentario_astéria(termo: str, pesquisa_resultado: str) -> str:
    if len(pesquisa_resultado) > 1000:
        pesquisa_resultado = pesquisa_resultado[:1000] + "..."

    prompt = f"""
Você é Astéria, uma IA Vtuber animada, engraçada e fofa. Acabei de fazer uma pesquisa sobre "{termo}". 
Aqui está o que encontrei:

{pesquisa_resultado}

Agora, comente de forma engraçada, amigável e fofa, como se estivesse explicando ou reagindo ao que leu:
"""
    resposta = ollama.generate(
        model="llama3",
        prompt=prompt,
        options={"temperature": 0.8}
    )
    return resposta["response"]

# Função para enviar textos grandes
async def enviar_resposta(channel, texto: str):
    for i in range(0, len(texto), 1990):
        await channel.send(texto[i:i+1990])

# Configuração do bot
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Bot conectado como {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    content = message.content.strip()

    if content.startswith("!pesquisar "):
        termo = content[len("!pesquisar "):].strip()
        await message.channel.send(f"Pesquisando sobre: **{termo}**...")

        pesquisa_resultado = pesquisar_web(termo)

        if "Nenhum resultado encontrado" in pesquisa_resultado:
            await message.channel.send(pesquisa_resultado)
            return

        await message.channel.send("Processando comentário da Astéria... 🤔💭")
        comentario_astéria = gerar_comentario_astéria(termo, pesquisa_resultado)

        resposta_final = f"**Resultado da pesquisa:**\n{pesquisa_resultado}\n\n**Comentário da Astéria:**\n{comentario_astéria}"
        await enviar_resposta(message.channel, resposta_final)

if __name__ == "__main__":
    TOKEN = os.getenv("DISCORD_BOT_TOKEN")
    if not TOKEN:
        print("Erro: defina a variável DISCORD_BOT_TOKEN com o token do bot")
    else:
        client.run(TOKEN)
