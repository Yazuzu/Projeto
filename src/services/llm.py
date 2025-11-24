import ollama
import asyncio
from typing import List, Dict, Optional, Literal
from collections import deque
from src.core.config import settings
from src.core.logger import setup_logger

logger = setup_logger(__name__)

ModelTier = Literal["high", "medium", "low"]

class LLMService:
    def __init__(self, memory_service=None):
        self.models = {
            "high": settings.MODEL_HIGH,
            "medium": settings.MODEL_MEDIUM,
            "low": settings.MODEL_LOW
        }
        self.memory_service = memory_service
        # Memória de curto prazo: mapeia user_id -> deque de mensagens
        self.memory: Dict[int, deque] = {}
        self.max_memory_len = 10  # Lembra das últimas 10 trocas

    def _get_model(self, tier: ModelTier) -> str:
        return self.models.get(tier, self.models["medium"])

    def _update_memory(self, user_id: int, role: str, content: str):
        if user_id not in self.memory:
            self.memory[user_id] = deque(maxlen=self.max_memory_len)
        self.memory[user_id].append({"role": role, "content": content})

    def _get_context(self, user_id: int) -> List[Dict[str, str]]:
        if user_id in self.memory:
            return list(self.memory[user_id])
        return []

    async def generate_response(
        self, 
        prompt: str, 
        user_id: int, 
        system_prompt: str, 
        tier: ModelTier = "medium",
        temperature: Optional[float] = None
    ) -> str:
        model = self._get_model(tier)
        
        # RAG: Busca memórias relevantes se o serviço estiver disponível
        rag_context = ""
        if self.memory_service:
            try:
                # Busca as 3 memórias mais relevantes (otimização)
                memories = self.memory_service.search_memory(prompt, limit=3)
                if memories:
                    rag_context = "\n# CONHECIMENTO DE CONTEXTO (use como referência, NÃO copie)\n"
                    for i, mem in enumerate(memories, 1):
                        # Trunca memórias muito longas (máx 300 chars cada)
                        truncated = mem[:300] + "..." if len(mem) > 300 else mem
                        rag_context += f"{i}. {truncated}\n"
                    rag_context += "\n⚠️ Use este conhecimento apenas para CONTEXTO. Crie respostas NOVAS e ORIGINAIS.\n"
            except Exception as e:
                logger.error(f"Erro ao buscar memória RAG: {e}")

        # Constrói o histórico de mensagens para o contexto
        full_system_prompt = system_prompt + rag_context
        messages = [{"role": "system", "content": full_system_prompt}]
        messages.extend(self._get_context(user_id))
        messages.append({"role": "user", "content": prompt})

        # Configurações de temperatura baseadas no tier
        if temperature is None:
            if tier == "high":
                temperature = 0.8  # Criativo (Roleplay)
            elif tier == "low":
                temperature = 0.2  # Preciso (Classificação)
            else:
                temperature = 0.7  # Equilibrado

        try:
            logger.info(f"⏳ Gerando resposta com modelo {model} ({tier})...")
            
            # Configuração de geração
            options = {
                "temperature": temperature,
                "num_predict": 1024 if tier == "high" else 512  # RP (high) = mais longo
            }
            
            response = await asyncio.to_thread(
                ollama.chat,
                model=model,
                messages=messages,
                options=options
            )
            
            content = response['message']['content']
            logger.info(f"✨ Geração concluída ({len(content)} chars)")
            
            # Atualiza memória
            self._update_memory(user_id, "user", prompt)
            self._update_memory(user_id, "assistant", content)
            
            return content

        except Exception as e:
            logger.error(f"Erro na geração com modelo {model}: {e}")
            if tier == "high":
                logger.info("Tentando fallback para tier medium...")
                return await self.generate_response(prompt, user_id, system_prompt, tier="medium")
            return "Desculpe, tive um problema ao processar isso."

    async def classify_emotion(self, text: str) -> str:
        """Usa o modelo leve para classificar emoção rapidamente."""
        prompt = f"""Analise a emoção da frase abaixo. Responda APENAS com uma das palavras: alegria, tristeza, raiva, sarcasmo, neutra.
        Frase: "{text}"
        Emoção:"""
        
        try:
            response = await asyncio.to_thread(
                ollama.generate,
                model=self._get_model("low"),
                prompt=prompt,
                options={"temperature": 0.1}
            )
            emotion = response['response'].strip().lower()
            valid_emotions = ["alegria", "tristeza", "raiva", "sarcasmo", "neutra"]
            for v in valid_emotions:
                if v in emotion:
                    return v
            return "neutra"
        except Exception as e:
            logger.error(f"Erro na classificação de emoção: {e}")
            return "neutra"

    async def decide_tier(self, prompt: str) -> ModelTier:
        """
        Usa o modelo leve para decidir se a tarefa requer um modelo 'high' (complexo) ou 'medium' (simples).
        Otimização: Mensagens curtas (< 7 palavras) vão direto para o tier médio para economizar tempo.
        """
        # Short Circuit: Se for muito curto E NÃO FOR PERGUNTA, usa modelo médio
        # Perguntas curtas ("Quem é você?") devem passar pelo router para talvez pegar o modelo High
        if len(prompt.split()) < 7 and "?" not in prompt:
            # Exceção: Se tiver palavrão, manda pro High pra reagir à altura
            palavroes = ["vadia", "idiota", "burra", "lixo", "merda", "porra", "caralho", "puta", "vagabunda", "desgraçada", "imbecil"]
            if any(p in prompt.lower() for p in palavroes):
                return "high"
            return "medium"

        system_prompt = """
        Classifique a complexidade da mensagem do usuário para escolher o modelo de IA adequado.
        
        Critérios:
        - COMPLEXO: Roleplay profundo, filosofia, escrita criativa, raciocínio abstrato, poemas, histórias.
        - SIMPLES: Conversa casual, perguntas diretas, lógica simples, cumprimentos, comandos.
        
        Responda APENAS com "COMPLEXO" ou "SIMPLES".
        """
        
        try:
            response = await asyncio.to_thread(
                ollama.generate,
                model=self._get_model("low"),
                prompt=prompt,
                system=system_prompt,
                options={"temperature": 0.1, "num_predict": 10}
            )
            decision = response['response'].strip().upper()
            
            if "COMPLEXO" in decision:
                return "high"
            return "medium"
            
        except Exception as e:
            logger.error(f"Erro no Smart Router: {e}")
            return "medium" # Fallback seguro
