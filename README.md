# 🚀 Auth Control API

**Auth Control API** is a FastAPI-based backend that handles secure authentication, role-based access control (RBAC), and user preferences such as language selection. This project is designed to be modular, extensible, and production-ready.

---

## ✨ Features

- 🔐 JWT-based authentication
- 👥 Role-based user access (`user`, `admin`, `superadmin`)
- 🌐 User language preferences
- 📦 FastAPI + Pydantic architecture
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
- `Passlib` for password hashing

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

Before running the application, create a `.env` file at the root of the project with the next structure:
**DATABASE_URL=postgresql://<your_user>:<your_password>@localhost:5432/<your_database>**

You can use the provided `.env.example` as a starting point:

```bash
cp .env.example .env
```

⚠️ Make sure the PostgreSQL server is running and the database exists.
☠️ Do not commit the .env file. It is ignored by .gitignore.

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

## 🧪 Example Users for Testing

The following example users are automatically created by the seed script:

| Name        | Email                    | Password     | Role        | Language |
|-------------|--------------------------|--------------|-------------|----------|
| Admin       | admin@example.net        | admin        | admin       | en       |
| Superadmin  | superadmin@example.net   | superadmin   | superadmin  | es       |
| User        | user@example.net         | user         | user        | fr       |

⚠️ These accounts are for development and testing purposes only. Do **not** use them in production environments.
