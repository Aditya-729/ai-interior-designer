#!/bin/bash

# Development script to spin up full stack

set -e

echo "🚀 Starting AI Interior Designer development environment..."

# Check prerequisites
command -v docker >/dev/null 2>&1 || { echo "Docker is required"; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "Python 3 is required"; exit 1; }

# Start infrastructure
echo "Starting infrastructure services..."
docker-compose up -d postgres qdrant

# Wait for services
echo "Waiting for services..."
sleep 5

# Setup backend
echo "Setting up backend..."
cd backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
cd ..

# Setup inference
echo "Setting up inference service..."
cd inference_service
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt
cd ..

# Setup frontend
echo "Setting up frontend..."
cd frontend
npm install
cd ..

echo "✅ Development environment ready!"
echo ""
echo "To start services:"
echo "  Backend: cd backend && source venv/bin/activate && python run.py"
echo "  Inference: cd inference_service && source venv/bin/activate && python run.py"
echo "  Frontend: cd frontend && npm run dev"
