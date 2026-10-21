# Fase 2 — O provedor do TVmaze

**Objetivo:** escrever o código que conversa com a API do TVmaze e devolve os itens no nosso formato único.

**Arquivo:** [`backend/app/provedores/tvmaze.py`](../backend/app/provedores/tvmaze.py)
**Testes:** `pytest tests/test_fase2_tvmaze.py`

## Antes de começar, leia (já estão prontos)

1. [`app/schemas.py`](../backend/app/schemas.py) — a classe `Item` é o formato único.
2. [`app/provedores/base.py`](../backend/app/provedores/base.py) — a "interface comum": todo provedor tem `buscar(termo)` e `detalhe(id_externo)`.
3. [`app/provedores/falso.py`](../backend/app/provedores/falso.py) — um provedor completo e simples, de exemplo.

## O que fazer

Três funções, nesta ordem:

### 1. `converter(show)`

Recebe um dicionário com uma série do TVmaze e devolve um `Item`. Toda a "tradução" fica aqui. O docstring da função tem o mapeamento campo a campo.

Teste só ela primeiro:

```bash
pytest tests/test_fase2_tvmaze.py -k converter
```

Pegadinhas que os testes verificam:

- `id` é número no TVmaze, mas `id_externo` é texto → `str(...)`
- `genres` pode ser `[]`, `premiered` pode ser `null`, `image` pode ser `null`
- `summary` vem com HTML → use a `limpar_html()` que já está pronta

### 2. `buscar(termo)`

```python
resposta = requests.get(url, params={...}, headers={...}, timeout=TIMEOUT)
```

- Termo vazio → `[]` **sem** chamar a API (por que gastar uma chamada?)
- A resposta é uma lista de `{"score": ..., "show": {...}}` — você só quer o `show`
- Erros de rede (`requests.RequestException`) ou status diferente de 200 → `raise ErroProvedor("...")`

### 3. `detalhe(id_externo)`

Igual ao buscar, mas com uma pegadinha: **404 não é erro do app**, só quer dizer "essa série não existe" → devolva `None`.

## Como os testes funcionam sem internet?

Abra [`tests/test_fase2_tvmaze.py`](../backend/tests/test_fase2_tvmaze.py). A fixture `chamadas` usa o `monkeypatch` do pytest para **trocar o `requests.get` por uma função falsa** que devolve o JSON salvo em `tests/dados/`. Assim:

- o teste é rápido;
- não quebra se o TVmaze estiver fora do ar;
- dá para simular erros (500, sem internet, timeout) que seriam difíceis de provocar de verdade.

Essa técnica se chama *mock* e é muito usada no mercado.

## Veja funcionando de verdade

Com os testes passando, rode o servidor (`uvicorn app.main:app --reload`) e no terminal Python:

```python
from app.provedores.tvmaze import ProvedorTVmaze
p = ProvedorTVmaze()
p.buscar("the office")
p.detalhe("526")
```

## Atenção às regras do TVmaze

- **Limite:** pelo menos 20 chamadas a cada 10 segundos por IP. Não faça loops chamando a API sem parar.
- **Licença CC BY-SA:** é obrigatório citar o TVmaze com link. O site já faz isso no rodapé, usando `credito_texto` e `credito_url` do provedor.

## Para conversar na mentoria

- Por que é o **provedor** que lança `ErroProvedor`, e não ele que devolve um erro 502 direto?
- O que é um `timeout` e o que acontece sem ele?
- Por que separar `converter()` em uma função própria facilita os testes?

## Checklist

- [ ] `pytest tests/test_fase2_tvmaze.py` passa inteiro
- [ ] Testei de verdade no terminal Python com uma série que eu gosto
- [ ] Fiz commit
