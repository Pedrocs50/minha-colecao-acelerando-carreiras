"""Configurações compartilhadas pelos testes (fixtures do pytest).

Já está pronto. Uma "fixture" é algo que o pytest prepara antes de cada
teste — basta colocar o nome dela como parâmetro da função de teste.
"""

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app import database as db
from app.main import app
from app.provedores import get_provedor
from app.provedores.falso import ProvedorFalso

PASTA_DADOS = Path(__file__).parent / "dados"


def carregar_json(nome: str):
    """Lê um JSON de exemplo da pasta tests/dados."""
    return json.loads((PASTA_DADOS / nome).read_text(encoding="utf-8"))


class RespostaFalsa:
    """Imita o objeto que o requests.get() devolve, sem ir à internet."""

    def __init__(self, status_code: int = 200, dados=None):
        self.status_code = status_code
        self._dados = dados
        self.ok = 200 <= status_code < 400

    def json(self):
        return self._dados

    def raise_for_status(self):
        import requests

        if not self.ok:
            raise requests.HTTPError(f"{self.status_code} Error")


@pytest.fixture
def conn(tmp_path):
    """Uma conexão com um banco NOVO e vazio, num arquivo temporário."""
    conexao = db.conectar(str(tmp_path / "teste.db"))
    yield conexao
    conexao.close()


@pytest.fixture
def cliente(conn):
    """Um cliente HTTP para testar as rotas, usando o provedor falso e
    o banco temporário no lugar dos de verdade."""
    app.dependency_overrides[get_provedor] = lambda: ProvedorFalso()
    app.dependency_overrides[db.get_db] = lambda: conn
    yield TestClient(app)
    app.dependency_overrides.clear()
