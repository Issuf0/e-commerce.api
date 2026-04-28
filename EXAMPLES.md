# 📬 Exemplos de Requisições — Bruno / Postman

Base URL: `http://localhost:8000`

Para endpoints autenticados, use o header:
```
Authorization: Bearer {{token}}
```
Onde `{{token}}` é o `access_token` retornado no `POST /auth/login`.

---

## 🟢 Health

### `GET /`
- **Auth:** não
- **Headers:** —
- **Body:** —

**Response 200**
```json
{ "status": "ok", "service": "ecommerce-api" }
```

---

## 🔑 Auth

### `POST /auth/login`
- **Auth:** não
- **Headers:** `Content-Type: application/json`

**Body — admin (criado automaticamente)**
```json
{
  "email": "admin@ecommerce.com",
  "password": "admin123"
}
```

**Body — cliente (após registo)**
```json
{
  "email": "maria@ex.com",
  "password": "senha123"
}
```

**Response 200**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

> Copie o `access_token` e use como Bearer nas próximas chamadas.

---

## 👥 Users

### `POST /users` — registar cliente
- **Auth:** público
- **Headers:** `Content-Type: application/json`

**Body**
```json
{
  "name": "Maria Silva",
  "email": "maria@ex.com",
  "password": "senha123"
}
```

**Response 201**
```json
{
  "id": 2,
  "name": "Maria Silva",
  "email": "maria@ex.com",
  "is_admin": false,
  "is_active": true,
  "created_at": "2026-04-27T22:15:00"
}
```

---

### `GET /users` — listar usuários (admin)
- **Auth:** Bearer (admin)
- **Query params (opcionais):** `skip=0&limit=100`

**Exemplo:** `GET http://localhost:8000/users?skip=0&limit=10`

**Response 200**
```json
[
  {
    "id": 1,
    "name": "Admin",
    "email": "admin@ecommerce.com",
    "is_admin": true,
    "is_active": true,
    "created_at": "2026-04-27T22:00:00"
  },
  {
    "id": 2,
    "name": "Maria Silva",
    "email": "maria@ex.com",
    "is_admin": false,
    "is_active": true,
    "created_at": "2026-04-27T22:15:00"
  }
]
```

---

### `GET /users/me` — meus dados
- **Auth:** Bearer (qualquer usuário autenticado)

**Response 200**
```json
{
  "id": 2,
  "name": "Maria Silva",
  "email": "maria@ex.com",
  "is_admin": false,
  "is_active": true,
  "created_at": "2026-04-27T22:15:00"
}
```

---

### `GET /users/{id}` — detalhe (admin)
- **Auth:** Bearer (admin)
- **Path param:** `id`

**Exemplo:** `GET http://localhost:8000/users/2`

---

### `PUT /users/{id}` — atualizar tudo (admin)
- **Auth:** Bearer (admin)
- **Headers:** `Content-Type: application/json`

**Body**
```json
{
  "name": "Maria Costa",
  "email": "maria.costa@ex.com",
  "password": "novaSenha123"
}
```

---

### `PATCH /users/{id}` — atualizar parcialmente (admin)
- **Auth:** Bearer (admin)
- **Headers:** `Content-Type: application/json`

**Body — só o nome**
```json
{ "name": "Maria C." }
```

**Body — desativar conta**
```json
{ "is_active": false }
```

**Body — só nova senha**
```json
{ "password": "outraSenha456" }
```

---

### `DELETE /users/{id}` — remover (admin)
- **Auth:** Bearer (admin)

**Exemplo:** `DELETE http://localhost:8000/users/2`

**Response 204** (sem corpo)

---

## 📦 Products

### `GET /products` — listar
- **Auth:** público
- **Query params (opcionais):** `skip=0&limit=100&q=camis`

**Exemplos:**
- `GET http://localhost:8000/products`
- `GET http://localhost:8000/products?q=camis&limit=5`

**Response 200**
```json
[
  {
    "id": 1,
    "name": "Camiseta Branca",
    "description": "100% algodão",
    "price": 59.9,
    "stock": 20,
    "created_at": "2026-04-27T22:30:00"
  }
]
```

---

### `GET /products/{id}` — detalhe
- **Auth:** público

**Exemplo:** `GET http://localhost:8000/products/1`

---

### `POST /products` — criar (admin)
- **Auth:** Bearer (admin)
- **Headers:** `Content-Type: application/json`

**Body**
```json
{
  "name": "Camiseta Branca",
  "description": "100% algodão",
  "price": 59.90,
  "stock": 20
}
```

**Response 201**
```json
{
  "id": 1,
  "name": "Camiseta Branca",
  "description": "100% algodão",
  "price": 59.9,
  "stock": 20,
  "created_at": "2026-04-27T22:30:00"
}
```

