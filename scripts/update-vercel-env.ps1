# Update Vercel Environment Variables
param(
    [string]$RailwayUrl = "https://ai-interior-designer-backend-production.up.railway.app"
)

Write-Host "Updating Vercel Environment Variables..." -ForegroundColor Yellow
Write-Host ""

$wsUrl = $RailwayUrl -replace 'https://', 'wss://'

Write-Host "Setting NEXT_PUBLIC_API_BASE = $RailwayUrl" -ForegroundColor Cyan
Write-Host "Setting NEXT_PUBLIC_WS_URL = $wsUrl" -ForegroundColor Cyan
Write-Host ""

Write-Host "Please set these in Vercel dashboard:" -ForegroundColor Yellow
Write-Host "1. Go to: https://vercel.com/dashboard" -ForegroundColor White
Write-Host "2. Select project: adityas-projects-e275b3df/frontend" -ForegroundColor White
Write-Host "3. Go to Settings -> Environment Variables" -ForegroundColor White
Write-Host "4. Add:" -ForegroundColor White
Write-Host "   NEXT_PUBLIC_API_BASE = $RailwayUrl" -ForegroundColor Gray
Write-Host "   NEXT_PUBLIC_WS_URL = $wsUrl" -ForegroundColor Gray
Write-Host "5. Redeploy" -ForegroundColor White
Write-Host ""

Write-Host "Or use Vercel CLI interactively:" -ForegroundColor Yellow
Write-Host "  cd frontend" -ForegroundColor Gray
Write-Host "  vercel env add NEXT_PUBLIC_API_BASE production" -ForegroundColor Gray
Write-Host "  (Enter: $RailwayUrl)" -ForegroundColor Gray
Write-Host "  vercel env add NEXT_PUBLIC_WS_URL production" -ForegroundColor Gray
Write-Host "  (Enter: $wsUrl)" -ForegroundColor Gray
Write-Host "  vercel --prod" -ForegroundColor Gray
Write-Host ""
