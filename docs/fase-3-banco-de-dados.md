# Fase 3 — Banco de dados (SQLite)

**Objetivo:** guardar a coleção num banco de dados, com as quatro operações do CRUD em SQL.

**Arquivo:** [`backend/app/database.py`](../backend/app/database.py)
**Testes:** `pytest tests/test_fase3_banco.py`

## Estude antes

- [SQLBolt](https://sqlbolt.com/) (inglês, interativo) — faça pelo menos as lições 1 a 4, 13, 14 e 15 (SELECT, WHERE, ORDER BY, INSERT, UPDATE, DELETE).
- [Módulo sqlite3](https://docs.python.org/pt-br/3/library/sqlite3.html) (português) — leia o tutorial do começo da página.

## O que já está pronto

- A tabela `itens` (`SQL_CRIAR_TABELA`). Leia coluna por coluna.
- `conectar()` — abre o banco e cria a tabela se não existir.
- `get_db()` — entrega uma conexão para cada requisição (você vai entender na fase 4).
- `agora()` — a data/hora para o campo `criado_em`.

Repare na linha `UNIQUE (provedor, id_externo)`: o banco **se recusa** a guardar o mesmo item duas vezes. Quem garante a regra é o banco, não o seu código.

## O que fazer

Cinco funções, cada uma com o passo a passo no docstring. Sugestão de ordem:

1. `buscar_item` (a mais simples: um `SELECT ... WHERE id = ?`)
2. `inserir_item` (usa a `buscar_item` no final)
3. `listar_itens`
4. `remover_item`
5. `atualizar_item` (a mais difícil)

Rode um teste por vez:

```bash
pytest tests/test_fase3_banco.py -k buscar
```

## Exemplo para se inspirar

```python
cursor = conn.execute(
    "SELECT * FROM itens WHERE status = ? ORDER BY id DESC",
    (status,),   # ← uma tupla! repare na vírgula
)
linhas = cursor.fetchall()
return [dict(linha) for linha in linhas]
```

## ⚠️ SQL injection

**Nunca** faça isto:

```python
conn.execute(f"SELECT * FROM itens WHERE status = '{status}'")   # ERRADO
```

Se alguém mandar `status = "x' OR '1'='1"`, a consulta muda de sentido. Com `?`, o SQLite trata o valor sempre como **dado**, nunca como **comando**. Pesquise "SQL injection" e "Bobby Tables" — vale a pena.

## Olhando o banco por dentro

O arquivo `colecao.db` aparece na pasta `backend` quando o servidor roda. Para ver o que tem dentro, instale a extensão **SQLite Viewer** no VS Code, ou use o [DB Browser for SQLite](https://sqlitebrowser.org/).

## Para conversar na mentoria

- Por que as funções devolvem `dict` e não `sqlite3.Row`?
- Por que `inserir_item` **não** trata o `IntegrityError`? Quem deveria tratar?
- O que é `conn.commit()` e o que acontece se você esquecer?

## Checklist

- [ ] `pytest tests/test_fase3_banco.py` passa inteiro
- [ ] Nenhum f-string com valores dentro de SQL
- [ ] Fiz commit
