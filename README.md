# Auth Control API

Auth Control API is a FastAPI backend that provides JWT authentication,
role-based access control and user preferences such as language selection.
It is intended as a foundation for projects that require a lightweight and
extensible auth service.

## Features

- JWT-based login with configurable expiry
- Roles: `user`, `admin`, and `superadmin`
- Endpoint for updating the authenticated user's language
- Admin endpoints for managing user status, role and language
- Example users endpoint for quick testing
- Comprehensive test suite with Pytest

## Tech Stack

- Python 3.11
- FastAPI & Pydantic
- SQLAlchemy & Alembic
- PostgreSQL
- JWT via [python-jose](https://python-jose.readthedocs.io/)
- bcrypt for password hashing
- Pytest

## Prebuilt Docker Image

A prebuilt **Compose stack** (PostgreSQL + migrations + seeds + API) is available.

### Prerequisites

- **Docker Engine** ≥ 20.10  
- **Docker Compose v2** (the `docker compose` plugin)

Check versions:

```bash
docker --version
docker compose version
```

**Linux quick install (Debian/Ubuntu):**

```bash
sudo apt-get update
sudo apt-get install -y docker.io docker-compose-plugin
```

**Windows quick install (PowerShell):**

Requirements: Windows 10 2004+ or Windows 11 with virtualization enabled.

Install WSL 2 (if not already enabled) and reboot if prompted:

```powershell
wsl --install
```

Install Docker Desktop:

```powershell
winget install -e --id Docker.DockerDesktop
```

Launch Docker Desktop once to finish setup (WSL 2 backend is the default).

### Run with one-liners

Download the compose file from the latest release and start the stack:

```bash
curl -fsSLO https://github.com/fernandomacia/auth-control-api/releases/latest/download/docker-compose.yml
docker compose up -d
```

### The stack exposes

PostgreSQL at localhost:55432 (inside the network it’s db:5432)
API at http://localhost:8000 with the following endpoints:

| Method | Endpoint           | Description                    |
|--------|--------------------|--------------------------------|
| GET    | `/health`          | Health check                   |
| POST   | `/login`           | Obtain JWT token               |
| PUT    | `/users/me`        | Update current user's language |
| PATCH  | `/users/{user_id}` | Partial user update (admin)    |
| GET    | `/users/examples`  | List seeded example users      |

All responses follow the standard `success`/`message`/`data` JSON structure.

### Stop the stack

```bash
docker compose down
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/fernandomacia/AuthControlApi.git
cd AuthControlApi
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the sample environment file and adjust values as needed:

```bash
cp .env.example .env
```

Required values include your database connection and JWT settings, e.g.:

```env
DATABASE_URL=postgresql://USER:PASSWORD@localhost:5432/DBNAME
JWT_SECRET_KEY=<generated secret>
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
ALLOWED_ORIGINS=http://localhost:3000
```

Generate a secure secret key:

```bash
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

### 5. Apply database migrations and seed data

```bash
alembic upgrade head
python -m app.db.run_seeds
```

### 6. Run the development server

```bash
uvicorn app.main:app --reload
```

## Example Users

The seed script creates several accounts for quick testing:

| Name        | Email                    | Password            | Role        | Language | Active |
|-------------|--------------------------|---------------------|-------------|----------|--------|
| Superadmin  | superadmin@example.net   | superadminPassword  | superadmin  | es       | true   |
| Admin       | admin@example.net        | adminPassword       | admin       | en       | true   |
| User        | user@example.net         | userPassword        | user        | fr       | true   |
| Inactive    | inactive@example.net     | inactivePassword    | user        | es       | false  |

These accounts are meant for development only. Do **not** use them in
production environments.

## Testing

Run the tests with:

```bash
pytest
```

The suite uses a temporary SQLite database located at
`tests/databases/test.db` and will not interfere with your development data.
