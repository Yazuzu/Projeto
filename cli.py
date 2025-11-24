import asyncio
import sys
from src.services.llm import LLMService
from src.services.persona import PersonaService
from src.core.logger import setup_logger

# Configura logger para o terminal
logger = setup_logger("CLI")

async def main():
    print("🤖 Iniciando Interface de Terminal da Astéria...")
    print("Carregando serviços...")
    
    try:
        llm = LLMService()
        persona = PersonaService()
        print("✅ Serviços carregados!")
    except Exception as e:
        print(f"❌ Erro ao carregar serviços: {e}")
        return

    print("\n💬 Chat iniciado! Digite 'sair' para encerrar.")
    print("-" * 50)

    user_id = 999999 # ID fictício para teste

    while True:
        try:
            user_input = input("\nVocê: ").strip()
            if not user_input:
                continue
            
            if user_input.lower() in ['sair', 'exit', 'quit']:
                print("👋 Encerrando...")
                break

            print("Thinking...", end="\r")

            # 1. Gera Contexto da Persona
            system_prompt = persona.gerar_contexto_prompt(user_input, user_id=user_id)

            # 2. Smart Router
            tier = await llm.decide_tier(user_input)
            print(f"[DEBUG] Tier escolhido: {tier}   ", end="\r")

            # 3. Gera Resposta
            resposta = await llm.generate_response(
                prompt=user_input,
                user_id=user_id,
                system_prompt=system_prompt,
                tier=tier
            )

            print(f"Astéria ({tier}): {resposta}")

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\n❌ Erro: {e}")

if __name__ == "__main__":
    asyncio.run(main())
