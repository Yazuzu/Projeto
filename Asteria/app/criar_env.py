import os

def criar_env():
    env_path = os.path.join(os.getcwd(), '.env')

    if os.path.exists(env_path):
        print("⚠️ O arquivo .env já existe.")
        sobrescrever = input("Deseja sobrescrever? (s/n): ").strip().lower()
        if sobrescrever != 's':
            print("Operação cancelada.")
            return

    token = input("Digite o token do seu bot Discord: ").strip()

    if not token:
        print("❌ Token inválido. Abortando...")
        return

    with open(env_path, 'w') as f:
        f.write(f'DISCORD_BOT_TOKEN={token}\n')

    print(f"✅ Arquivo .env criado com sucesso em: {env_path}")

if __name__ == "__main__":
    criar_env()
