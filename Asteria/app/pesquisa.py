from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup
import traceback

def pesquisar_web(termo):
    try:
        with DDGS() as ddgs:
            # Ajuste: região global para aumentar a chance de encontrar
            resultados = ddgs.text(termo, region='wt-wt', safesearch='moderate', max_results=3)
            resultados = list(resultados)
        
        print(f"[DEBUG] Resultados crus: {resultados}")

        if resultados:
            respostas = []
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
            }
            
            for resultado in resultados:
                # Ajuste: compatível com 'href' ou 'url'
                url = resultado.get("href") or resultado.get("url")
                if url:
                    try:
                        response = requests.get(url, headers=headers, timeout=5)
                        response.raise_for_status()
                        soup = BeautifulSoup(response.text, 'html.parser')
                        texto_visivel = ' '.join(soup.stripped_strings)
                        resumo = texto_visivel[:500] + "..." if len(texto_visivel) > 500 else texto_visivel
                        respostas.append(f"🔗 {url}\n📄 {resumo}")
                    except requests.RequestException as e:
                        print(f"[ERRO] Falha ao acessar {url}: {e}")
                        respostas.append(f"🔗 {url}\n❗ Erro ao acessar o conteúdo.")
            
            return "\n\n".join(respostas) if respostas else "Hmm... não encontrei nada sobre isso na web! 😅 Quer tentar outra coisa?"
        
        else:
            return "Hmm... não encontrei nada sobre isso na web! 😅 Quer tentar outra coisa?"
    
    except Exception as e:
        print(f"[ERRO] Erro inesperado: {e}")
        traceback.print_exc()
        return "Erro ao realizar a pesquisa. 😓"
