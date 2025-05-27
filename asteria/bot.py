import nextcord as discord
import asyncio
import os
from emotion import analyze_emotion
from memory_manager import adicionar_memoria, buscar_contexto
from web_search import pesquisar_web
from rp_utils import detectar_encenacao, aplicar_estilo_rp, quebrar_narracao_rp, enviar_resposta_com_quebra
from model_router import roteador_modelo
from utils import salvar_interacao

TOKEN = os.getenv("DISCORD_TOKEN")
CREATOR_ID = int(os.getenv("CREATOR_ID", "0"))

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Bot conectado! Nome: {client.user} - ID: {client.user.id}")

@client.event
async def on_member_join(member):
    canal = discord.utils.get(member.guild.text_channels, name="geral")
    if canal:
        await canal.send(f"Bem-vindo, {member.name}! Eu sou a Astéria, sua Vtuber provocadora!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    is_creator = message.author.id == CREATOR_ID
    content = message.content.strip()

    # Ignorar mensagens sem menção e sem "astéria"
    if not client.user.mentioned_in(message) and "astéria" not in content.lower():
        return

    # Comando pesquisar
    if content.startswith("!pesquisar "):
        termo = content[len("!pesquisar "):].strip()
        await message.channel.send(f"Pesquisando sobre {termo}...")
        resultado = await pesquisar_web(termo)
        comentario = roteador_modelo(f"Pesquisei '{termo}':\n{resultado}")
        await enviar_resposta_com_quebra(message.channel, f"Resultado:\n{resultado}\n\n{comentario}")
        return

    # Buscar contexto para prompt
    contextos = buscar_contexto(content)
    contexto = "\n".join(contextos) if contextos else "Sem contexto anterior."

    # Detecta emoção
    emocao = await analyze_emotion(content)
    prompt = f"Mensagem do usuário: {content}\n\nContexto: {contexto}\n\nEmoção detectada: {emocao}"
    resposta = roteador_modelo(prompt)

    # Detecta se deve entrar no modo encenação
    if detectar_encenacao(content):
        resposta = aplicar_estilo_rp(resposta)

    narracao, comentarios = quebrar_narracao_rp(resposta)

    await enviar_resposta_com_quebra(message.channel, narracao)

    for c in comentarios:
        await enviar_resposta_com_quebra(message.channel, f"//Astéria\n//{c}")

    salvar_interacao(message.author.name, content, resposta, contexto)
    adicionar_memoria(content)

if __name__ == "__main__":
    print("Iniciando bot...")
    client.run(TOKEN)
