import whisper

# Carrega o modelo de transcrição do Whisper.
# Modelos disponíveis: tiny, base, small, medium, large
# Para velocidade, recomendo "base" ou "small".
model = whisper.load_model("base")

def transcrever_audio(caminho_audio):
    try:
        result = model.transcribe(caminho_audio, fp16=False)
        texto = result['text']
        print(f"[INFO] Transcrição: {texto}")
        return texto
    except Exception as e:
        print(f"[ERRO] Falha na transcrição: {e}")
        return None
