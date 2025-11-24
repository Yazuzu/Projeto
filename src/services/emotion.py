from src.services.llm import LLMService

class EmotionService:
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service

    async def analyze(self, text: str) -> str:
        """Analisa a emoção do texto usando o modelo leve do LLMService."""
        return await self.llm.classify_emotion(text)
