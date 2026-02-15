# Automated setup script for AI Interior Designer

Write-Host "🚀 Starting automated setup..." -ForegroundColor Cyan
Write-Host ""

# Check if .env exists
if (-not (Test-Path .env)) {
    Write-Host "❌ .env file not found!" -ForegroundColor Red
    Write-Host "   Please create it first or run the setup wizard." -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ .env file found" -ForegroundColor Green

# Check if password is still placeholder
$envContent = Get-Content .env -Raw
if ($envContent -match "REPLACE_WITH_YOUR_ACTUAL_PASSWORD") {
    Write-Host ""
    Write-Host "⚠️  WARNING: Database password is still a placeholder!" -ForegroundColor Red
    Write-Host "   Please edit .env and replace REPLACE_WITH_YOUR_ACTUAL_PASSWORD" -ForegroundColor Yellow
    Write-Host "   Get password from: https://supabase.com/dashboard/project/pzsdvpemnroxylbhjirr/settings/database" -ForegroundColor Blue
    Write-Host ""
    $continue = Read-Host "Continue anyway? (y/n)"
    if ($continue -ne "y" -and $continue -ne "Y") {
        Write-Host "Setup cancelled. Please add your password first." -ForegroundColor Yellow
        exit 0
    }
}

Write-Host ""
Write-Host "📋 Setup Checklist:" -ForegroundColor Cyan
Write-Host ""

# Check Supabase credentials
Write-Host "1. Checking Supabase configuration..." -ForegroundColor Yellow
$supabaseHost = (Get-Content .env | Select-String "SUPABASE_DB_HOST").ToString().Split("=")[1].Trim()
if ($supabaseHost -and $supabaseHost -ne "db.xxxxx.supabase.co") {
    Write-Host "   ✅ Supabase host configured: $supabaseHost" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  Supabase host not configured" -ForegroundColor Yellow
}

# Check API keys
Write-Host ""
Write-Host "2. Checking API keys..." -ForegroundColor Yellow
$minoKey = (Get-Content .env | Select-String "MINO_AI_API_KEY").ToString().Split("=")[1].Trim()
$perplexityKey = (Get-Content .env | Select-String "PERPLEXITY_API_KEY").ToString().Split("=")[1].Trim()

if ($minoKey -and $minoKey -ne "your-mino-api-key") {
    Write-Host "   ✅ MINO_AI_API_KEY configured" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  MINO_AI_API_KEY not configured" -ForegroundColor Yellow
}

if ($perplexityKey -and $perplexityKey -ne "your-perplexity-api-key") {
    Write-Host "   ✅ PERPLEXITY_API_KEY configured" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  PERPLEXITY_API_KEY not configured" -ForegroundColor Yellow
}

# Check R2 storage
Write-Host ""
Write-Host "3. Checking R2 storage..." -ForegroundColor Yellow
$r2Endpoint = (Get-Content .env | Select-String "R2_ENDPOINT").ToString().Split("=")[1].Trim()
if ($r2Endpoint -and $r2Endpoint -ne "https://xxxxx.r2.cloudflarestorage.com") {
    Write-Host "   ✅ R2 storage configured" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  R2 storage not configured (optional for now)" -ForegroundColor Yellow
}

# Check Vercel URL
Write-Host ""
Write-Host "4. Checking Vercel configuration..." -ForegroundColor Yellow
$vercelUrl = (Get-Content .env | Select-String "FRONTEND_PUBLIC_URL").ToString().Split("=")[1].Trim()
if ($vercelUrl -and $vercelUrl -ne "https://your-app.vercel.app") {
    Write-Host "   ✅ Vercel URL configured: $vercelUrl" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  Vercel URL not configured yet" -ForegroundColor Yellow
    Write-Host "      Get it from: https://vercel.com/dashboard" -ForegroundColor Blue
}

Write-Host ""
Write-Host "📝 Next Steps:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Add your database password to .env (if not done)" -ForegroundColor White
Write-Host "2. Add your API keys to .env" -ForegroundColor White
Write-Host "3. Get Vercel URL and add to .env" -ForegroundColor White
Write-Host "4. Test Supabase connection:" -ForegroundColor White
Write-Host "   bash scripts/supabase-init.sh" -ForegroundColor Gray
Write-Host "5. Initialize database:" -ForegroundColor White
Write-Host "   cd backend && alembic upgrade head" -ForegroundColor Gray

Write-Host ""
Write-Host "✅ Setup check complete!" -ForegroundColor Green
