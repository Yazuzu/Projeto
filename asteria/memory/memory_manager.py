"""
Gerencia memória vetorial com FAISS e embeddings.
"""
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

modelo_embedding = SentenceTransformer('paraphrase-MiniLM-L6-v2')
index = faiss.IndexFlatL2(384)
base_frases = []

def adicionar_memoria(frase):
    emb = modelo_embedding.encode([frase])
    index.add(np.array(emb, dtype=np.float32))
    base_frases.append(frase)

def buscar_contexto(frase, k=3):
    if len(base_frases) == 0:
        return []
    emb = modelo_embedding.encode([frase])
    D, I = index.search(np.array(emb, dtype=np.float32), k)
    return [base_frases[i] for i in I[0] if i < len(base_frases)]
