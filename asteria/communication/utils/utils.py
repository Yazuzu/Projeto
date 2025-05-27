"""
Funções utilitárias diversas.
"""
import json
import datetime

def salvar_interacao(usuario, mensagem, resposta, contexto):
    registro = {
        "timestamp": datetime.datetime.now().isoformat(),
        "usuario": usuario,
        "mensagem": mensagem,
        "resposta": resposta,
        "contexto": contexto
    }
    with open("historico_interacoes.json", "a", encoding="utf-8") as f:
        f.write(json.dumps(registro, ensure_ascii=False) + "\n")
