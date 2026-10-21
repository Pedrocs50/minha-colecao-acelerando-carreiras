"""As rotas do back-end — FASES 4 e 5.

Para rodar o servidor (dentro da pasta backend, com o venv ativado):
    uvicorn app.main:app --reload

Depois abra:
    http://localhost:8000        -> o site (front-end, já pronto)
    http://localhost:8000/docs   -> documentação automática da API (teste por lá!)

O "contrato" que o front-end espera está em docs/contrato-da-api.md.
Rode os testes com:
    pytest tests/test_fase4_rotas.py
"""

import sqlite3
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, Response  # noqa: F401
from fastapi.staticfiles import StaticFiles

from app import database as db  # noqa: F401
from app.provedores import ErroProvedor, Provedor, get_provedor  # noqa: F401
from app.schemas import Item, ItemAtualizacao, ItemNovo, ItemSalvo, Status  # noqa: F401

app = FastAPI(title="Minha Coleção")


# ---------------------------------------------------------------------------
# EXEMPLO PRONTO — leia com atenção antes de escrever as suas rotas.
#
# - @app.get("/caminho") diz qual método HTTP e qual URL chegam aqui.
# - `provedor: Provedor = Depends(get_provedor)` faz o FastAPI chamar
#   get_provedor() e entregar o resultado. Nos testes, a gente troca
#   get_provedor por um provedor falso — por isso NUNCA crie o provedor
#   "na mão" dentro da rota.
# - O dicionário devolvido vira JSON automaticamente.
# ---------------------------------------------------------------------------
@app.get("/api/provedor")
def provedor_ativo(provedor: Provedor = Depends(get_provedor)):
    """Diz qual provedor está ativo e o crédito que precisa aparecer no site."""
    return {
        "nome": provedor.nome,
        "credito_texto": provedor.credito_texto,
        "credito_url": provedor.credito_url,
    }


# ---------------------------------------------------------------------------
# FASE 4 — a partir daqui é com você!
# ---------------------------------------------------------------------------


@app.get("/api/buscar", response_model=list[Item])
def buscar(q: str = "", provedor: Provedor = Depends(get_provedor)):
    """GET /api/buscar?q=termo

    Chama provedor.buscar(q) e devolve a lista.
    FASE 5: se o provedor lançar ErroProvedor, responda 502 com
    raise HTTPException(status_code=502, detail="mensagem amigável").
    """
    # TODO (fase 4)
    raise NotImplementedError("TODO fase 4: GET /api/buscar")


@app.post("/api/itens", response_model=ItemSalvo, status_code=201)
def criar_item(
    item: ItemNovo,
    conn: sqlite3.Connection = Depends(db.get_db),
    provedor: Provedor = Depends(get_provedor),
):
    """POST /api/itens  (corpo: JSON no formato ItemNovo)

    Salva com db.inserir_item(conn, provedor.nome, item.model_dump()).
    FASE 5: se o item já existir (sqlite3.IntegrityError), responda 409.
    """
    # TODO (fase 4)
    raise NotImplementedError("TODO fase 4: POST /api/itens")


@app.get("/api/itens", response_model=list[ItemSalvo])
def listar_itens(status: Status | None = None, conn: sqlite3.Connection = Depends(db.get_db)):
    """GET /api/itens  ou  GET /api/itens?status=concluido"""
    # TODO (fase 4)
    raise NotImplementedError("TODO fase 4: GET /api/itens")


# TODO (fase 4): agora escreva SOZINHA as três rotas abaixo, seguindo o
# modelo das de cima. Os testes em tests/test_fase4_rotas.py dizem
# exatamente o que cada uma deve responder.
#
#   GET    /api/itens/{item_id}  -> devolve o item (ItemSalvo), ou 404 se não existir
#   PUT    /api/itens/{item_id}  -> corpo ItemAtualizacao; altera e devolve o item, ou 404
#                                   dica: item.model_dump(exclude_unset=True) devolve
#                                   só os campos que o front realmente mandou
#   DELETE /api/itens/{item_id}  -> remove e responde 204 sem corpo, ou 404
#                                   dica: return Response(status_code=204)


# TODO (fase 7, opcional): GET /api/recomendacoes — veja docs/fase-7-ia.md
# Enquanto essa rota não existir, o botão "O que escolher hoje?" fica
# escondido no site (o front recebe 404 e entende que não tem).


# ---------------------------------------------------------------------------
# Serve o front-end (pasta /frontend). Já está pronto e precisa ficar
# por ÚLTIMO, senão ele "engole" as rotas /api.
# ---------------------------------------------------------------------------
PASTA_FRONTEND = Path(__file__).resolve().parents[2] / "frontend"
app.mount("/", StaticFiles(directory=PASTA_FRONTEND, html=True), name="frontend")
