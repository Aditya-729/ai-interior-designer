# Quick Railway Deployment - Interactive Script
Write-Host " Railway Quick Deploy" -ForegroundColor Cyan
Write-Host ""

Write-Host "Step 1: Login to Railway" -ForegroundColor Yellow
Write-Host "This will show you a URL to visit in your browser..." -ForegroundColor Gray
railway login --browserless

if ($LASTEXITCODE -ne 0) {
    Write-Host " Login failed. Please try again." -ForegroundColor Red
    exit 1
}

Write-Host " Logged in!" -ForegroundColor Green
Write-Host ""

Set-Location "$PSScriptRoot\..\backend"
Write-Host " Changed to backend directory" -ForegroundColor Gray
Write-Host ""

Write-Host "Step 2: Linking Railway project" -ForegroundColor Yellow
Write-Host "If this is your first time, Railway will create a new project." -ForegroundColor Gray
Write-Host ""

railway link

if ($LASTEXITCODE -ne 0) {
    Write-Host "  Project linking had issues. Continuing anyway..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Step 3: Configuring service..." -ForegroundColor Yellow
railway service --help 2>&1 | Out-Null

Write-Host ""
Write-Host "  IMPORTANT: Set Environment Variables" -ForegroundColor Yellow
Write-Host ""
Write-Host "Before deploying, you need to set environment variables:" -ForegroundColor White
Write-Host ""
Write-Host "Option 1: Via Railway Dashboard (Easier)" -ForegroundColor Cyan
Write-Host "1. Go to: https://railway.app/dashboard" -ForegroundColor White
Write-Host "2. Click on your project" -ForegroundColor White
Write-Host "3. Go to 'Variables' tab" -ForegroundColor White
Write-Host "4. Add all variables from your .env file" -ForegroundColor White
Write-Host ""
Write-Host "Required variables:" -ForegroundColor Yellow
Write-Host "  MINO_AI_API_KEY, PERPLEXITY_API_KEY" -ForegroundColor Gray
Write-Host "  R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY" -ForegroundColor Gray
Write-Host "  R2_BUCKET_NAME=ai-interior-designer, R2_ENDPOINT" -ForegroundColor Gray
Write-Host "  SUPABASE_DB_HOST, SUPABASE_DB_PORT=5432" -ForegroundColor Gray
Write-Host "  SUPABASE_DB_NAME=postgres, SUPABASE_DB_USER=postgres" -ForegroundColor Gray
Write-Host "  SUPABASE_DB_PASSWORD, JWT_SECRET" -ForegroundColor Gray
Write-Host "  ENVIRONMENT=production, PRODUCTION=true" -ForegroundColor Gray
Write-Host "  INFERENCE_DEVICE=cpu" -ForegroundColor Gray
Write-Host ""

$ready = Read-Host "Have you set all environment variables? (y/n)"

if ($ready -ne "y" -and $ready -ne "Y") {
    Write-Host ""
    Write-Host "Please set the variables first, then run this script again." -ForegroundColor Yellow
    Write-Host "You can set them via Railway dashboard or CLI." -ForegroundColor Gray
    exit 0
}

Write-Host ""
Write-Host "Step 4: Deploying to Railway..." -ForegroundColor Yellow
Write-Host "This will take 2-5 minutes..." -ForegroundColor Gray
Write-Host ""

railway up
$deployExitCode = $LASTEXITCODE

if ($deployExitCode -ne 0) {
    Write-Host ""
    Write-Host " Deployment failed. Check Railway dashboard for logs." -ForegroundColor Red
    Write-Host "   https://railway.app/dashboard" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Script completed!" -ForegroundColor Green
    exit 0
}

Write-Host ""
Write-Host " Deployment successful!" -ForegroundColor Green
Write-Host ""

Write-Host "Getting your backend URL..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

$railwayUrl = railway domain 2>&1
$actualUrl = $null

if ($railwayUrl -and $railwayUrl -notlike "*error*" -and $railwayUrl -notlike "*not found*" -and $railwayUrl -notlike "*No linked*") {
    $actualUrl = ($railwayUrl | Select-String -Pattern "https?://[^\s]+" | ForEach-Object { $_.Matches.Value }) | Select-Object -First 1
}

Write-Host ""
Write-Host " Deployment complete!" -ForegroundColor Green
Write-Host ""

if ($null -ne $actualUrl) {
    Write-Host "Your backend is live!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Backend URL: $actualUrl" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Next Steps:" -ForegroundColor Yellow
    Write-Host "1. Test your backend: $actualUrl/api/v1/system/health" -ForegroundColor White
    Write-Host ""
    Write-Host "2. Update Vercel environment variables:" -ForegroundColor White
    $wsUrl = $actualUrl -replace 'https://', 'wss://' -replace 'http://', 'ws://'
    Write-Host "   NEXT_PUBLIC_API_BASE = $actualUrl" -ForegroundColor Gray
    Write-Host "   NEXT_PUBLIC_WS_URL = $wsUrl" -ForegroundColor Gray
    Write-Host ""
    Write-Host "3. Redeploy Vercel" -ForegroundColor White
    Write-Host ""
}

if (-not $actualUrl) {
    Write-Host "Next Steps:" -ForegroundColor Yellow
    Write-Host "1. Get your backend URL from Railway dashboard:" -ForegroundColor White
    Write-Host "   https://railway.app/dashboard" -ForegroundColor Cyan
    Write-Host "   Your Project -> Settings -> Domains" -ForegroundColor Gray
    Write-Host ""
    Write-Host "2. Update Vercel environment variables:" -ForegroundColor White
    Write-Host "   NEXT_PUBLIC_API_BASE = https://your-app.railway.app" -ForegroundColor Gray
    Write-Host "   NEXT_PUBLIC_WS_URL = wss://your-app.railway.app" -ForegroundColor Gray
    Write-Host "   (Replace with your actual Railway URL)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "3. Redeploy Vercel" -ForegroundColor White
    Write-Host ""
}

Write-Host "Script completed!" -ForegroundColor Green
