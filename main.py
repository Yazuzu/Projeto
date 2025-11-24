import os
from src.core.config import settings
from src.core.bot import AsteriaBot
from src.core.logger import setup_logger

logger = setup_logger(__name__)

def main():
    if not settings.DISCORD_BOT_TOKEN:
        logger.error("❌ Token do bot não encontrado! Verifique o arquivo .env")
        return

    bot = AsteriaBot()
    
    try:
        bot.run(settings.DISCORD_BOT_TOKEN)
    except Exception as e:
        logger.critical(f"Erro fatal ao iniciar o bot: {e}")

if __name__ == "__main__":
    main()
