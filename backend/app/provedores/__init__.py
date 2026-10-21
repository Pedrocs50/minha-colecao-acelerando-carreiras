"""Escolhe qual provedor o app vai usar, de acordo com o .env.

Já está pronto. Quando você criar um provedor novo, registre ele no
dicionário PROVEDORES abaixo.
"""

from app import config
from app.provedores.base import ErroProvedor, Provedor
from app.provedores.falso import ProvedorFalso
from app.provedores.openlibrary import ProvedorOpenLibrary
from app.provedores.tvmaze import ProvedorTVmaze

PROVEDORES: dict[str, type[Provedor]] = {
    "tvmaze": ProvedorTVmaze,
    "openlibrary": ProvedorOpenLibrary,
    "falso": ProvedorFalso,
}


def get_provedor() -> Provedor:
    """Devolve o provedor ativo. As rotas recebem ele via Depends()."""
    try:
        classe = PROVEDORES[config.PROVEDOR]
    except KeyError:
        opcoes = ", ".join(PROVEDORES)
        raise RuntimeError(f"PROVEDOR={config.PROVEDOR!r} não existe. Opções: {opcoes}")
    return classe()


__all__ = ["ErroProvedor", "Provedor", "get_provedor", "PROVEDORES"]
