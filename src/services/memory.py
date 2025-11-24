import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import uuid
from typing import List, Dict
from src.core.logger import setup_logger

logger = setup_logger(__name__)

class MemoryService:
    def __init__(self, persist_directory: str = "./data/memory"):
        self.persist_directory = persist_directory
        
        # Inicializa ChromaDB
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Inicializa modelo de embeddings (leve e rápido)
        logger.info("🧠 Carregando modelo de embeddings (all-MiniLM-L6-v2)...")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Cria ou recupera a coleção
        self.collection = self.client.get_or_create_collection(name="asteria_memory")
        logger.info(f"📚 Memória carregada. Total de memórias: {self.collection.count()}")

    def add_memory(self, text: str, metadata: Dict = None):
        """Adiciona uma nova memória ao banco."""
        if metadata is None:
            metadata = {"source": "user_input", "type": "fact"}
            
        # Gera embedding
        embedding = self.embedding_model.encode(text).tolist()
        
        # Salva no Chroma
        self.collection.add(
            documents=[text],
            embeddings=[embedding],
            metadatas=[metadata],
            ids=[str(uuid.uuid4())]
        )
        logger.info(f"💾 Memória salva: '{text[:50]}...'")

    def search_memory(self, query: str, limit: int = 3) -> List[str]:
        """Busca memórias semanticamente relevantes."""
        query_embedding = self.embedding_model.encode(query).tolist()
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=limit
        )
        
        if results and results['documents']:
            return results['documents'][0]
        return []

    def forget_memory(self, term: str):
        """Remove memórias que contenham o termo (busca simples por texto)."""
        # Nota: Chroma não suporta delete por 'contains' nativo facilmente sem metadata,
        # mas podemos buscar e deletar os IDs retornados.
        results = self.collection.get(where_document={"$contains": term})
        
        if results and results['ids']:
            self.collection.delete(ids=results['ids'])
            logger.info(f"🗑️ {len(results['ids'])} memórias removidas contendo '{term}'.")
            return len(results['ids'])
        return 0
