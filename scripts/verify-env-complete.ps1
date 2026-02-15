# Complete .env verification script

Write-Host "🔍 Complete Environment Configuration Check" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""

$envFile = ".env"
if (-not (Test-Path $envFile)) {
    Write-Host "❌ .env file not found!" -ForegroundColor Red
    exit 1
}

$envContent = Get-Content $envFile
$allGood = $true

# Check Supabase
Write-Host "1. Supabase Database Configuration" -ForegroundColor Yellow
$supabaseHost = ($envContent | Select-String "SUPABASE_DB_HOST").ToString().Split("=")[1].Trim()
$supabasePort = ($envContent | Select-String "SUPABASE_DB_PORT").ToString().Split("=")[1].Trim()
$supabaseDb = ($envContent | Select-String "SUPABASE_DB_NAME").ToString().Split("=")[1].Trim()
$supabaseUser = ($envContent | Select-String "SUPABASE_DB_USER").ToString().Split("=")[1].Trim()
$supabasePwd = ($envContent | Select-String "SUPABASE_DB_PASSWORD").ToString().Split("=")[1].Trim()

if ($supabaseHost -and $supabaseHost -ne "db.xxxxx.supabase.co") {
    Write-Host "   ✅ Host: $supabaseHost" -ForegroundColor Green
} else {
    Write-Host "   ❌ Host not configured" -ForegroundColor Red
    $allGood = $false
}

Write-Host "   ✅ Port: $supabasePort" -ForegroundColor Green
Write-Host "   ✅ Database: $supabaseDb" -ForegroundColor Green
Write-Host "   ✅ User: $supabaseUser" -ForegroundColor Green

if ($supabasePwd -like '"*"') {
    Write-Host "   ✅ Password: [SET - properly quoted]" -ForegroundColor Green
} elseif ($supabasePwd -ne "REPLACE_WITH_YOUR_ACTUAL_PASSWORD" -and $supabasePwd -ne "") {
    if ($supabasePwd -like '*#*') {
        Write-Host "   ⚠️  Password: [SET but contains # - should be quoted]" -ForegroundColor Yellow
    } else {
        Write-Host "   ✅ Password: [SET]" -ForegroundColor Green
    }
} else {
    Write-Host "   ❌ Password: [NOT SET]" -ForegroundColor Red
    $allGood = $false
}

Write-Host ""

# Check API Keys
Write-Host "2. API Keys" -ForegroundColor Yellow
$minoKey = ($envContent | Select-String "MINO_AI_API_KEY").ToString().Split("=")[1].Trim()
$perplexityKey = ($envContent | Select-String "PERPLEXITY_API_KEY").ToString().Split("=")[1].Trim()

if ($minoKey -and $minoKey -ne "your-mino-api-key" -and $minoKey -ne "") {
    Write-Host "   ✅ MINO_AI_API_KEY: [SET]" -ForegroundColor Green
} else {
    Write-Host "   ❌ MINO_AI_API_KEY: [NOT SET]" -ForegroundColor Red
    $allGood = $false
}

if ($perplexityKey -and $perplexityKey -ne "your-perplexity-api-key" -and $perplexityKey -ne "") {
    Write-Host "   ✅ PERPLEXITY_API_KEY: [SET]" -ForegroundColor Green
} else {
    Write-Host "   ❌ PERPLEXITY_API_KEY: [NOT SET]" -ForegroundColor Red
    $allGood = $false
}

Write-Host ""

# Check R2 Storage (optional)
Write-Host "3. R2 Storage (Optional)" -ForegroundColor Yellow
$r2Endpoint = ($envContent | Select-String "R2_ENDPOINT").ToString().Split("=")[1].Trim()
if ($r2Endpoint -and $r2Endpoint -ne "https://xxxxx.r2.cloudflarestorage.com") {
    Write-Host "   ✅ R2 Storage: [CONFIGURED]" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  R2 Storage: [NOT CONFIGURED - optional]" -ForegroundColor Yellow
}

Write-Host ""

# Check Vercel URL
Write-Host "4. Vercel Configuration" -ForegroundColor Yellow
$vercelUrl = ($envContent | Select-String "FRONTEND_PUBLIC_URL").ToString().Split("=")[1].Trim()
if ($vercelUrl -and $vercelUrl -ne "https://your-app.vercel.app") {
    Write-Host "   ✅ Vercel URL: $vercelUrl" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  Vercel URL: [NOT SET - get from Vercel dashboard]" -ForegroundColor Yellow
}

Write-Host ""

# Summary
Write-Host "===========================================" -ForegroundColor Cyan
if ($allGood) {
    Write-Host "✅ All required configurations are set!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Test Supabase connection:" -ForegroundColor White
    Write-Host "     bash scripts/supabase-init.sh" -ForegroundColor Gray
    Write-Host "  2. Initialize database:" -ForegroundColor White
    Write-Host "     cd backend && alembic upgrade head" -ForegroundColor Gray
} else {
    Write-Host "⚠️  Some required configurations are missing" -ForegroundColor Yellow
    Write-Host "   Please check the items marked with ❌ above" -ForegroundColor Yellow
}
