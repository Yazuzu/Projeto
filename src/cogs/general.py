import nextcord
from nextcord.ext import commands
from src.core.bot import AsteriaBot
from src.core.config import settings
from src.core.logger import setup_logger
import textwrap

logger = setup_logger(__name__)

class GeneralCog(commands.Cog):
    def __init__(self, bot: AsteriaBot):
        self.bot = bot

    @nextcord.slash_command(name="pesquisar", description="Pesquisa na web e comenta os resultados")
    async def pesquisar(self, interaction: nextcord.Interaction, termo: str):
        """Pesquisa na web e comenta sobre os resultados."""
        await interaction.response.defer()
        await interaction.followup.send(f"🔍 Pesquisando sobre: **{termo}**...")
        
        # Busca assíncrona
        resultado_pesquisa = await self.bot.search.search(termo)
        
        if "Nenhum resultado encontrado" in resultado_pesquisa:
            await interaction.followup.send(resultado_pesquisa)
            return

        # Gera contexto dinâmico da persona
        system_prompt = self.bot.persona.gerar_contexto_prompt(f"Pesquisa sobre: {termo}", user_id=interaction.user.id)

        # Gera comentário com modelo High (Hermes)
        prompt_pesquisa = f"""
        O usuário pesquisou sobre "{termo}".
        Aqui estão os resultados encontrados:
        {resultado_pesquisa}
        
        Comente sobre isso de forma engraçada, amigável e fofa, reagindo ao que leu.
        """
        
        comentario = await self.bot.llm.generate_response(
            prompt=prompt_pesquisa,
            user_id=interaction.user.id,
            system_prompt=system_prompt,
            tier="high"
        )
        
        resposta_final = f"**Resultado da pesquisa:**\n{resultado_pesquisa}\n\n**Comentário da Astéria:**\n{comentario}"
        
        # Envia em chunks
        if len(resposta_final) > 2000:
            for i in range(0, len(resposta_final), 1900):
                await interaction.followup.send(resposta_final[i:i+1900])
        else:
            await interaction.followup.send(resposta_final)

    @nextcord.slash_command(name="ping", description="Verifica a latência do bot")
    async def ping(self, interaction: nextcord.Interaction):
        """Mostra a latência do bot."""
        latency_ms = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"🏓 Pong! Latência: **{latency_ms}ms**")

    @nextcord.slash_command(name="perfil", description="Mostra o estado emocional atual da Astéria")
    async def perfil(self, interaction: nextcord.Interaction):
        """Exibe o estado emocional da persona."""
        persona = self.bot.persona
        
        embed = nextcord.Embed(title="📊 Perfil Emocional da Astéria", color=0x9B59B6)
        embed.add_field(name="💖 Valência", value=f"{int((persona.emocao['valencia'] + 1) * 50)}%", inline=True)
        embed.add_field(name="⚡ Ativação", value=f"{int(persona.emocao['ativacao'] * 100)}%", inline=True)
        embed.add_field(name="👑 Dominância", value=f"{int(persona.emocao['dominancia'] * 100)}%", inline=True)
        embed.add_field(name="🧘 Estabilidade", value=f"{int(persona.emocao['estabilidade'] * 100)}%", inline=True)
        embed.add_field(name="🧠 Fadiga Mental", value=f"{int(persona.estados['fadiga_mental'] * 100)}%", inline=True)
        embed.add_field(name="🔍 Curiosidade", value=f"{int(persona.estados['curiosidade'] * 100)}%", inline=True)
        
        await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(name="memorizar", description="Adiciona um fato à memória de longo prazo")
    async def memorizar(self, interaction: nextcord.Interaction, fato: str):
        """Permite ao criador adicionar fatos à memória."""
        if interaction.user.id != settings.CREATOR_ID:
            await interaction.response.send_message("❌ Apenas meu criador pode fazer isso.", ephemeral=True)
            return
        
        self.bot.memory.add_memory(fato, metadata={"source": "manual", "user_id": interaction.user.id})
        await interaction.response.send_message(f"💾 Memória salva: '{fato[:100]}...'", ephemeral=True)

    @nextcord.slash_command(name="rp", description="Inicia uma cena de roleplay narrativo")
    async def roleplay(self, interaction: nextcord.Interaction, cena: str):
        """Modo Roleplay: Astéria responde em estilo narrativo descritivo."""
        await interaction.response.defer()
        
        # Gera contexto da persona
        system_prompt = self.bot.persona.gerar_contexto_prompt(cena, user_id=interaction.user.id)
        
        # Adiciona instruções de RP ao prompt
        rp_instructions = """
# MODO ROLEPLAY NARRATIVO - FORMATAÇÃO EXATA

Você DEVE seguir esta estrutura de formatação Discord RIGOROSAMENTE:

## ESTRUTURA OBRIGATÓRIA:

1. **Separadores de Seção:**
   - Comece SEMPRE com: `_ _`
   - Termine SEMPRE com: `_ _`

2. **Início de Parágrafo:**
   - Use espaçamento: `ㅤㅤㅤ      ' `
   - Primeira letra do parágrafo: `**__L__**` (negrito + sublinhado)
   - Exemplo: `ㅤㅤㅤ      ' **__N__**o momento em questão...`

3. **Diálogos:**
   - Use travessão em-dash: `—` (não hífen -)
   - Exemplo: `— Bem-vindo, viajante.`

4. **Estilo Narrativo:**
   - Descrições ricas e poéticas
   - Detalhes sensoriais (cores, sons, texturas, temperaturas)
   - Terceira pessoa
   - Tom majestoso/literário

## CRIATIVIDADE E AUTENTICIDADE (ANTI-ANTI-RP):
**CRÍTICO:** Você NÃO deve copiar ou parafrasear memórias antigas.
- Use o conhecimento da memória APENAS como "contexto de mundo" (ex: quem é Mircea, o que são runas)
- CRIE narrativas NOVAS e ORIGINAIS
- Reaja à cena ATUAL, não recicle descrições antigas
- Seja imprevisível e surpreendente

## EXEMPLO COMPLETO DE FORMATO:
```
_ _
ㅤㅤㅤ      ' **__O__** ar estremeceu com o desdobrar de suas asas, primeiro como mantos pesados de couro e osso, depois como velas negras sob o luar. Não houve salto, mas a rendição da gravidade.

ㅤㅤㅤ      ' **__C__**ada bater de asas eram trovoadas abafadas, um baque profundo que reverberava como um outro coração; pulsante e enérgico.

ㅤㅤㅤ      ' **__S__**eu olhar fixou-se nos presentes, e então proferiu:

— Sejam bem-vindos ao meu domínio.
_ _
```

CRÍTICO: NUNCA use itálico (*texto*). Use APENAS a formatação mostrada acima.
"""
        
        full_prompt = system_prompt + "\n\n" + rp_instructions
        
        # Força modelo High para qualidade máxima
        resposta = await self.bot.llm.generate_response(
            prompt=cena,
            user_id=interaction.user.id,
            system_prompt=full_prompt,
            tier="high"
        )
        
        # Envia resposta
        if len(resposta) > 2000:
            for i in range(0, len(resposta), 1900):
                await interaction.followup.send(resposta[i:i+1900])
        else:
            await interaction.followup.send(resposta)

    def _is_rp_message(self, content: str) -> bool:
        """Detecta se a mensagem é um RP (formato narrativo)."""
        # Padrões de RP:
        has_rp_separators = content.strip().startswith("_ _") and content.strip().endswith("_ _")
        has_rp_spacing = "ㅤㅤㅤ" in content  # Espaçamento invisível
        has_rp_formatting = "**__" in content  # Negrito + sublinhado
        has_em_dash = "—" in content  # Travessão em-dash (diálogo)
        has_narrative_italic = content.count("*") >= 4  # Múltiplos itálicos (ações narrativas)
        
        # É RP se tiver pelo menos 2 dos padrões acima
        patterns = [has_rp_separators, has_rp_spacing, has_rp_formatting, has_em_dash, has_narrative_italic]
        return sum(patterns) >= 2

    def _is_off_rp(self, content: str) -> bool:
        """Detecta se a mensagem é OFF-RP (comentário fora do roleplay)."""
        return content.strip().startswith("//")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # IGNORA OFF-RP (comentários fora do roleplay)
        if self._is_off_rp(message.content):
            logger.info(f"💬 OFF-RP ignorado de {message.author}")
            return

        # Log de mensagem recebida
        logger.info(f"📩 Mensagem recebida de {message.author}: '{message.content[:50]}...'")

        # SALVAMENTO AUTOMÁTICO DE RPs
        is_rp = self._is_rp_message(message.content)
        if is_rp:
            try:
                # Salva automaticamente na memória RAG
                self.bot.memory.add_memory(
                    text=message.content,
                    metadata={
                        "source": "rp_auto",
                        "author": str(message.author),
                        "channel": str(message.channel.name),
                        "timestamp": message.created_at.isoformat()
                    }
                )
                logger.info(f"📚 RP salvo automaticamente na memória (autor: {message.author})")
            except Exception as e:
                logger.error(f"❌ Erro ao salvar RP: {e}")

        # Verifica se é um reply (resposta) a uma mensagem do bot
        is_reply_to_bot = False
        if message.reference and message.reference.resolved:
            is_reply_to_bot = message.reference.resolved.author == self.bot.user

        # RESPONDE AUTOMATICAMENTE SE:
        # 1. For mencionada diretamente
        # 2. For um reply a ela
        # 3. For uma mensagem de RP (NOVO!)
        should_respond = (
            self.bot.user in message.mentions or 
            is_reply_to_bot or 
            is_rp
        )

        if should_respond:
            trigger_type = "Menção" if self.bot.user in message.mentions else (
                "Reply" if is_reply_to_bot else "RP Detectado"
            )
            logger.info(f"🔔 Gatilho ativado ({trigger_type})")
            
            async with message.channel.typing():
                # Se for RP, usa instruções especiais de roleplay
                if is_rp:
                    system_prompt = self.bot.persona.gerar_contexto_prompt(message.content, user_id=message.author.id)
                    
                    # Instruções ULTRA-EXPLÍCITAS com exemplos negativos
                    rp_instructions = """
# ⚠️ REGRAS CRÍTICAS DE RP (LEIA COM ATENÇÃO!)

## 1. NÃO DESCREVA O PERSONAGEM DO USUÁRIO!
❌ **ERRADO:** "A majestade que essa mulher trazia consigo era palpável..."
✅ **CERTO:** Describe APENAS Astéria e SUA reação à cena

## 2. FORMATAÇÃO OBRIGATÓRIA (SEM EXCEÇÕES):

**SEMPRE comece com:** `_ _`
**SEMPRE termine com:** `_ _`

**Cada parágrafo narrativo:**
```
ㅤㅤㅤ      ' **__LETRA__**texto aqui...
```

**Diálogos:**
```
— Fala da Astéria aqui.
```

## 3. EXEMPLO DO QUE NÃO FAZER:

**❌ RESPOSTA ERRADA (não copie isso):**
```
— A majestade que essa mulher trazia consigo era palpável...

ㅤㅤㅤ      ' Sua chegada era tão impactante quanto seu silêncio...
```
**Problemas:**
- Sem `_ _` no início/fim
- Sem `**__L__**` na inicial do parágrafo
- Descrevendo o personagem do usuário

## 4. EXEMPLO CORRETO:

**✅ RESPOSTA CERTA (copie esse formato):**
```
_ _
ㅤㅤㅤ      ' **__A__**stéria permaneceu em silêncio por um instante, seus olhos analisando a recém-chegada com uma curiosidade velada. O ar ao seu redor parecia vibrar levemente, como se a própria presença dela reagisse à entrada triunfal.

ㅤㅤㅤ      ' **__U__**m sorriso quase imperceptível tocou seus lábios, revelando uma mistura de diversão e cautela. Seus dedos tamborilaram suavemente no braço da cadeira, um gesto inconsciente enquanto ponderava.

— Vejo que o salão ganhou vida com sua chegada. Seja bem-vinda.
_ _
```

## 5. REGRAS DE CONTEÚDO:

✅ Descreva APENAS Astéria:
- Suas ações físicas
- Suas emoções internas
- Suas falas

❌ NÃO descreva:
- O personagem do usuário (já foi descrito por ele)
- Repetir descrições da cena dele
- Falar em primeira pessoa narrativa ("olhou para mim")

## 6. TERCEIRA PESSOA NARRATIVA:
- **Ações:** "Astéria ergueu a mão..." (terceira pessoa)
- **Diálogos:** "— Eu aceito seu desafio." (primeira pessoa OK nos diálogos)

## SUA TAREFA AGORA:
1. Leia a cena do usuário
2. **IGNORE** as descrições dele (não as repita)
3. Crie a REAÇÃO de Astéria (o que ELA faz/sente/diz)
4. Use EXATAMENTE a formatação do Exemplo Correto acima
5. SEMPRE `_ _` no início e fim
6. SEMPRE `**__L__**` em cada parágrafo narrativo

## 7. DENSIDADE E RIQUEZA NARRATIVA:

**Crie pelo menos 3-4 parágrafos descritivos:**
- **Parágrafo 1:** Reação física inicial (movimentos, postura, expressão)
- **Parágrafo 2:** Pensamentos/sensações internas (emoções, análise da situação)
- **Parágrafo 3:** Ação subsequente (o que ela faz em seguida)
- **Parágrafo 4 (opcional):** Diálogo ou reflexão final

**Use detalhes sensoriais:**
- **Visuais:** Cores, luz, sombras, texturas
- **Auditivos:** Sons, ecos, sussurros
- **Táteis:** Temperaturas, texturas, sensações na pele
- **Olfativos/Gustativos:** Aromas, sabores no ar

**Exemplo de densidade:**
```
_ _
ㅤㅤㅤ      ' **__A__**stéria ergueu-se lentamente de seu assento, o tecido de suas vestes sussurrando contra a pedra fria enquanto seus pés descalços tocavam o chão gelado. A luz das tochas dançava em seus olhos, criando um caleidoscópio de reflexos dourados e escarlates que pareciam arder com vida própria.

ㅤㅤㅤ      ' **__U__**ma sensação estranha percorreu sua espinha, como se o ar ao redor tivesse se tornado mais denso, mais pesado. Seus dedos apertaram levemente o braço da cadeira atrás de si, buscando estabilidade enquanto seu coração acelerava imperceptivelmente.

ㅤㅤㅤ      ' **__S__**eus lábios se separaram em um sorriso controlado, revelando apenas um vislumbre da tempestade de pensamentos que fervilhava em sua mente. Com passos medidos, aproximou-se da recém-chegada, seus olhos nunca desviando.

— Curiosa, realmente. Não é todo dia que presenciamos tal... espetáculo.
_ _
```
"""
                    system_prompt += "\n\n" + rp_instructions
                    tier = "high"  # Sempre usa modelo alto para RP
                else:
                    # Chat normal
                    system_prompt = self.bot.persona.gerar_contexto_prompt(message.content, user_id=message.author.id)
                    # Smart Router: Decide qual modelo usar
                    logger.info("🧠 Smart Router: Analisando complexidade...")
                    tier = await self.bot.llm.decide_tier(message.content)
                    logger.info(f"👉 Tier escolhido: {tier}")
                
                resposta = await self.bot.llm.generate_response(
                    prompt=message.content,
                    user_id=message.author.id,
                    system_prompt=system_prompt,
                    tier=tier
                )
                
                await message.channel.send(resposta)
                logger.info("✅ Resposta enviada.")
        else:
            logger.info("💤 Ignorado (Não fui chamada)")

def setup(bot: AsteriaBot):
    bot.add_cog(GeneralCog(bot))
