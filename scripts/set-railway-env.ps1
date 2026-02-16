# Set Railway Environment Variables
# This script sets all required environment variables in Railway

Write-Host "Setting Railway Environment Variables..." -ForegroundColor Yellow

# Read from .env file
$envFile = "$PSScriptRoot\..\.env"
if (-not (Test-Path $envFile)) {
    Write-Host "Error: .env file not found at $envFile" -ForegroundColor Red
    exit 1
}

# Parse .env file
$envVars = @{}
Get-Content $envFile | ForEach-Object {
    if ($_ -match '^([^#=]+)=(.*)$') {
        $key = $matches[1].Trim()
        $value = $matches[2].Trim().Trim('"').Trim("'")
        if ($key -and $value -and $value -ne 'your-*-key' -and $value -notlike '*yourdomain*' -and $value -notlike '*localhost*') {
            $envVars[$key] = $value
        }
    }
}

# Required variables to set
$requiredVars = @{
    'ENVIRONMENT' = 'production'
    'PRODUCTION' = 'true'
    'INFERENCE_DEVICE' = 'cpu'
    'SUPABASE_DB_HOST' = $envVars['SUPABASE_DB_HOST']
    'SUPABASE_DB_PORT' = '5432'
    'SUPABASE_DB_NAME' = 'postgres'
    'SUPABASE_DB_USER' = 'postgres'
    'SUPABASE_DB_PASSWORD' = $envVars['SUPABASE_DB_PASSWORD']
}

# Add API keys if available
if ($envVars['MINO_AI_API_KEY']) { $requiredVars['MINO_AI_API_KEY'] = $envVars['MINO_AI_API_KEY'] }
if ($envVars['PERPLEXITY_API_KEY']) { $requiredVars['PERPLEXITY_API_KEY'] = $envVars['PERPLEXITY_API_KEY'] }
if ($envVars['R2_ACCOUNT_ID']) { $requiredVars['R2_ACCOUNT_ID'] = $envVars['R2_ACCOUNT_ID'] }
if ($envVars['R2_ACCESS_KEY_ID']) { $requiredVars['R2_ACCESS_KEY_ID'] = $envVars['R2_ACCESS_KEY_ID'] }
if ($envVars['R2_SECRET_ACCESS_KEY']) { $requiredVars['R2_SECRET_ACCESS_KEY'] = $envVars['R2_SECRET_ACCESS_KEY'] }
if ($envVars['R2_ENDPOINT']) { $requiredVars['R2_ENDPOINT'] = $envVars['R2_ENDPOINT'] }
if ($envVars['R2_BUCKET_NAME']) { $requiredVars['R2_BUCKET_NAME'] = $envVars['R2_BUCKET_NAME'] }
if ($envVars['JWT_SECRET']) { $requiredVars['JWT_SECRET'] = $envVars['JWT_SECRET'] }

Write-Host ""
Write-Host "Setting variables in Railway..." -ForegroundColor Cyan

foreach ($key in $requiredVars.Keys) {
    $value = $requiredVars[$key]
    if ($value) {
        Write-Host "  Setting $key..." -ForegroundColor Gray
        railway variables set "$key=$value" 2>&1 | Out-Null
    }
}

Write-Host ""
Write-Host "Environment variables set!" -ForegroundColor Green
Write-Host ""
Write-Host "Note: You may need to set additional variables manually in Railway dashboard:" -ForegroundColor Yellow
Write-Host "  https://railway.com/project/df46718f-fd2b-48e5-94b7-8e95758397d8" -ForegroundColor Cyan
Write-Host ""
