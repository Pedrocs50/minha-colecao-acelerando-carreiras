"""Um provedor de mentira, que não acessa a internet.

Já está pronto. Serve para:
- os testes das rotas (não dependem da internet nem do TVmaze);
- desenvolver o front/back offline (coloque PROVEDOR=falso no .env).

Repare que ele segue exatamente a mesma interface do TVmaze. É por isso
que o resto do app funciona igual com qualquer um dos dois.
"""

from app.provedores.base import Provedor
from app.schemas import Item

ITENS = [
    Item(id_externo="1", titulo="A Série Inventada", subtitulo="Drama", ano=2020,
         descricao="Uma série que só existe nos testes."),
    Item(id_externo="2", titulo="Outra Série", subtitulo="Comédia", ano=2018),
    Item(id_externo="3", titulo="Documentário Teste", subtitulo="Documentário"),
]


class ProvedorFalso(Provedor):
    nome = "falso"
    credito_texto = "Dados de mentira, só para testes"
    credito_url = ""

    def buscar(self, termo: str) -> list[Item]:
        termo = termo.strip().lower()
        if not termo:
            return []
        return [item for item in ITENS if termo in item.titulo.lower()]

    def detalhe(self, id_externo: str) -> Item | None:
        for item in ITENS:
            if item.id_externo == id_externo:
                return item
        return None
