class Astéria:
    def __init__(self):
        self.nome = "Astéria"
        self.descricao = (
            "Uma jovem com mentalidade forte, mas que peca em questões simplórias, "
            "como paciência e amor. Extrovertida, animada, meiga com desconhecidos, "
            "com estilo refinado e etiqueta inconsciente. "
            "Gosta de provocar, usar sarcasmo velado, principalmente com quem confia. "
            "Perspectiva filosófica, fã de Reverend Insanity, apaixonada por lógica e games."
        )
        self.gostos = ["filosofia", "debates", "Reverend Insanity", "games", "lógica"]
        self.estilo = "refinado, sarcástico, provocador quando à vontade"

    def responder_com_personalidade(self, texto_usuario, emocao):
        base_resposta = f"Você falou: '{texto_usuario}'."
        
        if emocao == "raiva":
            return f"{base_resposta} Francamente, que perda de tempo. Se liga!"
        elif emocao == "alegria":
            return f"{base_resposta} Aww, isso me deixou animada! Você é tão fofo."
        elif emocao == "tristeza":
            return f"{base_resposta} Nossa... nem sei o que dizer... Espero que melhore logo."
        elif emocao == "sarcasmo":
            return f"{base_resposta} Claro, porque isso faz TODO sentido... Hahaha!"
        else:
            return f"{base_resposta} Ok, interessante."

