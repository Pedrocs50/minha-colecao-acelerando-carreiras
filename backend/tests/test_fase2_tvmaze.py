"""Testes da FASE 2: o provedor do TVmaze.

Estes testes NÃO acessam a internet. Eles trocam o requests.get por uma
função falsa (monkeypatch) que devolve um JSON de exemplo salvo em
tests/dados/. Assim o teste é rápido e não quebra se o TVmaze cair.

Rode com:  pytest tests/test_fase2_tvmaze.py
"""

import pytest
import requests

from app.provedores import tvmaze
from app.provedores.base import ErroProvedor
from app.provedores.tvmaze import ProvedorTVmaze, converter
from tests.conftest import RespostaFalsa, carregar_json


@pytest.fixture
def chamadas(monkeypatch):
    """Troca requests.get por uma versão falsa e guarda como ela foi chamada.

    No teste: chamadas.resposta = RespostaFalsa(...) define o que o
    "requests.get" vai devolver (ou uma exceção, que ele vai lançar);
    chamadas.lista guarda cada chamada como (url, kwargs).
    """

    class Registro:
        resposta = RespostaFalsa(200, [])
        lista = []

    def get_falso(url, **kwargs):
        Registro.lista.append((url, kwargs))
        if isinstance(Registro.resposta, Exception):
            raise Registro.resposta
        return Registro.resposta

    monkeypatch.setattr(tvmaze.requests, "get", get_falso)
    return Registro


# --- converter() -----------------------------------------------------------

def test_converter_serie_completa():
    show = carregar_json("tvmaze_detalhe.json")
    item = converter(show)
    assert item.id_externo == "169"  # string, não int!
    assert item.titulo == "Breaking Bad"
    assert item.subtitulo == "Drama, Crime, Thriller"
    assert item.ano == 2008
    assert item.imagem_url.endswith("1253519.jpg")
    assert "medium_portrait" in item.imagem_url
    assert item.descricao.startswith("Breaking Bad follows")
    assert "<" not in item.descricao  # sem tags HTML


def test_converter_serie_sem_imagem_sem_data_sem_generos():
    show = carregar_json("tvmaze_busca.json")[1]["show"]
    item = converter(show)
    assert item.id_externo == "99999"
    assert item.titulo == "Série Obscura"
    assert item.subtitulo is None
    assert item.ano is None
    assert item.imagem_url is None
    assert item.descricao is None


# --- buscar() --------------------------------------------------------------

def test_buscar_devolve_itens_no_formato_unico(chamadas):
    chamadas.resposta = RespostaFalsa(200, carregar_json("tvmaze_busca.json"))
    itens = ProvedorTVmaze().buscar("breaking")
    assert [i.titulo for i in itens] == ["Breaking Bad", "Série Obscura"]


def test_buscar_chama_a_url_certa_com_parametros_e_timeout(chamadas):
    ProvedorTVmaze().buscar("breaking")
    url, kwargs = chamadas.lista[0]
    assert url == "https://api.tvmaze.com/search/shows"
    assert kwargs["params"] == {"q": "breaking"}
    assert kwargs.get("timeout"), "sempre passe um timeout!"


def test_buscar_termo_vazio_nao_chama_a_api(chamadas):
    assert ProvedorTVmaze().buscar("   ") == []
    assert chamadas.lista == []


def test_buscar_sem_resultados(chamadas):
    chamadas.resposta = RespostaFalsa(200, [])
    assert ProvedorTVmaze().buscar("xyzxyzxyz") == []


def test_buscar_api_com_erro_lanca_erro_provedor(chamadas):
    chamadas.resposta = RespostaFalsa(500, None)
    with pytest.raises(ErroProvedor):
        ProvedorTVmaze().buscar("breaking")


def test_buscar_sem_internet_lanca_erro_provedor(chamadas):
    chamadas.resposta = requests.ConnectionError("sem internet")
    with pytest.raises(ErroProvedor):
        ProvedorTVmaze().buscar("breaking")


# --- detalhe() -------------------------------------------------------------

def test_detalhe_devolve_um_item(chamadas):
    chamadas.resposta = RespostaFalsa(200, carregar_json("tvmaze_detalhe.json"))
    item = ProvedorTVmaze().detalhe("169")
    assert item.titulo == "Breaking Bad"
    url, _ = chamadas.lista[0]
    assert url == "https://api.tvmaze.com/shows/169"


def test_detalhe_inexistente_devolve_none(chamadas):
    chamadas.resposta = RespostaFalsa(404, {"name": "Not Found"})
    assert ProvedorTVmaze().detalhe("0") is None


def test_detalhe_timeout_lanca_erro_provedor(chamadas):
    chamadas.resposta = requests.Timeout("demorou demais")
    with pytest.raises(ErroProvedor):
        ProvedorTVmaze().detalhe("169")
