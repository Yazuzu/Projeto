import os

project_structure = {
    "main.py": '''import asyncio
import nextcord
from nextcord.ext import commands
from config import TOKEN, PREFIX
from events import register_events
from commands import register_commands

intents = nextcord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

async def main():
    register_events(bot)
    register_commands(bot)
    await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
''',

    "config.py": '''import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = os.getenv("COMMAND_PREFIX", "!")
''',

    "commands.py": '''from nextcord.ext import commands

def register_commands(bot: commands.Bot):
    
    @bot.command(name="ping")
    async def ping(ctx):
        await ctx.send(f"Pong! Latência: {round(bot.latency * 1000)}ms")
    
    @bot.command(name="ajuda")
    async def ajuda(ctx):
        comandos = [
            "`ping` - Testa latência",
            "`ajuda` - Mostra comandos disponíveis",
        ]
        await ctx.send("**Comandos disponíveis:**\\n" + "\\n".join(comandos))
''',

    "events.py": '''from nextcord import Message

def register_events(bot):
    
    @bot.event
    async def on_ready():
        print(f"Bot conectado como {bot.user} (ID: {bot.user.id})")

    @bot.event
    async def on_message(message: Message):
        if message.author == bot.user:
            return
        await bot.process_commands(message)
''',

    "ai_module.py": '''from sentence_transformers import SentenceTransformer

class AIModel:
    def __init__(self):
        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    
    def encode(self, text):
        return self.model.encode(text)

ai = AIModel()
''',

    "memory_manager.py": '''import aiosqlite
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
''',

    "utils.py": '''import asyncio

async def run_blocking_io(func, *args):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, func, *args)
''',

    ".env": '''DISCORD_TOKEN=seu_token_aqui
COMMAND_PREFIX=!
'''
}

def create_files(structure: dict):
    for filename, content in structure.items():
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[+] Arquivo '{filename}' criado/substituído com sucesso.")

if __name__ == "__main__":
    create_files(project_structure)
