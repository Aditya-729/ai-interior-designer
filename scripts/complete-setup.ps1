# Complete automated setup - guides you through everything

Write-Host "🎯 Complete Setup Wizard" -ForegroundColor Cyan
Write-Host "=========================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Verify .env exists
Write-Host "Step 1: Checking .env file..." -ForegroundColor Yellow
if (-not (Test-Path .env)) {
    Write-Host "   Creating .env file..." -ForegroundColor Yellow
    # Create .env with your Supabase credentials
    @"
# Supabase Database
SUPABASE_DB_HOST=db.pzsdvpemnroxylbhjirr.supabase.co
SUPABASE_DB_PORT=5432
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres
SUPABASE_DB_PASSWORD=REPLACE_WITH_YOUR_ACTUAL_PASSWORD

# API Keys
MINO_AI_API_KEY=your-mino-api-key
PERPLEXITY_API_KEY=your-perplexity-api-key

# R2 Storage
R2_ACCOUNT_ID=your-r2-account-id
R2_ACCESS_KEY_ID=your-r2-access-key
R2_SECRET_ACCESS_KEY=your-r2-secret-key
R2_BUCKET_NAME=ai-interior-designer
R2_ENDPOINT=https://xxxxx.r2.cloudflarestorage.com

# Application URLs
BACKEND_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000
FRONTEND_PUBLIC_URL=https://your-app.vercel.app
PUBLIC_BACKEND_URL=https://api.yourdomain.com

# Settings
PRODUCTION=false
DEMO_MODE=false
ENVIRONMENT=development
JWT_SECRET=change-me-in-production
"@ | Out-File -FilePath ".env" -Encoding UTF8 -NoNewline
    Write-Host "   ✅ Created .env file" -ForegroundColor Green
} else {
    Write-Host "   ✅ .env file exists" -ForegroundColor Green
}

Write-Host ""
Write-Host "Step 2: Configuration Status" -ForegroundColor Yellow
Write-Host ""

# Run auto-setup check
& ".\scripts\auto-setup.ps1"

Write-Host ""
Write-Host "Step 3: Quick Actions" -ForegroundColor Yellow
Write-Host ""
Write-Host "Available commands:" -ForegroundColor Cyan
Write-Host "  • Edit .env: notepad .env" -ForegroundColor White
Write-Host "  • Check setup: .\scripts\auto-setup.ps1" -ForegroundColor White
Write-Host "  • Test Supabase: bash scripts/supabase-init.sh" -ForegroundColor White
Write-Host "  • Initialize DB: cd backend && alembic upgrade head" -ForegroundColor White

Write-Host ""
Write-Host "📚 Documentation:" -ForegroundColor Cyan
Write-Host "  • Quick Start: QUICK_START_YOUR_PROJECT.md" -ForegroundColor White
Write-Host "  • Add Password: ADD_YOUR_PASSWORD.md" -ForegroundColor White
Write-Host "  • Your Setup: YOUR_SETUP.md" -ForegroundColor White
