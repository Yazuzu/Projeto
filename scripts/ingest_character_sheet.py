#!/usr/bin/env python3
"""
Script para ingerir fichas de personagem na memória RAG da Astéria.
Processa arquivos .txt com fichas narrativas e as adiciona ao ChromaDB.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.services.memory import MemoryService

def ingest_character_sheet(file_path: str):
    """Ingere uma ficha de personagem na memória."""
    if not os.path.exists(file_path):
        print(f"❌ Arquivo não encontrado: {file_path}")
        return
    
    print(f"📋 Carregando ficha de personagem: {file_path}")
    memory = MemoryService()
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extrai nome do personagem do arquivo para metadata
    char_name = os.path.basename(file_path).replace('.txt', '').replace('_', ' ').title()
    
    # Divide por seções (linhas com #)
    sections = []
    current_section = ""
    
    for line in content.split('\n'):
        if line.strip().startswith('#') and current_section:
            sections.append(current_section.strip())
            current_section = ""
        current_section += line + "\n"
    
    if current_section.strip():
        sections.append(current_section.strip())
    
    print(f"📝 Encontradas {len(sections)} seções na ficha...")
    
    for i, section in enumerate(sections, 1):
        # Ignora seções muito curtas (menos de 100 caracteres)
        if len(section) < 100:
            continue
        
        # Adiciona à memória
        memory.add_memory(
            text=section,
            metadata={
                "source": "character_sheet",
                "character": char_name,
                "section_index": i,
                "file": os.path.basename(file_path)
            }
        )
        print(f"  ✅ Seção {i} adicionada ({len(section)} chars)")
    
    total_memories = memory.collection.count()
    print(f"\n🎉 Ficha de '{char_name}' ingerida! Total de memórias no banco: {total_memories}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python scripts/ingest_character_sheet.py [arquivo.txt]")
        print("\nExemplo:")
        print("  python scripts/ingest_character_sheet.py rp_sheets/asteria_base.txt")
        sys.exit(1)
    
    ingest_character_sheet(sys.argv[1])
