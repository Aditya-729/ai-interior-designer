#!/bin/bash

# Verify Supabase and Vercel setup

set -e

echo "🔍 Verifying setup..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found"
    echo "   Create .env file with your credentials"
    exit 1
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

echo ""
echo "📊 Supabase Configuration:"
if [ -z "$SUPABASE_DB_HOST" ]; then
    echo "   ❌ SUPABASE_DB_HOST not set"
else
    echo "   ✅ SUPABASE_DB_HOST: $SUPABASE_DB_HOST"
fi

if [ -z "$SUPABASE_DB_USER" ]; then
    echo "   ❌ SUPABASE_DB_USER not set"
else
    echo "   ✅ SUPABASE_DB_USER: $SUPABASE_DB_USER"
fi

if [ -z "$SUPABASE_DB_PASSWORD" ]; then
    echo "   ❌ SUPABASE_DB_PASSWORD not set"
else
    echo "   ✅ SUPABASE_DB_PASSWORD: [hidden]"
fi

echo ""
echo "🌐 Vercel Configuration:"
if [ -z "$FRONTEND_PUBLIC_URL" ]; then
    echo "   ⚠️  FRONTEND_PUBLIC_URL not set (will use Vercel default)"
else
    echo "   ✅ FRONTEND_PUBLIC_URL: $FRONTEND_PUBLIC_URL"
fi

echo ""
echo "🔧 Backend Configuration:"
if [ -z "$PUBLIC_BACKEND_URL" ]; then
    echo "   ⚠️  PUBLIC_BACKEND_URL not set (will use localhost)"
else
    echo "   ✅ PUBLIC_BACKEND_URL: $PUBLIC_BACKEND_URL"
fi

echo ""
echo "🧪 Testing Supabase Connection..."
if [ -n "$SUPABASE_DB_HOST" ] && [ -n "$SUPABASE_DB_USER" ] && [ -n "$SUPABASE_DB_PASSWORD" ]; then
    PGPASSWORD=$SUPABASE_DB_PASSWORD psql -h $SUPABASE_DB_HOST -p ${SUPABASE_DB_PORT:-5432} -U $SUPABASE_DB_USER -d $SUPABASE_DB_NAME -c "SELECT 1" > /dev/null 2>&1
    
    if [ $? -eq 0 ]; then
        echo "   ✅ Supabase connection successful!"
    else
        echo "   ❌ Supabase connection failed"
        echo "   Check your credentials and network connection"
    fi
else
    echo "   ⚠️  Cannot test - missing credentials"
fi

echo ""
echo "✅ Setup verification complete!"
echo ""
echo "Next steps:"
echo "1. If Supabase test failed, check credentials"
echo "2. Run: ./scripts/supabase-init.sh"
echo "3. Deploy to Vercel with environment variables"
echo "4. Test: ./scripts/public-smoke-test.sh"
