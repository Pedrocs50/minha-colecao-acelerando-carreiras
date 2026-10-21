# Contrato da API

O site (`frontend/`) foi escrito esperando exatamente estas rotas. Se o back-end seguir o contrato, tudo funciona.

Todas as respostas são JSON. Em caso de erro, o corpo é `{"detail": "mensagem"}`.

## Os formatos

**Item** — o formato único que todo provedor devolve:

```json
{
  "id_externo": "169",
  "titulo": "Breaking Bad",
  "subtitulo": "Drama, Crime, Thriller",
  "ano": 2008,
  "imagem_url": "https://static.tvmaze.com/...jpg",
  "descricao": "Breaking Bad follows protagonist Walter White..."
}
```

Só `id_externo` e `titulo` são obrigatórios; o resto pode ser `null`.

**ItemSalvo** — um item na coleção (Item + campos da usuária + campos do banco):

```json
{
  "id": 1,
  "provedor": "tvmaze",
  "id_externo": "169",
  "titulo": "Breaking Bad",
  "subtitulo": "Drama, Crime, Thriller",
  "ano": 2008,
  "imagem_url": "https://...",
  "descricao": "...",
  "status": "concluido",
  "nota": 5,
  "comentario": "Melhor série que já vi",
  "criado_em": "2026-10-21T18:30:00+00:00"
}
```

- `status`: `"quero"` | `"em_andamento"` | `"concluido"` | `"abandonado"`
- `nota`: inteiro de 1 a 5, ou `null`

## As rotas

| Método | Rota | Corpo | Sucesso | Erros |
|---|---|---|---|---|
| GET | `/api/provedor` | — | `200` `{nome, credito_texto, credito_url}` | — |
| GET | `/api/buscar?q=termo` | — | `200` lista de **Item** | `502` API externa falhou |
| POST | `/api/itens` | Item + `status`, `nota`, `comentario` | `201` **ItemSalvo** | `409` já existe, `422` inválido |
| GET | `/api/itens` | — | `200` lista de **ItemSalvo** (mais novo primeiro) | `422` status inválido |
| GET | `/api/itens?status=concluido` | — | `200` só os desse status | |
| GET | `/api/itens/{id}` | — | `200` **ItemSalvo** | `404` |
| PUT | `/api/itens/{id}` | qualquer um de `status`, `nota`, `comentario` | `200` **ItemSalvo** atualizado | `404`, `422` |
| DELETE | `/api/itens/{id}` | — | `204` sem corpo | `404` |
| GET | `/api/recomendacoes` | — | `200` `{item: ItemSalvo \| null, motivo}` | (fase 7, opcional) |

## Exemplos

```http
POST /api/itens
Content-Type: application/json

{
  "id_externo": "169",
  "titulo": "Breaking Bad",
  "subtitulo": "Drama, Crime, Thriller",
  "ano": 2008,
  "status": "quero",
  "nota": null,
  "comentario": "A Ana recomendou"
}
```

```http
PUT /api/itens/1
Content-Type: application/json

{"status": "concluido", "nota": 5}
```

No PUT, **só os campos enviados mudam**. O `comentario` acima continua "A Ana recomendou".
