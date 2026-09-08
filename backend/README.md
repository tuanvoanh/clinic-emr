# ClinicCare Mini EMR - Backend API

This is the FastAPI backend for the ClinicCare Mini EMR system. It provides RESTful APIs for managing patients, ICD-10 diagnosis codes, and consultation records.

## Tech Stack
- **Framework**: FastAPI (Python)
- **Database**: SQLite
- **ORM**: SQLAlchemy
- **Data Validation**: Pydantic
- **Migrations**: Alembic

## Project Structure
```text
backend/
├── alembic/              # Database migration scripts
├── app/
│   ├── api/              # API routers and endpoints
│   ├── core/             # Core configurations (database, settings)
│   ├── db/               # Database seeding and utilities
│   ├── models/           # SQLAlchemy models (DB schema)
│   ├── repositories/     # Database operations (Repository pattern)
│   ├── schemas/          # Pydantic schemas (Validation)
│   └── main.py           # FastAPI application entry point
├── alembic.ini           # Alembic configuration
├── requirements.txt      # Python dependencies
└── README.md             # This documentation
```

## Setup Instructions

### 1. Create a Virtual Environment
It is recommended to use a virtual environment to manage dependencies.
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 2. Install Dependencies
Install the required Python packages.
```bash
pip install -r requirements.txt
```

### 3. Database Setup & Migrations
We use Alembic to handle database migrations. Run the following command to apply the latest database schema (this will create `clinic.db`):
```bash
alembic upgrade head
```

**How to handle Database changes:**
Whenever you modify, add, or delete SQLAlchemy models in the `app/models/` directory, you must generate a new migration file and apply it. Follow these two steps:

1. **Auto-generate a new migration script:**
   ```bash
   alembic revision --autogenerate -m "Short description of your change"
   ```
   *(This compares your models with the current DB and creates a new Python script in `alembic/versions/`).*

2. **Apply the migration to the database:**
   ```bash
   alembic upgrade head
   ```
   *(This executes the migration script and updates `clinic.db` with your latest schema changes).*

> **Note:** SQLite's autogenerate functionality might sometimes misinterpret a column rename as a "drop and add" operation. It is best practice to briefly review the generated migration file in `alembic/versions/` before running `upgrade head`.

### 4. Seed Initial Data
The system requires standard ICD-10 codes. Run the seed script to populate the database with a sample set of 100 diagnosis codes:
```bash
python -m app.db.seed_icd10
```

### 5. Run the Server
Start the FastAPI application using Uvicorn.
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
The API will be available at `http://127.0.0.1:8000`.

## API Documentation
FastAPI automatically generates interactive API documentation. Once the server is running, you can access:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Testing

Install all dependencies before running the test suite:

```bash
pip install -r requirements.txt
```

Run all unit and integration tests:

```bash
python -m pytest
```

Run tests with a detailed coverage report:

```bash
python -m pytest --cov=app --cov-report=term-missing
```

The integration tests use an isolated SQLite in-memory database configured in
`tests/conftest.py`. The test schema and data exist only while each test is
running and do not modify the application database at `clinic.db`.

Latest test result:

```text
47 passed
Total coverage: 94%
```

Key coverage results:

```text
app/main.py                          100%
app/api/api_router.py               100%
app/api/endpoints/auth.py           100%
app/api/endpoints/consultation.py    91%
app/api/endpoints/diagnosis.py      100%
app/api/endpoints/patient.py        100%
app/repositories/consultation.py    100%
app/repositories/diagnosis.py       100%
app/repositories/patient.py          80%
app/repositories/user.py            100%
app/api/dependencies.py              89%
app/core/exceptions.py               76%
app/core/security.py                100%
```
