#!/bin/bash

# Public deployment smoke test script

set -e

echo "🧪 Running public deployment smoke tests..."

# Load environment
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

API_BASE="${PUBLIC_BACKEND_URL:-http://localhost:8000}"

echo "Testing API base: $API_BASE"

# Test 1: Health endpoint
echo ""
echo "1. Testing system health endpoint..."
HEALTH_RESPONSE=$(curl -s "${API_BASE}/api/v1/system/health")
echo "Response: $HEALTH_RESPONSE"

if echo "$HEALTH_RESPONSE" | grep -q '"status":"healthy"'; then
    echo "✅ Health check passed"
else
    echo "❌ Health check failed"
    exit 1
fi

# Test 2: Database connection
if echo "$HEALTH_RESPONSE" | grep -q '"database":"connected"'; then
    echo "✅ Database connected"
else
    echo "❌ Database not connected"
    exit 1
fi

# Test 3: Qdrant connection
if echo "$HEALTH_RESPONSE" | grep -q '"qdrant":"connected"'; then
    echo "✅ Qdrant connected"
else
    echo "⚠️  Qdrant not connected (optional)"
fi

# Test 4: Inference service
if echo "$HEALTH_RESPONSE" | grep -q '"inference_service":"connected"'; then
    echo "✅ Inference service connected"
else
    echo "⚠️  Inference service not connected"
fi

# Test 5: WebSocket URL endpoint
echo ""
echo "2. Testing WebSocket URL endpoint..."
WS_RESPONSE=$(curl -s "${API_BASE}/api/v1/system/ws-url")
echo "Response: $WS_RESPONSE"

if echo "$WS_RESPONSE" | grep -q '"ws_url"'; then
    echo "✅ WebSocket URL endpoint working"
else
    echo "❌ WebSocket URL endpoint failed"
    exit 1
fi

# Test 6: CORS headers (if testing from browser)
echo ""
echo "3. Testing CORS configuration..."
CORS_HEADERS=$(curl -s -I -X OPTIONS "${API_BASE}/api/v1/system/health" -H "Origin: ${FRONTEND_PUBLIC_URL:-http://localhost:3000}")

if echo "$CORS_HEADERS" | grep -q "Access-Control-Allow-Origin"; then
    echo "✅ CORS headers present"
else
    echo "⚠️  CORS headers not found (may be normal for GET requests)"
fi

# Test 7: Root endpoint
echo ""
echo "4. Testing root endpoint..."
ROOT_RESPONSE=$(curl -s "${API_BASE}/")
if echo "$ROOT_RESPONSE" | grep -q '"status":"ok"'; then
    echo "✅ Root endpoint working"
else
    echo "❌ Root endpoint failed"
    exit 1
fi

echo ""
echo "✅ All smoke tests passed!"
echo ""
echo "Next steps:"
echo "1. Test frontend: https://your-app.vercel.app"
echo "2. Test share link in incognito"
echo "3. Test authentication flow"
echo "4. Test image upload and editing"
