# Fase 6 — Trocando de tema (opcional)

**Objetivo:** provar na prática a ideia do projeto: escrever um provedor novo **sem mexer em mais nada** e ver o app inteiro mudar de tema.

## Parte A — Open Library (livros)

**Arquivo:** [`backend/app/provedores/openlibrary.py`](../backend/app/provedores/openlibrary.py) — o arquivo tem as URLs e um mapeamento sugerido.

1. Explore no navegador:
   - https://openlibrary.org/search.json?q=duna&limit=10
   - https://openlibrary.org/works/OL893414W.json
2. Implemente `buscar` e `detalhe`. Agora **ninguém** te dá o mapeamento pronto: olhe o JSON e decida.
3. **Escreva você mesma os testes** em `tests/test_fase6_openlibrary.py`, copiando o estilo de `test_fase2_tvmaze.py`. Salve exemplos de JSON em `tests/dados/`.
4. No `.env`, troque para `PROVEDOR=openlibrary`, reinicie o servidor e abra o site. 📚

Coisas novas que aparecem aqui:

- **Identificação:** mande o cabeçalho `User-Agent` com nome e e-mail (`config.USER_AGENT`) — com ele, o limite sobe de 1 para 3 requisições por segundo.
- **Imagem montada:** a capa não vem pronta, você monta a URL com o `cover_i`.
- **Campo que muda de tipo:** `description` às vezes é texto, às vezes `{"value": "..."}`.

Repare: o mesmo banco guarda séries **e** livros, porque a tabela tem a coluna `provedor`. A lista do site mostra tudo junto. Isso é um bug ou uma funcionalidade? Discuta na mentoria (e, se quiser, filtre a listagem pelo provedor ativo).

## Parte B — Outra API à sua escolha

Veja [apis-publicas.md](apis-publicas.md). Boas opções:

- **Art Institute of Chicago** — a URL da imagem é montada em duas partes (`config.iiif_url` + `image_id`).
- **Met Museum** — a busca devolve só IDs; você consulta cada obra depois (chamada em duas etapas).
- **iTunes Search** — uma API só para música, podcast, filmes e e-books.

Para registrar um provedor novo, adicione no dicionário `PROVEDORES` em [`app/provedores/__init__.py`](../backend/app/provedores/__init__.py).

## Parte C — TMDB: guardando uma chave de API

O [TMDB](https://developer.themoviedb.org) (filmes e séries) **exige chave**. É o cenário mais comum no mercado.

1. Crie a conta e peça a chave nas configurações (grátis para uso não comercial).
2. Coloque em `TMDB_API_KEY=...` no seu `.env` — **nunca** no código.
3. No provedor, use `config.TMDB_API_KEY`.
4. Antes de cada commit, rode `git status` e confira que o `.env` **não** aparece.
5. Os termos do TMDB exigem creditar com logotipo e a frase de que o produto usa a API mas não é endossado por eles. Use o `credito_texto`/`credito_url`.

> Se uma chave vazar no GitHub (mesmo que você apague depois, ela fica no histórico), **gere uma nova** no site da API. Robôs varrem o GitHub procurando chaves o tempo todo.

## Para conversar na mentoria

- Quantas linhas você mudou **fora** da pasta `provedores/` para trocar de tema? (A resposta ideal é zero.)
- Onde mais você já viu esse padrão de "interface comum + implementações trocáveis"? (Dica: pagamentos, envio de e-mail, armazenamento de arquivos…)
