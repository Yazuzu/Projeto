import os
import shutil

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def move_file(src, dest_dir):
    """Move arquivo para dest_dir, sobrescrevendo se necessário"""
    if os.path.exists(src):
        dest = os.path.join(dest_dir, os.path.basename(src))
        if os.path.exists(dest):
            os.remove(dest)
            print(f"Sobrescrevendo: {dest}")
        shutil.move(src, dest)
        print(f"Movido: {src} -> {dest}")

def deep_migrate_files(base_path):
    asteria_path = os.path.join(base_path, 'asteria')
    ensure_dir(asteria_path)

    dirs_to_move = [
        'bot', 'emotion', 'memory', 'model', 'web', 'utils',
        'communication', 'capture', 'processing', 'rp', 'tests', 'docs'
    ]

    for d in dirs_to_move:
        src = os.path.join(base_path, d)
        dest = os.path.join(asteria_path, d)
        if os.path.exists(src):
            if os.path.exists(dest):
                shutil.rmtree(dest)
                print(f"Removendo diretório duplicado: {dest}")
            shutil.move(src, dest)
            print(f"Diretório movido: {src} -> {dest}")

    files_to_move = [
        'main.py', 'utils.py', 'config.py', 'commands.py',
        'events.py', 'ai_module.py', 'memory_manager.py',
        'setup_project.py', 'script.py', 'web_tools.py'
    ]

    for f in files_to_move:
        src = os.path.join(base_path, f)
        move_file(src, asteria_path)

def cleanup_old_directories(base_path):
    dirs_to_remove = [
        'bot', 'emotion', 'memory', 'model', 'web', 'utils',
        'communication', 'capture', 'processing', 'rp', 'tests', 'docs'
    ]

    for d in dirs_to_remove:
        path = os.path.join(base_path, d)
        if os.path.exists(path):
            shutil.rmtree(path)
            print(f"Diretório removido: {path}")

def remove_py_cache(base_path):
    for root, dirs, files in os.walk(base_path):
        for d in dirs:
            if d == '__pycache__':
                full_path = os.path.join(root, d)
                shutil.rmtree(full_path)
                print(f"__pycache__ removido: {full_path}")

def main():
    print("=== REORGANIZADOR FINAL AIVTUBER (v2) ===")
    project_path = input("Digite o caminho completo do projeto: ").strip('"')

    if not os.path.exists(project_path):
        print("Erro: Diretório do projeto não encontrado!")
        return

    print("\n1. Migrando arquivos e diretórios...")
    deep_migrate_files(project_path)

    print("\n2. Limpando diretórios antigos...")
    cleanup_old_directories(project_path)

    print("\n3. Removendo __pycache__...")
    remove_py_cache(project_path)

    print("\n✔ Refatoração final concluída com sucesso!")
    print(f"→ Estrutura final em: {os.path.join(project_path, 'asteria')}")

if __name__ == "__main__":main()
