# Fase 1 — Entendendo HTTP e APIs

**Objetivo:** entender o que acontece quando um programa "chama uma API", antes de escrever código de verdade.

## Leia primeiro

- [O que é uma API REST](https://www.redhat.com/pt-br/topics/api/what-is-a-rest-api) (Red Hat, português)
- [Uma visão geral do HTTP](https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Overview) (MDN, português)
- [Métodos de requisição HTTP](https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Methods) (MDN, português)

## Os conceitos em uma página

Uma API web é um combinado: **você manda um pedido (request) para uma URL e recebe uma resposta (response).**

```
PEDIDO                                   RESPOSTA
GET /search/shows?q=girls                200 OK
Host: api.tvmaze.com                     Content-Type: application/json
User-Agent: MinhaColecao/0.1
                                         [{"score": 0.9, "show": {...}}, ...]
```

**Método** — o que você quer fazer:

| Método | Significa | No nosso app |
|---|---|---|
| `GET` | ler | buscar séries, listar a coleção |
| `POST` | criar | adicionar um item |
| `PUT` | alterar | mudar status/nota/comentário |
| `DELETE` | remover | tirar um item da lista |

Esses quatro são o **CRUD** (*Create, Read, Update, Delete*) da web.

**Parâmetros de consulta (query string)** — o que vem depois do `?`: `?q=girls&page=2`.

**JSON** — o formato do corpo da resposta. Em Python, `resposta.json()` vira listas e dicionários.

**Código de status** — o número que diz se deu certo:

| Faixa | Significado | Exemplos |
|---|---|---|
| 2xx | deu certo | `200 OK`, `201 Created`, `204 No Content` |
| 4xx | erro **de quem pediu** | `404 Not Found`, `409 Conflict`, `422` dados inválidos |
| 5xx | erro **do servidor** | `500` erro interno, `502` o servidor dependia de outro que falhou |

**Cabeçalhos (headers)** — informações extras do pedido/resposta. Ex.: `User-Agent` diz quem está pedindo; algumas APIs pedem que você se identifique por ali.

## Mão na massa

1. Abra no **navegador** (é um GET!):
   - https://api.tvmaze.com/search/shows?q=girls
   - https://api.tvmaze.com/shows/169
   - https://api.tvmaze.com/shows/0 (o que acontece?)

   Dica: o Firefox mostra o JSON bonitinho. No Chrome, instale uma extensão de "JSON viewer".

2. Abra as **ferramentas de desenvolvedor** do navegador (F12) → aba **Rede/Network**, recarregue a página e clique no pedido. Encontre: o método, o status e os cabeçalhos.

3. Rode e complete o script [`exploracao/01_primeiro_get.py`](../exploracao/01_primeiro_get.py):

   ```bash
   cd backend
   python ../exploracao/01_primeiro_get.py
   ```

   Material: [Requests: Quickstart](https://requests.readthedocs.io/en/latest/user/quickstart/) (inglês).

## Para conversar na mentoria

- Qual a diferença entre um erro 404 e um erro 500? De quem é a "culpa" em cada um?
- Por que o TVmaze devolve `id` como número, mas o nosso formato usa `id_externo` como texto? (pense em outras APIs: a Open Library usa ids como `"OL893415W"`)
- O que aconteceria com o seu programa se a API demorasse 5 minutos para responder?

## Checklist

- [ ] Sei explicar pedido, resposta, método, status e JSON com as minhas palavras
- [ ] Completei os TODOs do `01_primeiro_get.py`
- [ ] Sei o que acontece quando a internet cai durante um `requests.get`
