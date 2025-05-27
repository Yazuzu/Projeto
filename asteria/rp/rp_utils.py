"""
Funções de roleplay: detecção, estilo e envio.
"""
import random
import textwrap

MAX_DISCORD_MSG = 1900

def detectar_encenacao(mensagem):
    msg = mensagem.strip()
    return msg.startswith("*") or (msg.count("*") >= 2 and "*" in msg)

def aplicar_estilo_rp(resposta):
    prefixos = [
        "Ah, humano tolo! ",
        "Hehe, você ousa me desafiar? ",
        "Como uma verdadeira Vtuber provocadora, eu digo: ",
        "Ouça bem, mortal: ",
        "Astéria, a poderosa, responde: "
    ]
    return random.choice(prefixos) + resposta

def quebrar_narracao_rp(resposta):
    partes = resposta.split("//")
    narracao = partes[0].strip()
    comentarios = [p.strip() for p in partes[1:]]
    return narracao, comentarios

async def enviar_resposta_com_quebra(channel, texto):
    for parte in textwrap.wrap(texto, width=MAX_DISCORD_MSG, replace_whitespace=False):
        await channel.send(parte)
