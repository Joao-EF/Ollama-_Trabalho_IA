# Trabalho de Inteligência Artificial – 3ª etapa

Projeto acadêmico do curso de Ciência da Computação da UNIPAC Barbacena.

**Aluno:** João Emanuel de Faria  
**Matrícula:** 241-007675

## Objetivo

Executar um modelo de inteligência artificial localmente com o Ollama, observar as diferenças entre respostas geradas com temperaturas distintas e automatizar os testes utilizando Python.

## Requisitos

- Python 3
- [Ollama](https://ollama.com/download)
- Biblioteca `requests`
- Modelo `qwen2.5-coder:7b`

## Instalação e execução

Na pasta do projeto, execute:

```bash
python -m pip install requests
ollama pull qwen2.5-coder:7b
```

Mantenha o Ollama aberto. Caso o servidor não esteja em execução, utilize `ollama serve` em outro terminal.

Execute o script:

```bash
python atividade_ollama.py
```

Informe o Top-P (por exemplo, `0.9`) e o limite de tokens (por exemplo, `512`). Digite `s` para executar os três testes automaticamente ou `n` para escolher uma temperatura específica.

## Funcionamento

O programa envia o prompt para a API local do Ollama (`http://localhost:11434/api/generate`) e mostra a resposta no terminal conforme ela é gerada. O texto e os parâmetros utilizados são salvos automaticamente em arquivos `.txt` na pasta `resultados/`.

- `temperature`: controla a variedade das respostas.
- `top_p`: limita as opções de tokens consideradas pelo modelo.
- `num_predict`: define o máximo de tokens gerados.
- `seed`: utiliza o valor fixo 42 para ajudar na comparação dos testes do script.

Após instalar as dependências e baixar o modelo, é possível executar o programa sem internet.

## Testes manuais

Para testar diretamente no Ollama:

```bash
ollama run qwen2.5-coder:7b
```

Dentro da sessão, utilize `/clear` antes de cada novo teste e configure a temperatura com `/set parameter temperature 0.0`, `/set parameter temperature 0.8` ou `/set parameter temperature 1.5`. Envie o mesmo prompt em cada cenário:

> Crie uma função em Python que receba uma lista de números inteiros e retorne somente os números que são pares e maiores que 10. Explique a lógica utilizada e demonstre o resultado para a lista [2, 8, 10, 12, 15, 18, 21, 24].

Resultado esperado: `[12, 18, 24]`.

## Resultados dos testes manuais

| Temperatura | Observação |
| --- | --- |
| 0.0 | Código correto e explicação organizada. |
| 0.8 | Código correto, mas a explicação afirmou incorretamente que 10 não é par. |
| 1.5 | Código correto, com comentários explicando a função. |

Os três códigos apresentaram a lógica esperada. Os resultados mostram que uma temperatura elevada não provoca erros obrigatoriamente. As respostas de novas execuções podem variar.

## Estrutura do projeto

```text
atividade_ollama.py
README.md
Trabalho_IA_Etapa_3.pdf
resultados/  # criada automaticamente pelo script
```

O PDF contém os registros dos testes manuais e suas respectivas análises.
