"""
Pesquisa na web e resume resultados.
"""
import aiohttp
from duckduckgo_search import DDGS
from bs4 import BeautifulSoup
import asyncio

MAX_RESUMO = 500

async def buscar_resumo(session, url):
    try:
        async with session.get(url, timeout=10) as response:
            response.raise_for_status()
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            texto = ' '.join(soup.stripped_strings)
            resumo = texto[:MAX_RESUMO] + "..." if len(texto) > MAX_RESUMO else texto
            return f"🔗 {url}\n📄 {resumo}"
    except Exception as e:
        return f"🔗 {url}\n❗ Erro: {e}"

async def pesquisar_web(termo):
    try:
        loop = asyncio.get_running_loop()
        resultados = await loop.run_in_executor(None, lambda: list(DDGS().text(termo, region='pt-br', safesearch='moderate', max_results=2)))
        if not resultados:
            return "Nenhum resultado encontrado."

        headers = {"User-Agent": "Mozilla/5.0"}
        async with aiohttp.ClientSession(headers=headers) as session:
            tasks = [buscar_resumo(session, r.get("href") or r.get("url")) for r in resultados if r.get("href") or r.get("url")]
            respostas = await asyncio.gather(*tasks, return_exceptions=True)

        return "\n\n".join(res if not isinstance(res, Exception) else "❗ Erro ao acessar conteúdo." for res in respostas)
    except Exception as e:
        return f"Erro na pesquisa: {e}"
