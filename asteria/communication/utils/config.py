import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "seu_token_aqui")
CREATOR_ID = int(os.getenv("CREATOR_ID", 0))
EMOTION_DLL_PATH = os.getenv("EMOTION_DLL_PATH", "path_to_emotion.dll")
