from TTS.api import TTS

# Inicializa o modelo Coqui TTS para português brasileiro (modelo de voz neutra)
tts = TTS(model_name="tts_models/pt/cv/vits")

def testar_vozes(texto):
    speed = 80   # velocidade em %, 100 é normal
    noise = 50   # nível de ruído, ajusta naturalidade

    arquivo_saida = "resposta.wav"
    print(f"Gerando áudio: {arquivo_saida}")
    tts.tts_to_file(
        text=texto,
        file_path=arquivo_saida,
        speed=speed / 100,
        noise_scale=noise / 100,
    )
    print("Áudio gerado com sucesso.")

if __name__ == "__main__":
    texto_teste = "Olá! Estou testando minha voz neutra e natural."
    testar_vozes(texto_teste)
