# Fase 7 — "O que escolher hoje?" (opcional)

**Objetivo:** criar a rota `GET /api/recomendacoes`. Assim que ela existir, o botão **"O que escolher hoje?"** aparece sozinho no site.

## O formato da resposta

```json
{
  "item": { ...um ItemSalvo... },
  "motivo": "Você deu nota 5 para dramas policiais, e este está na sua lista há 3 semanas."
}
```

`item` pode ser `null` se não houver o que sugerir — aí o site mostra só o `motivo`.

## Passo 1 — sem IA

Comece simples, para ter algo funcionando:

- Pegue os itens com status `quero` e sorteie um (`random.choice`).
- Se não houver nenhum, devolva `{"item": null, "motivo": "Adicione itens com status 'Quero conhecer' primeiro."}`.
- Escreva um teste em `tests/test_fase7_recomendacoes.py`.

## Passo 2 — com IA

Agora use um modelo de linguagem (LLM) para escolher **e explicar** a escolha:

1. Monte um texto (*prompt*) com o que a pessoa já concluiu e deu nota alta, e com os itens que ela quer conhecer.
2. Peça ao modelo que escolha **um** dos itens da lista "quero" e explique em uma frase.
3. Peça a resposta em JSON (ex.: `{"id": 12, "motivo": "..."}`) e **confira** se o id existe mesmo — modelos às vezes inventam.

Coisas que você vai praticar:

- **Chave de API no `.env`** (de novo, e agora ela custa dinheiro se vazar!).
- **SDK oficial** do provedor de IA escolhido (por exemplo, o da Anthropic para usar o Claude) — leia a documentação oficial para ver o modelo atual e como fazer a chamada.
- **Tratamento de erro:** se a IA falhar ou demorar, caia no sorteio do passo 1 em vez de quebrar.
- **Testes sem gastar:** troque a chamada da IA por uma função falsa nos testes (igual fizemos com o `requests.get`).

## Para conversar na mentoria

- Que dados da usuária você está mandando para um serviço externo? Isso é ok?
- Como garantir que a resposta da IA está num formato que o seu código entende?
- Quanto custaria se 1.000 pessoas clicassem no botão por dia?
