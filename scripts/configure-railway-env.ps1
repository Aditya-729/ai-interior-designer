# Configure Railway Environment Variables
# This sets all required environment variables for Railway backend

Write-Host "Configuring Railway Environment Variables..." -ForegroundColor Yellow
Write-Host ""

$frontendUrl = "https://frontend-inky-eight-53.vercel.app"
$backendUrl = "https://ai-interior-designer-backend-production.up.railway.app"

Write-Host "Setting environment variables..." -ForegroundColor Cyan
Write-Host ""

# Read actual values from .env if available
$envFile = "$PSScriptRoot\..\.env"
$envVars = @{}

if (Test-Path $envFile) {
    Get-Content $envFile | ForEach-Object {
        if ($_ -match '^([^#=]+)=(.*)$') {
            $key = $matches[1].Trim()
            $value = $matches[2].Trim().Trim('"').Trim("'")
            if ($key -and $value) {
                $envVars[$key] = $value
            }
        }
    }
}

# Required variables
$varsToSet = @{
    'FRONTEND_PUBLIC_URL' = $frontendUrl
    'FRONTEND_URL' = $frontendUrl
    'BACKEND_URL' = $backendUrl
    'PUBLIC_BACKEND_URL' = $backendUrl
    'ENVIRONMENT' = 'production'
    'PRODUCTION' = 'true'
    'INFERENCE_DEVICE' = 'cpu'
    'SUPABASE_DB_HOST' = 'db.pzsdvpemnroxylbhjirr.supabase.co'
    'SUPABASE_DB_PORT' = '5432'
    'SUPABASE_DB_NAME' = 'postgres'
    'SUPABASE_DB_USER' = 'postgres'
    'SUPABASE_DB_PASSWORD' = 'cuetpassaiinterior'
    'JWT_SECRET' = if ($envVars['JWT_SECRET'] -and $envVars['JWT_SECRET'] -ne 'change-me-in-production') { $envVars['JWT_SECRET'] } else { 'prod-secret-' + (New-Guid).ToString().Substring(0, 16) }
}

# Add API keys if available
if ($envVars['MINO_AI_API_KEY'] -and $envVars['MINO_AI_API_KEY'] -ne 'your-mino-api-key') {
    $varsToSet['MINO_AI_API_KEY'] = $envVars['MINO_AI_API_KEY']
}
if ($envVars['PERPLEXITY_API_KEY'] -and $envVars['PERPLEXITY_API_KEY'] -ne 'your-perplexity-api-key') {
    $varsToSet['PERPLEXITY_API_KEY'] = $envVars['PERPLEXITY_API_KEY']
}
if ($envVars['R2_ACCOUNT_ID'] -and $envVars['R2_ACCOUNT_ID'] -ne 'your-r2-account-id') {
    $varsToSet['R2_ACCOUNT_ID'] = $envVars['R2_ACCOUNT_ID']
    $varsToSet['R2_ACCESS_KEY_ID'] = $envVars['R2_ACCESS_KEY_ID']
    $varsToSet['R2_SECRET_ACCESS_KEY'] = $envVars['R2_SECRET_ACCESS_KEY']
    $varsToSet['R2_ENDPOINT'] = $envVars['R2_ENDPOINT']
    $varsToSet['R2_BUCKET_NAME'] = if ($envVars['R2_BUCKET_NAME']) { $envVars['R2_BUCKET_NAME'] } else { 'ai-interior-designer' }
}

Write-Host "Variables to set:" -ForegroundColor Yellow
foreach ($key in $varsToSet.Keys) {
    Write-Host "  $key = $($varsToSet[$key])" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Please set these in Railway dashboard:" -ForegroundColor Cyan
Write-Host "  https://railway.com/project/df46718f-fd2b-48e5-94b7-8e95758397d8" -ForegroundColor Blue
Write-Host ""
Write-Host "Or use Railway CLI (after linking service):" -ForegroundColor Yellow
foreach ($key in $varsToSet.Keys) {
    $value = $varsToSet[$key]
    Write-Host "  railway variables set `"$key=$value`"" -ForegroundColor Gray
}
Write-Host ""
