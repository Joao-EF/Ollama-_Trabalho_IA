import requests
import json
from pathlib import Path
from datetime import datetime

URL = 'http://localhost:11434/api/generate'
MODELO = 'qwen2.5-coder:7b'
PROMPT = ('Crie uma função em Python que receba uma lista de números inteiros '
          'e retorne somente os números que são pares e maiores que 10. '
          'Explique a lógica utilizada e demonstre o resultado para a lista '
          '[2, 8, 10, 12, 15, 18, 21, 24].')


def gerar_resposta(temperatura, top_p, num_predict):
    dados = {
        'model': MODELO,
        'prompt': PROMPT,
        'stream': True,
        'options': {
            'temperature': temperatura,
            'top_p': top_p,
            'num_predict': num_predict,
            'seed': 42
        }
    }
    pasta = Path(__file__).resolve().parent / 'resultados'
    pasta.mkdir(exist_ok=True)
    data = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    arquivo = pasta / f'temperatura_{temperatura}_{data}.txt'
    with requests.post(URL, json=dados, stream=True, timeout=(10, 600)) as resposta:
        resposta.raise_for_status()
        with arquivo.open('w', encoding='utf-8') as saida:
            saida.write(f'Modelo: {MODELO}\nTemperatura: {temperatura}\n'
                        f'Top-P: {top_p}\nNum_predict: {num_predict}\nSeed: 42\n'
                        f'Prompt: {PROMPT}\n\nResposta:\n')
            terminou = False
            for linha in resposta.iter_lines():
                if not linha:
                    continue
                mensagem = json.loads(linha)
                if mensagem.get('error'):
                    raise RuntimeError(mensagem['error'])
                trecho = mensagem.get('response', '')
                print(trecho, end='', flush=True)
                saida.write(trecho)
                if mensagem.get('done'):
                    terminou = True
                    saida.write(f"\n\nTokens gerados: {mensagem.get('eval_count', 'N/D')}\n"
                                f"Motivo do fim: {mensagem.get('done_reason', 'N/D')}\n")
                    break
            if not terminou:
                raise RuntimeError('Fluxo interrompido; arquivo parcial.')
    print(f'\n\nResposta salva em: {arquivo}')


if __name__ == '__main__':
    try:
        top_p = float(input('Top-P (ex.: 0.9): ').replace(',', '.'))
        num_predict = int(input('Limite de tokens (ex.: 512): '))
        if not 0 < top_p <= 1 or num_predict <= 0:
            raise ValueError('Top-P deve estar em (0, 1] e o limite deve ser positivo.')
        modo = input('Executar todos os três testes? (s/n): ').strip().lower()
        temperaturas = [0.0, 0.8, 1.5] if modo == 's' else [float(input('Temperatura: ').replace(',', '.'))]
        for temperatura in temperaturas:
            if not 0 <= temperatura <= 2:
                raise ValueError('Informe uma temperatura entre 0 e 2.')
            print(f'\n--- Temperatura {temperatura} ---\n')
            gerar_resposta(temperatura, top_p, num_predict)
    except (requests.RequestException, ValueError, RuntimeError, OSError) as erro:
        print(f'Erro: {erro}')
