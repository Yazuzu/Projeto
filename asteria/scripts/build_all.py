import subprocess
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
