"""
Gerencia o contexto da conversa, memória e histórico.
"""

class ContextManager:
    def __init__(self):
        self.historico = []

    def adicionar(self, mensagem):
        self.historico.append(mensagem)

    def obter_contexto(self, limite=5):
        return self.historico[-limite:]
