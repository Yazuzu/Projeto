import os
import asyncio
import nextcord as discord
from ctypes import CDLL, c_char_p
import ollama
from tts import falar_com_emocao
from dotenv import load_dotenv
import textwrap

load_dotenv()

# Carregue DLL de emoção, caminho pode ser variável de ambiente
lib_path = os.getenv("EMOTION_DLL_PATH", r"C:\Users\ybren\Projeto\core\target\release\emotion.dll")

if not os.path.exists(lib_path):
    raise FileNotFoundError(f"Não encontrei a DLL de emoção em: {lib_path}")

lib = CDLL(lib_path)
lib.analyze_emotion.restype = c_char_p

def analyze_emotion(text):
    try:
        result = lib.analyze_emotion(text.encode("utf-8"))
        return result.decode("utf-8")
    except Exception as e:
        print(f"Erro ao analisar emoção: {e}")
        return "neutra"

CREATOR_ID = int(os.getenv("CREATOR_ID", "766317071369109544"))

def gerar_prompt(texto_usuario, emocao, is_creator):
    criador_texto = ""
    if is_creator:
        criador_texto = ("A pessoa que está falando é o seu criador, que você chama carinhosamente "
                         "'Yuzuki'. Trate-o com respeito, mas que goste de o provocar e brincar com ele.\n")

    prompt = f"""
    Você é Astéria, uma garota que responde com emoção {emocao}.
    {criador_texto}
    Exemplos de respostas:
    - Se estiver raiva, diga algo como: "Larga de ser besta, seu retardado!"
    - Se estiver alegria, diga algo como: "Aww, você é fofo!"

    Agora, responda de forma natural e amigável:
    Usuário: {texto_usuario}
    Astéria:"""
    
    return textwrap.dedent(prompt)

def gerar_resposta(texto_usuario, is_creator=False):
    emocao = analyze_emotion(texto_usuario)
    prompt = gerar_prompt(texto_usuario, emocao, is_creator)
    try:
        resposta = ollama.generate(
            model="llama3",
            prompt=prompt,
            options={"temperature": 0.7}
        )
        return resposta["response"], emocao
    except Exception as e:
        print(f"Erro ao gerar resposta: {e}")
        return "Desculpe, não consegui pensar em uma resposta agora.", emocao

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Bot conectado como {client.user}')

@client.event
async def on_error(event, *args, **kwargs):
    print(f"Erro no evento {event}:")
    import traceback
    traceback.print_exc()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    is_creator = (message.author.id == CREATOR_ID)
    content = message.content.strip()

    if content.startswith("!sair") and is_creator:
        await message.channel.send("Saindo do servidor... Até logo!")
        await message.guild.leave()
        return

    if content.startswith("!falar "):
        if not is_creator:
            await message.channel.send("Somente meu criador pode usar esse comando.")
            return

        texto_falar = content[len("!falar "):].strip()
        if not texto_falar:
            await message.channel.send("Por favor, forneça o texto para eu falar.")
            return

        resposta, emocao = gerar_resposta(texto_falar, is_creator)

        caminho_audio = await falar_com_emocao(resposta, emocao)

        if caminho_audio and os.path.exists(caminho_audio):
            await message.channel.send(resposta)
            await message.channel.send(file=discord.File(caminho_audio))

            member = message.guild.get_member(message.author.id) if message.guild else None

            if member and member.voice and member.voice.channel:
                try:
                    vc = discord.utils.get(client.voice_clients, guild=message.guild)
                    if not vc or not vc.is_connected():
                        vc = await member.voice.channel.connect()
                    elif vc.channel != member.voice.channel:
                        await vc.move_to(member.voice.channel)

                    if not vc.is_playing():
                        vc.play(discord.FFmpegPCMAudio(caminho_audio))

                        while vc.is_playing():
                            await asyncio.sleep(1)
                        if vc.is_connected():
                            await vc.disconnect()
                    else:
                        await message.channel.send("Já estou tocando algo no canal de voz!")
                except Exception as e:
                    await message.channel.send(f"Erro ao reproduzir áudio: {e}")
            else:
                await message.channel.send("Entre em um canal de voz para eu poder falar por lá!")

            os.remove(caminho_audio)
        else:
            await message.channel.send("Erro ao gerar áudio :(")
        return

    resposta, _ = gerar_resposta(content, is_creator)
    await message.channel.send(resposta)

if __name__ == "__main__":
    TOKEN = os.getenv("DISCORD_BOT_TOKEN")
    if not TOKEN:
        print("Erro: defina a variável DISCORD_BOT_TOKEN no .env")
    else:
        client.run(TOKEN)
