import aiohttp
from duckduckgo_search import DDGS
from bs4 import BeautifulSoup
import asyncio
from src.core.logger import setup_logger

logger = setup_logger(__name__)

class SearchService:
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

    async def search(self, query: str, max_results: int = 3) -> str:
        """Realiza pesquisa no DuckDuckGo e extrai conteúdo das páginas de forma assíncrona."""
        try:
            # DuckDuckGo Search (executado em thread pois a lib é síncrona/bloqueante em partes)
            results = await asyncio.to_thread(
                lambda: list(DDGS().text(query, region='pt-br', safesearch='moderate', max_results=max_results))
            )

            if not results:
                return "Nenhum resultado encontrado."

            formatted_results = []
            
            async with aiohttp.ClientSession(headers=self.headers) as session:
                tasks = [self._fetch_page_content(session, r.get("href")) for r in results]
                contents = await asyncio.gather(*tasks)

                for result, content in zip(results, contents):
                    url = result.get("href")
                    if content:
                        formatted_results.append(f"🔗 {url}\n📄 {content}")
                    else:
                        formatted_results.append(f"🔗 {url}\n⚠️ Não foi possível ler o conteúdo.")

            return "\n\n".join(formatted_results)

        except Exception as e:
            logger.error(f"Erro na pesquisa: {e}")
            return f"Erro ao pesquisar: {e}"

    async def _fetch_page_content(self, session: aiohttp.ClientSession, url: str) -> str:
        if not url:
            return ""
        try:
            async with session.get(url, timeout=10) as response:
                if response.status != 200:
                    return ""
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                # Remove scripts e estilos
                for script in soup(["script", "style"]):
                    script.decompose()
                
                text = soup.get_text(separator=' ', strip=True)
                # Limita o tamanho do texto por página
                return text[:500] + "..." if len(text) > 500 else text
        except Exception as e:
            logger.warning(f"Erro ao acessar {url}: {e}")
            return ""
