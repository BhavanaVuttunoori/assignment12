# Web API - Module 12 Assignment
The Assignment 12 deliverable is a fully tested FastAPI user authentication and calculation service with BREAD operations, packaged for local development, Docker usage, and CI/CD. This README documents how the project is structured, what was implemented, and how to reproduce the results.

## Project Highlights
Built with FastAPI and SQLAlchemy to expose user registration/login and calculation operations through REST endpoints with database persistence. Secure user authentication with bcrypt password hashing and comprehensive validation. BREAD pattern implementation (Browse, Read, Edit, Add, Delete) for calculation management. Robust Pydantic validation in app/schemas.py with explicit error handling (division by zero, email format, password strength). Comprehensive automated test suite covering user and calculation scenarios (30+ tests with pytest). SQLAlchemy ORM models with proper relationships between Users and Calculations tables. Continuous Integration via GitHub Actions to test with PostgreSQL, build Docker images, and deploy to Docker Hub. Containerized delivery: public Docker image available at bhavanavuttunoori/webapi-assignment.

## Getting Started
### 1. Setup Environment
```bash
cd "webapi 12 ass"
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. Run the Application Locally
```bash
uvicorn app.main:app --reload
```
Navigate to http://localhost:8000/docs for the Swagger UI or hit REST endpoints directly (e.g. POST http://localhost:8000/users/register).

## Docker Usage
### Build Locally (optional)
```bash
docker build -t webapi-assignment .
docker run -p 8000:8000 -e DATABASE_URL=postgresql://user:password@localhost:5432/webapi_db webapi-assignment
```

### Pull Prebuilt Image
```bash
docker pull bhavanavuttunoori/webapi-assignment:latest
docker run -p 8000:8000 -e DATABASE_URL=postgresql://user:password@localhost:5432/webapi_db bhavanavuttunoori/webapi-assignment:latest
```

### Using Docker Compose
```bash
docker-compose up -d
```
The application will be available at http://localhost:8000 with PostgreSQL database.

## Testing Strategy
**Unit Tests (tests/test_users.py)**: verify user registration, login, validation rules and error handling. **Unit Tests (tests/test_calculations.py)**: verify calculation CRUD operations, pagination, filtering, and business logic. **Integration Tests**: exercise each API route through FastAPI's test client with database operations.

Run the full suite:
```bash
pytest tests/ -v
```

Run with coverage:
```bash
pytest tests/ --cov=app --cov-report=term-missing --cov-report=html
```

View coverage report:
```bash
start htmlcov/index.html  # Windows
open htmlcov/index.html   # Mac/Linux
```

## Project Structure
```
webapi 12 ass/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application with all endpoints
│   ├── database.py          # Database configuration and session management
│   ├── models.py            # SQLAlchemy ORM models (User, Calculation)
│   ├── schemas.py           # Pydantic validation schemas
│   ├── utils.py             # Helper functions (password hashing, calculations)
│   └── routes/
│       ├── __init__.py
│       ├── users.py         # User registration and login endpoints
│       └── calculations.py  # Calculation BREAD endpoints
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures and test database setup
│   ├── test_users.py        # User endpoint tests
│   └── test_calculations.py # Calculation endpoint tests
├── .github/
│   └── workflows/
│       └── ci-cd.yml        # GitHub Actions CI/CD pipeline
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pyproject.toml
├── .env.example
├── README.md
└── REFLECTION.md
```

## API Endpoints
### User Operations
**Create User (Register):**
```http
POST /users/register
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Login:**
```http
POST /users/login
Content-Type: application/json

{
  "username": "johndoe",
  "password": "securepassword123"
}
```

**Get User:**
```http
GET /users/{user_id}
```

### Calculation Operations (BREAD)
**Browse Calculations:**
```http
GET /calculations?skip=0&limit=100&user_id=1
```

**Read Calculation:**
```http
GET /calculations/{calculation_id}
```

**Edit Calculation:**
```http
PATCH /calculations/{calculation_id}
Content-Type: application/json

{
  "operation": "multiply",
  "operand1": 20
}
```

