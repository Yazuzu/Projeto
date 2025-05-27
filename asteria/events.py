from nextcord import Message

def register_events(bot):
    
    @bot.event
    async def on_ready():
        print(f"Bot conectado como {bot.user} (ID: {bot.user.id})")

    @bot.event
    async def on_message(message: Message):
        if message.author == bot.user:
            return
        await bot.process_commands(message)
