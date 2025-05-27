from nextcord.ext import commands

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
        await ctx.send("**Comandos disponíveis:**\n" + "\n".join(comandos))
