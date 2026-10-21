"""Testes das FASES 4 e 5: as rotas da API (app/main.py).

Aqui o `cliente` faz requisições HTTP de verdade para o app, mas usando
o provedor FALSO (sem internet) e um banco temporário (veja conftest.py).

Rode com:  pytest tests/test_fase4_rotas.py
Só os da fase 5:  pytest tests/test_fase4_rotas.py -k fase5
"""

from app.provedores import get_provedor
from app.provedores.base import ErroProvedor
from app.provedores.falso import ProvedorFalso
from app.main import app

NOVO = {
    "id_externo": "1",
    "titulo": "A Série Inventada",
    "subtitulo": "Drama",
    "ano": 2020,
    "status": "quero",
}


def criar(cliente, **mudancas):
    resposta = cliente.post("/api/itens", json={**NOVO, **mudancas})
    assert resposta.status_code == 201, resposta.text
    return resposta.json()


# --- exemplo pronto ----------------------------------------------------------

def test_provedor_ativo(cliente):
    resposta = cliente.get("/api/provedor")
    assert resposta.status_code == 200
    assert resposta.json()["nome"] == "falso"


# --- FASE 4: GET /api/buscar -----------------------------------------------

def test_buscar(cliente):
    resposta = cliente.get("/api/buscar", params={"q": "série"})
    assert resposta.status_code == 200
    titulos = [i["titulo"] for i in resposta.json()]
    assert titulos == ["A Série Inventada", "Outra Série"]


def test_buscar_sem_termo_devolve_lista_vazia(cliente):
    resposta = cliente.get("/api/buscar")
    assert resposta.status_code == 200
    assert resposta.json() == []


# --- FASE 4: POST /api/itens -----------------------------------------------

def test_criar_item(cliente):
    item = criar(cliente, nota=4, comentario="recomendação da Ana")
    assert item["id"] >= 1
    assert item["titulo"] == "A Série Inventada"
    assert item["nota"] == 4
    assert item["comentario"] == "recomendação da Ana"
    assert item["provedor"] == "falso"


def test_criar_item_sem_status_usa_quero(cliente):
    corpo = {k: v for k, v in NOVO.items() if k != "status"}
    resposta = cliente.post("/api/itens", json=corpo)
    assert resposta.status_code == 201
    assert resposta.json()["status"] == "quero"


# --- FASE 4: GET /api/itens ------------------------------------------------

def test_listar_itens(cliente):
    criar(cliente, id_externo="1")
    criar(cliente, id_externo="2", status="concluido")
    resposta = cliente.get("/api/itens")
    assert resposta.status_code == 200
    assert len(resposta.json()) == 2


def test_listar_itens_filtrando_status(cliente):
    criar(cliente, id_externo="1")
    criar(cliente, id_externo="2", status="concluido")
    resposta = cliente.get("/api/itens", params={"status": "concluido"})
    assert [i["id_externo"] for i in resposta.json()] == ["2"]


# --- FASE 4: GET /api/itens/{id} -------------------------------------------

def test_pegar_um_item(cliente):
    item = criar(cliente)
    resposta = cliente.get(f"/api/itens/{item['id']}")
    assert resposta.status_code == 200
    assert resposta.json() == item


# --- FASE 4: PUT /api/itens/{id} -------------------------------------------

def test_atualizar_item(cliente):
    item = criar(cliente, comentario="ainda não vi")
    resposta = cliente.put(f"/api/itens/{item['id']}", json={"status": "concluido", "nota": 5})
    assert resposta.status_code == 200
    atualizado = resposta.json()
    assert atualizado["status"] == "concluido"
    assert atualizado["nota"] == 5
    assert atualizado["comentario"] == "ainda não vi"  # não mudou


# --- FASE 4: DELETE /api/itens/{id} ----------------------------------------

def test_remover_item(cliente):
    item = criar(cliente)
    resposta = cliente.delete(f"/api/itens/{item['id']}")
    assert resposta.status_code == 204
    assert resposta.content == b""
    assert cliente.get(f"/api/itens/{item['id']}").status_code == 404


# --- FASE 5: erros e validação ----------------------------------------------
# Um app profissional nunca responde 500 ("deu ruim") para erros previsíveis.

def test_fase5_item_inexistente_da_404(cliente):
    assert cliente.get("/api/itens/999").status_code == 404
    assert cliente.put("/api/itens/999", json={"nota": 3}).status_code == 404
    assert cliente.delete("/api/itens/999").status_code == 404


def test_fase5_item_repetido_da_409(cliente):
    criar(cliente)
    resposta = cliente.post("/api/itens", json=NOVO)
    assert resposta.status_code == 409
    assert resposta.json()["detail"]  # tem uma mensagem explicando


def test_fase5_nota_fora_de_1_a_5_da_422(cliente):
    assert cliente.post("/api/itens", json={**NOVO, "nota": 10}).status_code == 422
    item = criar(cliente)
    assert cliente.put(f"/api/itens/{item['id']}", json={"nota": 0}).status_code == 422


def test_fase5_status_invalido_da_422(cliente):
    resposta = cliente.post("/api/itens", json={**NOVO, "status": "talvez"})
    assert resposta.status_code == 422


def test_fase5_provedor_fora_do_ar_da_502(cliente):
    class ProvedorQuebrado(ProvedorFalso):
        def buscar(self, termo):
            raise ErroProvedor("A API não respondeu")

    app.dependency_overrides[get_provedor] = lambda: ProvedorQuebrado()
    resposta = cliente.get("/api/buscar", params={"q": "qualquer"})
    assert resposta.status_code == 502
    assert resposta.json()["detail"]
