
import requests
import json

url = "http://localhost:11434/api/generate"

dados = {
    "model": "qwen2.5-coder:7b",
    "prompt": "Crie uma função em Python que some dois números.",
    "stream": True
}

resposta = requests.post(url, json=dados, stream=True)
resposta.raise_for_status()

for linha in resposta.iter_lines():
    if linha:
        conteudo = json.loads(linha)

        texto = conteudo.get("response", "")

        print(texto, end="", flush=True)

        if conteudo.get("done"):
            break

resposta.close()
