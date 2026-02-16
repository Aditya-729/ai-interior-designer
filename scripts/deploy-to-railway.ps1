# Deploy Backend to Railway - Automated Script
# This script will help you deploy your backend to Railway

Write-Host "🚂 Railway Deployment Script" -ForegroundColor Cyan
Write-Host ""

# Check if Railway CLI is installed
$railwayInstalled = Get-Command railway -ErrorAction SilentlyContinue

if (-not $railwayInstalled) {
    Write-Host "⚠️  Railway CLI not found!" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Installing Railway CLI..." -ForegroundColor Yellow
    
    # Try npm first
    $npmInstalled = Get-Command npm -ErrorAction SilentlyContinue
    if ($npmInstalled) {
        Write-Host "Installing via npm..." -ForegroundColor Gray
        npm install -g @railway/cli
    } else {
        Write-Host ""
        Write-Host "Please install Railway CLI manually:" -ForegroundColor Yellow
        Write-Host "1. Go to: https://railway.app/cli" -ForegroundColor White
        Write-Host "2. Download and install Railway CLI" -ForegroundColor White
        Write-Host "3. Or install via npm: npm install -g @railway/cli" -ForegroundColor White
        Write-Host ""
        $continue = Read-Host "Press Enter after installing Railway CLI, or type 'skip' to continue"
        if ($continue -eq "skip") {
            Write-Host "Skipping Railway CLI check..." -ForegroundColor Yellow
        }
    }
}

# Verify Railway CLI
$railwayInstalled = Get-Command railway -ErrorAction SilentlyContinue
if (-not $railwayInstalled) {
    Write-Host "❌ Railway CLI still not found. Please install it first." -ForegroundColor Red
    exit 1
}

Write-Host "✅ Railway CLI found!" -ForegroundColor Green
Write-Host ""

# Change to backend directory
Set-Location "$PSScriptRoot\..\backend"

Write-Host "📁 Current directory: $(Get-Location)" -ForegroundColor Gray
Write-Host ""

# Check if user is logged in
Write-Host "Checking Railway authentication..." -ForegroundColor Yellow
$authCheck = railway whoami 2>&1

if ($authCheck -like "*not logged in*" -or $authCheck -like "*error*") {
    Write-Host "⚠️  Not logged in to Railway" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please log in to Railway:" -ForegroundColor Cyan
    Write-Host "1. This will open your browser" -ForegroundColor White
    Write-Host "2. Authorize Railway CLI" -ForegroundColor White
    Write-Host ""
    $proceed = Read-Host "Press Enter to open Railway login (or type 'skip' to login manually later)"
    
    if ($proceed -ne "skip") {
        railway login
    } else {
        Write-Host "Please run 'railway login' manually, then run this script again." -ForegroundColor Yellow
        exit 0
    }
} else {
    Write-Host "✅ Logged in to Railway as: $authCheck" -ForegroundColor Green
}

Write-Host ""
Write-Host "🚀 Starting Railway deployment..." -ForegroundColor Cyan
Write-Host ""

# Check if project exists
Write-Host "Checking for existing Railway project..." -ForegroundColor Yellow
$projectCheck = railway status 2>&1

if ($projectCheck -like "*not linked*" -or $projectCheck -like "*error*") {
    Write-Host "No Railway project linked. Creating new project..." -ForegroundColor Yellow
    Write-Host ""
    
    # Link to GitHub repo
    Write-Host "Linking to GitHub repository..." -ForegroundColor Yellow
    Write-Host "This will create a new Railway project from your GitHub repo." -ForegroundColor Gray
    Write-Host ""
    
    railway link
    
    Write-Host ""
    Write-Host "✅ Project linked!" -ForegroundColor Green
} else {
    Write-Host "✅ Project already linked!" -ForegroundColor Green
}

Write-Host ""
Write-Host "📝 Setting up Railway configuration..." -ForegroundColor Yellow

# Railway will auto-detect Python and use Procfile/runtime.txt
Write-Host "✅ Configuration files ready:" -ForegroundColor Green
Write-Host "  - Procfile (start command)" -ForegroundColor Gray
Write-Host "  - runtime.txt (Python version)" -ForegroundColor Gray
Write-Host "  - railway.json (Railway config)" -ForegroundColor Gray