**Add Calculation:**
```http
POST /calculations?user_id=1
Content-Type: application/json

{
  "operation": "add",
  "operand1": 10.5,
  "operand2": 5.2
}
```

**Delete Calculation:**
```http
DELETE /calculations/{calculation_id}
```

## BREAD Pattern Implementation
The BREAD pattern in app/routes/calculations.py provides comprehensive calculation management:

**Browse**: List all calculations with pagination (skip, limit) and filtering by user_id. **Read**: Retrieve specific calculation by ID with full details. **Edit**: Update calculation operation or operands with automatic result recalculation. **Add**: Create new calculation with validation and automatic result computation. **Delete**: Remove calculation from database.

Supported operations: Add, Subtract, Multiply, Divide with division by zero protection.

Example usage:
```python
# Browse calculations
GET /calculations?skip=0&limit=10&user_id=1

# Add new calculation
POST /calculations?user_id=1
{"operation": "add", "operand1": 10, "operand2": 5}  # Returns 15

# Edit calculation
PATCH /calculations/1
{"operation": "multiply"}  # Recalculates with new operation

# Delete calculation
DELETE /calculations/1
```

## Database Schema
**Users Table:**
- id (Integer, Primary Key)
- username (String, Unique, Indexed)
- email (String, Unique, Indexed)
- hashed_password (String)
- created_at (DateTime)

**Calculations Table:**
- id (Integer, Primary Key)
- operation (String: add, subtract, multiply, divide)
- operand1 (Float)
- operand2 (Float)
- result (Float)
- created_at (DateTime)
- updated_at (DateTime)
- user_id (Integer, Foreign Key to users.id)

**Relationship**: One User can have many Calculations (one-to-many with cascade delete).

## Continuous Integration
The repository includes a GitHub Actions workflow (.github/workflows/ci-cd.yml) that runs on every push:

**Test Job:**
- Set up Python 3.11
- Start PostgreSQL 15 service container
- Install dependencies with caching
- Run user tests (test_users.py)
- Run calculation tests (test_calculations.py)
- Generate and upload test results

**Build and Push Job (main branch only):**
- Build Docker image
- Tag with latest and commit SHA
- Push to Docker Hub (bhavanavuttunoori/webapi-assignment)

**Required GitHub Secrets:**
- DOCKER_USERNAME: Your Docker Hub username
- DOCKER_PASSWORD: Your Docker Hub access token

## Assignment Instructions & Deliverables
**Objective**: Implement and test user registration/login endpoints and calculation CRUD operations with comprehensive integration testing and CI/CD pipeline.

### Implementation Checklist
✅ SQLAlchemy models for User and Calculation with proper relationships. ✅ Pydantic schemas with validation (division by zero, email format, password strength). ✅ User registration endpoint with duplicate detection and password hashing. ✅ User login endpoint with password verification. ✅ Calculation BREAD endpoints (Browse, Read, Edit, Add, Delete). ✅ 30+ comprehensive tests covering user and calculation scenarios. ✅ FastAPI application with full CRUD operations. ✅ GitHub Actions workflow with PostgreSQL integration. ✅ Docker containerization with docker-compose support. ✅ Comprehensive documentation.

### Submission Package
- GitHub repository: https://github.com/BhavanaVuttunoori/assignment12
- Docker Hub image: https://hub.docker.com/r/bhavanavuttunoori/webapi-assignment
- Screenshots demonstrating:
  - Successful GitHub Actions workflow
  - Docker Hub deployment
  - Test coverage report
  - API documentation (Swagger UI)
  - User registration working
  - User login working
  - Calculation operations working

### Grading Guidelines
**Criterion: User Routes (25 Points)**
- Registration endpoint with validation and password hashing
- Login endpoint with password verification
- User retrieval endpoint
- Proper error handling (duplicate users, invalid credentials)

**Criterion: Calculation Routes (25 Points)**
- Browse endpoint with pagination and filtering
- Read endpoint for specific calculation
- Edit endpoint with automatic recalculation
- Add endpoint with validation
- Delete endpoint
- Proper error handling (division by zero, not found)

