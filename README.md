# 🛒 E-commerce API

API REST simples de e-commerce construída com **FastAPI**, **SQLAlchemy** e **JWT**.
Inclui gestão de usuários, produtos e pedidos, com autenticação via Bearer Token e perfis `admin` e `cliente`.

---

## 📁 Estrutura do projeto

```
app/
├── config/        # Conexão com DB e settings (.env)
├── models/        # Modelos SQLAlchemy
├── schemas/       # Pydantic (validação)
├── routes/        # Definição de rotas (APIRouter)
├── controllers/   # Agrupamento de rotas por lógica
├── services/      # Lógica de negócio (Auth, User, etc.)
├── utils/         # Ferramentas (Security, Helpers)
└── main.py        # Ponto de entrada
```

---

## 🚀 Como inicializar

### 1. Pré-requisitos

- Python **3.10+**
- `pip` instalado
- **MySQL** ou **MariaDB** rodando localmente (porta `3306`)
- Uma base de dados chamada `e_commerce` (criada automaticamente pelo passo 7 ou manualmente: `CREATE DATABASE e_commerce CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`)

### 2. Clonar e entrar na pasta

```bash
cd e-commerce
```

### 3. Criar e ativar um ambiente virtual

```bash
python -m venv .venv
source .venv/bin/activate     # Linux/Mac
# .venv\Scripts\activate      # Windows
```

### 4. Instalar dependências

```bash
pip install -r requirements.txt
```

### 5. Configurar variáveis de ambiente

Copie o arquivo de exemplo e ajuste se necessário:

```bash
cp .env.example .env
```

| Variável | Descrição | Padrão |
|---|---|---|
| `DATABASE_URL` | URL do banco (SQLAlchemy) | `mysql+pymysql://root:Zuleca@localhost:3306/e_commerce` |
| `SECRET_KEY` | Chave secreta usada para assinar JWT | *altere em produção* |
| `ALGORITHM` | Algoritmo do JWT | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Validade do token | `60` |

### 6. Rodar o servidor

```bash
uvicorn app.main:app --reload
```

A API ficará disponível em **http://localhost:8000**.

### 7. Documentação interativa

- Swagger UI: **http://localhost:8000/docs**
- ReDoc: **http://localhost:8000/redoc**

---

## 👤 Usuário admin padrão

Na primeira inicialização um admin é criado automaticamente:

| Campo | Valor |
|---|---|
| Email | `admin@ecommerce.com` |
| Senha | `admin123` |

> ⚠️ Altere essa senha em produção.

---

## 🔐 Autenticação

A API usa **JWT (Bearer Token)**. O fluxo é:

1. Faça login em `POST /auth/login` para receber um `access_token`.
2. Envie o token no cabeçalho de todas as rotas protegidas:

```
Authorization: Bearer <seu_token>
```

No Swagger UI clique no botão **Authorize** e cole o token.

---

## 📚 Endpoints

Todos os endpoints respondem em JSON. Cada recurso suporta os métodos: **GET**, **POST**, **PUT**, **PATCH** e **DELETE**.

### 🔑 Auth

| Método | Rota | Descrição | Auth |
|---|---|---|---|
| `POST` | `/auth/login` | Autentica e retorna JWT | público |

### 👥 Usuários (`/users`)

| Método | Rota | Descrição | Auth |
|---|---|---|---|
| `POST` | `/users` | Registra um novo usuário (cliente) | público |
| `GET` | `/users` | Lista todos os usuários | admin |
| `GET` | `/users/me` | Dados do usuário logado | autenticado |
| `GET` | `/users/{id}` | Detalhe de um usuário | admin |
| `PUT` | `/users/{id}` | Substitui dados do usuário (full update) | admin |
| `PATCH` | `/users/{id}` | Atualização parcial (nome, email, senha, status) | admin |
| `DELETE` | `/users/{id}` | Remove o usuário | admin |

### 📦 Produtos (`/products`)

| Método | Rota | Descrição | Auth |
|---|---|---|---|
| `GET` | `/products` | Lista produtos (`?q=` busca por nome) | público |
| `GET` | `/products/{id}` | Detalhe de um produto | público |
| `POST` | `/products` | Cria um produto | admin |
| `PUT` | `/products/{id}` | Substitui um produto (full update) | admin |
| `PATCH` | `/products/{id}` | Atualização parcial (ex.: só estoque) | admin |
| `DELETE` | `/products/{id}` | Remove o produto | admin |

### 🧾 Pedidos (`/orders`)

| Método | Rota | Descrição | Auth |
|---|---|---|---|
| `GET` | `/orders` | Lista pedidos (admin vê todos; cliente vê os seus) | autenticado |
| `GET` | `/orders/{id}` | Detalhe de um pedido | dono ou admin |
| `POST` | `/orders` | Cria um pedido (debita estoque automaticamente) | autenticado |
| `PUT` | `/orders/{id}/status` | Substitui o status (full) | admin |
| `PATCH` | `/orders/{id}/status` | Atualiza parcialmente o status | admin |
| `DELETE` | `/orders/{id}` | Remove um pedido | admin |

Status possíveis: `pending`, `paid`, `shipped`, `delivered`, `cancelled`.

---

## 🧪 Exemplos rápidos (cURL)

### Login

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@ecommerce.com","password":"admin123"}'
```

### Registrar cliente

```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Maria","email":"maria@ex.com","password":"senha123"}'
```

### Criar produto (admin)

```bash
curl -X POST http://localhost:8000/products \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Camiseta","description":"Algodão","price":59.90,"stock":20}'
```

### Atualizar apenas o estoque (PATCH)

```bash
curl -X PATCH http://localhost:8000/products/1 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"stock":50}'
```

### Criar um pedido

```bash
curl -X POST http://localhost:8000/orders \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"items":[{"product_id":1,"quantity":2}]}'
```

### Atualizar status de um pedido

```bash
curl -X PATCH http://localhost:8000/orders/1/status \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status":"paid"}'
```

---

## 🧩 Como a API é organizada

Cada camada tem uma responsabilidade clara:

- **`config/`** — Carrega settings (`.env`) e inicializa a engine/sessão do SQLAlchemy.
- **`models/`** — Mapeamento ORM (User, Product, Order, OrderItem).
- **`schemas/`** — Pydantic para entrada/saída e validação.
- **`services/`** — Regras de negócio (validação, transações, integração com o ORM).
- **`controllers/`** — Wrappers que orquestram services e expõem métodos para as rotas.
- **`routes/`** — `APIRouter` para cada recurso, declara HTTP method, path e dependências.
- **`utils/`** — Hash de senha, JWT, dependências de autenticação/autorização.
- **`main.py`** — Cria a app, registra os routers, sobe o banco e cria o admin inicial.

Fluxo de uma requisição:

```
HTTP Request
  → routes/*  (endpoint, valida path/query/body via schemas)
  → controllers/*  (chama o service apropriado)
  → services/*  (regra de negócio + transação)
  → models/*  (SQLAlchemy)
  → DB
```

---

## 🛠️ Próximos passos

- Adicionar paginação rica (limit/offset com metadados).
- Adicionar Alembic para migrações versionadas.
- Adicionar testes com `pytest` + `httpx`.
- Adicionar Docker e GitHub Actions.

---

## 📄 Licença

MIT.
