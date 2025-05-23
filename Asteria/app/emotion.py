from ctypes import CDLL, c_char_p
import os

# Caminho absoluto para a DLL compilada pelo Rust
lib_path = os.path.abspath(r"C:\Users\ybren\Projeto\core\target\release\emotion.dll")
lib = CDLL(lib_path)

# Define o tipo de retorno da função analyze_emotion
lib.analyze_emotion.restype = c_char_p

def analyze_emotion(text: str) -> str:
    """Chama a DLL Rust para analisar a emoção no texto."""
    resultado = lib.analyze_emotion(text.encode("utf-8"))
    return resultado.decode("utf-8")
