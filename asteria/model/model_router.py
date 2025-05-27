"""
Roteador inteligente de modelos IA.
"""
def roteador_modelo(prompt, modelo_preferido="auto"):
    import ollama
    if modelo_preferido == "auto":
        if "código" in prompt.lower():
            modelo = "gpt4all"
        elif "emoção" in prompt.lower():
            modelo = "vicuna"
        else:
            modelo = "llama3"
    else:
        modelo = modelo_preferido

    print(f"[ROTEADOR] Modelo: {modelo}")
    if modelo in ["llama3", "vicuna"]:
        resposta = ollama.generate(model=modelo, prompt=prompt, options={"temperature": 0.7, "num_predict": 256})["response"]
    elif modelo == "gpt4all":
        resposta = gpt4all_generate(prompt)
    else:
        resposta = "Modelo não encontrado."
    return resposta

def gpt4all_generate(prompt):
    return f"[GPT4All] {prompt[:100]}..."
