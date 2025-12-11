# Verification Script - Check Project Completeness
# Run this to verify everything is set up correctly

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Project Verification Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$allGood = $true

# Check directory structure
Write-Host "Checking directory structure..." -ForegroundColor Yellow
$requiredDirs = @("app", "app\routes", "tests", ".github", ".github\workflows")
foreach ($dir in $requiredDirs) {
    if (Test-Path $dir) {
        Write-Host "  ✓ $dir exists" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $dir missing" -ForegroundColor Red
        $allGood = $false
    }
}

# Check required files
Write-Host ""
Write-Host "Checking required files..." -ForegroundColor Yellow
$requiredFiles = @(
    "app\main.py",
    "app\models.py",
    "app\schemas.py",
    "app\database.py",
    "app\utils.py",
    "app\routes\users.py",
    "app\routes\calculations.py",
    "tests\conftest.py",
    "tests\test_users.py",
    "tests\test_calculations.py",
    ".github\workflows\ci-cd.yml",
    "Dockerfile",
    "docker-compose.yml",
    "requirements.txt",
    "README.md",
    "REFLECTION.md"
)

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "  ✓ $file exists" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $file missing" -ForegroundColor Red
        $allGood = $false
    }
}

# Check Python
Write-Host ""
Write-Host "Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "  ✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Python not found" -ForegroundColor Red
    $allGood = $false
}

# Check if venv exists
Write-Host ""
Write-Host "Checking virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "  ✓ Virtual environment exists" -ForegroundColor Green
} else {
    Write-Host "  ! Virtual environment not created yet" -ForegroundColor Yellow
    Write-Host "    Run: python -m venv venv" -ForegroundColor Cyan
}

# Check .env file
Write-Host ""
Write-Host "Checking environment configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "  ✓ .env file exists" -ForegroundColor Green
} else {
    Write-Host "  ! .env file not created yet" -ForegroundColor Yellow
    Write-Host "    Run: copy .env.example .env" -ForegroundColor Cyan
}

# Check Docker
Write-Host ""
Write-Host "Checking Docker..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version
    Write-Host "  ✓ Docker found: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "  ! Docker not found (optional)" -ForegroundColor Yellow
}

# Check PostgreSQL
Write-Host ""
Write-Host "Checking PostgreSQL..." -ForegroundColor Yellow
try {
    $pgVersion = psql --version
    Write-Host "  ✓ PostgreSQL found: $pgVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ PostgreSQL not found" -ForegroundColor Red
    $allGood = $false
}

# Count test files
Write-Host ""
Write-Host "Analyzing tests..." -ForegroundColor Yellow
if (Test-Path "tests\test_users.py") {
    $userTests = (Select-String -Path "tests\test_users.py" -Pattern "def test_").Count
    Write-Host "  ✓ User tests: $userTests test cases" -ForegroundColor Green
}
if (Test-Path "tests\test_calculations.py") {
    $calcTests = (Select-String -Path "tests\test_calculations.py" -Pattern "def test_").Count
    Write-Host "  ✓ Calculation tests: $calcTests test cases" -ForegroundColor Green
}

# Check API endpoints
Write-Host ""
Write-Host "Analyzing API endpoints..." -ForegroundColor Yellow
if (Test-Path "app\routes\users.py") {
    $userRoutes = (Select-String -Path "app\routes\users.py" -Pattern "@router\.(get|post|put|patch|delete)").Count
    Write-Host "  ✓ User endpoints: $userRoutes routes" -ForegroundColor Green
}
if (Test-Path "app\routes\calculations.py") {
    $calcRoutes = (Select-String -Path "app\routes\calculations.py" -Pattern "@router\.(get|post|put|patch|delete)").Count
    Write-Host "  ✓ Calculation endpoints: $calcRoutes routes" -ForegroundColor Green
}

# Summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
if ($allGood) {
    Write-Host "  ✓ All Critical Checks Passed!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Next Steps:" -ForegroundColor Yellow
    Write-Host "1. Set up virtual environment and install dependencies" -ForegroundColor White
    Write-Host "   python -m venv venv" -ForegroundColor Cyan
    Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor Cyan
    Write-Host "   pip install -r requirements.txt" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "2. Configure database" -ForegroundColor White
    Write-Host "   copy .env.example .env" -ForegroundColor Cyan
    Write-Host "   # Edit .env with your credentials" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "3. Create databases" -ForegroundColor White
    Write-Host "   createdb webapi_db" -ForegroundColor Cyan
    Write-Host "   createdb test_webapi_db" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "4. Run the application" -ForegroundColor White
    Write-Host "   uvicorn app.main:app --reload" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "5. Run tests" -ForegroundColor White
    Write-Host "   pytest tests/ -v" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "OR use Docker:" -ForegroundColor Yellow
    Write-Host "   docker-compose up --build" -ForegroundColor Cyan
} else {
    Write-Host "  ! Some Checks Failed" -ForegroundColor Yellow
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Please address the issues marked with ✗ above" -ForegroundColor Yellow
}
Write-Host ""
Write-Host "For detailed instructions, see:" -ForegroundColor Yellow
Write-Host "  - QUICKSTART.md" -ForegroundColor Cyan
Write-Host "  - README.md" -ForegroundColor Cyan
Write-Host ""
