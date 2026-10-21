"""FASE 1 — Seu primeiro contato com uma API de verdade.

Rode a partir da pasta backend (com o venv ativado):
    python ../exploracao/01_primeiro_get.py

Não tem teste aqui: o objetivo é EXPLORAR. Mude as coisas, quebre,
leia as mensagens de erro. Responda as perguntas em comentários no
próprio arquivo ou no seu caderno.
"""

import requests

# 1) Um GET simples ------------------------------------------------------------
resposta = requests.get(
    "https://api.tvmaze.com/search/shows",
    params={"q": "girls"},  # o requests monta "?q=girls" para você
    timeout=10,
)

print("URL que foi chamada:", resposta.url)
print("Código de status:", resposta.status_code)
print("Tipo do conteúdo:", resposta.headers.get("Content-Type"))

dados = resposta.json()  # transforma o texto JSON em listas/dicionários do Python
print("Quantos resultados:", len(dados))
print("Primeiro resultado (só o nome):", dados[0]["show"]["name"])

# PERGUNTAS:
# a) Qual é o tipo de `dados`? E de `dados[0]`? (use type())
# b) Imprima as CHAVES do primeiro "show" (dica: .keys()). Quais você usaria
#    para mostrar a série num site?
# c) Troque "girls" por um termo que não existe (ex.: "xzxzxzxz").
#    O que volta? O status muda?


# 2) Um item só ----------------------------------------------------------------
# TODO: faça um GET em https://api.tvmaze.com/shows/169 e imprima
#       o nome, os gêneros e a data de estreia.


# 3) Quando dá errado ----------------------------------------------------------
# TODO: faça um GET em https://api.tvmaze.com/shows/0
#       Qual o status? O que tem no JSON?
#
# TODO: chame uma URL que não existe, como https://api.tvmaze.com/nao-existe
#
# TODO: desligue o Wi-Fi (ou use uma URL inventada como
#       https://essa-api-nao-existe-123.com) e rode de novo. Qual erro
#       aparece? Como você faria o programa NÃO quebrar? (pesquise try/except
#       com requests.RequestException)


# 4) Desafio -------------------------------------------------------------------
# TODO: escreva uma função `listar_series(termo)` que imprime, para cada
#       resultado, uma linha assim:
#           Breaking Bad (2008) — Drama, Crime, Thriller
#       E se a série não tiver data de estreia? E se não tiver gênero?
#       (essa função é o embrião do provedor que você vai escrever na fase 2!)
