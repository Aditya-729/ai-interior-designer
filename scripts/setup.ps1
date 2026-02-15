# PowerShell setup script for Windows

Write-Host "🚀 Setting up AI Interior Designer..." -ForegroundColor Green

# Check prerequisites
Write-Host "Checking prerequisites..."
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python is required but not installed. Aborting." -ForegroundColor Red
    exit 1
}
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "Node.js is required but not installed. Aborting." -ForegroundColor Red
    exit 1
}
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "Docker is required but not installed. Aborting." -ForegroundColor Red
    exit 1
}

# Create .env if it doesn't exist
if (-not (Test-Path .env)) {
    Write-Host "Creating .env from .env.example..."
    Copy-Item .env.example .env
    Write-Host "⚠️  Please edit .env with your API keys and configuration" -ForegroundColor Yellow
}

# Start infrastructure
Write-Host "Starting infrastructure services..."
docker-compose up -d postgres qdrant

# Wait for services
Write-Host "Waiting for services to be ready..."
Start-Sleep -Seconds 5

# Setup backend
Write-Host "Setting up backend..."
Set-Location backend
if (-not (Test-Path venv)) {
    python -m venv venv
}
& .\venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
Set-Location ..

# Setup inference service
Write-Host "Setting up inference service..."
Set-Location inference_service
if (-not (Test-Path venv)) {
    python -m venv venv
}
& .\venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
Set-Location ..

# Setup frontend
Write-Host "Setting up frontend..."
Set-Location frontend
npm install
Set-Location ..

# Run database migrations
Write-Host "Running database migrations..."
Set-Location backend
& .\venv\Scripts\Activate.ps1
python -m alembic upgrade head
Set-Location ..

Write-Host "✅ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:"
Write-Host "1. Edit .env with your API keys"
Write-Host "2. Run ./scripts/download_models.sh to download AI models"
Write-Host "3. Start backend: cd backend && venv\Scripts\activate && uvicorn main:app --reload"
Write-Host "4. Start inference: cd inference_service && venv\Scripts\activate && python server.py"
Write-Host "5. Start frontend: cd frontend && npm run dev"
