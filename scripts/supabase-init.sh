#!/bin/bash

# Supabase database initialization script

set -e

echo "🔍 Checking Supabase connection..."

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Check required variables
if [ -z "$SUPABASE_DB_HOST" ] || [ -z "$SUPABASE_DB_USER" ] || [ -z "$SUPABASE_DB_PASSWORD" ]; then
    echo "❌ Missing Supabase database credentials in .env"
    echo "Required: SUPABASE_DB_HOST, SUPABASE_DB_USER, SUPABASE_DB_PASSWORD, SUPABASE_DB_NAME"
    exit 1
fi

# Test connection
echo "Testing database connection..."
PGPASSWORD=$SUPABASE_DB_PASSWORD psql -h $SUPABASE_DB_HOST -p ${SUPABASE_DB_PORT:-5432} -U $SUPABASE_DB_USER -d $SUPABASE_DB_NAME -c "SELECT 1" > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✅ Database connection successful"
else
    echo "❌ Database connection failed"
    exit 1
fi

# Run migrations
echo "Running database migrations..."
cd backend
source venv/bin/activate 2>/dev/null || python -m venv venv && source venv/bin/activate
pip install -q -r requirements.txt

# Set database URL for Alembic
export DATABASE_URL="postgresql://${SUPABASE_DB_USER}:${SUPABASE_DB_PASSWORD}@${SUPABASE_DB_HOST}:${SUPABASE_DB_PORT:-5432}/${SUPABASE_DB_NAME}"

alembic upgrade head

echo "✅ Supabase initialization complete!"
