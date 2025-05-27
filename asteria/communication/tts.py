"""
Text-to-Speech para respostas faladas.
"""

import pyttsx3

engine = pyttsx3.init()

def falar(texto):
    engine.say(texto)
    engine.runAndWait()
