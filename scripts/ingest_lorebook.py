#!/usr/bin/env python3
"""
Script para ingerir Lorebooks (arquivos de texto) na memória RAG da Astéria.
Uso: python scripts/ingest_lorebook.py [caminho_do_arquivo.txt]
"""

import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.services.memory import MemoryService

def ingest_lorebook(file_path: str):
    """Ingere um arquivo de Lorebook na memória."""
    if not os.path.exists(file_path):
        print(f"❌ Arquivo não encontrado: {file_path}")
        return
    
    print(f"📖 Carregando Lorebook: {file_path}")
    memory = MemoryService()
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Divide o texto em parágrafos (blocos separados por linhas vazias)
    paragraphs = [p.strip() for p in content.split('\n\n') if p.strip() and not p.strip().startswith('#')]
    
    print(f"📝 Encontrados {len(paragraphs)} parágrafos para processar...")
    
    for i, paragraph in enumerate(paragraphs, 1):
        # Ignora parágrafos muito curtos (menos de 50 caracteres)
        if len(paragraph) < 50:
            continue
            
        # Adiciona à memória
        memory.add_memory(
            text=paragraph,
            metadata={
                "source": "lorebook",
                "file": os.path.basename(file_path),
                "paragraph_index": i
            }
        )
        print(f"  ✅ Parágrafo {i} adicionado ({len(paragraph)} chars)")
    
    total_memories = memory.collection.count()
    print(f"\n🎉 Ingestão completa! Total de memórias no banco: {total_memories}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python scripts/ingest_lorebook.py [arquivo.txt]")
        print("\nExemplo:")
        print("  python scripts/ingest_lorebook.py lorebooks/mircea_rp_sessions.txt")
        sys.exit(1)
    
    ingest_lorebook(sys.argv[1])
