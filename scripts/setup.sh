#!/bin/bash

# Setup script for the entire project

set -e

echo "🚀 Setting up AI Interior Designer..."

# Check prerequisites
echo "Checking prerequisites..."
command -v python3 >/dev/null 2>&1 || { echo "Python 3 is required but not installed. Aborting." >&2; exit 1; }
command -v node >/dev/null 2>&1 || { echo "Node.js is required but not installed. Aborting." >&2; exit 1; }
command -v docker >/dev/null 2>&1 || { echo "Docker is required but not installed. Aborting." >&2; exit 1; }

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your API keys and configuration"
fi

# Start infrastructure
echo "Starting infrastructure services..."
docker-compose up -d postgres qdrant

# Wait for services to be ready
echo "Waiting for services to be ready..."
sleep 5

# Setup backend
echo "Setting up backend..."
cd backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cd ..

# Setup inference service
echo "Setting up inference service..."
cd inference_service
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cd ..

# Setup frontend
echo "Setting up frontend..."
cd frontend
npm install
cd ..

# Run database migrations
echo "Running database migrations..."
cd backend
source venv/bin/activate
python -m alembic upgrade head
cd ..

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env with your API keys"
echo "2. Run ./scripts/download_models.sh to download AI models"
echo "3. Start backend: cd backend && source venv/bin/activate && uvicorn main:app --reload"
echo "4. Start inference: cd inference_service && source venv/bin/activate && python server.py"
echo "5. Start frontend: cd frontend && npm run dev"
