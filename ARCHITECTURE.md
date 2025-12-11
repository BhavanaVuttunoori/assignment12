# Project Architecture

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client / Browser                         │
│                    http://localhost:8000/docs                    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTP Requests
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                        FastAPI Application                       │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                         main.py                            │  │
│  │              (Application Entry Point)                     │  │
│  └──────────────────────┬────────────────────────────────────┘  │
│                         │                                        │
│         ┌───────────────┴───────────────┐                       │
│         ▼                               ▼                       │
│  ┌──────────────┐               ┌──────────────┐               │
│  │   User       │               │ Calculation  │               │
│  │   Routes     │               │   Routes     │               │
│  │ /users/*     │               │/calculations/*               │
│  └──────┬───────┘               └──────┬───────┘               │
│         │                               │                       │
│         └───────────────┬───────────────┘                       │
│                         ▼                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   Pydantic Schemas                       │   │
│  │          (Validation & Serialization)                    │   │
│  │  - UserCreate, UserLogin, UserRead                      │   │
│  │  - CalculationCreate, CalculationUpdate, CalculationRead│   │
│  └──────────────────────┬──────────────────────────────────┘   │
│                         ▼                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  Business Logic                          │   │
│  │                    (utils.py)                            │   │
│  │  - Password Hashing (bcrypt)                            │   │
│  │  - Calculations (add, subtract, multiply, divide)       │   │
│  └──────────────────────┬──────────────────────────────────┘   │
│                         ▼                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │               SQLAlchemy ORM Layer                       │   │
│  │                   (models.py)                            │   │
│  │  - User Model                                           │   │
│  │  - Calculation Model                                    │   │
│  └──────────────────────┬──────────────────────────────────┘   │
└────────────────────────┼────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                     PostgreSQL Database                          │
│  ┌────────────────┐                 ┌────────────────┐          │
│  │  users table   │                 │calculations tbl│          │
│  ├────────────────┤                 ├────────────────┤          │
│  │ id             │                 │ id             │          │
│  │ username       │◄────────────────┤ user_id (FK)   │          │
│  │ email          │  1:many         │ operation      │          │
│  │ hashed_password│                 │ operand1       │          │
│  │ created_at     │                 │ operand2       │          │
│  └────────────────┘                 │ result         │          │
│                                     │ created_at     │          │
│                                     │ updated_at     │          │
│                                     └────────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

## Request Flow

### User Registration Flow

```
1. Client (Browser)
   POST /users/register
   {username, email, password}
        │
        ▼
2. FastAPI Router (users.py)
   @router.post("/register")
        │
        ▼
3. Pydantic Validation (schemas.py)
   UserCreate schema validates:
   - Username length (3-50)
   - Email format
   - Password length (6+)
        │
        ▼
4. Business Logic (utils.py)
   hash_password(password)
   → bcrypt hashing
        │
        ▼
5. Database Check (users.py)
   Check if username/email exists
        │
        ▼
6. SQLAlchemy ORM (models.py)
   User(username, email, hashed_password)
        │
        ▼
7. PostgreSQL
   INSERT INTO users...
        │
        ▼
8. Response
   201 Created
   {id, username, email, created_at}
```

### Calculation Creation Flow

```
1. Client
   POST /calculations?user_id=1
   {operation, operand1, operand2}
        │
        ▼
2. FastAPI Router (calculations.py)
   @router.post("")
        │
        ▼
3. Pydantic Validation
   CalculationCreate schema validates:
   - Operation type (add|subtract|multiply|divide)
   - Operands are numbers
   - Division by zero check
        │
        ▼
4. User Verification
   Query User table
   Verify user_id exists
        │
        ▼
5. Business Logic
   calculate(operation, operand1, operand2)
   → Compute result
        │
        ▼
6. SQLAlchemy ORM
   Calculation(operation, operand1, operand2, result, user_id)
        │
        ▼
7. PostgreSQL
   INSERT INTO calculations...
        │
        ▼
8. Response
   201 Created
   {id, operation, operand1, operand2, result, user_id, timestamps}
```

## Testing Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         pytest Framework                         │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                      conftest.py                          │  │
│  │  - Test database setup                                    │  │
│  │  - Fixtures (sample_user)                                 │  │
│  │  - Dependency overrides                                   │  │
│  └──────────────────────┬────────────────────────────────────┘  │
│                         │                                        │
│         ┌───────────────┴───────────────┐                       │
│         ▼                               ▼                       │
│  ┌──────────────┐               ┌──────────────┐               │
│  │test_users.py │               │test_calcs.py │               │
│  │  10+ tests   │               │  20+ tests   │               │
│  └──────┬───────┘               └──────┬───────┘               │
│         │                               │                       │
│         └───────────────┬───────────────┘                       │
│                         ▼                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              TestClient (httpx)                          │   │
│  │         Simulates HTTP requests to API                   │   │
│  └──────────────────────┬──────────────────────────────────┘   │
│                         ▼                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                 FastAPI Application                      │   │
│  │            (with test database)                          │   │
│  └──────────────────────┬──────────────────────────────────┘   │
└────────────────────────┼────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                  Test PostgreSQL Database                        │
│           (Created/Dropped for each test)                        │
└─────────────────────────────────────────────────────────────────┘
```

## CI/CD Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                          GitHub                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Git Push to main                        │  │
│  └──────────────────────┬────────────────────────────────────┘  │
│                         │ Triggers                               │
│                         ▼                                        │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                   GitHub Actions                           │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │               Test Job                              │  │  │
│  │  │  1. Checkout code                                   │  │  │
│  │  │  2. Setup Python 3.11                               │  │  │
│  │  │  3. Start PostgreSQL service                        │  │  │
│  │  │  4. Install dependencies                            │  │  │
│  │  │  5. Run pytest                                      │  │  │
│  │  │  6. Upload test results                             │  │  │
│  │  └─────────────────────┬───────────────────────────────┘  │  │
│  │                        │ On Success                        │  │
│  │                        ▼                                   │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │            Build & Push Job                         │  │  │
│  │  │  1. Checkout code                                   │  │  │
│  │  │  2. Setup Docker Buildx                             │  │  │
│  │  │  3. Login to Docker Hub                             │  │  │
│  │  │  4. Build Docker image                              │  │  │
│  │  │  5. Push to Docker Hub                              │  │  │
│  │  │     - Tag: latest                                   │  │  │
│  │  │     - Tag: {commit-sha}                             │  │  │
│  │  └─────────────────────┬───────────────────────────────┘  │  │
│  └────────────────────────┼────────────────────────────────────┘  │
└───────────────────────────┼───────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Docker Hub                                │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │           YOUR_USERNAME/webapi-assignment                 │  │
│  │  - latest (always most recent)                            │  │
│  │  - {commit-sha} (specific version)                        │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Docker Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      Docker Compose                              │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                  docker-compose.yml                        │  │
│  └──────────────┬─────────────────────┬──────────────────────┘  │
│                 │                     │                          │
│                 ▼                     ▼                          │
│  ┌──────────────────────┐ ┌──────────────────────┐             │
│  │   Database Service   │ │    Web Service       │             │
│  │  ┌────────────────┐  │ │  ┌────────────────┐  │             │
│  │  │  postgres:15   │  │ │  │  Dockerfile    │  │             │
│  │  │                │  │ │  │                │  │             │
│  │  │  Port: 5432    │◄─┼─┼──│  Port: 8000    │  │             │
│  │  │                │  │ │  │                │  │             │
│  │  │  Volume:       │  │ │  │  Depends on db │  │             │
│  │  │  postgres_data │  │ │  └────────────────┘  │             │
│  │  └────────────────┘  │ └──────────────────────┘             │
│  └──────────────────────┘                                       │
└─────────────────────────────────────────────────────────────────┘
```

## Security Layers

```
┌─────────────────────────────────────────────────────────────────┐
│                      Security Layers                             │
│                                                                  │
│  Layer 1: Input Validation                                      │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Pydantic Schemas                                         │  │
│  │  - Type checking                                          │  │
│  │  - Field constraints (length, format, patterns)           │  │
│  │  - Custom validators (division by zero)                   │  │
│  └───────────────────────────────────────────────────────────┘  │
│                            │                                     │
│  Layer 2: Authentication                                        │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Password Security                                        │  │
│  │  - Bcrypt hashing (cost factor: 12)                      │  │
│  │  - Salt generation                                        │  │
│  │  - Secure verification                                    │  │
│  └───────────────────────────────────────────────────────────┘  │
│                            │                                     │
│  Layer 3: Database Protection                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  SQLAlchemy ORM                                           │  │
│  │  - SQL injection prevention                               │  │
│  │  - Parameterized queries                                  │  │
│  │  - Type safety                                            │  │
│  └───────────────────────────────────────────────────────────┘  │
│                            │                                     │
│  Layer 4: Environment Security                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Configuration                                            │  │
│  │  - .env files (not in git)                                │  │
│  │  - GitHub Secrets                                         │  │
│  │  - No hardcoded credentials                               │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow Summary

```
User Action → API Endpoint → Validation → Business Logic → ORM → Database
                                                                     │
Response ← Serialization ← Model Instance ← Query Result ←──────────┘
```

## Technology Stack

```
┌────────────────────────────────────────────────────────┐
│                    Frontend Layer                      │
│  - OpenAPI/Swagger UI (Interactive Documentation)     │
│  - ReDoc (Alternative Documentation)                   │
└──────────────────┬─────────────────────────────────────┘
                   │
┌──────────────────▼─────────────────────────────────────┐
│                   API Layer                            │
│  - FastAPI 0.104.1 (Web Framework)                    │
│  - Uvicorn (ASGI Server)                              │
│  - Pydantic 2.5.0 (Validation)                        │
└──────────────────┬─────────────────────────────────────┘
                   │
┌──────────────────▼─────────────────────────────────────┐
│                 Business Layer                         │
│  - Python 3.11                                        │
│  - Passlib (Password Hashing)                         │
│  - Bcrypt (Cryptography)                              │
└──────────────────┬─────────────────────────────────────┘
                   │
┌──────────────────▼─────────────────────────────────────┐
│                  Data Layer                            │
│  - SQLAlchemy 2.0.23 (ORM)                            │
│  - PostgreSQL 15 (Database)                           │
│  - psycopg2-binary (DB Driver)                        │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│                   Testing Layer                        │
│  - pytest 7.4.3 (Testing Framework)                   │
│  - httpx 0.25.2 (HTTP Client)                         │
│  - pytest-asyncio (Async Testing)                     │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│                   DevOps Layer                         │
│  - Docker (Containerization)                          │
│  - Docker Compose (Multi-container)                   │
│  - GitHub Actions (CI/CD)                             │
│  - Docker Hub (Registry)                              │
└────────────────────────────────────────────────────────┘
```

This architecture ensures:
- ✅ Separation of concerns
- ✅ Maintainability
- ✅ Testability
- ✅ Security
- ✅ Scalability
