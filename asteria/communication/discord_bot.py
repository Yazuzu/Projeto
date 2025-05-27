"""
Bot Discord usando nextcord para interação com usuários.
"""

import nextcord
from nextcord.ext import commands
from utils.config import DISCORD_TOKEN
from utils.logger import setup_logger

logger = setup_logger()
intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    logger.info(f"Bot conectado como {bot.user} (ID: {bot.user.id})")

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send("Pong!")

def run():
    bot.run(DISCORD_TOKEN)
