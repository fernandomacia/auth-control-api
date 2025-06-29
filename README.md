# 🚀 Auth Control API

**Auth Control API** is a FastAPI-based backend that handles secure authentication, role-based access control (RBAC), and user preferences such as language selection. This project is designed to be modular, extensible, and production-ready.

---

## ✨ Features

- 🔐 JWT-based authentication
- 👥 Role-based user access (`user`, `admin`, `superadmin`)
- 🌐 User language preferences
- 📦 FastAPI + Pydantic architecture
- 🧪 Testing
- ⚙️ Ready to scale with new modules

---

## 🧱 Tech Stack

- Python 3.11.2
- FastAPI
- Pydantic
- Uvicorn
- SQLAlchemy + Alembic
- PostgreSQL
- JWT via `python-jose`
- bcrypt for password hashing 
- Pytest

---

## 🔧 Installation & Run

### 📥 Clone the repository

```bash
git clone https://github.com/fernandomacia/AuthControlApi.git
cd AuthControlApi
```

### 🐍 Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```
### 📦 Install dependencies

```bash
pip install -r requirements.txt
```

### ⚙️ Environment Configuration

Before running the application, create a `.env` file at the root of the project.
You can use the provided `.env.example` as a starting point:

```bash
cp .env.example .env
```
☠️ Do not commit the .env file. It is ignored by .gitignore.
⚠️ Make sure the PostgreSQL server is running and create <your_database>. Then write your credentials into your .env file:

```env
DATABASE_URL=postgresql://<your_user>:<your_password>@localhost:5432/<your_database>
```

🔐 JWT Secret Key Setup. For security reasons, you must provide a strong secret key for JWT signing. This key is used to encode and verify authentication tokens, and should never be hardcoded or weak.
You can generate a secur key using Python:

```bash
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

Once generated, copy the output into your .env file:

```env
JWT_SECRET_KEY=your_generated_secure_key_here
```

### 🛠️ Apply database migrations

```bash
alembic upgrade head
```

### 🌱 Seed initial data (roles, languages, test users)

```bash
python -m app.db.run_seeds
```

### ▶️ Run the development server

```bash
uvicorn app.main:app --reload
```

---

## Example Users

The following example users are automatically created by the seed script:

| Name        | Email                    | Password     | Role        | Language |
|-------------|--------------------------|--------------|-------------|----------|
| Admin       | admin@example.net        | admin        | admin       | en       |
| Superadmin  | superadmin@example.net   | superadmin   | superadmin  | es       |
| User        | user@example.net         | user         | user        | fr       |

⚠️ These accounts are for development and testing purposes only. Do **not** use them in production environments.

## 🧪 Testing

This project includes automated tests using Pytest and FastAPI's TestClient.

To run the test suite:

```bash
pytest
```

📂 Tests are located in the /tests/ directory and use a separate SQLite database stored in:

```text
./tests/databases/test.db
```

**Included tests:**

✅ /login endpoint success and error cases

🧪 Custom fixtures with isolated user, role, and language seeding


✅ Tests are safe to run. They do not affect your development or production data.

