from TTS.api import TTS
import asyncio

tts = TTS(model_name="tts_models/pt/cv/vits")

async def falar_com_emocao(texto, emocao):
    caminho_audio = "resposta.wav"
    
    # Parâmetros para deixar a voz mais feminina e fluída
    speed = 0.9           # reduz um pouco a velocidade para soar mais natural
    speaker_idx = 0       # índice do speaker, pode variar para mudar voz (teste outros)
    noise_scale = 0.6     # controla a naturalidade, valores entre 0.5 e 0.8 funcionam bem
    
    # Chamada de síntese com parâmetros personalizados
    tts.tts_to_file(
        text=texto,
        speaker=speaker_idx,
        speed=speed,
        noise_scale=noise_scale,
        file_path=caminho_audio
    )
    
    return caminho_audio
