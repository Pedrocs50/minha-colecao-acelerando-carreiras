"""Configurações do app, lidas do arquivo .env.

Este arquivo já está pronto. Leia para entender como o python-dotenv
carrega variáveis de ambiente — é assim que guardamos segredos (como
chaves de API) sem colocar no código.
"""

import os

from dotenv import load_dotenv

# Lê o arquivo .env (se existir) e coloca os valores em os.environ
load_dotenv()

PROVEDOR = os.getenv("PROVEDOR", "tvmaze")
DB_PATH = os.getenv("DB_PATH", "colecao.db")
CONTATO_EMAIL = os.getenv("CONTATO_EMAIL", "")
TMDB_API_KEY = os.getenv("TMDB_API_KEY", "")

# Nome que o app usa para se identificar nas APIs (cabeçalho User-Agent)
USER_AGENT = f"MinhaColecao/0.1 ({CONTATO_EMAIL or 'sem-contato'})"
