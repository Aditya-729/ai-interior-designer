#!/bin/bash

# Environment checker script

echo "🔍 Checking environment setup..."

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ Python: $PYTHON_VERSION"
else
    echo "❌ Python 3 not found"
    exit 1
fi

# Check Node.js
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo "✅ Node.js: $NODE_VERSION"
else
    echo "❌ Node.js not found"
    exit 1
fi

# Check Docker
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version)
    echo "✅ Docker: $DOCKER_VERSION"
else
    echo "❌ Docker not found"
    exit 1
fi

# Check .env file
if [ -f .env ]; then
    echo "✅ .env file exists"
    
    # Check required variables
    source .env
    
    REQUIRED_VARS=(
        "MINO_AI_API_KEY"
        "PERPLEXITY_API_KEY"
        "R2_ACCOUNT_ID"
        "R2_ACCESS_KEY_ID"
        "R2_SECRET_ACCESS_KEY"
        "R2_ENDPOINT"
    )
    
    MISSING_VARS=()
    for var in "${REQUIRED_VARS[@]}"; do
        if [ -z "${!var}" ]; then
            MISSING_VARS+=("$var")
        fi
    done
    
    if [ ${#MISSING_VARS[@]} -eq 0 ]; then
        echo "✅ All required environment variables set"
    else
        echo "❌ Missing environment variables:"
        for var in "${MISSING_VARS[@]}"; do
            echo "   - $var"
        done
    fi
else
    echo "❌ .env file not found"
    exit 1
fi

# Check PostgreSQL connection
if docker ps | grep -q postgres; then
    echo "✅ PostgreSQL container running"
else
    echo "⚠️  PostgreSQL container not running"
fi

# Check Qdrant connection
if docker ps | grep -q qdrant; then
    echo "✅ Qdrant container running"
else
    echo "⚠️  Qdrant container not running"
fi

echo ""
echo "✅ Environment check complete!"
