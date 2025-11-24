import nextcord
from nextcord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Diagnóstico conectado como {bot.user}")
    print("ℹ️  Envie uma mensagem em qualquer canal que o bot tenha acesso.")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    print(f"📩 Mensagem recebida: '{message.content}'")
    print(f"   Autor: {message.author}")
    print(f"   Canal: {message.channel}")
    
    if not message.content:
        print("⚠️  ALERTA: Conteúdo da mensagem vazio! 'Message Content Intent' provavelmente está DESATIVADO no Developer Portal.")
    else:
        print("✅  Conteúdo visível. Intents parecem estar configurados corretamente.")
        await message.channel.send(f"Diagnóstico: Recebi sua mensagem: '{message.content}'")

if __name__ == "__main__":
    if not TOKEN:
        print("❌ Token não encontrado no .env")
    else:
        print("🔄 Iniciando diagnóstico...")
        bot.run(TOKEN)
