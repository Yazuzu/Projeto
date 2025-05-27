import os
import subprocess
import shutil
from youtubesearchpython import VideosSearch
from faster_whisper import WhisperModel
import noisereduce as nr
import soundfile as sf
from pydub import AudioSegment

# Configurações
PERSONAGEM = "Tanya Degurechaff voice lines"
OUTPUT_DIR = "dataset_tanya"
TEMP_DIR = os.path.join(OUTPUT_DIR, "temp")
PROCESSED_DIR = os.path.join(OUTPUT_DIR, "processed")

for lang in ['ja', 'en']:
    os.makedirs(os.path.join(PROCESSED_DIR, lang), exist_ok=True)

os.makedirs(TEMP_DIR, exist_ok=True)

# Pesquisa vídeos
print(f"[INFO] Pesquisando vídeos de: {PERSONAGEM}")
videosSearch = VideosSearch(PERSONAGEM, limit=10)
results = videosSearch.result()['result']
video_urls = [video['link'] for video in results]
print(f"[INFO] URLs encontradas: {video_urls}")

# Baixa vídeos em .wav
for url in video_urls:
    print(f"[INFO] Baixando: {url}")
    subprocess.run([
        'yt-dlp',
        '-f', 'bestaudio',
        '--extract-audio',
        '--audio-format', 'wav',
        '-o', os.path.join(TEMP_DIR, '%(title)s.%(ext)s'),
        url
    ])

# Modelo de transcrição
model = WhisperModel("base", device="cpu")

for filename in os.listdir(TEMP_DIR):
    if not filename.endswith(".wav"):
        continue

    audio_path = os.path.join(TEMP_DIR, filename)
    print(f"[INFO] Transcrevendo: {audio_path}")

    segments, info = model.transcribe(audio_path)
    detected_lang = info.language
    print(f"[INFO] Idioma detectado: {detected_lang}")

    if detected_lang not in ['ja', 'en']:
        print(f"[INFO] Ignorando {filename}, idioma não suportado.")
        os.remove(audio_path)
        continue

    # Separar voz com Demucs
    print(f"[INFO] Separando voz com Demucs: {filename}")
    subprocess.run(['demucs', audio_path])

    sep_dir = os.path.join('separated', 'htdemucs', filename[:-4])
    vocals_path = os.path.join(sep_dir, 'vocals.wav')

    if not os.path.exists(vocals_path):
        print(f"[WARNING] Separação falhou: {filename}")
        continue

    # Pré-processamento: reduzir para mono e 16kHz
    print(f"[INFO] Convertendo para mono e 16kHz: {vocals_path}")
    sound = AudioSegment.from_wav(vocals_path)
    sound = sound.set_channels(1)
    sound = sound.set_frame_rate(16000)
    sound.export(vocals_path, format="wav")

    # Redução de ruído
    print(f"[INFO] Reduzindo ruído: {vocals_path}")
    data, rate = sf.read(vocals_path)
    reduced_noise = nr.reduce_noise(y=data, sr=rate)
    clean_filename = f'clean_{filename}'
    clean_path = os.path.join(PROCESSED_DIR, detected_lang, clean_filename)
    sf.write(clean_path, reduced_noise, rate)

    print(f"[INFO] Processado e movido: {clean_path}")

    # Limpeza
    os.remove(audio_path)
    shutil.rmtree(sep_dir, ignore_errors=True)

print("[INFO] Pipeline completo: Download → Separação (Demucs) → Conversão → Ruído → Classificação bilíngue.")
