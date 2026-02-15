#!/bin/bash

# Supabase database backup script
# Runs daily to export database to local file

set -e

echo "📦 Creating Supabase database backup..."

# Load environment
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Check required variables
if [ -z "$SUPABASE_DB_HOST" ] || [ -z "$SUPABASE_DB_USER" ] || [ -z "$SUPABASE_DB_PASSWORD" ]; then
    echo "❌ Missing Supabase credentials"
    exit 1
fi

# Create backup directory
BACKUP_DIR="./backups"
mkdir -p "$BACKUP_DIR"

# Generate backup filename
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/supabase_backup_$TIMESTAMP.sql"

# Export database
echo "Exporting database..."
PGPASSWORD=$SUPABASE_DB_PASSWORD pg_dump \
    -h $SUPABASE_DB_HOST \
    -p ${SUPABASE_DB_PORT:-5432} \
    -U $SUPABASE_DB_USER \
    -d $SUPABASE_DB_NAME \
    --no-owner \
    --no-privileges \
    > "$BACKUP_FILE"

# Compress backup
gzip "$BACKUP_FILE"
echo "✅ Backup created: ${BACKUP_FILE}.gz"

# Keep only last 7 days of backups
find "$BACKUP_DIR" -name "supabase_backup_*.sql.gz" -mtime +7 -delete

echo "✅ Backup complete!"
