"""
Bot principal da Astéria.
"""
import nextcord as discord
import asyncio
from emotion.emotion import analyze_emotion
from memory.memory_manager import adicionar_memoria, buscar_contexto
from web.web_search import pesquisar_web
from rp.rp_utils import detectar_encenacao, aplicar_estilo_rp, quebrar_narracao_rp, enviar_resposta_com_quebra
from model.model_router import roteador_modelo
from utils.utils import salvar_interacao
from utils.config import DISCORD_TOKEN, CREATOR_ID
from utils.logger import setup_logger

logger = setup_logger()
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    logger.info(f"Bot conectado! Nome: {client.user} - ID: {client.user.id}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    is_creator = message.author.id == CREATOR_ID
    content = message.content.strip()

    if not client.user.mentioned_in(message) and "astéria" not in content.lower():
        return

    if content.startswith("!pesquisar "):
        termo = content[len("!pesquisar "):].strip()
        await message.channel.send(f"Pesquisando sobre {termo}...")
        resultado = await pesquisar_web(termo)
        comentario = roteador_modelo(f"Pesquisei '{termo}':\n{resultado}")
        await enviar_resposta_com_quebra(message.channel, f"Resultado:\n{resultado}\n\n{comentario}")
        return

    contextos = buscar_contexto(content)
    contexto = "\n".join(contextos) if contextos else "Sem contexto anterior."
    emocao = await analyze_emotion(content)
    prompt = f"Mensagem do usuário: {content}\n\nContexto: {contexto}\n\nEmoção detectada: {emocao}"
    resposta = roteador_modelo(prompt)

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
    client.run(DISCORD_TOKEN)
