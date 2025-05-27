"""
Integração com DLL para análise emocional.
"""
from ctypes import CDLL, c_char_p
import os

LIB_PATH = os.getenv("EMOTION_DLL_PATH", "path_to_emotion.dll")
lib = CDLL(LIB_PATH)
lib.analyze_emotion.restype = c_char_p

async def analyze_emotion(text: str) -> str:
    result = lib.analyze_emotion(text.encode("utf-8"))
    return result.decode("utf-8")
