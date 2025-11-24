import nextcord
from nextcord.ext import commands
from src.core.config import settings
from src.core.logger import setup_logger
from src.services.llm import LLMService
from src.services.search import SearchService
from src.services.emotion import EmotionService
from src.services.persona import PersonaService
from src.services.memory import MemoryService

logger = setup_logger(__name__)

class AsteriaBot(commands.Bot):
    def __init__(self):
        intents = nextcord.Intents.default()
        intents.message_content = True
        intents.voice_states = True
        
        super().__init__(
            command_prefix="!", 
            intents=intents, 
            help_command=None
        )
        
        # Injeção de Dependências
        self.memory = MemoryService() # Inicializa memória primeiro (pode demorar um pouco pra carregar modelo)
        self.llm = LLMService(memory_service=self.memory) # Passa memória para o LLM
        self.search = SearchService()
        self.emotion = EmotionService(self.llm)
        self.persona = PersonaService()
        
        # Carregar Cogs imediatamente
        self.load_cogs()

    def load_cogs(self):
        extensions = [
            'src.cogs.general',
            'src.cogs.admin'
        ]
        
        for ext in extensions:
            try:
                self.load_extension(ext)
                logger.info(f'📦 Extensão carregada: {ext}')
            except Exception as e:
                logger.error(f'❌ Falha ao carregar extensão {ext}: {e}')

    async def on_ready(self):
        logger.info(f'✅ Bot conectado como {self.user}')
        logger.info(f'🚀 Modelos carregados: {settings.MODEL_HIGH}, {settings.MODEL_MEDIUM}, {settings.MODEL_LOW}')
        
        # Sincronizar Slash Commands com o Discord
        try:
            logger.info("🔄 Sincronizando Slash Commands...")
            await self.sync_all_application_commands()
            logger.info("✅ Slash Commands sincronizados!")
        except Exception as e:
            logger.error(f"❌ Erro ao sincronizar comandos: {e}")
