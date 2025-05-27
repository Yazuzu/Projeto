import aiosqlite
import numpy as np
import faiss

class MemoryManager:
    def __init__(self, db_path="bot.db"):
        self.db_path = db_path
        self.index = faiss.IndexFlatL2(384)
        self.phrases = []

    async def init_db(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS memoria (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    frase TEXT,
                    embedding BLOB
                )
            """)
            await db.commit()

    async def load_memory(self):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT frase, embedding FROM memoria") as cursor:
                rows = await cursor.fetchall()

        embeddings = []
        for frase, emb_blob in rows:
            self.phrases.append(frase)
            if emb_blob:
                emb = np.frombuffer(emb_blob, dtype=np.float32)
                embeddings.append(emb)

        if embeddings:
            self.index.add(np.vstack(embeddings))
    
    async def add_memory(self, frase, embedding):
        emb_blob = np.array(embedding, dtype=np.float32).tobytes()
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("INSERT INTO memoria (frase, embedding) VALUES (?, ?)", (frase, emb_blob))
            await db.commit()

        self.phrases.append(frase)
        self.index.add(np.array([embedding], dtype=np.float32))

memory_manager = MemoryManager()
