import os
import asyncio
from nextcord.ext import commands
from config import TOKEN, PREFIX
from events import register_events
from commands import register_commands
import nextcord

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
