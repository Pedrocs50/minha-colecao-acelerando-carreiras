# Fase 0 — Preparando o ambiente

## Você vai precisar

- **Python 3.11 ou mais novo** — confira com `python --version`
- **Git** — confira com `git --version`
- Um editor (recomendo o **VS Code** com a extensão *Python*)

## Passo a passo

Todos os comandos abaixo são rodados **dentro da pasta `backend`**.

### 1. Ambiente virtual (venv)

Um *venv* é uma "caixinha" com as bibliotecas só deste projeto, para não misturar com as de outros projetos.

```bash
cd backend
python -m venv .venv
```

Ative a caixinha (você vai fazer isso **toda vez** que abrir um terminal novo):

```bash
# Windows (PowerShell)
.venv\Scripts\activate

# Mac / Linux
source .venv/bin/activate
```

Deu certo se aparecer `(.venv)` no começo da linha do terminal.

> **Windows:** se o PowerShell reclamar de "execução de scripts desabilitada", rode uma vez:
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

| Biblioteca | Para quê |
|---|---|
| `fastapi` | criar as rotas da API |
| `uvicorn` | o servidor que roda o FastAPI |
| `requests` | chamar APIs externas |
| `python-dotenv` | ler o arquivo `.env` |
| `pytest` + `httpx` | testes |

### 3. Crie o seu `.env`

```bash
# Windows
copy .env.example .env
# Mac / Linux
cp .env.example .env
```

Abra o `.env` e coloque o seu e-mail em `CONTATO_EMAIL`. Esse arquivo guarda configurações e, mais para frente, **segredos** (chaves de API). Por isso ele está no `.gitignore` e **nunca** vai para o GitHub. O `.env.example` (sem segredos) é que fica no repositório, para mostrar quais variáveis existem.

### 4. Suba o servidor

```bash
uvicorn app.main:app --reload
```

- http://localhost:8000 → o site
- http://localhost:8000/docs → a documentação automática da API

O `--reload` faz o servidor reiniciar sozinho quando você salva um arquivo. Para parar: `Ctrl + C`.

O site vai abrir, mas com mensagens de erro em laranja. **É esperado!** O back-end ainda é só esqueleto.

### 5. Rode os testes

```bash
pytest
```

Quase tudo vai falhar com `NotImplementedError: TODO fase X`. Também é esperado. Ao longo do projeto você vai ver esse número de falhas cair até zero. 🎯

## Estrutura de pastas

```
backend/
  app/
    main.py            ← rotas (fase 4, 5, 7)
    database.py        ← banco SQLite (fase 3)
    schemas.py         ← formatos dos dados (pronto, leia!)
    config.py          ← lê o .env (pronto)
    provedores/
      base.py          ← a interface comum (pronto, leia!)
      tvmaze.py        ← fase 2
      openlibrary.py   ← fase 6
      falso.py         ← provedor de mentira para testes (pronto)
  tests/               ← os testes de cada fase
frontend/              ← o site (pronto, não precisa mexer)
exploracao/            ← scripts para brincar (fase 1)
docs/                  ← estes guias
```

## Checklist

- [ ] `python --version` mostra 3.11+
- [ ] O venv está ativado (`(.venv)` no terminal)
- [ ] `pip install -r requirements.txt` rodou sem erro
- [ ] Existe um arquivo `backend/.env`
- [ ] http://localhost:8000/docs abre
- [ ] `pytest` roda (mesmo com falhas)
