"""Provedor do TVmaze (séries de TV) — FASE 2.

Documentação: https://www.tvmaze.com/api
- Não precisa de chave.
- Limite: pelo menos 20 chamadas a cada 10 segundos por IP.
- Licença CC BY-SA: é OBRIGATÓRIO citar o TVmaze como fonte, com link.

Antes de programar, abra no navegador e olhe o JSON que volta:
    https://api.tvmaze.com/search/shows?q=breaking
    https://api.tvmaze.com/shows/169

Rode os testes desta fase com:
    pytest tests/test_fase2_tvmaze.py
"""

import re

import requests

from app import config
from app.provedores.base import ErroProvedor, Provedor
from app.schemas import Item

URL_BASE = "https://api.tvmaze.com"
TIMEOUT = 10  # segundos. Sem timeout, uma API lenta trava o seu app.


def limpar_html(texto: str | None) -> str | None:
    """O TVmaze manda o resumo com tags HTML (<p>, <b>...). Isto tira as tags.

    Já está pronto. Exemplo: "<p><b>Oi</b> tudo bem</p>" -> "Oi tudo bem"
    """
    if not texto:
        return None
    return re.sub(r"<[^>]+>", "", texto).strip() or None


def converter(show: dict) -> Item:
    """Transforma um "show" do JSON do TVmaze no nosso formato único (Item).

    Mapeamento esperado:
        id_externo  <- show["id"]            (atenção: tem que virar str!)
        titulo      <- show["name"]
        subtitulo   <- show["genres"] juntos com ", "  (ex.: "Drama, Crime")
                       ou None se a lista estiver vazia
        ano         <- os 4 primeiros caracteres de show["premiered"], como int
                       ("2008-01-20" -> 2008), ou None se não tiver data
        imagem_url  <- show["image"]["medium"], ou None se show["image"] for None
        descricao   <- limpar_html(show["summary"])

    Dica: use show.get("campo") em vez de show["campo"] quando o campo
    puder faltar ou vir null. Teste com séries pouco conhecidas: muitas
    não têm imagem nem data de estreia.
    """
    # TODO (fase 2): monte e devolva um Item(...)
    raise NotImplementedError("TODO fase 2: converter()")


class ProvedorTVmaze(Provedor):
    nome = "tvmaze"
    credito_texto = "Dados de séries fornecidos pelo TVmaze (CC BY-SA)"
    credito_url = "https://www.tvmaze.com"

    def buscar(self, termo: str) -> list[Item]:
        """GET {URL_BASE}/search/shows?q=termo

        Passos:
        1. Se o termo estiver vazio (ou só espaços), devolva [] sem chamar a API.
        2. Faça o GET com requests.get(url, params={"q": termo},
           headers={"User-Agent": config.USER_AGENT}, timeout=TIMEOUT).
        3. Se der erro de conexão/timeout (requests.RequestException),
           ou se o status não for 200, lance ErroProvedor("mensagem").
        4. A resposta é uma LISTA de {"score": ..., "show": {...}}.
           Converta cada "show" com converter() e devolva a lista.
        """
        # TODO (fase 2)
        raise NotImplementedError("TODO fase 2: buscar()")

    def detalhe(self, id_externo: str) -> Item | None:
        """GET {URL_BASE}/shows/{id_externo}

        - Status 404 -> a série não existe -> devolva None.
        - Outro status diferente de 200, ou erro de conexão -> ErroProvedor.
        - 200 -> converta o JSON (aqui ele já é o "show" direto) e devolva.
        """
        # TODO (fase 2)
        raise NotImplementedError("TODO fase 2: detalhe()")
