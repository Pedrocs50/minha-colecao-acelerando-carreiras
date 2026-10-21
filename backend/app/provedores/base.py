"""A "interface comum" que todo provedor de dados precisa seguir.

Este arquivo já está pronto. A ideia central do projeto está aqui:
o resto do app (rotas, banco, front-end) só conhece esta classe.
Trocar de tema = trocar de provedor, sem mexer no resto.
"""

from abc import ABC, abstractmethod

from app.schemas import Item


class ErroProvedor(Exception):
    """Lançada quando a API externa falha (fora do ar, timeout, resposta
    estranha...). As rotas transformam isso em um erro 502 para o front."""


class Provedor(ABC):
    # Nome curto do provedor (o mesmo usado no .env, ex.: "tvmaze")
    nome: str = ""
    # Crédito exigido pelos termos de uso da API (aparece no rodapé do site)
    credito_texto: str = ""
    credito_url: str = ""

    @abstractmethod
    def buscar(self, termo: str) -> list[Item]:
        """Procura itens pelo termo e devolve uma lista no formato único."""

    @abstractmethod
    def detalhe(self, id_externo: str) -> Item | None:
        """Devolve um item pelo id dele na API externa, ou None se não existir."""
