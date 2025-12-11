# Setup Script for Module 12 Assignment
# Run this script to set up the project quickly

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Module 12 Assignment Setup Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "✓ $pythonVersion found" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.11+" -ForegroundColor Red
    exit 1
}

# Check PostgreSQL installation
Write-Host "Checking PostgreSQL installation..." -ForegroundColor Yellow
try {
    $pgVersion = psql --version
    Write-Host "✓ $pgVersion found" -ForegroundColor Green
} catch {
    Write-Host "✗ PostgreSQL not found. Please install PostgreSQL 15+" -ForegroundColor Red
    Write-Host "  Download from: https://www.postgresql.org/download/" -ForegroundColor Yellow
    exit 1
}

# Create virtual environment
Write-Host ""
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "✓ Virtual environment already exists" -ForegroundColor Green
} else {
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
Write-Host "✓ Virtual environment activated" -ForegroundColor Green

# Install dependencies
Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install --upgrade pip | Out-Null
pip install -r requirements.txt
Write-Host "✓ Dependencies installed" -ForegroundColor Green

# Create .env file if it doesn't exist
Write-Host ""
Write-Host "Setting up environment variables..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "✓ .env file already exists" -ForegroundColor Green
} else {
    Copy-Item ".env.example" ".env"
    Write-Host "✓ .env file created from .env.example" -ForegroundColor Green
    Write-Host "  Please edit .env with your database credentials" -ForegroundColor Yellow
}

# Create databases
Write-Host ""
Write-Host "Setting up databases..." -ForegroundColor Yellow
$dbUser = Read-Host "Enter PostgreSQL username (default: postgres)"
if ([string]::IsNullOrWhiteSpace($dbUser)) { $dbUser = "postgres" }

Write-Host "Creating development database..." -ForegroundColor Yellow
psql -U $dbUser -c "CREATE DATABASE webapi_db;" 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Development database created" -ForegroundColor Green
} else {
    Write-Host "! Database might already exist or credentials incorrect" -ForegroundColor Yellow
}

Write-Host "Creating test database..." -ForegroundColor Yellow
psql -U $dbUser -c "CREATE DATABASE test_webapi_db;" 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Test database created" -ForegroundColor Green
} else {
    Write-Host "! Test database might already exist or credentials incorrect" -ForegroundColor Yellow
}

# Summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Edit .env file with your database credentials" -ForegroundColor White
Write-Host "2. Run the application:" -ForegroundColor White
Write-Host "   uvicorn app.main:app --reload" -ForegroundColor Cyan
Write-Host "3. Access API documentation:" -ForegroundColor White
Write-Host "   http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "4. Run tests:" -ForegroundColor White
Write-Host "   pytest tests/ -v" -ForegroundColor Cyan
Write-Host ""
Write-Host "For Docker setup:" -ForegroundColor Yellow
Write-Host "   docker-compose up --build" -ForegroundColor Cyan
Write-Host ""
Write-Host "For detailed instructions, see QUICKSTART.md" -ForegroundColor Yellow
Write-Host ""
