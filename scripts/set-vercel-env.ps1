# Set Vercel Environment Variables
# This script helps you set the required environment variables for your Vercel deployment

Write-Host "Setting Vercel Environment Variables" -ForegroundColor Yellow
Write-Host ""

# Get backend API URL
$apiBase = Read-Host "Enter your backend API URL (e.g., https://api.yourdomain.com or http://localhost:8000 for testing)"

if ([string]::IsNullOrWhiteSpace($apiBase)) {
    Write-Host "⚠️  No API URL provided. Using placeholder." -ForegroundColor Yellow
    $apiBase = "https://api.yourdomain.com"
}

# Determine WebSocket URL
if ($apiBase -like "https://*") {
    $wsUrl = $apiBase -replace "https://", "wss://"
} elseif ($apiBase -like "http://*") {
    $wsUrl = $apiBase -replace "http://", "ws://"
} else {
    $wsUrl = "wss://$apiBase"
}

Write-Host ""
Write-Host "Setting environment variables:" -ForegroundColor Cyan
Write-Host "  NEXT_PUBLIC_API_BASE = $apiBase" -ForegroundColor Gray
Write-Host "  NEXT_PUBLIC_WS_URL = $wsUrl" -ForegroundColor Gray
Write-Host ""

# Change to frontend directory
Set-Location "$PSScriptRoot\..\frontend"

# Set environment variables for production
Write-Host "Setting for Production environment..." -ForegroundColor Yellow
vercel env add NEXT_PUBLIC_API_BASE production <<< $apiBase
vercel env add NEXT_PUBLIC_WS_URL production <<< $wsUrl

Write-Host ""
Write-Host "✅ Environment variables set!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Redeploy your Vercel project:" -ForegroundColor White
Write-Host "   cd frontend" -ForegroundColor Gray
Write-Host "   vercel --prod" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Or trigger a new deployment by pushing to GitHub" -ForegroundColor White
Write-Host ""
