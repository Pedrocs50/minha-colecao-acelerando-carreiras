# APIs públicas para usar como provedor

Informações conferidas em 21/10/2026. **Limites e regras mudam: antes de usar, confira a página oficial.**

## Recomendação

1. **Primeiro provedor:** TVmaze — sem chave, sem cadastro, e séries agradam quase todo mundo.
2. **Segundo provedor (opcional):** Open Library ou Art Institute — mostra que trocar de tema não muda o CRUD.
3. **Mais para frente:** TMDB — para aprender a lidar com chave e créditos.

## Resumo

| API | Tema | Chave? | Limite | Atenção |
|---|---|---|---|---|
| [TVmaze](https://www.tvmaze.com/api) | séries | não | ≥ 20 chamadas / 10 s por IP | citar o TVmaze com link (CC BY-SA) |
| [Open Library](https://openlibrary.org/developers/api) | livros | não | 1/s, ou 3/s com `User-Agent` identificado | capas em API separada |
| [iTunes Search](https://performance-partners.apple.com/search-api) | música, podcast, filmes, e-books | não | ~20 / minuto (pode mudar) | uma API, vários temas |
| [Art Institute of Chicago](https://api.artic.edu/docs/) | arte | não | 60 / minuto por IP | mandar `AIC-User-Agent`; URL da imagem montada em duas partes |
| [Met Museum](https://metmuseum.github.io/) | arte (domínio público) | não | 80 / segundo | a busca antiga foi desativada em 01/10/2026 — use `/public/collection/v1.1/search`; busca devolve só IDs |
| [TheMealDB](https://www.themealdb.com/api.php) | receitas | chave de teste `1` | — | para publicar o app é preciso ser apoiador pago |
| [TMDB](https://developer.themoviedb.org) | filmes e séries | **sim** (grátis, não comercial) | — | crédito obrigatório com logo + aviso de não endosso |
| [Jikan](https://jikan.moe) | anime e mangá | não | — | só se você curtir o tema |
| [Google Books](https://developers.google.com/books) | livros | sim (chave ou token) | — | mais trabalhoso que a Open Library |

## Detalhes úteis

### TVmaze
- Busca: `GET https://api.tvmaze.com/search/shows?q=termo`
- Detalhe: `GET https://api.tvmaze.com/shows/{id}`
- Dados: nome, gêneros, estreia, nota, resumo (em HTML) e imagem.

### Open Library
- Busca: `GET https://openlibrary.org/search.json?q=termo`
- Detalhe: `GET https://openlibrary.org/works/{id}.json`
- Capa: `https://covers.openlibrary.org/b/id/{cover_i}-M.jpg`

### iTunes Search
- `GET https://itunes.apple.com/search?term=...&media=music` (ou `podcast`, `movie`, `ebook`)

### Art Institute of Chicago
- `GET https://api.artic.edu/api/v1/artworks/search?q=termo&fields=id,title,artist_display,date_display,image_id`
- Imagem: `{config.iiif_url}/{image_id}/full/843,/0/default.jpg` — o `config.iiif_url` vem na própria resposta.

### Met Museum
- Busca: `/public/collection/v1.1/search?q=termo` → devolve uma lista de IDs
- Depois consulte cada obra pelo ID (chamada em duas etapas — cuidado para não fazer 500 chamadas de uma vez!)

### TheMealDB
- `GET https://www.themealdb.com/api/json/v1/1/search.php?s=termo`

## Para achar outras

[github.com/public-apis/public-apis](https://github.com/public-apis/public-apis) — milhares de APIs públicas por tema, com indicação de quais pedem chave.

## Regras que valem para todas

- **Nunca** coloque chave de API no código ou no GitHub: use o `.env`.
- **Respeite os limites** e se identifique (`User-Agent`) quando a documentação pedir.
- **Dê os créditos** que cada API exige (o site mostra o `credito_texto` do provedor no rodapé).
- **Trate erros:** a API pode cair, demorar ou voltar vazia.
