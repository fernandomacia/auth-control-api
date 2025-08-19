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

A ready-to-use Docker image bundles the API, database, and seeded users.
Download it and run the service without any additional setup:

```bash
docker pull ghcr.io/fernandomacia/auth-control-api:latest
docker run -p 8000:8000 ghcr.io/fernandomacia/auth-control-api:latest
```

The image exposes the following endpoints:

| Method | Endpoint           | Description                    |
|--------|--------------------|--------------------------------|
| GET    | `/health`          | Health check                   |
| POST   | `/login`           | Obtain JWT token               |
| PUT    | `/users/me`        | Update current user's language |
| PATCH  | `/users/{user_id}` | Partial user update (admin)    |
| GET    | `/users/examples`  | List seeded example users      |

All responses follow the standard `success`/`message`/`data` JSON structure.

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