Write-Host ""
Write-Host "⚠️  IMPORTANT: Environment Variables" -ForegroundColor Yellow
Write-Host ""
Write-Host "You need to set environment variables in Railway:" -ForegroundColor White
Write-Host "1. Go to: https://railway.app/dashboard" -ForegroundColor Cyan
Write-Host "2. Click on your project" -ForegroundColor White
Write-Host "3. Go to 'Variables' tab" -ForegroundColor White
Write-Host "4. Add all variables from your .env file" -ForegroundColor White
Write-Host ""
Write-Host "Required variables:" -ForegroundColor Cyan
Write-Host "  - MINO_AI_API_KEY" -ForegroundColor Gray
Write-Host "  - PERPLEXITY_API_KEY" -ForegroundColor Gray
Write-Host "  - R2_ACCOUNT_ID" -ForegroundColor Gray
Write-Host "  - R2_ACCESS_KEY_ID" -ForegroundColor Gray
Write-Host "  - R2_SECRET_ACCESS_KEY" -ForegroundColor Gray
Write-Host "  - R2_BUCKET_NAME" -ForegroundColor Gray
Write-Host "  - R2_ENDPOINT" -ForegroundColor Gray
Write-Host "  - SUPABASE_DB_HOST" -ForegroundColor Gray
Write-Host "  - SUPABASE_DB_PORT" -ForegroundColor Gray
Write-Host "  - SUPABASE_DB_NAME" -ForegroundColor Gray
Write-Host "  - SUPABASE_DB_USER" -ForegroundColor Gray
Write-Host "  - SUPABASE_DB_PASSWORD" -ForegroundColor Gray
Write-Host "  - JWT_SECRET" -ForegroundColor Gray
Write-Host "  - ENVIRONMENT=production" -ForegroundColor Gray
Write-Host "  - PRODUCTION=true" -ForegroundColor Gray
Write-Host "  - INFERENCE_DEVICE=cpu" -ForegroundColor Gray
Write-Host ""

# Set root directory (if needed)
Write-Host "Setting root directory to 'backend'..." -ForegroundColor Yellow
railway variables set RAILWAY_SERVICE_ROOT=backend 2>&1 | Out-Null

Write-Host ""
$proceed = Read-Host "Have you set all environment variables in Railway dashboard? (y/n)"

if ($proceed -ne "y" -and $proceed -ne "Y") {
    Write-Host ""
    Write-Host "Please set the environment variables first:" -ForegroundColor Yellow
    Write-Host "1. Go to Railway dashboard" -ForegroundColor White
    Write-Host "2. Add all variables" -ForegroundColor White
    Write-Host "3. Run this script again" -ForegroundColor White
    Write-Host ""
    exit 0
}

Write-Host ""
Write-Host "🚀 Deploying to Railway..." -ForegroundColor Cyan
Write-Host "This may take 2-5 minutes..." -ForegroundColor Gray
Write-Host ""

# Deploy
railway up

Write-Host ""
Write-Host "✅ Deployment initiated!" -ForegroundColor Green
Write-Host ""

# Get deployment URL
Write-Host "Getting deployment URL..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

$url = railway domain 2>&1
if ($url -and $url -notlike "*error*" -and $url -notlike "*not found*") {
    Write-Host ""
    Write-Host "🎉 Deployment successful!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Your backend is available at:" -ForegroundColor Cyan
    Write-Host "  $url" -ForegroundColor White
    Write-Host ""
    Write-Host "📋 Next steps:" -ForegroundColor Yellow
    Write-Host "1. Test your backend: $url/api/v1/system/health" -ForegroundColor White
    Write-Host "2. Update Vercel environment variables:" -ForegroundColor White
    Write-Host "   NEXT_PUBLIC_API_BASE = $url" -ForegroundColor Gray
    Write-Host "   NEXT_PUBLIC_WS_URL = $($url -replace 'https://', 'wss://')" -ForegroundColor Gray
    Write-Host "3. Redeploy Vercel" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "⚠️  Could not get URL automatically" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please check Railway dashboard:" -ForegroundColor White
    Write-Host "1. Go to: https://railway.app/dashboard" -ForegroundColor Cyan
    Write-Host "2. Click on your project" -ForegroundColor White
    Write-Host "3. Go to 'Settings' → 'Domains'" -ForegroundColor White
    Write-Host "4. Copy your Railway URL" -ForegroundColor White
    Write-Host ""
}

Write-Host "✅ Script completed!" -ForegroundColor Green
Write-Host ""
