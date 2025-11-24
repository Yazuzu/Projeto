import nextcord
from nextcord.ext import commands
from src.core.bot import AsteriaBot
from src.core.config import settings

class AdminCog(commands.Cog):
    def __init__(self, bot: AsteriaBot):
        self.bot = bot

    def is_creator(self, user_id: int):
        return user_id == settings.CREATOR_ID

    @nextcord.slash_command(name="admin", description="Comandos administrativos (Apenas Criador)")
    async def admin(self, interaction: nextcord.Interaction):
        pass  # Comando pai para subcomandos

    @admin.subcommand(name="desligar", description="Desliga o bot")
    async def desligar(self, interaction: nextcord.Interaction):
        """Desliga o bot (Apenas criador)."""
        if not self.is_creator(interaction.user.id):
            await interaction.response.send_message("❌ Você não tem permissão para isso.", ephemeral=True)
            return
            
        await interaction.response.send_message("👋 Desligando... Até logo!")
        await self.bot.close()

    @admin.subcommand(name="modelos", description="Lista os modelos de IA configurados")
    async def modelos(self, interaction: nextcord.Interaction):
        """Lista os modelos configurados."""
        msg = (
            f"**Configuração de Modelos:**\n"
            f"🚀 **Alta (Roleplay):** `{self.bot.llm.models['high']}`\n"
            f"⚖️ **Média (Chat):** `{self.bot.llm.models['medium']}`\n"
            f"🪶 **Baixa (Rápido):** `{self.bot.llm.models['low']}`"
        )
        await interaction.response.send_message(msg)

def setup(bot: AsteriaBot):
    bot.add_cog(AdminCog(bot))
