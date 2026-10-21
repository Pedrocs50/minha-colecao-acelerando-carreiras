# Minha Coleção 📚🎬🎨

Um app web para guardar a **sua coleção** de qualquer coisa — séries, livros, obras de arte, receitas… Você busca os itens numa **API pública** (em vez de digitar tudo à mão), salva na sua lista e marca status, nota e comentário.

O site (front-end) **já está pronto**. A sua missão é construir o **back-end em Python**: conversar com a API externa, guardar os dados num banco SQLite e expor as rotas que o site usa.

## O que você vai aprender

| Assunto | Onde aparece no projeto |
|---|---|
| Como funciona uma API (pedido, resposta, JSON, códigos de status) | Fase 1 e 2 |
| Consumir uma API em Python (`requests`) | Fase 2 |
| Banco de dados e SQL (`sqlite3`) | Fase 3 |
| Criar uma API REST com rotas de CRUD (`FastAPI`) | Fase 4 |
| Tratar erros sem deixar o app quebrar | Fase 5 |
| Esconder diferenças atrás de uma interface comum (um padrão muito usado no mercado) | Fase 6 |
| Guardar chave de API com segurança (`.env`) | Fase 6 (TMDB) e 7 |
| Testes automatizados (`pytest`) | Todas |

Tudo isso é o básico que quase toda pessoa desenvolvedora usa no dia a dia — e dá para mostrar em entrevista.

## Como o app é organizado

```
  Navegador (frontend/ — pronto)
        │  fetch("/api/...")
        ▼
  Rotas (backend/app/main.py)  ◄── fase 4 e 5
        │                 │
        ▼                 ▼
  Banco SQLite        Provedor de dados  ◄── fase 2 e 6
  (app/database.py)   (app/provedores/)
   ◄── fase 3              │  requests.get(...)
                           ▼
                    API pública (TVmaze, Open Library…)
```

A ideia mais importante: **as rotas e o banco não sabem de onde vêm os itens.** Quem sabe é o *provedor*, um pedaço pequeno de código que conversa com uma API específica e sempre devolve os itens **no mesmo formato**:

```json
{
  "id_externo": "169",
  "titulo": "Breaking Bad",
  "subtitulo": "Drama, Crime",
  "ano": 2008,
  "imagem_url": "https://...",
  "descricao": "Um professor de química..."
}
```

Trocar de tema (de séries para livros, por exemplo) = trocar de provedor no arquivo `.env`. O resto continua igual.

## Começando

Siga o passo a passo em **[docs/00-preparando-o-ambiente.md](docs/00-preparando-o-ambiente.md)**. Em resumo:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate        # no Windows (no Mac/Linux: source .venv/bin/activate)
pip install -r requirements.txt
copy .env.example .env        # no Mac/Linux: cp .env.example .env
uvicorn app.main:app --reload
```

Abra http://localhost:8000 — o site vai abrir, mas vai mostrar erros, porque o back-end ainda está cheio de `TODO`. É com você! 🙂

## As fases

Faça na ordem. Cada fase tem um guia, os arquivos para mexer e testes que dizem quando está pronto.

| Fase | Guia | Você mexe em | Pronto quando… |
|---|---|---|---|
| 0 | [Preparando o ambiente](docs/00-preparando-o-ambiente.md) | — | o servidor sobe |
| 1 | [HTTP e APIs](docs/fase-1-http-e-apis.md) | `exploracao/01_primeiro_get.py` | você responde as perguntas do script |
| 2 | [O provedor do TVmaze](docs/fase-2-provedor-tvmaze.md) | `app/provedores/tvmaze.py` | `pytest tests/test_fase2_tvmaze.py` passa |
| 3 | [Banco de dados](docs/fase-3-banco-de-dados.md) | `app/database.py` | `pytest tests/test_fase3_banco.py` passa |
| 4 | [Rotas do CRUD](docs/fase-4-rotas-crud.md) | `app/main.py` | `pytest tests/test_fase4_rotas.py -k "not fase5"` passa e o site funciona |
| 5 | [Erros e validação](docs/fase-5-erros.md) | `app/main.py` | `pytest` inteiro passa ✅ |
| 6 | [Trocando de tema](docs/fase-6-segundo-provedor.md) *(opcional)* | `app/provedores/openlibrary.py` | o app vira uma coleção de livros só mudando o `.env` |
| 7 | [IA: "o que escolher hoje?"](docs/fase-7-ia.md) *(opcional)* | `app/main.py` | o botão aparece e funciona |

Referências que você vai consultar o tempo todo:

- [docs/contrato-da-api.md](docs/contrato-da-api.md) — o que cada rota recebe e devolve
- [docs/apis-publicas.md](docs/apis-publicas.md) — APIs que dá para usar como provedor
- [docs/materiais.md](docs/materiais.md) — materiais de estudo por fase

## Dicas de ouro

- **Rode os testes sempre.** Um teste falhando não é um fracasso, é uma lista do que falta fazer. Leia a mensagem de erro com calma.
- **Use o http://localhost:8000/docs.** O FastAPI gera uma página onde você testa cada rota clicando em "Try it out".
- **Faça commits pequenos** a cada coisa que funcionar (`git add . && git commit -m "fase 2: converter do tvmaze"`).
- **Nunca suba o `.env` para o GitHub.** Ele já está no `.gitignore` — não tire de lá.
- **Travou por mais de 30 minutos?** Anote o que tentou e leve para a mentoria. Saber explicar onde travou já é metade da solução.
