# Configure project with your Supabase and Vercel IDs

Write-Host "Configuring with your project IDs..." -ForegroundColor Cyan
Write-Host ""

# Supabase Organization
$SUPABASE_ORG = "vqdppqslarmzzgmyixsw"
$SUPABASE_URL = "https://supabase.com/dashboard/org/$SUPABASE_ORG"

# Vercel Project ID
$VERCEL_PROJECT_ID = "k6KjI0PFMQvhpMDtmzlZK9ca"

Write-Host "Your Project Information:" -ForegroundColor Yellow
Write-Host "   Supabase Org: $SUPABASE_ORG"
Write-Host "   Vercel Project ID: $VERCEL_PROJECT_ID"
Write-Host ""

# Check if .env exists
if (-not (Test-Path .env)) {
    Write-Host ".env file not found. Please create it manually." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Get Supabase Database Credentials:" -ForegroundColor Yellow
Write-Host "   Go to: $SUPABASE_URL" -ForegroundColor White
Write-Host "   Click on your project" -ForegroundColor White
Write-Host "   Settings -> Database -> Connection string (URI)" -ForegroundColor White
Write-Host ""
Write-Host "2. Get Vercel Project URL:" -ForegroundColor Yellow
Write-Host "   Go to: https://vercel.com/dashboard" -ForegroundColor White
Write-Host "   Find project ID: $VERCEL_PROJECT_ID" -ForegroundColor White
Write-Host ""
Write-Host "3. Update .env file with credentials" -ForegroundColor Yellow
Write-Host ""

# Create a quick reference file
$content = @"
# Your Project IDs - Keep for Reference

## Supabase
Organization: $SUPABASE_ORG
Dashboard: $SUPABASE_URL
Projects: $SUPABASE_URL/projects

## Vercel
Project ID: $VERCEL_PROJECT_ID
Dashboard: https://vercel.com/dashboard

## Next Steps
1. Get Supabase database credentials (see scripts/get-supabase-credentials.md)
2. Get Vercel project URL (see scripts/get-vercel-credentials.md)
3. Update .env file
4. Run: ./scripts/verify-setup.sh
"@

$content | Out-File -FilePath "YOUR_PROJECT_IDS.txt" -Encoding UTF8

Write-Host "Created YOUR_PROJECT_IDS.txt for quick reference" -ForegroundColor Green
Write-Host ""
Write-Host "Detailed guides:" -ForegroundColor Cyan
Write-Host "   - Supabase: scripts/get-supabase-credentials.md" -ForegroundColor White
Write-Host "   - Vercel: scripts/get-vercel-credentials.md" -ForegroundColor White
Write-Host "   - Complete Setup: YOUR_SETUP.md" -ForegroundColor White
