"""Banco de dados (SQLite) — FASE 3.

Material de apoio: https://docs.python.org/pt-br/3/library/sqlite3.html
(o tutorial no começo da página mostra criar tabela, inserir e consultar).

Regras de ouro:
- SEMPRE use "?" para colocar valores no SQL:
      conn.execute("SELECT * FROM itens WHERE id = ?", (item_id,))
  NUNCA monte o SQL com f-string usando valores que vieram de fora
  (isso abre brecha para SQL injection).
- Depois de INSERT/UPDATE/DELETE, chame conn.commit().

Rode os testes desta fase com:
    pytest tests/test_fase3_banco.py
"""

import sqlite3
from datetime import datetime, timezone
from typing import Iterator

from app import config

# A tabela já está desenhada para você. Leia com calma: cada coluna
# corresponde a um campo do Item (do provedor) ou a um campo seu.
SQL_CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS itens (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    provedor    TEXT    NOT NULL,
    id_externo  TEXT    NOT NULL,
    titulo      TEXT    NOT NULL,
    subtitulo   TEXT,
    ano         INTEGER,
    imagem_url  TEXT,
    descricao   TEXT,
    status      TEXT    NOT NULL DEFAULT 'quero',
    nota        INTEGER,
    comentario  TEXT,
    criado_em   TEXT    NOT NULL,
    UNIQUE (provedor, id_externo)  -- o mesmo item não entra duas vezes
)
"""


def conectar(caminho: str = config.DB_PATH) -> sqlite3.Connection:
    """Abre a conexão e garante que a tabela existe. Já está pronto."""
    conn = sqlite3.connect(caminho, check_same_thread=False)
    # Faz cada linha se comportar como um dicionário: linha["titulo"]
    conn.row_factory = sqlite3.Row
    conn.execute(SQL_CRIAR_TABELA)
    return conn


def get_db() -> Iterator[sqlite3.Connection]:
    """Entrega uma conexão para cada requisição e fecha no final.

    Já está pronto. As rotas recebem a conexão com Depends(get_db).
    Nos testes, trocamos isto por um banco temporário.
    """
    conn = conectar()
    try:
        yield conn
    finally:
        conn.close()


def agora() -> str:
    """Data/hora atual em texto (formato ISO). Use no campo criado_em."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


# ---------------------------------------------------------------------------
# A partir daqui é com você!
# Todas as funções devolvem dicionários (dict(linha)), não sqlite3.Row.
# ---------------------------------------------------------------------------


def inserir_item(conn: sqlite3.Connection, provedor: str, dados: dict) -> dict:
    """Insere um item e devolve ele como ficou salvo (com id e criado_em).

    `dados` tem as chaves: id_externo, titulo, subtitulo, ano, imagem_url,
    descricao, status, nota, comentario.

    Se o item já existir (mesmo provedor + id_externo), o SQLite lança
    sqlite3.IntegrityError. NÃO trate aqui: deixe o erro subir, a rota
    é que decide o que responder.

    Dica: depois do INSERT, `cursor.lastrowid` tem o id novo. Use
    buscar_item() para devolver o item completo.
    """
    # TODO (fase 3)
    raise NotImplementedError("TODO fase 3: inserir_item()")


def listar_itens(conn: sqlite3.Connection, status: str | None = None) -> list[dict]:
    """Devolve todos os itens, do mais novo para o mais antigo (ORDER BY id DESC).

    Se `status` vier preenchido, devolve só os itens com aquele status.
    """
    # TODO (fase 3)
    raise NotImplementedError("TODO fase 3: listar_itens()")


def buscar_item(conn: sqlite3.Connection, item_id: int) -> dict | None:
    """Devolve o item com esse id, ou None se não existir.

    Dica: cursor.fetchone() devolve None quando não acha nada.
    """
    # TODO (fase 3)
    raise NotImplementedError("TODO fase 3: buscar_item()")


def atualizar_item(conn: sqlite3.Connection, item_id: int, campos: dict) -> dict | None:
    """Altera só os campos enviados e devolve o item atualizado.

    `campos` é algo como {"status": "concluido", "nota": 5}. Só pode
    conter status, nota e/ou comentario.

    - Se o item não existir, devolva None.
    - Se `campos` estiver vazio, não rode UPDATE: só devolva o item.

    Dica: dá para montar o "SET status = ?, nota = ?" a partir das chaves
    do dicionário — as CHAVES são seguras porque o schema ItemAtualizacao
    já filtrou quais podem chegar; os VALORES continuam indo pelos "?".
    """
    # TODO (fase 3)
    raise NotImplementedError("TODO fase 3: atualizar_item()")


def remover_item(conn: sqlite3.Connection, item_id: int) -> bool:
    """Remove o item. Devolve True se removeu, False se ele não existia.

    Dica: depois do DELETE, cursor.rowcount diz quantas linhas foram apagadas.
    """
    # TODO (fase 3)
    raise NotImplementedError("TODO fase 3: remover_item()")
