import os
import shutil
import subprocess

def create_extended_structure(base_path):
    """Cria estrutura de diretórios para projeto multilinguagem"""
    new_dirs = [
        'ai/chatbot',
        'ai/emotion',
        'ai/memory',
        'ai/model',
        'avatar/animations',
        'avatar/model',
        'interfaces/twitch',
        'interfaces/discord',
        'interfaces/web',
        'processing',
        'rp',
        'utils',
        'tests',
        'docs',
        'native/cpp_modules',
        'native/rust_modules',
        'java/src',
        'csharp/src',
        'scripts'
    ]
    
    for directory in new_dirs:
        os.makedirs(os.path.join(base_path, directory), exist_ok=True)
        print(f"Criado: {directory}")

def create_multilang_templates(base_path):
    """Cria templates para módulos multilinguagem"""
    templates = {
        'native/cpp_modules/hello_world.cpp': '''#include <iostream>

extern "C" void greet() {
    std::cout << "Hello from C++ module!" << std::endl;
}
''',
        'native/rust_modules/lib.rs': '''#[no_mangle]
pub extern "C" fn greet() {
    println!("Hello from Rust module!");
}
''',
        'java/src/Main.java': '''public class Main {
    public static void main(String[] args) {
        System.out.println("Hello from Java module!");
    }
}
''',
        'csharp/src/Program.cs': '''using System;

namespace Vtuber
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Hello from C# module!");
        }
    }
}
'''
    }
    
    for path, content in templates.items():
        full_path = os.path.join(base_path, path)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Template criado: {path}")

def create_automation_scripts(base_path):
    """Cria scripts de automação build/run"""
    scripts = {
        'scripts/build_all.py': '''import subprocess
import os

def build_cpp():
    print("[Build] C++ module...")
    os.chdir('native/cpp_modules')
    subprocess.run(['g++', '-shared', '-o', 'libhello.so', 'hello_world.cpp'])
    os.chdir('../../')

def build_rust():
    print("[Build] Rust module...")
    os.chdir('native/rust_modules')
    subprocess.run(['cargo', 'build', '--release'])
    os.chdir('../../')

def build_java():
    print("[Build] Java module...")
    os.chdir('java/src')
    subprocess.run(['javac', 'Main.java'])
    os.chdir('../../..')

def build_csharp():
    print("[Build] C# module...")
    os.chdir('csharp/src')
    subprocess.run(['dotnet', 'build'])
    os.chdir('../../..')

def main():
    build_cpp()
    build_rust()
    build_java()
    build_csharp()
    print("✅ Build completo!")

if __name__ == "__main__":
    main()
''',
        'scripts/run_vtuber.py': '''import subprocess

def run_python_main():
    print("[Run] Python Main...")
    subprocess.run(['python', 'main.py'])

def main():
    run_python_main()

if __name__ == "__main__":
    main()
'''
    }

    for path, content in scripts.items():
        full_path = os.path.join(base_path, path)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Script criado: {path}")

def overwrite_main(base_path):
    """Sobrescreve main.py com suporte multilinguagem"""
    main_content = '''# main.py - Ponto de entrada principal
from ai.chatbot import bot
from interfaces.tts import TTSEngine
from avatar.controller import AvatarController

import ctypes
import subprocess

class AIVTuber:
    def __init__(self):
        self.bot = bot.AsteriaBot()
        self.tts = TTSEngine()
        self.avatar = AvatarController()

    def run(self):
        """Loop principal da AIVTuber"""
        print("AIVTuber inicializada!")
        self.bot.start()
        self.run_multilang_modules()

    def run_multilang_modules(self):
        print("Executando módulos multilinguagem...")

        # C++ FFI
        try:
            cpp = ctypes.CDLL('./native/cpp_modules/libhello.so')
            cpp.greet()
        except Exception as e:
            print(f"Erro C++: {e}")

        # Java subprocess
        try:
            subprocess.run(['java', '-cp', 'java/src', 'Main'])
        except Exception as e:
            print(f"Erro Java: {e}")

        # C# e Rust - assumido como binários gerados manualmente
        print("C# e Rust devem ser executados conforme build local.")

if __name__ == "__main__":
    vt = AIVTuber()
    vt.run()
'''
    with open(os.path.join(base_path, 'main.py'), 'w', encoding='utf-8') as f:
        f.write(main_content)
    print("main.py sobrescrito com sucesso.")

def update_requirements(base_path):
    """Atualiza requirements.txt"""
    requirements = '''# Dependências principais
nextcord>=3.0.0
aiohttp>=3.8.0
sentence-transformers>=2.2.0
faiss-cpu>=1.7.0
duckduckgo-search>=3.0.0
beautifulsoup4>=4.11.0
numpy>=1.23.0
python-dotenv>=0.19.0
pyttsx3>=2.90
ollama>=0.1.0
cffi>=1.15.0
'''
    with open(os.path.join(base_path, 'requirements.txt'), 'w', encoding='utf-8') as f:
        f.write(requirements)
    print("requirements.txt atualizado.")

def main():
    print("=== EXPANSOR DE PROJETO AIVTUBER ===")
    project_path = input("Digite o caminho completo do projeto: ").strip('"')

    if not os.path.exists(project_path):
        print("Erro: Diretório do projeto não encontrado!")
        return

    print("\n1. Criando nova estrutura de diretórios...")
    create_extended_structure(project_path)

    print("\n2. Criando templates multilinguagem...")
    create_multilang_templates(project_path)

    print("\n3. Criando scripts de automação...")
    create_automation_scripts(project_path)

    print("\n4. Sobrescrevendo main.py...")
    overwrite_main(project_path)

    print("\n5. Atualizando dependências...")
    update_requirements(project_path)

    print("\n✔ Expansão concluída com sucesso!")
    print("\nPróximos passos:")
    print("- Compile os módulos: python scripts/build_all.py")
    print("- Execute a AI Vtuber: python scripts/run_vtuber.py")
    print("- Configure PATHs e ambientes conforme necessário.")

if __name__ == "__main__":main()
