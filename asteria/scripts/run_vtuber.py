import subprocess

def run_python_main():
    print("[Run] Python Main...")
    subprocess.run(['python', 'main.py'])

def main():
    run_python_main()

if __name__ == "__main__":
    main()