---

### `PUT /products/{id}` — substituir tudo (admin)
- **Auth:** Bearer (admin)
- **Headers:** `Content-Type: application/json`

**Body**
```json
{
  "name": "Camiseta Preta",
  "description": "Algodão pima",
  "price": 79.90,
  "stock": 15
}
```

---

### `PATCH /products/{id}` — parcial (admin)
- **Auth:** Bearer (admin)
- **Headers:** `Content-Type: application/json`

**Body — só preço**
```json
{ "price": 49.90 }
```

**Body — só estoque (reposição)**
```json
{ "stock": 100 }
```

**Body — preço + estoque**
```json
{ "price": 49.90, "stock": 80 }
```

---

### `DELETE /products/{id}` — remover (admin)
- **Auth:** Bearer (admin)

**Exemplo:** `DELETE http://localhost:8000/products/1`

**Response 204** (sem corpo)

---

## 🧾 Orders

### `GET /orders` — listar
- **Auth:** Bearer
- **Comportamento:** admin vê todos; cliente vê apenas os seus.

**Exemplo:** `GET http://localhost:8000/orders`

**Response 200**
```json
[
  {
    "id": 1,
    "user_id": 2,
    "status": "PENDING",
    "total": 119.8,
    "created_at": "2026-04-27T22:45:00",
    "items": [
      { "id": 1, "product_id": 1, "quantity": 2, "unit_price": 59.9 }
    ]
  }
]
```

---

### `GET /orders/{id}` — detalhe
- **Auth:** Bearer (dono do pedido ou admin)

**Exemplo:** `GET http://localhost:8000/orders/1`

---

### `POST /orders` — criar pedido
- **Auth:** Bearer (qualquer autenticado)
- **Headers:** `Content-Type: application/json`
- **Comportamento:** debita estoque e calcula `total` automaticamente.

**Body — 1 item**
```json
{
  "items": [
    { "product_id": 1, "quantity": 2 }
  ]
}
```

**Body — múltiplos itens**
```json
{
  "items": [
    { "product_id": 1, "quantity": 2 },
    { "product_id": 3, "quantity": 1 }
  ]
}
```

**Response 201**
```json
{
  "id": 1,
  "user_id": 2,
  "status": "PENDING",
  "total": 119.8,
  "created_at": "2026-04-27T22:45:00",
  "items": [
    { "id": 1, "product_id": 1, "quantity": 2, "unit_price": 59.9 }
  ]
}
```

**Erros comuns**
- `404` — produto não encontrado: `{"detail": "Produto 99 não encontrado"}`
- `400` — estoque insuficiente: `{"detail": "Estoque insuficiente para o produto 'Camiseta Branca'"}`

---

### `PUT /orders/{id}/status` — substituir status (admin)
- **Auth:** Bearer (admin)
- **Headers:** `Content-Type: application/json`

**Body**
```json
{ "status": "paid" }
```

Valores aceitos: `pending`, `paid`, `shipped`, `delivered`, `cancelled`.

---

### `PATCH /orders/{id}/status` — atualizar status (admin)
- **Auth:** Bearer (admin)
- **Headers:** `Content-Type: application/json`

**Body — marcar como pago**
```json
{ "status": "paid" }
```

**Body — marcar como enviado**
```json
{ "status": "shipped" }
```

**Body — cancelar**
```json
{ "status": "cancelled" }
```

---

### `DELETE /orders/{id}` — remover (admin)
- **Auth:** Bearer (admin)

**Exemplo:** `DELETE http://localhost:8000/orders/1`

**Response 204** (sem corpo)

---

## 🧪 Fluxo completo recomendado para testar

1. `POST /auth/login` com admin → guarda `access_token` numa variável `{{token}}`.
2. `POST /products` → cria 2-3 produtos (admin).
3. `POST /users` → registra um cliente (`maria@ex.com`).
4. `POST /auth/login` como cliente → guarda outro token (`{{token_cliente}}`).
5. `POST /orders` (com `{{token_cliente}}`) → cria um pedido.
6. `GET /orders` (com `{{token_cliente}}`) → confere que vê só os seus.
7. `PATCH /orders/1/status` (com `{{token}}` admin) → muda status para `paid`.
8. `GET /products/1` → confirma que o estoque foi debitado.

---

## 💡 Dicas para Bruno/Postman

- **Variável de ambiente `baseUrl`:** `http://localhost:8000`
- **Variável `token`:** copie do response do login.
- **Pré-script (Postman) para salvar token automaticamente:**
  ```js
  pm.environment.set("token", pm.response.json().access_token);
  ```
- **Bruno (Vars → Post-Response):**
  ```js
  bru.setEnvVar("token", res.body.access_token);
  ```
