"""Testes da FASE 3: as funções do banco de dados (app/database.py).

Cada teste recebe `conn`, um banco novinho e vazio (veja conftest.py).
Rode com:  pytest tests/test_fase3_banco.py
"""

import sqlite3

import pytest

from app import database as db


def dados_exemplo(**mudancas) -> dict:
    dados = {
        "id_externo": "169",
        "titulo": "Breaking Bad",
        "subtitulo": "Drama, Crime",
        "ano": 2008,
        "imagem_url": None,
        "descricao": "Um professor de química...",
        "status": "quero",
        "nota": None,
        "comentario": None,
    }
    dados.update(mudancas)
    return dados


def test_inserir_devolve_item_com_id_e_data(conn):
    item = db.inserir_item(conn, "tvmaze", dados_exemplo())
    assert isinstance(item, dict)
    assert item["id"] >= 1
    assert item["titulo"] == "Breaking Bad"
    assert item["provedor"] == "tvmaze"
    assert item["status"] == "quero"
    assert item["criado_em"]


def test_inserir_o_mesmo_item_duas_vezes_da_erro(conn):
    db.inserir_item(conn, "tvmaze", dados_exemplo())
    with pytest.raises(sqlite3.IntegrityError):
        db.inserir_item(conn, "tvmaze", dados_exemplo())


def test_mesmo_id_externo_em_provedores_diferentes_pode(conn):
    db.inserir_item(conn, "tvmaze", dados_exemplo())
    db.inserir_item(conn, "openlibrary", dados_exemplo())
    assert len(db.listar_itens(conn)) == 2


def test_listar_vazio(conn):
    assert db.listar_itens(conn) == []


def test_listar_do_mais_novo_para_o_mais_antigo(conn):
    db.inserir_item(conn, "tvmaze", dados_exemplo(id_externo="1", titulo="Primeiro"))
    db.inserir_item(conn, "tvmaze", dados_exemplo(id_externo="2", titulo="Segundo"))
    titulos = [i["titulo"] for i in db.listar_itens(conn)]
    assert titulos == ["Segundo", "Primeiro"]


def test_listar_filtrando_por_status(conn):
    db.inserir_item(conn, "tvmaze", dados_exemplo(id_externo="1", status="quero"))
    db.inserir_item(conn, "tvmaze", dados_exemplo(id_externo="2", status="concluido"))
    db.inserir_item(conn, "tvmaze", dados_exemplo(id_externo="3", status="concluido"))
    concluidos = db.listar_itens(conn, status="concluido")
    assert len(concluidos) == 2
    assert all(i["status"] == "concluido" for i in concluidos)
    assert all(isinstance(i, dict) for i in concluidos)


def test_buscar_item_existente(conn):
    novo = db.inserir_item(conn, "tvmaze", dados_exemplo())
    achado = db.buscar_item(conn, novo["id"])
    assert achado == novo


def test_buscar_item_inexistente(conn):
    assert db.buscar_item(conn, 999) is None


def test_atualizar_so_os_campos_enviados(conn):
    novo = db.inserir_item(conn, "tvmaze", dados_exemplo(comentario="quero muito"))
    atualizado = db.atualizar_item(conn, novo["id"], {"status": "concluido", "nota": 5})
    assert atualizado["status"] == "concluido"
    assert atualizado["nota"] == 5
    assert atualizado["comentario"] == "quero muito"  # não mexeu
    assert db.buscar_item(conn, novo["id"])["nota"] == 5  # salvou mesmo


def test_atualizar_sem_campos_devolve_o_item(conn):
    novo = db.inserir_item(conn, "tvmaze", dados_exemplo())
    assert db.atualizar_item(conn, novo["id"], {}) == novo


def test_atualizar_inexistente(conn):
    assert db.atualizar_item(conn, 999, {"nota": 3}) is None


def test_remover(conn):
    novo = db.inserir_item(conn, "tvmaze", dados_exemplo())
    assert db.remover_item(conn, novo["id"]) is True
    assert db.buscar_item(conn, novo["id"]) is None


def test_remover_inexistente(conn):
    assert db.remover_item(conn, 999) is False
