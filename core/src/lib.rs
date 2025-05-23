import os
from ctypes import CDLL, c_char_p
import ollama
from pesquisa import pesquisar_web
from tts import falar_com_emocao
from twitchio.ext import commands

# Define o caminho absoluto para a DLL do Rust (Windows .dll)
lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../core/target/release/libemotion.dll"))

# Carrega a DLL
lib = CDLL(lib_path)

# Define o tipo de retorno da função analyze_emotion
lib.analyze_emotion.restype = c_char_p

def analyze_emotion(text):
    result = lib.analyze_emotion(text.encode("utf-8"))
    return result.decode("utf-8")

# Função para gerar resposta com emoção
def gerar_resposta(texto_usuario):
    emocao = analyze_emotion(texto_usuario)

    prompt = f"""
    [Você é Astéria, uma VTuber {emocao}.]
    [Exemplo de raiva]: "Larga de ser besta, seu retardado! 😾"
    [Exemplo de alegria]: "Aww, você é fofo! 😽"

    Usuário: {texto_usuario}
    Astéria:"""

    resposta = ollama.generate(
        model="llama3-8b-instruct-q4",
        prompt=prompt,
        options={"temperature": 0.7}
    )
    return resposta["response"], emocao

# Bot do Twitch
class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token="SEU_TOKEN_TWITCH", prefix="!", initial_channels=["SEU_CANAL"])

    async def event_message(self, message):
        if message.echo:
            return
        resposta, emocao = gerar_resposta(message.content)
        await message.channel.send(resposta)
        await falar_com_emocao(resposta, emocao)

if __name__ == "__main__":
    bot = Bot()
    bot.run()
