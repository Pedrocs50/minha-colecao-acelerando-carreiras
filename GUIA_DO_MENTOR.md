# Guia do mentor

Notas para quem acompanha o projeto. A mentorada pode ler sem problema — não tem spoiler aqui.

## O desenho do projeto

- **Front-end pronto** (`frontend/`, HTML + JS puro). Ela não precisa mexer, então o foco fica 100% no back-end.
- **Back-end em esqueleto** com `TODO` e docstrings explicando o que cada função faz. O que é "encanamento" (config, conexão, injeção de dependência, schemas, servir o front) já vem pronto e comentado, para ela ler e entender, mas não travar nisso.
- **Testes já escritos** para as fases 2 a 5. Eles são a especificação: quando `pytest` passa inteiro, o MVP está pronto. Na fase 6 ela escreve os próprios testes.
- **Progressão de autonomia:** na fase 2 o mapeamento vem descrito; na 3 os passos vêm em dica; na 4, três rotas vêm com assinatura e três ela escreve do zero; na 6 ela decide o mapeamento e escreve os testes.
- **Provedor falso** (`app/provedores/falso.py`) serve de exemplo de implementação, deixa os testes de rota independentes da internet e permite rodar offline (`PROVEDOR=falso`).

## Ritmo sugerido

| Semana | Fase | Foco da conversa |
|---|---|---|
| 1 | 0 e 1 | ambiente, venv, HTTP, status codes, ler JSON |
| 2 | 2 | requests, timeout, mock nos testes, interface comum |
| 3 | 3 | SQL, `?` vs f-string (SQL injection), commit |
| 4–5 | 4 | FastAPI, `Depends`, contrato front/back, /docs |
| 6 | 5 | erros, 404/409/422/502, mensagens para usuário |
| 7+ | 6 e 7 | opcional: segundo provedor, chave de API, IA |

Ajuste ao ritmo dela. Cada doc de fase termina com "Para conversar na mentoria" — são boas perguntas para abrir a sessão.

## Gabarito

Existe uma solução de referência completa na branch local **`gabarito`** (todos os testes passando).

```bash
git diff main gabarito -- backend/app      # ver só a solução
git checkout gabarito                      # rodar a versão pronta
```

> **Antes de compartilhar o repositório com ela**, decida o que fazer com essa branch. Se for subir para o GitHub, faça `git push origin main` (só a main) — ou apague a branch com `git branch -D gabarito` depois de guardar uma cópia. Se ela clonar um repo que tem o gabarito, o desafio perde a graça.

## Pontos de atenção (para revisar no código dela)

- `?` em todo SQL — nenhum f-string com valor.
- `timeout` em todo `requests.get`.
- Nenhum `except:` "pelado" engolindo erro — capturar `requests.RequestException`, não `Exception`.
- `.env` fora do Git (`git status` antes de cada commit).
- Mensagens de erro amigáveis no `detail`, sem stack trace.
- Créditos das APIs no rodapé (o front já mostra; ela só precisa preencher `credito_texto`/`credito_url` em provedores novos).

## Se quiser estender

- Filtrar a listagem pelo provedor ativo (hoje séries e livros aparecem juntos se ela trocar o provedor).
- Paginação no `GET /api/itens`.
- Cache das buscas (para respeitar limites de API).
- GitHub Actions rodando o `pytest` a cada push — ótimo para o portfólio.
- Deploy (Render, Railway, Fly.io…) — lembrar das regras de crédito e de que a chave de teste do TheMealDB não vale para app publicado.
