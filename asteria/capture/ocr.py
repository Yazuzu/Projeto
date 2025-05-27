"""
Extração de texto da imagem usando OCR.
"""

import pytesseract
from PIL import Image

def extrair_texto(imagem: Image.Image) -> str:
    texto = pytesseract.image_to_string(imagem)
    return texto
