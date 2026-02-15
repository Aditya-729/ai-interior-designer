#!/bin/bash

# Reset script to clean database and start fresh

set -e

echo "⚠️  Resetting database and cleaning up..."

# Stop services
docker-compose down

# Remove volumes
docker volume rm interior_designer_postgres_data interior_designer_qdrant_data 2>/dev/null || true

# Start fresh
docker-compose up -d postgres qdrant

# Wait for services
sleep 5

# Run migrations
cd backend
source venv/bin/activate
alembic upgrade head
cd ..

echo "✅ Database reset complete!"
