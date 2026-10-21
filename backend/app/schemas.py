"""Formatos (schemas) dos dados que entram e saem da API.

Este arquivo já está pronto. O FastAPI usa essas classes do Pydantic
para validar o JSON que chega e para documentar a API em /docs.
"""

from typing import Literal, Optional

from pydantic import BaseModel, Field

# Os status possíveis de um item na coleção. Servem para qualquer tema.
Status = Literal["quero", "em_andamento", "concluido", "abandonado"]


class Item(BaseModel):
    """O formato ÚNICO que todo provedor devolve.

    Não importa se os dados vieram do TVmaze, da Open Library ou do
    Art Institute: depois de passar pelo provedor, tudo fica assim.
    """

    id_externo: str
    titulo: str
    subtitulo: Optional[str] = None
    ano: Optional[int] = None
    imagem_url: Optional[str] = None
    descricao: Optional[str] = None


class ItemNovo(Item):
    """O que o front-end manda no POST /api/itens: o item + os campos da Clara."""

    status: Status = "quero"
    nota: Optional[int] = Field(default=None, ge=1, le=5)
    comentario: Optional[str] = None


class ItemAtualizacao(BaseModel):
    """O que o front-end manda no PUT /api/itens/{id}. Tudo é opcional:
    só os campos enviados são alterados."""

    status: Optional[Status] = None
    nota: Optional[int] = Field(default=None, ge=1, le=5)
    comentario: Optional[str] = None


class ItemSalvo(ItemNovo):
    """Um item como ele fica guardado no banco."""

    id: int
    provedor: str
    criado_em: str
