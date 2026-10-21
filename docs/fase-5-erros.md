# Fase 5 — Erros e validação

**Objetivo:** o app **nunca** pode quebrar com erro 500 por causa de algo previsível. Cada problema vira uma resposta clara, com o código de status certo.

**Arquivo:** [`backend/app/main.py`](../backend/app/main.py)
**Testes:** `pytest tests/test_fase4_rotas.py -k fase5` — e depois `pytest` inteiro ✅

## Os casos

| Situação | Quem detecta | Resposta |
|---|---|---|
| Item com esse id não existe | o banco devolve `None` / `False` | `404` |
| Item já está na coleção | `sqlite3.IntegrityError` | `409` |
| Nota 10, status "talvez" | o Pydantic, sozinho | `422` (de graça!) |
| API externa fora do ar / lenta | `ErroProvedor` | `502` |

Para responder um erro no FastAPI:

```python
from fastapi import HTTPException

raise HTTPException(status_code=404, detail="Item não encontrado")
```

O `detail` aparece para a usuária na caixa laranja do site. Escreva mensagens que **ajudem**, como "Esse item já está na sua coleção", e não "IntegrityError: UNIQUE constraint failed".

## Repare no 422

Você não escreveu nada para validar a nota de 1 a 5 — está em `schemas.py`:

```python
nota: Optional[int] = Field(default=None, ge=1, le=5)
```

Teste no /docs mandando `"nota": 10` e leia a resposta: o FastAPI explica exatamente qual campo está errado.

## Teste "na vida real"

- Desligue o Wi-Fi e busque algo no site. O que aparece?
- Adicione a mesma série duas vezes.
- No /docs, chame `GET /api/itens/99999`.

## Para conversar na mentoria

- Por que 502 e não 500 quando o TVmaze cai?
- Por que mostrar o erro técnico do Python para a usuária é ruim (inclusive para segurança)?
- O que mais poderia dar errado que os testes ainda não cobrem? (ex.: o TVmaze mudar o formato do JSON)

## Checklist

- [ ] `pytest` passa **inteiro** 🎉
- [ ] Nenhuma ação no site gera erro 500
- [ ] Fiz commit — e esse é um ótimo momento para subir o projeto no GitHub e colocar no portfólio
