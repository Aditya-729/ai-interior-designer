# Create .env file from Supabase connection string

param(
    [Parameter(Mandatory=$true)]
    [string]$ConnectionString,
    
    [Parameter(Mandatory=$false)]
    [string]$Password
)

Write-Host "Creating .env file from connection string..." -ForegroundColor Cyan
Write-Host ""

# Replace [YOUR-PASSWORD] with actual password if provided
if ($Password) {
    $ConnectionString = $ConnectionString -replace "\[YOUR-PASSWORD\]", $Password
}

# Parse connection string
if ($ConnectionString -match "postgresql://([^:]+):([^@]+)@([^:]+):(\d+)/(.+)") {
    $user = $matches[1]
    $password = $matches[2]
    $dbHost = $matches[3]
    $port = $matches[4]
    $database = $matches[5]
    
    Write-Host "Extracted Credentials:" -ForegroundColor Green
    Write-Host "  Host: $dbHost" -ForegroundColor Yellow
    Write-Host "  Port: $port" -ForegroundColor Yellow
    Write-Host "  Database: $database" -ForegroundColor Yellow
    Write-Host "  User: $user" -ForegroundColor Yellow
    
    if ($password -eq "[YOUR-PASSWORD]") {
        Write-Host "  Password: [NEEDS TO BE REPLACED]" -ForegroundColor Red
        Write-Host ""
        Write-Host "⚠️  You need to replace [YOUR-PASSWORD] with your actual database password!" -ForegroundColor Red
        Write-Host "   Get it from: Supabase Dashboard -> Settings -> Database -> Database password" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Creating .env file with placeholder. Please edit it to add your password." -ForegroundColor Yellow
    } else {
        Write-Host "  Password: [SET]" -ForegroundColor Green
    }
    
    # Read existing .env.example or create new
    $envContent = @"
# ============================================
# AI Interior Designer - Environment Variables
# ============================================

# Supabase Database
SUPABASE_DB_HOST=$dbHost
SUPABASE_DB_PORT=$port
SUPABASE_DB_NAME=$database
SUPABASE_DB_USER=$user
SUPABASE_DB_PASSWORD=$password

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
"@
    
    $envContent | Out-File -FilePath ".env" -Encoding UTF8 -NoNewline
    
    Write-Host ""
    Write-Host "✅ Created .env file!" -ForegroundColor Green
    Write-Host ""
    
    if ($password -eq "[YOUR-PASSWORD]") {
        Write-Host "⚠️  IMPORTANT: Edit .env and replace REPLACE_WITH_YOUR_ACTUAL_PASSWORD with your real password" -ForegroundColor Red
        Write-Host "   Location: Supabase Dashboard -> Settings -> Database -> Database password" -ForegroundColor Yellow
    } else {
        Write-Host "✅ All credentials set!" -ForegroundColor Green
    }
    
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "1. Edit .env and add your API keys (MINO_AI_API_KEY, PERPLEXITY_API_KEY)" -ForegroundColor White
    Write-Host "2. Add R2 storage credentials (if using)" -ForegroundColor White
    Write-Host "3. Test connection: bash scripts/supabase-init.sh" -ForegroundColor White
    
} else {
    Write-Host "Error: Invalid connection string format" -ForegroundColor Red
    Write-Host "Expected format: postgresql://user:password@host:port/database" -ForegroundColor Yellow
    exit 1
}
