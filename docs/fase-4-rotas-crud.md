# Fase 4 — As rotas do CRUD (FastAPI)

**Objetivo:** juntar provedor + banco e expor tudo como uma API REST que o site consome.

**Arquivo:** [`backend/app/main.py`](../backend/app/main.py)
**Testes:** `pytest tests/test_fase4_rotas.py -k "not fase5"`
**Contrato:** [contrato-da-api.md](contrato-da-api.md)

## Estude antes

[Tutorial do FastAPI em português](https://fastapi.tiangolo.com/pt/tutorial/) — leia:

1. Primeiros passos
2. Parâmetros de path (`/api/itens/{item_id}`)
3. Parâmetros de consulta (`?q=...`, `?status=...`)
4. Corpo da requisição (o JSON do POST/PUT)
5. *Bônus:* Dependências (`Depends`) e Tratamento de erros (`HTTPException`)

> A própria documentação avisa que a tradução foi feita por IA com revisão humana. Se algo parecer estranho, compare com a versão em inglês.

## O que fazer

Em ordem:

1. `GET /api/buscar` — chama `provedor.buscar(q)`
2. `POST /api/itens` — chama `db.inserir_item(...)`
3. `GET /api/itens` — chama `db.listar_itens(...)`
4. **Sozinha, do zero:** `GET`, `PUT` e `DELETE` em `/api/itens/{item_id}`

As três primeiras já têm a "assinatura" pronta. As três últimas você escreve inteiras — os testes dizem o que cada uma precisa responder.

## Como funciona o `Depends`

```python
@app.get("/api/itens")
def listar_itens(conn: sqlite3.Connection = Depends(db.get_db)):
    ...
```

Você não cria a conexão: **pede** uma, e o FastAPI entrega. Nos testes, a gente troca o `get_db` por um banco temporário e o `get_provedor` pelo provedor falso (veja `tests/conftest.py`). É por isso que os testes de rota não acessam a internet nem sujam o seu `colecao.db`.

## Teste de três jeitos

1. **Testes automáticos:** `pytest tests/test_fase4_rotas.py -k "not fase5"`
2. **Página /docs:** http://localhost:8000/docs → abra uma rota → *Try it out* → *Execute*. Veja o status e o JSON.
3. **O site de verdade:** http://localhost:8000 — busque uma série, adicione, edite, filtre, remova. 🎉

## Para conversar na mentoria

- Por que o POST devolve `201` e não `200`? E por que o DELETE devolve `204`?
- O que o `response_model=ItemSalvo` faz? (dica: tente devolver um campo a mais)
- Por que é bom o front-end e o back-end combinarem um "contrato" antes?

## Checklist

- [ ] `pytest tests/test_fase4_rotas.py -k "not fase5"` passa
- [ ] Consigo fazer o CRUD inteiro pelo site
- [ ] Testei pelo menos uma rota pelo /docs
- [ ] Fiz commit
