# employer-api

API em **FastAPI** para gestão de usuários e perfis (SQLite + SQLModel) com autenticação JWT.

## Requisitos

- Python 3.11+ (recomendado)
- `pip`

## Setup (macOS/Linux)

1) Criar e ativar o ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate
```

2) Instalar dependências:

```bash
pip install -r requirements.txt
```

3) Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto (ou ajuste o existente) com, no mínimo:

```env
SECRET_KEY="sua-chave-secreta" // pode usa a de fallback que tá em "config.py"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
ENABLE_SEED=true

# Seed de dados (recomendado somente em DEV)
ENABLE_SEED=true
```

Observações:
- `ENABLE_SEED=true` cria usuários/perfis de exemplo no startup (útil para desenvolvimento). Em produção, deixe `ENABLE_SEED=false`.

## Executando o projeto

Na raiz do projeto:

```bash
uvicorn src.main:app --reload
```

A API sobe por padrão em:

- http://127.0.0.1:8000
- Swagger: http://127.0.0.1:8000/docs

## Banco de dados

O projeto usa SQLite no arquivo `database.db` na raiz.

Para “resetar” o banco (DEV):

```bash
rm -f database.db
```

Para acessa o banco:

```bash
sqlite3 database.db
```

Para sair do banco:

```bash
.exit
```

Na próxima inicialização, as tabelas serão recriadas automaticamente.

## Autenticação (JWT)

- Endpoint de login: `POST /auth/token`
- O Swagger permite autenticar via botão **Authorize** (Bearer token).

Exemplo via curl:

```bash
curl -X POST http://127.0.0.1:8000/auth/token \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=admin&password=admin123'
```

A resposta contém `access_token`. Use assim:

```bash
TOKEN="<cole-o-token-aqui>"
curl http://127.0.0.1:8000/perfis \
  -H "Authorization: Bearer $TOKEN"
```

## Endpoints principais

- `POST /auth/token` (login)
- `GET /perfis` (lista/busca perfis; requer auth)
  - Parâmetros opcionais:
    - `query`: busca textual (nome, sobrenome, usuário, email, departamento)
    - `departamento`: filtra por departamento (somente SUPER)
- `POST /perfis` (cria usuário + perfil; requer auth)
- `PUT /perfis/{perfil_id}` (atualiza campos do perfil; requer auth)
- `DELETE /perfis/{perfil_id}` (remove perfil; requer auth)

## Regras de permissão (resumo)

- `SUPER`:
  - Pode listar todos os perfis
  - Pode filtrar por `departamento` e buscar por `query`
- `GESTOR`:
  - Só lista/busca perfis do próprio departamento (não consegue filtrar outro departamento)
- `FUNCIONARIO`:
  - Não pode listar perfis

## Notas

- Os usuários de seed e senhas padrão existem para facilitar desenvolvimento. Evite usar `ENABLE_SEED=true` em produção.
