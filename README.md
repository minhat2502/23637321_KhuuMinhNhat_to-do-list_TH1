# To-Do List API

API quản lý công việc (To-Do List) xây dựng bằng FastAPI, SQLAlchemy và xác thực JWT.

## Yêu cầu

- Python 3.10+

---

## Cách chạy dự án

### 1. Clone & cài đặt

```bash
git clone <repo-url>
cd TH1

# Tạo virtual environment
python -m venv .venv

# Kích hoạt (Windows)
.venv\Scripts\activate

# Cài dependencies
pip install -r requirements.txt
```

### 2. Chạy migration (tạo database)

```bash
alembic upgrade head
```

> Lệnh này tạo file `todos.db` và tất cả các bảng.

### 3. Khởi động server

```bash
uvicorn main:app --reload
```

- API: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## Cách sử dụng API

### Bước 1 — Đăng ký tài khoản

```
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

### Bước 2 — Đăng nhập lấy token

```
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=password123
```

Phản hồi:
```json
{ "access_token": "eyJ...", "token_type": "bearer" }
```

### Bước 3 — Gọi API với token

Thêm header vào mọi request:
```
Authorization: Bearer <access_token>
```

---

## Chạy Tests

```bash
pytest tests/ -v
```

Kết quả mong đợi: **21 passed**

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | FastAPI 0.135 |
| ORM | SQLAlchemy 2.0 |
| Database | SQLite (via Alembic) |
| Auth | JWT (python-jose + bcrypt) |
| Config | pydantic-settings |
| Testing | pytest + httpx |

## Project Structure

```
.
├── main.py
├── core/
│   ├── config.py       # App settings (pydantic-settings)
│   ├── deps.py         # get_current_user dependency
│   └── security.py     # JWT + bcrypt helpers
├── db/
│   ├── models.py       # SQLAlchemy ORM models
│   └── session.py      # Engine, SessionLocal, get_db
├── schemas/
│   ├── todo.py         # Pydantic schemas for todos
│   └── user.py         # Pydantic schemas for users
├── repositories/
│   ├── todo_repo.py    # DB queries for todos
│   └── user_repo.py    # DB queries for users
├── services/
│   ├── todo_service.py # Business logic for todos
│   └── user_service.py # Business logic for users
├── routers/
│   ├── todo_router.py  # /todos routes
│   └── auth_router.py  # /auth routes
├── tests/
│   ├── conftest.py     # Test fixtures
│   ├── test_auth.py    # Auth tests (6 cases)
│   └── test_todos.py   # Todo tests (15 cases)
├── alembic/            # Database migrations
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env
```

## Setup (Local)

```bash
# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/macOS

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start the server
uvicorn main:app --reload
```

API is available at `http://localhost:8000`.  
Interactive docs: `http://localhost:8000/docs`

## Setup (Docker)

```bash
docker-compose up --build
```

Database is persisted in the `./data/` volume.

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_NAME` | `To-Do List API` | Application name |
| `DEBUG` | `False` | Enable debug mode |
| `API_V1_PREFIX` | `/api/v1` | API route prefix |
| `DATABASE_URL` | `sqlite:///./todos.db` | SQLAlchemy DB URL |

## API Endpoints

### Auth

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/auth/register` | Register a new user |
| POST | `/api/v1/auth/login` | Login, get JWT token |
| GET | `/api/v1/auth/me` | Get current user info |

### Todos (requires `Authorization: Bearer <token>`)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/todos` | List todos (filter/sort/paginate) |
| POST | `/api/v1/todos` | Create a todo |
| GET | `/api/v1/todos/overdue` | List overdue todos |
| GET | `/api/v1/todos/today` | List todos due today |
| GET | `/api/v1/todos/{id}` | Get a todo by ID |
| PUT | `/api/v1/todos/{id}` | Full update a todo |
| PATCH | `/api/v1/todos/{id}` | Partial update a todo |
| POST | `/api/v1/todos/{id}/complete` | Mark todo as done |
| DELETE | `/api/v1/todos/{id}` | Delete a todo |

### Query Parameters (GET /todos)

| Param | Type | Description |
|-------|------|-------------|
| `q` | string | Search by title |
| `is_done` | bool | Filter by completion status |
| `sort` | `asc`/`desc` | Sort by creation date |
| `limit` | int | Page size (default 10) |
| `offset` | int | Page offset (default 0) |

## Running Tests

```bash
pytest tests/ -v
```

Expected output: **21 passed**.