**Criterion: Testing (25 Points)**
- 30+ unit and integration tests
- User registration and login tests
- Calculation CRUD tests
- Error scenario tests
- Test database isolation

**Criterion: CI/CD Pipeline (15 Points)**
- GitHub Actions workflow configuration
- PostgreSQL service container integration
- Docker build and push automation
- Automated test execution

**Criterion: Documentation (10 Points)**
- Comprehensive README with setup instructions
- API documentation via Swagger
- Reflection document
- Code comments and docstrings

## Helpful Commands
| Task | Command |
|------|---------|
| Install dependencies | `pip install -r requirements.txt` |
| Run application | `uvicorn app.main:app --reload` |
| Run all tests | `pytest tests/ -v` |
| Run tests with coverage | `pytest tests/ --cov=app --cov-report=html` |
| Run user tests only | `pytest tests/test_users.py -v` |
| Run calculation tests only | `pytest tests/test_calculations.py -v` |
| Build Docker image | `docker build -t webapi-assignment .` |
| Run with Docker Compose | `docker-compose up -d` |
| Stop Docker Compose | `docker-compose down` |
| View container logs | `docker logs -f webapi_app` |
| Setup script | `.\setup.ps1` |
| Verify project | `.\verify.ps1` |

## Submission Tips
✅ Commit frequently with meaningful messages describing each feature. ✅ Keep .env or secrets out of version control (use .gitignore). ✅ Verify all tests pass locally before pushing. ✅ Ensure GitHub Actions workflow completes successfully. ✅ Capture required screenshots showing green checkmarks in Actions tab. ✅ Verify Docker image is publicly accessible on Docker Hub. ✅ Update README with your actual GitHub and Docker Hub usernames. ✅ Include reflection document discussing implementation challenges and solutions.

## Learning Outcomes
**CLO3: Create Python applications with automated testing**
- Comprehensive unit tests for user and calculation endpoints
- Integration tests with database operations
- Test fixtures and database isolation
- 30+ tests with comprehensive coverage

**CLO4: Set up GitHub Actions for CI**
- Automated testing on push and pull requests
- PostgreSQL service containers
- Automated Docker builds and deployment
- Test result uploads

**CLO9: Apply containerization techniques**
- Optimized Dockerfile for production
- Docker Compose for local development
- Environment variable management
- Service orchestration with health checks

**CLO10: Create, consume, and test REST APIs**
- RESTful endpoint design (BREAD pattern)
- Proper HTTP methods and status codes
- API documentation with OpenAPI/Swagger
- Request/response validation

**CLO11: Integrate with SQL databases**
- SQLAlchemy ORM models with relationships
- Foreign key constraints and cascade operations
- Database session management
- PostgreSQL in production

**CLO12: Serialize/deserialize JSON with Pydantic**
- Input validation schemas with custom validators
- Output serialization with from_attributes
- Type safety with Python type hints
- Email validation and password strength checks

**CLO13: Implement secure authentication**
- Password hashing with bcrypt
- Secure password storage
- Email validation with regex patterns
- User authentication and authorization foundation

## Author
**Bhavana Vuttunoori**
- GitHub: https://github.com/BhavanaVuttunoori
- Repository: https://github.com/BhavanaVuttunoori/assignment12

## Acknowledgments
FastAPI documentation and community examples. SQLAlchemy ORM patterns and best practices. Pydantic validation framework. GitHub Actions workflow templates. Course instructors for project guidance.

## Support
For questions or issues:
- Check the GitHub Issues: https://github.com/BhavanaVuttunoori/assignment12/issues
- Review the API documentation at http://localhost:8000/docs
- Check QUICKSTART.md for setup instructions
- Review REFLECTION.md for implementation insights
- Contact the repository maintainer

## License
This project is licensed under the MIT License - see the LICENSE file for details.

**Note**: This project was created as part of Module 12 assignment for demonstrating user authentication, calculation CRUD operations with BREAD pattern, comprehensive integration testing, and CI/CD pipelines.
