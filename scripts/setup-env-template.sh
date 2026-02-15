#!/bin/bash

# Create .env file template with placeholders

echo "📝 Creating .env template..."

cat > .env << 'EOF'
# ============================================
# AI Interior Designer - Environment Variables
# ============================================

# Supabase Database (from supabase.com dashboard)
SUPABASE_DB_HOST=db.xxxxx.supabase.co
SUPABASE_DB_PORT=5432
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres
SUPABASE_DB_PASSWORD=your-password-here

# Legacy Postgres (for local development)
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=interior_designer
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# API Keys
MINO_AI_API_KEY=your-mino-api-key
PERPLEXITY_API_KEY=your-perplexity-api-key

# Cloudflare R2 (S3-compatible storage)
R2_ACCOUNT_ID=your-r2-account-id
R2_ACCESS_KEY_ID=your-r2-access-key
R2_SECRET_ACCESS_KEY=your-r2-secret-key
R2_BUCKET_NAME=ai-interior-designer
R2_ENDPOINT=https://xxxxx.r2.cloudflarestorage.com

# Vector Database
QDRANT_HOST=localhost
QDRANT_PORT=6333

# Application URLs
BACKEND_URL=http://localhost:8000
PUBLIC_BACKEND_URL=https://api.yourdomain.com
FRONTEND_URL=http://localhost:3000
FRONTEND_PUBLIC_URL=https://your-app.vercel.app

# Production Settings
PRODUCTION=false
DEMO_MODE=false
ENVIRONMENT=development

# JWT Secret (change in production!)
JWT_SECRET=change-me-in-production

# GPU Queue
GPU_MAX_CONCURRENT=2
GPU_QUEUE_MAX_SIZE=10

# Inference Service
INFERENCE_SERVICE_URL=http://localhost:8001
INFERENCE_DEVICE=cuda

# Logging
LOG_LEVEL=INFO
EOF

echo "✅ .env template created!"
echo ""
echo "📋 Next steps:"
echo "1. Edit .env and fill in your Supabase credentials"
echo "2. Add your API keys (Mino AI, Perplexity)"
echo "3. Configure R2 storage credentials"
echo "4. Set your public URLs (after domain setup)"
echo "5. Run: ./scripts/verify-setup.sh"
