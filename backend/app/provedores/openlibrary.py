"""Provedor da Open Library (livros) — FASE 6 (opcional).

Documentação: https://openlibrary.org/developers/api
- Não precisa de chave.
- Limite: 1 requisição/segundo, ou 3/segundo se você mandar um
  User-Agent com nome do app e e-mail (use config.USER_AGENT).

O objetivo desta fase é provar a ideia do projeto: você escreve SÓ este
arquivo, troca PROVEDOR=openlibrary no .env, e o app inteiro passa a ser
uma coleção de livros — sem mexer nas rotas, no banco nem no front.

Pistas para começar (abra no navegador):
    https://openlibrary.org/search.json?q=duna&limit=10
    https://openlibrary.org/works/OL893415W.json
    Capas: https://covers.openlibrary.org/b/id/{cover_i}-M.jpg

Sugestão de mapeamento (olhe o JSON e decida você!):
    id_externo <- "key" (ex.: "/works/OL893415W" -> guarde só "OL893415W")
    titulo     <- "title"
    subtitulo  <- autores ("author_name"), juntos com ", "
    ano        <- "first_publish_year"
    imagem_url <- monte com "cover_i"
    descricao  <- no detalhe, o campo "description" (às vezes é texto,
                  às vezes é um dict {"value": "..."} — trate os dois!)

Desafio extra: escreva você mesma os testes, no estilo de
tests/test_fase2_tvmaze.py, em tests/test_fase6_openlibrary.py.
"""

import requests  # noqa: F401  (você vai usar)

from app import config  # noqa: F401
from app.provedores.base import ErroProvedor, Provedor  # noqa: F401
from app.schemas import Item

URL_BASE = "https://openlibrary.org"
TIMEOUT = 10


class ProvedorOpenLibrary(Provedor):
    nome = "openlibrary"
    credito_texto = "Dados de livros fornecidos pela Open Library"
    credito_url = "https://openlibrary.org"

    def buscar(self, termo: str) -> list[Item]:
        # TODO (fase 6)
        raise NotImplementedError("TODO fase 6: buscar() da Open Library")

    def detalhe(self, id_externo: str) -> Item | None:
        # TODO (fase 6)
        raise NotImplementedError("TODO fase 6: detalhe() da Open Library")
