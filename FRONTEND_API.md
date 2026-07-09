# Expense Tracker API — Frontend Documentation

Base URL: `http://localhost:8000`

Interactive docs: `http://localhost:8000/docs`

CORS is enabled for:
- `http://localhost:3000`
- `http://127.0.0.1:3000`

---

## Authentication

The API uses **JWT bearer tokens**. After signup or login, store the `access_token` and send it on protected requests (when route protection is added).

### Sign Up

Create a new user account.

**Endpoint:** `POST /auth/signup`

**Request body:**

```json
{
  "email": "user@example.com",
  "password": "secret123"
}
```

| Field      | Type   | Required | Rules              |
|------------|--------|----------|--------------------|
| `email`    | string | yes      | Valid email format |
| `password` | string | yes      | Minimum 6 characters |

**Success response:** `201 Created`

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": 1,
  "email": "user@example.com"
}
```

**Error responses:**

| Status | When |
|--------|------|
| `400`  | Email is already registered |
| `422`  | Invalid email or password too short |

---

### Login

Sign in with an existing account.

**Endpoint:** `POST /auth/login`

**Request body:**

```json
{
  "email": "user@example.com",
  "password": "secret123"
}
```

**Success response:** `200 OK`

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": 1,
  "email": "user@example.com"
}
```

**Error responses:**

| Status | When |
|--------|------|
| `401`  | Invalid email or password |
| `422`  | Invalid request body |

---

### Using the token

Store the token after signup/login (e.g. `localStorage` or a secure cookie):

```javascript
localStorage.setItem("access_token", data.access_token);
localStorage.setItem("user_id", data.user_id);
localStorage.setItem("email", data.email);
```

Send it on authenticated requests:

```javascript
const token = localStorage.getItem("access_token");

fetch("http://localhost:8000/expenses", {
  headers: {
    Authorization: `Bearer ${token}`,
    "Content-Type": "application/json",
  },
});
```

Tokens expire after **24 hours**.

---

## Frontend examples

### Sign up

```javascript
async function signUp(email, password) {
  const response = await fetch("http://localhost:8000/auth/signup", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Sign up failed");
  }

  return response.json();
}
```

### Login

```javascript
async function login(email, password) {
  const response = await fetch("http://localhost:8000/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Login failed");
  }

  return response.json();
}
```

### Axios setup (optional)

```javascript
import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export async function signUp(email, password) {
  const { data } = await api.post("/auth/signup", { email, password });
  return data;
}

export async function login(email, password) {
  const { data } = await api.post("/auth/login", { email, password });
  return data;
}
```

---

## Expenses

### List expenses

**Endpoint:** `GET /expenses`

**Query params (optional):**

| Param      | Type   | Example      | Description |
|------------|--------|--------------|-------------|
| `category` | string | `Food`       | Filter by category |
| `date`     | string | `2026-06-22` | Filter by date (YYYY-MM-DD) |

**Response:** `200 OK`

```json
[
  {
    "id": 1,
    "title": "Groceries",
    "amount": 45.5,
    "category": "Food",
    "date": "2026-06-22",
    "description": "Weekly shopping"
  }
]
```

---

### Get one expense

**Endpoint:** `GET /expenses/{expense_id}`

**Response:** `200 OK` — single expense object

**Errors:** `404` if not found

---

### Create expense

**Endpoint:** `POST /expenses`

**Request body:**

```json
{
  "title": "Groceries",
  "amount": 45.5,
  "category": "Food",
  "date": "2026-06-22",
  "description": "Weekly shopping"
}
```

| Field         | Type   | Required | Rules |
|---------------|--------|----------|-------|
| `title`       | string | yes      | — |
| `amount`      | number | yes      | Must be > 0 |
| `category`    | string | yes      | — |
| `date`        | string | yes      | YYYY-MM-DD |
| `description` | string | no       | Defaults to `""` |

**Response:** `201 Created`

```json
{
  "message": "Expense created successfully"
}
```

---

### Update expense

**Endpoint:** `PUT /expenses/{expense_id}`

**Request body:** Same shape as create expense.

**Response:** `200 OK`

```json
{
  "message": "Expense updated successfully"
}
```

**Errors:** `404` if not found

---

### Delete expense

**Endpoint:** `DELETE /expenses/{expense_id}`

**Response:** `200 OK`

```json
{
  "message": "Expense deleted successfully"
}
```

**Errors:** `404` if not found

---

## Dashboard

### Summary

**Endpoint:** `GET /dashboard/summary`

**Response:**

```json
{
  "totalExpenses": 1250.75,
  "totalTransactions": 42,
  "averageExpense": 29.78,
  "topCategory": "Food"
}
```

---

### Recent expenses

**Endpoint:** `GET /dashboard/recent`

**Response:**

```json
[
  {
    "id": 5,
    "title": "Coffee",
    "amount": 4.5
  }
]
```

Returns up to 5 most recent expenses.

---

### Category summary

**Endpoint:** `GET /dashboard/category-summary`

**Response:**

```json
[
  {
    "category": "Food",
    "total": 450.0
  },
  {
    "category": "Travel",
    "total": 320.0
  }
]
```

---

## Categories

### List categories

**Endpoint:** `GET /categories`

**Response:**

```json
[
  "Food",
  "Travel",
  "Shopping",
  "Bills",
  "Entertainment",
  "Healthcare",
  "Education"
]
```

---

## Error format

Validation and API errors follow this shape:

```json
{
  "detail": "Invalid email or password"
}
```

Validation errors (`422`):

```json
{
  "detail": [
    {
      "loc": ["body", "password"],
      "msg": "String should have at least 6 characters",
      "type": "string_too_short"
    }
  ]
}
```

---

## Suggested frontend flow

1. **Sign up / Login page** — call `/auth/signup` or `/auth/login`, save token and user info.
2. **Protected routes** — redirect to login if no token is stored.
3. **Dashboard page** — fetch `/dashboard/summary`, `/dashboard/recent`, `/dashboard/category-summary`.
4. **Expenses page** — fetch `/expenses`, support create/update/delete.
5. **Category dropdown** — populate from `/categories`.

---

## Quick reference

| Method | Endpoint                    | Description        |
|--------|-----------------------------|--------------------|
| POST   | `/auth/signup`              | Create account     |
| POST   | `/auth/login`               | Sign in            |
| GET    | `/expenses`                 | List expenses      |
| GET    | `/expenses/{id}`            | Get expense        |
| POST   | `/expenses`                 | Create expense     |
| PUT    | `/expenses/{id}`            | Update expense     |
| DELETE | `/expenses/{id}`            | Delete expense     |
| GET    | `/dashboard/summary`        | Dashboard totals   |
| GET    | `/dashboard/recent`         | Recent expenses    |
| GET    | `/dashboard/category-summary` | Totals by category |
| GET    | `/categories`               | List categories    |
